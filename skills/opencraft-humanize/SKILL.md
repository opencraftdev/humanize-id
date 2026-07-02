---
name: opencraft-humanize
version: "1.0.0"
description: Menghilangkan gaya khas AI (ChatGPT·Claude·Gemini) dari teks bahasa Indonesia tanpa mengubah makna — terjemahanisme, idiom AI ("Kesimpulannya", "Tidak dapat dipungkiri", "Di era digital"), pasif "di-" berlebihan, konjungsi pembuka spam, nominalisasi, ritme seragam, emoji/bullet berlebih. 10 kategori × 40+ pola, severity S1–S3. Mode Fast (1 agen) default; Strict (pipeline 5 agen) via --strict atau otomatis >8.000 karakter. Opsi register formal/santai. Pemicu — "hilangkan gaya AI", "humanize teks ini", "buat tulisan ini lebih natural", "hapus AI-tell", "biar nggak kayak AI", "rapikan tulisan ChatGPT", "humanize indonesia", "/opencraft-humanize". Tindak lanjut ("kategori X saja", "humanize ulang", "turunkan intensitas", "paragraf ini saja") juga skill ini. Koreksi ejaan murni kerjakan langsung; terjemahan dan penulisan konten baru bukan skill ini.
---

# opencraft-humanize — Orkestrator (v1.0)

## Phase 0: Setup dan penentuan mode

Cetak satu baris status lebih dulu:

```
opencraft-humanize v1.0 — mode {fast|strict} / run_id: {YYYY-MM-DD-NNN}
```

### Penentuan mode
- User menulis `--strict` / "mode ketat" / "pipeline lengkap" → **strict**
- Input > 8.000 karakter → **strict** (naik otomatis, beri tahu 1 baris)
- Selain itu → **fast (default)**

### run_id
- Semua path relatif cwd. Folder kerja: `_workspace/{YYYY-MM-DD-NNN}/`.
- Cek urutan hari ini via `Glob(pattern="_workspace/{YYYY-MM-DD}-*/01_input.txt")`
  → NNN terbesar + 1; tidak ada → 001. (Glob file penanda, bukan direktori.)
- Perintah tindak lanjut ("kategori X saja", "humanize ulang") → pakai
  run_id lama + mode strict.

### Input dan opsi
1. Buat `_workspace/{run_id}/`, simpan teks ke `01_input.txt`. Jika argumen
   berupa path `.txt`/`.md`, Read dulu isinya. Argumen kosong → minta user
   menempelkan teks, berhenti.
2. Deteksi genre dari 300 karakter pertama: `artikel | laporan | blog |
   surat-resmi` (opsi user menang).
3. Deteksi register masukan (baku/percakapan) — jalankan
   `python3 {CLAUDE_PLUGIN_ROOT}/skills/opencraft-humanize/references/metrics_id.py --input _workspace/{run_id}/01_input.txt`
   dan baca bidang `register`. Skrip gagal → tebak dari teks, lanjut.
4. Opsi (bahasa alami di akhir argumen), default dalam kurung:
   `genre: artikel|laporan|blog|surat-resmi` (auto) ·
   `intensitas: konservatif|standar|agresif` (standar) ·
   `severity-min: S1|S2|S3` (S2) ·
   `register: pertahankan|formal|santai` (pertahankan) · `--strict`.
5. Input bukan bahasa Indonesia → "Hanya teks bahasa Indonesia yang
   didukung." — berhenti.

## Mode Fast (default, ≤5.000 karakter, target ~3 menit)

Panggil agen `humanize-id-monolith` SEKALI via tool Agent dengan input:

```
input_path: <abs>/_workspace/{run_id}/01_input.txt
quick_rules_path: <abs path ke references/quick-rules-id.md>
register_table_path: <abs path ke references/tabel-register.md>  # hanya bila register != pertahankan
genre_hint: artikel|laporan|blog|surat-resmi
register_target: pertahankan|formal|santai
intensitas: konservatif|standar|agresif
severity_min: S1|S2|S3
```

