# Hướng dẫn gán nhãn (Labeling Guidelines) – K = 8 lớp

> Nguồn điều luật: `data/ohs_law_articles.json` (VBHN 14/VBHN-VPQH 2024). Mapping Điều -> lớp: `LABELS` trong `src/config.py` (nguồn duy nhất).
> Trạng thái: **v2, đã qua review chéo (gpt-6-sol, 2026-09-28)**. Sau khi chốt, mọi thay đổi phải gán lại nhãn toàn bộ dataset.

## 1. Nguyên tắc cốt lõi: gán theo Điều, lớp suy ra từ Điều

Người gán nhãn **chỉ chọn `article_id`**: Điều luật trả lời trực tiếp nhất cho câu hỏi. `label_id` **không gán tay**, luôn là `ARTICLE_TO_LABEL[article_id]`.

Lý do: retrieval chỉ tìm Điều trong lớp được dự đoán (`project-analysis.md` mục 7). Nếu lớp và Điều đích khác lớp nhau (vd gán C3 nhưng câu trả lời nằm ở Đ12 thuộc C0), retrieval không bao giờ tìm đúng. Gán theo Điều bảo đảm bất biến `label_id == ARTICLE_TO_LABEL[article_id]` bằng cấu trúc, không phụ thuộc người gán nhãn.

| Trường | Người gán nhãn điền? | Ý nghĩa |
|---|:---:|---|
| `article_id` | có | Điều trả lời trực tiếp nhất (Đ1–62) |
| `article_clause` | không bắt buộc | Khoản cụ thể nếu xác định được, vd `"12.7"`. Dùng cho Error Analysis |
| `label_id`, `label_code` | **không** | Sinh tự động từ `article_id` |
| `asks_penalty` | có | `true` nếu câu hỏi hỏi mức phạt (xem R4) |
| `seed_id`, `source` | có | Xem `project-analysis.md` mục 3.2 |

## 2. Bảng lớp (nội dung chính của các Điều)

| ID | Mã | Điều | Nội dung chính |
|:---:|---|---|---|
| 0 | `QUY_DINH_CHUNG` | 1–12 | Phạm vi, đối tượng, giải thích từ ngữ, chính sách, nguyên tắc; quyền/nghĩa vụ tổng quát của NLĐ (Đ6) và NSDLĐ (Đ7); vai trò Mặt trận, công đoàn, Hội nông dân; **các hành vi bị nghiêm cấm (Đ12)** |
| 1 | `BIEN_PHAP_PHONG_NGUA` | 13, 15–20, 22, 25, 28–33 | Thông tin, tuyên truyền (Đ13); nội quy, trách nhiệm bảo đảm nơi làm việc của NSDLĐ/NLĐ (Đ15–17); kiểm soát yếu tố nguy hiểm, có hại (Đ18); xử lý sự cố, ứng cứu khẩn cấp (Đ19); cải thiện điều kiện (Đ20); nghề nặng nhọc độc hại (Đ22); thời gian tiếp xúc yếu tố có hại (Đ25); máy, thiết bị nghiêm ngặt, kiểm định (Đ28–33) |
| 2 | `PHUONG_TIEN_BAO_HO` | 23 | Phương tiện bảo vệ cá nhân: ai được trang cấp, nguyên tắc trang cấp, nghĩa vụ sử dụng |
| 3 | `SUC_KHOE_BOI_DUONG` | 21, 24, 26, 27 | Khám sức khỏe, khám phát hiện & điều trị bệnh nghề nghiệp (Đ21); bồi dưỡng bằng hiện vật (Đ24); điều dưỡng phục hồi sức khỏe hằng năm (Đ26); quản lý hồ sơ sức khỏe (Đ27) |
| 4 | `KHAI_BAO_DIEU_TRA` | 34–37 | Khai báo; điều tra, đoàn điều tra, thời hạn điều tra; thống kê, báo cáo tai nạn, sự cố, bệnh nghề nghiệp |
| 5 | `CHE_DO_BOI_THUONG` | 38–40 | Trách nhiệm **của NSDLĐ**: sơ cứu, tạm ứng & thanh toán chi phí y tế, trả lương khi nghỉ điều trị, bồi thường/trợ cấp tính theo tháng tiền lương, thời hạn 05 ngày (Đ38); trường hợp đặc thù, NSDLĐ không đóng BH (Đ39); không được hưởng từ NSDLĐ (Đ40) |
| 6 | `HUAN_LUYEN_ATLD` | 14 | Huấn luyện ATVSLĐ: đối tượng phải huấn luyện, NSDLĐ tổ chức huấn luyện, thẻ an toàn, chứng chỉ, tổ chức hoạt động huấn luyện (Đ14 không ghi thời hạn cụ thể) |
| 7 | `BAO_HIEM_TNLD` | 41–62 | Quỹ BH TNLĐ-BNN: nguyên tắc, sử dụng quỹ, đối tượng, mức đóng; điều kiện hưởng; giám định mức suy giảm khả năng lao động (Đ47, 62); trợ cấp một lần/hằng tháng theo mức lương cơ sở; trợ cấp phục vụ, tử tuất; dưỡng sức sau điều trị (Đ54); chuyển đổi nghề; hỗ trợ phòng ngừa (Đ56); hồ sơ & giải quyết hưởng chế độ |

