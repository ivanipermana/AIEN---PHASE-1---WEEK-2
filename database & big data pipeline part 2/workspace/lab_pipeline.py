"""KirimKita: batch, streaming lokal, dan orkestrasi. Python 3.11+."""
import argparse
import asyncio
import json
import sqlite3
import time
from datetime import date
from pathlib import Path

# Semua path mengikuti lokasi paket, bukan folder terminal.
PACKAGE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = PACKAGE_DIR / 'data' / 'checkout_events.json'


def source_events():
    """Memuat 12 delivery: 10 event unik dan 2 pengiriman ulang identik."""
    return json.loads(DATA_PATH.read_text(encoding='utf-8'))


def clean_event(event):
    """Aturan yang sama dipakai batch dan stream. Edit di sini saat challenge."""
    if event['order_value'] <= 0:
        return None, 'NONPOSITIVE_VALUE'
    promised_days = (date.fromisoformat(event['promised_date'])
                     - date.fromisoformat(event['order_date'])).days
    if promised_days < 0:
        return None, 'PROMISE_BEFORE_ORDER'
    city = event['destination_city'].strip().upper() or 'UNKNOWN'
    return (event['order_id'], event['order_value'], city, promised_days), None


def connect(path):
    db = sqlite3.connect(path)
    db.executescript('''
    CREATE TABLE IF NOT EXISTS features(
      mode TEXT, order_id TEXT, order_value REAL, destination_city TEXT,
      promised_days INTEGER, PRIMARY KEY(mode, order_id));
    CREATE TABLE IF NOT EXISTS raw_events(
      run_id TEXT, delivery_no INTEGER, mode TEXT, payload TEXT,
      PRIMARY KEY(run_id, delivery_no));
    CREATE TABLE IF NOT EXISTS quarantine(
      mode TEXT, event_id TEXT, order_id TEXT, reason TEXT,
      PRIMARY KEY(mode, event_id));
    CREATE TABLE IF NOT EXISTS metrics(
      run_id TEXT PRIMARY KEY, mode TEXT, input_count INTEGER,
      valid_count INTEGER, rejected_count INTEGER, duplicate_count INTEGER,
      first_output_s REAL, total_s REAL, max_queue INTEGER, producer_wait_s REAL);
    ''')
    return db


class Run:
    def __init__(self, db_path, mode):
        self.db = connect(db_path)
        self.mode = mode
        self.run_id = f'{mode}-{time.time_ns()}'
        self.start = time.perf_counter()
        self.seen = {}
        self.input = self.valid = self.rejected = self.duplicates = 0
        self.first = None
        self.max_queue = 0
        self.producer_wait = 0.0

    def process(self, event):
        self.input += 1
        payload = json.dumps(event, sort_keys=True)
        with self.db:
            self.db.execute('INSERT INTO raw_events VALUES(?,?,?,?)',
                            (self.run_id, self.input, self.mode, payload))
            if event['event_id'] in self.seen:
                if self.seen[event['event_id']] != payload:
                    raise ValueError('event_id sama dengan payload berbeda: lab harus dihentikan')
                self.duplicates += 1
                print(f"SKIP duplicate {event['event_id']}", flush=True)
                return
            row, reason = clean_event(event)
            if reason:
                self.db.execute('''INSERT INTO quarantine VALUES(?,?,?,?)
                  ON CONFLICT(mode,event_id) DO UPDATE SET reason=excluded.reason''',
                  (self.mode, event['event_id'], event['order_id'], reason))
            else:
                self.db.execute('''INSERT INTO features VALUES(?,?,?,?,?)
                  ON CONFLICT(mode,order_id) DO UPDATE SET
                  order_value=excluded.order_value,
                  destination_city=excluded.destination_city,
                  promised_days=excluded.promised_days''', (self.mode, *row))
        # Status diperbarui setelah transaksi berhasil.
        self.seen[event['event_id']] = payload
        if reason:
            self.rejected += 1
            print(f"REJECT {event['order_id']} {reason}", flush=True)
        else:
            self.valid += 1
            if self.first is None:
                self.first = time.perf_counter() - self.start
            print(f"SAVE {event['order_id']} +{time.perf_counter()-self.start:.2f}s", flush=True)

    def finish(self):
        total = time.perf_counter() - self.start
        row = (self.run_id, self.mode, self.input, self.valid, self.rejected,
               self.duplicates, self.first, total, self.max_queue, self.producer_wait)
        with self.db:
            self.db.execute('INSERT INTO metrics VALUES(?,?,?,?,?,?,?,?,?,?)', row)
        print(json.dumps(dict(run_id=self.run_id, mode=self.mode, input=self.input,
                              valid=self.valid, rejected=self.rejected,
                              duplicates=self.duplicates, first_output_s=self.first,
                              total_s=round(total, 3), max_queue=self.max_queue,
                              producer_wait_s=round(self.producer_wait, 3)), indent=2))


def run_batch(args, mode='batch'):
    run = Run(args.db, mode)
    try:
        buffer = []
        for event in source_events():
            time.sleep(args.interval)
            buffer.append(event)
            print(f'COLLECT {len(buffer):02}/12', flush=True)
        print('BATCH READY: sumber selesai; transformasi dimulai', flush=True)
        for event in buffer:
            time.sleep(args.work)
            run.process(event)
        run.finish()
    finally:
        run.db.close()


