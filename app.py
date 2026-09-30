"""Demo Streamlit: nhập câu hỏi -> nhóm quy định (ML) -> Điều luật liên quan (cosine similarity).

Chạy: streamlit run app.py   (cần models/best_classifier.joblib từ notebook)
"""
from __future__ import annotations

import time

import joblib
import numpy as np
import pandas as pd
import streamlit as st

from src.config import LABELS, MODELS_DIR
from src.preprocess import preprocess
from src.retrieval import ArticleRetriever

st.set_page_config(page_title="Tra cứu Luật ATVSLĐ", page_icon="⚖️", layout="wide")


@st.cache_resource
def load():
    return joblib.load(MODELS_DIR / "best_classifier.joblib"), ArticleRetriever()


def class_scores(model, text: str) -> np.ndarray:
    clf = model.named_steps["clf"]
    x = model.named_steps["tfidf"].transform([text])
    if hasattr(clf, "predict_proba"):
        return clf.predict_proba(x)[0]
    s = clf.decision_function(x)[0]  # LinearSVC: softmax trên decision score, chỉ để xếp hạng, không phải xác suất hiệu chỉnh
    e = np.exp(s - s.max())
    return e / e.sum()


model, retriever = load()
st.title("⚖️ Tra cứu Luật An toàn, vệ sinh lao động")
st.caption("Luật 84/2015/QH13 (VBHN 14/VBHN-VPQH 2024) · Phạm vi: Điều 1–62 · Đồ án CS114 Máy học UIT")

examples = [
    "Công ty phát tiền thay cho khẩu trang và găng tay bảo hộ có đúng luật không?",
    "Làm ca đêm trong môi trường độc hại thì được bồi dưỡng bằng hiện vật không?",
    "Bị tai nạn trên đường đi làm có được bảo hiểm trả trợ cấp không?",
    "Làm việc với nồi hơi thì có bắt buộc phải có thẻ an toàn không?",
    "Xảy ra tai nạn chết người ở công trường thì phải báo cho cơ quan nào?",
]
# Form: bấm "Tra cứu" gửi đúng nội dung đang có trong ô, kể cả khi chưa rời khỏi ô nhập
# (ngoài form, text_area chỉ nhận giá trị mới khi blur/Ctrl+Enter nên có thể tra câu cũ).
with st.form("query"):
    q = st.text_area("Nhập câu hỏi / tình huống", value=examples[0], height=90)
    st.write("Ví dụ:", " · ".join(f"`{e[:45]}…`" for e in examples[1:]))
    k = st.slider("Số Điều luật hiển thị", 1, 5, 3)
    submitted = st.form_submit_button("Tra cứu", type="primary")

if submitted and q.strip():
    t0 = time.perf_counter()
    clean = preprocess(q)
    probs = class_scores(model, clean)
    order = np.argsort(-probs)
    label = int(model.classes_[order[0]])
    hits = retriever.rank(clean, label, k)
    ms = (time.perf_counter() - t0) * 1000

    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("1. Nhóm quy định dự đoán")
        st.metric(f"C{label} · {LABELS[label][0]}", f"{probs[order[0]]:.0%}", help="Điểm tương đối giữa các lớp")
        st.write(LABELS[label][1])
        top = order[:4]
        st.bar_chart(pd.DataFrame({"Lớp": [f"C{int(model.classes_[i])} {LABELS[int(model.classes_[i])][0]}" for i in top],
                                   "Điểm": [float(probs[i]) for i in top]}),
                     x="Lớp", y="Điểm", horizontal=True, sort="-Điểm")
        if probs[order[0]] < 0.4:
            st.warning("Độ tin cậy thấp: câu hỏi có thể nằm ngoài phạm vi Đ1–62 hoặc hỏi nhiều ý.")
        st.caption(f"Tiền xử lý: `{clean}` · {ms:.0f} ms")
    with c2:
        st.subheader("2. Điều luật liên quan")
        for rank, (aid, sim) in enumerate(hits, 1):
            a = retriever.articles[aid]
            with st.expander(f"#{rank} · Điều {aid}. {a['title']}  (cosine = {sim:.3f})", expanded=rank == 1):
                if a.get("amended_2024"):
                    st.info("Điều này có khoản được sửa đổi bởi Luật BHXH 41/2024/QH15.")
                st.markdown("\n\n".join(a["paragraphs"]))
        st.caption("Mức xử phạt hành chính: chưa tích hợp (xem Hướng phát triển trong báo cáo).")
