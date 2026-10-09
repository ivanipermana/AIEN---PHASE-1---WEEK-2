# Hands-on 60 menit: Data Quality untuk AI dengan GX Core

## Hasil belajar
Peserta menjalankan profiling dan empat aturan GX, menginvestigasi satu root cause,
memverifikasi perbaikan, serta menentukan tindak lanjut dan peran governance.

## Mulai
1. Clone folder hands-on dan buka di VS Code.
2. Selesaikan setup di SETUP.md sebelum kelas.
3. Buka Hands_On_Peserta.ipynb dan pilih kernel virtual environment.
4. Jalankan sel berurutan. Lengkapi bagian TODO. Kerangka GX sudah disediakan.
5. Isi LAPORAN_PESERTA.md dan simpan notebook beserta outputnya.

## Alokasi waktu
| Menit | Aktivitas |
|---|---|
| 00–05 | Konteks dan data dictionary |
| 05–15 | Profiling |
| 15–30 | Empat Expectations dan Checkpoint |
| 30–40 | Data Docs dan investigasi join |
| 40–50 | Perbaikan dan validasi ulang |
| 50–60 | Laporan, governance, debrief |

## Deliverable
- Notebook lengkap dengan output.
- reports/before_summary.csv dan reports/after_summary.csv.
- LAPORAN_PESERTA.md yang berisi bukti dan rekomendasi.
- Hasil GX JSON dan Data Docs lokal dibuat otomatis setelah validasi.

## Batas latihan
Tidak membangun model, tidak melakukan profiling otomatis GX, dan tidak memasang orkestrator.
Profiling menggunakan pandas. GX memvalidasi aturan; peserta menelusuri root cause dengan data sumber.
Satu perbaikan dapat meninggalkan kegagalan aturan lain. Jangan mengubah threshold agar batch terlihat lulus.

## Referensi
- https://docs.greatexpectations.io/docs/core/connect_to_data/dataframes/
- https://docs.greatexpectations.io/docs/core/trigger_actions_based_on_results/create_a_checkpoint_with_actions/
