# Analytics and Data Storytelling for AI Solutions
## Hands-on: Evaluasi Chatbot Customer Service

**Applied AI Engineer Bootcamp**  
**Topik:** metrik keberhasilan AI, dashboard evaluasi, dan komunikasi insight  
**Tools:** Python, Pandas, Matplotlib, Jupyter atau Google Colab  
**Challenge:** 40 menit. Setup sebelum kelas, demo terpandu sebelum challenge.

Selamat datang di praktikum Analytics & Data Storytelling for AI Solutions.

Tim layanan pelanggan toko fiktif **KirimKita** sedang membandingkan dua versi chatbot. Tim ingin memilih kandidat untuk **uji coba terbatas**, dengan mempertimbangkan kualitas jawaban, penyelesaian masalah, waktu respons, serta biaya pemrosesan.

Anda akan membaca data evaluasi, menghitung metrik, membuat dashboard, lalu menyampaikan rekomendasi kepada stakeholder. Seluruh data bersifat sintetis. Anda tidak perlu membangun chatbot atau mengakses API berbayar untuk mengerjakan latihan ini.

Mulai dari [Mulai_Di_Sini.html](Mulai_Di_Sini.html) untuk panduan menjalankan setiap file. Versi teks tersedia di [Mulai_Di_Sini.md](Mulai_Di_Sini.md).

## Tujuan Pembelajaran

Setelah menyelesaikan praktikum, Anda mampu:

1. **Menghubungkan keputusan bisnis dengan metrik:** memilih indikator kualitas, operasional, dan penyelesaian masalah.
2. **Membaca kontrak data:** menjelaskan grain, key unik, label, dan denominator.
3. **Menghitung metrik evaluasi:** pass rate, resolution rate, median, P95, dan rata-rata biaya.
4. **Membangun dashboard sederhana:** membandingkan versi dan kategori dengan label serta satuan yang jelas.
5. **Mengomunikasikan insight:** menyampaikan temuan, trade-off, rekomendasi bersyarat, dan keterbatasan.

## Pengaturan Environment & Tools

Pilih **satu jalur** berikut. Hasil belajar dan dataset sama.

| Jalur | Kapan digunakan | Persiapan |
|---|---|---|
| Google Colab | Peserta belum mempunyai environment Python lokal | Buka notebook peserta|
| Jupyter lokal | Python kelas sudah tersedia | Ekstrak ZIP, instal requirements di virtual environment, buka notebook. |
| Streamlit lokal, opsional | Ingin menampilkan hasil sebagai aplikasi dashboard | Selesaikan notebook dahulu, lalu jalankan starter/dashboard.py. |

**Prasyarat:** dasar Python, pemahaman tabel/CSV, persentase, dan rata-rata. Pengetahuan Pandas dapat diperkenalkan melalui demo kecil.

**Pembagian waktu:** setup 15–30 menit sebelum kelas, demo terpandu sekitar 10 menit dalam segmen pengajaran, challenge 40 menit, dan pembahasan mengikuti rundown PPT. Instalasi tidak dihitung sebagai waktu challenge.

### Jalur lokal

Gunakan Python 3.11 atau lebih baru. Jalankan perintah dari folder root paket, yaitu folder yang berisi `readme.md`, `data`, dan `workspace`.

Windows:

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe initial/setup.py
.venv\Scripts\python.exe -m jupyter lab
```

macOS/Linux:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python initial/setup.py
.venv/bin/python -m jupyter lab
```

Perintah memakai interpreter virtual environment secara langsung sehingga aktivasi shell tidak diperlukan. Setelah Jupyter terbuka, pilih `workspace/analisis.ipynb`.

### Jalur Colab

