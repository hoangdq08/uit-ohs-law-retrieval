"""Sinh slide thuyết trình (~12 trang) từ reports/results.json + figures.

Chạy sau notebook: python -m scripts.build_slides
"""
from __future__ import annotations

import json

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

from src.config import FIGURES_DIR, LABELS, ROOT

RESULTS = ROOT / "reports" / "results.json"
OUT = ROOT / "reports" / "Slide_BaoCao_DoAn.pptx"
NAVY = RGBColor(0x1A, 0x36, 0x5D)
ACCENT = RGBColor(0xDD, 0x6B, 0x20)
GREY = RGBColor(0x4A, 0x55, 0x68)
MODEL_VI = {"MultinomialNB": "Naive Bayes", "LogisticRegression": "Logistic Reg.", "LinearSVC": "LinearSVC",
            "RandomForest": "Random Forest"}


def pct(x) -> str:
    return "–" if x is None else f"{100 * float(x):.1f}%"


class Deck:
    def __init__(self):
        self.prs = Presentation()
        self.prs.slide_width, self.prs.slide_height = Inches(13.333), Inches(7.5)
        self.blank = self.prs.slide_layouts[6]

    def slide(self, title: str, subtitle: str | None = None):
        s = self.prs.slides.add_slide(self.blank)
        bar = s.shapes.add_shape(1, 0, 0, self.prs.slide_width, Inches(0.12))
        bar.fill.solid(); bar.fill.fore_color.rgb = ACCENT; bar.line.fill.background()
        tb = s.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12), Inches(0.9)).text_frame
        tb.text = title
        r = tb.paragraphs[0].runs[0]; r.font.size = Pt(30); r.font.bold = True; r.font.color.rgb = NAVY
        if subtitle:
            p = tb.add_paragraph(); p.text = subtitle
            p.runs[0].font.size = Pt(15); p.runs[0].font.color.rgb = GREY
        return s

    def bullets(self, s, items, left=0.7, top=1.6, width=12, size=19):
        tf = s.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(5.5)).text_frame
        tf.word_wrap = True
        for i, it in enumerate(items):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            sub = it.startswith("  ")
            p.text = ("– " if sub else "• ") + it.strip()
            p.level = 1 if sub else 0
            p.space_after = Pt(8)
            for r in p.runs:
                r.font.size = Pt(size - 3 if sub else size); r.font.color.rgb = GREY if sub else RGBColor(0x1A, 0x20, 0x2C)

    def image(self, s, name, left, top, width=None, height=None):
        path = FIGURES_DIR / f"{name}.png"
        if path.exists():
            s.shapes.add_picture(str(path), Inches(left), Inches(top),
                                 width=Inches(width) if width else None, height=Inches(height) if height else None)

    def table(self, s, header, rows, left, top, width, row_h=0.42, size=13):
        t = s.shapes.add_table(len(rows) + 1, len(header), Inches(left), Inches(top), Inches(width),
                               Inches(row_h * (len(rows) + 1))).table
        for j, h in enumerate(header):
            c = t.cell(0, j); c.text = str(h)
            c.text_frame.paragraphs[0].runs[0].font.size = Pt(size); c.text_frame.paragraphs[0].runs[0].font.bold = True
        for i, row in enumerate(rows, 1):
            for j, v in enumerate(row):
                c = t.cell(i, j); c.text = str(v)
                c.text_frame.paragraphs[0].runs[0].font.size = Pt(size)

    def save(self):
        self.prs.save(OUT)


