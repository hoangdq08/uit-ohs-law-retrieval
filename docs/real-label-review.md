# Review nhãn câu hỏi thật (9 dòng chưa chắc)

Nguồn nhãn duy nhất: `data/raw/real_labeled.jsonl`. "Dòng" là thứ tự dòng đếm từ 0.
Nhãn hiện tại do gpt-6-sol gán. Nhóm đọc câu trả lời gốc (link), đối chiếu Điều luật, rồi ghi quyết định vào cột **Nhóm**.

Quy tắc (docs/labeling-guidelines.md): chọn Điều của Luật ATVSLĐ **trả lời trực tiếp** câu hỏi.
- `in_scope` + `article_id`: câu trả lời chủ yếu dựa trên 1 Điều trong Đ1–62.
- `out_of_scope`: vấn đề chính do văn bản khác quyết định (Luật BHXH, BLLĐ, Nghị định, QCVN...).
- `multi_intent`: cần từ 2 Điều thuộc 2 lớp khác nhau trở lên mới trả lời được.

Cột "Gợi ý" là ý kiến của Claude sau khi đọc câu hỏi và Điều luật, **chưa đọc toàn văn câu trả lời gốc**. Nhóm quyết định cuối.

## Tóm tắt

| Dòng | Nhãn hiện tại | Gợi ý | Nhóm |
|---|---|---|---|
| 9 | in_scope Đ45 (C7) | Giữ | |
| 30 | out_of_scope | Giữ | |
| 33 | out_of_scope | **Cân nhắc** in_scope Đ14 (C6) | |
| 45 | out_of_scope | Giữ | |
| 62 | in_scope Đ38 (C5) | Giữ | |
| 64 | in_scope Đ39 (C5) | **Cân nhắc** Đ38 (cùng C5, chỉ đổi Điều) | |
| 89 | out_of_scope | Giữ | |
| 97 | out_of_scope | Giữ | |
| 100 | out_of_scope | Giữ | |

Chỉ dòng 33 có thể đổi lớp (ảnh hưởng F1 câu thật). Dòng 64 nếu đổi chỉ ảnh hưởng số liệu tra cứu Điều.

## Chi tiết

### Dòng 9: in_scope Đ45 (C7 BAO_HIEM_TNLD)
- Câu hỏi: Luật BHXH 2024 quy định NLĐ bị tai nạn giao thông trên đường đi làm/về được hưởng chế độ ốm đau. Vậy trường hợp này có được hưởng chế độ tai nạn lao động theo Luật ATVSLĐ 2015 không?
- Lý do gpt-6-sol: hỏi điều kiện hưởng bảo hiểm TNLĐ theo Điều 45.
- Đ45.1.c: "Trên tuyến đường đi từ nơi ở đến nơi làm việc hoặc từ nơi làm việc về nơi ở trong khoảng thời gian và tuyến đường hợp lý" là một trường hợp được hưởng chế độ TNLĐ.
- Gợi ý: **giữ**. Câu hỏi nêu tên Luật ATVSLĐ và đúng điều kiện ở Đ45.1.c.
- Link: https://chinhsachonline.chinhphu.vn/co-duoc-huong-dong-thoi-che-do-om-dau-va-tai-nan-lao-dong-82557.htm

### Dòng 30: out_of_scope
- Câu hỏi: lao động nữ điều trị vô sinh (IVF), sảy thai, nghỉ ốm, chấm dứt HĐLĐ... có đủ điều kiện hưởng chế độ thai sản không, hồ sơ nộp ở đâu?
- Lý do gpt-6-sol: chế độ BHXH; câu trả lời viện dẫn khoản 5 Điều 50 Luật BHXH 2024.
- Gợi ý: **giữ**. Thai sản không thuộc Luật ATVSLĐ.
- Link: https://chinhsachonline.chinhphu.vn/che-do-thai-san-voi-lao-dong-nu-dieu-tri-vo-sinh-84863.htm

### Dòng 33: out_of_scope (cân nhắc in_scope Đ14)
- Câu hỏi (rút gọn): QCVN 03:2011/BLĐTBXH yêu cầu người hàn điện phải có chứng chỉ, được huấn luyện ATLĐ và cấp thẻ an toàn. Công ty chủ yếu hàn điện trở (bấm nút), hàn mạch tự động. Doanh nghiệp có được tự đào tạo NLĐ vận hành thiết bị này không?
- Lý do gpt-6-sol: hỏi chứng chỉ chuyên môn theo quy chuẩn kỹ thuật, không phải huấn luyện chung Điều 14. Câu trả lời viện dẫn điểm 3.4.2.1 QCVN 03:2011.
- Đ14.2: "Người sử dụng lao động tổ chức huấn luyện cho người lao động làm công việc có yêu cầu nghiêm ngặt về an toàn, vệ sinh lao động và cấp thẻ an toàn trước khi bố trí làm công việc này."
- Gợi ý: **cân nhắc**. Nếu câu trả lời gốc chỉ dựa trên QCVN (chứng chỉ nghề) thì giữ out_of_scope. Nếu câu trả lời có nhắc huấn luyện và thẻ an toàn theo Đ14 thì đổi thành `in_scope`, `article_id: 14`.
- Link: https://chinhsachonline.chinhphu.vn/doanh-nghiep-co-duoc-tu-dao-tao-nguoi-lao-dong-van-hanh-thiet-bi-80660.htm

