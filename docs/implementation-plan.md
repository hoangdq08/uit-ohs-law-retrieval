# KẾ HOẠCH TRIỂN KHAI CHI TIẾT ĐỒ ÁN MÁY HỌC (ACTION PLAN)

> **Đề tài:** Xây dựng hệ thống Xử lý ngôn ngữ tự nhiên tra cứu các nội dung của Luật An toàn, vệ sinh lao động  
> **Thời gian thực hiện:** 4 Tuần  
> **Căn cứ yêu cầu:** [YeuCau.md](./course-requirements.md) & `TomTat.md` (tóm tắt bài giảng, chưa có trong repo)

> [!NOTE]
> **Changelog so với bản gốc (`PlanThucHien.md`):**
> 1. Tên file dữ liệu/code đổi sang tiếng Anh theo repo `uit-ohs-law-retrieval` (báo cáo Word, slide giữ tên tiếng Việt).
> 2. Split và GridSearchCV theo nhóm `seed_id` (xem [project-analysis.md](./project-analysis.md) mục 3.3).
> 3. Ablation: cấu hình "bỏ tách từ" không lọc stopwords, so với cấu hình "không stopwords".
> 4. Bỏ các con số kết quả viết trước (F1 ~91%, tụt 5.8%), thay bằng placeholder chờ thực nghiệm.
> 5. Thêm đánh giá Top-k cho module tra cứu và `data/penalties.json`.

> [!IMPORTANT]
> **Lịch thực tế (2026-09-28): deadline trước sáng thứ Tư, thay cho lịch 4 tuần bên dưới.** Các mục 2 (lịch theo tuần) và 3 (phân công) chỉ còn giá trị tham khảo.
>
> | Khung giờ | Việc | Đầu ra |
> |---|---|---|
> | T2 sáng | Sinh dataset synthetic (40 seed × 5 văn phong × 8 lớp) + validate; crawl câu hỏi thật chinhsachonline.chinhphu.vn + gán nhãn | `data/raw/gen/*.jsonl`, `data/processed/real_test.csv` |
> | T2 chiều | Notebook: EDA, tiền xử lý, group split, 4 mô hình + GridSearch, metrics, CM, ablation, error analysis; review chéo leakage | `notebooks/uit_ohs_law_retrieval.ipynb` |
> | T2 tối | Retrieval Top-k, demo Streamlit, figures | `src/retrieval.py`, `app.py`, `reports/figures/` |
> | T3 sáng | Sinh báo cáo Word + slide từ `reports/results.json` | `reports/*.docx`, `reports/*.pptx` |
> | T3 chiều | **Nhóm** đọc/sửa báo cáo, kiểm tra ngẫu nhiên ~100 mẫu, chụp màn hình demo, tập thuyết trình | Bản nộp |
>
> **Đã cắt so với plan gốc:** thu 300 seed thật + gán tay, đo Cohen's kappa, `penalties.json` (NĐ 12/2022) → chuyển sang Hướng phát triển.
> **Dữ liệu:** tập train/val/test là synthetic sinh bằng LLM từ nội dung Điều luật (ghi rõ trong báo cáo); test thật là câu hỏi người dân từ cổng Chính phủ, không dùng khi train/chọn model.

---

## 1. MỤC TIÊU & SẢN PHẨM BÀN GIAO (MILESTONES & DELIVERABLES)

```
                       TIẾN ĐỘ 4 TUẦN THỰC HIỆN
  Tuần 1              Tuần 2              Tuần 3              Tuần 4
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  DATASET &   │───>│  MODELING &  │───>│ EVALUATION & │───>│ REPORTING &  │
│ PREPROCESS   │    │ TUNING (ML)  │    │   ABLATION   │    │   DEFENSE    │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
 - Cào/Sinh data     - 4 mô hình ML      - So sánh F1        - Báo cáo Word
 - Gán nhãn 8 lớp    - GridSearch CV     - Confusion Matrix  - Slide 15 trang
 - Underthesea NLP   - Chống Leakage     - Ablation Study    - Demo App
```

