import json
import sys
from pathlib import Path
root=Path(__file__).resolve().parent
if sys.version_info < (3,9):
    raise SystemExit('Gunakan Python 3.9 atau lebih baru.')
for name in ('data/manifest.json','data/policy_v1.json','data/policy_v2.json','data/test_cases.json'):
    data=json.loads((root/name).read_text(encoding='utf-8'))
    print('OK',name)
from workspace import tasks
from lab_core.pipeline import FAQApplication
app=FAQApplication(tasks)
result,trace,events=app.ask('Berapa hari batas refund?')
assert result['status']=='ok',result
print('OK: aplikasi mock dapat berjalan. Periksa versi sumber pada trace.')
print('Tidak memerlukan pip install, API key, atau internet untuk lab wajib.')