Agen menulis `_workspace/{run_id}/final.md` (isi + blok komentar
`<!-- HUMANIZE-SUMMARY -->`). Lalu sampaikan ke user:

1. Satu baris: `Selesai. Perubahan X% / Grade Y / cek mandiri N/6`
2. Teks hasil (blok markdown)
3. Tabel ringkas: deteksi per kategori (sebelum → sesudah) + cek mandiri
4. Grade ≤ B → tawarkan `--strict` untuk verifikasi 5 agen

## Mode Strict (`--strict` atau otomatis)

### Phase A — Deteksi
Panggil `id-ai-tell-detector`:
```
input_path: …/01_input.txt
taxonomy_path: <abs path ke references/taksonomi-ai-tell.md>
genre_hint / severity_min: (dari Phase 0)
```
Keluaran: `02_detection.json`.

### Phase B — Penulisan ulang (maks 3 ronde)
Panggil `id-style-rewriter`:
```
input_path: …/01_input.txt
detection_path: …/02_detection.json
playbook_path: <abs path ke references/playbook-penulisan.md>
register_table_path: <abs>  # hanya bila register != pertahankan
register_target / intensitas: (dari Phase 0)
target_findings: (kosong = semua; ronde 2+ = daftar ID temuan)
```
Keluaran: `03_rewrite.md` (+ `03_rewrite_v2.md`, `_v3` di ronde lanjutan).

### Phase C — Verifikasi paralel
Panggil DUA agen sekaligus (satu pesan, dua tool call):
- `id-fidelity-auditor` (input: `01_input.txt`, `03_rewrite.md` terbaru,
  `03_rewrite_edits.json`) → `04_fidelity_audit.json`
- `id-naturalness-reviewer` (input: `03_rewrite.md` terbaru,
  `02_detection.json`, taxonomy_path) → `05_naturalness_review.json`

Matriks keputusan:

| fidelity | naturalness | Putusan |
|---|---|---|
| lolos_penuh | terima / terima_dengan_catatan | **Final** → Phase D |
| lolos_penuh | tulis_ulang_ronde_2 | Phase B lagi (target_findings terisi) |
| lolos_penuh | rollback | Rollback edit bermasalah → Phase B |
| lolos_bersyarat | — | Phase B hanya untuk edit yang dirollback |
| gagal | — | Phase B penuh; ronde ke-3 gagal → **tahan-untuk-manusia** |

### Phase D — Final
1. Salin hasil terakhir ke `final.md` + blok `<!-- HUMANIZE-SUMMARY -->`
   (format sama dengan fast).
2. Sampaikan ke user seperti butir 1–4 mode fast, plus verdict audit.

## Tindak lanjut

| Sinyal user | Aksi |
|---|---|
| "kategori X saja" | strict, Phase B ulang hanya temuan kategori X |
| "paragraf ini saja" | run_id baru berisi paragraf itu, strict |
| "humanize ulang" | `final.md` lama jadi input baru, strict Phase B |
| "turunkan/naikkan intensitas" | ulang dari Phase A dengan intensitas baru |
| "ubah ke santai/formal" | pass register saja pada `final.md` + audit fidelity |

## Pagar pengaman (tidak bisa ditawar)

- Makna, fakta, angka, tanggal, nama diri, kutipan langsung: 100% sama.
- Hanya span temuan yang boleh diedit.
- Perubahan >30% = peringatan; >50% = hentikan + rollback.
- Genre dan register tidak bergeser (kecuali register diminta).
- Pass register di luar hitungan change-rate tapi tetap diaudit fidelity.
- Jangan memuat CLAUDE.md/berkas proyek lain untuk menebak opsi.

## Referensi

- `references/quick-rules-id.md` — rulebook ringkas (fast)
- `references/taksonomi-ai-tell.md` — SSOT 10 kategori (strict)
- `references/playbook-penulisan.md` — resep penulisan ulang (strict)
- `references/tabel-register.md` — konversi baku ↔ percakapan
- `references/metrics_id.py` — metrik kuantitatif (`python3 … --input f.txt`)
