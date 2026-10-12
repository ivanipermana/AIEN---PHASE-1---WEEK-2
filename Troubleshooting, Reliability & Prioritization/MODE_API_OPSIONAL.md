# Mode LLM API Opsional

Mode ini untuk eksperimen setelah lab wajib atau kelas yang kredensialnya telah disiapkan sebelum sesi. Lab 60 menit dapat diselesaikan seluruhnya dengan mock.

Adapter tersedia pada `lab_core/model.py`, menggunakan OpenAI Responses API melalui Python standard library. Pertanyaan dan konteks fiktif dikirim ketika Anda memilih `--provider openai`. Mode mock tidak mengirim data jaringan.

## Konfigurasi

Set `OPENAI_API_KEY` dan `AIEN_OPENAI_MODEL` pada environment shell atau pengelola secret yang biasa Anda gunakan. Isi model dengan model yang memang tersedia pada akun Anda. Jangan menaruh key dalam kode, worksheet, atau output. Aplikasi tidak menyediakan model default, tidak mencetak key, dan tidak menyimpan file credential.

Periksa keberadaan variabel tanpa mencetak nilainya:

```bash
python -c "import os; print('Key tersedia:', bool(os.getenv('OPENAI_API_KEY'))); print('Model tersedia:', bool(os.getenv('AIEN_OPENAI_MODEL')))"
```

Mulai dengan satu request:

```bash
python app.py ask --provider openai --question "Berapa hari batas refund?" --run live_demo
```

Jika sudah sesuai, jalankan evaluasi:

```bash
python app.py evaluate --provider openai --run live_eval
```

Panggilan API menggunakan kuota/biaya akun. Skenario timeout Q10 tetap diinjeksi lokal agar reproducible; ia tidak sengaja menunggu atau membuat provider nyata timeout. Skenario normal menggunakan API sungguhan.

## Interpretasi

Durasi live bergantung jaringan, model, dan beban. Jangan membandingkan hasil live dengan mock sebagai benchmark model. `usage` diambil dari provider ketika tersedia. Respons model dapat bervariasi; checker keyword dapat memberi false negative sehingga pengajar perlu meninjau makna jawaban. ID sumber yang dihasilkan model tetap perlu diperiksa terhadap konteks.

Model latency yang melebihi timeout dapat berakhir fallback pada solusi, sehingga timeout 20 detik dalam config bukan target produksi universal. Retry hanya untuk timeout pada panggilan generasi teks, bukan retry segala jenis HTTP error. HTTP429/401 diteruskan sebagai error provider dan perlu investigasi berbeda. Tidak ada tool yang melakukan pembayaran atau efek samping dalam lab ini.

Adapter mengikuti [official OpenAI documentation: text generation](https://developers.openai.com/api/docs/guides/text) dan [quickstart](https://developers.openai.com/api/docs/quickstart). Body memakai model, instructions, input, dan store=false. Parser membaca output message/content bertipe output_text.

Integrasi dan parsing diuji dengan respons HTTP yang dimock. Panggilan provider nyata tidak dijalankan saat paket dibuat karena tidak ada kredensial yang diberikan.
