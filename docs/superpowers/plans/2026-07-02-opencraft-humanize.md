# opencraft-humanize Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `opencraft-humanize` Claude Code plugin — a Bahasa Indonesia AI-tell humanizer with fast/strict modes — installable via `/plugin marketplace add opencraftdev/humanize-id`.

**Architecture:** A plugin repo of markdown prompt assets (1 orchestrator skill + 5 agents + 4 reference rulebooks) plus one stdlib-only Python metrics module. The "engine" is Claude; the repo is the rulebook. Modeled on the proven epoko77-ai/im-not-ai layout.

**Tech Stack:** Claude Code plugin conventions (`.claude-plugin/plugin.json`, `skills/`, `agents/`), Python 3 stdlib only (re, statistics, json, argparse), git + gh CLI.

## Global Constraints

- All user-facing docs, skill instructions, and agent prompts in **Bahasa Indonesia** (pattern examples always Indonesian).
- Plugin + command + marketplace name: **`opencraft-humanize`**. Repo: existing **`opencraftdev/humanize-id`** (remote `origin` already configured).
- Python: **stdlib only** — no konlpy-equivalents, no pip installs. Tests are plain `assert`, run with `python3 tests/test_metrics_id.py`.
- Guardrails (verbatim in every agent): makna tidak berubah; change-rate >30% warning / >50% abort+rollback; genre & register tidak bergeser; Do-NOT list (nama diri, angka/tanggal/satuan, kutipan langsung, teks hukum, akronim standar AI/API/GPU/LLM/dll).
- Severity: S1 (satu kemunculan = bukti AI, wajib hapus) / S2 (1–2× boleh, 3×+ hapus) / S3 (bermasalah hanya jika bertumpuk). Grade A–D per spec.
- Workspace convention: `_workspace/{YYYY-MM-DD-NNN}/` with `01_input.txt`, `02_detection.json`, `03_rewrite.md`, `04_fidelity_audit.json`, `05_naturalness_review.json`, `final.md`.
- Working directory: `/Users/user/Project_Apps/opencraft-humanize` (git repo on `main`, spec already committed).
- Commit messages end with `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`.

---

### Task 1: Plugin scaffolding — manifests, license, gitignore

**Files:**
- Create: `.claude-plugin/plugin.json`
- Create: `.claude-plugin/marketplace.json`
- Create: `LICENSE`
- Create: `.gitignore`

**Interfaces:**
- Produces: plugin name `opencraft-humanize` and marketplace name `opencraft-humanize` — README (Task 8) and SKILL.md (Task 5) reference these exact names in install/usage strings.

- [ ] **Step 1: Write `.claude-plugin/plugin.json`**

```json
{
  "name": "opencraft-humanize",
  "version": "1.0.0",
  "description": "Menghilangkan gaya khas AI dari teks bahasa Indonesia tanpa mengubah makna — mode Fast (1 agen) + Strict (pipeline 5 agen). 10 kategori × 40+ pola AI-tell.",
  "author": {
    "name": "opencraftdev"
  },
  "homepage": "https://github.com/opencraftdev/humanize-id",
  "repository": "https://github.com/opencraftdev/humanize-id",
  "license": "MIT",
  "keywords": ["indonesian", "bahasa-indonesia", "humanize", "ai-detector", "penulisan-ulang", "terjemahanisme"],
  "skills": ["./skills/"]
}
```

- [ ] **Step 2: Write `.claude-plugin/marketplace.json`**

```json
{
  "name": "opencraft-humanize",
  "owner": {
    "name": "opencraftdev"
  },
  "metadata": {
    "description": "Marketplace untuk plugin opencraft-humanize — penghilang gaya AI untuk teks bahasa Indonesia",
    "version": "1.0.0",
    "pluginRoot": "."
  },
  "plugins": [
    {
      "name": "opencraft-humanize",
      "source": "./",
      "description": "Skill orkestrator + 5 subagen untuk menghilangkan gaya khas AI dari teks bahasa Indonesia (Fast + Strict).",
      "version": "1.0.0",
      "keywords": ["indonesian", "humanize", "ai-detector", "penulisan-ulang"]
    }
  ]
}
```

- [ ] **Step 3: Write `LICENSE`** (MIT, year 2026, holder `opencraftdev`)

```
MIT License

Copyright (c) 2026 opencraftdev

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 4: Write `.gitignore`**

```
_workspace/
__pycache__/
*.pyc
.DS_Store
```

- [ ] **Step 5: Validate both manifests parse**

Run: `python3 -m json.tool .claude-plugin/plugin.json > /dev/null && python3 -m json.tool .claude-plugin/marketplace.json > /dev/null && echo VALID`
Expected: `VALID`

- [ ] **Step 6: Commit**

```bash
git add .claude-plugin LICENSE .gitignore
git commit -m "feat: plugin scaffolding — manifests, MIT license, gitignore

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 2: metrics_id.py — TDD

**Files:**
- Test: `tests/test_metrics_id.py`
- Create: `skills/opencraft-humanize/references/metrics_id.py`

**Interfaces:**
- Produces: module `metrics_id` with pure functions `sentence_length_stdev(text) -> float`, `conjunction_initial_rate(text) -> dict`, `passive_di_rate(text) -> dict`, `nominalization_density(text) -> dict`, `melakukan_nomina_count(text) -> int`, `signature_phrase_count(text) -> int`, `hedging_count(text) -> int`, `hal_density(text) -> dict`, `lexical_diversity(text) -> float`, `detect_register(text) -> dict`, `analyze(text) -> dict`; CLI `python3 metrics_id.py --input f.txt [--output f.json]`. SKILL.md (Task 5) references `detect_register` for Phase 0 register detection.

