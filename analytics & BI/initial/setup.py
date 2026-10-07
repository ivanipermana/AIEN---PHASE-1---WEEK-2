"""Persiapan idempoten. Tidak mengubah dataset atau jawaban."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[1]
(root/'output').mkdir(exist_ok=True)
for name in ['check_environment.py','check_data.py']:
    subprocess.run([sys.executable,str(root/'starter'/name)],check=True)
print('Setup selesai. Buka workspace/analisis.ipynb, lalu baca Mulai_Di_Sini.html.')