1. Ekstrak ZIP di komputer untuk mengambil `workspace/analisis.ipynb`.
2. Buka [Google Colab](https://colab.research.google.com/) dan unggah notebook tersebut.
3. Jalankan sel persiapan dalam notebook yang sama. 
4. Sel persiapan mengekstrak struktur folder dalam runtime dan menentukan `ROOT`.
5. Jalankan sel import dan pemeriksaan data, lalu lanjutkan challenge.

Gunakan satu paket per runtime. File dalam runtime Colab dapat hilang ketika sesi berakhir. Unduh notebook dan hasil sebelum menutupnya. Jalur Colab menghasilkan dashboard dalam notebook; aplikasi Streamlit opsional dijalankan secara lokal.

## Hands-On-Lab

### Langkah 1: Pemeriksaan environment

Jalur lokal menjalankan `initial/setup.py`. Script membuat folder output jika belum ada, memeriksa import package, lalu memeriksa kontrak dataset. Jalur Colab melakukan persiapan dan pemeriksaan yang setara melalui sel awal notebook.

`initial/setup.py` aman dijalankan ulang untuk latihan ini: script tidak mengubah dataset dan tidak menimpa jawaban. Mengulang sel ekspor dalam notebook memperbarui file hasil dengan nama yang sama di `output`.

### Langkah 2: Pemeriksaan sumber

Pemeriksaan sumber tersedia di `starter/check_data.py`. Pemeriksaan ini tidak menghitung solusi challenge.

| Pemeriksaan | Kondisi sumber |
|---|---:|
| Jumlah baris evaluasi | 400 |
| question_id unik | 200 |
| Versi chatbot | A dan B |
| Kasus per versi | 200 |
| Kategori | 4 |
| Kasus per kategori per versi | 50 |
| Duplikat pasangan question_id dan model_version | 0 |

Dataset bersih agar latihan berfokus pada analisis. Tugas Anda tetap mencakup membaca hasil pemeriksaan dan menjelaskan mengapa pemeriksaan tersebut diperlukan.

### Langkah 3: Demo terpandu

Buka `starter/demo.ipynb` bersama instruktur. Demo memakai empat baris terpisah dari dataset challenge dan menjelaskan:

- `groupby()` untuk membentuk kelompok.
- `agg()` untuk menghitung beberapa metrik.
- `mean()` pada label 0/1 untuk mendapatkan proporsi.
- Pemilihan baris gagal melalui kondisi boolean.

Setelah demo, buka kembali `workspace/analisis.ipynb` untuk challenge utama. Variabel dari notebook demo tidak otomatis tersedia pada notebook lain.

### Langkah 4: Cara mengerjakan notebook

1. Buka panduan ini berdampingan dengan notebook.
2. Jalankan sel persiapan dan import terlebih dahulu.
3. Lengkapi bagian bertanda `...`, `__PIVOT__`, dan `NotImplementedError`.
4. Jalankan satu sel dengan **Shift+Enter**. Tunggu sampai selesai sebelum menjalankan sel yang bergantung padanya.
5. Bila mengubah fungsi, jalankan ulang sel fungsi dan seluruh sel turunannya.
6. Catat interpretasi di `workspace/jawaban.md`. File tersebut dapat diedit dengan editor teks.

`NotImplementedError` adalah penanda tugas yang belum dikerjakan. Jangan menjalankan semua sel template sebelum mengisinya. Setelah seluruh tugas selesai, jalankan ulang dari awal untuk memeriksa ketergantungan variabel.

### Troubleshooting Isu Umum

| Gejala | Penyebab yang mungkin | Perbaikan |
|---|---|---|
| ModuleNotFoundError | Package belum ada pada kernel aktif | Gunakan interpreter virtual environment yang sama saat menginstal dan membuka Jupyter. |
| FileNotFoundError untuk CSV | ZIP belum diekstrak atau notebook di luar paket | Ikuti sel persiapan dan periksa nilai ROOT. |
| NotImplementedError | Fungsi challenge belum dilengkapi | Ganti isi fungsi sesuai instruksi, lalu jalankan ulang. |
| KeyError: Ellipsis | Token `...` masih ada | Isi nama kolom atau daftar kolom yang diminta. |
| NameError untuk `__PIVOT__` | Bagian pivot belum diisi | Ganti dengan pemanggilan pivot berdasarkan petunjuk. |
| NameError untuk summary | Sel agregasi belum berhasil | Jalankan sel sesuai urutan, perbaiki error pertama. |
| Angka persen tampil 0,78 | Proporsi belum dikalikan 100 | Kolom dengan akhiran `_pct` memakai skala 0–100. |
| Checker menunjukkan FAIL | Kolom, angka, file, atau presisi belum sesuai | Baca pemeriksaan yang gagal, koreksi, lalu ekspor ulang. |
| Hasil Colab hilang | Runtime berakhir | Unggah paket lagi dan jalankan notebook yang sudah disimpan. |
| Dashboard app meminta hasil | File output belum ada | Selesaikan notebook dan jalankan sel ekspor terlebih dahulu. |

## Layout Direktori Praktikum

```text
Analytics_AI/
├── readme.md / readme.html             # Panduan materi dan tugas
├── requirements.txt                   # Dependensi notebook lokal
├── requirements-dashboard.txt         # Tambahan untuk dashboard opsional
├── initial/
│   └── setup.py                       # Persiapan tanpa mengubah jawaban
├── data/
│   └── chatbot_evaluation.csv          # Dataset sintetis, sama dengan PPT
├── starter/
│   ├── check_environment.py            # Pemeriksaan package
│   ├── check_data.py                   # Pemeriksaan kontrak sumber
│   ├── demo.ipynb                      # Demo kecil sebelum challenge
│   └── dashboard.py                    # Aplikasi pembaca ekspor peserta
├── workspace/
│   ├── analisis.ipynb                  # WORKSPACE PESERTA: kode dilengkapi
│   └── jawaban.md / jawaban.html       # Lembar refleksi, MD untuk diedit
├── test/
│   ├── check_results.py                # Pemeriksaan PASS/FAIL + checks.csv
│   └── assert_results.py               # Berhenti dengan error jika gagal
└── output/
    └── README.txt                     # File hasil muncul setelah latihan
```

Versi HTML lembar jawaban adalah salinan baca/cetak. Mengubah Markdown tidak otomatis mengubah HTML. Kumpulkan Markdown yang sudah diisi.

## Kontrak Data dan Kamus Kolom

**Grain:** satu baris adalah hasil satu pertanyaan pada satu versi chatbot. Key unik adalah pasangan `question_id` dan `model_version`. Versi A dan B menerima 200 pertanyaan yang sama.

| Kolom | Tipe dan satuan | Makna |
|---|---|---|
| question_id | Teks | Identitas pertanyaan, Q001 sampai Q200. |
| model_version | A atau B | Versi yang menjawab pertanyaan tersebut. |
| category | Teks | pengiriman, pembayaran, retur, atau produk. |
| answer_pass | 0 atau 1 | Jawaban memenuhi rubrik kebenaran, relevansi, dan kelengkapan. |
| resolved | 0 atau 1 | Penilai simulasi menganggap kebutuhan kasus terselesaikan. |
| latency_seconds | Angka, detik | Durasi hingga respons selesai. |
| cost_usd | Angka, USD | Biaya pemrosesan satu pertanyaan. |
| failure_reason | Teks atau kosong | Alasan jawaban gagal. Kosong pada jawaban lolos. |

CSV tidak memuat teks pertanyaan dan jawaban. Analisis penyebab pada lab terbatas pada kategori alasan yang sudah tersedia. Untuk investigasi nyata, tim perlu mengambil contoh jawaban dan referensinya dari sistem evaluasi.

### Aturan label dan missing values

- `answer_pass = 1` berarti seluruh syarat rubrik terpenuhi: fakta sesuai referensi, relevan dengan pertanyaan, dan cukup lengkap untuk kebutuhan kasus.
- `answer_pass = 0` berarti setidaknya satu syarat gagal.
- `resolved` merupakan outcome simulasi yang berbeda dari kualitas jawaban.
- Semua label dan metrik numerik dalam dataset latihan tersedia. Denominator per versi berjumlah 200.
- `failure_reason` boleh kosong pada jawaban lolos. Nilai kosong pada kolom ini tidak berarti dataset rusak.
- Pada data nyata, label yang belum tersedia tidak boleh otomatis diubah menjadi 0. Laporkan coverage dan denominator label yang sudah dinilai.

### Batas data

Angka bersifat sintetis, tanpa tanggal pengujian atau data kepuasan pengguna. Jangan membuat grafik tren waktu dari dataset ini. Biaya hanya biaya pemrosesan yang tercatat, bukan keseluruhan biaya layanan. Jumlah 200 kasus merupakan pilihan latihan dan tidak menetapkan ukuran evaluasi produksi.

## Konsep Guided Hands-on

### Konsep 1: Keputusan bisnis dan kelompok metrik

| Kelompok | Contoh metrik | Pertanyaan |
|---|---|---|
| Kualitas AI | Answer pass rate | Seberapa sering jawaban memenuhi rubrik? |
| Operasional | Latency, average cost | Berapa lama respons dan berapa biaya prosesnya? |
| Penyelesaian masalah | Resolution rate | Seberapa sering kebutuhan kasus terselesaikan? |

Kepuasan pengguna perlu pengukuran tersendiri. Jawaban yang benar dan cepat dapat mendukung pengalaman pengguna, tetapi dataset ini belum mengukur hubungan tersebut.

### Konsep 2: Definisi metrik

| Metrik | Rumus/operasi | Satuan output |
|---|---|---|
| Answer pass rate | Jumlah answer_pass=1 ÷ jumlah kasus dinilai × 100 | persen |
| Resolution rate | Jumlah resolved=1 ÷ jumlah kasus dievaluasi × 100 | persen |
| Median latency | Median latency_seconds | detik |
| P95 latency | quantile(0.95), interpolasi linear | detik |
| Average cost | Total cost_usd ÷ jumlah kasus | USD/pertanyaan |

Pada label `[1, 1, 1, 0]`, mean sama dengan 0,75. Dalam satuan persen, hasilnya 75%.

P95 menunjukkan batas yang kira-kira mencakup 95% observasi. Pandas memakai interpolasi linear secara default. Nilainya tidak harus sama dengan salah satu pengamatan. Median dan P95 menjelaskan bagian distribusi yang berbeda.

### Konsep 3: Proporsi, percentage points, dan perubahan relatif

Contoh terpisah: sebuah metrik berubah dari 60% ke 75%.

- Perubahan absolut: `75 − 60 = 15 percentage points`.
- Perubahan relatif: `(75 − 60) ÷ 60 × 100% = 25%`.

Untuk biaya, perubahan relatif dihitung terhadap biaya versi awal. Sebutkan pembanding dan satuan agar stakeholder memahami perubahan.

### Konsep 4: Agregasi dan format panjang/lebar

`groupby()` membagi baris berdasarkan kolom kunci. `agg()` menerapkan fungsi pada setiap kelompok. `reset_index()` mengembalikan kolom kunci agar mudah diekspor.

Tabel kategori berbentuk panjang memiliki satu baris per pasangan kategori–versi. `pivot()` mengubahnya menjadi kategori sebagai baris dan A/B sebagai kolom. Bentuk lebar memudahkan bar chart berdampingan.

Jangan menjumlahkan persentase dua versi. Jangan menghitung median seluruh data dengan merata-ratakan median tiap kategori. Jika dashboard mengubah cakupan, hitung ulang dari data yang sesuai atau nyatakan bahwa ringkasan tetap memakai cakupan keseluruhan.

### Konsep 5: Dashboard yang dapat dibaca

Dashboard minimum memiliki empat grafik: kualitas per kategori, kualitas/penyelesaian per versi, median/P95 latency, dan biaya per versi. Pisahkan sumbu persen, detik, dan USD. Sumbu persentase dimulai dari 0 dan berakhir pada 100.

Setiap grafik memiliki judul, label, serta legenda yang tepat. Sertakan cakupan 200 kasus per versi dan penanda data sintetis. Tabel detail kegagalan mendukung investigasi setelah melihat pola grafik.

### Konsep 6: Data storytelling

Gunakan urutan tujuan, temuan, bukti, implikasi, rekomendasi, dan keterbatasan. Bedakan observasi yang langsung terlihat dari dugaan penyebab.

Contoh terpisah: “Kategori aktivasi memiliki pass rate terendah” merupakan observasi. “Dokumen aktivasi mungkin belum lengkap” merupakan hipotesis yang membutuhkan pemeriksaan referensi. Rekomendasi dapat berupa peninjauan kasus gagal sebelum mengubah sumber jawaban.

## Challenge Hands-on Python

Buka `workspace/analisis.ipynb`. Selesaikan bagian A–E berikut dalam **40 menit**. Pengerjaan berpasangan diperbolehkan, tetapi setiap peserta harus mampu menjelaskan hasil.

### Challenge 1: Metrik dan Keputusan — 5 Menit

Isi bagian A lembar jawaban.

1. Nyatakan keputusan yang akan dibuat tim.
2. Jelaskan grain dan key unik dataset.
3. Pilih satu metrik kualitas dan satu metrik operasional.
4. Jelaskan denominator resolution rate dan arti label resolved.

**Output:** tujuan analisis serta definisi metrik. Tidak perlu membuat diagram tambahan.

### Challenge 2: Profiling — 5 Menit

Lengkapi sel B pada notebook.

1. Hitung jumlah baris dan pertanyaan unik.
2. Hitung duplikasi pasangan ID–versi.
3. Tampilkan jumlah kasus per versi dan kategori.
4. Jelaskan kolom mana yang boleh kosong.

**Checkpoint:** 400 baris, 200 pertanyaan unik, 0 duplikat pasangan ID–versi. Pertanyaan yang sama muncul sekali pada A dan sekali pada B.

### Challenge 3: Perhitungan Metrik — 10 Menit

Lengkapi tiga fungsi pada sel C:

- `make_summary(data)`: ringkasan per versi.
- `make_category_summary(data)`: ukuran sampel dan pass rate per kategori–versi.
- `get_failed_cases(data)`: semua kolom pada baris answer_pass=0.

**Kontrak hasil:**

| Output | Kolom wajib |
|---|---|
| summary | model_version, n, pass_rate_pct, resolution_rate_pct, median_latency_s, p95_latency_s, avg_cost_usd |
| category_summary | model_version, category, n, pass_rate_pct |
| failed_cases | Seluruh kolom sumber, hanya baris answer_pass=0 |

**Checkpoint:** summary memiliki 2 baris. category_summary memiliki 8 baris dengan n=50 pada setiap baris. Kolom `_pct` memakai skala 0–100. Pertahankan presisi penuh saat ekspor.

### Challenge 4: Dashboard dan Ekspor — 10 Menit

Lengkapi pivot pada sel D lalu jalankan scaffold visual.

1. Periksa keempat grafik, legenda, dan satuannya.
2. Bandingkan kualitas, latency, dan biaya secara terpisah.
3. Identifikasi kategori dengan pass rate terendah pada versi B.
4. Ekspor summary.csv, category_summary.csv, failed_cases.csv, dan dashboard.png ke folder output.

**Pertanyaan refleksi:** mengapa grafik kualitas keseluruhan saja belum cukup untuk menentukan prioritas perbaikan?

### Challenge 5: Pemeriksaan dan Rekomendasi — 10 Menit

Jalankan sel pemeriksaan pada notebook. Alternatif lokal:

```bash
python test/check_results.py
```

Gunakan interpreter virtual environment, seperti pada langkah setup. Sel notebook otomatis menggunakan interpreter kernel yang aktif.

1. Perbaiki setiap FAIL dan ekspor ulang.
2. Tulis tiga temuan dengan angka dan satuan.
3. Jelaskan satu trade-off.
4. Buat rekomendasi bersyarat untuk pilot terbatas.
5. Nyatakan satu keterbatasan dan data tambahan yang diperlukan.

**Target minimum:** pemeriksaan hasil lulus dan Anda dapat menjelaskan alasan rekomendasinya. Narasi 80–120 kata dapat menjadi bahan untuk satu slide presentasi.

## Verifikasi & Pemeriksaan Solusi

`test/check_results.py` menampilkan pemeriksaan, aktual, target, dan status. Hasil tersimpan pada `output/checks.csv`. Script menghitung acuan secara independen dari dataset sumber menggunakan standard library Python.

Pemeriksaan mencakup:

- Kelengkapan file hasil dan keunikan versi/kategori.
- Jumlah kasus dan nilai seluruh metrik ringkasan.
- Pass rate serta ukuran sampel per kategori.
- Identitas dan alasan kasus gagal.
- Keberadaan file PNG dashboard.

Pemeriksaan PNG hanya memverifikasi format file. Kejelasan visual, label, interpretasi, dan mutu rekomendasi tetap dinilai instruktur. Toleransi nilai numerik adalah 0,0000001, sehingga simpan presisi penuh saat ekspor dan lakukan pembulatan hanya untuk tampilan.

Untuk pemeriksaan yang berhenti dengan error jika hasil belum benar:

```bash
python test/assert_results.py
```


### Output yang dikumpulkan

1. `analisis_NAMA.ipynb`: notebook hasil kerja, disimpan beserta output.
2. `jawaban_NAMA.md`: definisi metrik, temuan, dan narasi.
3. `summary.csv`, `category_summary.csv`, `failed_cases.csv`, dan `checks.csv`.
4. `dashboard.png`.
5. Satu slide rekomendasi. Jika waktu terbatas, gunakan narasi pada lembar jawaban sebagai bahan presentasi.

Di Colab, sel terakhir dapat mengemas file output ke ZIP. Notebook dan lembar jawaban perlu disimpan terpisah. `jawaban.html` bersifat baca/cetak dan tidak menyimpan isian otomatis.

## Dashboard Interaktif — Opsional, di Luar 40 Menit

Setelah output tersedia, instal `requirements-dashboard.txt` menggunakan interpreter environment yang sama, lalu jalankan:

```bash
python -m streamlit run starter/dashboard.py
```

Aplikasi membaca hasil yang sudah Anda hitung. Filter kategori mengubah grafik kategori dan tabel kasus gagal. Ringkasan seluruh dataset tetap memakai semua kategori dan diberi label demikian. Ini mencegah pengguna mengira metrik global ikut terfilter.

## Challenge Tambahan — Opsional

- Hitung biaya pemrosesan per kasus terselesaikan: total biaya dibagi jumlah resolved=1. Jelaskan batas interpretasinya.
- Bandingkan perubahan dalam percentage points dengan kenaikan relatif.
- Rancang pengukuran kepuasan pengguna saat pilot, termasuk cara mengumpulkan feedback dan denominator.
- Jelaskan bagaimana menerapkan alur metrik dan storytelling pada model klasifikasi, misalnya precision/recall dan biaya kesalahan.

## Instruksi Pembersihan

Simpan notebook, lembar jawaban, dan hasil ekspor. Tutup kernel Jupyter jika sudah selesai. Hentikan Streamlit dengan Ctrl+C pada terminal yang menjalankannya. Pada Colab, unduh hasil sebelum mengakhiri sesi. Dataset dan folder latihan dapat disimpan untuk pengulangan; paket tidak menghapus file otomatis.

Selamat! Anda telah menghasilkan analisis evaluasi AI yang dapat dihitung ulang, dashboard untuk membaca pola, dan rekomendasi yang menjelaskan batas bukti.
