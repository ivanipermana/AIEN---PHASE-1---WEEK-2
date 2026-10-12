# Tugas Tambahan

Dikerjakan setelah tiga TODO wajib selesai. Tidak menambah alokasi 60 menit.

## 1. Retry sementara

```bash
python app.py ask --question "Apa metode pembayaran?" --scenario transient_timeout --run retry_demo
python app.py inspect --run retry_demo
```

Mengapa request sukses pada percobaan kedua? Bandingkan events dengan timeout yang selalu gagal. Apa risiko jika MAX_RETRIES terlalu besar? Di lab, jumlah retry terbatas sudah diimplementasikan pengajar.

## 2. Pengurangan konteks

Ubah TOP_K pada `lab_core/config.py` dari 2 menjadi 1. Jalankan test set dengan label baru. Apakah semua kasus tetap lulus? Bandingkan token input pada generation span. Coba pertanyaan gabungan yang membutuhkan dua sumber: "Berapa lama pengiriman dan kapan invoice dikirim?" Model mock hanya mengekstrak sumber pertama, jadi hasil tidak menilai kemampuan sintesis LLM. Catat keterbatasan ini, lalu gunakan mode live bila akses sudah tersedia.

## 3. Recovery drill konseptual

Jawab skenario RTO/RPO di worksheet. Tentukan data sumber dan konfigurasi yang perlu dipulihkan agar aplikasi dapat memakai kebijakan aktif. Lab ini tidak menyimulasikan disaster recovery infrastruktur atau menjamin target pemulihan.