### Bộ sản phẩm cuối cùng nộp cho Giảng viên:
1. **File Báo cáo Word (`BaoCao_DoAn_MayHoc.docx`):** Đầy đủ 10 chương mục theo chuẩn mục 5 của [YeuCau.md](./course-requirements.md).
2. **File Mã nguồn Notebook (`notebooks/uit_ohs_law_retrieval.ipynb`):** Chạy từ đầu đến cuối không lỗi, có Markdown giải thích từng ô code, trực quan hóa biểu đồ đẹp mắt.
3. **Tập Dữ Liệu (`data/processed/ohs_questions_clean.csv`, `data/ohs_law_articles.json`, `data/penalties.json`):** Có cấu trúc rõ ràng, sẵn sàng để tái lập thực nghiệm.
4. **Slide Thuyết Trình (`Slide_BaoCao_DoAn.pptx`):** 12 - 15 slide tóm tắt toàn bộ công trình, biểu đồ và điểm nhấn phản biện.
5. **Giao diện Demo (`app.py` - Streamlit):** Ứng dụng web mini cho phép người dùng gõ câu hỏi và hiển thị ngay kết quả phân loại + trích xuất điều luật thực tế.

---

## 2. KẾ HOẠCH CHI TIẾT THEO TỪNG TUẦN (WEEK-BY-WEEK ROADMAP)

### TUẦN 1: XÂY DỰNG DỮ LIỆU & PIPELINE TIỀN XỬ LÝ NLP TIẾNG VIỆT
*Mục tiêu tuần:* Hoàn thiện tập dữ liệu ~1.700 câu hỏi có gán nhãn chuẩn và xây dựng xong pipeline xử lý văn bản tiếng Việt.

| Ngày | Nhiệm vụ cụ thể | Người phụ trách | Sản phẩm hoàn thành (Output) |
| :---: | :--- | :---: | :--- |
| **Ngày 1** | - ✅ Cấu trúc hóa VBHN 14/VBHN-VPQH (2024) bằng `scripts/build_articles.py` -> `ohs_law_articles.json` (93 Điều: số điều, tên, nội dung, chương/mục, cờ sửa đổi 2024).<br>- ✅ Đối chiếu bảng nhãn 8 lớp với văn bản, cập nhật `LABELS` trong `src/config.py`.<br>- Chốt [labeling-guidelines.md](./labeling-guidelines.md) trước khi gán nhãn. | Nhóm | `data/ohs_law_articles.json` |
| **Ngày 2** | - Gán nhãn theo 8 nhóm chủ đề pháp lý ($C_0 \to C_7$), theo `labeling-guidelines.md`.<br>- Thu thập ~300 câu hỏi thực tế từ Cổng MOLISA, LuatVietnam, Thư Ký Luật (`source=real`, mỗi câu có `seed_id`). | Thành viên 1 | `data/raw/seed_questions.csv` |
| **Ngày 3 - 4** | - Sinh dữ liệu tăng cường (Augmentation / Paraphrasing) theo đa dạng văn phong (công nhân, nhân sự, khiếu nại). Mỗi câu sinh ra giữ `seed_id` của câu gốc, `source=augmented`.<br>- Đạt tối thiểu 180 - 220 mẫu cho mỗi nhóm (~1.700 mẫu). | Thành viên 1 + 2 | `data/raw/ohs_questions_raw.csv` |
| **Ngày 5** | - Thực hiện EDA (Exploratory Data Analysis):<br>  * Phân phối số lượng mẫu giữa các lớp (kiểm tra mất cân bằng).<br>  * Phân phối độ dài câu (Word count distribution).<br>  * Biểu đồ đám mây từ (WordCloud) cho từng lớp. | Thành viên 2 | File notebook phần EDA + biểu đồ |
| **Ngày 6 - 7** | - Viết module tiền xử lý NLP tiếng Việt:<br>  * Làm sạch ký tự, chuẩn hóa NFC, hạ chữ thường.<br>  * Tách từ bằng `underthesea.word_tokenize(format="text")`.<br>  * Xây dựng bộ `stopwords_vi_legal.txt` (bảo lưu từ phủ định).<br>- Xuất file dữ liệu sạch đã sẵn sàng. | Thành viên 3 | `src/preprocess.py`, `data/processed/ohs_questions_clean.csv` |

---

### TUẦN 2: THIẾT KẾ MÔ HÌNH MACHINE LEARNING & HUẤN LUYỆN
*Mục tiêu tuần:* Huấn luyện thành công ít nhất 4 mô hình Machine Learning, tối ưu hóa siêu tham số bằng Cross-Validation và đảm bảo tuyệt đối không bị Data Leakage.

