# Lembar Jawaban P1W3D5

Nama / pasangan: ...  
Tanggal: ...

## 1. Model data (05–15)

Pilih document, key-value, graph, wide-column, vector, atau relational.

| Fitur dan pola akses | Pilihan | Alasan / trade-off |
|---|---|---|
| Katalog produk, atribut antar kategori berbeda | ... | ... |
| Session login, lookup berdasarkan session ID | ... | ... |
| Telusuri akun-perangkat-alamat beberapa lompatan untuk fraud | ... | ... |
| Log besar, append intensif, dibaca per user dan waktu | ... | ... |
| Cari produk berdasarkan kemiripan makna | ... | ... |
| Pembayaran, transaksi lintas saldo dan catatan pembayaran | ... | ... |

Contoh atribut baru yang Anda tambahkan di dokumen produk: ...
Apakah model data yang fleksibel tetap memerlukan validasi? Mengapa? ...

## 2. Replication dan partition (15–30)

Prediksi stok yang dibaca C setelah A-B menerima write 7: ...

| Kondisi | Kebijakan | Status | Stok / alasan penolakan |
|---|---|---|---|
| C terisolasi | serve_local | ... | ... |
| C terisolasi | require_majority | ... | ... |
| C sudah disinkronkan | serve_local | ... | ... |

A-B terus menerima write dalam simulasi. Apa dampaknya pada pengguna di sisi C? ...
Untuk stok checkout dan katalog deskripsi produk, apakah Anda memilih kebijakan yang sama? ...
Mengapa mengembalikan error belum berarti memenuhi availability dalam CAP? ...

## 3. Sharding (30–45)

Catat JUMLAH REQUEST per shard, bukan hanya jumlah produk.

| Traffic | Strategi | Shard 0 | Shard 1 | Shard 2 | Porsi shard terbesar |
|---|---|---|---|---|---|
| Flash sale | Range | ... | ... | ... | ... |
| Flash sale | Hash | ... | ... | ... | ... |
| Hot product | Range | ... | ... | ... | ... |
| Hot product | Hash | ... | ... | ... | ... |

Mengapa jumlah produk merata belum tentu berarti beban request merata? ...
Mengapa hashing belum mengatasi satu produk yang sangat populer? ...
Usulkan satu mitigasi untuk hot product dan jelaskan batasnya: ...
Bedakan tujuan replication dan sharding dalam satu kalimat masing-masing: ...

## 4. Quorum (45–55)

Setiap kasus dimulai ulang: A=B=C berisi stok 10. Write 7 hanya mencapai A-B.
Parameter R adalah jumlah respons yang diperlukan, bukan jumlah node total.

| W | R | Node baca yang terjangkau | Status write | Status read | Stok terbaca |
|---|---|---|---|---|---|
| 1 | 1 | C | ... | ... | ... |
| 2 | 2 | C | ... | ... | ... |
| 2 | 2 | B,C | ... | ... | ... |
| 3 | 1 | A,B | ... | ... | ... |

Ulangi kasus pilihan Anda dengan **write hanya mencapai C**, lalu catat W, R,
status write, node baca, dan status read: ...

Saat satu node terisolasi, apa konsekuensi menaikkan W atau R? ...
Mengapa W+R>N belum cukup untuk mengklaim semua sistem pasti linearizable? ...

## 5. Exit ticket (55–60)

1. Pilih penyimpanan untuk satu fitur AI marketplace dan jelaskan pola aksesnya: ...
2. Apa trade-off yang Anda pilih untuk pembacaan stok saat partition? ...
3. Apakah eksperimen ini membuktikan failover otomatis atau kecepatan database nyata? Jelaskan: ...

Checklist sebelum mengumpulkan:
- [ ] Nama terisi dan keenam pilihan model punya alasan.
- [ ] Hasil replication, empat distribusi sharding, dan empat kasus quorum tercatat.
- [ ] Eksperimen tambahan write ke C dicatat.
- [ ] Notebook tersimpan dengan output, exit ticket terisi, dan `.venv` tidak ikut ZIP.