- [ ] **Step 1: Write the failing test file `tests/test_metrics_id.py`**

```python
"""Tes metrics_id — jalankan: python3 tests/test_metrics_id.py"""
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "skills", "opencraft-humanize", "references"))

import metrics_id as m

AI_TEXT = (
    "Selain itu, transformasi digital memainkan peran penting dalam "
    "pengimplementasian kebijakan. "
    "Oleh karena itu, perusahaan melakukan evaluasi terhadap hal ini. "
    "Dengan demikian, dapat dikatakan bahwa optimalisasi dilakukan "
    "secara berkelanjutan."
)

INFORMAL_TEXT = "Gue sih udah bilang, proyek ini nggak bakal jalan dong."


def test_sentence_split():
    assert len(m._sentences(AI_TEXT)) == 3
    assert m._sentences("") == []


def test_sentence_length_stdev():
    assert m.sentence_length_stdev("Satu dua tiga.") == 0.0
    assert m.sentence_length_stdev(AI_TEXT) > 0.0


def test_conjunction_initial_rate():
    r = m.conjunction_initial_rate(AI_TEXT)
    assert r["count"] == 3 and r["sentences"] == 3 and r["rate"] == 1.0


def test_passive_di_rate():
    # "dikatakan", "dilakukan" pasif; "digital" masuk pengecualian
    assert m.passive_di_rate(AI_TEXT)["count"] == 2


def test_nominalization_density():
    # pengimplementasian, kebijakan, perusahaan, optimalisasi
    assert m.nominalization_density(AI_TEXT)["count"] == 4


def test_melakukan_nomina_count():
    assert m.melakukan_nomina_count(AI_TEXT) == 1


def test_signature_phrase_count():
    assert m.signature_phrase_count(AI_TEXT) == 1  # memainkan peran penting


def test_hedging_count():
    assert m.hedging_count(AI_TEXT) == 1  # dapat dikatakan bahwa


def test_hal_density():
    assert m.hal_density(AI_TEXT)["count"] == 1  # hal ini


def test_lexical_diversity():
    assert 0.0 < m.lexical_diversity(AI_TEXT) <= 1.0
    assert m.lexical_diversity("") == 0.0


def test_detect_register():
    assert m.detect_register(AI_TEXT)["register"] == "baku"
    r = m.detect_register(INFORMAL_TEXT)
    assert r["register"] == "percakapan" and len(r["penanda"]) >= 2


def test_analyze_keys():
    a = m.analyze(AI_TEXT)
    for key in ("versi", "jumlah_kata", "sentence_length_stdev",
                "conjunction_initial_rate", "passive_di_rate",
                "nominalization_density", "melakukan_nomina_count",
                "signature_phrase_count", "hedging_count", "hal_density",
                "lexical_diversity", "register"):
        assert key in a, key


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"ok {fn.__name__}")
    print(f"LULUS {len(fns)} tes")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tests/test_metrics_id.py`
Expected: `ModuleNotFoundError: No module named 'metrics_id'`

- [ ] **Step 3: Write `skills/opencraft-humanize/references/metrics_id.py`**

