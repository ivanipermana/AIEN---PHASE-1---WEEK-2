"""Pemeriksaan struktur sumber; tidak menghitung solusi challenge."""
from pathlib import Path
import pandas as pd
EXPECTED = {'question_id', 'model_version', 'category', 'answer_pass', 'resolved', 'latency_seconds', 'cost_usd', 'failure_reason'}
def validate_source(data):
    problems = []
    if set(data.columns) != EXPECTED:
        raise ValueError(f'Kolom wajib: {sorted(EXPECTED)}')
    if len(data) != 400: problems.append('Jumlah baris harus 400.')
    if data[['question_id','model_version','category']].isna().any().any(): problems.append('ID, versi, kategori wajib terisi.')
    if data.duplicated(['question_id','model_version']).any(): problems.append('Pasangan ID–versi tidak unik.')
    if set(data.model_version) != {'A','B'}: problems.append('Versi harus A dan B.')
    if set(data.category) != {'pengiriman','pembayaran','retur','produk'}: problems.append('Kategori tidak sesuai kontrak.')
    if not data[['answer_pass','resolved']].isin([0,1]).all().all(): problems.append('Label harus lengkap dan bernilai 0/1.')
    for column in ['latency_seconds','cost_usd']:
        numeric = pd.to_numeric(data[column], errors='coerce')
        if numeric.isna().any() or (numeric < 0).any() or not numeric.map(lambda n: __import__('math').isfinite(n)).all():
            problems.append(f'{column} harus angka finite nonnegatif.')
    a=set(data.loc[data.model_version=='A','question_id']); b=set(data.loc[data.model_version=='B','question_id'])
    if a != b or len(a) != 200: problems.append('Kasus A/B harus sama, 200 ID unik.')
    counts=data.groupby(['model_version','category']).size()
    if len(counts)!=8 or not counts.eq(50).all(): problems.append('Setiap kategori harus 50 kasus per versi.')
    if problems: raise ValueError('\n'.join(problems))
    print('PASS: kontrak data sumber terpenuhi.')
if __name__ == '__main__':
    root=Path(__file__).resolve().parents[1]
    validate_source(pd.read_csv(root/'data/chatbot_evaluation.csv'))
