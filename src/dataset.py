"""Nạp dataset + chia Train/Val/Test theo nhóm seed_id (chống leakage do paraphrase).

Chạy: python -m src.dataset  (build data/processed/ohs_questions.csv + in thống kê split)
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

from src.config import (ARTICLE_TO_LABEL, CLEAN_QUESTIONS_PATH, LABEL_CODES, PROCESSED_DIR,
                        RANDOM_STATE, RAW_DIR)

GEN_DIR = RAW_DIR / "gen"
DATASET_PATH = PROCESSED_DIR / "ohs_questions.csv"
REAL_TEST_PATH = PROCESSED_DIR / "real_test.csv"


def load_generated() -> pd.DataFrame:
    rows = []
    for f in sorted(GEN_DIR.glob("c[0-7].jsonl")):
        rows += [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
    df = pd.DataFrame(rows)
    df["label_id"] = df["article_id"].map(ARTICLE_TO_LABEL)  # nhãn suy ra từ Điều, không gán tay
    assert df["label_id"].notna().all(), "article_id ngoài phạm vi Đ1-62"
    df["label_id"] = df["label_id"].astype(int)
    df["label_code"] = df["label_id"].map(LABEL_CODES)
    df["source"] = "synthetic"
    df.insert(0, "id", range(len(df)))
    return df


def group_split(df: pd.DataFrame, test_frac: float = 0.15, val_frac: float = 0.15) -> pd.Series:
    """Gán 'train'/'val'/'test' sao cho mọi câu cùng seed_id nằm chung 1 tập, giữ tỷ lệ lớp.

    Dùng StratifiedGroupKFold: tách test = 1 fold trong ~1/test_frac folds, rồi tách val từ phần còn lại.
    """
    split = pd.Series("train", index=df.index)
    y, g = df["label_id"].to_numpy(), df["seed_id"].to_numpy()

    n_test = round(1 / test_frac)
    sgkf = StratifiedGroupKFold(n_splits=n_test, shuffle=True, random_state=RANDOM_STATE)
    rest_idx, test_idx = next(sgkf.split(df, y, g))
    split.iloc[test_idx] = "test"

    n_val = round((1 - test_frac) / val_frac)
    sgkf2 = StratifiedGroupKFold(n_splits=n_val, shuffle=True, random_state=RANDOM_STATE)
    tr_rel, val_rel = next(sgkf2.split(rest_idx, y[rest_idx], g[rest_idx]))
    split.iloc[rest_idx[val_rel]] = "val"

    # Bất biến chống leakage: không seed nào xuất hiện ở 2 tập.
    seeds = {s: set(df.loc[split == s, "seed_id"]) for s in ("train", "val", "test")}
    assert not (seeds["train"] & seeds["val"] or seeds["train"] & seeds["test"] or seeds["val"] & seeds["test"])
    return split


def load_dataset() -> pd.DataFrame:
    return pd.read_csv(DATASET_PATH)


def load_real_test() -> pd.DataFrame | None:
    return pd.read_csv(REAL_TEST_PATH) if REAL_TEST_PATH.exists() else None


if __name__ == "__main__":
    from src.preprocess import preprocess

    df = load_generated()
    df["split"] = group_split(df)
    df["question_clean"] = df["question"].map(preprocess)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATASET_PATH, index=False)
    df.to_csv(CLEAN_QUESTIONS_PATH, index=False)
    print(df.groupby(["split"]).size().to_string())
    print(pd.crosstab(df["label_code"], df["split"]).to_string())
    print(pd.crosstab(df["label_code"], df["split"], normalize="columns").round(3).to_string())
