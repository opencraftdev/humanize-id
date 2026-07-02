# Taksonomi AI-Tell Bahasa Indonesia — SSOT (v1.0)

Sumber kebenaran tunggal untuk semua pola "gaya khas AI" dalam teks bahasa
Indonesia. Mode strict memakai file ini; mode fast memakai ringkasannya
(`quick-rules-id.md`). ID di kedua file identik 1:1.

**Severity:**
- **S1 — bukti kuat**: satu kemunculan sudah menandakan AI. Wajib hilang.
- **S2 — kuat**: 1–2× wajar, 3×+ berulang wajib dikurangi.
- **S3 — lemah**: bermasalah hanya bila bertumpuk dengan pola lain.

**Siklus bukti (untuk versi berikutnya):** kumpulkan sampel keluaran AI
(ChatGPT/Claude/Gemini) per genre → hitung frekuensi kandidat pola pada
sampel AI vs tulisan manusia → promosikan ke taksonomi hanya bila rasio
frekuensinya timpang → turunkan/tahan pola yang tidak terbukti.

---

## A. Terjemahanisme (calque Inggris)

### A-1 · S2 — Pasif "di-" berlebihan
**Definisi:** Kalimat pasif dipakai saat pelaku jelas dan bentuk aktif lebih alami — pola kalimat Inggris pasif yang diterjemahkan mentah.
**Contoh:** "Keputusan itu diambil oleh manajemen setelah rapat." → "Manajemen mengambil keputusan itu setelah rapat."
**Catatan deteksi:** Sinyal kuat bila ada frasa "oleh + pelaku". Pasif tanpa pelaku yang memang lazim di laporan formal bukan target.

### A-2 · S1 — "yang mana" sebagai penghubung
**Definisi:** Calque "which" sebagai penyambung antarklausa; bukan bahasa Indonesia baku maupun percakapan alami.
**Contoh:** "Penjualan turun 20%, yang mana hal ini mengkhawatirkan." → "Penjualan turun 20%. Itu mengkhawatirkan."
**Catatan deteksi:** "yang mana" untuk pertanyaan pilihan ("yang mana yang benar?") bukan target.

### A-3 · S1 — "di mana" non-lokasi
**Definisi:** Calque "where" untuk klausa relatif tanpa makna tempat.
**Contoh:** "Ini sistem di mana pengguna dapat berbagi berkas." → "Ini sistem yang memungkinkan pengguna berbagi berkas."
**Catatan deteksi:** "di mana" makna lokasi/tanya lokasi bukan target.

### A-4 · S1 — "melakukan + nomina"
**Definisi:** Calque "do/perform + noun"; verba dinominakan lalu digandeng "melakukan".
**Contoh:** "Tim melakukan pengujian terhadap fitur baru." → "Tim menguji fitur baru."
**Catatan deteksi:** Sah bila nominanya memang tak berverba lazim ("melakukan pelanggaran" boleh).

### A-5 · S2 — "memiliki" berulang
**Definisi:** Calque "have"; setiap kepemilikan/atribut dipaksa lewat "memiliki".
**Contoh:** "Produk ini memiliki keunggulan dan memiliki harga bersaing." → "Produk ini unggul dan harganya bersaing."
**Catatan deteksi:** Target bila ≥3× dalam satu bagian pendek.

### A-6 · S1 — "adalah merupakan"
**Definisi:** Kopula ganda; redundansi yang nyaris eksklusif keluaran mesin.
**Contoh:** "Jakarta adalah merupakan ibu kota." → "Jakarta adalah ibu kota."
**Catatan deteksi:** Cari substring literal.

### A-7 · S2 — "dikarenakan"
**Definisi:** Bentuk pasif kaku pengganti "karena", umum di keluaran AI formal.
**Contoh:** "Acara dibatalkan dikarenakan hujan." → "Acara dibatalkan karena hujan."

### A-8 · S2 — "terhadap" untuk objek netral
**Definisi:** Calque "towards/of"; "terhadap" dipakai untuk objek yang bukan sasaran/lawan.
**Contoh:** "pemahaman terhadap materi" → "pemahaman materi" / "paham akan materi".
**Catatan deteksi:** "terhadap" dengan makna berhadapan ("kekerasan terhadap anak") bukan target.

### A-9 · S2 — "dalam rangka"
**Definisi:** Frasa birokratis pengganti "untuk"; AI memakainya sebagai penanda formalitas.
**Contoh:** "dalam rangka meningkatkan mutu" → "untuk meningkatkan mutu".

