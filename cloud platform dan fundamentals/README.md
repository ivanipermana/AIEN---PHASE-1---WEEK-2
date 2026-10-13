# Hands-on Cloud AI

Anda akan menyimpan dokumen di Google Cloud Storage, membacanya melalui Python di
Google Colab, lalu menghasilkan dua versi ringkasan dengan Gemini API.

## Isi folder

```text
Hands_On_Cloud_AI/
├── README.md
├── 01_Hands_On_Peserta.ipynb
├── LEMBAR_JAWABAN.md
└── data/
    └── laporan_operasional.txt
```

## Mulai dari sini

1. Selesaikan persiapan akun dan akses bersama instruktur sebelum kelas.
2. Buka [Google Colab](https://colab.research.google.com), pilih **File → Upload notebook**,
   lalu upload `01_Hands_On_Peserta.ipynb` dari folder ini.
3. Jalankan sel satu per satu dan lengkapi empat TODO. Hindari **Run all** karena cleanup
   berada di akhir notebook.
4. Ikuti panduan berikut. Simpan hasil ringkasan dan isi `LEMBAR_JAWABAN.md`.

Tools: Google Cloud Console, Cloud Storage, Google Colab, dan Gemini API melalui AI Studio.
Tidak diperlukan instalasi Python di laptop. Akun, billing, IAM, dan API key harus siap
sebelum sesi. Biaya dan kuota mengikuti project kelas; latihan ini tidak dijamin gratis.

## Output yang diharapkan

- File `hasil_cloud_ai_NAMAPESERTA.json` yang diunduh dari notebook.
- `LEMBAR_JAWABAN.md` yang sudah diisi, termasuk tiga verifikasi fakta dan status cleanup.
- Jika diminta instruktur, screenshot bucket/object tanpa kredensial.

Colab menyediakan compute yang dikelola; provisioning VM tidak termasuk latihan ini.

---

## Panduan langkah demi langkah

## Sebelum kelas

- Akun Google dapat membuka Colab dan project Google Cloud kelas.
- Siapkan API key Gemini pribadi melalui https://aistudio.google.com/apikey.
  Gunakan project/API key yang disetujui instruktur. Jangan berbagi API key antar peserta.
- Di sidebar Colab, buka **Secrets** (ikon kunci), tambahkan `GEMINI_API_KEY`,
  tempel nilai key, lalu aktifkan akses untuk notebook ini. Jangan menaruh key di sel kode.
- Simpan file `data/laporan_operasional.txt` dari paket ke laptop.

## Jadwal

| Menit | Aktivitas | Bukti berhasil |
|---|---|---|
| 0–10 | Memahami alur; buka notebook; install library; login | Sel setup selesai |
| 10–20 | Buat bucket privat dan upload file | File muncul di daftar Objects |
| 20–35 | Isi konfigurasi dan TODO untuk membaca file | Teks dan hasil cek angka muncul |
| 35–50 | Isi TODO API; hasilkan dua versi ringkasan | Dua hasil AI ditampilkan |
| 50–60 | Verifikasi fakta, jawab refleksi, cleanup | Jawaban tersimpan; file latihan dihapus |

## 1. Buka notebook dan login

Upload `01_Hands_On_Peserta.ipynb` ke Colab. Gunakan runtime Python dengan CPU.
Jalankan sel instalasi dan login. Pilih akun Google yang sudah diberi akses ke project kelas.
Login Colab memberi kredensial untuk Cloud Storage; key Gemini dipakai untuk model API.
Keduanya adalah mekanisme autentikasi yang berbeda.

## 2. Buat bucket dan upload dokumen

1. Buka https://console.cloud.google.com/storage/browser dan pilih project kelas.
2. Pilih **Create bucket**. Gunakan nama unik seperti
   `aien-lab-KODEKELAS-p01-rmt002` (huruf kecil; ganti semua placeholder).
3. Pilih region yang diberikan instruktur dan storage class **Standard**.
4. Gunakan **Uniform bucket-level access** dan tetap aktifkan pencegahan akses publik.
5. Untuk lab, ikuti konfigurasi soft delete dari instruktur. Jangan aktifkan retention lock.
6. Buat bucket. Buka bucket → **Upload files** → pilih `laporan_operasional.txt`.
7. Pastikan nama object persis `laporan_operasional.txt`, bukan berada dalam folder lain.

## 3. Baca dokumen lewat Python

Isi `PROJECT_ID`, `BUCKET_NAME`, dan `NAMA_PESERTA`. Project ID berbeda dari nama tampilan project.
Isi empat TODO notebook: nama bucket, nama object, ID model pada panggilan API, dan prompt kedua.
Gunakan method `download_as_text(encoding="utf-8")` untuk mengambil isi dokumen.
Notebook sudah memberikan sebagian besar kode agar waktu dipakai memahami alur.

Cek bahwa dokumen memiliki penjualan September Rp120.000.000 dan 64 pesanan terlambat.
Jika teks tidak muncul, hentikan dulu; jangan lanjut memanggil AI dengan input yang salah.

## 4. Panggil model AI

Model default notebook mengikuti contoh dokumentasi yang dicek saat paket dibuat.
Instruktur harus mengonfirmasi ketersediaan model pada akun kelas sebelum sesi.
Jika diberi ID model berbeda, ubah `MODEL_ID` sesuai arahan.

Jalankan ringkasan pertama, lalu ubah prompt kedua menjadi memo untuk manajer:
ringkasan singkat, dua risiko, dua usulan tindakan, dan informasi yang belum tersedia.
Simpan kedua hasil. Output dapat berbeda antar peserta; nilai akurasi dan kejelasannya.
Batasi latihan pada dua panggilan yang berhasil; pengulangan akan memakai kuota tambahan.

## 5. Periksa fakta dan simpan hasil

Periksa angka penjualan, target, dan keterlambatan terhadap dokumen sumber.
Jika AI menyebut sebab keterlambatan yang pasti atau margin keuntungan, tandai sebagai
klaim yang tidak didukung dokumen. Usulan tindakan harus dibedakan dari fakta.
Jalankan sel ekspor dan download file hasil, lalu isi `LEMBAR_JAWABAN.md`.

## 6. Cleanup

Setelah hasil tersimpan, jalankan sel cleanup. Ketik nama bucket ketika diminta.
Kode hanya menghapus object latihan yang dikonfigurasi, tidak menghapus bucket atau project.
Buka Console untuk memastikan object tidak lagi ada pada daftar aktif.

Jika bucket dibuat khusus oleh Anda untuk latihan, hapus bucket yang sudah kosong dari Console
sesuai arahan instruktur. Jangan hapus bucket bersama. Soft-deleted object dapat tetap disimpan
sesuai kebijakan bucket; instruktur menangani kebijakan retensi dan biaya lab.
Hapus Secrets dari salinan notebook jika tidak akan dipakai lagi; API key khusus lab dapat
Anda hapus di AI Studio setelah sesi. Jangan menghapus key yang dipakai aplikasi lain.

## Troubleshooting singkat

| Kendala | Langkah |
|---|---|
| Storage 403 | Pastikan akun login, Project ID, dan akses IAM; hubungi instruktur |
| Storage 404 | Cek nama bucket dan object, termasuk huruf besar/kecil dan folder |
| Secret tidak terbaca | Nama harus `GEMINI_API_KEY`; aktifkan notebook access |
| Model 404 | Gunakan ID model yang sudah diuji instruktur |
| API 429 | Tunggu sesuai pesan layanan; jangan menjalankan ulang berkali-kali |
| Import gagal | Jalankan install; jika diminta, restart runtime lalu ulang login dan konfigurasi |

Jika API belum bisa dipakai, tetap selesaikan pembacaan storage dan evaluasi contoh manual
bersama instruktur. Tandai panggilan API sebagai belum selesai, bukan berhasil.