```python
"""Metrik kuantitatif opencraft-humanize v1.0.

Hanya pustaka standar. Morfologi diaproksimasi dengan regex + daftar
afiks/leksikon — tanpa dependensi NLP. Ambang penilaian (berapa yang
"terlalu banyak") ada di quick-rules-id.md, bukan di sini.

CLI: python3 metrics_id.py --input teks.txt [--output metrik.json]
"""

from __future__ import annotations

import argparse
import json
import re
from statistics import pstdev

VERSION = "1.0"

_SENT_SPLIT = re.compile(r"(?<=[.!?…])\s+")
_WORD = re.compile(r"[a-zA-Z][a-zA-Z\-]*")

# Kata berawalan "di" yang BUKAN kata kerja pasif (pengecualian umum).
# ponytail: daftar heuristik, tambah entri saat false positive ditemukan
_DI_NON_PASSIVE = {
    "dia", "diri", "dirinya", "dini", "dinas", "digital", "dimensi",
    "diskusi", "disiplin", "direktur", "direksi", "diagram", "diet",
    "divisi", "dialog", "diameter", "diabetes", "dinamika", "dinamis",
    "diplomasi", "diplomat", "diskon", "distribusi", "distributor",
}

# Idiom khas AI (kategori D taksonomi) — dicocokkan lowercase substring.
_SIGNATURE_PHRASES = (
    "kesimpulannya",
    "sebagai kesimpulan",
    "tidak dapat dipungkiri",
    "tak dapat dipungkiri",
    "di era digital",
    "di era modern",
    "penting untuk dicatat",
    "penting untuk diingat",
    "penting untuk dipahami",
    "memainkan peran penting",
    "memainkan peranan penting",
    "seiring berkembangnya",
    "seiring dengan perkembangan",
)

_HEDGING_PHRASES = (
    "dapat dikatakan bahwa",
    "mungkin dapat",
    "cenderung dapat",
    "berpotensi untuk dapat",
    "bisa jadi merupakan",
)

_INITIAL_CONJUNCTIONS = (
    "selain itu", "oleh karena itu", "dengan demikian", "di sisi lain",
    "lebih lanjut", "namun", "sementara itu", "terlebih lagi",
)

# Penanda register percakapan. "aku/kamu" sengaja tidak dimasukkan
# (muncul juga di teks baku-sastra) demi menekan false positive.
_INFORMAL_MARKERS = {
    "nggak", "gak", "engga", "enggak", "gue", "gua", "lo", "lu",
    "sih", "dong", "deh", "kok", "banget", "kayak", "gitu", "gini",
    "udah", "aja", "nih", "tuh", "ntar", "gimana", "emang", "biar",
}

_NOMINALIZATION = re.compile(r"^(pe[a-z]{2,}an|ke[a-z]{2,}an|[a-z]{3,}isasi|[a-z]{3,}itas)$")


def _sentences(text):
    return [s.strip() for s in _SENT_SPLIT.split(text.strip()) if s.strip()]


def _words(text):
    return [w.lower() for w in _WORD.findall(text)]


def _per_100(count, total):
    return round(100.0 * count / total, 2) if total else 0.0


def sentence_length_stdev(text):
    lengths = [len(_words(s)) for s in _sentences(text)]
    return round(pstdev(lengths), 2) if len(lengths) >= 2 else 0.0


def conjunction_initial_rate(text):
    sents = _sentences(text)
    count = sum(
        1 for s in sents
        if s.lower().lstrip('*#>-— "\'').startswith(_INITIAL_CONJUNCTIONS)
    )
    return {
        "count": count,
        "sentences": len(sents),
        "rate": round(count / len(sents), 3) if sents else 0.0,
    }


def passive_di_rate(text):
    words = _words(text)
    hits = [w for w in words
            if w.startswith("di") and len(w) > 4 and w not in _DI_NON_PASSIVE]
    return {"count": len(hits), "per_100_kata": _per_100(len(hits), len(words))}


def nominalization_density(text):
    words = _words(text)
    hits = [w for w in words if _NOMINALIZATION.match(w)]
    return {"count": len(hits), "per_100_kata": _per_100(len(hits), len(words))}


def melakukan_nomina_count(text):
    return len(re.findall(r"\bmelakukan\s+\w+", text, flags=re.IGNORECASE))


def signature_phrase_count(text):
    low = text.lower()
    return sum(low.count(p) for p in _SIGNATURE_PHRASES)


def hedging_count(text):
    low = text.lower()
    return sum(low.count(p) for p in _HEDGING_PHRASES)


def hal_density(text):
    words = _words(text)
    count = len(re.findall(r"\bhal (ini|itu|tersebut)\b", text.lower()))
    return {"count": count, "per_100_kata": _per_100(count, len(words))}


def lexical_diversity(text):
    words = _words(text)
    return round(len(set(words)) / len(words), 3) if words else 0.0


def detect_register(text):
    hits = sorted(set(_words(text)) & _INFORMAL_MARKERS)
    return {
        "register": "percakapan" if len(hits) >= 2 else "baku",
        "penanda": hits,
    }


def analyze(text):
    return {
        "versi": VERSION,
        "jumlah_kata": len(_words(text)),
        "sentence_length_stdev": sentence_length_stdev(text),
        "conjunction_initial_rate": conjunction_initial_rate(text),
        "passive_di_rate": passive_di_rate(text),
        "nominalization_density": nominalization_density(text),
        "melakukan_nomina_count": melakukan_nomina_count(text),
        "signature_phrase_count": signature_phrase_count(text),
        "hedging_count": hedging_count(text),
        "hal_density": hal_density(text),
        "lexical_diversity": lexical_diversity(text),
        "register": detect_register(text),
    }


def main():
    ap = argparse.ArgumentParser(description="Metrik AI-tell bahasa Indonesia")
    ap.add_argument("--input", required=True)
    ap.add_argument("--output")
    args = ap.parse_args()
    with open(args.input, encoding="utf-8") as f:
        result = analyze(f.read())
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(payload + "\n")
    else:
        print(payload)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 tests/test_metrics_id.py`
Expected: `ok test_...` lines ending with `LULUS 12 tes`

If a count assertion fails, fix the lexicon/regex (or the fixture comment), not the assertion semantics — the fixture sentences were chosen so each count is hand-verifiable.

- [ ] **Step 5: Smoke-test the CLI**

Run: `printf 'Selain itu, hal ini dilakukan secara berkelanjutan.' > /tmp/oh-smoke.txt && python3 skills/opencraft-humanize/references/metrics_id.py --input /tmp/oh-smoke.txt | python3 -m json.tool > /dev/null && echo CLI-OK`
Expected: `CLI-OK`

- [ ] **Step 6: Commit**

```bash
git add tests/test_metrics_id.py skills/opencraft-humanize/references/metrics_id.py
git commit -m "feat: metrics_id.py — 10 metrik AI-tell bahasa Indonesia + tes

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 3: Rulebooks — quick-rules-id.md + tabel-register.md

**Files:**
- Create: `skills/opencraft-humanize/references/quick-rules-id.md`
- Create: `skills/opencraft-humanize/references/tabel-register.md`

**Interfaces:**
- Produces: pattern IDs (A-1…J-3), the 6-item self-check checklist, and grade rules — the monolith agent (Task 6) reads this file verbatim as its entire rulebook; strict agents (Task 7) reference the same IDs. `tabel-register.md` is read by monolith/rewriter only when `register: formal|santai` requested.

- [ ] **Step 1: Write `skills/opencraft-humanize/references/quick-rules-id.md`**

```markdown
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
6. **Tidak menambah gaya baru** (tak ada metafora/retorika yang tidak ada di asli)

## Grade (nilai mandiri)

