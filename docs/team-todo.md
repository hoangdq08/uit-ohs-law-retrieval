# Việc còn lại cho nhóm (trước sáng thứ 4)

Mọi số liệu trong báo cáo/slide đã sinh từ lần chạy thật. Các việc dưới đây cần **người** làm.
Làm xong việc nào thì đánh `[x]`. Việc 1 và 2 thay đổi dữ liệu nên phải chạy lại pipeline (mục "Chạy lại" cuối file).

## A. Review dữ liệu (làm trước, vì có thể đổi số liệu)

- [x] **1a. Gán nhãn mù 176 câu hỏi thật.** A (Toàn) gán tay. Phiếu B được điền bằng Codex (`annotation_source=ai_assisted`), nên `score` tính B là **LLM thứ hai, không phải người**. Báo cáo ghi đúng như vậy.
  - Kết quả: A so với GPT đồng thuận 98.3%, kappa 0.96 (xem `reports/agreement.json`).
  - Nhãn GPT gốc được đóng băng ở `data/raw/blind/llm_labels_frozen.jsonl`: sửa `real_labeled.jsonl` sau này không làm đổi số đồng thuận. **Không xoá file này.**
  - Không có thời gian thì bỏ qua: nếu Thái tự gán mù (không xem phiếu B cũ, không dùng AI) trên phiếu trắng, thì xoá cột `annotation_source` của phiếu B, chạy lại `score`, báo cáo sẽ tự ghi kappa giữa hai người.
- [ ] **1b. Chốt nhãn** (A, ~15 phút) → `docs/label-adjudication.md`
  - Mục 1 (3 câu A khác GPT: 33, 73, 124): mở link, quyết định. Nếu GPT sai thì sửa `decision`/`article_id` trong `data/raw/real_labeled.jsonl`.
  - Mục 2 (9 câu chỉ B khác): đọc lướt, thường giữ nguyên.
  - Không sửa tay `data/processed/real_test.csv` và file trong `data/raw/blind/`.
  - Có sửa thì chạy lại mục B.
- [x] **2. Đọc kiểm tra 40 câu synthetic** → `docs/synthetic-sample-review.md`: 40/40 ok, báo cáo tự điền.

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
Đoạn về độ đồng thuận ở mục 2.3 báo cáo tự điền từ `reports/agreement.json`, không cần sửa tay. Nếu có sửa phiếu A/B thì chạy `.venv/bin/python -m scripts.blind_labeling score` trước `build_report`.

## C. Chỉnh tay trên file Word/PowerPoint (làm sau cùng)

`reports/BaoCao_DoAn_MayHoc.docx`:
- [x] Trang bìa: tự lấy từ `reports/Nhom27.txt`.
- [x] Mục 2.3: review synthetic và độ đồng thuận tự điền.
- [x] Mục 7.4 + slide "Demo giao diện": tự lấy từ `reports/figures/demo.png` (thay ảnh thì ghi đè file này rồi build lại).
- [ ] Đọc lại toàn bộ 1 lượt, đặc biệt mục 6, 7.2 (ablation), 7.3 (phân tích lỗi), 7.5 (ngoài phạm vi). Các nhận xét được viết thận trọng theo số liệu; ai thuyết trình phần nào cần hiểu phần đó.

`reports/Slide_BaoCao_DoAn.pptx`:
- [x] Slide 1: đã có tên thành viên (Toàn làm).
- [x] Slide 11 "Demo giao diện": ảnh demo đã có (build_slides tự thêm).

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

- **Dữ liệu ở đâu ra?** 1600 câu do LLM (Claude) sinh theo `docs/labeling-guidelines.md`, nhãn lớp suy tự động từ Điều. Kiểm bằng `scripts/validate_generated.py` + nhóm đọc mẫu 40 câu (40/40 đúng). Câu thật từ chinhsachonline.chinhphu.vn (176 câu thu thập, 42 trong phạm vi), nhãn GPT gán theo Điều mà Bộ viện dẫn, rồi 1 thành viên gán nhãn mù độc lập: đồng thuận 98.3%, kappa 0.96 với GPT.
- **Sao không có kappa giữa 2 người?** Nói thẳng: chỉ có 1 người gán tay; phiếu thứ hai làm bằng AI nên nhóm không tính là người và đã ghi rõ trong báo cáo. Đây là hạn chế, ghi ở Hướng phát triển.
- **Vì sao chia theo seed_id?** 5 văn phong của 1 câu gốc gần như cùng nội dung; chia ngẫu nhiên thì paraphrase lọt sang test, điểm bị thổi phồng.
- **Vì sao chọn LinearSVC?** Val Macro-F1 cao nhất. Nhưng CV lại xếp LogReg cao hơn, chênh lệch nhỏ hơn độ lệch chuẩn giữa các fold, nên báo cáo không khẳng định SVC vượt trội.
- **Vì sao câu thật thấp hơn nhiều so với test (~90%)?** Khác biệt miền: câu thật dài, nhiều bối cảnh, viện dẫn Nghị định; test synthetic ngắn. Tập thật chỉ vài chục câu và lệch lớp (C0, C4, C6 chỉ 1 câu) nên dao động lớn. Lấy số chính xác trong báo cáo sau khi chạy lại.
- **Ablation cho thấy gì?** Mọi chênh lệch nhỏ hơn std giữa các fold: chưa bước tiền xử lý nào được chứng minh cải thiện rõ.

## Không cần làm

- Review toàn bộ 1600 câu synthetic.
- Sửa code, thêm tính năng, tinh chỉnh model theo tập câu thật (sẽ thành rò rỉ dữ liệu).