def main() -> None:
    R = json.loads(RESULTS.read_text(encoding="utf-8"))
    M, best = R["models"], R["best_model"]
    has_real = R.get("n_real", 0) > 0
    d = Deck()

    s = d.slide("Tra cứu Luật An toàn, vệ sinh lao động bằng NLP tiếng Việt",
                "Đồ án môn Máy học · GVHD: Thầy Cáp Phạm Đình Thăng · Nhóm: <tên thành viên>")
    d.bullets(s, ["Bài toán: câu hỏi đời thường → nhóm quy định → Điều luật cụ thể",
                  "Luật 84/2015/QH13, văn bản hợp nhất 14/VBHN-VPQH (2024), phạm vi Điều 1–62",
                  "Cốt lõi Machine Learning: phân loại văn bản 8 lớp, so sánh 4 mô hình"], top=2.4, size=22)

    s = d.slide("Bối cảnh & kiến trúc hai giai đoạn")
    d.bullets(s, ["Người lao động hỏi bằng ngôn ngữ đời thường, không nhớ số Điều, Khoản",
                  "Tìm kiếm từ khóa chính xác: dễ không ra kết quả hoặc ra quá nhiều",
                  "Giai đoạn 1 (ML): TF-IDF + bộ phân loại → 1 trong 8 nhóm quy định",
                  "Giai đoạn 2 (IR): cosine similarity giữa câu hỏi và các Điều trong nhóm → Top-k Điều luật",
                  "Không dùng LLM/API bên ngoài để trả lời: toàn bộ là mô hình học máy truyền thống"])

    s = d.slide("Hệ thống 8 lớp nhãn", "Mỗi Điều thuộc đúng 1 lớp; nhãn câu hỏi suy ra từ Điều trả lời trực tiếp")
    d.table(s, ["Lớp", "Mã", "Nội dung", "Số Điều"],
            [[f"C{k}", v[0], v[1], len(v[2])] for k, v in LABELS.items()], 0.6, 1.7, 12.1, size=13)

    s = d.slide("Dữ liệu", f"{R['n_samples']} câu hỏi · {R['n_seeds']} câu gốc × 5 văn phong"
                + (f" · {R['n_real']} câu hỏi thật" if has_real else ""))
    sz = R["split_sizes"]
    d.bullets(s, [f"Synthetic có kiểm soát: 40 câu gốc/lớp viết từ nội dung Điều luật, 5 văn phong (trung tính, công nhân, HSE, khiếu nại, rút gọn)",
                  "Cân bằng lớp: 200 mẫu mỗi lớp",
                  f"Chia theo nhóm câu gốc (StratifiedGroupKFold): train {sz.get('train')} · val {sz.get('val')} · test {sz.get('test')}",
                  "  Mọi paraphrase của một câu gốc nằm cùng 1 tập → không rò rỉ",
                  ] + ([f"Test thật: {R['n_real']} câu của người dân trên chinhsachonline.chinhphu.vn, nhãn theo Điều mà Bộ trả lời viện dẫn"] if has_real else []),
              width=6.3, size=17)
    d.image(s, "eda_class_distribution", 7.0, 1.7, width=6.0)

    s = d.slide("EDA & tiền xử lý")
    d.image(s, "eda_wordcloud", 0.4, 1.4, width=7.6)
    d.bullets(s, ["NFC, chữ thường, bỏ URL/ký tự đặc biệt",
                  "Tách từ underthesea: bảo hộ lao động → bảo_hộ_lao_động",
                  "Lọc stopwords, giữ từ phủ định (không, chưa, cấm, được)",
                  "TF-IDF (1,2)-gram, sublinear_tf, min_df=2",
                  "Vectorizer nằm trong Pipeline: fit chỉ trên train"], left=8.2, width=4.9, size=16)

    s = d.slide("So sánh 4 mô hình", "GridSearchCV + StratifiedGroupKFold(5), tối ưu Macro-F1; chọn theo validation")
    hdr = ["Mô hình", "CV F1", "Train F1", "Val F1", "Test F1"] + (["Thật F1"] if has_real else [])
    d.table(s, hdr, [[MODEL_VI[m], pct(x["cv_macro_f1"]), pct(x["train_macro_f1"]), pct(x["val_macro_f1"]),
                      pct(x["test_macro_f1"])] + ([pct(x.get("real_macro_f1"))] if has_real else []) for m, x in M.items()],
            0.6, 1.8, 7.0, size=14)
    d.image(s, "model_comparison", 7.8, 1.8, width=5.3)
    tb = s.shapes.add_textbox(Inches(0.6), Inches(4.4), Inches(7), Inches(1)).text_frame
    tb.text = f"Tốt nhất: {MODEL_VI[best]} (val Macro-F1 {pct(M[best]['val_macro_f1'])})"
    tb.paragraphs[0].runs[0].font.size = Pt(22); tb.paragraphs[0].runs[0].font.bold = True
    tb.paragraphs[0].runs[0].font.color.rgb = ACCENT

    s = d.slide("Ma trận nhầm lẫn", f"{MODEL_VI[best]} · test synthetic" + (" và câu hỏi thật" if has_real else ""))
    d.image(s, "confusion_matrix", 0.5, 1.5, width=12.3)

    s = d.slide("Ablation study", f"{MODEL_VI[best]} · mỗi cặp chỉ khác 1 yếu tố")
    ab = R["ablation"]
    d.table(s, ["Cấu hình", "CV F1 ± std", "Test F1"] + (["Thật F1"] if has_real else []),
            [[k, f"{pct(v['cv_f1_mean'])} ± {100 * v['cv_f1_std']:.1f}", pct(v["test_f1"])]
             + ([pct(v.get("real_f1"))] if has_real else []) for k, v in ab.items()], 0.5, 1.7, 8.2, size=13)
    d.image(s, "ablation", 8.9, 1.7, width=4.2)

    s = d.slide("Phân tích lỗi")
    tc = list(R["top_confusions"].items())[:4]
    d.bullets(s, ["Cặp hay nhầm nhất (4 mô hình, test):"] + [f"  {k}: {v} lần" for k, v in tc]
              + ["Accuracy theo văn phong: " + ", ".join(f"{k} {pct(v)}" for k, v in R["acc_by_style"].items())]
              + ([f"Câu hỏi thật dài ~{R.get('real_len_mean', 0):.0f} âm tiết, nhiều bối cảnh và dẫn chiếu Nghị định → domain shift"] if has_real else []),
              width=7.2, size=17)
    d.image(s, "acc_by_style", 7.9, 1.8, width=5.1)

    s = d.slide("Tra cứu Điều luật (giai đoạn 2)")
    ret = R["retrieval"]
    cols = list(ret)
    d.table(s, ["Chỉ số"] + cols, [[k] + [pct(ret[c][k]) for c in cols] for k in ret[cols[0]]], 0.6, 1.6, 7.5, size=13)
    d.bullets(s, ["Oracle: biết đúng lớp → đo riêng retrieval", "End-to-end: dùng lớp dự đoán",
                  "No-filter: tìm trên cả 62 Điều (baseline)", "Demo: streamlit run app.py"], left=8.4, width=4.6, size=16)

    s = d.slide("Kết luận & hướng phát triển")
    d.bullets(s, [f"Pipeline hoàn chỉnh: corpus 93 Điều (2024) → {R['n_samples']} câu hỏi → 4 mô hình → ablation → tra cứu → demo",
                  f"{MODEL_VI[best]} tốt nhất; chia theo nhóm câu gốc để số liệu không bị thổi phồng",
                  "Hạn chế: dữ liệu huấn luyện synthetic, test thật nhỏ, chưa xử lý câu nhiều ý / ngoài phạm vi, chưa có mức phạt",
                  "Hướng phát triển: thêm dữ liệu thật + kappa, multi-label, Đ63–93 và Nghị định, NĐ 12/2022 mức phạt, PhoBERT"])

    s = d.slide("Cảm ơn thầy và các bạn đã lắng nghe", "Hỏi & đáp")
    d.save()
    print(f"-> {OUT} ({len(d.prs.slides)} slides)")


if __name__ == "__main__":
    main()
