# Câu hỏi borderline, lớp 0-3 (dùng cho Error Analysis)

Mỗi dòng: câu hỏi -> Điều đã chọn (lớp). Lý do. Quy tắc tham chiếu: `docs/labeling-guidelines.md`.

## C0 QUY_DINH_CHUNG

1. "Công ty trả tiền thay cho bồi dưỡng bằng hiện vật có được không?" (c0-040) -> **Đ12 (C0)**. R3: hỏi "có được không" về hành vi nêu tại 12.7. Dễ bị kéo sang Đ24 (C3) vì trùng từ "bồi dưỡng hiện vật".
2. "Chậm đóng bảo hiểm TNLĐ có bị cấm?" (c0-036) -> **Đ12 (C0)**. R3, khoản 12.2. Nhiều từ vựng của C7 (bảo hiểm, đóng) nên model từ túi từ dễ dự đoán C7.
3. "Cho người lao động làm công việc có yêu cầu nghiêm ngặt về an toàn khi chưa được huấn luyện có bị cấm không?" (c0-039) -> **Đ12 (C0)**. R3, khoản 12.6. Cạnh tranh với Đ14 (C6) và Đ17.3 (C1).
4. "Người lao động có quyền từ chối làm công việc có nguy cơ tai nạn đe dọa tính mạng mà vẫn được trả đủ lương không?" (c0-016) -> **Đ6 (C0)**. Quyền tại 6.1.đ, không có Điều chuyên biệt. Đ7.2.c và Đ19.2.a cũng nói "không được buộc trở lại làm việc" nhưng từ phía NSDLĐ, câu này hỏi quyền của NLĐ.
5. "Công ty có quyền huy động người lao động tham gia ứng cứu khẩn cấp khi xảy ra sự cố không?" (c0-025) -> **Đ7 (C0)**. Quyền của NSDLĐ tại 7.1.d. Dễ nhầm với Đ19 (C1) vì chung ngữ cảnh ứng cứu khẩn cấp. Đ19 quy định trách nhiệm xử lý sự cố, không quy định quyền huy động NLĐ.

## C1 BIEN_PHAP_PHONG_NGUA

1. "Công ty có phải trang bị phương tiện kỹ thuật, y tế để sơ cứu kịp thời khi xảy ra tai nạn không?" (c1-019) -> **Đ19 (C1)**. Câu hỏi về chuẩn bị phương tiện ứng cứu (19.1), không phải ai trả chi phí sơ cứu (Đ38, C5). Mục 4 C4 vs C5: "sơ cứu".
2. "Sự cố kỹ thuật nghiêm trọng vượt quá khả năng ứng phó của cơ sở thì phải xử lý như thế nào?" (c1-021) -> **Đ19 (C1)**. Báo cáo cấp trên để huy động ứng cứu (19.2.c), không phải khai báo theo thủ tục (Đ34, C4). Cạnh tranh thêm với Đ78 (OOD).
3. "Công ty có trách nhiệm gì về thời gian tiếp xúc với yếu tố có hại của người lao động?" (c1-027) -> **Đ25 (C1)**. Nằm giữa khối Đ21-27 của C3 và chung từ vựng sức khỏe/độc hại. Đ25 không nêu số giờ cụ thể.
4. "Danh mục nghề, công việc nặng nhọc, độc hại, nguy hiểm do cơ quan nào ban hành?" (c1-024) -> **Đ22 (C1)**. Phân loại nghề thuộc C1 theo mục 4 C1 vs C3, dù câu hỏi dễ bị kéo sang C3 (khám SK 06 tháng, bồi dưỡng cho nghề độc hại).
5. "Khi đưa máy, thiết bị có yêu cầu nghiêm ngặt vào sử dụng hoặc thải bỏ thì có phải khai báo không?" (c1-034) -> **Đ30 (C1)**. Chữ "khai báo" ở đây là khai báo thiết bị (30.2), không phải khai báo tai nạn/sự cố (Đ34, C4).

## C2 PHUONG_TIEN_BAO_HO

