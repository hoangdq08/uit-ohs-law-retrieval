"""Kiểm tra file câu hỏi sinh ra: data/raw/gen/c{k}.jsonl.

Mỗi dòng: {"seed_id": "c3-001", "article_id": 21, "style": "neutral|worker|hr|complaint|short",
           "question": "..."}
Mỗi seed_id có đúng 5 dòng (1 neutral + 4 paraphrase), cùng article_id.
Chạy: python -m scripts.validate_generated [k ...]
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict

from src.config import LABELS, RAW_DIR

GEN_DIR = RAW_DIR / "gen"
STYLES = {"neutral", "worker", "hr", "complaint", "short"}
SEEDS_PER_CLASS = 40
_ID = re.compile(r"^c(\d)-\d{3}$")


def norm(q: str) -> str:
    q = unicodedata.normalize("NFC", q).lower()
    return re.sub(r"[^\w\s]", "", q).strip()


def validate(k: int) -> list[str]:
    path = GEN_DIR / f"c{k}.jsonl"
    if not path.exists():
        return [f"c{k}: thiếu file {path}"]
    errs: list[str] = []
    allowed = set(LABELS[k][2])
    groups: dict[str, list[dict]] = defaultdict(list)
    seen: Counter = Counter()
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError as e:
            errs.append(f"c{k}:{i} JSON lỗi: {e}")
            continue
        sid, art, style, q = r.get("seed_id"), r.get("article_id"), r.get("style"), r.get("question", "")
        m = _ID.match(str(sid))
        if not m or int(m.group(1)) != k:
            errs.append(f"c{k}:{i} seed_id sai định dạng: {sid}")
        if art not in allowed:
            errs.append(f"c{k}:{i} article_id {art} không thuộc lớp {k}")
        if style not in STYLES:
            errs.append(f"c{k}:{i} style lạ: {style}")
        n_words = len(q.split())
        if not 2 <= n_words <= 60:
            errs.append(f"c{k}:{i} độ dài {n_words} từ bất thường")
        seen[norm(q)] += 1
        groups[sid].append(r)
    for sid, rows in groups.items():
        styles = sorted(r["style"] for r in rows)
        if styles != sorted(STYLES):
            errs.append(f"c{k} {sid}: styles {styles}, cần đủ 5 style mỗi style 1 lần")
        if len({r["article_id"] for r in rows}) != 1:
            errs.append(f"c{k} {sid}: article_id không đồng nhất trong nhóm")
    if len(groups) != SEEDS_PER_CLASS:
        errs.append(f"c{k}: {len(groups)} seed, cần {SEEDS_PER_CLASS}")
    dups = [q for q, c in seen.items() if c > 1]
    if dups:
        errs.append(f"c{k}: {len(dups)} câu trùng lặp, vd: {dups[0][:80]}")
    arts = Counter(g[0]["article_id"] for g in groups.values())
    missing = allowed - set(arts)
    if missing:
        errs.append(f"c{k}: chưa có seed cho Điều {sorted(missing)}")
    return errs


if __name__ == "__main__":
    ks = [int(a) for a in sys.argv[1:]] or list(LABELS)
    total = 0
    for k in ks:
        e = validate(k)
        total += len(e)
        print(f"c{k}: {'OK' if not e else f'{len(e)} lỗi'}")
        for x in e[:15]:
            print("  -", x)
    sys.exit(1 if total else 0)