async def run_stream(args):
    run = Run(args.db, 'stream')
    queue = asyncio.Queue(maxsize=args.queue_size)

    async def producer():
        for event in source_events():
            await asyncio.sleep(args.interval)
            start_put = time.perf_counter()
            await queue.put(event)
            run.producer_wait += time.perf_counter() - start_put
            run.max_queue = max(run.max_queue, queue.qsize())
            print(f"SEND {event['event_id']} queue={queue.qsize()}", flush=True)
        await queue.put(None)  # Sentinel: akhir sumber terbatas untuk kelas.

    async def consumer():
        while True:
            event = await queue.get()
            try:
                if event is None:
                    return
                await asyncio.sleep(args.work)
                run.process(event)
            finally:
                queue.task_done()

    try:
        # TaskGroup membatalkan pasangan task jika salah satunya gagal.
        async with asyncio.TaskGroup() as group:
            group.create_task(producer())
            group.create_task(consumer())
        await queue.join()
        run.finish()
    finally:
        run.db.close()


def run_orchestrated(args):
    try:
        from prefect import flow, task
    except ImportError:
        raise SystemExit('Prefect belum tersedia. Jalankan: python -m pip install "prefect>=3,<4"')
    attempts = {'save': 0}

    @task(persist_result=False, cache_policy=None)
    def extract():
        return source_events()

    @task(persist_result=False, cache_policy=None)
    def validate(events):
        for event in events:
            clean_event(event)  # Verifikasi struktur sebelum tahap tulis.
        return events

    # TODO PESERTA B: ubah jeda retry menjadi 1 detik, lalu amati log.
    @task(retries=2, retry_delay_seconds=2, persist_result=False, cache_policy=None)
    def save(events):
        attempts['save'] += 1
        if args.fail_once and attempts['save'] == 1:
            raise ConnectionError('SIMULASI gangguan sementara sebelum penulisan')
        run = Run(args.db, 'orchestrated')
        try:
            for event in events:
                run.process(event)
            run.finish()
        finally:
            run.db.close()

    @flow(name='kirimkita-batch', log_prints=True)
    def pipeline():
        save(validate(extract()))

    pipeline()
    print(f"Percobaan task save: {attempts['save']}")


def inspect_db(args):
    # TODO PESERTA A: tambahkan query HIGH_VALUE pada daftar query di bawah.
    # Tampilkan mode, order_id, dan is_high_value (1 jika order_value >= 200000).
    with connect(args.db) as db:
        for title, query in [
            ('FEATURES', 'SELECT * FROM features ORDER BY mode,order_id'),
            ('QUARANTINE', 'SELECT * FROM quarantine ORDER BY mode,event_id'),
            ('METRICS (5 run terakhir)', 'SELECT * FROM metrics ORDER BY rowid DESC LIMIT 5')]:
            print('\n' + title)
            cursor = db.execute(query)
            print(' | '.join(col[0] for col in cursor.description))
            for row in cursor:
                print(row)


def check(args):
    checks = []
    with connect(args.db) as db:
        data = {}
        for mode in ('batch', 'stream'):
            data[mode] = db.execute('''SELECT order_id,order_value,destination_city,promised_days
              FROM features WHERE mode=? ORDER BY order_id''', (mode,)).fetchall()
            checks.append((f'{mode}: features=8', len(data[mode]) == 8))
            checks.append((f'{mode}: O004 UNKNOWN', any(r[0]=='O004' and r[2]=='UNKNOWN' for r in data[mode])))
            q = db.execute('SELECT order_id,reason FROM quarantine WHERE mode=? ORDER BY order_id', (mode,)).fetchall()
            checks.append((f'{mode}: quarantine benar', q == [('O003','NONPOSITIVE_VALUE'),('O006','PROMISE_BEFORE_ORDER')]))
            m = db.execute('''SELECT input_count,valid_count,rejected_count,duplicate_count
              FROM metrics WHERE mode=? ORDER BY rowid DESC LIMIT 1''', (mode,)).fetchone()
            checks.append((f'{mode}: metrics 12/8/2/2', m == (12,8,2,2)))
            checks.append((f'{mode}: raw lengkap', db.execute('''SELECT COUNT(*) FROM raw_events
              WHERE run_id=(SELECT run_id FROM metrics WHERE mode=? ORDER BY rowid DESC LIMIT 1)''', (mode,)).fetchone()[0] == 12))
        checks.append(('Batch dan stream menghasilkan fitur identik', data['batch']==data['stream'] and len(data['batch'])>0))
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'} | {name}")
    if not all(ok for _, ok in checks):
        raise SystemExit(1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['batch','stream','orchestrate','inspect','check'])
    parser.add_argument('--db', default=str(PACKAGE_DIR / 'output' / 'kirimkita_part2.db'))
    parser.add_argument('--interval', type=float, default=0.5)
    parser.add_argument('--work', type=float, default=0.1)
    parser.add_argument('--queue-size', type=int, default=3)
    parser.add_argument('--fail-once', action='store_true')
    args = parser.parse_args()
    if args.interval < 0 or args.work < 0 or args.queue_size < 1:
        parser.error('interval/work harus >= 0; queue-size harus >= 1')
    Path(args.db).resolve().parent.mkdir(parents=True, exist_ok=True)
    print(f'Database: {Path(args.db).resolve()}', flush=True)
    if args.mode == 'batch':
        run_batch(args)
    elif args.mode == 'stream':
        asyncio.run(run_stream(args))
    elif args.mode == 'orchestrate':
        run_orchestrated(args)
    elif args.mode == 'inspect':
        inspect_db(args)
    else:
        check(args)


if __name__ == '__main__':
    main()
