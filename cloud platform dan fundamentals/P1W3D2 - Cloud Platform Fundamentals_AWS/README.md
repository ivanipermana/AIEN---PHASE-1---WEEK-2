# Hands-on Cloud Platform Fundamentals — 60 menit

## Skenario dan tujuan
Anda menjadi data engineer toko online. Simpan 60 transaksi ke S3 lokal, jalankan Python untuk menghitung penjualan per kategori, simpan hasil ke S3, lalu bersihkan resource lab.

Setelah lab, Anda dapat menggunakan enam operasi Boto3, membedakan object storage dan compute, serta menjelaskan alasan teardown dan penggunaan compute batch.

Alur: orders.csv → S3 raw/orders.csv → Python lokal → S3 processed/summary.csv.
Floci mewakili storage AWS dalam simulasi. Python lokal mewakili worker compute. Ini bukan deployment compute ke AWS.

## Sebelum kelas (di luar durasi 60 menit)
1. Pasang dan jalankan Docker Desktop. Pada Windows, gunakan terminal WSL dengan integrasi Docker aktif.
2. Pasang Python 3.11+, uv, serta VS Code/Cursor.
3. Ekstrak paket. Buka terminal di folder yang berisi lab.py dan compose.yaml.
4. Jalankan `docker compose pull` dan `uv sync` sebelum kelas, agar unduhan tidak menghabiskan waktu lab.
5. Setiap peserta menggunakan emulator sendiri. Semua command di bawah dijalankan dari folder paket.

Kode memakai endpoint 127.0.0.1:4566, region us-east-1, dan kredensial dummy test. Tidak perlu akun AWS. Gunakan terminal komputer/WSL, bukan Python di container lain.

## Rundown
| Menit | Aktivitas |
|---|---|
| 0–10 | Menjalankan emulator dan mengecek koneksi |
| 10–20 | Provision bucket, upload data, dan list objek |
| 20–35 | Membaca data dan menghasilkan ringkasan |
| 35–45 | Membaca hasil melalui proses Python baru |
| 45–55 | Eksperimen BucketNotEmpty dan teardown |
| 55–60 | Refleksi storage, compute, dan FinOps |

## 1. Setup (0–10 menit)
```bash
docker compose up -d
uv run python lab.py check
```
Checkpoint: `Koneksi S3 lokal berhasil.` Jika layanan masih memulai, ulangi check setelah beberapa detik.
Buka lab.py. Hanya isi TODO 1–6. Fungsi aggregate dan CLI sudah tersedia.

## 2. Provision dan ingest (10–20 menit)
Lengkapi TODO 1 menggunakan create_bucket. Lengkapi TODO 2 menggunakan upload_file. Lengkapi TODO 3 menggunakan list_objects_v2 dengan parameter **params yang sudah disediakan.

Gunakan nama Anda menggantikan budi di SEMUA perintah berikut.
```bash
uv run python lab.py provision --bucket aien-orders-budi
uv run python lab.py ingest --bucket aien-orders-budi
```
Checkpoint: daftar objek berisi `raw/orders.csv`. raw/ adalah prefix key, bukan direktori sistem operasi.
Hint parameter: `Bucket=bucket`, `Key=key`. upload_file memakai urutan filename, bucket, key; konversikan Path menjadi str.

## 3. Process dan simpan hasil (20–35 menit)
Lengkapi TODO 4: panggil get_object, baca response["Body"], dan decode utf-8. Tutup Body setelah membaca.
```bash
uv run python lab.py process --bucket aien-orders-budi
```
aggregate sudah menghitung quantity × unit_price dan mengelompokkan kategori. Fungsi upload yang Anda tulis dipakai lagi untuk hasilnya.
Checkpoint: hasil/summary.csv tersimpan lokal dan di key processed/summary.csv. Output mempunyai tiga kategori; order_count total adalah 60. Seluruh harga dalam rupiah.

Jalankan process sekali lagi. Apa yang terjadi pada jumlah objek? Dengan key yang sama dan versioning nonaktif, hasil ditimpa, sehingga tidak muncul file ringkasan tambahan.

