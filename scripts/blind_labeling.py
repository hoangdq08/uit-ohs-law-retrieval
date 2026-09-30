"""Phiếu gán nhãn mù cho câu hỏi thật + tính độ đồng thuận.

Mục đích: người gán nhãn độc lập (không xem nhãn LLM), đo đồng thuận với nhãn GPT gốc (Cohen's kappa trên lớp,
% trùng Điều). Phiếu: data/raw/blind/annotator_A.csv, annotator_B.csv (cùng thứ tự, KHÔNG có nhãn LLM).
Mỗi người điền decision (in_scope | out_of_scope | multi_intent) và article_id (khi in_scope).
Phiếu có cột annotation_source chứa "ai" (vd ai_assisted) được coi là LLM thứ hai, không tính là người.
Nhãn GPT được so từ bản đóng băng blind/llm_labels_frozen.jsonl (chụp lần chạy score đầu tiên), để việc sửa
real_labeled.jsonl theo kết quả review không làm đồng thuận bị thổi phồng.

Chạy:
  python -m scripts.blind_labeling make    # tạo phiếu (KHÔNG ghi đè phiếu đã có người điền, trừ khi --force)
  python -m scripts.blind_labeling score   # tính đồng thuận -> reports/agreement.json
"""
from __future__ import annotations

import argparse
import json
import sys

import pandas as pd
from sklearn.metrics import cohen_kappa_score

from src.config import ARTICLE_TO_LABEL, RAW_DIR, ROOT

BLIND = RAW_DIR / "blind"
SRC = RAW_DIR / "real_labeled.jsonl"
FROZEN = BLIND / "llm_labels_frozen.jsonl"
CAND = RAW_DIR / "real_candidates.jsonl"
OUT = ROOT / "reports" / "agreement.json"
DECISIONS = {"in_scope", "out_of_scope", "multi_intent"}


def _read_jsonl(p):
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def make(force: bool) -> int:
    rows = _read_jsonl(SRC)
    ans = {r["url"]: r.get("answer", "") for r in _read_jsonl(CAND)} if CAND.exists() else {}
    BLIND.mkdir(parents=True, exist_ok=True)
    sheet = pd.DataFrame({
        "row": range(len(rows)),  # = số dòng trong real_labeled.jsonl (đếm từ 0)
        "question": [r["question"] for r in rows],
        "answer_excerpt": [ans.get(r["url"], "")[:1500] for r in rows],
        "url": [r["url"] for r in rows],
        "decision": "", "article_id": "", "note": "",
    })
    for who in ("A", "B"):
        p = BLIND / f"annotator_{who}.csv"
        if p.exists() and not force:
            filled = pd.read_csv(p, dtype=str).get("decision", pd.Series(dtype=str)).fillna("").str.strip().ne("").sum()
            if filled:
                print(f"{p} đã có {filled} dòng được điền, không ghi đè (dùng --force nếu chắc chắn).")
                return 1
        sheet.to_csv(p, index=False, encoding="utf-8-sig")  # utf-8-sig để Excel mở đúng tiếng Việt
        print(f"-> {p} ({len(sheet)} câu)")
    return 0


def _load(who: str) -> pd.DataFrame:
    d = pd.read_csv(BLIND / f"annotator_{who}.csv", dtype=str).fillna("")
    d["decision"] = d["decision"].str.strip()
    d["article_id"] = pd.to_numeric(d["article_id"].str.strip(), errors="coerce")
    return d


def _cls(dec, aid):
    """Nhãn so sánh: lớp 0–7 nếu in_scope, ngược lại chính decision."""
    if dec == "in_scope" and aid == aid and int(aid) in ARTICLE_TO_LABEL:
        return f"C{ARTICLE_TO_LABEL[int(aid)]}"
    return dec


def score() -> int:
    sheets = {w: _load(w) for w in ("A", "B") if (BLIND / f"annotator_{w}.csv").exists()}
    if not FROZEN.exists():
        FROZEN.write_text(SRC.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"Đóng băng nhãn GPT gốc -> {FROZEN}")
    llm = _read_jsonl(FROZEN)
    bad = [f"{w} dòng {r}: decision={d!r}" for w, df in sheets.items()
           for r, d in zip(df["row"], df["decision"]) if d and d not in DECISIONS]
    bad += [f"{w} dòng {r}: in_scope thiếu/sai article_id" for w, df in sheets.items()
            for r, d, x in zip(df["row"], df["decision"], df["article_id"])
            if d == "in_scope" and not (x == x and int(x) in ARTICLE_TO_LABEL)]
    if bad:
        print("\n".join(bad)); return 1
    # Nguồn nhãn: "GPT" (nhãn gốc) + từng phiếu. Mỗi nguồn: (tên, là người?, {row: (decision, article_id)})
    src = {"GPT": (False, {i: (r["decision"], r.get("article_id") or float("nan")) for i, r in enumerate(llm)})}
    for w, df in sheets.items():
        is_ai = df.get("annotation_source", pd.Series(dtype=str)).str.lower().str.startswith("ai").any()
        src[w] = (not is_ai, {int(r): (d, x) for r, d, x in zip(df["row"], df["decision"], df["article_id"]) if d})
    humans = [w for w, (h, _) in src.items() if h]
    if not humans:
        print("Chưa có phiếu nào do người điền."); return 1

    def pair(p, q):
        rows = sorted(set(src[p][1]) & set(src[q][1]))
        cp = [_cls(*src[p][1][r]) for r in rows]
        cq = [_cls(*src[q][1][r]) for r in rows]
        both_in = [r for r in rows if src[p][1][r][0] == src[q][1][r][0] == "in_scope"]
        art = sum(float(src[p][1][r][1]) == float(src[q][1][r][1]) for r in both_in)
        return {"a": p, "b": q, "n": len(rows), "agreement": sum(x == y for x, y in zip(cp, cq)) / len(rows),
                "cohen_kappa": cohen_kappa_score(cp, cq),
                "article_agreement_when_both_in_scope": (art / len(both_in)) if both_in else None,
                "n_both_in_scope": len(both_in),
                "disagreements": [{"row": r, p: x, q: y} for r, x, y in zip(rows, cp, cq) if x != y]}

    names = list(src)
    pairs = [pair(p, q) for i, p in enumerate(names) for q in names[i + 1:]]
    res = {"sources": {w: ("human" if h else "llm") for w, (h, _) in src.items()},
           "n_real": len(llm), "pairs": pairs}
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=2, default=float), encoding="utf-8")
    for pr in pairs:
        tag = lambda w: f"{w}({res['sources'][w]})"
        print(f"{tag(pr['a'])} vs {tag(pr['b'])}: {pr['n']} câu, đồng thuận {pr['agreement']:.1%}, "
              f"kappa {pr['cohen_kappa']:.3f}, khác {len(pr['disagreements'])} câu")
    print(f"-> {OUT}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["make", "score"])
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    sys.exit(make(a.force) if a.cmd == "make" else score())
