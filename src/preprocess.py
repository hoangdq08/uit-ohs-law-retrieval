"""Tiền xử lý văn bản tiếng Việt: normalize -> word segmentation -> stopwords.

Các cờ `segment` / `remove_stopwords` phục vụ Ablation Study.
"""
from __future__ import annotations

import re
import sys
import unicodedata
from functools import lru_cache

from src.config import STOPWORDS_PATH

_URL = re.compile(r"https?://\S+|www\.\S+")
_EMAIL = re.compile(r"\S+@\S+")
_HTML = re.compile(r"<[^>]+>")
# Giữ chữ (gồm tiếng Việt có dấu), số và khoảng trắng.
_NON_WORD = re.compile(r"[^\w\s]", flags=re.UNICODE)
_SPACES = re.compile(r"\s+")


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFC", str(text)).lower()
    text = _HTML.sub(" ", text)
    text = _URL.sub(" ", text)
    text = _EMAIL.sub(" ", text)
    text = _NON_WORD.sub(" ", text).replace("_", " ")
    return _SPACES.sub(" ", text).strip()


def segment(text: str) -> str:
    from underthesea import word_tokenize  # import chậm, chỉ load khi cần

    return word_tokenize(text, format="text")


@lru_cache(maxsize=1)
def load_stopwords() -> frozenset[str]:
    lines = STOPWORDS_PATH.read_text(encoding="utf-8").splitlines()
    return frozenset(l.strip() for l in lines if l.strip() and not l.startswith("#"))


def remove_stopwords(text: str) -> str:
    stop = load_stopwords()
    return " ".join(t for t in text.split() if t not in stop)


def preprocess(text: str, *, segment_words: bool = True, drop_stopwords: bool = True) -> str:
    text = normalize(text)
    if segment_words:
        text = segment(text)
    if drop_stopwords:
        text = remove_stopwords(text)
    return text


if __name__ == "__main__":
    sample = " ".join(sys.argv[1:]) or "Công nhân ngã giàn giáo thì công ty bồi thường gì?"
    print("raw   :", sample)
    print("norm  :", normalize(sample))
    print("full  :", preprocess(sample))
    print("no_seg:", preprocess(sample, segment_words=False))
    print("no_sw :", preprocess(sample, drop_stopwords=False))
