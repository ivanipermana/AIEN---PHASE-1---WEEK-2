# Database and Big Data Pipeline Part 2
## Hands-on: Batch & Streaming Data Pipeline for AI


Kode baseline dapat dijalankan. Lengkapi tugas TODO A dan B pada workspace, eksperimen sesuai panduan, dan jawaban refleksi. Checkpoint target tetap tersedia untuk pemeriksaan mandiri.

Buka **readme.html** di browser untuk panduan lengkap, konsep, challenge, checkpoint, dan troubleshooting. Format panduan mengikuti Part 1 dan menggunakan kasus KirimKita.

## Mulai di sini

1. Ekstrak seluruh folder jika menerima ZIP. Jangan menjalankan file langsung dari dalam ZIP.
2. Buka folder ini di editor dan buka terminal pada folder utama.
3. Gunakan Python 3.11 atau lebih baru.
4. Buat virtual environment dan pasang requirements sebelum kelas.

macOS/Linux:
```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Windows PowerShell:
```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```
Pada Windows ganti `python` di bawah dengan `.\.venv\Scripts\python.exe`.

## Urutan praktik

```sh
python starter/check_environment.py
python workspace/lab_pipeline.py batch --interval 0.5 --work 0.1
python workspace/lab_pipeline.py orchestrate --fail-once
python workspace/lab_pipeline.py stream --interval 0.5 --work 0.1 --queue-size 3
python workspace/lab_pipeline.py inspect
python test/check_pipeline.py
```

Eksperimen backpressure:
```sh
python workspace/lab_pipeline.py stream --interval 0.1 --work 0.6 --queue-size 3 --db output/antrean.db
```

## Isi folder

- `readme.html`: panduan kelas lengkap.
- `data/checkout_events.json`: 12 delivery, termasuk dua pengiriman ulang.
- `workspace/lab_pipeline.py`: kode batch, stream, Prefect, dan inspeksi.
- `workspace/jawaban.md`: lembar jawaban yang dilengkapi peserta.
- `starter/check_environment.py`: pemeriksaan kesiapan.
- `test/check_pipeline.py`: pemeriksaan hasil batch dan stream.
- `output/`: database dan bukti hasil yang dibuat saat praktik.

## Hasil yang diharapkan

Setiap mode menghasilkan 8 fitur, 2 event ditolak, dan 2 delivery duplikat dari 12 input. Batch dan stream menghasilkan nilai fitur yang sama. Replay tidak menambah fitur, tetapi raw dan metrik bertambah untuk audit.

Data ini adalah fitur checkout siap konsumsi model, bukan prediksi model. Streaming merupakan simulasi producer–consumer dalam satu proses dengan antrean memori. Lab tidak mengklaim exactly-once atau pemulihan pesan setelah proses mati.

Prefect hanya diperlukan untuk Challenge 2. Ia dapat memulai server lokal sementara dan membutuhkan port lokal. Tidak perlu akun cloud. Dataset dan mode batch/stream dapat berjalan offline.

## Pengumpulan

Simpan script, jawaban, database output/kirimkita_part2.db, serta bukti retry dan antrean. Simpan checkpoint dengan:
```sh
python test/check_pipeline.py > output/hasil_check_NAMA.txt
```

Database Part 1 tidak diubah. Tidak ada perintah penghapusan otomatis.