Lưu ý: một Điều có thể chứa khoản thuộc chủ đề khác (vd Đ16.3 nhắc bảo hộ, Đ16.7 nhắc huấn luyện, Đ38.9 nhắc hồ sơ BH, Đ56.2 nhắc huấn luyện). Không sao: áp R2 để chọn Điều, lớp đi theo Điều.

## 3. Quy tắc chọn Điều (áp dụng theo thứ tự)

- **R1. Hỏi gì chọn nấy.** Dựa trên mệnh đề hỏi, không dựa trên bối cảnh. "Công nhân ngã giàn giáo, *công ty phải khai báo cho ai*?" -> Đ34 (C4).
- **R2. Điều chuyên biệt thắng Điều liệt kê.** Nếu Điều liệt kê chung (Đ6, Đ7, Đ16, Đ17) và một Điều chuyên biệt cùng trả lời, chọn Điều chuyên biệt. "Công ty không cấp đồ bảo hộ" -> Đ23 (C2), không phải Đ16.3. "NLĐ có phải đi huấn luyện trước khi vận hành máy?" -> Đ14 (C6), không phải Đ17.3.
- **R3. Hỏi "có bị cấm / có được phép không" về một hành vi nêu tại Đ12 -> Đ12 (C0).** Đ12 là nơi duy nhất nói trực tiếp hành vi đó bị cấm.
  - "Công ty trả tiền thay bồi dưỡng hiện vật có được không?" -> Đ12 (khoản 7).
  - "Chưa huấn luyện mà cho vận hành máy có bị cấm không?" -> Đ12 (khoản 6).
  - Ngược lại, hỏi **nội dung chế độ / cách thực hiện** -> Điều chuyên biệt: "Bồi dưỡng hiện vật gồm những gì, ai được hưởng?" -> Đ24 (C3). "Công ty phải huấn luyện những ai?" -> Đ14 (C6).
- **R4. Câu hỏi mức phạt:** chọn Điều quy định **nghĩa vụ bị vi phạm** và đặt `asks_penalty=true`. Luật không chứa số tiền phạt (Đ90 chỉ nêu nguyên tắc xử lý), nên demo chỉ hiển thị mức phạt khi `data/penalties.json` có mục cho Điều đó, có trích dẫn nghị định và đã kiểm tra hiệu lực. Nếu không có, demo ghi "chưa có dữ liệu mức phạt". Không để cosine similarity trên văn bản Luật "trả lời" con số.
- **R5. Câu hỏi nhiều ý** (cần ≥ 2 Điều khác nhau để trả lời, vd "khai báo cho ai **và** bồi thường bao nhiêu?" cần Đ34 + Đ38): **không đưa vào tập train/val/test chính.** Ghi vào `data/raw/multi_intent.csv` với danh sách `article_ids`. Tập này dùng cho phần Error Analysis/Hướng phát triển (multi-label). Không tách thành 2 mẫu cùng câu chữ khác nhãn (tạo nhãn mâu thuẫn cho cùng một input).
- **R6. Ngoài phạm vi** (câu trả lời nằm ở Đ63–93 hoặc ngoài Luật): không gán nhãn 0–7. Ghi vào `data/raw/out_of_scope.csv` (xem mục 5).
- **R7. Không xác định được sau R1–R6:** loại, ghi vào `data/raw/rejected.csv` kèm lý do. Không đoán.