- **A**: S1 sisa 0, S2 sisa ≤2, perubahan 10–25%, cek mandiri 6/6
- **B**: S1 sisa 0, S2 sisa ≤4, cek mandiri ≥5/6
- **C**: S1 sisa 1–2 atau cek mandiri ≤4 — sarankan `--strict`
- **D**: S1 sisa ≥3 atau perubahan >50% — tahan, minta tinjauan manusia
```

- [ ] **Step 2: Write `skills/opencraft-humanize/references/tabel-register.md`**

```markdown
# Tabel Register — konversi baku ↔ percakapan (v1.0)

Dibaca HANYA saat user meminta `register: formal` atau `register: santai`.
Konversi berjalan SETELAH humanize selesai, di luar hitungan change-rate,
tetapi tetap diaudit fidelity: makna, nama, angka, kutipan tak boleh berubah.

## Prinsip

1. Konversi mekanis per tabel — bukan menulis ulang gaya. Jangan menambah
   humor, slang berat, atau kepribadian yang tidak ada di teks asli.
2. Kutipan langsung TIDAK dikonversi (ucapan orang tetap apa adanya).
3. Teks hukum, judul karya, istilah teknis tetap.
4. Konsisten satu arah untuk seluruh teks — tidak campur.

## Tabel kata

| Baku | Percakapan |
|---|---|
| tidak | nggak |
| saya | aku |
| Anda | kamu |
| sudah | udah |
| belum | belum |
| hanya | cuma |
| sangat | banget (posisi setelah kata: "bagus banget") |
| seperti | kayak |
| begitu | gitu |
| begini | gini |
| bagaimana | gimana |
| mengapa / kenapa | kenapa |
| tetapi / namun | tapi |
| kemudian | terus |
| ingin | pengin |
| memang | emang |
| dengan | sama (hanya makna "bersama"; makna instrumen tetap "pakai") |

## Partikel (arah santai saja)

- `sih`, `dong`, `deh`, `kok`, `nih`, `lho` — maksimal 1 partikel per 2–3
  kalimat, hanya di kalimat yang nadanya memang menegaskan/mengajak.
  Jangan ditabur merata.

## Afiks (arah santai)

- me- boleh luruh pada verba umum: "membawa" → "bawa", "melihat" → "lihat".
  Hanya jika hasilnya lazim diucapkan; ragu = biarkan.
- Arah formal: kebalikannya — kembalikan prefiks penuh, buang partikel,
  ganti kosakata kolom kanan ke kolom kiri.

## Yang TIDAK pernah berubah (kedua arah)

Nama diri, angka, tanggal, satuan, kutipan langsung, akronim, istilah teknis,
fakta dan urutan klaim.
```

- [ ] **Step 3: Verify structure**

Run: `grep -c '^| [A-J]-' skills/opencraft-humanize/references/quick-rules-id.md && grep -q 'Cek mandiri' skills/opencraft-humanize/references/quick-rules-id.md && grep -q 'Tabel kata' skills/opencraft-humanize/references/tabel-register.md && echo STRUKTUR-OK`
Expected: a count ≥ 40, then `STRUKTUR-OK`

- [ ] **Step 4: Commit**

```bash
git add skills/opencraft-humanize/references/quick-rules-id.md skills/opencraft-humanize/references/tabel-register.md
git commit -m "feat: quick-rules-id (47 pola S1/S2) + tabel register baku<->percakapan

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 4: References — taksonomi-ai-tell.md + playbook-penulisan.md

**Files:**
- Create: `skills/opencraft-humanize/references/taksonomi-ai-tell.md`
- Create: `skills/opencraft-humanize/references/playbook-penulisan.md`

**Interfaces:**
- Consumes: pattern IDs from Task 3 (taxonomy must be a superset with identical IDs — same A-1…J-3, plus contoh kalimat and S3 additions).
- Produces: the SSOT read by strict-mode agents (`id-ai-tell-detector` reads taksonomi; `id-style-rewriter` reads playbook).

- [ ] **Step 1: Write `skills/opencraft-humanize/references/taksonomi-ai-tell.md`**

The file = the quick-rules table expanded: for **every** ID in quick-rules-id.md, one block with `**Definisi**`, `**Contoh** (kalimat AI → perbaikan)`, `**Catatan deteksi**`. Header explains severity S1/S2/S3 and the evidence-mining loop. Then three S3 additions. Complete content:

````markdown
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
````

- [ ] **Step 2: Write `skills/opencraft-humanize/references/playbook-penulisan.md`**

```markdown
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
```

- [ ] **Step 3: Verify taxonomy ⊇ quick-rules IDs**

Run: `python3 -c "
import re
qr = open('skills/opencraft-humanize/references/quick-rules-id.md').read()
tx = open('skills/opencraft-humanize/references/taksonomi-ai-tell.md').read()
qids = set(re.findall(r'^\| ([A-J]-\d+) ', qr, re.M))
tids = set(re.findall(r'^### ([A-J]-\d+) ', tx, re.M))
missing = qids - tids
assert not missing, f'ID quick-rules tanpa entri taksonomi: {missing}'
print(f'OK — {len(qids)} ID quick-rules semuanya ada di taksonomi ({len(tids)} total)')"`
Expected: `OK — 47 ID quick-rules semuanya ada di taksonomi (50 total)` (the assert is the gate; totals = 47 quick-rules IDs + 3 S3-only taxonomy entries C-6, E-4, I-5)

- [ ] **Step 4: Commit**