### A-10 · S2 — "tersebut" bertubi
**Definisi:** Anafora "tersebut" pada hampir setiap rujukan ulang, calque "the/said".
**Contoh:** "Aplikasi tersebut… fitur tersebut… pengguna tersebut…" → variasikan: "itu", ulangi nominanya, atau hapus.
**Catatan deteksi:** ≥4 per paragraf.

## B. Istilah Inggris berlebih

### B-1 · S2 — Kurung Inggris tiap kemunculan
**Definisi:** Padanan Inggris dalam kurung diulang di tiap kemunculan istilah.
**Contoh:** "kecerdasan buatan (Artificial Intelligence)… kecerdasan buatan (Artificial Intelligence)…" → padankan sekali, selanjutnya Indonesia saja.

### B-2 · S2 — Inggris padahal ada padanan lazim
**Definisi:** Kata Inggris dibiarkan padahal padanan Indonesianya umum.
**Contoh:** "Kita perlu improve proses ini agar lebih impactful." → "Kita perlu memperbaiki proses ini agar dampaknya lebih terasa."
**Catatan deteksi:** Istilah teknis standar dan akronim (API, machine learning dalam konteks teknis) bukan target.

## C. Pola struktural

### C-1 · S2 — Enumerasi "Pertama/Kedua/Ketiga" mekanis
**Contoh:** tiga paragraf berturut dibuka "Pertama,… Kedua,… Ketiga,…" → leburkan ke prosa; sisakan urutan alami bila memang prosedur.

### C-2 · S1 — Emoji di teks formal
**Contoh:** "Mari kita mulai! 🚀" dalam artikel → hapus semua emoji di genre artikel/laporan/surat-resmi. Blog santai: kurangi drastis.

### C-3 · S2 — Bullet berlebihan pada teks naratif
**Contoh:** argumen esai dipecah jadi 7 bullet satu-baris → gabungkan jadi paragraf; bullet hanya untuk data yang memang daftar.

### C-4 · S1 — Heading "X: Y" berulang
**Contoh:** "Efisiensi: Kunci Pertumbuhan Bisnis Modern" berulang pola → heading pendek deklaratif.

### C-5 · S2 — Indeks "(1) (2) (3)" dalam kalimat
**Contoh:** "Ada tiga faktor: (1) biaya, (2) waktu, (3) kualitas." → "Ada tiga faktor: biaya, waktu, dan kualitas."

### C-6 · S3 — Panjang paragraf seragam
**Definisi:** Semua paragraf 3–4 kalimat rata. Sinyal lemah; masalah hanya bila bertumpuk dengan E-1/E-2.

## D. Idiom khas AI

### D-1 · S1 — "Kesimpulannya," / "Sebagai kesimpulan"
**Contoh:** "Kesimpulannya, transformasi digital tidak bisa dihindari." → hapus pembuka; biarkan kalimat penutup berdiri sendiri.

### D-2 · S1 — "Tidak dapat dipungkiri"
**Contoh:** "Tidak dapat dipungkiri bahwa teknologi mengubah hidup kita." → "Teknologi mengubah hidup kita." (atau klaim yang lebih spesifik)

### D-3 · S1 — Pembuka "Di era …"
**Contoh:** "Di era digital yang semakin berkembang pesat ini, …" → buang; mulai dari inti kalimat.

### D-4 · S1 — "Penting untuk dicatat/diingat/dipahami bahwa"
**Contoh:** "Penting untuk dicatat bahwa data ini belum final." → "Data ini belum final."

### D-5 · S1 — "memainkan peran(an) penting"
**Contoh:** "Media sosial memainkan peran penting dalam pemasaran." → "Separuh calon pembeli menemukan produk lewat media sosial." (peran dibuat konkret)

### D-6 · S1 — "Seiring berkembangnya …"
**Contoh:** "Seiring berkembangnya teknologi, kebutuhan berubah." → sebab konkret atau langsung klaimnya.

### D-7 · S1 — Kosakata hype ≥3×
**Contoh:** "revolusioner… luar biasa… menakjubkan…" → ganti fakta, angka, atau perbandingan konkret.

### D-8 · S2 — Penutup ajakan generik
**Contoh:** "Mari kita sambut masa depan dengan optimisme." → tutup dengan pernyataan/temuan, bukan seruan kosong.

### D-9 · S2 — "bukan hanya X, tetapi juga Y" berulang
**Contoh:** dua+ kemunculan → sisakan satu, sisanya kalimat lugas.

## E. Keseragaman ritme

### E-1 · S2 — Panjang kalimat seragam
**Definisi:** Deviasi standar panjang kalimat < ~5 kata (ukur dengan `metrics_id.sentence_length_stdev`).
**Perbaikan:** sisipkan kalimat pendek tegas dan satu kalimat panjang per bagian — tanpa menambah isi baru.

