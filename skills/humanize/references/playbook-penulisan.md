# Playbook Penulisan Ulang (v1.0)

Resep eksekusi untuk `id-style-rewriter` (strict) dan `humanize-id-monolith`
(fast). Taksonomi menjawab "apa yang salah"; playbook menjawab "bagaimana
memperbaikinya tanpa merusak".

## Urutan pengerjaan (per paragraf)

1. **D dulu** (idiom khas AI) — menghapus klise memendekkan kalimat,
   memudahkan langkah berikutnya.
2. **A → I → G** (terjemahanisme, nomina kosong, hedging) — perbaikan
   tataran frasa.
3. **H → F** (konjungsi, modifikasi) — penipisan.
4. **B → C → J** (istilah Inggris, struktur, dekorasi) — tataran dokumen.
5. **E terakhir** (ritme) — baru bisa dinilai setelah isi kalimat stabil.

## Aturan edit bedah

- Satu edit = satu span temuan. Jangan menulis ulang kalimat yang tidak
  mengandung temuan.
- Setiap edit dicatat berpasangan (sebelum → sesudah) untuk audit dan
  kemungkinan rollback per-edit.
- Bila dua temuan tumpang tindih dalam satu kalimat, tangani sekali jalan
  dengan satu edit gabungan — jangan dua edit bertumpuk.
- Pantau change-rate berjalan; mendekati 30% → prioritaskan hanya S1 sisa.

## Resep per kategori

| Kategori | Resep inti | Jebakan yang harus dihindari |
|---|---|---|
| A | Kembalikan ke struktur predikat Indonesia: pelaku-di-depan, verba asli | Jangan mengaktifkan pasif yang memang lazim (laporan resmi) |
| B | Padankan sekali, lalu konsisten Indonesia | Jangan menerjemahkan istilah teknis mapan |
| C | Prosa > daftar untuk teks naratif | Data tabular biarkan tetap daftar/tabel |
| D | Hapus, atau ganti dengan klaim spesifik dari isi teks | Jangan mengarang fakta baru sebagai pengganti klise |
| E | Sisipkan variasi panjang dengan MEMECAH/MENGGABUNG kalimat yang ada | Jangan menambah kalimat berisi gagasan baru |
| F | Verba > nominalisasi; satu pengintensif cukup | Jangan mengganti kata yang mengubah kadar klaim |
| G | Satu pelunak maksimal per klaim; tegaskan bila teks sumber tegas | Jangan menegaskan klaim yang penulis memang buat ragu |
| H | Buang konjungsi pembuka; andalkan urutan gagasan | Sisakan penghubung pada lompatan logika sungguhan |
| I | Buang nomina kosong, langsung ke subjek/predikat nyata | — |
| J | Penekanan visual = maksimal 2 per dokumen | Jangan buang formatting struktural (heading sah, kode) |

## Tabel toleransi genre

| Pola | Artikel | Laporan | Blog | Surat resmi |
|---|---|---|---|---|
| Bullet (C-3) | rendah | tinggi | sedang | rendah |
| Emoji (C-2) | 0 | 0 | rendah | 0 |
| "dalam rangka" (A-9) | hapus | boleh 1× | hapus | boleh 1× |
| Pasif (A-1) | rendah | sedang–tinggi | rendah | sedang |
| Partikel percakapan | 0 | 0 | boleh (register santai) | 0 |
| Bold (J-1) | 1–2 | sedang | sedang | 0 |

## Pass register (bila diminta)

Jalankan SETELAH seluruh langkah di atas selesai, mengikuti
`tabel-register.md`. Konversi register di luar hitungan change-rate, tetapi
fidelity audit tetap berlaku penuh.
