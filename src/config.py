"""Cấu hình chung: paths, nhãn, random_state."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
MODELS_DIR = ROOT / "models"
FIGURES_DIR = ROOT / "reports" / "figures"

ARTICLES_PATH = DATA_DIR / "ohs_law_articles.json"
STOPWORDS_PATH = DATA_DIR / "stopwords_vi_legal.txt"
RAW_QUESTIONS_PATH = RAW_DIR / "ohs_questions_raw.csv"
CLEAN_QUESTIONS_PATH = PROCESSED_DIR / "ohs_questions_clean.csv"

RANDOM_STATE = 42

# 8 lớp theo docs/project-analysis.md mục 3.1, mỗi Điều chỉ thuộc 1 lớp.
# Đã đối chiếu tiêu đề Điều với văn bản gốc (data/ohs_law_articles.json, 2026-09-28):
# C3 = Đ21 (khám SK), Đ24 (bồi dưỡng hiện vật), Đ26 (điều dưỡng phục hồi SK), Đ27 (quản lý SK).
# Đ25 (thời giờ làm việc nơi nguy hiểm) chuyển về C1.
# C7 = Mục 3 Chương III (Đ41-62). Đ63-93 ngoài phạm vi (xem docs/project-analysis.md).
# Nguồn văn bản: VBHN 14/VBHN-VPQH (2024), xem scripts/build_articles.py.
LABELS = {
    0: ("QUY_DINH_CHUNG", "Quy định chung, quyền và nghĩa vụ", list(range(1, 13))),
    1: ("BIEN_PHAP_PHONG_NGUA", "Biện pháp phòng ngừa, cải thiện điều kiện làm việc",
        [a for a in range(13, 34) if a not in (14, 21, 23, 24, 26, 27)]),
    2: ("PHUONG_TIEN_BAO_HO", "Phương tiện bảo vệ cá nhân", [23]),
    3: ("SUC_KHOE_BOI_DUONG", "Khám sức khỏe, bệnh nghề nghiệp, bồi dưỡng hiện vật", [21, 24, 26, 27]),
    4: ("KHAI_BAO_DIEU_TRA", "Khai báo, điều tra, thống kê tai nạn/sự cố", list(range(34, 38))),
    5: ("CHE_DO_BOI_THUONG", "Bồi thường, trợ cấp tai nạn lao động", list(range(38, 41))),
    6: ("HUAN_LUYEN_ATLD", "Huấn luyện an toàn, vệ sinh lao động", [14]),
    7: ("BAO_HIEM_TNLD", "Bảo hiểm tai nạn lao động, bệnh nghề nghiệp (Quỹ BHXH chi trả)", list(range(41, 63))),
}

LABEL_CODES = {k: v[0] for k, v in LABELS.items()}
ARTICLE_TO_LABEL = {a: k for k, v in LABELS.items() for a in v[2]}

assert len(ARTICLE_TO_LABEL) == sum(len(v[2]) for v in LABELS.values()), "Điều bị gán cho >1 lớp"
