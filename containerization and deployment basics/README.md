# Hands-on 60 Menit: Dockerize API Sentimen

## Hasil belajar
- Membedakan Dockerfile, image, dan container.
- Melengkapi Dockerfile, build image, dan menjalankan API di container.
- Menguji endpoint, membaca log, dan memperbaiki port mapping.

## Sebelum kelas — tidak termasuk 60 menit
1. Pasang Docker Desktop dan jalankan sampai Engine aktif. Linux boleh memakai Docker Engine.
2. Siapkan VS Code/editor dan browser. Gunakan Terminal macOS/Linux atau PowerShell Windows.
3. Ekstrak seluruh paket, buka folder Paket_Peserta, dan buka terminal di folder tersebut.
4. Jalankan perintah berikut. Baris Server pada docker version harus tersedia.

```bash
docker version
docker pull python:3.12-slim
```

Koneksi internet diperlukan untuk pull image dan pip saat build.
Pengajar menyiapkan cache dependency atau image cadangan sebelum kelas.
Python lokal tidak wajib: seluruh API berjalan di dalam container.
Perintah praktik berikut sama untuk PowerShell dan terminal macOS/Linux;
semua perintah ditulis satu baris. Jangan mengetik tanda pagar prompt terminal.

## 0–10 menit — lihat aplikasi dan kenali file
Buka app.py, requirements.txt, sentiment.py, dan data/model.json.
Diagram alurnya: teks → API FastAPI → model Naive Bayes → respons JSON.

Model kecil sudah dilatih dari 45 contoh sintetis Bahasa Indonesia.
Ini model machine learning, bukan LLM. demo_score adalah skor posterior model
demonstrasi yang belum dikalibrasi, bukan jaminan akurasi.
Model tidak memahami negasi, konteks kompleks, atau sarkasme dengan andal.
Input tanpa kata yang dikenal menghasilkan unknown.

Tulis di worksheet: apa yang perlu ikut dikemas selain app.py?

## 10–25 menit — lengkapi Dockerfile
Edit Dockerfile. Periksa juga `.dockerignore` yang sudah disediakan.
File model di `data/` wajib ikut image, jadi jangan mengecualikan folder tersebut.

Ganti placeholder berikut:

| Placeholder | Isi | Mengapa |
|---|---|---|
| TODO_REQUIREMENTS | requirements.txt | Dependency tersedia sebelum kode aplikasi disalin. |
| TODO_PYTHON_FILES | app.py sentiment.py | API dan kode inferensi ikut dikemas. |
| TODO_MODEL_DIRECTORY | data/ | Parameter model tersedia saat aplikasi dimulai. |
| TODO_HOST | 0.0.0.0 | Server mendengarkan seluruh interface di dalam container. |
| TODO_PORT | 8000 | Port tempat Uvicorn mendengarkan di dalam container. |

Diskusikan fungsi FROM, WORKDIR, COPY, RUN, USER, EXPOSE, CMD.
Instruksi USER sudah disediakan agar API berjalan sebagai appuser, bukan root.
`.dockerignore` mengurangi build context dan mengecualikan `.env` dari pengiriman ke builder.
RUN berjalan saat build; CMD menentukan proses default saat container dimulai.
EXPOSE mendokumentasikan port, sedangkan -p membuat port mapping.

## 25–35 menit — build image
Dari folder yang berisi Dockerfile:

```bash
docker build -t sentiment-api:lab .
docker image ls sentiment-api
```

Titik terakhir adalah build context: folder file yang bisa diakses proses build.
Berhasil jika image sentiment-api dengan tag lab muncul.
Jika gagal, cari langkah pertama yang error, bukan hanya baris terakhir.

## 35–45 menit — jalankan dan uji API

```bash
docker run -d --name sentiment-lab -p 127.0.0.1:8000:8000 -e APP_NAME=Kelas-AI sentiment-api:lab
docker ps
docker logs sentiment-lab
docker exec sentiment-lab id
```

Buka http://localhost:8000/health. Harapkan status ok, app_name Kelas-AI, dan model_version nb-id-demo-v1.
Perintah `id` harus menunjukkan uid=10001(appuser).
Buka http://localhost:8000/docs → POST /predict → Try it out.
Ganti request body, klik Execute, lalu catat respons:

```json
{"text": "layanan cepat dan ramah"}
```

Ulangi dengan barang rusak kualitas jelek dan toko buka jam sembilan.
Harapkan positive, negative, neutral untuk tiga contoh tersebut.
Cek docker logs lagi untuk melihat hasil inferensi dan request HTTP.
Jangan mengharapkan angka demo_score tertentu untuk semua input.

## 45–55 menit — tantangan: container Up, browser gagal
Jalankan container kedua dengan mapping yang sengaja salah:

```bash
docker run -d --name sentiment-port-bug -p 127.0.0.1:8001:9999 sentiment-api:lab
docker ps
docker logs sentiment-port-bug
docker port sentiment-port-bug
```

Coba http://localhost:8001/health. Akses gagal walau container Up.
Bandingkan port pada log Uvicorn dengan kolom PORTS di docker ps.
Jelaskan diagnosis dalam worksheet, lalu perbaiki:

```bash
docker stop sentiment-port-bug
docker rm sentiment-port-bug
docker run -d --name sentiment-port-fixed -p 127.0.0.1:8001:8000 sentiment-api:lab
```

Uji http://localhost:8001/health dan http://localhost:8001/docs.
docker rm di sini hanya menghapus container latihan yang telah dihentikan.

## 55–60 menit — kumpulkan dan review
Lengkapi worksheet.md dan simpan dua screenshot di bukti/.
Kumpulkan Dockerfile, worksheet.md, dan bukti/; tidak perlu mengirim image Docker.
Akhiri dengan menghentikan dan menghapus hanya container latihan:

```bash
docker stop sentiment-lab sentiment-port-fixed
docker rm sentiment-lab sentiment-port-fixed
```

## Jika menemui kendala
| Gejala | Periksa / tindakan |
|---|---|
| Cannot connect to Docker daemon | Jalankan Docker Desktop; tunggu Engine siap. |
| Dockerfile tidak ditemukan | Terminal harus di folder Paket_Peserta, bukan folder ZIP induk. |
| COPY gagal / TODO masih ada | Lengkapi placeholder dan pastikan semua file diekstrak. |
| Nama container sudah dipakai | docker ps -a; stop lalu rm hanya container latihan bernama sama. |
| Port 8000 sudah dipakai | Gunakan -p 127.0.0.1:8002:8000, lalu buka localhost:8002. |
| Browser gagal tetapi container Up | Cek docker port dan docker logs; port kanan harus 8000. |
| Module atau model tidak ditemukan | Pastikan COPY menyertakan sentiment.py dan data/; build ulang. |
| Model salah menilai kalimat baru | Ini model demo kecil; diagnosis kualitas model terpisah dari deployment. |
| Download/build terlalu lama | Gunakan image cadangan instruktur untuk melanjutkan; build mandiri tetap belum dinilai lulus. |

## Pengayaan setelah kelas
Ubah judul API pada app.py dan build ulang. Amati apakah layer instalasi dependensi
menggunakan cache. Untuk sesi berikutnya, tambahkan database, named volume,
Compose, dan healthcheck. Pengayaan ini di luar 60 menit.

## Referensi
- [FastAPI dalam Docker](https://fastapi.tiangolo.com/deployment/docker/)
- [Port mapping Docker](https://docs.docker.com/engine/network/port-publishing/)
- [Container logs](https://docs.docker.com/engine/logging/)

- [Docker build best practices](https://docs.docker.com/build/building/best-practices/)
