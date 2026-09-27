# Việc còn lại cho nhóm (trước sáng thứ 4)

Mọi số liệu trong báo cáo/slide đã sinh từ lần chạy thật. Các việc dưới đây cần **người** làm.
Làm xong việc nào thì đánh `[x]`. Việc 1 và 2 thay đổi dữ liệu nên phải chạy lại pipeline (mục "Chạy lại" cuối file).

## A. Review dữ liệu (làm trước, vì có thể đổi số liệu)

- [ ] **1. Review 9 nhãn câu hỏi thật** (~20 phút) → `docs/real-label-review.md`
  - Thực tế chỉ cần mở link của **dòng 33** (có thể đổi thành in_scope Đ14) và **dòng 64** (có thể đổi Đ39 → Đ38). 7 dòng còn lại gợi ý giữ nguyên, đọc lướt xác nhận.
  - Sửa trong `data/raw/real_labeled.jsonl` (trường `decision`, `article_id`). Không sửa tay `data/processed/real_test.csv`.
  - Ghi số nhãn đã đổi: ____
- [ ] **2. Đọc kiểm tra 40 câu synthetic** (~20 phút) → `docs/synthetic-sample-review.md`
  - Điền cột OK?/Ghi chú. Câu sai: sửa cả 5 dòng cùng `seed_id` trong `data/raw/gen/c{k}.jsonl`, rồi chạy `python -m scripts.validate_generated`.
  - Ghi: đã đọc 40, sai ____, đã sửa/loại ____

## B. Chạy lại (chỉ khi việc 1 hoặc 2 có sửa dữ liệu)

```bash
cd uit-ohs-law-retrieval
.venv/bin/python -m scripts.validate_generated        # nếu sửa data/raw/gen
.venv/bin/python -m src.dataset                       # nếu sửa data/raw/gen
.venv/bin/python -m scripts.build_real_test
.venv/bin/python -m scripts.build_notebook
.venv/bin/jupyter nbconvert --to notebook --execute --inplace notebooks/uit_ohs_law_retrieval.ipynb --ExecutePreprocessor.timeout=1800
.venv/bin/python -m scripts.build_report
.venv/bin/python -m scripts.build_slides
```

Lưu ý: `build_report` / `build_slides` **ghi đè** file .docx/.pptx. Chạy lại xong mới làm mục C, nếu không sẽ mất chỉnh sửa tay.

## C. Chỉnh tay trên file Word/PowerPoint (làm sau cùng)

`reports/BaoCao_DoAn_MayHoc.docx`:
- [ ] Trang bìa: điền `<Họ tên – MSSV>` (3 dòng).
- [ ] Mục 2.3: thay đoạn `[NHÓM ĐIỀN SAU KHI REVIEW ...]` bằng kết quả việc 2 (vd "Nhóm đã đọc kiểm tra 40 câu gốc, phát hiện 1 câu sai, đã sửa.").
- [ ] Mục 2.3: thay đoạn `[NHÓM ĐIỀN SAU KHI REVIEW ...]` về câu hỏi thật bằng kết quả việc 1.
- [ ] Mục 7.4: thay `[Chèn ảnh chụp màn hình demo]` bằng ảnh chụp. Chạy demo: `.venv/bin/streamlit run app.py`, nhập 1 câu ví dụ, bấm "Tra cứu", chụp cả 2 cột kết quả.
- [ ] Đọc lại toàn bộ 1 lượt, đặc biệt mục 6, 7.2 (ablation), 7.3 (phân tích lỗi), 7.5 (ngoài phạm vi). Các nhận xét được viết thận trọng theo số liệu; ai thuyết trình phần nào cần hiểu phần đó.

`reports/Slide_BaoCao_DoAn.pptx`:
- [ ] Slide 1: điền `<tên thành viên>`.
- [ ] Slide 10 (tra cứu): có thể chèn ảnh demo.

## D. Kịch bản demo (đã chạy thử với model hiện tại)

Chạy: `.venv/bin/streamlit run app.py` (model `models/best_classifier.joblib` đã có sẵn trong repo, không cần chạy notebook trước).
Nếu chạy lại notebook thì model có thể đổi, cần thử lại các câu dưới.

| # | Câu nhập | Kết quả khi thử | Nói gì |
|---|---|---|---|
| 1 | Công ty phát tiền thay cho khẩu trang và găng tay bảo hộ có đúng luật không? | C2 Phương tiện bảo vệ cá nhân, Đ23 | Lớp chỉ có 1 Điều, tra cứu đúng ngay |
| 2 | Làm ca đêm trong môi trường độc hại thì được bồi dưỡng bằng hiện vật không? | C3, Đ24 đứng đầu | Lớp nhiều Điều, retrieval chọn đúng Điều trong lớp |
| 3 | Xảy ra tai nạn chết người ở công trường thì phải báo cho cơ quan nào? | C4, Đ34 Khai báo đứng đầu | Văn phong đời thường vẫn đúng |
| 4 | Bị tai nạn trên đường đi làm có được bảo hiểm trả trợ cấp không? | C7, Đ45 Điều kiện hưởng đứng đầu | Phân biệt bảo hiểm (C7) với trách nhiệm công ty (C5) |
| 5 | Lao động nữ sinh con được nghỉ thai sản mấy tháng? | Vẫn gán C7 với điểm thấp (~0.31), trả Điều không liên quan | **Chủ động nêu hạn chế:** câu ngoài phạm vi (thuộc Luật BHXH) nhưng hệ thống không từ chối, đúng như mục 7.5 báo cáo |

Tránh dùng khi demo: "Công nhân ngã giàn giáo gãy chân thì công ty có phải trả viện phí không?" (đúng lớp C5 nhưng Đ39 đứng trên Đ38, và điểm chỉ 0.23 nên hiện cảnh báo độ tin cậy thấp).

## E. Chuẩn bị trả lời khi thầy hỏi

- **Dữ liệu ở đâu ra?** 1600 câu do LLM (Claude) sinh theo `docs/labeling-guidelines.md`, nhãn lớp suy tự động từ Điều. Kiểm bằng `scripts/validate_generated.py` + nhóm đọc mẫu 40 câu. 29 câu thật từ chinhsachonline.chinhphu.vn, nhãn LLM gán theo Điều mà Bộ viện dẫn, nhóm review dòng chưa chắc.
- **Vì sao chia theo seed_id?** 5 văn phong của 1 câu gốc gần như cùng nội dung; chia ngẫu nhiên thì paraphrase lọt sang test, điểm bị thổi phồng.
- **Vì sao chọn LinearSVC?** Val Macro-F1 cao nhất. Nhưng CV lại xếp LogReg cao hơn, chênh lệch nhỏ hơn độ lệch chuẩn giữa các fold, nên báo cáo không khẳng định SVC vượt trội.
- **Vì sao câu thật chỉ ~60% trong khi test ~90%?** Khác biệt miền: câu thật dài ~127 âm tiết, nhiều bối cảnh, viện dẫn Nghị định; test synthetic ~20 âm tiết. Tập thật chỉ 29 câu nên dao động lớn.
- **Ablation cho thấy gì?** Mọi chênh lệch nhỏ hơn std giữa các fold: chưa bước tiền xử lý nào được chứng minh cải thiện rõ.

## Không cần làm

- Review toàn bộ 1600 câu synthetic hoặc 116 câu thật.
- Đo Cohen's kappa (đã ghi ở Hướng phát triển).
- Sửa code, thêm tính năng, tinh chỉnh model theo tập câu thật (sẽ thành rò rỉ dữ liệu).
