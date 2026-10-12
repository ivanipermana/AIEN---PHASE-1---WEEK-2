# Laporan Peserta

Nama/kelompok:

## 1. Baseline

| Ukuran | Baseline | After |
|---|---|---|
| Quality lulus / jumlah kasus | ... | ... |
| Model OK | ... | ... |
| Fallback (degraded) | ... | ... |
| Request error | ... | ... |
| Served rate (ok + degraded) | ... | ... |
| p95 status ok, ms | ... | ... |
| Versi dokumen aktif yang digunakan | ... | ... |

## 2. Diagnosis

| Masalah | Gejala | Bukti spesifik / request_id | Penyebab terbukti / hipotesis | Verifikasi |
|---|---|---|---|---|
| Jawaban kebijakan | ... | ... | ... | ... |
| Timeout | ... | ... | ... | ... |

Mengapa HTTP/request success tidak otomatis berarti jawaban benar?

Mengapa menambah retry tanpa batas dapat memperburuk pengalaman pengguna?

## 3. Prioritas

Skala impact: 1 = gangguan kecil, 3 = masalah berarti pada satu kelompok pengguna, 5 = tugas inti terganggu/risiko serius. Effort: 1 = hingga 1 jam, 3 = hingga 1 hari kerja, 5 = beberapa hari dan dependensi. 2/4 berada di antaranya. Nilai di bawah merupakan estimasi pekerjaan nyata termasuk pengujian, bukan durasi mengetik dalam lab.

| Opsi | Perbaikan | Impact | Effort | Impact / effort |
|---|---|---:|---:|---:|
| A | Memakai sumber kebijakan aktif | 5 | 2 | ... |
| B | Menambahkan fallback setelah timeout | 4 | 2 | ... |
| C | Memindahkan aplikasi ke model lebih besar | 3 | 5 | ... |
| D | Mengubah tampilan chat | 1 | 1 | ... |

Prioritas pertama:

Prioritas kedua:

Bukti dan pertimbangan risiko:

Mitigasi sementara untuk jawaban kebijakan lama:

Asumsi yang dapat mengubah urutan:

## 4. Perubahan dan verifikasi

| Perubahan kode | Owner (peran) | Kriteria berhasil | Kondisi rollback/fallback |
|---|---|---|---|
| ... | ... | ... | ... |
| ... | ... | ... | ... |

Jumlah percobaan generation pada timeout:

Apakah request normal sesudah timeout berhasil? Bukti:

Apakah p95 status ok menggambarkan pengalaman pengguna yang mendapat fallback? Jelaskan:

## 5. Kesimpulan

Tuliskan rekomendasi 3–5 kalimat dengan diagnosis, keputusan prioritas, hasil, dan satu keterbatasan.

## Bonus pemulihan (jika waktu tersedia)

Gangguan pukul 10:00. Layanan pulih 10:25. Data terakhir yang dapat dipulihkan berasal dari 09:00. Target RTO 30 menit, RPO 15 menit.

- Waktu pemulihan aktual:
- Potensi gap data:
- Target mana yang meleset:
- Saran perbaikan proses pemulihan:
