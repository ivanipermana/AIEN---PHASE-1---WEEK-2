# Bantuan Singkat

| Kendala | Langkah berikutnya |
|---|---|
| BucketAlreadyExists | Ganti nama bucket dengan nama unik di terraform.tfvars dan buat ulang plan |
| AWS token expired | Login ulang dengan metode yang diberikan pengajar |
| AccessDenied | Periksa akun dengan aws sts get-caller-identity, lalu minta pengajar memeriksa izin |
| Push ditolak | Pastikan URL remote dan autentikasi GitHub benar; gunakan repository kosong |
| CI fmt gagal | Jalankan terraform fmt di infra, commit perubahan, lalu push |
| CI init readonly gagal | Pastikan infra/.terraform.lock.hcl sudah di-commit. Jika checksum platform belum tersedia, jalankan perintah di bawah dan commit hasilnya |
| CI belum muncul | Pastikan PR menuju main dan workflow sudah ada di repository |
| Destroy gagal: bucket tidak kosong | Hapus hanya objek percobaan milik lab, lalu buat ulang destroy plan |

Untuk checksum platform CI, dari `infra/`:

```bash
terraform providers lock -platform=linux_amd64 -platform=darwin_arm64 -platform=windows_amd64
```

Perintah ini membutuhkan koneksi ke registry. Commit perubahan `.terraform.lock.hcl`, lalu push ulang. Jangan hapus state atau menggunakan force-unlock untuk mencoba memperbaiki error.

Pada menit 50, prioritaskan cleanup. Jika PR/CI belum selesai, catat kendala pada lembar pengumpulan. Review kode dapat dilanjutkan setelah resource lab dihapus.
