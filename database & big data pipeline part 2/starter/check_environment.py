"""Jalankan dari folder utama: python starter/check_environment.py"""
from pathlib import Path
import sys
import sqlite3
import asyncio
import json
import importlib.metadata
root = Path(__file__).resolve().parent.parent
checks = [('Python >= 3.11', sys.version_info >= (3, 11)),
          ('asyncio.TaskGroup', hasattr(asyncio, 'TaskGroup')),
          ('Script workspace tersedia', (root/'workspace/lab_pipeline.py').is_file())]
events = json.loads((root/'data/checkout_events.json').read_text())
checks.append(('Dataset 12 delivery', len(events) == 12))
for label, ok in checks:
    print(('PASS' if ok else 'FAIL') + ' | ' + label)
print('SQLite:', sqlite3.sqlite_version)
try:
    print('Prefect:', importlib.metadata.version('prefect'))
except importlib.metadata.PackageNotFoundError:
    print('BELUM SIAP Challenge 2 | pip install -r requirements.txt')
    print('Batch dan streaming tetap dapat dijalankan.')
if not all(ok for _,ok in checks):
    raise SystemExit(1)
