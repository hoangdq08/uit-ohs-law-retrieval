# uit-ohs-law-retrieval

Đồ án môn Máy học (UIT): hệ thống tra cứu Luật An toàn, vệ sinh lao động (Luật 84/2015/QH13) bằng NLP tiếng Việt.

Kiến trúc 2 giai đoạn:
1. **Classifier (lõi ML):** câu hỏi -> nhóm quy định (8 lớp, Đ1–62). TF-IDF (1,2)-gram + MNB / LogReg / LinearSVC / RandomForest.
2. **Retrieval:** trong nhóm dự đoán, xếp hạng Điều luật bằng cosine similarity.

## Cấu trúc

```
docs/
  course-requirements.md    # đề của thầy (nguyên văn)
  project-analysis.md       # phân tích đề tài (đã chỉnh, xem changelog đầu file)
  implementation-plan.md    # kế hoạch 4 tuần (đã chỉnh)
  labeling-guidelines.md    # tiêu chí gán nhãn 8 lớp
data/
  raw/                      # ohs_questions_raw.csv, seed questions
  processed/                # ohs_questions_clean.csv
  ohs_law_articles.json     # corpus Điều luật
  stopwords_vi_legal.txt    # stopwords (đã giữ lại từ phủ định/điều kiện)
src/
  config.py                 # paths, labels, random_state
  preprocess.py             # normalize -> word segment -> stopwords
scripts/
  build_articles.py         # tải + parse VBHN 14/VBHN-VPQH (2024) -> ohs_law_articles.json
notebooks/                  # uit_ohs_law_retrieval.ipynb
models/                     # *.joblib (gitignored)
reports/figures/            # biểu đồ EDA, confusion matrix
app.py                      # Streamlit demo (sau)
```

## Setup

`underthesea` chưa hỗ trợ Python 3.14, dùng 3.12:

```bash
uv venv --python 3.12
source .venv/bin/activate
uv pip install -r requirements.txt
python -m src.preprocess "Công nhân KHÔNG được trang bị đồ bảo hộ lao động thì sao?"
```

## Chạy lại toàn bộ

```bash
python -m scripts.validate_generated          # kiểm data/raw/gen/c0..c7.jsonl
python -m src.dataset                         # -> data/processed/ohs_questions.csv (split theo seed)
python -m scripts.build_real_test             # data/raw/real_labeled.jsonl -> data/processed/real_test.csv
python -m scripts.build_notebook
jupyter nbconvert --to notebook --execute --inplace notebooks/uit_ohs_law_retrieval.ipynb --ExecutePreprocessor.timeout=1800
python -m scripts.build_report                # -> reports/BaoCao_DoAn_MayHoc.docx
python -m scripts.build_slides                # -> reports/Slide_BaoCao_DoAn.pptx
streamlit run app.py
```

Sửa nhãn câu hỏi thật: chỉ sửa `data/raw/real_labeled.jsonl` (`decision` = `in_scope` / `out_of_scope` / `multi_intent`, và `article_id` khi in_scope). Không sửa tay `real_test.csv`. Sau đó chạy từ `build_real_test` trở xuống.

## Quy tắc thực nghiệm

- `random_state=42` ở mọi bước.
- Vectorizer chỉ `fit` trên train, `transform` cho val/test.
- Dữ liệu augmentation: split theo nhóm câu seed (`seed_id`) để tránh paraphrase của cùng một câu rơi vào cả train và test.
