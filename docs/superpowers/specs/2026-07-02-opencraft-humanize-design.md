# opencraft-humanize — Design Spec (v1.0)

**Date:** 2026-07-02
**Status:** Approved design, pending implementation plan
**Reference implementation:** [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai) (Korean humanizer, v2.0)

## Purpose

A Claude Code plugin that removes "AI tells" from Bahasa Indonesia text — the style, rhythm, and phrasing patterns that mark text as written by ChatGPT/Claude/Gemini — while guaranteeing the content (facts, numbers, proper nouns, quotes) stays byte-identical. Installable via the Claude Code plugin marketplace.

## Decisions (locked with user)

| Decision | Choice |
|---|---|
| v1 scope | Fast mode **and** strict 5-agent pipeline (full port) |
| Documentation/prompt language | Full Bahasa Indonesia (pattern examples always Indonesian) |
| Plugin + command name | `opencraft-humanize` (`/opencraft-humanize`) |
| GitHub repo | Existing `opencraftdev/humanize-id` (public, remote already configured in this working copy) |
| Metrics | Include `metrics_id.py` (stdlib-only Python) + one test file |
| Register default | `pertahankan` (preserve input register); `formal` / `santai` opt-in |

## Repo layout

```
opencraft-humanize/            (repo: opencraftdev/humanize-id)
├── .claude-plugin/
│   ├── plugin.json            # name: opencraft-humanize
│   └── marketplace.json       # marketplace name: opencraft-humanize
├── skills/
│   └── opencraft-humanize/
│       ├── SKILL.md           # orchestrator (mode routing, run_id, phases)
│       └── references/
│           ├── quick-rules-id.md      # slim rulebook — fast mode only
│           ├── taksonomi-ai-tell.md   # SSOT: 10 kategori × 40+ pola, severity S1–S3
│           ├── playbook-penulisan.md  # resep penulisan ulang per kategori + tabel genre
│           ├── tabel-register.md      # tabel konversi baku ↔ percakapan
│           └── metrics_id.py          # metrik kuantitatif, stdlib only
├── agents/
│   ├── humanize-id-monolith.md        # fast mode: deteksi+tulis ulang+cek mandiri, 1 panggilan
│   ├── id-ai-tell-detector.md         # strict: laporan span JSON
│   ├── id-style-rewriter.md           # strict: edit bedah per finding + register pass
│   ├── id-fidelity-auditor.md         # strict: audit kesetaraan makna
│   └── id-naturalness-reviewer.md     # strict: sisa AI-tell + over-polish
├── tests/test_metrics_id.py
├── docs/superpowers/specs/            # design docs (this file)
├── README.md                          # Bahasa Indonesia, install marketplace
└── LICENSE                            # MIT
```

