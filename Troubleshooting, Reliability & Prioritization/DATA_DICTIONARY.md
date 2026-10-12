# Kamus Data dan Istilah

Semua dokumen dan kebijakan merupakan data perusahaan fiktif. FAQ URL `https://support.example.com/faq` adalah placeholder, bukan layanan yang harus dibuka.

## Dokumen

`manifest.current_version`: versi dokumen yang telah disetujui sebagai sumber aktif. `manifest.versions`: lokasi file sumber tiap versi. `id`: ID dokumen untuk menghubungkan retrieval dan jawaban. `keywords`: kata yang digunakan oleh pencarian sederhana. `body`: isi kebijakan. Retrieval memilih dokumen berdasarkan jumlah keyword pertanyaan yang cocok, kemudian mengurutkan ID untuk tie-break.

Tidak ada vector database, embeddings, atau background ingestion dalam lab wajib. TODO 2 memperbaiki pemilihan sumber aktif, bukan memulihkan job ingestion produksi.

## Trace

| Field | Arti |
|---|---|
| `request_id` | ID untuk menghubungkan result, trace, events |
| `timestamp` | Waktu UTC dalam ISO8601 |
| `provider` | mock atau openai |
| `status` | ok, degraded, error setelah TODO 1 selesai |
| `duration_ms` | Durasi seluruh request lokal dalam milidetik |
| `spans` | Operasi retrieval, generation, fallback |
| `index_version` | Versi dokumen yang retrieval gunakan |
| `current_version` | Versi aktif menurut manifest |
| `document_ids` | Sumber yang retrieval pilih |
| `attempt` | Percobaan generation, mulai dari 1 |
| `input_tokens` / `output_tokens` | Usage provider atau estimasi mock |
| `token_measurement` | provider_usage atau estimated_chars_div_4 |
| `error_type` | Jenis error tanpa credential |

Trace menyimpan metadata sumber, durasi, dan usage. Result menyimpan pertanyaan/jawaban fiktif untuk evaluasi. Error spans tidak memiliki token usage jika provider tidak memberikannya. Jumlah durasi spans tidak selalu sama dengan total karena total juga mencakup overhead dan backoff.

## Status dan metrics

- `ok`: model menghasilkan jawaban, termasuk jawaban penolakan karena sumber tidak cukup.
- `degraded`: model gagal, aplikasi memberi fallback.
- `error`: aplikasi belum bisa memberi respons yang sesuai.
- `ok_rate`: jumlah ok / seluruh kasus.
- `served_rate`: (ok + degraded) / seluruh kasus. Ini ukuran pelayanan dalam lab, bukan SLA uptime produksi.
- `error_rate`: error / seluruh kasus.
- `quality_pass_rate`: kasus yang lulus kriteria / seluruh kasus. Fallback dapat lulus kasus reliability walaupun bukan jawaban model.
- `p95_ok_ms`: nearest-rank pada durasi status ok, tidak memasukkan fallback/error.

Quality checker memakai required keywords, forbidden phrases, sumber, dan expected status. Kriteria sempit ini cocok untuk kasus deterministik dan memerlukan review manusia ketika memakai LLM.

## Reliability

Timeout membatasi waktu menunggu operasi. Dalam mock, error timeout diinjeksi agar dapat diulang. Mode API memakai timeout socket per call; aplikasi ini belum menerapkan total deadline global untuk seluruh request. Retry maksimum 1 berarti maksimal 2 percobaan. Backoff memberi jeda, jitter menambahkan variasi acak. Fallback adalah alternatif respons yang aman ketika jalur model gagal.
