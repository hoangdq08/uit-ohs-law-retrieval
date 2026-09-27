# Mẫu 40 câu gốc synthetic để nhóm đọc kiểm tra

Mỗi lớp 5 câu gốc chọn ngẫu nhiên (seed 42), chỉ hiện văn phong `neutral` (4 văn phong kia là paraphrase cùng ý, cùng Điều).
Đánh dấu cột **OK?**: `ok` nếu Điều trả lời trực tiếp câu hỏi, `sai` nếu không (ghi Điều đúng hoặc lý do vào Ghi chú).
Tra Điều: `data/ohs_law_articles.json` hoặc https://luatvietnam.vn (VBHN 14/VBHN-VPQH 2024).

## C0 QUY_DINH_CHUNG: Quy định chung, quyền và nghĩa vụ

| seed_id | Câu hỏi | Điều gán | OK? | Ghi chú |
|---|---|---|---|---|
| c0-002 | Người đang thử việc có thuộc đối tượng áp dụng của Luật An toàn, vệ sinh lao động không? | Đ2 Đối tượng áp dụng | | |
| c0-008 | Yếu tố có hại theo Luật An toàn, vệ sinh lao động được hiểu thế nào? | Đ3 Giải thích từ ngữ | | |
| c0-015 | Trong bảo đảm an toàn, vệ sinh lao động, biện pháp nào được ưu tiên theo nguyên tắc của luật? | Đ5 Nguyên tắc bảo đảm an toàn, vệ sinh lao động | | |
| c0-016 | Người lao động có quyền từ chối làm công việc có nguy cơ tai nạn đe dọa tính mạng mà vẫn được trả đủ lương không? | Đ6 Quyền và nghĩa vụ về an toàn, vệ sinh lao động của người lao động | | |
| c0-018 | Sau khi điều trị ổn định tai nạn lao động, người lao động có quyền yêu cầu công ty bố trí công việc phù hợp không? | Đ6 Quyền và nghĩa vụ về an toàn, vệ sinh lao động của người lao động | | |

## C1 BIEN_PHAP_PHONG_NGUA: Biện pháp phòng ngừa, cải thiện điều kiện làm việc

| seed_id | Câu hỏi | Điều gán | OK? | Ghi chú |
|---|---|---|---|---|
| c1-006 | Nơi làm việc phải đạt những yêu cầu gì về bụi, tiếng ồn, độ thoáng? | Đ16 Trách nhiệm của người sử dụng lao động trong việc bảo đảm an toàn, vệ sinh lao động tại nơi làm việc | | |
| c1-007 | Công ty có phải bố trí đủ buồng tắm, buồng vệ sinh tại nơi làm việc không? | Đ16 Trách nhiệm của người sử dụng lao động trong việc bảo đảm an toàn, vệ sinh lao động tại nơi làm việc | | |
| c1-009 | Công ty có phải định kỳ kiểm tra, bảo dưỡng máy móc, nhà xưởng, kho tàng không? | Đ16 Trách nhiệm của người sử dụng lao động trong việc bảo đảm an toàn, vệ sinh lao động tại nơi làm việc | | |
| c1-035 | Trong quá trình sử dụng thiết bị nghiêm ngặt, tổ chức, cá nhân phải lập và lưu giữ hồ sơ gì? | Đ30 Sử dụng máy, thiết bị, vật tư, chất có yêu cầu nghiêm ngặt về an toàn, vệ sinh lao động | | |
| c1-038 | Việc kiểm định máy, thiết bị có yêu cầu nghiêm ngặt phải bảo đảm những yêu cầu gì? | Đ31 Kiểm định máy, thiết bị, vật tư có yêu cầu nghiêm ngặt về an toàn lao động | | |

## C2 PHUONG_TIEN_BAO_HO: Phương tiện bảo vệ cá nhân

