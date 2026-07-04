# opencraft-humanize — AI-Style Remover for Indonesian v1.1

A Claude Code plugin that removes the "AI voice" (ChatGPT · Claude ·
Gemini) from Indonesian text — **without changing a single fact**. Only
style, rhythm, and word choice are touched.

Translationese ("melakukan pembelian", "yang mana", overused "di-"
passives), AI signature idioms ("Kesimpulannya,", "Tidak dapat dipungkiri",
"Di era digital yang semakin berkembang"), sentence-opening connector spam
("Selain itu… Oleh karena itu…"), chained nominalizations, uniform sentence
rhythm, emoji/bullet overload — **10 categories × 40+ patterns**, classified
by severity S1/S2/S3, detected per span and rewritten surgically.

## Installation

```
/plugin marketplace add opencraftdev/humanize-id
/plugin install opencraft-humanize
```

Open a new session, then `/opencraft-humanize:humanize` — or just plain
language: "hilangkan gaya AI dari teks ini".

## Usage

```
/opencraft-humanize:humanize [text or path to a .txt/.md file]
```

Options are written in natural language at the end of the arguments:

| Option | Values | Default |
|---|---|---|
| `genre` | artikel · laporan · blog · surat-resmi | auto-detect |
| `intensitas` | konservatif · standar · agresif | standar |
| `severity-min` | S1 · S2 · S3 | S2 |
| `register` | pertahankan · formal · santai | pertahankan |
| `suara` | netral · hidup | netral |
| `contoh-gaya` | path to a sample of your own writing (.txt/.md) | none |
| `--strict` | force the 5-agent pipeline | off |

Example: `/opencraft-humanize:humanize draft.md genre: artikel register: santai`

## Two modes

**Fast (default, ≤5,000 characters, ~3 min)** — a single agent
(`humanize-id-monolith`) detects, rewrites, asks itself the adversarial
question ("what still makes this obviously AI?"), and self-checks in one
call. Output: `_workspace/{run}/final.md` containing the result plus a
`<!-- HUMANIZE-SUMMARY -->` block (metrics, grade, highlights) that stays
invisible when the markdown is rendered.

**Strict (`--strict`, automatic for >8,000 characters)** — 5-agent pipeline:

```
01_input.txt
   ↓ [id-ai-tell-detector]      → 02_detection.json
   ↓ [id-style-rewriter]        → 03_rewrite.md (max 3 rounds)
   ↓ in parallel:
   ├ [id-fidelity-auditor]      → 04_fidelity_audit.json (13-point meaning check)
   └ [id-naturalness-reviewer]  → 05_naturalness_review.json (residual tells + over-polish)
   ↓ orchestrator verdict       → final.md  (or hold-for-human)
```

## Four guardrails

1. **Meaning never changes** — facts, numbers, names, quotes stay 100% intact.
2. **Evidence-based** — only spans matched to a finding get edited.
3. **Genre & register preserved** — an article stays an article; formal
   stays formal (unless `register:` is requested).
4. **Anti over-polish** — >30% change raises a warning, >50% force-aborts.

## Register option

Default is **pertahankan** (preserve): formal text comes out formal, casual
comes out casual. `register: formal` / `register: santai` runs a mechanical
conversion (word + particle + affix tables) AFTER humanizing — direct
quotes, names, and numbers are never converted.

## Voice option (anti-sterile)

Removing AI tells alone often yields text that is clean but flat — sterile
is a tell too. `suara: hidup` permits rhythm variation, mild stance, and
natural asides WITHOUT new facts or claims (full rules:
`skills/humanize/references/suara-hidup.md`; `SUA-n` edits still count
toward the change rate and are fidelity-audited in strict mode).

`contoh-gaya: <path>` calibrates word choice and rhythm to a sample of
your own writing — usable independently of `suara: hidup`.

## Result grades

| Grade | Meaning |
|---|---|
| A | 0 residual S1, ≤2 S2, 10–25% change, self-check 6/6 |
| B | 0 residual S1, ≤4 S2 — still publishable |
| C | 1–2 residual S1 — running `--strict` is recommended |
| D | ≥3 S1 or >50% change — needs human review |

## Follow-ups (natural language only)

- "kategori terjemahanisme saja yang diulang" (redo only the translationese category)
- "paragraf kedua saja" (second paragraph only)
- "humanize ulang" (second round on the result)
- "turunkan intensitas" / "ubah ke santai" (lower intensity / switch to casual)
- "hidupkan suaranya" (re-run with `suara: hidup`)

## Quantitative metrics

`skills/humanize/references/metrics_id.py` (Python standard library only,
zero dependencies):

```bash
python3 skills/humanize/references/metrics_id.py --input text.txt
```

10 metrics: sentence-length stdev, opening-conjunction ratio, "di-" passive
ratio, nominalization density, "melakukan + noun", AI signature idioms,
hedging, "hal ini" density, lexical diversity, register detection.

Tests: `python3 tests/test_metrics_id.py`

## Taxonomy & contributing

Source of truth: `skills/humanize/references/taksonomi-ai-tell.md`.
New patterns are promoted through an evidence cycle: collect AI-output
samples per genre → compare frequencies against human writing → promote
only patterns with lopsided ratios. PRs with sample evidence are very
welcome.

## License

MIT — see [LICENSE](LICENSE).

*Architecture inspired by [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai) (Korean humanizer); voice pass & adversarial question adapted from [blader/humanizer](https://github.com/blader/humanizer).*
