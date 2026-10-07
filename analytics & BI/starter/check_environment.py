from pathlib import Path
import importlib,sys
print('Python:',sys.version.split()[0])
failed=[]
for name in ['pandas','matplotlib']:
    try:
        mod=importlib.import_module(name);print('PASS',name,getattr(mod,'__version__',''))
    except Exception as exc:
        failed.append(name);print('FAIL',name,str(exc))
root=Path(__file__).resolve().parents[1]
print('Dataset:', 'PASS' if (root/'data/chatbot_evaluation.csv').is_file() else 'FAIL')
if failed:
    print('Gunakan environment kelas atau pasang requirements.txt di virtual environment.')
    sys.exit(1)
