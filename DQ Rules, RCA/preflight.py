from pathlib import Path
import sys
import pandas as pd
import great_expectations as gx
from src.lab import create_checkpoint, validate

root = Path(__file__).resolve().parent
print('Python:', sys.version.split()[0], 'GX:', gx.__version__, 'pandas:', pd.__version__)
assert gx.__version__ == '1.24.0', 'Gunakan GX Core sesuai requirements.txt'
assert pd.__version__ == '2.3.3', 'Gunakan pandas sesuai requirements.txt'
assert all((root/'data'/x).exists() for x in ['customer_source.csv','usage_source.csv','customer_snapshot.csv'])
expectation = gx.expectations.ExpectColumnValuesToNotBeNull(column='customer_id', meta={'rule_id':'PREFLIGHT'})
context, checkpoint = create_checkpoint(root, [expectation])
summary, docs = validate(context, checkpoint, pd.DataFrame({'customer_id':['00001']}), 'preflight', root)
assert summary['success'].all()
assert docs, 'Data Docs belum terbentuk'
print('PREFLIGHT OK')
print('Data Docs:', docs[0])
