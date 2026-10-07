"""Wrapper pemeriksaan; opsi --db dapat diteruskan ke script utama."""
from pathlib import Path
import subprocess
import sys
script = Path(__file__).resolve().parent.parent/'workspace'/'lab_pipeline.py'
raise SystemExit(subprocess.call([sys.executable, str(script), 'check', *sys.argv[1:]]))
