"""Định nghĩa 4 mô hình + lưới siêu tham số + hàm train/eval dùng chung cho notebook.

TF-IDF nằm TRONG Pipeline, nên GridSearchCV fit lại vectorizer trong từng fold (không leakage),
và khi đánh giá val/test chỉ gọi transform.
"""
from __future__ import annotations

import time

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import GridSearchCV, StratifiedGroupKFold
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from src.config import RANDOM_STATE


def tfidf(ngram=(1, 2)) -> TfidfVectorizer:
    # token_pattern mặc định bỏ token 1 ký tự; giữ mọi chuỗi không trắng để không mất âm tiết/từ ghép "_".
    return TfidfVectorizer(ngram_range=ngram, sublinear_tf=True, min_df=2, max_features=5000,
                           token_pattern=r"(?u)\S+", lowercase=False)


def build_models() -> dict[str, tuple[Pipeline, dict]]:
    return {
        "MultinomialNB": (
            Pipeline([("tfidf", tfidf()), ("clf", MultinomialNB())]),
            {"clf__alpha": [0.01, 0.05, 0.1, 0.5, 1.0]},
        ),
        "LogisticRegression": (
            Pipeline([("tfidf", tfidf()), ("clf", LogisticRegression(max_iter=3000, random_state=RANDOM_STATE))]),
            {"clf__C": [0.1, 1.0, 10.0, 100.0], "clf__class_weight": [None, "balanced"]},
        ),
        "LinearSVC": (
            Pipeline([("tfidf", tfidf()), ("clf", LinearSVC(random_state=RANDOM_STATE))]),
            {"clf__C": [0.01, 0.1, 1.0, 10.0], "clf__loss": ["hinge", "squared_hinge"],
             "clf__class_weight": [None, "balanced"]},
        ),
        "RandomForest": (
            Pipeline([("tfidf", tfidf()), ("clf", RandomForestClassifier(random_state=RANDOM_STATE, n_jobs=-1))]),
            {"clf__n_estimators": [200, 400], "clf__max_depth": [None, 50], "clf__min_samples_leaf": [1, 2]},
        ),
    }


def grid_search(pipe: Pipeline, grid: dict, X, y, groups) -> GridSearchCV:
    cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    gs = GridSearchCV(pipe, grid, scoring="f1_macro", cv=cv, n_jobs=-1, refit=True, return_train_score=True)
    gs.fit(X, y, groups=groups)
    return gs


def scores(y_true, y_pred) -> dict:
    p, r, f, _ = precision_recall_fscore_support(y_true, y_pred, average="macro", zero_division=0)
    return {"accuracy": accuracy_score(y_true, y_pred), "macro_precision": p, "macro_recall": r, "macro_f1": f}


def fit_eval(name: str, pipe: Pipeline, grid: dict, tr: pd.DataFrame, evals: dict[str, pd.DataFrame],
             text_col: str = "question_clean") -> tuple[GridSearchCV, dict]:
    t0 = time.perf_counter()
    gs = grid_search(pipe, grid, tr[text_col], tr["label_id"], tr["seed_id"])
    fit_s = time.perf_counter() - t0
    row = {"model": name, "best_params": gs.best_params_, "cv_macro_f1": gs.best_score_,
           "fit_seconds": round(fit_s, 1)}
    for split_name, d in {"train": tr, **evals}.items():
        pred = gs.predict(d[text_col])
        row.update({f"{split_name}_{k}": v for k, v in scores(d["label_id"], pred).items()})
    return gs, row