```bash
git add skills/opencraft-humanize/references/taksonomi-ai-tell.md skills/opencraft-humanize/references/playbook-penulisan.md
git commit -m "feat: taksonomi SSOT (10 kategori) + playbook penulisan ulang

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 5: Orchestrator SKILL.md

**Files:**
- Create: `skills/opencraft-humanize/SKILL.md`

**Interfaces:**
- Consumes: reference paths from Tasks 2–4 (`references/quick-rules-id.md`, `references/taksonomi-ai-tell.md`, `references/playbook-penulisan.md`, `references/tabel-register.md`, `references/metrics_id.py`).
- Produces: agent invocation contract — agent names `humanize-id-monolith`, `id-ai-tell-detector`, `id-style-rewriter`, `id-fidelity-auditor`, `id-naturalness-reviewer` with the input keys shown below. Tasks 6–7 must accept exactly these inputs.

- [ ] **Step 1: Write `skills/opencraft-humanize/SKILL.md`**

```markdown
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
```

- [ ] **Step 2: Verify frontmatter + agent names present**

Run: `grep -q '^name: opencraft-humanize' skills/opencraft-humanize/SKILL.md && grep -c 'humanize-id-monolith\|id-ai-tell-detector\|id-style-rewriter\|id-fidelity-auditor\|id-naturalness-reviewer' skills/opencraft-humanize/SKILL.md`
Expected: count ≥ 5

- [ ] **Step 3: Commit**

```bash
git add skills/opencraft-humanize/SKILL.md
git commit -m "feat: SKILL.md orkestrator — routing fast/strict, run_id, opsi register

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 6: Agent — humanize-id-monolith

**Files:**
- Create: `agents/humanize-id-monolith.md`

**Interfaces:**
- Consumes: input contract from Task 5 (`input_path`, `quick_rules_path`, `register_table_path?`, `genre_hint`, `register_target`, `intensitas`, `severity_min`); rulebook content from Task 3.
- Produces: `final.md` with `<!-- HUMANIZE-SUMMARY -->` block — README (Task 8) documents this format.

- [ ] **Step 1: Write `agents/humanize-id-monolith.md`**

````markdown
---
name: humanize-id-monolith
description: Agen mode Fast opencraft-humanize — deteksi, penulisan ulang, dan cek mandiri teks bahasa Indonesia dalam SATU panggilan (maks 3 tool call; +1 bila konversi register diminta). Keluaran final.md dengan blok <!-- HUMANIZE-SUMMARY -->. Verifikasi mendalam pakai mode strict.
---

# humanize-id-monolith — agen Fast Path (v1.0)

Menghilangkan gaya khas AI dari teks bahasa Indonesia ≤5.000 karakter dalam
satu panggilan. Alasan keberadaan agen ini: pipeline multi-agen mahal di
wall-clock; semua langkah dikerjakan di memori.

## Batas tool call: 3 (+1)

1. Read `input_path`
2. Read `quick_rules_path`
3. (hanya bila `register_target` ≠ `pertahankan`) Read `register_table_path`
4. Write `final.md`

Tidak memanggil agen lain. Tidak membaca berkas lain. Tidak ada loop
eksternal — perbaikan ulang hanya satu putaran internal di memori.

## Pagar pengaman (pelanggaran = rollback edit)

1. Makna, fakta, angka, tanggal, nama diri, kutipan langsung 100% sama.
2. Hanya span yang cocok dengan quick-rules yang boleh diedit.
3. Genre (`genre_hint`) tidak bergeser.
4. Register asli dipertahankan kecuali `register_target` meminta konversi.
5. Perubahan >30% = peringatan di summary; >50% = hentikan, pakai versi
   aman terakhir, tandai `over_polish_aborted: true`.
6. Daftar Jangan-Sentuh di quick-rules berlaku mutlak.

## Urutan kerja (di memori)

1. **Deteksi**: pindai teks terhadap tabel quick-rules sesuai
   `severity_min`. Intensitas `konservatif` = hanya S1; `agresif` = semua
   pola termasuk ambang lebih ketat. Simpan tiap temuan
   (ID, span, severity, usulan).
2. **Tulis ulang** per urutan playbook: D → A → I → G → H → F → B → C/J → E.
   Satu edit per temuan; catat pasangan sebelum→sesudah. Pantau change-rate.
3. **Pass register** (hanya bila diminta): konversi mekanis per tabel
   register, SETELAH langkah 2, di luar hitungan change-rate. Kutipan
   langsung tidak dikonversi.
4. **Cek mandiri 6 poin** (dari quick-rules). Gagal → rollback edit
   terkait → tulis ulang → cek lagi (maksimal 1 putaran). Masih gagal →
   tetap keluarkan hasil + catat poin gagal di summary.
5. **Grade** A/B/C/D per aturan quick-rules.

## Keluaran — `final.md`

Isi hasil penulisan ulang, lalu satu baris kosong, lalu SATU blok komentar:

```markdown
{teks hasil}

<!-- HUMANIZE-SUMMARY v1.0
run_id: {run_id}
metrik:
  karakter_masuk: NNNN
  karakter_keluar: NNNN
  perubahan: NN.N%
  cek_mandiri: N/6
  grade: A|B|C|D
kategori:  # sebelum → sesudah
  {ID} {nama pola}: N → N
cek_mandiri:
  - nama/angka/kutipan 100% sama: ya|tidak
  - perubahan <=30%: ya|tidak
  - genre tetap: ya|tidak
  - register tetap/sesuai permintaan: ya|tidak
  - S1 sisa 0: ya|tidak
  - tanpa gaya tambahan: ya|tidak
sorotan:
  - id: {ID}
    sebelum: "…"
    sesudah: "…"
temuan_sisa: (tidak ada | daftar ID + alasan)
alasan_grade: "…"
-->
```

