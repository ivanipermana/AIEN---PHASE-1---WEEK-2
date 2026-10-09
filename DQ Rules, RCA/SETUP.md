# Setup sebelum kelas

Gunakan Python 3.11–3.13. Versi yang diuji pada paket ini dicatat di VALIDATION.md pada paket instruktur.
Tools: VS Code, ekstensi Python dan Jupyter. Internet diperlukan saat instalasi saja.
Tidak memerlukan akun GX Cloud, token, database, atau WSL untuk latihan lokal ini.
Analytics GX dinonaktifkan dalam helper agar validasi dapat berjalan lokal tanpa telemetry.

## Windows PowerShell
Jalankan dari folder Paket_Peserta:
```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe preflight.py
```
Pilih kernel melalui VS Code: Select Kernel, Python Environments, .venv.
Jika belum muncul, gunakan Select Interpreter dan pilih .venv/Scripts/python.exe.
Tidak perlu mengubah execution policy karena aktivasi environment tidak diperlukan.

## macOS / Linux
```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python preflight.py
```
Pilih kernel .venv/bin/python di VS Code.

## Pemeriksaan sebelum kelas
preflight.py menjalankan satu Checkpoint sederhana dan membuat Data Docs lokal.
Pesan PREFLIGHT OK menunjukkan dependensi dan konfigurasi GX berfungsi.
Jika import gagal, cek bahwa terminal dan notebook memakai interpreter .venv yang sama.
Jika data tidak ditemukan, buka notebook dari folder paket yang sudah diekstrak, bukan dari ZIP.
Jika Data Docs tidak terbuka melalui link notebook, buka index.html yang dicetak menggunakan browser.
Jalankan Restart Kernel lalu Run All untuk memulai ulang notebook.

Jika pip mengatakan versi tidak ditemukan, cek akses package index dan versi Python.
Jangan mengganti versi GX tanpa menguji ulang karena API antarversi berbeda.
