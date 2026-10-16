# Hands-on 60 Menit: Terraform S3 dan GitHub CI

Target: peserta membuat bucket S3 dengan Terraform, mendeteksi drift, dan mengirim perubahan melalui PR dengan pemeriksaan otomatis.

Gunakan starter code di folder `infra/` dan workflow `.github/workflows/terraform-check.yml` dari paket ini. Kerjakan berpasangan sebagai engineer dan reviewer. Setiap peserta mengelola bucket dan state masing-masing.

## Persiapan peserta sebelum kelas

Selesaikan persiapan ini sebelum waktu latihan 60 menit dimulai.

1. Pastikan Terraform 1.16.6, Git, AWS CLI, editor, dan akun GitHub tersedia.
2. Login ke akun AWS sandbox yang ditentukan pengajar. Jalankan `aws sts get-caller-identity` dan pastikan akun benar. Jika izin belum tersedia, hubungi pengajar sebelum kelas.
3. Ekstrak paket. Buka folder `paket-peserta-p1w3d4` di editor dan terminal.
4. Buat repository GitHub **kosong** tanpa README otomatis. Jangan memakai repository lain yang sudah berisi pekerjaan.
5. Jalankan perintah persiapan berikut dari root paket:

```bash
git init -b main
cd infra
cp terraform.tfvars.example terraform.tfvars
```

Edit `infra/terraform.tfvars`: ganti `bucket_name` dengan nama unik, misalnya `aien-p1w3d4-namaanda-20261016-7ab3`. Gunakan huruf kecil, angka, dan tanda hubung. Biarkan environment `dev`.

Dari folder `infra/`:

```bash
terraform init
terraform validate
cd ..
git add .
git diff --cached --name-only
```

Pastikan `.terraform.lock.hcl` masuk daftar, sedangkan `.terraform/`, `terraform.tfvars`, state, dan saved plan tidak masuk. Lalu:

```bash
git commit -m "chore: prepare terraform lab"
git remote add origin https://github.com/USERNAME/NAMA-REPO.git
git push -u origin main
```

Ganti URL dengan repository Anda. Pastikan GitHub Actions aktif. Jangan memasukkan credential ke kode atau Git. Workflow menggunakan provider yang dipilih dalam lock file hasil init.

Satu operator memakai satu local state untuk bucket miliknya. Pasangan mereview PR, tidak menjalankan apply dari state lokal terpisah untuk bucket yang sama. AWS dapat mengenakan biaya; bucket tetap kosong dan wajib dihapus pada akhir latihan.

## Jadwal

| Menit | Kegiatan | Hasil |
|---|---|---|
| 00–05 | Baca konfigurasi dan prediksi plan | Mengenali provider, resource, dependency |
| 05–20 | Plan, apply, lalu plan ulang | Bucket terbentuk dan no-change plan |
| 20–30 | Simulasi drift tag lewat Console | Drift terdeteksi dan diperbaiki |
| 30–45 | Feature branch, PR, dan CI | PR mendapat review dan fmt/validate lulus |
| 45–50 | Merge dan apply dari main | Tag Owner diterapkan |
| 50–60 | Destroy dan refleksi | Resource lab dihapus |

## 00–05: Baca desired state

Buka `infra/main.tf`. Identifikasi bucket, tags, serta public access block.

Pertanyaan: mengapa `aws_s3_bucket_public_access_block.data_lake` merujuk `aws_s3_bucket.data_lake.id`?

Jawaban: referensi membentuk dependency, sehingga Terraform membuat bucket sebelum memasang public access block. Urutan penulisan blok tidak menentukan urutan eksekusi.

## 05–20: Provisioning

Dari root repository:

```bash
cd infra
terraform validate
terraform plan -out=create.tfplan
```

Baca plan. Ekspektasi: `2 to add, 0 to change, 0 to destroy`. Ada dua resource Terraform, tetapi hanya satu bucket S3.

```bash
terraform apply create.tfplan
terraform output
terraform plan
```

Saved plan langsung dieksekusi tanpa prompt tambahan. Jalankan setelah memeriksa bahwa isinya hanya resource lab.

Ekspektasi terakhir: `No changes`. Periksa bucket di AWS Console. Jangan mengunggah dataset agar cleanup tetap singkat.