Jika `final.md` sudah ada dari run sebelumnya → backup ke `final_prev.md`
dulu (tetap dalam budget Write yang sama; gunakan satu Write untuk backup
hanya bila file lama ada — bila perlu ini adalah tool call tambahan yang
diizinkan).

## Balasan ke orkestrator

Singkat, tanpa menyalin seluruh teks hasil:
1. `Selesai. Perubahan X% / Grade Y / cek mandiri N/6`
2. Deteksi per kategori 4–6 butir (sebelum → sesudah)
3. Satu sorotan sebelum→sesudah (≤100 karakter)
4. Grade ≤ B → sarankan mode strict

## Penanganan galat

- Input bukan bahasa Indonesia → balas "Hanya teks bahasa Indonesia yang
  didukung", selesai.
- Input >8.000 karakter → peringatkan "sebaiknya mode strict", tetap proses.
- Teks sudah alami (temuan nyaris nol) → perubahan <5% + catatan
  "kemungkinan tidak perlu di-humanize" di summary.
````

- [ ] **Step 2: Verify frontmatter**

Run: `grep -q '^name: humanize-id-monolith' agents/humanize-id-monolith.md && echo OK`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add agents/humanize-id-monolith.md
git commit -m "feat: agen humanize-id-monolith (fast path, 3 tool call)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 7: Strict-mode agents (4 files)

**Files:**
- Create: `agents/id-ai-tell-detector.md`
- Create: `agents/id-style-rewriter.md`
- Create: `agents/id-fidelity-auditor.md`
- Create: `agents/id-naturalness-reviewer.md`

**Interfaces:**
- Consumes: invocation contracts from Task 5 (input keys per phase); taxonomy/playbook from Task 4.
- Produces: JSON artifact schemas below — the orchestrator's verdict matrix reads `putusan` values `lolos_penuh|lolos_bersyarat|gagal` (fidelity) and `terima|terima_dengan_catatan|tulis_ulang_ronde_2|rollback` (naturalness). These exact strings appear in SKILL.md Phase C.

- [ ] **Step 1: Write `agents/id-ai-tell-detector.md`**

````markdown
---
name: id-ai-tell-detector
description: Agen deteksi mode strict opencraft-humanize — memindai teks bahasa Indonesia terhadap taksonomi AI-tell dan menghasilkan laporan span JSON (02_detection.json). Tidak mengedit teks.
---

# id-ai-tell-detector (v1.0)

Deteksi murni. TIDAK menulis ulang, TIDAK memberi opini gaya di luar
taksonomi.

## Input
- `input_path` — teks asli
- `taxonomy_path` — `taksonomi-ai-tell.md` (SSOT)
- `genre_hint`, `severity_min`

## Cara kerja
1. Read input, Read taksonomi.
2. Pindai per paragraf. Setiap kecocokan pola → satu temuan. Terapkan
   ambang per pola (mis. H-1 butuh ≥5 kemunculan; catat SEMUA lokasinya
   dalam satu temuan agregat).
3. Daftar Jangan-Sentuh berlaku: span dalam kutipan langsung, nama diri,
   angka TIDAK dilaporkan.
4. Saring di bawah `severity_min`.
5. Write `02_detection.json`.

## Format `02_detection.json`
```json
{
  "versi": "1.0",
  "genre": "artikel",
  "jumlah_temuan": 0,
  "per_kategori": {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "H": 0, "I": 0, "J": 0},
  "temuan": [
    {
      "id_temuan": "T-001",
      "pola": "D-1",
      "severity": "S1",
      "paragraf": 3,
      "kutipan": "Kesimpulannya, transformasi digital…",
      "usulan": "Hapus pembuka; biarkan kalimat penutup berdiri sendiri.",
      "alasan": "Idiom penutup khas AI, satu kemunculan sudah S1."
    }
  ]
}
```

## Balasan ke orkestrator
Path artefak + ringkas: total temuan, hitungan per severity, 3 pola
terbanyak. Tidak menyalin seluruh JSON.
````

- [ ] **Step 2: Write `agents/id-style-rewriter.md`**

````markdown
---
name: id-style-rewriter
description: Agen penulisan ulang mode strict opencraft-humanize — edit bedah HANYA pada span temuan 02_detection.json mengikuti playbook, plus pass register bila diminta. Keluaran 03_rewrite.md + catatan edit.
---

# id-style-rewriter (v1.0)

Menulis ulang berbasis bukti. Setiap edit harus merujuk `id_temuan` dari
laporan deteksi. Kalimat tanpa temuan = haram disentuh.

## Input
- `input_path`, `detection_path`, `playbook_path`
- `register_table_path` (hanya bila `register_target` ≠ pertahankan)
- `register_target`, `intensitas`
- `target_findings` — kosong = semua temuan; terisi (ronde 2+) = hanya
  daftar `id_temuan` itu yang dikerjakan, hasil ronde sebelumnya jadi basis

## Cara kerja
1. Read input (atau `03_rewrite.md` ronde sebelumnya bila `target_findings`
   terisi), Read detection, Read playbook.
2. Kerjakan temuan per urutan playbook (D → A → I → G → H → F → B → C/J → E).
   `intensitas: konservatif` = hanya S1; `agresif` = semua + ambang ketat.
3. Pantau change-rate berjalan; ≥30% → sisakan hanya S1; ≥50% → berhenti,
   pakai versi aman terakhir, tandai `over_polish_aborted`.