1. "Công ty có được phát tiền thay cho việc trang cấp phương tiện bảo vệ cá nhân không?" (c2-005) -> **Đ23 (C2)**. Khác R3: "phát tiền thay PTBVCN" nằm ở 23.3.b, không có trong Đ12 (Đ12.7 chỉ nói bồi dưỡng hiện vật). Lỗi dễ gặp: gán Đ12 vì cấu trúc "trả tiền thay ... có được không" giống hệt c0-040.
2. "Ngoài việc cấp phương tiện bảo vệ cá nhân, công ty có phải áp dụng giải pháp kỹ thuật để hạn chế yếu tố nguy hiểm không?" (c2-013) -> **Đ23 (C2)**. Khoản 23.2. Nội dung trùng với Đ16.4, Đ18 (C1). Chọn Đ23 vì câu hỏi đặt giải pháp kỹ thuật trong quan hệ với việc cấp PTBVCN.
3. "Người lao động có bắt buộc phải sử dụng phương tiện bảo vệ cá nhân đã được cấp trong khi làm việc không?" (c2-003) -> **Đ23 (C2)**. R2: Đ23.1 chuyên biệt thắng Đ6.2.b và Đ17.2 (danh sách nghĩa vụ chung). Seed "NLĐ có phải bảo quản PTBVCN" đã bị loại khỏi C2 vì "bảo quản" chỉ có ở Đ6.2.b/Đ17.2, Đ23 không nói.
4. "Phương tiện bảo vệ cá nhân đã qua sử dụng ở nơi dễ nhiễm độc có phải được khử độc không?" (c2-012) -> **Đ23 (C2)**. Khoản 23.3.d. Dễ nhầm với Đ18.1 (C1), khoản này nói khử độc cho người lao động chứ không phải cho PTBVCN.
5. "Công ty có được thu lại tiền khi người lao động làm hỏng phương tiện bảo vệ cá nhân không?" (c2-035) -> **Đ23 (C2)**. Áp 23.3.b (không thu tiền của NLĐ để mua PTBVCN). Luật không nói rõ trường hợp NLĐ làm hỏng do lỗi. Nếu reviewer cho rằng câu này cần văn bản hướng dẫn (Thông tư) thì chuyển sang R7.

## C3 SUC_KHOE_BOI_DUONG

1. "Chi phí khám sức khỏe định kỳ cho người lao động do ai chi trả?" (c3-011) -> **Đ21 (C3)**. Khoản 21.6. Chữ "chi trả" dễ kéo sang C5 (Đ38) hoặc C7. Mục 4 C3 vs C7: công ty trả chi phí khám -> Đ21.
2. "Người lao động được chẩn đoán mắc bệnh nghề nghiệp có được công ty đưa đi điều trị không?" (c3-010) -> **Đ21 (C3)**. Khoản 21.5. Cạnh tranh với Đ38 (C5, thanh toán chi phí y tế cho người bị BNN) và Đ46 (C7). Câu hỏi về hành động đưa đi điều trị, không hỏi ai trả tiền.
3. "Người lao động đã được Hội đồng y khoa giám định có phải khám sức khỏe lại khi trở lại làm việc không?" (c3-016) -> **Đ21 (C3)**. Ngoại lệ tại 21.3. Có từ "giám định" và "Hội đồng y khoa" rất gần Đ47/62 (C7).
4. "Công ty có bắt buộc phải tổ chức điều dưỡng phục hồi sức khỏe cho người lao động không?" (c3-028) -> **Đ26 (C3)**. Đ26 chỉ "khuyến khích", không bắt buộc. Dễ nhầm với dưỡng sức sau điều trị Đ54 (C7) do chung từ "phục hồi sức khỏe".
5. "Công ty có phải sắp xếp công việc phù hợp với sức khỏe của người lao động không?" (c3-035) -> **Đ27 (C3)**. Khoản 27.1 (theo tiêu chuẩn sức khỏe và kết quả khám). Rất gần Đ6.1.d (C0, bố trí việc phù hợp sau TNLĐ/BNN). Phân biệt: căn cứ kết quả khám sức khỏe -> Đ27. Sau điều trị tai nạn -> Đ6.
