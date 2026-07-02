"""Tes metrics_id — jalankan: python3 tests/test_metrics_id.py"""
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "skills", "humanize", "references"))

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