| Ngày | Nhiệm vụ cụ thể | Người phụ trách | Sản phẩm hoàn thành (Output) |
| :---: | :--- | :---: | :--- |
| **Ngày 8** | - Thiết lập phân chia dữ liệu Train/Val/Test (~70% - 15% - 15%) bằng `StratifiedGroupKFold` với `groups=seed_id` (paraphrase cùng seed nằm chung 1 tập).<br>- Kiểm tra: giao `seed_id` giữa các tập phải rỗng (assert trong code).<br>- **Phòng chống Data Leakage:** Khởi tạo `TfidfVectorizer(ngram_range=(1,2))` chỉ `fit_transform` trên `X_train`, và `transform` trên `X_val`, `X_test`. | Thành viên 1 | `src/split.py` & Vectorizer chuẩn |
| **Ngày 9** | - Cài đặt và huấn luyện **Mô hình 1: Multinomial Naive Bayes** (Baseline Model).<br>- Ghi nhận các chỉ số hiệu suất ban đầu. | Thành viên 2 | Baseline MNB model + log kết quả |
| **Ngày 10** | - Cài đặt và huấn luyện **Mô hình 2: Logistic Regression** (Softmax / OvR).<br>- Thử nghiệm `class_weight='balanced'`, tinh chỉnh $C \in [0.1, 1.0, 10.0]$. | Thành viên 2 | Logistic Regression model |
| **Ngày 11** | - Cài đặt và huấn luyện **Mô hình 3: Linear Support Vector Machine (LinearSVC)**.<br>- Thử nghiệm hàm mất mát Hinge Loss / Squared Hinge Loss, tinh chỉnh siêu tham số $C$. | Thành viên 3 | LinearSVC model |
| **Ngày 12** | - Cài đặt và huấn luyện **Mô hình 4: Random Forest Classifier** (Tree-based Ensemble).<br>- Tinh chỉnh `n_estimators`, `max_depth`, trích xuất Feature Importance (Top-20 từ khóa quan trọng nhất). | Thành viên 3 | Random Forest model + Bảng Feature Importance |
| **Ngày 13 - 14** | - Tinh chỉnh siêu tham số toàn diện bằng `GridSearchCV` kết hợp `StratifiedGroupKFold(n_splits=5)` (truyền `groups=seed_id`). TF-IDF đặt trong `Pipeline` để fit lại trong từng fold.<br>- Lưu lại các trọng số và model tốt nhất (`models/*.joblib`). | Nhóm | Toàn bộ các model đã tối ưu |

---

### TUẦN 3: ĐÁNH GIÁ ĐA CHIỀU, ABLATION STUDY & XÂY DỰNG DEMO
*Mục tiêu tuần:* Thực hiện toàn bộ các thực nghiệm phản biện khoa học (Ablation Study, Error Analysis), ghép nối module tra cứu Cosine Similarity và hoàn thiện giao diện Demo.