### Dòng 45: out_of_scope
- Câu hỏi: NLĐ ký HĐLĐ ở 2 nơi, nơi thứ 2 có phải trả thêm vào lương khoản tương đương mức đóng BHXH, BHYT, BHTN không?
- Lý do gpt-6-sol: thuộc BLLĐ và các luật bảo hiểm; câu trả lời viện dẫn khoản 4 Điều 85 Luật BHXH 2014.
- Gợi ý: **giữ**. Lưu ý Đ43 Luật ATVSLĐ (đóng BH TNLĐ khi có nhiều HĐLĐ) liên quan, nhưng câu hỏi hỏi BHXH, BHYT, BHTN chứ không hỏi BH TNLĐ.
- Link: https://chinhsachonline.chinhphu.vn/ky-nhieu-hop-dong-lao-dong-dong-bhxh-the-nao-68894.htm

### Dòng 62: in_scope Đ38 (C5 CHE_DO_BOI_THUONG)
- Câu hỏi: đang làm tại công ty thì bị xe tải của khách hàng đâm, suy giảm 45%. Công ty nói không phải lỗi NSDLĐ nên chỉ trợ cấp, không bồi thường. Đúng không?
- Lý do gpt-6-sol: trách nhiệm bồi thường theo Điều 38.
- Đ38.4: bồi thường cho NLĐ bị TNLĐ "mà không hoàn toàn do lỗi của chính người này gây ra". Đ38.5: trợ cấp khi do lỗi của chính NLĐ.
- Gợi ý: **giữ**. Tai nạn do người khác gây ra, không phải lỗi NLĐ, nên thuộc Đ38.4 (bồi thường), không phải 38.5.
- Link: https://chinhsachonline.chinhphu.vn/can-cu-bien-ban-dieu-tra-tai-nan-lao-dong-de-duoc-boi-thuong-22271.htm

### Dòng 64: in_scope Đ39 (cân nhắc Đ38, cùng lớp C5)
- Câu hỏi: theo khoản 2 Điều 39, NLĐ bị tai nạn trên đường đi làm được NSDLĐ trợ cấp. Trường hợp này NSDLĐ có bắt buộc trả chi phí y tế, tiền lương trong thời gian điều trị không?
- Lý do gpt-6-sol: trường hợp Điều 39.2.
- Đ39.2 chỉ nói trợ cấp theo khoản 5 Điều 38. Chi phí y tế và tiền lương điều trị nằm ở Đ38.2 và Đ38.3.
- Gợi ý: **cân nhắc**. Câu hỏi nhắc Đ39 nhưng điều đang hỏi (chi phí y tế, lương) nằm ở Đ38. Đọc câu trả lời gốc: nếu kết luận dựa trên Đ38.2, 38.3 thì đổi `article_id: 38`. Lớp không đổi (cả hai thuộc C5).
- Link: https://chinhsachonline.chinhphu.vn/co-bat-buoc-dn-tra-phi-dieu-tri-khi-nguoi-lao-dong-bi-tai-nan-21653.htm

### Dòng 89: out_of_scope
- Câu hỏi: chế độ làm việc với lao động nữ làm công việc nặng nhọc, độc hại khi mang thai và nuôi con dưới 12 tháng (khoản 2, khoản 4 Điều 137 BLLĐ 2019).
- Lý do gpt-6-sol: thuộc BLLĐ; câu trả lời viện dẫn Điều 137 BLLĐ.
- Gợi ý: **giữ**.
- Link: https://chinhsachonline.chinhphu.vn/che-do-lam-viec-doi-voi-lao-dong-nu-nuoi-con-duoi-12-thang-tuoi-84178.htm

### Dòng 97: out_of_scope
- Câu hỏi: giáo viên suy giảm khả năng lao động xin nghỉ hưu sớm, cách tính lương hưu?
- Lý do gpt-6-sol: hưu trí theo Luật BHXH; câu trả lời viện dẫn khoản 1 Điều 65 Luật BHXH.
- Gợi ý: **giữ**.
- Link: https://chinhsachonline.chinhphu.vn/nghi-do-suy-giam-kha-nang-lao-dong-luong-huu-tinh-the-nao-80538.htm

### Dòng 100: out_of_scope
- Câu hỏi: đang đi học nghề nặng nhọc, độc hại, có lương và đóng BHXH, có được miễn giảm học phí không?
- Lý do gpt-6-sol: pháp luật giáo dục; câu trả lời viện dẫn khoản 5 Điều 20 Nghị định 81/2021.
- Gợi ý: **giữ**.
- Link: https://chinhsachonline.chinhphu.vn/van-huong-luong-khi-di-hoc-co-duoc-mien-giam-hoc-phi-78595.htm

## Sau khi review

1. Sửa `decision` / `article_id` của dòng tương ứng trong `data/raw/real_labeled.jsonl` (giữ nguyên các trường khác).
2. Chạy:
   ```bash
   .venv/bin/python -m scripts.build_real_test
   .venv/bin/python -m scripts.build_notebook
   .venv/bin/jupyter nbconvert --to notebook --execute --inplace notebooks/uit_ohs_law_retrieval.ipynb --ExecutePreprocessor.timeout=1800
   .venv/bin/python -m scripts.build_report && .venv/bin/python -m scripts.build_slides
   ```
3. Không cần ghi tay vào báo cáo: việc kiểm chứng nhãn nay làm bằng gán nhãn mù (`docs/team-todo.md` mục A.1), báo cáo tự lấy số từ `reports/agreement.json`. File này chỉ là ghi chú tham khảo khi thảo luận các dòng chưa chắc (tập thật đã mở rộng lên 176 dòng, các dòng mới chưa chắc: 124, 130–133, 138, 141, 145, 174, 175).
