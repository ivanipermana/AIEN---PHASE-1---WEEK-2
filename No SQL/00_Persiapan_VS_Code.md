# Persiapan sebelum kelas

Alokasikan 15–20 menit terpisah dari hands-on. Siapkan Python 3.10 atau lebih baru,
VS Code, extension **Python** (`ms-python.python`), dan **Jupyter** (`ms-toolsai.jupyter`).
Internet hanya diperlukan saat instalasi. Eksperimen setelah setup berjalan offline.

## 1. Buka folder

Ekstrak ZIP dan buka folder `Paket_Peserta` dengan File > Open Folder. Buka Terminal >
New Terminal. Pastikan `README.md`, `simulator.py`, dan folder `data` terlihat.

## 2. Buat environment dan pasang kernel

Windows PowerShell:

```powershell
py -3 --version
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

macOS / Linux:

```bash
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Tidak perlu mengaktifkan environment atau mengubah execution policy PowerShell.
Environment ini hanya dipakai untuk latihan lokal.

## 3. Pilih kernel notebook

Buka `01_Hands_On_Peserta.ipynb`. Klik **Select Kernel** di kanan atas, pilih
**Python Environments**, lalu Python dari `.venv` yang baru dibuat. Jika belum muncul,
gunakan **Python: Select Interpreter** di Command Palette dan pilih interpreter `.venv`,
kemudian pilih kembali kernel notebook. Jalankan cell persiapan. Hasil yang benar:
`Siap: 30 produk | 60 request flash sale`.

## Troubleshooting

| Gejala | Langkah |
|---|---|
| `python` / `py` tidak ditemukan | Pasang Python dahulu, lalu buka ulang VS Code |
| `No module named ipykernel` | Jalankan perintah pip di atas dan pilih kernel `.venv` |
| `No module named simulator` / file data tidak ditemukan | Ekstrak seluruh ZIP, buka folder paket, simpan notebook di sebelah `simulator.py`, restart kernel |
| Perubahan `simulator.py` belum terbaca | Restart kernel, lalu jalankan dari atas |
| Nilai eksperimen berubah karena urutan cell | Restart kernel lalu Run All. Setiap eksperimen utama membuat cluster baru |
| Notebook tidak bisa dieksekusi dalam Restricted Mode | Tinjau isi paket dan izinkan Workspace Trust jika Anda mempercayai foldernya |
| Kernel bermasalah saat kelas | Kerjakan bersama pasangan. Alternatif terminal: jalankan perintah di bawah dan isi lembar jawaban |

Fallback tanpa Jupyter, untuk demo replication dan sharding:

```bash
python simulator.py
```

Pada Windows bisa memakai `py simulator.py`, pada macOS/Linux `python3 simulator.py`.
Fallback ini hanya menampilkan demo; notebook tetap jalur utama untuk mengubah parameter
serta menjalankan eksperimen quorum. Bila diperlukan, panggil fungsi simulator dari Python REPL.

Panduan resmi: [Jupyter Notebooks in VS Code](https://code.visualstudio.com/docs/datascience/jupyter-notebooks).