| Ngày | Nhiệm vụ cụ thể | Người phụ trách | Sản phẩm hoàn thành (Output) |
| :---: | :--- | :---: | :--- |
| **Ngày 15 - 16** | - Đánh giá đa chiều trên tập Test độc lập:<br>  * Xuất bảng so sánh Accuracy, Macro-Precision, Macro-Recall, Macro-F1, Training Time giữa 4 mô hình.<br>  * Vẽ biểu đồ Ma trận nhầm lẫn (Confusion Matrix Heatmap) bằng `seaborn`. | Thành viên 2 | Bảng so sánh tổng thể + Biểu đồ Confusion Matrix |
| **Ngày 17 - 18** | - **Thực hiện Ablation Study (Bắt buộc theo yêu cầu Thầy Thăng)**, mỗi cặp chỉ khác 1 yếu tố:<br>  * #1 Full: Tách từ + lọc Stopwords + (1,2)-gram.<br>  * #2 Bỏ tách từ (không lọc stopwords), so với #4.<br>  * #3 Bỏ Bigram (chỉ Unigram), so với #1.<br>  * #4 Không lọc Stopwords, so với #1.<br>  * #5 (tùy chọn) Bỏ tách từ + Unigram, so với #2.<br>- Lập bảng đối chứng mức thay đổi Macro-F1 (kèm độ lệch chuẩn qua CV). | Thành viên 1 | Bảng đối chứng Ablation Study + Nhận xét khoa học |
| **Ngày 19** | - **Thực hiện Error Analysis (Phân tích lỗi sâu):**<br>  * Lọc danh sách các câu hỏi bị phân loại sai trên tập Test.<br>  * Mổ xẻ 10 ca sai điển hình (chỉ rõ câu hỏi, nhãn thật, nhãn mô hình đoán, lý do ngữ nghĩa hoặc từ khóa chồng lấn). | Thành viên 1 | Báo cáo phân tích lỗi sai (Error Analysis Report) |
| **Ngày 20** | - Xây dựng module **Information Retrieval (Tra cứu chi tiết):**<br>  * Lấy nhãn dự đoán từ mô hình tốt nhất (chọn theo kết quả thực nghiệm).<br>  * Tính Cosine Similarity giữa câu hỏi và danh sách các điều luật thuộc nhóm đó.<br>  * Trích xuất Top-1 Điều luật chính xác nhất cùng mức phạt hành chính (`data/penalties.json`, trích từ NĐ 12/2022).<br>  * Đánh giá Top-1 / Top-3 accuracy theo `article_id`, ở 2 chế độ oracle label và predicted label. | Thành viên 3 | `src/retrieval.py` |
| **Ngày 21** | - Xây dựng giao diện Demo bằng **Streamlit (`app.py`)**:<br>  * Ô nhập câu hỏi tình huống.<br>  * Hiển thị: Nhóm luật dự đoán (kèm độ tự tin xác suất) $\to$ Trích lục Điều luật chi tiết $\to$ Mức phạt vi phạm nếu có. | Thành viên 3 | Ứng dụng Demo hoàn chỉnh chạy trên máy cục bộ |

---

### TUẦN 4: HOÀN THIỆN BÁO CÁO WORD, SLIDE & LUYỆN VẤN ĐÁP
*Mục tiêu tuần:* Hoàn tất hồ sơ đồ án nộp cho Giảng viên, sẵn sàng bảo vệ đạt điểm tuyệt đối.

| Ngày | Nhiệm vụ cụ thể | Người phụ trách | Sản phẩm hoàn thành (Output) |
| :---: | :--- | :---: | :--- |
| **Ngày 22 - 24** | - Viết Báo cáo Word hoàn chỉnh 10 phần theo đúng mục 5 trong [YeuCau.md](./course-requirements.md):<br>  1. Tóm tắt đề tài<br>  2. Giới thiệu bài toán & Dataset<br>  3. EDA + Biểu đồ<br>  4. Tiền xử lý dữ liệu<br>  5. Mô hình và thông số kỹ thuật<br>  6. Kết quả và phân tích số liệu<br>  7. So sánh các mô hình<br>  8. Kết luận<br>  9. Hướng phát triển<br>  10. Phụ lục code & Trích dẫn | Thành viên 1 + Nhóm | `BaoCao_DoAn_MayHoc.docx` |
| **Ngày 25 - 26** | - Soạn Slide thuyết trình PowerPoint (12 - 15 slides):<br>  * Thiết kế trực quan, súc tích, nhiều sơ đồ và biểu đồ thay vì chữ.<br>  * Nhấn mạnh: Sơ đồ kiến trúc, Bảng Benchmark, Bảng Ablation Study, Confusion Matrix, Error Analysis và Demo thực tế. | Thành viên 2 + 3 | `Slide_BaoCao_DoAn.pptx` |
| **Ngày 27** | - Rà soát toàn bộ Code Notebook, làm sạch comment, kiểm tra khả năng chạy lại từ đầu (`Restart & Run All Cells`) trong 1 phút.<br>- Đóng gói thư mục sản phẩm chuẩn nộp bài. | Thành viên 3 | Thư mục mã nguồn sạch hoàn hảo |
| **Ngày 28** | - Cả nhóm tập dượt thuyết trình (Canh thời gian 10 - 12 phút).<br>- Phản biện nội bộ dựa trên **Bộ 6 câu hỏi vấn đáp của Thầy Thăng** trong `TomTat.md` (tóm tắt bài giảng, chưa có trong repo). | Cả nhóm | Hoàn toàn tự tin bước vào buổi báo cáo |

