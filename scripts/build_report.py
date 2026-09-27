"""Sinh báo cáo Word (10 mục theo docs/course-requirements.md) từ reports/results.json + figures.

Chạy sau notebook: python -m scripts.build_report
Mọi con số lấy từ results.json. Phần nhận xét được viết theo điều kiện trên số liệu (không hard-code kết quả).
Nhóm cần đọc lại, sửa giọng văn và bổ sung thông tin nhóm (tên, MSSV) trước khi nộp.
"""
from __future__ import annotations

import json

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

from src.config import FIGURES_DIR, LABELS, ROOT

RESULTS = ROOT / "reports" / "results.json"
OUT = ROOT / "reports" / "BaoCao_DoAn_MayHoc.docx"
MODEL_VI = {"MultinomialNB": "Multinomial Naive Bayes", "LogisticRegression": "Logistic Regression",
            "LinearSVC": "Linear SVM (LinearSVC)", "RandomForest": "Random Forest"}


def pct(x) -> str:
    return "–" if x is None else f"{100 * float(x):.2f}%"


class Report:
    def __init__(self):
        self.d = Document()
        st = self.d.styles["Normal"]
        st.font.name = "Times New Roman"
        st.font.size = Pt(13)
        st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
        for s in self.d.sections:
            s.left_margin, s.right_margin, s.top_margin, s.bottom_margin = Cm(3), Cm(2), Cm(2), Cm(2)
        self.fig_no = 0
        self.tab_no = 0

    def h(self, text, level=1):
        p = self.d.add_heading(text, level=level)
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
        return p

    def p(self, text, bold=False, italic=False, align=None):
        par = self.d.add_paragraph()
        r = par.add_run(text)
        r.bold, r.italic = bold, italic
        par.paragraph_format.space_after = Pt(6)
        par.paragraph_format.line_spacing = 1.3
        if align:
            par.alignment = align
        return par

    def bullets(self, items):
        for it in items:
            par = self.d.add_paragraph(style="List Bullet")
            par.add_run(it)

    def table(self, header, rows, caption):
        self.tab_no += 1
        self.p(f"Bảng {self.tab_no}. {caption}", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        t = self.d.add_table(rows=1, cols=len(header))
        t.style = "Light Grid Accent 1"
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        for i, c in enumerate(header):
            t.rows[0].cells[i].text = str(c)
            for r in t.rows[0].cells[i].paragraphs[0].runs:
                r.bold = True
                r.font.size = Pt(11)
        for row in rows:
            cells = t.add_row().cells
            for i, c in enumerate(row):
                cells[i].text = str(c)
                for r in cells[i].paragraphs[0].runs:
                    r.font.size = Pt(11)
        self.d.add_paragraph()

    def fig(self, name, caption, width=15):
        path = FIGURES_DIR / f"{name}.png"
        if not path.exists():
            self.p(f"[Thiếu hình {name}.png]", italic=True)
            return
        self.fig_no += 1
        self.d.add_picture(str(path), width=Cm(width))
        self.d.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        self.p(f"Hình {self.fig_no}. {caption}", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    def code(self, text):
        par = self.d.add_paragraph()
        r = par.add_run(text)
        r.font.name = "Consolas"
        r.font.size = Pt(9)

    def save(self):
        self.d.save(OUT)


def main() -> None:
    R = json.loads(RESULTS.read_text(encoding="utf-8"))
    M = R["models"]
    best = R["best_model"]
    has_real = R.get("n_real", 0) > 0
    rank = sorted(M, key=lambda m: -M[m]["val_macro_f1"])
    second = rank[1]
    abl = R["ablation"]
    keys = list(abl)
    full, noseg, uni, nosw = keys[0], keys[1], keys[2], keys[3]
    rp = Report()

    # Trang bìa
    for line, size, bold in [("ĐẠI HỌC QUỐC GIA TP. HỒ CHÍ MINH", 13, True),
                             ("TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN", 13, True), ("", 13, False),
                             ("ĐỒ ÁN MÔN HỌC MÁY HỌC", 16, True), ("", 13, False),
                             ("XÂY DỰNG HỆ THỐNG XỬ LÝ NGÔN NGỮ TỰ NHIÊN TRA CỨU", 18, True),
                             ("LUẬT AN TOÀN, VỆ SINH LAO ĐỘNG", 18, True), ("", 13, False),
                             ("Giảng viên hướng dẫn: Thầy Cáp Phạm Đình Thăng", 13, False),
                             ("Nhóm thực hiện: <Họ tên – MSSV>", 13, False),
                             ("<Họ tên – MSSV>", 13, False), ("<Họ tên – MSSV>", 13, False)]:
        par = rp.d.add_paragraph()
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = par.add_run(line)
        r.bold, r.font.size = bold, Pt(size)
    rp.d.add_page_break()

    # 1
    rp.h("1. Tóm tắt đề tài")
    rp.p(f"Đề tài xây dựng hệ thống tra cứu Luật An toàn, vệ sinh lao động (Luật 84/2015/QH13, văn bản hợp nhất "
         f"14/VBHN-VPQH năm 2024) từ câu hỏi tiếng Việt tự nhiên. Hệ thống gồm hai giai đoạn: (1) mô hình Machine "
         f"Learning phân loại câu hỏi vào 8 nhóm quy định (Điều 1–62); (2) module truy vấn xếp hạng Điều luật cụ thể "
         f"trong nhóm dự đoán bằng độ tương đồng cosine trên TF-IDF.")
    rp.p(f"Bộ dữ liệu gồm {R['n_samples']} câu hỏi ({R['n_seeds']} câu gốc × 5 văn phong) được sinh có kiểm soát từ "
         f"nội dung từng Điều luật, chia Train/Val/Test theo nhóm câu gốc để tránh rò rỉ dữ liệu"
         + (f", cùng {R['n_real']} câu hỏi thật của người dân từ Cổng Hỏi đáp chính sách Chính phủ làm tập kiểm tra độc lập." if has_real else "."))
    rp.p(f"Bốn mô hình được so sánh: Multinomial Naive Bayes, Logistic Regression, LinearSVC và Random Forest, tinh "
         f"chỉnh bằng GridSearchCV với StratifiedGroupKFold. Mô hình tốt nhất theo Macro-F1 trên tập validation là "
         f"{MODEL_VI[best]} (val Macro-F1 = {pct(M[best]['val_macro_f1'])}, test Macro-F1 = {pct(M[best]['test_macro_f1'])}"
         + (f", câu hỏi thật Macro-F1 = {pct(M[best]['real_macro_f1'])}" if has_real else "") + ").")

    # 2
    rp.h("2. Giới thiệu bài toán và bộ dữ liệu")
    rp.h("2.1. Bài toán", 2)
    rp.p("Người lao động và cán bộ nhân sự thường hỏi về an toàn lao động bằng ngôn ngữ đời thường, không nhớ số Điều, "
         "Khoản. Tìm kiếm theo từ khóa chính xác dễ trả về kết quả không liên quan. Đề tài mô hình hóa việc tra cứu "
         "thành bài toán học có giám sát: phân loại văn bản đa lớp (K = 8), đầu vào là câu hỏi, đầu ra là nhóm quy định; "
         "sau đó truy vấn Điều luật trong nhóm.")
    rp.h("2.2. Hệ thống nhãn", 2)
    rp.p("Nhãn được thiết kế theo cấu trúc Chương/Mục của Luật, mỗi Điều thuộc đúng một lớp. Người tạo dữ liệu chỉ "
         "chọn Điều luật trả lời trực tiếp câu hỏi; nhãn lớp được suy ra tự động từ Điều, bảo đảm nhãn và Điều đích luôn "
         "nhất quán (chi tiết: docs/labeling-guidelines.md).")
    rp.table(["Lớp", "Mã", "Nội dung", "Điều"],
             [[f"C{k}", v[0], v[1], f"{min(v[2])}–{max(v[2])}" if len(v[2]) > 1 and v[2] == list(range(min(v[2]), max(v[2]) + 1))
               else ", ".join(map(str, v[2]))] for k, v in LABELS.items()], "Tám lớp nhãn và phạm vi Điều luật")
    rp.h("2.3. Bộ dữ liệu", 2)
    rp.p(f"Tổng số mẫu: {R['n_samples']}; số lớp: 8; số câu gốc: {R['n_seeds']} (40 câu gốc mỗi lớp). Mỗi câu gốc có "
         f"5 biến thể: trung tính, văn phong công nhân, văn phong nhân sự/HSE, khiếu nại và dạng rút gọn. Các lớp có số "
         f"mẫu bằng nhau nên không mất cân bằng lớp; tuy nhiên số Điều mỗi lớp rất khác nhau (C2, C6: 1 Điều; C7: 22 Điều).")
    rp.table(["Lớp", "Số mẫu", "Số câu gốc", "Số Điều có câu hỏi", "Tỷ lệ"],
             [[r["label_code"], r["so_mau"], r["so_seed"], r["so_dieu"], f"{r['ty_le_%']}%"] for r in R["class_dist"]],
             "Phân bố mẫu theo lớp")
    rp.p("Dữ liệu được chia Train/Validation/Test ≈ 70/15/15 bằng StratifiedGroupKFold với nhóm là câu gốc: mọi biến thể "
         "của cùng một câu gốc nằm trong cùng một tập. Nếu chia ngẫu nhiên, các câu paraphrase gần giống nhau sẽ xuất hiện "
         "ở cả train và test, làm kết quả bị thổi phồng. Notebook kiểm tra giao các nhóm giữa ba tập bằng rỗng.")
    rows = [[r["label_code"], r["train"], r["val"], r["test"]] for r in R["split_table"]]
    rp.table(["Lớp", "Train", "Val", "Test"], rows, "Số mẫu mỗi lớp trên từng tập")
    if has_real:
        rp.p(f"Tập test thật gồm {R['n_real']} câu hỏi thực tế từ chinhsachonline.chinhphu.vn, nhãn lấy theo Điều của "
             f"Luật ATVSLĐ mà cơ quan nhà nước viện dẫn trong câu trả lời. Tập này không được dùng khi huấn luyện hay "
             f"chọn mô hình. Phân bố lớp của tập này không đều (phản ánh nhu cầu hỏi thực tế).")

    # 3
    rp.h("3. Phân tích khám phá dữ liệu (EDA)")
    rp.fig("eda_class_distribution", "Số mẫu và số Điều luật mỗi lớp")
    ls = R["len_stats"]
    rp.p(f"Độ dài câu hỏi trung bình {ls['mean']} âm tiết (min {ls['min']}, max {ls['max']}). Văn phong rút gọn ngắn nhất "
         f"({R['len_by_style'].get('short')}), văn phong khiếu nại dài nhất ({R['len_by_style'].get('complaint')})."
         + (f" Câu hỏi thật có độ dài trung bình {R.get('real_len_mean', 0):.1f} âm tiết"
            + (", dài hơn nhiều so với dữ liệu synthetic, thường kèm bối cảnh cụ thể." if R.get('real_len_mean', 0) > 1.5 * ls['mean'] else ".")
            if has_real else ""))
    rp.fig("eda_length", "Phân bố độ dài câu hỏi")
    rp.fig("eda_wordcloud", "WordCloud theo lớp (sau tách từ và lọc stopwords)", 16)
    rp.table(["Lớp", "Từ đặc trưng (TF-IDF trung bình)"], [[k, v] for k, v in R["top_terms"].items()],
             "Các từ đặc trưng nhất mỗi lớp trên tập train")

    # 4
    rp.h("4. Tiền xử lý dữ liệu")
    rp.bullets(["Chuẩn hóa Unicode NFC, chuyển chữ thường, loại URL, email, thẻ HTML, ký tự đặc biệt.",
                "Tách từ tiếng Việt bằng underthesea.word_tokenize: ghép các âm tiết thành từ (vd “bảo hộ lao động” → bảo_hộ_lao_động).",
                "Lọc stopwords tiếng Việt, cố ý giữ các từ phủ định/điều kiện (không, chưa, cấm, được, phải, nếu) vì chúng đảo nghĩa câu hỏi pháp lý.",
                "Trích đặc trưng TF-IDF (1,2)-gram, sublinear_tf, min_df = 2, max_features = 5000.",
                "Chống rò rỉ dữ liệu: TfidfVectorizer nằm trong sklearn Pipeline nên chỉ được fit trên dữ liệu huấn luyện của từng fold; val/test chỉ transform."])
    rp.table(["Câu gốc", "Sau tiền xử lý"], [[e["question"], e["full (tách từ + stopwords)"]] for e in R["preprocess_examples"]],
             "Ví dụ tiền xử lý")

    # 5
    rp.h("5. Mô hình và thông số")
    rp.bullets(["Multinomial Naive Bayes: mô hình xác suất với giả định độc lập có điều kiện giữa các từ; baseline nhanh cho phân loại văn bản.",
                "Logistic Regression: hàm softmax với hàm mất mát cross-entropy, điều chuẩn L2 (tham số C).",
                "LinearSVC: tìm siêu phẳng lề cực đại, hàm mất mát hinge / squared hinge; phù hợp dữ liệu thưa nhiều chiều như TF-IDF.",
                "Random Forest: tập hợp cây quyết định huấn luyện bằng bagging và chọn đặc trưng ngẫu nhiên; cho biết độ quan trọng đặc trưng."])
    rp.p("Siêu tham số được chọn bằng GridSearchCV, 5-fold StratifiedGroupKFold trên tập train (nhóm theo câu gốc), tiêu chí Macro-F1.")
    rp.table(["Mô hình", "Siêu tham số tốt nhất", "CV Macro-F1", "Thời gian (s)"],
             [[MODEL_VI[m], ", ".join(f"{k.replace('clf__', '')}={v}" for k, v in M[m]["best_params"].items()),
               pct(M[m]["cv_macro_f1"]), M[m]["fit_seconds"]] for m in M], "Siêu tham số sau tinh chỉnh")

    # 6
    rp.h("6. Kết quả và phân tích")
    hdr = ["Mô hình", "Val Acc", "Val P", "Val R", "Val F1", "Test Acc", "Test F1"] + (["Thật Acc", "Thật F1"] if has_real else [])
    rows = []
    for m in M:
        x = M[m]
        rows.append([MODEL_VI[m], pct(x["val_accuracy"]), pct(x["val_macro_precision"]), pct(x["val_macro_recall"]),
                     pct(x["val_macro_f1"]), pct(x["test_accuracy"]), pct(x["test_macro_f1"])]
                    + ([pct(x.get("real_accuracy")), pct(x.get("real_macro_f1"))] if has_real else []))
    rp.table(hdr, rows, "So sánh hiệu suất (Macro-average)")
    rp.fig("model_comparison", "Macro-F1 theo mô hình và tập dữ liệu")
    diff = M[best]["val_macro_f1"] - M[second]["val_macro_f1"]
    rp.p(f"Mô hình tốt nhất là {MODEL_VI[best]}, hơn mô hình đứng thứ hai ({MODEL_VI[second]}) {100 * diff:.2f} điểm "
         f"phần trăm Macro-F1 trên validation. Thứ hạng theo val Macro-F1: " + " > ".join(MODEL_VI[m] for m in rank) + ".")
    pc = R["per_class_test"]
    worst = sorted(pc, key=lambda c: pc[c]["f1-score"])[:2]
    rp.table(["Lớp", "Precision", "Recall", "F1", "Số mẫu"],
             [[c, pct(v["precision"]), pct(v["recall"]), pct(v["f1-score"]), int(v["support"])] for c, v in pc.items()],
             f"Chỉ số từng lớp của {MODEL_VI[best]} trên test")
    rp.p(f"Hai lớp có F1 thấp nhất trên test là {worst[0]} ({pct(pc[worst[0]]['f1-score'])}) và {worst[1]} "
         f"({pct(pc[worst[1]]['f1-score'])}). Macro-F1 được dùng làm chỉ số chính vì tính trung bình đều giữa các lớp, "
         f"không để lớp lớn lấn át (quan trọng với tập test thật có phân bố lệch).")
    rp.fig("confusion_matrix", f"Ma trận nhầm lẫn của {MODEL_VI[best]}", 16)
    tc = R["top_confusions"]
    rp.p("Các cặp nhầm lẫn nhiều nhất (cộng dồn 4 mô hình, test synthetic): "
         + "; ".join(f"{k} ({v} lần)" for k, v in list(tc.items())[:5]) + ".")
    gap = R["train_val_gap"]
    rp.h("Overfitting / underfitting", 3)
    rp.table(["Mô hình", "Train F1", "Val F1", "Chênh lệch"],
             [[MODEL_VI[m], pct(M[m]["train_macro_f1"]), pct(M[m]["val_macro_f1"]), pct(gap[m])] for m in M],
             "So sánh Train và Validation")
    over = [MODEL_VI[m] for m in M if gap[m] > 0.1]
    rp.p(("Các mô hình có chênh lệch train–val trên 10 điểm: " + ", ".join(over) + ", cho thấy dấu hiệu overfitting "
          "(mô hình nhớ từ vựng của tập train). ") if over else "Không mô hình nào có chênh lệch train–val trên 10 điểm. ")
    if has_real:
        drop = M[best]["test_macro_f1"] - M[best]["real_macro_f1"]
        if drop > 0.05:
            rp.p(f"Khoảng cách quan trọng nhất là giữa test synthetic và câu hỏi thật: Macro-F1 của {MODEL_VI[best]} giảm "
                 f"{100 * drop:.2f} điểm. Giả thuyết: domain shift (câu hỏi thật dài hơn, nhiều bối cảnh, dùng từ ngữ của "
                 f"Nghị định/Thông tư, phân bố lớp khác). Lưu ý tập thật chỉ có {R['n_real']} câu nên số liệu dao động lớn.")
        else:
            rp.p(f"Macro-F1 trên câu hỏi thật chênh {100 * drop:+.2f} điểm so với test synthetic; tập thật chỉ có "
                 f"{R['n_real']} câu nên chưa đủ để kết luận về khả năng tổng quát.")
    rp.fig("rf_feature_importance", "Top-20 đặc trưng quan trọng của Random Forest", 12)

    # 7
    rp.h("7. So sánh mô hình, Ablation study và phân tích lỗi")
    rp.h("7.1. Vì sao mô hình này tốt hơn", 2)
    linear_top = best in ("LinearSVC", "LogisticRegression")
    rp.p(("Kết quả phù hợp với nhận định thường gặp: với TF-IDF (thưa, hàng nghìn chiều, ít mẫu), mô hình tuyến tính "
          "(LinearSVC, Logistic Regression) có lợi thế vì mỗi từ khóa đóng góp tuyến tính vào quyết định và điều chuẩn giúp "
          "tổng quát hóa. ") if linear_top else
         (f"Khác với nhận định thường gặp (mô hình tuyến tính mạnh trên TF-IDF), {MODEL_VI[best]} tốt nhất trên dữ liệu này; "
          "nhóm cần phân tích thêm nguyên nhân. "))
    rp.p("Naive Bayes giả định các từ độc lập có điều kiện, không mô hình hóa tương quan giữa các bigram. Random Forest chia "
         "nhánh trên từng đặc trưng thưa, khó tận dụng hàng nghìn từ hiếm và dễ khớp quá mức tập train "
         f"(chênh lệch train–val của RF: {pct(R['train_val_gap'].get('RandomForest'))}).")
    rp.p("Kết quả thực nghiệm: " + ", ".join(f"{MODEL_VI[m]} {pct(M[m]['val_macro_f1'])}" for m in rank) + " (val Macro-F1).")
    rp.h("7.2. Ablation study", 2)
    rp.table(["Cấu hình", "CV F1 (± std)", "Val F1", "Test F1"] + (["Thật F1"] if has_real else []) + ["Số đặc trưng"],
             [[k, f"{pct(v['cv_f1_mean'])} ± {100 * v['cv_f1_std']:.2f}", pct(v["val_f1"]), pct(v["test_f1"])]
              + ([pct(v.get("real_f1"))] if has_real else []) + [v["n_features"]] for k, v in abl.items()],
             f"Ablation study trên {MODEL_VI[best]}")
    rp.fig("ablation", "Ablation study")

    def delta(a, b, key="cv_f1_mean"):
        return 100 * (abl[a][key] - abl[b][key])
    rp.bullets([
        f"Tách từ tiếng Việt (#4 so với #2): chênh {delta(nosw, noseg):+.2f} điểm CV Macro-F1.",
        f"Bigram (#1 so với #3): chênh {delta(full, uni):+.2f} điểm.",
        f"Lọc stopwords (#1 so với #4): chênh {delta(full, nosw):+.2f} điểm.",
    ])
    rp.p("Nhận xét: chênh lệch nào nhỏ hơn độ lệch chuẩn qua các fold thì không đủ bằng chứng để khẳng định bước đó có "
         "ích trên bộ dữ liệu này. Nhóm cần diễn giải bảng trên theo số liệu thực tế, không mặc định mọi bước tiền xử lý đều cải thiện kết quả.",
         italic=True)
    rp.h("7.3. Phân tích lỗi", 2)
    rp.p(f"Trên test synthetic, {MODEL_VI[best]} sai {R['n_errors_test']} câu. Accuracy theo văn phong: "
         + ", ".join(f"{k} {pct(v)}" for k, v in R["acc_by_style"].items()) + ".")
    rp.fig("acc_by_style", "Accuracy theo văn phong", 11)
    rp.table(["Câu hỏi", "Điều", "Nhãn thật", "Dự đoán"],
             [[e["question"], e["article_id"], e["true_code"], e["pred_code"]] for e in R["error_examples"][:10]],
             "Ví dụ câu bị phân loại sai (test synthetic)")
    if has_real and R.get("real_error_examples"):
        rp.table(["Câu hỏi thật", "Điều", "Nhãn thật", "Dự đoán"],
                 [[e["question"][:300], e["article_id"], e["label_code"], e["pred_code"]] for e in R["real_error_examples"][:8]],
                 "Ví dụ câu hỏi thật bị phân loại sai")
    top_pair = next(iter(R.get("top_confusions", {})), "hai lớp gần nghĩa")
    rp.p("Các nguyên nhân lỗi thường gặp (nhóm cần đối chiếu với bảng trên): (1) giao thoa ngữ nghĩa giữa các lớp "
         f"dùng chung từ vựng, rõ nhất ở cặp {top_pair} trên test synthetic, và giữa trách nhiệm doanh nghiệp (C5) với "
         "chế độ bảo hiểm (C7) trên câu hỏi thật; (2) câu hỏi ngắn "
         "thiếu ngữ cảnh; (3) câu hỏi thật hỏi nhiều ý hoặc dẫn chiếu Nghị định/Thông tư; (4) từ ngữ đời thường không có "
         "trong tập huấn luyện.", italic=True)

    # 7.4 Kết quả module truy vấn (giai đoạn 2)
    rp.h("7.4. Kết quả module tra cứu Điều luật", 2)
    ret = R["retrieval"]
    cols = list(ret)
    rp.table(["Chỉ số"] + cols, [[k] + [pct(ret[c][k]) for c in cols] for k in ret[cols[0]]],
             "Top-k accuracy của module truy vấn Điều luật")
    t = ret["test"]
    rp.p(f"Oracle (biết đúng lớp): Top-1 = {pct(t['oracle_top1'])}, Top-3 = {pct(t['oracle_top3'])}. End-to-end (lớp dự "
         f"đoán): Top-1 = {pct(t['e2e_top1'])}. Chênh lệch oracle – end-to-end là lỗi lan truyền từ bộ phân loại. So với "
         f"tìm trên toàn bộ 62 Điều (Top-1 = {pct(t['nofilter_top1'])}), bước phân loại "
         + ("giúp thu hẹp không gian tìm kiếm và tăng độ chính xác." if t["e2e_top1"] > t["nofilter_top1"] else
            "không cải thiện Top-1; nhóm cần thảo luận nguyên nhân.")
         + f" Riêng các lớp có nhiều hơn 1 Điều, oracle Top-1 = {pct(t['oracle_top1_multi_article_classes'])}.")
    rp.p("Giao diện demo (Streamlit, app.py): người dùng nhập câu hỏi, hệ thống hiển thị nhóm quy định dự đoán, điểm tin "
         "cậy tương đối và toàn văn các Điều luật liên quan nhất. [Chèn ảnh chụp màn hình demo]", italic=True)
    if R.get("ood"):
        o = R["ood"]
        rr = o["reject_rate"]
        rp.h("7.5. Câu hỏi ngoài phạm vi", 2)
        rp.p(f"Trong {R['n_real'] + R.get('n_real_ood', 0)} câu hỏi thật thu thập được có liên quan đến an toàn lao động, "
             f"{R.get('n_real_ood', 0)} câu thực chất thuộc văn bản khác (chủ yếu Luật Bảo hiểm xã hội 2024, Bộ luật Lao động, "
             f"Nghị định/Thông tư) nên được đánh dấu ngoài phạm vi. Dùng xác suất lớn nhất của Logistic Regression làm độ tin "
             f"cậy, ngưỡng chọn tại phân vị 5% trên validation ({o['threshold']:.3f}). Tỷ lệ bị từ chối: câu ngoài phạm vi "
             f"{pct(rr.get('ood_real'))}, câu thật trong phạm vi {pct(rr.get('real_in_scope'))}, test synthetic {pct(rr.get('test'))}.")
        rp.p(("Độ tin cậy max-softmax phân biệt kém câu ngoài phạm vi: phần lớn câu ngoài phạm vi vẫn vượt ngưỡng, "
              "giả thuyết là do câu về bảo hiểm xã hội dùng chung từ vựng với C5/C7. Cần tập huấn luyện có lớp ngoài phạm vi hoặc phương pháp "
              "phát hiện OOD tốt hơn.") if rr.get("ood_real", 0) < 0.3 else
             "Ngưỡng độ tin cậy từ chối được phần lớn câu ngoài phạm vi, có thể dùng trong demo.")
        rp.fig("ood_confidence", "Phân bố độ tin cậy: trong phạm vi và ngoài phạm vi", 13)

    # 9
    rp.h("8. Kết luận")
    rp.p(f"Đề tài đã xây dựng được pipeline hoàn chỉnh: corpus 93 Điều luật cập nhật 2024, bộ dữ liệu {R['n_samples']} câu "
         f"hỏi 8 lớp, so sánh 4 mô hình ML với quy trình chống rò rỉ dữ liệu, ablation study, phân tích lỗi và demo tra cứu.")
    rp.p("Hạn chế: dữ liệu huấn luyện được sinh tự động nên văn phong đồng đều hơn thực tế; tập câu hỏi thật nhỏ; chưa "
         "xử lý câu hỏi nhiều ý và câu ngoài phạm vi (Điều 63–93); chưa tích hợp mức xử phạt hành chính.")
    rp.h("9. Hướng phát triển")
    rp.bullets(["Thu thập và gán nhãn thêm câu hỏi thật, đo độ đồng thuận giữa người gán nhãn (Cohen's kappa).",
                "Phân loại đa nhãn (multi-label) cho câu hỏi nhiều ý; mở rộng ra Điều 63–93 và các Nghị định, Thông tư hướng dẫn.",
                "Tích hợp mức xử phạt theo Nghị định 12/2022/NĐ-CP (sau khi kiểm tra hiệu lực).",
                "Hiệu chỉnh xác suất (CalibratedClassifierCV) để phát hiện câu hỏi ngoài phạm vi.",
                "So sánh với mô hình ngôn ngữ tiền huấn luyện tiếng Việt (PhoBERT) và truy vấn ngữ nghĩa bằng embedding."])

    # 10
    rp.h("10. Phụ lục")
    rp.bullets(["Mã nguồn: notebooks/uit_ohs_law_retrieval.ipynb, src/ (config, preprocess, dataset, models, retrieval), scripts/, app.py.",
                "Dữ liệu: data/ohs_law_articles.json, data/processed/ohs_questions.csv, data/processed/real_test.csv.",
                "Tài liệu thiết kế: docs/project-analysis.md, docs/labeling-guidelines.md.",
                "Tái lập: pip install -r requirements.txt; python -m scripts.build_articles; python -m src.dataset; chạy notebook; streamlit run app.py."])
    rp.h("Tài liệu tham khảo", 2)
    rp.bullets(["Quốc hội (2015). Luật An toàn, vệ sinh lao động số 84/2015/QH13.",
                "Văn phòng Quốc hội (2024). Văn bản hợp nhất số 14/VBHN-VPQH Luật An toàn, vệ sinh lao động.",
                "Cổng Hỏi đáp chính sách, Cổng TTĐT Chính phủ: https://chinhsachonline.chinhphu.vn.",
                "Pedregosa et al. (2011). Scikit-learn: Machine Learning in Python. JMLR 12.",
                "Underthesea – Vietnamese NLP Toolkit. https://github.com/undertheseanlp/underthesea."])
    rp.save()
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
