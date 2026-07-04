# Quick Rules ID — rulebook ringkas mode Fast (v1.0)

Dipakai agen `humanize-id-monolith` untuk deteksi + penulisan ulang + cek
mandiri dalam satu panggilan. Hanya pola S1·S2 inti; taksonomi lengkap ada
di `taksonomi-ai-tell.md`. Prinsip: definisi 1 baris + perbaikan 1 baris.

**Jangan-Sentuh (deteksi & penulisan ulang):** nama diri/produk/lembaga,
angka·tanggal·satuan, kutipan langsung dalam tanda petik, teks hukum,
notasi matematika/kimia/statistik, akronim standar (AI·API·GPU·LLM·MCP dll).

**Pagar over-polish:** perubahan >30% = peringatan, >50% = hentikan + rollback.

---

## A. Terjemahanisme

| ID | Pola | Sev | Perbaikan |
|---|---|---|---|
| A-1 | Pasif "di-" saat pelaku jelas & aktif lebih alami | S2 | Jadikan pelaku subjek ("Keputusan diambil oleh manajemen" → "Manajemen mengambil keputusan") |
| A-2 | "yang mana" sebagai penghubung | S1 | Hapus atau pecah kalimat |
| A-3 | "di mana" non-lokasi ("sistem di mana pengguna…") | S1 | "yang", pecah kalimat, atau "tempat" jika benar lokasi |
| A-4 | "melakukan + nomina" ("melakukan pembelian") | S1 | Kembalikan ke verba ("membeli") |
| A-5 | "memiliki" berulang 3×+ | S2 | "punya", "ber-", atau restrukturisasi ("memiliki dampak" → "berdampak") |
| A-6 | "adalah merupakan" | S1 | Pilih salah satu |
| A-7 | "dikarenakan" | S2 | "karena" |
| A-8 | "terhadap" untuk objek non-lawan ("pemahaman terhadap") | S2 | "tentang", "akan", atau langsung objek |
| A-9 | "dalam rangka" | S2 | "untuk" |
| A-10 | "tersebut" 4×+ per paragraf | S2 | "itu", ganti nomina, atau hapus |

## B. Istilah Inggris berlebih

| ID | Pola | Sev | Perbaikan |
|---|---|---|---|
| B-1 | Kurung Inggris tiap kemunculan ("kecerdasan buatan (Artificial Intelligence)" berulang) | S2 | Padankan sekali di kemunculan pertama, selanjutnya Indonesia saja |
| B-2 | Kata Inggris padahal padanan lazim ada ("improve", "impactful") | S2 | Terjemahkan; istilah teknis standar dibiarkan |

## C. Pola struktural

| ID | Pola | Sev | Perbaikan |
|---|---|---|---|
| C-1 | "Pertama, … Kedua, … Ketiga, …" mekanis | S2 | Leburkan ke prosa atau sisakan penomoran alami |
| C-2 | Emoji di genre artikel/laporan/surat-resmi | S1 | Hapus semua |
| C-3 | Bullet berlebihan pada teks naratif | S2 | Gabungkan jadi paragraf prosa |
| C-4 | Heading pola "X: Y" berulang | S1 | Heading pendek biasa |
| C-5 | Indeks "(1) … (2) … (3)" dalam kalimat | S2 | Leburkan atau baris baru sederhana |

## D. Idiom khas AI

| ID | Pola | Sev | Perbaikan |
|---|---|---|---|
| D-1 | "Kesimpulannya," / "Sebagai kesimpulan" | S1 | Hapus; biarkan paragraf penutup menutup sendiri |
| D-2 | "Tidak/Tak dapat dipungkiri (bahwa)" | S1 | Hapus atau ganti klaim konkret |
| D-3 | "Di era digital/modern (yang semakin berkembang)" | S1 | Hapus pembuka klise; mulai dari inti |
| D-4 | "Penting untuk dicatat/diingat/dipahami bahwa" | S1 | Hapus; langsung isinya |
| D-5 | "memainkan peran(an) penting" | S1 | Nyatakan perannya secara konkret |
| D-6 | "Seiring (dengan) berkembangnya/perkembangan …" | S1 | Hapus atau ganti sebab konkret |
| D-7 | Kata hype ("revolusioner", "luar biasa", "menakjubkan", "game-changer") 3×+ | S1 | Ganti fakta/angka konkret |
| D-8 | Penutup ajakan generik ("Mari kita…", "Sudah saatnya kita…") | S2 | Tutup dengan pernyataan biasa |
| D-9 | "bukan hanya X, tetapi juga Y" berulang | S2 | Sisakan satu; sisanya kalimat biasa |

## E. Keseragaman ritme