| seed_id | Câu hỏi | Điều gán | OK? | Ghi chú |
|---|---|---|---|---|
| c2-002 | Công ty có bắt buộc phải cấp đồ bảo hộ lao động cho công nhân làm việc có yếu tố nguy hiểm không? | Đ23 Phương tiện bảo vệ cá nhân trong lao động | | |
| c2-003 | Người lao động có bắt buộc phải sử dụng phương tiện bảo vệ cá nhân đã được cấp trong khi làm việc không? | Đ23 Phương tiện bảo vệ cá nhân trong lao động | | |
| c2-006 | Công ty có được buộc người lao động tự mua phương tiện bảo vệ cá nhân không? | Đ23 Phương tiện bảo vệ cá nhân trong lao động | | |
| c2-014 | Cơ quan nào quy định chế độ trang cấp phương tiện bảo vệ cá nhân trong lao động? | Đ23 Phương tiện bảo vệ cá nhân trong lao động | | |
| c2-028 | Người lao động làm việc với điện có được cấp găng tay, ủng cách điện không? | Đ23 Phương tiện bảo vệ cá nhân trong lao động | | |

## C3 SUC_KHOE_BOI_DUONG: Khám sức khỏe, bệnh nghề nghiệp, bồi dưỡng hiện vật

| seed_id | Câu hỏi | Điều gán | OK? | Ghi chú |
|---|---|---|---|---|
| c3-002 | Người làm nghề nặng nhọc, độc hại, nguy hiểm được khám sức khỏe bao lâu một lần? | Đ21 Khám sức khỏe và điều trị bệnh nghề nghiệp cho người lao động | | |
| c3-015 | Công ty có trách nhiệm tổ chức khám sức khỏe cho người lao động hằng năm không? | Đ21 Khám sức khỏe và điều trị bệnh nghề nghiệp cho người lao động | | |
| c3-033 | Công ty có phải lập hồ sơ sức khỏe riêng cho người bị bệnh nghề nghiệp không? | Đ27 Quản lý sức khỏe người lao động | | |
| c3-036 | Công ty có phải báo cáo việc quản lý sức khỏe người lao động cho cơ quan y tế không? | Đ27 Quản lý sức khỏe người lao động | | |
| c3-039 | Công ty có phải lưu giữ kết quả khám sức khỏe của người lao động trong hồ sơ không? | Đ27 Quản lý sức khỏe người lao động | | |

## C4 KHAI_BAO_DIEU_TRA: Khai báo, điều tra, thống kê tai nạn/sự cố

| seed_id | Câu hỏi | Điều gán | OK? | Ghi chú |
|---|---|---|---|---|
| c4-013 | Ai có trách nhiệm thành lập Đoàn điều tra tai nạn lao động cấp cơ sở? | Đ35 Điều tra vụ tai nạn lao động, sự cố kỹ thuật gây mất an toàn, vệ sinh lao động, sự cố kỹ thuật gây mất an toàn, vệ sinh lao động nghiêm trọng | | |
| c4-015 | Tai nạn lao động chết người do cơ quan nào điều tra? | Đ35 Điều tra vụ tai nạn lao động, sự cố kỹ thuật gây mất an toàn, vệ sinh lao động, sự cố kỹ thuật gây mất an toàn, vệ sinh lao động nghiêm trọng | | |
| c4-027 | Biên bản điều tra tai nạn lao động phải được gửi đến những ai? | Đ35 Điều tra vụ tai nạn lao động, sự cố kỹ thuật gây mất an toàn, vệ sinh lao động, sự cố kỹ thuật gây mất an toàn, vệ sinh lao động nghiêm trọng | | |
| c4-029 | Người làm việc không theo hợp đồng lao động bị tai nạn làm bị thương nặng thì ai lập biên bản ghi nhận sự việc? | Đ35 Điều tra vụ tai nạn lao động, sự cố kỹ thuật gây mất an toàn, vệ sinh lao động, sự cố kỹ thuật gây mất an toàn, vệ sinh lao động nghiêm trọng | | |
| c4-035 | Cơ quan nào xây dựng và quản lý cơ sở dữ liệu về an toàn lao động trên phạm vi cả nước? | Đ36 Thống kê, báo cáo tai nạn lao động, sự cố kỹ thuật gây mất an toàn, vệ sinh lao động nghiêm trọng | | |

## C5 CHE_DO_BOI_THUONG: Bồi thường, trợ cấp tai nạn lao động

