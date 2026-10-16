"""Simulasi pendidikan deterministik. Tidak membuka jaringan atau koneksi database.
Node ialah dict dalam satu proses. Daftar reachable diberikan peserta secara eksplisit.
Quorum memakai satu penulis, versi berurutan, tanpa concurrent write atau failover.
"""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import csv
import json

BASE = Path(__file__).resolve().parent

def load_products():
    return json.loads((BASE / 'data/products.json').read_text(encoding='utf-8'))

def load_traffic(filename):
    allowed = {'traffic_flash_sale.csv', 'traffic_hot_product.csv'}
    if filename not in allowed:
        raise ValueError('Pilih salah satu dataset traffic paket.')
    with (BASE / 'data' / filename).open(newline='') as f:
        return [int(row['product_id']) for row in csv.DictReader(f)]

def new_cluster():
    return {name: {'stock': 10, 'version': 0} for name in 'ABC'}

def _names(cluster, names):
    names = list(names)
    if not names or len(names) != len(set(names)) or any(n not in cluster for n in names):
        raise ValueError('Nama node harus unik, dikenal, dan tidak kosong.')
    return names

def leader_write(cluster, stock, reachable=('A', 'B')):
    names = _names(cluster, reachable)
    if 'A' not in names or len(names) < 2:
        return {'status': 'DITOLAK', 'reason': 'Primary A membutuhkan mayoritas 2 dari 3.'}
    version = cluster['A']['version'] + 1
    for name in names:
        cluster[name] = {'stock': stock, 'version': version}
    return {'status': 'OK', 'stock': stock, 'ack': names}

def replica_read(cluster, node='C', policy='serve_local', reachable=('C',)):
    names = _names(cluster, reachable)
    if node not in names:
        raise ValueError('Node tujuan harus dapat dijangkau.')
    if policy not in ('serve_local', 'require_majority'):
        raise ValueError('Policy tidak dikenal.')
    # Model sederhana: pembaca hanya mengizinkan hasil terbaru lewat sisi mayoritas
    # yang memiliki primary A. Ini kebijakan lab, bukan implementasi linearizable read.
    if policy == 'require_majority':
        if 'A' not in names or len(names) < 2:
            return {'status': 'DITOLAK', 'reason': 'Tidak dapat memverifikasi versi lewat primary dan mayoritas.'}
        return {'status': 'OK', **deepcopy(cluster['A'])}
    return {'status': 'OK', **deepcopy(cluster[node])}

def sync_from_primary(cluster):
    for name in cluster:
        cluster[name] = deepcopy(cluster['A'])
    return deepcopy(cluster)

def range_shard(product_id):
    if not 1 <= product_id <= 30:
        raise ValueError('Range lab hanya untuk product_id 1..30.')
    return (product_id - 1) // 10

def hash_shard(product_id):
    # Fungsi hash sederhana untuk ID integer, bukan consistent hashing.
    return product_id % 3

def shard_load(product_ids, strategy):
    counts = Counter(strategy(i) for i in product_ids)
    return {f'shard_{i}': counts[i] for i in range(3)}

def show_load(label, loads):
    print(label)
    for shard, count in loads.items():
        print(f'  {shard}: {count:3d} ' + '#' * (count // 2))
    total = sum(loads.values())
    print(f'  Total: {total}; beban terbesar: {max(loads.values()) / total:.1%}' if total else '  Tidak ada request')

def quorum_write(cluster, stock, W, reachable):
    names = _names(cluster, reachable)
    if not isinstance(W, int) or not 1 <= W <= len(cluster):
        raise ValueError('W harus integer 1..N.')
    if len(names) < W:
        return {'status': 'DITOLAK', 'reason': f'Hanya {len(names)} node, perlu W={W}.'}
    # Satu penulis logis dengan urutan versi global untuk kebutuhan eksperimen.
    version = max(row['version'] for row in cluster.values()) + 1
    for name in names:
        cluster[name] = {'stock': stock, 'version': version}
    return {'status': 'OK', 'ack': names, 'version': version}

def quorum_read(cluster, R, reachable):
    names = _names(cluster, reachable)
    if not isinstance(R, int) or not 1 <= R <= len(cluster):
        raise ValueError('R harus integer 1..N.')
    if len(names) < R:
        return {'status': 'DITOLAK', 'reason': f'Hanya {len(names)} node, perlu R={R}.'}
    respondents = names[:R]
    newest = max((cluster[n] for n in respondents), key=lambda row: row['version'])
    return {'status': 'OK', 'respondents': respondents, **deepcopy(newest)}

if __name__ == '__main__':
    print('Simulator siap. Produk:', len(load_products()))
    c = new_cluster()
    print('Write A-B:', leader_write(c, 7))
    print('Read C:', replica_read(c))
    for filename in ('traffic_flash_sale.csv', 'traffic_hot_product.csv'):
        for label, fn in [('range', range_shard), ('hash', hash_shard)]:
            show_load(filename + ' / ' + label, shard_load(load_traffic(filename), fn))