| ID | Pola | Sev | Perbaikan |
|---|---|---|---|
| E-1 | Panjang kalimat seragam (stdev < 5 kata) | S2 | Sisipkan 1–2 kalimat pendek + 1 panjang per bagian |
| E-2 | Awalan kalimat sama berulang 3×+ | S2 | Variasikan struktur pembuka |
| E-3 | Register campur (baku + gaul) dalam satu paragraf | S2 | Konsisten satu register per teks |

## F. Modifikasi berlebih

| ID | Pola | Sev | Perbaikan |
|---|---|---|---|
| F-1 | "sangat" / "sekali" 4×+ | S2 | Hapus atau ganti kata yang lebih tepat |
| F-2 | Rantai nominalisasi pe-an/ke-an/-isasi/-itas ("pengimplementasian kebijakan") | S2 | Kembalikan ke verba ("menerapkan kebijakan") |
| F-3 | Sinonim ganda ("penting dan krusial") | S2 | Pilih satu |
| F-4 | "secara + adjektiva" 3×+ ("secara signifikan/efektif") | S2 | Adverbia langsung atau hapus |

## G. Hedging

| ID | Pola | Sev | Perbaikan |
|---|---|---|---|
| G-1 | "dapat dikatakan bahwa" | S1 | Hapus; katakan langsung |
| G-2 | Tumpukan pelunak ("mungkin dapat cenderung") | S2 | Sisakan satu pelunak atau tegaskan |
| G-3 | "berpotensi untuk dapat" | S2 | "bisa" / "berpotensi" saja |
| G-4 | Keseimbangan aman tanpa sikap ("di satu sisi… di sisi lain…" berulang) | S2 | Ambil posisi di 1–2 titik |

## H. Konjungsi awal kalimat

| ID | Pola | Sev | Perbaikan |
|---|---|---|---|
| H-1 | "Selain itu / Oleh karena itu / Dengan demikian / Di sisi lain / Lebih lanjut" 5×+ | S1 | Buang mayoritas; biarkan alur kalimat mengalir |
| H-2 | "Hal ini" pembuka kalimat 3×+ | S1 | Sebut subjek aslinya |
| H-3 | "Dalam hal ini / Dalam konteks ini" 2×+ | S2 | Hapus atau leburkan |

## I. Nomina kosong

| ID | Pola | Sev | Perbaikan |
|---|---|---|---|
| I-1 | "hal ini menunjukkan bahwa" | S2 | "artinya", atau langsung simpulan |
| I-2 | "merupakan suatu/sebuah" | S2 | "adalah" atau langsung predikat |
| I-3 | "dengan adanya" / "adanya" berlebihan | S2 | Hapus "adanya" ("dengan adanya pelatihan" → "dengan pelatihan") |
| I-4 | Penutup "…yang perlu diperhatikan" | S2 | Nyatakan apa yang harus dilakukan |

## J. Dekorasi visual

| ID | Pola | Sev | Perbaikan |
|---|---|---|---|
| J-1 | **Bold** berlebihan di badan teks | S2 | Sisakan 1–2 penekanan kunci |
| J-2 | Tanda kutip penekanan 5×+ | S1 | Sisakan yang benar-benar kutipan/istilah |
| J-3 | Em-dash (—) berulang | S2 | Koma, titik, atau pecah kalimat |

---

## Cek mandiri (6 poin — wajib setelah penulisan ulang)

Satu poin gagal = rollback edit terkait, tulis ulang, cek lagi (maks 1 putaran).

1. **Nama diri, angka, tanggal, kutipan 100% sama** dengan teks asli
2. **Perubahan ≤30%** (>50% = hentikan pekerjaan)
3. **Genre tidak bergeser** (artikel tetap artikel, laporan tetap laporan)
4. **Register dipertahankan** (kecuali user minta konversi)
5. **Sisa S1 = 0** (D-1…D-7, A-2, A-3, A-4, A-6, C-2, C-4, G-1, H-1, H-2, J-2)
6. **Tidak menambah gaya baru** (tak ada metafora/retorika yang tidak ada
   di asli; `suara: hidup` → hanya tambahan yang diizinkan suara-hidup.md,
   tetap tanpa fakta/klaim baru)

## Grade (nilai mandiri)

- **A**: S1 sisa 0, S2 sisa ≤2, perubahan 10–25%, cek mandiri 6/6
- **B**: S1 sisa 0, S2 sisa ≤4, cek mandiri ≥5/6
- **C**: S1 sisa 1–2 atau cek mandiri ≤4 — sarankan `--strict`
- **D**: S1 sisa ≥3 atau perubahan >50% — tahan, minta tinjauan manusia
