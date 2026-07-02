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
6. **Pass kelancaran** — setelah semua kategori selesai: baca ulang sebagai
   penutur asli, perhalus kalimat yang masih berkerangka Inggris
   (lihat §Pass kelancaran di bawah).

## Aturan edit bedah

- Satu edit = satu span temuan. Jangan menulis ulang kalimat yang tidak
  mengandung temuan — kecuali dalam pass kelancaran (§ di bawah), yang
  punya aturan dan pencatatannya sendiri.
- **Unit penulisan ulang adalah KALIMAT, bukan kata.** Mengganti kata per
  usulan pola lalu meninggalkan urutan kata di sekitarnya = kerangka
  kalimat Inggris tetap utuh dan hasilnya masih terasa AI. Setelah
  menerapkan usulan, susun ulang kalimatnya bila perlu.
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

## Pass kelancaran (wajib, sebelum register)

Model bahasa menulis Indonesia dengan kerangka kalimat Inggris — menghapus
pola per taksonomi saja tidak cukup, karena kalimat tanpa temuan tetap
membawa urutan kata khas mesin. Karena itu, setelah seluruh edit berbasis
temuan selesai:

1. Baca ulang seluruh hasil sebagai penutur asli.
2. Kalimat yang masih terasa terjemahan (urutan kata kaku, keterangan
   menumpuk di akhir ala Inggris, anak kalimat menggantung) BOLEH
   diperhalus meski tidak match pola apa pun.
3. Batasnya keras: makna, fakta, angka, istilah, register, dan genre tetap;
   tanpa metafora/gaya baru; daftar Jangan-Sentuh tetap berlaku; edit
   tercatat berpasangan dengan ID `FLU-1`, `FLU-2`, … dan MASUK hitungan
   change-rate (berbeda dari pass register).

### Kalibrasi rasa (contoh, bukan pola)

- "Teknologi ini memberikan kemampuan kepada pengguna untuk mengelola
  keuangan mereka dengan lebih efektif."
  → "Teknologi ini membantu pengguna mengatur keuangan dengan lebih baik."
- "Proses ini memerlukan waktu yang tidak sebentar dan komitmen yang
  berkelanjutan dari seluruh tim."
  → "Prosesnya makan waktu, dan seluruh tim harus berkomitmen terus."

## Pass register (bila diminta)

Jalankan SETELAH seluruh langkah di atas selesai, mengikuti
`tabel-register.md`. Konversi register di luar hitungan change-rate, tetapi
fidelity audit tetap berlaku penuh.
