# Flash Sale: NoSQL, Reliability & Scalability

P1W3D5 · Hands-on 60 menit · VS Code + Python · Berpasangan

## Mulai di sini

1. Ekstrak seluruh ZIP. Jangan hanya memindahkan notebook.
2. Buka folder **Paket_Peserta** lewat **File > Open Folder** di VS Code.
3. Selesaikan `00_Persiapan_VS_Code.md` sebelum kelas.
4. Buka `01_Hands_On_Peserta.ipynb`, pilih kernel `.venv`, lalu jalankan cell dari atas.
5. Ikuti aktivitas dan isi `02_Lembar_Jawaban.md`.

## Tujuan

Anda dapat memilih model penyimpanan berdasarkan pola akses, menjelaskan dampak
partition pada pembacaan, membedakan replication dari sharding, dan menjelaskan
konsekuensi pengaturan quorum. Tidak perlu menulis simulator dari nol.

## Kasus

Marketplace menjual produk dengan atribut beragam. Saat flash sale, produk terbaru
menerima sebagian besar request. Tiga replika menyimpan stok produk. Sebuah gangguan
jaringan memisahkan node C dari A dan B, sementara pengguna tetap mengakses layanan.
Tim Anda diminta menjelaskan hasil eksperimen dan keputusan desainnya.

## Jadwal tepat 60 menit

| Menit | Kegiatan | Bukti kerja |
|---|---|---|
| 00–05 | Briefing, pembagian peran, cek notebook | Cell persiapan berhasil |
| 05–15 | Model data dan pola akses | Enam keputusan + contoh JSON |
| 15–30 | Replication dan partition | Hasil dua kebijakan baca + pemulihan |
| 30–45 | Range dan hash sharding | Empat distribusi request + analisis hotspot |
| 45–55 | Tunable consistency | Tabel empat eksperimen quorum |
| 55–60 | Debrief dan pengumpulan | Exit ticket dan file tersimpan |

Satu orang mengoperasikan VS Code, satu orang memprediksi dan mencatat. Tukar peran
pada menit 30. Untuk setiap eksperimen: prediksi, jalankan, lalu jelaskan hasil.

## Isi paket

- `00_Persiapan_VS_Code.md`: instalasi dan troubleshooting sebelum kelas.
- `01_Hands_On_Peserta.ipynb`: instruksi, eksperimen runnable, dan tugas parameter.
- `02_Lembar_Jawaban.md`: tempat mengumpulkan keputusan dan observasi.
- `simulator.py`: simulator siap pakai yang boleh dibaca.
- `data/`: 30 produk dan dua pola traffic sintetis.
- `requirements.txt`: kernel notebook saja. Simulasi memakai library bawaan Python.

## Pengumpulan

Isi nama pada lembar jawaban. Simpan notebook beserta output dan lembar jawaban ke
folder `Nama1_Nama2_P1W3D5`, lalu ZIP dan serahkan sesuai kanal kelas.
Jangan menyertakan `.venv`. Minimum: semua tabel terisi, output eksperimen tersimpan,
dan exit ticket dijawab dengan alasan.

## Batas simulasi

Semua node adalah dictionary di satu proses Python. Partition direpresentasikan oleh
parameter `reachable`, tanpa jaringan sungguhan. Pemulihan dilakukan manual. Latency,
pemilihan leader, failover otomatis, conflict resolution dan transaksi concurrent
tidak dimodelkan. Jangan menggunakan hasil lab sebagai benchmark database.

Kebijakan `serve_local` memperlihatkan stale read, bukan jaminan AP penuh.
`require_majority` memperlihatkan penolakan pada sisi minoritas. CAP membahas
konsistensi linearizable dan ketersediaan saat partition, bukan sekadar HTTP response.
Error penolakan tidak memenuhi ketersediaan operasi yang diminta dalam pengertian CAP.
Replikasi menyimpan salinan data. Sharding membagi data dan beban ke kelompok berbeda.
Keduanya dapat dipakai bersama. Replikasi sendiri juga bukan pengganti backup.
