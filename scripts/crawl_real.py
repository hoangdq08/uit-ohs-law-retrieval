"""Crawl câu hỏi thật từ Cổng Hỏi đáp chính sách (chinhsachonline.chinhphu.vn) làm tập test thật.

Chỉ lấy câu hỏi + câu trả lời có nhắc "an toàn, vệ sinh lao động" hoặc chủ đề ATVSLĐ,
dùng cho mục đích học thuật. Crawl chậm (delay 1.5s), có cache.
Output: data/raw/real_candidates.jsonl (chưa gán nhãn).
Chỉ THÊM câu mới vào cuối file (theo URL), không đổi thứ tự câu cũ, vì real_labeled.jsonl đánh số theo thứ tự này.
Chạy: python -m scripts.crawl_real [--pages N]
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import time
import urllib.parse
import urllib.request

from src.config import RAW_DIR

BASE = "https://chinhsachonline.chinhphu.vn"
CACHE = RAW_DIR / "crawl_cache"  # gitignored
OUT = RAW_DIR / "real_candidates.jsonl"
DELAY = 1.5
PAGES_PER_KEYWORD = 4  # ~11 kết quả/trang
KEYWORDS = [
    "tai nạn lao động", "bệnh nghề nghiệp", "an toàn vệ sinh lao động", "bảo hộ lao động",
    "phương tiện bảo vệ cá nhân", "bồi dưỡng bằng hiện vật", "khám sức khỏe định kỳ",
    "huấn luyện an toàn", "thẻ an toàn", "khai báo tai nạn", "điều tra tai nạn",
    "trợ cấp tai nạn lao động", "giám định suy giảm", "nặng nhọc độc hại", "kiểm định",
    "quan trắc môi trường lao động", "dưỡng sức phục hồi", "tai nạn trên đường đi",
    "bồi thường tai nạn", "điều dưỡng phục hồi",
    "trợ cấp bệnh nghề nghiệp", "chế độ tai nạn lao động", "suy giảm khả năng lao động",
    "vệ sinh lao động", "an toàn lao động", "trang bị bảo hộ", "tai nạn khi đi công tác",
    "độc hại", "máy móc thiết bị nghiêm ngặt", "sự cố kỹ thuật",
]
_RELEVANT = re.compile(
    r"an toàn, vệ sinh lao động|an toàn vệ sinh lao động|tai nạn lao động|bệnh nghề nghiệp|"
    r"bảo hộ lao động|bồi dưỡng bằng hiện vật|huấn luyện an toàn|kiểm định kỹ thuật an toàn|"
    r"phương tiện bảo vệ cá nhân|nặng nhọc, độc hại|nặng nhọc độc hại|khám sức khỏe định kỳ|"
    r"suy giảm khả năng lao động|sự cố kỹ thuật",
    re.I)
_CITES_LAW = re.compile(r"Luật An toàn, vệ sinh lao động|Luật ATVSLĐ", re.I)


def get(url: str) -> str:
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / (hashlib.md5(url.encode()).hexdigest() + ".html")
    if f.exists():
        return f.read_text(encoding="utf-8")
    time.sleep(DELAY)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (UIT student project)"})
    body = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    f.write_text(body, encoding="utf-8")
    return body


def to_text(fragment: str) -> str:
    t = html.unescape(re.sub(r"<[^>]+>", " ", fragment))
    return re.sub(r"\s+", " ", t).strip()


def list_urls(keyword: str, pages: int) -> list[str]:
    urls: list[str] = []
    q = urllib.parse.quote(keyword)
    for page in range(1, pages + 1):
        path = "/danh-sach-cau-hoi.htm" if page == 1 else f"/danh-sach-cau-hoi/trang-{page}.htm"
        s = get(f"{BASE}{path}?typeqa=0&lvid=0&bnid=0&search={q}")
        # Chỉ lấy kết quả tìm kiếm (class question-title), bỏ link sidebar "xem nhiều"/"mới nhất".
        found = re.findall(r'<a href="(/[a-z0-9-]+-\d+\.htm)" title="[^"]*" class="question-title"', s)
        if not found:
            break
        urls.extend(found)
    return urls


def parse_detail(s: str) -> dict | None:
    text = to_text(re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", s))
    m = re.search(r"Chi tiết câu hỏi\s*(.+?)\s*Trả lời\s*(.+?)\s*(?:Chia sẻ|Tin liên quan|$)", text)
    if not m:
        return None
    title = re.search(r"<title>(.*?)</title>", s, re.S)
    return {"title": to_text(title.group(1)) if title else "", "question": m.group(1).strip(),
            "answer": m.group(2).strip()[:3000]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=int, default=PAGES_PER_KEYWORD, help="số trang kết quả mỗi từ khoá")
    args = ap.parse_args()
    old = [json.loads(l) for l in OUT.read_text(encoding="utf-8").splitlines() if l.strip()] if OUT.exists() else []
    have = {r["url"] for r in old}
    seen: set[str] = set()
    rows = []
    for kw in KEYWORDS:
        try:
            paths = list_urls(kw, args.pages)
        except Exception as e:  # 1 từ khoá lỗi mạng không làm mất cả lần crawl
            print(f"{kw!r}: lỗi {e}", flush=True)
            continue
        for path in paths:
            if path in seen:
                continue
            seen.add(path)
            if BASE + path in have:
                continue
            try:
                d = parse_detail(get(BASE + path))
            except Exception as e:
                print(f"  {path}: lỗi {e}", flush=True)
                continue
            # Giữ nếu câu HỎI thuộc chủ đề ATVSLĐ, hoặc câu TRẢ LỜI viện dẫn Luật ATVSLĐ.
            if not d or not (_RELEVANT.search(d["question"]) or _CITES_LAW.search(d["answer"])):
                continue
            d["url"] = BASE + path
            d["keyword"] = kw
            d["cited_articles_84_2015"] = sorted({int(x) for x in re.findall(
                r"Điều (\d+)[^.;]{0,80}?Luật An toàn, vệ sinh lao động", d["answer"])})
            rows.append(d)
        print(f"{kw!r}: {len(rows)} câu mới liên quan (đã xét {len(seen)} URL)", flush=True)
    with OUT.open("a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"-> {OUT}: {len(old)} câu cũ + {len(rows)} câu mới")


if __name__ == "__main__":
    main()
