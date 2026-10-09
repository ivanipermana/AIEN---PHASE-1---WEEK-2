# Data dictionary dan kontrak latihan

Semua data sintetis. Tidak memuat data pribadi nyata. Angka dan threshold khusus latihan.

## Konteks
Prediksi dibuat pada 1 Agustus 2026 untuk pelanggan aktif. Label menunjukkan pembatalan dalam 30 hari setelah snapshot.
Untuk latihan, data dibekukan pada 5 September 2026 sehingga periode label seluruh baris sudah selesai.
Satu baris = satu pelanggan pada satu tanggal snapshot. Dataset ini untuk latihan kualitas data, bukan training model.

| Kolom | Tipe/makna | Ketentuan |
|---|---|---|
| customer_id | String, identitas pelanggan | Lima digit pada sumber resmi, nol awal bermakna. Wajib terisi. Tidak boleh dikonversi menjadi integer. |
| snapshot_date | String tanggal YYYY-MM-DD | Tanggal kondisi pelanggan, bagian dari kunci gabungan |
| source_system | Kategori asal pelanggan | legacy atau modern |
| tenure_months | Integer, lama berlangganan | Bulan, >= 0 |
| monthly_fee | Integer, harga paket per bulan | Rupiah, >= 0. Tidak mencakup kredit/refund. |
| complaint_count_30d | Integer | Keluhan selama 30 hari sebelum snapshot |
| region | Kategori | Barat, Tengah, Timur |
| usage_30d | Numerik | Jumlah penggunaan selama 30 hari sebelum snapshot. Nol berarti tidak ada penggunaan. Null berarti data tidak tersedia. |
| churn_next_30d | Integer 0/1 | Label pembatalan dalam 30 hari setelah snapshot, tidak digunakan sebagai feature |

## File dan lineage
- customer_source.csv: sumber resmi pelanggan sebelum transformasi, 100 baris.
- usage_source.csv: sumber agregasi penggunaan, 100 baris, kunci gabungan unik.
- customer_snapshot.csv: hasil pipeline yang akan diaudit.
- Alur: customer_source, normalisasi ID, left join usage_source, simulasi ingestion replay, customer_snapshot.
- Join menggunakan pasangan customer_id dan snapshot_date.

## Empat aturan yang disepakati untuk simulasi
| ID | Aturan | Toleransi | Owner | Severity / tindakan |
|---|---|---|---|---|
| DQ01 | customer_id terisi | 100% | Data Owner pelanggan | Critical: tahan batch, investigasi ID kosong |
| DQ02 | Pasangan ID dan snapshot unik | 100% | Data Steward pelanggan | Critical: tahan batch, investigasi replay |
| DQ03 | monthly_fee >= 0 | 100% nilai non-null | Data Owner billing | Critical: tahan batch, konfirmasi sumber billing |
| DQ04 | usage_30d terisi | Minimal 95% baris | Data Steward usage | Critical: tahan batch, investigasi sumber dan join |

Threshold 95% merupakan keputusan fiktif untuk latihan, bukan benchmark industri.
DQ03 memeriksa validitas nilai non-null, bukan completeness biaya. Tambahkan aturan null jika dibutuhkan di penggunaan nyata.
Meta severity/action mencatat kebijakan latihan. GX tidak otomatis menghentikan pipeline karena metadata tersebut.
Dalam notebook, keputusan hold/release dibuat secara eksplisit dari hasil aturan.
Data Custodian/pipeline engineer melaksanakan perbaikan, menjalankan ulang batch, dan menyimpan bukti.
Seluruh aturan kritis harus lulus sebelum release pada kebijakan latihan ini.
