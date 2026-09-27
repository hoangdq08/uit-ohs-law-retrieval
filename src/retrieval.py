"""Giai đoạn 2: xếp hạng Điều luật trong lớp dự đoán bằng cosine similarity TF-IDF.

Vectorizer của retrieval fit trên văn bản Điều luật (corpus cố định, không phải dữ liệu train),
nên không gây leakage giữa train/test câu hỏi.
"""
from __future__ import annotations

import json

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.config import ARTICLE_TO_LABEL, ARTICLES_PATH
from src.preprocess import preprocess


class ArticleRetriever:
    def __init__(self, articles: list[dict] | None = None):
        if articles is None:
            articles = json.loads(ARTICLES_PATH.read_text(encoding="utf-8"))["articles"]
        self.articles = {a["article_id"]: a for a in articles if a["article_id"] in ARTICLE_TO_LABEL}
        self.ids = sorted(self.articles)
        docs = [preprocess(f"{self.articles[i]['title']}. {self.articles[i]['title']}. {self.articles[i]['text']}")
                for i in self.ids]  # lặp tiêu đề 2 lần: tiêu đề mang nhiều tín hiệu nhất
        self.vec = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, token_pattern=r"(?u)\S+",
                                   lowercase=False)
        self.doc_matrix = self.vec.fit_transform(docs)
        self.label_of = np.array([ARTICLE_TO_LABEL[i] for i in self.ids])

    def rank(self, question_clean: str, label_id: int | None = None, k: int = 3) -> list[tuple[int, float]]:
        sims = cosine_similarity(self.vec.transform([question_clean]), self.doc_matrix).ravel()
        mask = np.ones_like(sims, dtype=bool) if label_id is None else self.label_of == label_id
        order = [j for j in np.argsort(-sims) if mask[j]][:k]
        return [(self.ids[j], float(sims[j])) for j in order]


def topk_accuracy(retriever: ArticleRetriever, questions, true_articles, labels, k: int) -> float:
    hits = [t in [a for a, _ in retriever.rank(q, l, k)] for q, t, l in zip(questions, true_articles, labels)]
    return float(np.mean(hits))