### E-2 · S2 — Awalan kalimat berulang
**Contoh:** tiga kalimat berturut dibuka subjek yang sama persis → variasikan pembuka (keterangan, klausa anak).

### E-3 · S2 — Register campur
**Contoh:** "Oleh karena itu, implementasinya nggak maksimal dong." → satu register konsisten; campuran baku+gaul dalam satu paragraf = tanda mesin.

### E-4 · S3 — Transisi paragraf selalu eksplisit
**Definisi:** Setiap paragraf dibuka penghubung eksplisit. Lemah sendiri; kuat bila bertumpuk H-1.

## F. Modifikasi berlebih

### F-1 · S2 — "sangat"/"sekali" spam
**Contoh:** ≥4 kemunculan → hapus atau pilih kata yang sudah mengandung intensitas ("sangat besar" → "masif" hanya jika sesuai register).

### F-2 · S2 — Rantai nominalisasi
**Contoh:** "pengimplementasian kebijakan pengoptimalisasian" → "menerapkan kebijakan untuk mengoptimalkan…". Ukur dengan `metrics_id.nominalization_density`.

### F-3 · S2 — Sinonim ganda
**Contoh:** "penting dan krusial", "cepat dan efisien" (saat maknanya sama) → pilih satu.

### F-4 · S2 — "secara + adjektiva" spam
**Contoh:** "secara signifikan… secara efektif… secara berkelanjutan…" ≥3× → adverbia langsung atau hapus.

## G. Hedging

### G-1 · S1 — "dapat dikatakan bahwa"
**Contoh:** "Dapat dikatakan bahwa proyek ini berhasil." → "Proyek ini berhasil."

### G-2 · S2 — Tumpukan pelunak
**Contoh:** "mungkin dapat cenderung meningkat" → satu pelunak maksimal: "cenderung meningkat".

### G-3 · S2 — "berpotensi untuk dapat"
**Contoh:** → "berpotensi" / "bisa".

### G-4 · S2 — Keseimbangan aman tanpa sikap
**Contoh:** "Di satu sisi… di sisi lain…" berulang tanpa pernah mengambil posisi → pertahankan nuansa, tapi beri sikap di 1–2 titik.

## H. Konjungsi awal kalimat

### H-1 · S1 — Konjungsi pembuka spam
**Definisi:** "Selain itu / Oleh karena itu / Dengan demikian / Di sisi lain / Lebih lanjut / Sementara itu" ≥5 kemunculan pembuka kalimat (ukur dengan `metrics_id.conjunction_initial_rate`).
**Perbaikan:** buang mayoritas; urutan gagasan yang baik tak butuh rambu di tiap kalimat.

### H-2 · S1 — "Hal ini" pembuka ≥3×
**Contoh:** "Hal ini menunjukkan… Hal ini berarti…" → sebut subjek aslinya: "Penurunan itu menunjukkan…".

### H-3 · S2 — "Dalam hal ini / Dalam konteks ini" ≥2×
**Perbaikan:** hapus atau leburkan ke kalimat.

## I. Nomina kosong

### I-1 · S2 — "hal ini menunjukkan bahwa"
**Contoh:** → "artinya," atau langsung simpulannya.

### I-2 · S2 — "merupakan suatu/sebuah"
**Contoh:** "Ini merupakan suatu pencapaian." → "Ini pencapaian." / "Ini sebuah pencapaian." (pilih satu penanda)

### I-3 · S2 — "(dengan) adanya" berlebihan
**Contoh:** "Dengan adanya pelatihan, karyawan berkembang." → "Dengan pelatihan, karyawan berkembang."

### I-4 · S2 — Penutup "…yang perlu diperhatikan"
**Contoh:** → nyatakan langsung apa yang harus diperhatikan/dilakukan.

### I-5 · S3 — "keberadaan" sebagai subjek abstrak
**Contoh:** "Keberadaan fitur ini membantu pengguna." → "Fitur ini membantu pengguna." Lemah sendiri, kuat bila bertumpuk I-2/I-3.

## J. Dekorasi visual

### J-1 · S2 — Bold berlebihan
**Contoh:** ≥5 frasa **bold** di badan artikel → sisakan 1–2 penekanan yang benar-benar kunci.

### J-2 · S1 — Tanda kutip penekanan ≥5×
**Contoh:** kata "biasa" diberi "tanda kutip" untuk "penekanan" → sisakan hanya kutipan sungguhan dan istilah yang diperkenalkan.

### J-3 · S2 — Em-dash berulang
**Contoh:** — di hampir tiap paragraf → koma, titik, atau pecah kalimat.
