# opencraft-humanize — Penghilang Gaya AI untuk Bahasa Indonesia v1.0

Plugin Claude Code yang menghilangkan "gaya khas AI" (ChatGPT · Claude ·
Gemini) dari teks bahasa Indonesia — **tanpa mengubah makna satu fakta pun**.
Yang diubah hanya gaya, ritme, dan pilihan kata.

Terjemahanisme ("melakukan pembelian", "yang mana", pasif "di-" berlebihan),
idiom khas AI ("Kesimpulannya,", "Tidak dapat dipungkiri", "Di era digital
yang semakin berkembang"), konjungsi pembuka spam ("Selain itu… Oleh karena
itu…"), nominalisasi berantai, ritme kalimat seragam, emoji/bullet
berlebihan — **10 kategori × 40+ pola**, diklasifikasi severity S1/S2/S3,
dideteksi per span lalu ditulis ulang secara bedah.

## Instalasi

```
/plugin marketplace add opencraftdev/humanize-id
/plugin install opencraft-humanize
```

Buka sesi baru, lalu `/opencraft-humanize:humanize` — atau cukup bahasa alami:
"hilangkan gaya AI dari teks ini".

## Pemakaian

```
/opencraft-humanize:humanize [teks atau path berkas .txt/.md]
```

Opsi ditulis bahasa alami di akhir argumen:

| Opsi | Nilai | Default |
|---|---|---|
| `genre` | artikel · laporan · blog · surat-resmi | deteksi otomatis |
| `intensitas` | konservatif · standar · agresif | standar |
| `severity-min` | S1 · S2 · S3 | S2 |
| `register` | pertahankan · formal · santai | pertahankan |
| `--strict` | paksa pipeline 5 agen | mati |

Contoh: `/opencraft-humanize:humanize draf.md genre: artikel register: santai`

## Dua mode

**Fast (default, ≤5.000 karakter, ~3 menit)** — satu agen
(`humanize-id-monolith`) mendeteksi, menulis ulang, dan mengecek mandiri
dalam satu panggilan. Keluaran: `_workspace/{run}/final.md` berisi teks hasil
plus blok `<!-- HUMANIZE-SUMMARY -->` (metrik, grade, sorotan) yang tidak
tampil saat markdown dirender.

**Strict (`--strict`, otomatis untuk >8.000 karakter)** — pipeline 5 agen:

```
01_input.txt
   ↓ [id-ai-tell-detector]      → 02_detection.json
   ↓ [id-style-rewriter]        → 03_rewrite.md (maks 3 ronde)
   ↓ paralel:
   ├ [id-fidelity-auditor]      → 04_fidelity_audit.json (13 poin makna)
   └ [id-naturalness-reviewer]  → 05_naturalness_review.json (sisa + over-polish)
   ↓ putusan orkestrator        → final.md  (atau tahan-untuk-manusia)
```

## Empat pagar pengaman

1. **Makna tidak berubah** — fakta, angka, nama, kutipan 100% asli.
2. **Berbasis bukti** — hanya span temuan yang diedit.
3. **Genre & register tetap** — artikel tetap artikel; baku tetap baku
   (kecuali `register:` diminta).
4. **Anti over-polish** — perubahan >30% peringatan, >50% dihentikan paksa.

## Opsi register

Default **pertahankan**: teks baku keluar baku, santai keluar santai.
`register: formal` / `register: santai` menjalankan konversi mekanis
(tabel kata + partikel + afiks) SETELAH humanize — kutipan langsung, nama,
dan angka tidak pernah ikut dikonversi.

## Grade hasil

| Grade | Arti |
|---|---|
| A | S1 sisa 0, S2 ≤2, perubahan 10–25%, cek mandiri 6/6 |
| B | S1 sisa 0, S2 ≤4 — masih layak terbit |
| C | S1 sisa 1–2 — disarankan jalankan `--strict` |
| D | S1 ≥3 atau perubahan >50% — perlu tinjauan manusia |

## Tindak lanjut (bahasa alami saja)

- "kategori terjemahanisme saja yang diulang"
- "paragraf kedua saja"
- "humanize ulang" (ronde kedua atas hasil)
- "turunkan intensitas" / "ubah ke santai"

## Metrik kuantitatif

`skills/humanize/references/metrics_id.py` (pustaka standar
Python, tanpa dependensi):

```bash
python3 skills/humanize/references/metrics_id.py --input teks.txt
```

10 metrik: stdev panjang kalimat, rasio konjungsi pembuka, rasio pasif
"di-", densitas nominalisasi, "melakukan + nomina", idiom khas AI, hedging,
densitas "hal ini", keragaman leksikal, deteksi register.

Tes: `python3 tests/test_metrics_id.py`

## Taksonomi & kontribusi

Sumber kebenaran: `skills/humanize/references/taksonomi-ai-tell.md`.
Pola baru dipromosikan lewat siklus bukti: kumpulkan sampel keluaran AI per
genre → bandingkan frekuensi terhadap tulisan manusia → promosikan hanya
yang rasionya timpang. PR dengan bukti sampel sangat diterima.

## Lisensi

MIT — lihat [LICENSE](LICENSE).

*Terinspirasi arsitektur [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai) (humanizer bahasa Korea).*
