# Suara Hidup — pass suara opsional (v1.0)

Dibaca HANYA bila `suara: hidup` diminta atau `contoh-gaya` diberikan.
Prinsip (diadaptasi dari blader/humanizer §Personality and Soul): teks yang
bersih dari AI-tell tapi tanpa suara tetap terbaca seperti mesin — steril
juga tell. Pass ini menambah denyut, TANPA menambah fakta.

## Kapan berlaku

- `suara: hidup` diminta user. Default `netral` = pass ini dilewati.
- Genre blog/artikel opini: penuh. Laporan/surat-resmi: HANYA variasi
  ritme — netral-datar memang suara manusia yang benar di genre itu.

## Tanda teks bersih-tapi-mati (sasaran pass ini)

- Semua kalimat panjang dan strukturnya seragam
- Tidak ada sikap; hanya melaporkan netral
- Tidak ada pengakuan ragu atau ambivalen
- Terlalu rapi: tidak ada jeda, selingan, atau napas alami

## Yang BOLEH

1. **Ritme**: pecah, pendekkan, panjangkan. Kalimat pendek menohok. Lalu
   satu kalimat panjang yang santai jalannya dan tiba di tujuannya sendiri.
2. **Sikap ringan pada klaim yang SUDAH ada**: "Angka ini menarik" boleh
   jadi "Angkanya lumayan mengejutkan" — arah penilaian tidak berubah.
3. **Selingan singkat** (koma atau kurung, bukan em-dash) yang hanya
   merestrukturisasi isi yang ada: "(setidaknya sejauh datanya bicara)".
4. **Pengakuan ketidakpastian** yang sudah tersirat di teks asli.

## Yang TETAP HARAM

- Fakta, angka, contoh, anekdot, metafora, atau klaim BARU.
- Sikap yang membalik atau menggeser arah penilaian teks asli.
- Humor atau kegenitan di genre formal.
- Register bergeser (kecuali `register:` memang diminta).
- Emoji, em-dash, atau pola AI-tell mana pun dari quick-rules/taksonomi.

## Kalibrasi contoh gaya (`contoh_gaya_path`, opsional)

Bila user memberi sampel tulisannya sendiri, baca dulu dan catat:

- pola panjang kalimat (pendek menghentak? panjang mengalir? campur?)
- level diksi (santai? akademis? di antaranya?)
- kebiasaan tanda baca dan frasa khas yang berulang
- cara membuka paragraf dan berpindah topik (penghubung eksplisit? langsung?)

Tiru pola itu pada SEMUA edit (temuan, FLU, SUA) — jangan "menaikkan kelas"
diksi user. Kalibrasi ini boleh dipakai meski `suara: netral`: ia hanya
mengarahkan pilihan kata/ritme pada edit yang sudah diizinkan, bukan
menambah edit baru. Tanpa sampel → suara alami bervariasi (default).

## Pencatatan

Setiap edit pass ini dicatat `SUA-n` (pola `"SUA"`), masuk hitungan
change-rate — ambang 30%/50% tetap berlaku. Mode strict: fidelity auditor
tetap memeriksa semua edit SUA seperti edit lain.