---

## 3. PHÂN CÔNG VAI TRÒ & TRÁCH NHIỆM (ROLE & RESPONSIBILITIES)

Mẫu phân công nhóm 3 thành viên (linh hoạt điều chỉnh theo số lượng thành viên thực tế của nhóm):

| Thành viên | Vai trò chính | Trách nhiệm cốt lõi |
| :--- | :--- | :--- |
| **Thành viên 1** *(Trưởng nhóm)* | **Data Lead & Technical Writer** | - Quản lý tiến độ chung.<br>- Xây dựng và kiểm tra chất lượng tập Dataset.<br>- Viết Báo cáo Word 10 chương mục.<br>- Phân tích lỗi sai (Error Analysis). |
| **Thành viên 2** | **ML Modeling & Optimization Lead** | - Viết Pipeline EDA và trực quan hóa số liệu.<br>- Cài đặt và huấn luyện 4 mô hình Machine Learning.<br>- Tinh chỉnh siêu tham số bằng GridSearchCV.<br>- Soạn nội dung slide kỹ thuật. |
| **Thành viên 3** | **Evaluation & Demo App Lead** | - Xây dựng Pipeline tiền xử lý văn bản tiếng Việt (`underthesea`).<br>- Thực hiện Ablation Study và xuất bảng so sánh.<br>- Lập trình module Tra cứu (Cosine Similarity) & App Demo Streamlit.<br>- Rà soát kỹ thuật và kiểm thử mã nguồn. |

---

## 4. CHECKLIST KIỂM TRA CHẤT LƯỢNG (QUALITY ASSURANCE CHECKLIST)

Trước khi nộp sản phẩm cho Thầy Cáp Phạm Đình Thăng, nhóm phải tick đủ toàn bộ danh sách kiểm tra sau:

- [ ] **1. Không bị Data Leakage:** Đã đảm bảo gọi `fit_transform` trên `X_train` và chỉ gọi `transform` trên `X_val`/`X_test` chưa?
- [ ] **2. Phân chia Stratified Group Split:** Đã chia theo `seed_id` (không seed nào nằm ở 2 tập) và kiểm tra phân phối lớp đồng đều chưa?
- [ ] **3. Đủ số lượng mô hình:** Đã cài đặt ít nhất 3 - 4 mô hình Machine Learning khác nhau (Naive Bayes, Logistic Regression, LinearSVC, Random Forest) chưa?
- [ ] **4. Đánh giá đa chiều:** Đã có đầy đủ Accuracy, Precision, Recall, Macro-F1 và Confusion Matrix chưa?
- [ ] **5. Có Ablation Study:** Đã thực hiện ít nhất 3 cấu hình đối chứng để chứng minh vai trò của Tách từ tiếng Việt, N-gram và Stopwords chưa?
- [ ] **6. Có Error Analysis:** Đã mổ xẻ cụ thể các mẫu dữ liệu bị đoán sai trên Confusion Matrix chưa?
- [ ] **7. Biện luận chỉ số hợp lý:** Đã chuẩn bị sẵn lời giải thích tại sao dùng Macro-F1 thay vì chỉ nhìn vào Accuracy chưa?
- [ ] **8. Khả năng tái lập (Reproducibility):** Đã cố định `random_state=42` ở tất cả các bước chia dữ liệu và khởi tạo mô hình chưa?

---

## 5. DÀN Ý CHI TIẾT FILE BÁO CÁO WORD (THEO CHUẨN YÊU CẦU MÔN HỌC)

Cấu trúc file Word bắt buộc tuân theo 10 phần tại mục 5 trong [YeuCau.md](./course-requirements.md):