## 4. Eksperimen decoupled storage–compute (35–45 menit)
Saat command process selesai, proses Python sudah berhenti. Biarkan container Floci tetap menyala.
```bash
uv run python lab.py inspect --bucket aien-orders-budi
```
Checkpoint: proses Python baru dapat membaca hasil yang disimpan oleh proses sebelumnya. Daftar objek berisi tepat raw/orders.csv dan processed/summary.csv.

Jawab: komponen mana yang menyimpan data? Komponen mana yang menghitung? Mengapa hasil masih bisa dibaca setelah proses penghitung berhenti?
Eksperimen ini menunjukkan pemisahan proses dan penyimpanan. Jangan menghentikan Floci pada tahap ini; Floci masih menyediakan akses storage.

## 5. Teardown (45–55 menit)
Lengkapi TODO 6 terlebih dahulu.
```bash
uv run python lab.py try-delete --bucket aien-orders-budi
```
Checkpoint: `BucketNotEmpty`. Ini eksperimen yang disengaja, bukan kegagalan lab.
Lengkapi TODO 5. Langkah teardown memakai list_keys, delete_one, dan delete_bucket.
```bash
uv run python lab.py teardown --bucket aien-orders-budi
```
Checkpoint: `Teardown berhasil: bucket sudah tidak ada.`
Setelah menyimpan bukti, hentikan layanan:
```bash
docker compose down
```
Bucket lab tidak mengaktifkan versioning. Pada bucket AWS dengan versioning, seluruh versi objek dan delete marker juga perlu dibersihkan. Jangan menggunakan kode teardown lab untuk bucket lain.

## 6. Refleksi FinOps (55–60 menit)
Gunakan tarif asumsi latihan, bukan harga AWS aktual:
- Compute: USD 0,05/jam.
- Storage: 10 GB × USD 0,023/GB/bulan.
- Periode: 30 hari. Abaikan request, transfer data, pajak, dan biaya resource lain.

Hitung total biaya untuk (A) compute 24 jam/hari dan (B) compute batch 1 jam/hari. Berapa selisihnya? Komponen mana tetap dibayar ketika compute berhenti?
Perhitungan ini ilustrasi, bukan tagihan Floci maupun estimasi AWS lengkap.

## Bukti yang dikumpulkan
Isi JAWABAN.md. Sertakan output ingest, process, inspect, try-delete, dan teardown. Jangan hanya mengirim screenshot kode.

## Troubleshooting
| Gejala | Langkah |
|---|---|
| Docker daemon tidak terhubung | Jalankan Docker Desktop, tunggu engine siap |
| Port 4566 sudah dipakai | Periksa layanan yang memakai port; hentikan emulator lama milik Anda |
| Koneksi Floci gagal | Jalankan docker compose ps dan docker compose logs floci, lalu ulangi check |
| NotImplementedError | Lengkapi TODO yang disebut pesan |
| NoSuchBucket / NoSuchKey | Periksa urutan langkah dan konsistensi --bucket |
| Image/package gagal diunduh | Periksa jaringan, lakukan pull dan uv sync sebelum kelas |
| BucketNotEmpty saat try-delete | Ini checkpoint yang diharapkan; lanjutkan teardown |

## Referensi
- Materi kelas: Cloud Platform Fundamentals, terutama slide 3, 13, dan 23–27.
- Floci dan konfigurasi Compose: https://github.com/floci-io/floci
- Boto3 get_object: https://docs.aws.amazon.com/boto3/latest/reference/services/s3/client/get_object.html
- Aturan DeleteBucket: https://docs.aws.amazon.com/AmazonS3/latest/API/API_DeleteBucket.html

Emulator membantu latihan API. Ia tidak membuktikan kesamaan seluruh perilaku AWS, IAM, ketahanan data, performa, atau billing. Instructor sebaiknya membekukan tag/digest image dan uv.lock sesudah rehearsal pada lingkungan kelas.
