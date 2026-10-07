# Lembar Jawaban Peserta

```text
Nama:
Tanggal:
Versi Python / Prefect:
Path database utama:

A. Pipeline batch
- Urutan sumber, validasi, transformasi, dan penyimpanan:
- Bagian kode yang menunggu satu batch penuh:
- Input / valid / rejected / duplicate:
- Hasil O001 dan O004:
- ID dengan is_high_value = 1:
- Hasil eksperimen order_value = 0 sebelum/sesudah perubahan:
- Mengapa delivered_date tidak masuk fitur checkout?

B. Orkestrasi
- Urutan task:
- Task yang gagal dan jumlah percobaan:
- Bukti retry berhasil:
- Dampak mengubah retry_delay_seconds:
- Contoh error yang tidak selesai hanya dengan retry:

C. Streaming
- Peran producer, antrean, consumer, dan sentinel:
- Bukti output muncul sebelum sumber selesai:
- Mengapa antrean dalam memori tidak tahan restart?

D. Tabel hasil eksperimen (satuan waktu: detik)
Mode | interval | work | queue_size | first_output_s | total_s | max_queue | producer_wait_s
Batch | 0.5 | 0.1 | tidak berlaku | ... | ... | 0 | 0
Stream | 0.5 | 0.1 | 3 | ... | ... | ... | ...
Stream lambat | 0.1 | 0.6 | 3 | ... | ... | ... | ...
Stream lambat | 0.1 | 0.6 | 1 | ... | ... | ... | ...

E. Verifikasi dan refleksi
- Hasil check sebelum / setelah replay:
- Jumlah fitur batch / stream sebelum dan setelah replay:
- Mengapa raw bertambah tetapi features tidak?
- Kapan memilih batch? Kapan memilih streaming?
- Mengapa hasil ini bukan bukti exactly-once atau benchmark produksi?

```
