"""Tải và parse Luật An toàn, vệ sinh lao động -> data/ohs_law_articles.json.

Nguồn: Văn bản hợp nhất 14/VBHN-VPQH (16/09/2024) trên LuatVietnam, tức Luật 84/2015/QH13
đã cập nhật sửa đổi của Luật BHXH 41/2024/QH15 (hiệu lực 01/07/2025).
Chạy: python -m scripts.build_articles [--refresh]
"""
from __future__ import annotations

import html
import json
import re
import sys
import unicodedata
import urllib.request

from src.config import ARTICLE_TO_LABEL, ARTICLES_PATH, LABEL_CODES, RAW_DIR

SOURCE_URL = ("https://luatvietnam.vn/lao-dong/"
              "van-ban-hop-nhat-14-vbhn-vpqh-2024-hop-nhat-luat-an-toan-ve-sinh-lao-dong-375139-d5.html")
SOURCE_NAME = "Văn bản hợp nhất 14/VBHN-VPQH ngày 16/09/2024 (Luật 84/2015/QH13, sửa đổi bởi Luật 41/2024/QH15)"
CACHE_PATH = RAW_DIR / "vbhn_14_2024_luatvietnam.html"  # gitignored
N_ARTICLES = 93

_ARTICLE = re.compile(r"^Điều (\d+)\.\s*(.+)$")
_CHAPTER = re.compile(r"^Chương ([IVX]+)\.\s*(.+)$")
_SECTION = re.compile(r"^Mục (\d+)\.\s*(.+)$")
# Marker chú thích của VBHN: "3 [3] ", " [1] ", hoặc số chú thích dính cuối tiêu đề ("... THI HÀNH 8").
_FOOTNOTE = re.compile(r"\s*\b(\d+) \[\1\]\s*|\s*\[\d+\]\s*")
_TRAILING_NUM = re.compile(r"\s+\d+$")
_NOISE = {"Đang theo dõi", "Phân tích Đang theo dõi"}


def fetch(refresh: bool = False) -> str:
    if CACHE_PATH.exists() and not refresh:
        return CACHE_PATH.read_text(encoding="utf-8")
    req = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"})
    raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    CACHE_PATH.write_text(raw, encoding="utf-8")
    return raw


def html_to_lines(raw: str) -> list[str]:
    # Tooltip "được hướng dẫn bởi..." nằm trong data-title, bỏ trước khi strip tag.
    s = re.sub(r'data-title="[^"]*"', "", raw)
    s = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", s)
    s = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</h\d>", "\n", s)
    s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    s = unicodedata.normalize("NFC", s)
    lines = (re.sub(r"[ \t\xa0]+", " ", l).strip() for l in s.splitlines())
    return [l for l in lines if l and l not in _NOISE]


def _strip_footnote(line: str) -> tuple[str, bool]:
    cleaned = _FOOTNOTE.sub(" ", line)
    return re.sub(r"\s+", " ", cleaned).strip(), cleaned != line


def parse(lines: list[str]) -> list[dict]:
    start = lines.index("Chương I. QUY ĐỊNH CHUNG")
    end = lines.index("VĂN PHÒNG QUỐC HỘI", start)

    articles: list[dict] = []
    chapter = section = None
    for line in lines[start:end]:
        if m := _CHAPTER.match(line):
            chapter = {"number": m.group(1), "title": _TRAILING_NUM.sub("", m.group(2)).strip()}
            section = None
            continue
        if m := _SECTION.match(line):
            section = {"number": int(m.group(1)), "title": m.group(2).strip()}
            continue
        if m := _ARTICLE.match(line):
            title, _ = _strip_footnote(m.group(2))
            articles.append({
                "article_id": int(m.group(1)),
                "title": title,
                "chapter": dict(chapter),
                "section": dict(section) if section else None,
                "amended_2024": False,
                "paragraphs": [],
            })
            continue
        text, had_marker = _strip_footnote(line)
        if not text:  # dòng chỉ có marker, vd "[8]" gắn với tiêu đề Chương VII
            continue
        articles[-1]["paragraphs"].append(text)
        articles[-1]["amended_2024"] |= had_marker
    return articles


def build(refresh: bool = False) -> list[dict]:
    articles = parse(html_to_lines(fetch(refresh)))
    ids = [a["article_id"] for a in articles]
    assert ids == list(range(1, N_ARTICLES + 1)), f"Thiếu/lặp Điều: {ids}"
    for a in articles:
        assert a["paragraphs"], f"Điều {a['article_id']} rỗng"
        blob = a["title"] + " ".join(a["paragraphs"])
        assert "hướng dẫn bởi" not in blob and "[" not in blob, f"Điều {a['article_id']} còn chú thích"
        label = ARTICLE_TO_LABEL.get(a["article_id"])
        a["label_id"] = label
        a["label_code"] = LABEL_CODES.get(label)
        a["text"] = "\n".join(a["paragraphs"])
    return articles


if __name__ == "__main__":
    arts = build(refresh="--refresh" in sys.argv)
    payload = {"law": "Luật An toàn, vệ sinh lao động", "source": SOURCE_NAME,
               "source_url": SOURCE_URL, "articles": arts}
    ARTICLES_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    mapped = sum(a["label_id"] is not None for a in arts)
    amended = [a["article_id"] for a in arts if a["amended_2024"]]
    print(f"{len(arts)} articles -> {ARTICLES_PATH.name} ({mapped} mapped, amended_2024={amended})")