```
Trang bìa & Mục lục
1. Tóm tắt đề tài (Executive Summary)
   - Giới thiệu bài toán, mục tiêu, kết quả chính đạt được và mô hình tối ưu nhất.
2. Giới thiệu bài toán & Tập dữ liệu
   - Giới thiệu Luật An toàn, vệ sinh lao động 2015.
   - Thống kê bộ dữ liệu: Số lượng mẫu (~1.700), 8 lớp nhãn, bảng mô tả chi tiết từng lớp.
   - Phương pháp phân chia tập Train / Validation / Test.
3. Phân tích khám phá dữ liệu (EDA)
   - Biểu đồ phân bố số lượng mẫu theo từng lớp (Class distribution).
   - Biểu đồ phân bố độ dài câu hỏi (Sentence length).
   - Đám mây từ khóa (WordCloud) đại diện cho từng nhóm pháp lý.
4. Tiền xử lý dữ liệu (Data Preprocessing)
   - Các bước làm sạch, chuẩn hóa văn bản tiếng Việt.
   - Thuật toán tách từ tiếng Việt (Word Segmentation qua Underthesea).
   - Danh sách Stopwords pháp lý.
   - Kỹ thuật trích xuất đặc trưng TF-IDF (Unigram + Bigram).
5. Mô hình Machine Learning & Cấu hình tham số
   - Trình bày cơ sở lý thuyết ngắn gọn của 4 mô hình: MultinomialNB, Logistic Regression, LinearSVC, Random Forest.
   - Bảng tổng hợp các siêu tham số sau khi tinh chỉnh qua GridSearchCV.
6. Kết quả thực nghiệm và Phân tích
   - Bảng so sánh tổng thể các chỉ số: Accuracy, Precision, Recall, Macro-F1.
   - Phân tích chi tiết Ma trận nhầm lẫn (Confusion Matrix Heatmap).
   - Kiểm tra hiện tượng Overfitting / Underfitting giữa tập Train và Validation.
7. So sánh mô hình & Thực nghiệm loại bỏ (Ablation Study)
   - Nhận xét khoa học: Tại sao mô hình này vượt trội hơn mô hình kia?
   - Bảng kết quả Ablation Study kiểm chứng các bước tiền xử lý.
   - Phân tích lỗi sai chuyên sâu (Error Analysis) trên các mẫu bị phân loại nhầm.
8. Module Tra cứu Thông tin & Minh họa Hệ thống Demo
   - Kiến trúc module tính độ tương đồng Cosine Similarity trích xuất Điều luật cụ thể.
   - Ảnh chụp màn hình giao diện ứng dụng Demo thực tế.
9. Kết luận & Hướng phát triển
   - Đánh giá mức độ hoàn thành so với mục tiêu ban đầu.
   - Các hạn chế hiện tại (số lượng dữ liệu, câu hỏi phức hợp đa ý).
   - Hướng mở rộng: Multilabel classification, tích hợp thêm các văn bản dưới luật (Nghị định, Thông tư).
10. Phụ lục mã nguồn & Tài liệu tham khảo
```

---

## 6. KỊCH BẢN THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN (12 PHÚT VÀNG)

- **Phút 1 - 2 (Mở đầu & Bối cảnh):** Nêu bật tính cấp thiết của việc tra cứu Luật ATVSLĐ bằng ngôn ngữ tự nhiên; định hình rõ bài toán Machine Learning phân loại ý định pháp lý.
- **Phút 3 - 4 (Dữ liệu & Tiền xử lý):** Trình bày ngắn gọn về Dataset ~1.700 mẫu 8 lớp; nhấn mạnh bước tách từ tiếng Việt bằng `underthesea` và kỹ thuật chống Data Leakage.
- **Phút 5 - 7 (Mô hình & Bảng kết quả Benchmark):** 
  - Chiếu bảng so sánh 4 mô hình: Naive Bayes, Logistic Regression, LinearSVC, Random Forest.
  - Tuyên bố mô hình chiến thắng: `<model tốt nhất>` đạt Macro-F1 `<kết quả thực nghiệm>`.
- **Phút 8 - 9 (Điểm nhấn ăn điểm: Ablation Study & Error Analysis):**
  - Chiếu bảng Ablation Study: mức thay đổi F1 khi bỏ tách từ tiếng Việt là `<kết quả thực nghiệm>`.
  - Mở Confusion Matrix và chỉ ra chính xác 1-2 trường hợp đoán sai do câu hỏi giao thoa ngữ nghĩa.
- **Phút 10 - 11 (Demo Trực tiếp):**
  - Thao tác trên giao diện Streamlit: Gõ 1 câu hỏi thực tế $\to$ Hệ thống dự đoán đúng nhóm luật $\to$ Trả về đúng số Điều và mức phạt trong vòng 0.2 giây.
- **Phút 12 (Kết luận & Mời Hội đồng chấm):** Tóm tắt đóng góp và sẵn sàng trả lời phản biện của Thầy.
