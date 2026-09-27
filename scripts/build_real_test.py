"""Sinh data/processed/real_test.csv từ data/raw/real_labeled.jsonl (nguồn nhãn duy nhất của câu hỏi thật).

Sửa nhãn: chỉ sửa real_labeled.jsonl, mỗi dòng có
  decision   : "in_scope" | "out_of_scope" | "multi_intent"
  article_id : số Điều (1–62) trả lời trực tiếp câu hỏi, bắt buộc khi decision = in_scope, null nếu khác
Nhãn lớp suy ra từ Điều (ARTICLE_TO_LABEL), giống dữ liệu synthetic, người gán không chọn lớp.

Chạy: python -m scripts.build_real_test   (rồi chạy lại notebook, report, slides)
"""
from __future__ import annotations

import collections
import json
import sys

import pandas as pd

from src.config import ARTICLE_TO_LABEL, LABEL_CODES, RAW_DIR
from src.dataset import REAL_TEST_PATH

SRC = RAW_DIR / "real_labeled.jsonl"
DECISIONS = {"in_scope", "out_of_scope", "multi_intent"}


def main() -> int:
    rows = [json.loads(l) for l in SRC.read_text(encoding="utf-8").splitlines() if l.strip()]
    errs, out = [], []
    for i, r in enumerate(rows):  # i = số dòng đếm từ 0, khớp cách đánh số khi review
        d = r.get("decision")
        if d not in DECISIONS:
            errs.append(f"dòng {i}: decision không hợp lệ: {d!r}")
            continue
        if d != "in_scope":
            continue
        aid = r.get("article_id")
        if not isinstance(aid, int) or aid not in ARTICLE_TO_LABEL:
            errs.append(f"dòng {i}: in_scope nhưng article_id={aid!r} không thuộc Điều 1–62 trong phạm vi")
            continue
        lid = ARTICLE_TO_LABEL[aid]
        out.append({"question": r["question"], "article_id": aid, "label_id": lid,
                    "label_code": LABEL_CODES[lid], "url": r.get("url", "")})
    if errs:
        print("\n".join(errs))
        print(f"{len(errs)} lỗi, không ghi file.")
        return 1

    df = pd.DataFrame(out)
    df.insert(0, "id", range(len(df)))
    df.to_csv(REAL_TEST_PATH, index=False)
    print(f"{len(rows)} câu: " + ", ".join(f"{k} {v}" for k, v in collections.Counter(r["decision"] for r in rows).items()))
    print(f"-> {REAL_TEST_PATH} ({len(df)} câu)")
    print(df["label_code"].value_counts().to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