## 4. Cặp lớp dễ nhầm

Mỗi dòng: tín hiệu trong câu hỏi -> Điều đích (lớp).

### C5 vs C7: ai chi trả, theo cơ chế nào
| Câu hỏi | Điều (lớp) |
|---|---|
| Công ty có phải trả viện phí, tạm ứng tiền cấp cứu, trả lương khi nghỉ điều trị? Công ty bồi thường bao nhiêu tháng lương? | Đ38 (C5) |
| Tai nạn trên đường đi làm do người khác gây ra, công ty có phải trả gì? | Đ39 (C5) |
| **Công ty không/chưa đóng BH TNLĐ** thì ai trả trợ cấp cho tôi? | Đ39 (C5), dù câu nhắc "bảo hiểm", "hằng tháng" |
| Say rượu, tự gây thương tích có được **công ty** bồi thường? | Đ40 (C5) |
| Điều kiện để **được bảo hiểm/quỹ** chi trả chế độ TNLĐ (kể cả tai nạn trên đường đi làm)? | Đ45 (C7) |
| Mức trợ cấp một lần/hằng tháng của **bảo hiểm**, giám định suy giảm bao nhiêu % thì được hưởng? | Đ47–49 (C7) |
| Mức đóng BH TNLĐ, ai phải đóng? | Đ43, 44 (C7) |
| Hồ sơ hưởng chế độ TNLĐ gồm gì, nộp ở đâu? | Đ57 (C7) |
| **Chung chung**: "Bị tai nạn lao động được hưởng chế độ gì?" | Đ38 (C5): trách nhiệm đầu tiên; Đ38.9 dẫn sang Mục 3 |

### C4 vs C5: thủ tục hay tiền
- Khai báo, điều tra, biên bản, đoàn điều tra, **thời hạn điều tra** -> Đ34/35 (C4).
- Chi phí, bồi thường, **thời hạn trả bồi thường (05 ngày)** -> Đ38 (C5).
- "Sau tai nạn bao lâu công ty phải giải quyết?" không rõ điều tra hay trả tiền -> R7.
- "Sơ cứu": hỏi **tổ chức ứng cứu, hành động** -> Đ19 (C1); hỏi **ai trả tiền sơ cứu/cấp cứu** -> Đ38 (C5).

### C1 vs C4: xử lý sự cố hay khai báo sự cố
- Báo cáo **để huy động, điều phối ứng cứu**, sơ tán, dừng máy, kế hoạch ứng cứu -> Đ19 (C1).
- Khai báo vụ việc theo thủ tục (báo cơ quan lao động, công an, thời hạn khai báo) -> Đ34 (C4).
- "Báo cho ai" không rõ mục đích -> R7.

### C1 vs C3: môi trường/phân loại nghề hay chăm sóc con người
- Danh mục, phân loại nghề nặng nhọc độc hại -> Đ22 (C1). Quan trắc, yếu tố có hại nơi làm việc -> Đ18 (C1). Thời gian tiếp xúc yếu tố có hại -> Đ25 (C1); lưu ý Đ25 không có số giờ cụ thể (dẫn sang pháp luật lao động).
- Khám sức khỏe, khám/điều trị bệnh nghề nghiệp -> Đ21 (C3). Bồi dưỡng hiện vật -> Đ24 (C3).
- "Làm nghề độc hại có được chăm sóc sức khỏe gì?" không nêu hành động cụ thể -> R7.