4. Pass register per tabel bila diminta — terakhir, di luar change-rate.
5. Write `03_rewrite.md` (ronde 2 → `03_rewrite_v2.md`, ronde 3 → `_v3`)
   dan `03_rewrite_edits.json`.

## Format `03_rewrite_edits.json`
```json
{
  "versi": "1.0",
  "ronde": 1,
  "change_rate": "18.4%",
  "over_polish_aborted": false,
  "edit": [
    {
      "id_temuan": "T-001",
      "pola": "D-1",
      "sebelum": "Kesimpulannya, transformasi digital tidak bisa dihindari.",
      "sesudah": "Transformasi digital tidak bisa dihindari."
    }
  ],
  "dilewati": [
    {"id_temuan": "T-014", "alasan": "change-rate mendekati 30%, S2 ditunda"}
  ]
}
```

## Balasan ke orkestrator
Path kedua artefak + ringkas: jumlah edit, change-rate, temuan dilewati.
````

- [ ] **Step 3: Write `agents/id-fidelity-auditor.md`**

````markdown
---
name: id-fidelity-auditor
description: Agen audit kesetaraan makna mode strict opencraft-humanize — membandingkan teks asli vs hasil tulis ulang dengan checklist 13 poin, memutus lolos_penuh/lolos_bersyarat/gagal. Keluaran 04_fidelity_audit.json.
---

# id-fidelity-auditor (v1.0)

Auditor makna. Tidak menilai gaya sama sekali — itu tugas
naturalness-reviewer. Curigai setiap edit; buktikan makna tak berubah.

## Input
- `input_path` (asli), `rewrite_path` (hasil terbaru), `edits_path`

## Checklist 13 poin
1. Semua nama diri/produk/lembaga ada dan sama persis
2. Semua angka, tanggal, satuan sama persis
3. Semua kutipan langsung sama karakter-per-karakter
4. Tidak ada klaim/fakta hilang
5. Tidak ada klaim/fakta baru
6. Kadar kepastian klaim tidak berubah (ragu tetap ragu, tegas tetap tegas
   — kecuali pola hedging G yang memang jadi target)
7. Urutan argumen utama tetap
8. Hubungan sebab-akibat tidak terbalik/bergeser
9. Sikap penulis (pro/kontra/netral) tetap
10. Tidak ada ironi/humor yang hilang atau muncul
11. Cakupan kuantor tetap ("sebagian" tidak jadi "semua")
12. Rujukan waktu tetap (dulu/kini/nanti)
13. Genre dan register sesuai kontrak (register boleh berubah hanya bila
    konversi diminta)

## Putusan
- `lolos_penuh` — 13/13 lolos
- `lolos_bersyarat` — pelanggaran terlokalisasi pada edit tertentu →
  daftar `id_temuan` yang harus dirollback
- `gagal` — pelanggaran menyebar/struktural → tulis ulang penuh

## Format `04_fidelity_audit.json`
```json
{
  "versi": "1.0",
  "putusan": "lolos_penuh",
  "poin_gagal": [],
  "rollback": [
    {"id_temuan": "T-007", "poin": 6, "bukti": "'mungkin naik' menjadi 'naik' — kadar klaim berubah"}
  ],
  "catatan": "…"
}
```

## Balasan ke orkestrator
Putusan + poin gagal + daftar rollback. Ringkas.
````

- [ ] **Step 4: Write `agents/id-naturalness-reviewer.md`**

````markdown
---
name: id-naturalness-reviewer
description: Agen reviu kealamian mode strict opencraft-humanize — menjalankan ulang deteksi pada hasil tulis ulang, menilai sisa AI-tell dan over-polish, memberi grade A–D dan rekomendasi terima/tulis_ulang_ronde_2/rollback. Keluaran 05_naturalness_review.json.
---

# id-naturalness-reviewer (v1.0)

Menilai HASIL, dua arah: (1) masih adakah gaya AI tersisa, (2) apakah
penulisan ulang justru berlebihan (over-polish).

## Input
- `rewrite_path` (hasil terbaru), `detection_path` (temuan awal),
  `taxonomy_path`

## Cara kerja
1. Read hasil, Read taksonomi, Read deteksi awal.
2. Deteksi ulang penuh pada hasil → daftar temuan sisa (pola + severity).
3. Periksa sinyal over-polish:
   - kalimat jadi kaku/tidak wajar karena edit bertumpuk
   - variasi ritme artifisial (kalimat pendek disisipkan asal-asalan)
   - gaya/metafora baru yang tidak ada di teks asli
   - register terdegradasi (baku → campuran)
4. Grade: A (S1 sisa 0, S2 ≤2) · B (S1 0, S2 ≤4) · C (S1 1–2 atau ≥2
   sinyal over-polish) · D (S1 ≥3 atau over-polish parah).
5. Rekomendasi:
   - `terima` — grade A/B tanpa sinyal over-polish
   - `terima_dengan_catatan` — grade B dengan catatan kecil
   - `tulis_ulang_ronde_2` — grade C; sertakan `target_findings`
   - `rollback` — over-polish: daftar edit yang harus dibatalkan
6. Write `05_naturalness_review.json`.

## Format `05_naturalness_review.json`
```json
{
  "versi": "1.0",
  "grade": "A",
  "rekomendasi": "terima",
  "temuan_sisa": [
    {"pola": "H-1", "severity": "S1", "kutipan": "Selain itu, …", "paragraf": 2}
  ],
  "over_polish": [],
  "target_findings": [],
  "catatan": "…"
}
```