`init` telah dilakukan saat persiapan untuk mengunduh provider dan menyiapkan working directory. Peserta tetap menjalankan plan dan apply sendiri.

## 20–30: Drift

Di AWS Console, ubah hanya tag `Environment` pada bucket lab dari `dev` ke `manual-change`.

```bash
terraform state list
terraform plan -out=repair.tfplan
```

Perhatikan plan yang mengembalikan tag ke `dev`. Pastikan tidak ada bucket yang dihapus atau diganti.

```bash
terraform apply repair.tfplan
terraform plan
```

Checkpoint: plan kembali `No changes`. Jelaskan bahwa resource aktual menyimpang dari konfigurasi. Ini tidak selalu berarti file state rusak.

## 30–45: PR dan CI

Kembali ke root repository:

```bash
cd ..
git switch -c feat/add-owner-tag
```

Tambahkan satu tag pada `infra/main.tf`:

```hcl
    Owner = "nama-anda"
```

Lalu:

```bash
cd infra
terraform fmt
terraform validate
terraform plan
cd ..
git add infra/main.tf
git commit -m "feat: add owner tag to data lake"
git push -u origin feat/add-owner-tag
```

Buka PR ke `main` dan tulis ringkasan plan: perubahan tag in-place, tanpa create atau destroy. Pasangan memberi satu komentar review mengenai dampak plan atau keamanan konfigurasi. Contributor merespons sebelum merge.

Workflow bawaan berjalan otomatis untuk PR:

```text
terraform fmt -check -recursive
terraform init -backend=false -input=false -lockfile=readonly
terraform validate
```

CI ini memeriksa format dan konfigurasi tanpa credential AWS. Plan AWS dijalankan lokal dan ringkasannya direview di PR. Authenticated plan CI membutuhkan akses AWS serta state bersama dan menjadi materi lanjutan.

Checkpoint: satu PR dengan komentar reviewer dan CI hijau. Percobaan sengaja membuat CI gagal dikeluarkan dari sesi satu jam. Jika CI gagal karena format, jalankan fmt, commit, dan push ulang. Jika ada antrean runner, gunakan waktu tunggu untuk review dan refleksi.

## 45–50: Deploy perubahan approved

Setelah review dan CI lulus, merge PR. Dari root repository:

```bash
git switch main
git pull --ff-only
cd infra
terraform plan -out=approved.tfplan
terraform apply approved.tfplan
```

Periksa tag Owner di Console. Merge mengubah kode yang disetujui, sedangkan apply mengubah resource aktual.

Jika PR atau CI belum selesai pada menit 50, prioritaskan cleanup. Catat tahap kolaborasi yang belum selesai dan lanjutkan review PR setelah kelas tanpa melakukan provisioning lagi.

## 50–60: Cleanup dan refleksi

Dari `infra/`:

```bash
terraform plan -destroy -out=cleanup.tfplan
terraform apply cleanup.tfplan
terraform state list
```

Baca destroy plan sebelum apply. Ekspektasi: hanya dua resource lab dihapus dan state list kosong. `terraform destroy` adalah alternatif dengan prompt konfirmasi; cukup pilih satu cara.

Jika bucket tidak kosong, hapus hanya objek percobaan yang Anda buat sebelum membuat ulang destroy plan. Jangan menghapus file state untuk melakukan cleanup.

Jawab singkat:

1. Mengapa plan kedua setelah apply menunjukkan no changes?
2. Apa yang terjadi ketika tag diubah di luar Terraform?
3. Mengapa state tidak boleh di-commit ke Git?
4. Mengapa CI hijau dan merge PR belum berarti resource telah berubah?

## Bukti pengumpulan

- Ringkasan plan awal dan no-change plan.
- Screenshot/ringkasan drift tag yang terdeteksi.
- Link PR dengan komentar review dan hasil CI.
- Bukti state list kosong setelah cleanup.

Jangan kumpulkan state, credential, atau binary saved plan.

## Batas cakupan

Latihan ini mencakup desired state, dependency, plan/apply, drift, Git review, CI format/validate, dan destroy. Remote backend, locking, authenticated plan CI, eksperimen CI gagal, dan auto-apply tidak masuk jadwal satu jam. Untuk kerja tim pada resource yang sama, pengajar akan membahas remote state dan locking pada sesi lanjutan.