| seed_id | Câu hỏi | Điều gán | OK? | Ghi chú |
|---|---|---|---|---|
| c5-001 | Khi người lao động bị tai nạn lao động, ai phải tạm ứng chi phí sơ cứu, cấp cứu? | Đ38 Trách nhiệm của người sử dụng lao động đối với người lao động bị tai nạn lao động, bệnh nghề nghiệp | | |
| c5-011 | Người lao động bị tai nạn lao động do lỗi của chính mình thì có được công ty trợ cấp không? | Đ38 Trách nhiệm của người sử dụng lao động đối với người lao động bị tai nạn lao động, bệnh nghề nghiệp | | |
| c5-018 | Tiền lương làm căn cứ tính bồi thường tai nạn lao động gồm những khoản nào? | Đ38 Trách nhiệm của người sử dụng lao động đối với người lao động bị tai nạn lao động, bệnh nghề nghiệp | | |
| c5-028 | Tai nạn trên đường đi làm về mà không xác định được người gây ra thì công ty có phải trợ cấp cho người lao động không? | Đ39 Trách nhiệm của người sử dụng lao động về bồi thường, trợ cấp trong những trường hợp đặc thù khi người lao động bị tai nạn lao động | | |
| c5-038 | Người lao động bị tai nạn do sử dụng ma túy thì có được công ty bồi thường không? | Đ40 Trường hợp người lao động không được hưởng chế độ từ người sử dụng lao động khi bị tai nạn lao động | | |

## C6 HUAN_LUYEN_ATLD: Huấn luyện an toàn, vệ sinh lao động

| seed_id | Câu hỏi | Điều gán | OK? | Ghi chú |
|---|---|---|---|---|
| c6-007 | Người lao động làm công việc có yêu cầu nghiêm ngặt về an toàn có phải được huấn luyện trước khi làm không? | Đ14 Huấn luyện an toàn, vệ sinh lao động | | |
| c6-010 | Công nhân vận hành xe nâng có phải học huấn luyện và có thẻ an toàn không? | Đ14 Huấn luyện an toàn, vệ sinh lao động | | |
| c6-014 | Người lao động làm việc không theo hợp đồng lao động có phải được huấn luyện an toàn không? | Đ14 Huấn luyện an toàn, vệ sinh lao động | | |
| c6-018 | Người lao động mới tuyển dụng có phải được huấn luyện an toàn trước khi bố trí làm việc không? | Đ14 Huấn luyện an toàn, vệ sinh lao động | | |
| c6-022 | Nhân viên văn phòng có phải được huấn luyện an toàn, vệ sinh lao động không? | Đ14 Huấn luyện an toàn, vệ sinh lao động | | |

## C7 BAO_HIEM_TNLD: Bảo hiểm tai nạn lao động, bệnh nghề nghiệp (Quỹ BHXH chi trả)

| seed_id | Câu hỏi | Điều gán | OK? | Ghi chú |
|---|---|---|---|---|
| c7-006 | Quỹ bảo hiểm tai nạn lao động, bệnh nghề nghiệp được hình thành từ những nguồn nào? | Đ44 Mức đóng, nguồn hình thành Quỹ bảo hiểm tai nạn lao động, bệnh nghề nghiệp | | |
| c7-007 | Người lao động cần đáp ứng điều kiện gì để được hưởng chế độ tai nạn lao động từ quỹ bảo hiểm? | Đ45 Điều kiện hưởng chế độ tai nạn lao động | | |
| c7-023 | Thời điểm hưởng trợ cấp tai nạn lao động từ bảo hiểm được tính từ khi nào? | Đ50 Thời điểm hưởng trợ cấp | | |
| c7-025 | Người lao động bị suy giảm khả năng lao động từ 81% trở lên bị liệt cột sống có được hưởng trợ cấp phục vụ không? | Đ52 Trợ cấp phục vụ | | |
| c7-039 | Cơ quan bảo hiểm giải quyết chế độ tai nạn lao động chậm so với thời hạn thì phải chịu trách nhiệm gì? | Đ61 Giải quyết hưởng chế độ bảo hiểm tai nạn lao động, bệnh nghề nghiệp chậm so với thời hạn quy định | | |

## Kết quả

- Số câu đã đọc: 40
- Số câu sai: 
- Đã sửa/loại: 

Sửa câu sai: sửa cả 5 dòng cùng `seed_id` trong `data/raw/gen/c{k}.jsonl` (hoặc báo lại để sinh câu thay), rồi chạy lại toàn bộ theo README.
