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
    "lebih lanjut", "sementara itu",
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