Deliberately skipped for v1 (add when needed): `install.sh`/Codex CLI support (marketplace covers install), taxonomist agent (pattern promotion is manual for now), separate `humanize-redo` skill (follow-up commands are routed by the orchestrator's follow-up table).

## Pipeline

### Phase 0 — Setup (orchestrator SKILL.md)
- Print one status line: `opencraft-humanize v1.0 — {fast|strict} / run_id: {YYYY-MM-DD-NNN}`
- Create `_workspace/{run_id}/` in cwd, save `01_input.txt`
- Detect genre from first 300 chars (user override wins): `artikel | laporan | blog | surat-resmi`
- Detect input register: `baku | percakapan` (heuristic in metrics_id.py)
- Mode routing: `--strict` or "mode ketat" → strict; input > 8.000 chars → strict (auto-upgrade, 1-line notice); else fast

### Fast mode (default, ≤5.000 chars, target ~3 min)
Single `humanize-id-monolith` agent call, hard cap 3 tool calls (+1 Read of `tabel-register.md` only when register conversion is requested):
1. Read `01_input.txt`
2. Read `quick-rules-id.md` (slim rulebook, S1/S2 only)
3. In memory: detect spans → rewrite per span → self-check 6 poin → grade A–D → (optional register pass)
4. Write `final.md` (body + `<!-- HUMANIZE-SUMMARY -->` HTML comment block: metrics, category counts before→after, self-check, grade, highlights)

### Strict mode (`--strict` or >8.000 chars)
1. `id-ai-tell-detector` → `02_detection.json` (span, pattern ID, severity, suggested fix)
2. `id-style-rewriter` → `03_rewrite.md` + diff JSON — edits **only** detected spans; register pass at the end if requested
3. Parallel verification:
   - `id-fidelity-auditor` → `04_fidelity_audit.json` (13-point meaning-equivalence checklist)
   - `id-naturalness-reviewer` → `05_naturalness_review.json` (residual tells, over-polish, grade)
4. Orchestrator verdict matrix:

| fidelity | naturalness | Verdict |
|---|---|---|
| lolos penuh | terima | final.md + summary |
| lolos penuh | tulis-ulang ronde 2 | rewriter re-run on target findings (max 3 rounds) |
| lolos penuh | rollback | roll back offending edits, re-run |
| lolos bersyarat | — | retry only rolled-back edits |
| gagal | — | full rewrite round; after 3 rounds → `tahan-untuk-manusia` |

### Register pass (both modes)
- Option `register: pertahankan (default) | formal | santai`
- Runs **after** humanize edits, driven by `tabel-register.md` (word table: tidak→nggak, saya→aku, partikel sih/dong/kok policy, what never changes)
- **Exempt from change-rate caps** (converting register legitimately touches many words) but still covered by fidelity audit (meaning/quotes/numbers unchanged)
- Register *inconsistency* within a paragraph is itself a detected tell (kategori E)

## Guardrails (both modes, non-negotiable)

1. **Makna tidak berubah** — facts, claims, numbers, dates, proper nouns, direct quotes 100% preserved; violation = rollback
2. **Berbasis bukti** — only detected spans are edited
3. **Genre tidak bergeser** — artikel stays artikel
4. **Register dipertahankan** unless user opts into conversion
5. **Change-rate**: >30% warning, >50% abort + rollback to last safe version
6. **Do-NOT list**: proper nouns, product names, numbers/dates/units, direct quotes, legal text, standard acronyms (AI, API, GPU, dll.)

## Taxonomy — 10 kategori (SSOT: taksonomi-ai-tell.md)

| ID | Kategori | Contoh pola (non-exhaustive) |
|----|----------|------------------------------|
| A | Terjemahanisme | pasif "di-" berlebihan saat aktif lebih alami; "yang mana"/"di mana" sebagai penghubung; "melakukan + nomina" ("melakukan pembelian"→"membeli"); "memiliki" spam; "adalah merupakan"; "dikarenakan" |
| B | Istilah Inggris berlebih | kurung Inggris tiap kemunculan; kata terjemahkan-able dibiarkan Inggris |
| C | Pola struktural | "Pertama/Kedua/Ketiga" mekanis; emoji; bullet berlebih; heading "X: Y" berulang; indeks "(1)(2)(3)" |
| D | Idiom khas AI | "Kesimpulannya,"; "Tidak dapat dipungkiri"; "Di era digital yang semakin berkembang"; "Penting untuk dicatat bahwa"; "memainkan peran penting"; "Seiring berkembangnya teknologi" |
| E | Keseragaman ritme | panjang kalimat seragam (stdev rendah); awalan kalimat berulang; register campur baku+gaul dalam satu paragraf |
| F | Modifikasi berlebih | "sangat"/"sekali" spam; rantai nominalisasi pe-an/ke-an/-isasi/-itas |
| G | Hedging | "dapat dikatakan bahwa"; "mungkin dapat"; tumpukan pelunak |
| H | Konjungsi awal kalimat | "Selain itu"/"Oleh karena itu"/"Dengan demikian"/"Di sisi lain" spam |
| I | Nomina kosong | "hal ini menunjukkan"; "merupakan suatu"; "adanya" berlebihan |
| J | Dekorasi visual | bold berlebihan; tanda kutip penekanan; em-dash spam |

- **Severity:** S1 (satu kemunculan = bukti AI, wajib hapus) / S2 (1–2× boleh, 3×+ hapus) / S3 (bermasalah hanya jika bertumpuk)
- **Grade:** A (S1 sisa 0, S2 ≤2, perubahan 10–25%, self-check 6/6) / B (S1 0, S2 ≤4, ≥5/6) / C (S1 1–2 → sarankan strict) / D (S1 ≥3 atau perubahan >50% → tahan)
- `quick-rules-id.md` = compressed S1/S2 subset, 1-line definition + 1-line fix per pattern, Do-NOT list, self-check checklist — small enough for one agent context
- Taxonomy v1 is seeded from model knowledge of AI-Indonesian output; README documents the evidence-mining loop (collect AI samples → validate pattern frequency → promote/demote patterns) for future versions

## metrics_id.py

Stdlib only (re, statistics, json, argparse, collections). ~10 pure functions:

`sentence_length_stdev`, `conjunction_initial_rate`, `passive_di_rate`, `nominalization_density`, `melakukan_nomina_count`, `signature_phrase_count`, `hedging_count`, `hal_density`, `lexical_diversity`, `detect_register` (heuristik: nggak/gak/aku/gue/sih/dong/kok/banget → percakapan)

CLI: `python metrics_id.py --input file.txt --output metrics.json`
Tests: `tests/test_metrics_id.py`, plain assert-based, runnable with `python tests/test_metrics_id.py`.

Morphology is approximated with regex + affix lists (no NLP dependencies) — same tradeoff the Korean repo made deliberately.

## Distribution

- `plugin.json`: name `opencraft-humanize`, bundles `skills/` + `agents/`
- `marketplace.json`: marketplace name `opencraft-humanize`, plugin source `./`
- Push to existing `opencraftdev/humanize-id`
- Install:
  ```
  /plugin marketplace add opencraftdev/humanize-id
  /plugin install opencraft-humanize@opencraft-humanize
  ```
- Trigger: `/opencraft-humanize [teks|file]` or natural language ("hilangkan gaya AI", "humanize teks ini", "buat tulisan ini lebih natural")

## Options (natural language at end of arguments)

- `genre: artikel|laporan|blog|surat-resmi` (default: auto-detect)
- `intensitas: konservatif|standar|agresif` (default: standar)
- `severity-min: S1|S2|S3` (default: S2)
- `register: pertahankan|formal|santai` (default: pertahankan)
- `--strict` — force 5-agent pipeline

## Error handling

- Non-Indonesian input → "Hanya teks bahasa Indonesia yang didukung", stop
- Change-rate >50% → rollback to last safe version, mark `over_polish_aborted: true` in summary
- Self-check violation unresolved after 1 retry (fast) / 3 rounds (strict) → output anyway + flag unresolved items in summary
- Already-human text (near-zero detections) → change <5%, note "kemungkinan tidak perlu di-humanize"

## Testing / verification

1. `python tests/test_metrics_id.py` passes
2. Both JSON manifests parse (`python -m json.tool`)
3. Live E2E: install plugin locally, feed an AI-generated Indonesian sample (~2.000 chars) through fast mode — expect change-rate 10–25%, grade A/B, names/numbers byte-identical
4. Strict-mode smoke test on an 8.000+ char sample
5. Register conversion test: formal→santai on a short sample, verify quotes/numbers untouched
