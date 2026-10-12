# Lab 60 Menit: Perbaikan Chatbot FAQ

Anda adalah AI Engineer untuk chatbot FAQ perusahaan fiktif. Pengguna melaporkan jawaban kebijakan lama dan kegagalan layanan saat model timeout. Tugas Anda: menemukan bukti, memilih prioritas, memperbaiki aplikasi, lalu menguji hasilnya.

## Persiapan sebelum kelas

Python 3.9 atau lebih baru dan VS Code/terminal sudah tersedia. Di macOS/Linux gunakan `python3`, di Windows gunakan `py`; contoh di bawah menggunakan `python` untuk interpreter Python 3 yang sudah disiapkan.

```bash
python preflight.py
```

Preflight harus menampilkan `OK` untuk seluruh file dan aplikasi mock. Jawaban kebijakan lama merupakan kondisi awal yang disengaja. Jika command `python` tidak dikenali, gunakan `python3` atau `py` secara konsisten untuk semua langkah.

## 0–5 menit: baseline

Jalankan 10 kasus uji sebelum mengubah kode:

```bash
python app.py evaluate --run baseline
```

Buka `output/baseline/report.html` dengan browser. Baca jawaban kasus Q05–Q07 dan perilaku Q10. Catat jumlah kasus lulus, status ok/degraded/error, serta versi dokumen dalam trace. Baseline sengaja belum memenuhi seluruh pengujian.

Uji satu pertanyaan jika dibutuhkan:

```bash
python app.py ask --question "Berapa hari batas refund?" --run demo_awal
```

## 5–15 menit: observability

Edit **TODO 1** pada `workspace/tasks.py`. Lengkapi total durasi dan status request menggunakan parameter yang sudah tersedia. Jangan menghapus metadata atau spans. Durasi individual retrieval/generation sudah direkam aplikasi.

```bash
python app.py evaluate --run observed
python app.py inspect --run observed --request-id Q05
python app.py inspect --run observed --request-id Q10
```

Buka juga `output/observed/events.jsonl`. Cocokkan `request_id` antara hasil, events, dan trace. Pada Q10, berapa jumlah percobaan generation? Apa yang terjadi setelah retry habis? Apakah request model yang gagal mempunyai token usage? Jangan menebak usage yang tidak tersedia.

## 15–25 menit: diagnosis

Bandingkan `data/manifest.json` dengan `index_version` di trace. Baca isi `data/policy_v1.json` dan `data/policy_v2.json`.

Tuliskan dalam `workspace/jawaban.md`:

- Dua gejala dan kasus yang terdampak.
- Bukti dari jawaban, sumber, logs, atau trace.
- Penyebab yang dapat dibuktikan lewat kode versus hipotesis yang masih perlu diuji.
- Tindakan yang dapat mengurangi dampak sambil menunggu perbaikan.

Timeout Q10 sengaja diinjeksi. Ini membuktikan kelemahan handling kegagalan, bukan membuktikan bahwa provider nyata sedang outage.

## 25–30 menit: prioritas

Gunakan tabel impact/effort pada worksheet. Hitung rasio, pilih dua perbaikan, dan jelaskan urutannya. Pertimbangkan risiko jawaban kebijakan salah serta ketergantungan antarperbaikan. Estimasi adalah asumsi latihan, bukan ukuran universal.

## 30–45 menit: implementasi

Edit **TODO 2** dan **TODO 3** pada `workspace/tasks.py`:

1. Gunakan versi dokumen aktif yang terdaftar dalam manifest. Jangan sekadar mengganti string v1 menjadi v2: versi aktif harus mengikuti manifest agar perubahan berikutnya tidak memerlukan edit kode.
2. Setelah retry timeout habis, berikan pesan gangguan dan tautan FAQ yang diterima fungsi. Hindari mengarang jawaban kebijakan.

Retry terbatas sudah disediakan: `MAX_RETRIES = 1` berarti paling banyak dua percobaan. Fallback harus berstatus `degraded`, bukan `ok`. Pipeline mengatur status tersebut setelah fungsi fallback mengembalikan pesan.