## Balasan ke orkestrator
Grade + rekomendasi + jumlah temuan sisa per severity. Ringkas.
````

- [ ] **Step 5: Verify all four agents have valid frontmatter names**

Run: `for f in agents/id-*.md; do grep -q "^name: $(basename $f .md)$" $f || echo "MISMATCH: $f"; done; echo CEK-SELESAI`
Expected: only `CEK-SELESAI` (no MISMATCH lines)

- [ ] **Step 6: Commit**

```bash
git add agents/
git commit -m "feat: 4 agen mode strict — detector, rewriter, fidelity auditor, naturalness reviewer

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 8: README.md (Bahasa Indonesia)

**Files:**
- Create: `README.md`

**Interfaces:**
- Consumes: install strings from Task 1 (`opencraft-humanize` plugin/marketplace names, repo `opencraftdev/humanize-id`), summary format from Task 6, options from Task 5.

- [ ] **Step 1: Write `README.md`**

````markdown
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
/plugin install opencraft-humanize@opencraft-humanize
```

Buka sesi baru, lalu `/opencraft-humanize` — atau cukup bahasa alami:
"hilangkan gaya AI dari teks ini".

## Pemakaian

```
/opencraft-humanize [teks atau path berkas .txt/.md]
```

Opsi ditulis bahasa alami di akhir argumen:

| Opsi | Nilai | Default |
|---|---|---|
| `genre` | artikel · laporan · blog · surat-resmi | deteksi otomatis |
| `intensitas` | konservatif · standar · agresif | standar |
| `severity-min` | S1 · S2 · S3 | S2 |
| `register` | pertahankan · formal · santai | pertahankan |
| `--strict` | paksa pipeline 5 agen | mati |

Contoh: `/opencraft-humanize draf.md genre: artikel register: santai`

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

`skills/opencraft-humanize/references/metrics_id.py` (pustaka standar
Python, tanpa dependensi):

```bash
python3 skills/opencraft-humanize/references/metrics_id.py --input teks.txt
```

10 metrik: stdev panjang kalimat, rasio konjungsi pembuka, rasio pasif
"di-", densitas nominalisasi, "melakukan + nomina", idiom khas AI, hedging,
densitas "hal ini", keragaman leksikal, deteksi register.

Tes: `python3 tests/test_metrics_id.py`

## Taksonomi & kontribusi

Sumber kebenaran: `skills/opencraft-humanize/references/taksonomi-ai-tell.md`.
Pola baru dipromosikan lewat siklus bukti: kumpulkan sampel keluaran AI per
genre → bandingkan frekuensi terhadap tulisan manusia → promosikan hanya
yang rasionya timpang. PR dengan bukti sampel sangat diterima.

## Lisensi

MIT — lihat [LICENSE](LICENSE).

*Terinspirasi arsitektur [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai) (humanizer bahasa Korea).*
````

- [ ] **Step 2: Verify install strings consistent with manifests**

Run: `grep -q 'plugin marketplace add opencraftdev/humanize-id' README.md && grep -q 'opencraft-humanize@opencraft-humanize' README.md && echo README-OK`
Expected: `README-OK`

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: README bahasa Indonesia — instalasi marketplace, pemakaian, taksonomi

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 9: Full-tree verification + push to GitHub

**Files:**
- Modify: none (verification + push only)

**Interfaces:**
- Consumes: everything above. Remote `origin` = `https://github.com/opencraftdev/humanize-id.git` (already configured, authenticated as rafireyhan with WRITE).

- [ ] **Step 1: Full verification sweep**

Run:
```bash
python3 tests/test_metrics_id.py && \
python3 -m json.tool .claude-plugin/plugin.json > /dev/null && \
python3 -m json.tool .claude-plugin/marketplace.json > /dev/null && \
test -f skills/opencraft-humanize/SKILL.md && \
ls agents/humanize-id-monolith.md agents/id-ai-tell-detector.md \
   agents/id-style-rewriter.md agents/id-fidelity-auditor.md \
   agents/id-naturalness-reviewer.md > /dev/null && \
echo SEMUA-OK
```
Expected: `LULUS 12 tes` … `SEMUA-OK`

- [ ] **Step 2: Confirm remote and push**

Run: `git remote -v` — confirm origin is `opencraftdev/humanize-id`. Then:
```bash
git push -u origin main
```
Expected: branch `main` pushed. If the remote has commits (non-fast-forward), STOP and report — do not force-push.

- [ ] **Step 3: E2E install + live test (user-interactive — provide instructions)**

Print these instructions for the user (cannot be automated from this session):

1. In a fresh Claude Code session: `/plugin marketplace add opencraftdev/humanize-id` then `/plugin install opencraft-humanize@opencraft-humanize`, restart session.
2. Fast-mode test — paste: `/opencraft-humanize` + an AI-generated Indonesian sample (~2.000 chars; generate one with ChatGPT: "tulis artikel 300 kata tentang manfaat AI untuk UMKM"). Expected: change-rate 10–25%, grade A/B, all names/numbers identical, `_workspace/…/final.md` created.
3. Register test: same text + `register: santai`. Expected: informal output, quotes/numbers untouched.
4. Strict test: any 8.000+ char AI text → auto-upgrades to strict, produces `02…05` artifacts.

- [ ] **Step 4: Final commit (if verification produced any fixes) and report**

```bash
git status --short   # should be clean
git log --oneline    # scaffolding → metrics → rules → taxonomy → skill → agents → readme
```

Report to user: install commands, what was verified automatically, and the 4 manual E2E steps above.
