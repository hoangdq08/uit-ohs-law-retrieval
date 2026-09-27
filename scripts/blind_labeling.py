"""Phiếu gán nhãn mù cho câu hỏi thật + tính độ đồng thuận.

Mục đích: 2 thành viên tự gán nhãn độc lập (không xem nhãn LLM), đo:
  - đồng thuận người A vs người B (Cohen's kappa trên lớp, % trùng Điều)
  - đồng thuận người (khi A và B thống nhất) vs LLM
Phiếu: data/raw/blind/annotator_A.csv, annotator_B.csv (cùng thứ tự, KHÔNG có nhãn LLM).
Mỗi người chỉ điền 2 cột: decision (in_scope | out_of_scope | multi_intent) và article_id (khi in_scope).

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
    a, b = _load("A"), _load("B")
    llm = _read_jsonl(SRC)
    done = (a["decision"] != "") & (b["decision"] != "")
    bad = [f"{w} dòng {r}: decision={d!r}" for w, df in (("A", a), ("B", b))
           for r, d in zip(df["row"], df["decision"]) if d and d not in DECISIONS]
    bad += [f"{w} dòng {r}: in_scope thiếu/sai article_id" for w, df in (("A", a), ("B", b))
            for r, d, x in zip(df["row"], df["decision"], df["article_id"])
            if d == "in_scope" and not (x == x and int(x) in ARTICLE_TO_LABEL)]
    if bad:
        print("\n".join(bad)); return 1
    idx = done[done].index
    if len(idx) == 0:
        print("Chưa có dòng nào được cả A và B điền."); return 1
    ca = [_cls(a.at[i, "decision"], a.at[i, "article_id"]) for i in idx]
    cb = [_cls(b.at[i, "decision"], b.at[i, "article_id"]) for i in idx]
    cl = [_cls(llm[int(a.at[i, "row"])]["decision"], llm[int(a.at[i, "row"])].get("article_id") or float("nan")) for i in idx]
    agree_ab = [x == y for x, y in zip(ca, cb)]
    both_in = [i for i in idx if a.at[i, "decision"] == b.at[i, "decision"] == "in_scope"]
    art_ab = sum(a.at[i, "article_id"] == b.at[i, "article_id"] for i in both_in)
    cons = [(x, z) for x, y, z in zip(ca, cb, cl) if x == y]  # nhãn đồng thuận của người vs LLM
    res = {
        "n_scored": len(idx),
        "human_human": {"agreement": sum(agree_ab) / len(idx), "cohen_kappa": cohen_kappa_score(ca, cb),
                        "article_agreement_when_both_in_scope": (art_ab / len(both_in)) if both_in else None,
                        "n_both_in_scope": len(both_in)},
        "human_vs_llm": {"n_human_consensus": len(cons),
                         "agreement": (sum(x == z for x, z in cons) / len(cons)) if cons else None,
                         "cohen_kappa": cohen_kappa_score([x for x, _ in cons], [z for _, z in cons]) if len(cons) > 1 else None},
        "disagreements_ab": [{"row": int(a.at[i, "row"]), "A": x, "B": y, "llm": z}
                             for i, x, y, z in zip(idx, ca, cb, cl) if x != y],
        "human_consensus_differs_from_llm": [{"row": int(a.at[i, "row"]), "human": x, "llm": z}
                                             for i, x, y, z in zip(idx, ca, cb, cl) if x == y and x != z],
    }
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=2, default=float), encoding="utf-8")
    hh, hl = res["human_human"], res["human_vs_llm"]
    print(f"{len(idx)} câu. A vs B: đồng thuận {hh['agreement']:.1%}, kappa {hh['cohen_kappa']:.3f}")
    if hl["agreement"] is not None:
        print(f"Người (đồng thuận, {hl['n_human_consensus']} câu) vs LLM: {hl['agreement']:.1%}")
    print(f"A≠B: {len(res['disagreements_ab'])} câu, cần thảo luận chốt. Người≠LLM: {len(res['human_consensus_differs_from_llm'])} câu.")
    print(f"-> {OUT}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["make", "score"])
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    sys.exit(make(a.force) if a.cmd == "make" else score())