## 45–55 menit: evaluasi ulang

```bash
python app.py evaluate --run after
python app.py compare --before baseline --after after
python check_work.py
```

Buka `output/after/report.html`, cek seluruh kasus. `check_work.py` memeriksa kualitas, telemetry, batas percobaan, keberhasilan retry sementara, dan request normal sesudah timeout. Bila belum lulus, gunakan pesan checker untuk memperbaiki kode. Gunakan label baru seperti `after2` bila melakukan run berikutnya.

Jumlah `ok` bisa tetap sama walaupun reliability membaik: Q10 kini mendapat fallback, bukan jawaban model. Bedakan `ok_rate`, `served_rate`, dan quality pass rate.

## 55–60 menit: laporan

Lengkapi kesimpulan pada `workspace/jawaban.md`: urutan perbaikan, bukti hasil, owner, kondisi fallback/rollback, serta satu keterbatasan evaluasi.

Kumpulkan `workspace/tasks.py`, `workspace/jawaban.md`, dan folder run baseline/after. Jangan mengumpulkan API key jika mencoba mode API.

## Struktur project

| File/folder | Fungsi |
|---|---|
| `workspace/tasks.py` | Satu-satunya file kode wajib yang diedit peserta |
| `workspace/jawaban.md` | Worksheet diagnosis dan prioritas |
| `app.py` | CLI untuk ask, evaluate, inspect, compare |
| `lab_core/retrieval.py` | Pencarian keyword pada dokumen lokal |
| `lab_core/model.py` | Model mock dan adapter API opsional |
| `lab_core/pipeline.py` | Alur request, retry terbatas, spans, dan fallback |
| `data/manifest.json` | Versi sumber yang aktif |
| `data/test_cases.json` | 10 kasus uji tetap |
| `output/<run>/report.html` | Laporan yang bisa dibuka tanpa server |
| `output/<run>/traces.jsonl` | Trace tiap request |
| `output/<run>/events.jsonl` | Events timeout/retry/fallback |
| `output/<run>/metrics.json` | Ringkasan evaluasi |

## Jika mengalami kendala

- **Run sudah ada:** gunakan `--run baseline2`, `after2`, dan seterusnya. Aplikasi menjaga baseline dengan menolak menimpa run lama.
- **File tidak ditemukan:** pastikan ZIP diekstrak lengkap dan Anda berada dalam folder paket. Program membaca data relatif terhadap lokasi project.
- **Timeout di baseline:** kondisi ini disengaja. Evaluasi menangkap kegagalan dan melanjutkan kasus berikutnya.
- **Nilai durasi berbeda dengan teman:** waktu diukur pada komputer masing-masing. Jangan mengharapkan angka latency persis sama.
- **Belum mengenal JSON:** lihat `DATA_DICTIONARY.md` dan fokus pada request_id, status, index_version, duration_ms.
- **Notebook:** buka notebook di folder project. Jalankan command dengan `!python app.py evaluate --run baseline`, atau `%run app.py evaluate --run baseline`. Gunakan kernel Python 3 dan folder kerja yang sama. Kode yang diedit tetap `workspace/tasks.py`; setiap command CLI memulai proses baru sehingga perubahan langsung terbaca.

## Batas interpretasi

Mode mock mengambil teks dari dokumen sebagai jawaban. Tidak ada inferensi LLM atau embeddings. Durasi berasal dari proses lokal termasuk jeda model yang disimulasikan. Token mock adalah perkiraan karakter/4, bukan tokenizer. Test set berisi 10 kasus dengan checker berbasis keyword/source; ini belum menilai seluruh variasi semantik, hallucination, atau kualitas produksi. Fallback dihitung terpisah dari respons model yang sukses.

Mode API sungguhan dan latihan tambahan dijelaskan di `MODE_API_OPSIONAL.md` serta `BONUS.md`.