### C3 vs C7: sức khỏe, bệnh nghề nghiệp
- Khám phát hiện, điều trị BNN, **công ty trả chi phí khám** -> Đ21 (C3).
- **Điều dưỡng phục hồi sức khỏe hằng năm** do công ty tổ chức (nghề độc hại, sức khỏe kém) -> Đ26 (C3).
- **Nghỉ dưỡng sức sau khi điều trị** TNLĐ/BNN (5–10 ngày, tiền theo mức lương cơ sở) -> Đ54 (C7).
- Điều kiện hưởng chế độ BNN -> Đ46 (C7). Giám định mức suy giảm -> Đ47/62 (C7).
- Thống kê, báo cáo BNN -> Đ37 (C4).

### C1 vs C6: tuyên truyền hay huấn luyện
- Thông tin, tuyên truyền, biển cảnh báo, bảng chỉ dẫn -> Đ13 hoặc Đ16 (C1).
- Khóa huấn luyện, thẻ an toàn, chứng chỉ, huấn luyện trước khi bố trí công việc nghiêm ngặt -> Đ14 (C6) (R2 thắng Đ16.7, Đ17.3).
- Hỏi cả hai -> R5.

### C0 vs lớp cụ thể
- C0 chỉ khi: định nghĩa (Đ3), phạm vi/đối tượng (Đ1–2), chính sách/nguyên tắc (Đ4–5), quyền/nghĩa vụ tổng quát không có Điều chuyên biệt (vd quyền từ chối làm việc nguy hiểm Đ6.1.đ), vai trò tổ chức (Đ8–11), hoặc R3 (hỏi có bị cấm).
- Các khoản Đ12 chạm lớp khác: 12.2 (trốn đóng BH, chạm C7), 12.3 (máy chưa kiểm định, chạm C1), 12.6 (chưa huấn luyện, chạm C6), 12.7 (tiền thay hiện vật, chạm C3). Áp R3 để quyết.

## 5. Tập ngoài phạm vi (OOD)

- Thu ~50–100 câu có câu trả lời ở Đ63–93 (lao động nữ/cao tuổi/thuê lại, bộ phận ATVSLĐ, kế hoạch ATVSLĐ, thanh tra...) và câu ngoài Luật. Lưu ý các cặp dễ lẫn vào trong phạm vi: Đ78 (kế hoạch ứng cứu) vs Đ19, Đ81 (thống kê ATVSLĐ) vs Đ36–37.
- **Không train** trên tập này. Chỉ dùng để chọn và đánh giá ngưỡng độ tự tin của demo (tỷ lệ OOD bị từ chối vs tỷ lệ câu trong phạm vi bị từ chối nhầm). Ngưỡng chỉ có ý nghĩa sau khi đo trên tập này; LinearSVC không có xác suất sẵn, cần `CalibratedClassifierCV` hoặc dùng LogReg cho điểm tin cậy.

## 6. Quy trình đảm bảo chất lượng nhãn

1. **Adjudication:** hai người gán `article_id` độc lập trên **10% mẫu**, lấy mẫu có chủ đích để phủ đủ các cặp ở mục 4 (không chỉ ngẫu nhiên), `random_state=42`. Tính **Cohen's kappa** trên `label_id` (suy ra) và tỷ lệ trùng `article_id`. Mục tiêu κ ≥ 0.8; thấp hơn thì bổ sung ví dụ vào mục 4 và gán lại.
2. **Augmentation:** câu `augmented` kế thừa `article_id` của seed. Reviewer kiểm tra paraphrase **không đổi chủ thể chi trả hoặc mục đích hỏi** (vd "công ty trả" thành "bảo hiểm trả" là đổi Điều, loại câu đó).
3. **Kiểm tra tự động** khi build dataset: `label_id == ARTICLE_TO_LABEL[article_id]`, `article_id ∈ [1, 62]`, mọi `seed_id` của câu augmented tồn tại trong tập seed.
4. Báo cáo trong EDA: số câu bị loại theo R5/R6/R7, số câu `asks_penalty`.
