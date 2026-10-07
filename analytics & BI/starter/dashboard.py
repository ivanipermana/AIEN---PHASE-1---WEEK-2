"""Dashboard opsional; membaca hasil ekspor peserta, tidak mengerjakan agregasi challenge."""
from pathlib import Path
import pandas as pd
import streamlit as st
ROOT=Path(__file__).resolve().parents[1]
st.set_page_config(page_title='Evaluasi Chatbot A/B',layout='wide')
st.title('Evaluasi Chatbot A/B')
st.caption('Data sintetis untuk pembelajaran. Resolved merupakan penilaian simulasi.')
try:
    summary=pd.read_csv(ROOT/'output/summary.csv').set_index('model_version').sort_index()
    category=pd.read_csv(ROOT/'output/category_summary.csv')
    failed=pd.read_csv(ROOT/'output/failed_cases.csv')
except FileNotFoundError:
    st.info('Selesaikan notebook dan ekspor hasil ke output terlebih dahulu.');st.stop()
st.subheader('Ringkasan seluruh dataset')
st.caption('Ringkasan di bagian ini mencakup semua kategori; filter di bawah hanya mengubah grafik kategori dan tabel kegagalan.')
st.dataframe(summary.style.format({'pass_rate_pct':'{:.1f}','resolution_rate_pct':'{:.1f}','median_latency_s':'{:.3f}','p95_latency_s':'{:.3f}','avg_cost_usd':'{:.5f}'}))
left,right=st.columns(2)
with left:
    st.subheader('Waktu respons (detik)')
    st.bar_chart(summary[['median_latency_s','p95_latency_s']],stack=False)
with right:
    st.subheader('Biaya (USD/pertanyaan)')
    st.bar_chart(summary[['avg_cost_usd']],stack=False)
st.subheader('Analisis kategori')
options=sorted(category.category.unique())
selected=st.multiselect('Kategori yang ditampilkan',options,default=options)
selected_data=category[category.category.isin(selected)]
if not selected:
    st.info('Pilih minimal satu kategori untuk menampilkan detail.')
else:
    st.caption('Answer pass rate (%). Setiap kategori memiliki 50 kasus per versi pada dataset latihan.')
    st.bar_chart(selected_data.pivot(index='category',columns='model_version',values='pass_rate_pct'),stack=False)
    st.dataframe(selected_data[['model_version','category','n']])
    st.subheader('Kasus gagal pada kategori pilihan')
    st.dataframe(failed[failed.category.isin(selected)])
st.caption('Tulis rekomendasi dan batas klaim pada workspace/jawaban.md. Dashboard ini belum mengukur kepuasan pengguna nyata.')
