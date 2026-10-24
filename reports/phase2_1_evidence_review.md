# Báo Cáo Nghiệm Thu Tính Liêm Chính Bằng Chứng & Hoàn Tất Quyết Định Nguồn Dữ Liệu
*(Phase 2.1 — Evidence Integrity Review & Source Decision Finalization Report)*

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam (Used Car Price Prediction in Vietnam)
- **Giai đoạn**: Phase 2.1 — Evidence Integrity Review & Source Decision Finalization
- **Thời gian lập**: 19/10/2026, 00:35:00 (Múi giờ: Asia/Ho_Chi_Minh)
- **Người thực hiện**: Senior Data Scientist & Technical Reviewer
- **Môi trường thực thi**: Windows 11, Python `3.11.9`, pytest `9.1.1`
- **Mục đích**: Kiểm định độc lập toàn bộ các khẳng định kỹ thuật trong Phase 2, sửa đổi các nhận định chưa đủ bằng chứng, chuẩn hóa bảng đánh giá nguồn dữ liệu, và chuẩn bị tài liệu 5 câu hỏi quyết định gửi Mentor trước khi bước vào Phase 3.

---

## 1. Danh Mục Các Kết Luận Đã Hiệu Chỉnh (Corrected Conclusions)

Qua quá trình rà soát độc lập, 5 nhóm kết luận chưa chính xác hoặc thiếu bằng chứng đã được sửa đổi triệt để:

### A. Phân định rạch ròi giữa Unit Tests và Chất Lượng Dữ Liệu (Data Quality)
- **Trước khi sửa**: Bảng so sánh nguồn tại Phase 2 ghi nhận chất lượng dữ liệu của Oto.com.vn là *"Đo lường một phần (36 tests pass)"*.
- **Hiệu chỉnh**: 36 unit tests chỉ kiểm chứng logic xử lý của code Python trên các trường hợp kiểm thử giả lập (synthetic fixtures). Chất lượng dữ liệu thực tế (Missing Rate, Parse Error Rate trên tin thật, Duplicate Rate, khoảng phân tán của Target) chỉ có thể đo lường khi tiếp cận dữ liệu thật.
- **Trạng thái chuẩn hóa**: Chuyển toàn bộ các cột chất lượng dữ liệu chưa có file thực tế sang **`NOT MEASURED` (Chưa đo lường)**. Tuyệt đối không tự bịa đặt số liệu giả định.

### B. Xác định 4 điều kiện độc lập kích hoạt Pilot (Không thay thế lẫn nhau)
- **Trước khi sửa**: Tài liệu cũ ghi nhận điều kiện kích hoạt Nhánh A là *"Nextgen Vietnam chấp thuận HOẶC Mentor phê duyệt"*.
- **Hiệu chỉnh**: Việc Mentor phê duyệt phương pháp học tập **không thể thay thế về mặt pháp lý** cho quyền sở hữu trí tuệ của đơn vị vận hành website thương mại (Mục 10.1 Quy chế Oto.com.vn).
- **Trạng thái chuẩn hóa**: Xác lập 4 điều kiện độc lập bắt buộc: (1) Mentor duyệt phương pháp; (2) ToS nguồn phù hợp; (3) Đơn vị sở hữu chấp thuận khi ToS cấm; (4) Nhóm đáp ứng kỹ thuật an toàn (PII scrub, rate limit $\ge$ 3.0s).

### C. Hiệu chỉnh nhận định về Dataset Kaggle (Vietnam Automobile Dataset)
- **Trước khi sửa**: Coi nhãn `MIT License` trên Kaggle là giấy phép hợp lệ và tự suy đoán dataset *"chỉ dành cho học thuật cá nhân"*.
- **Hiệu chỉnh**: Phân định rạch ròi giữa nhãn do uploader tự chọn trên hosting Kaggle và quyền phát hành dữ liệu nguồn. Dữ liệu gốc xuất phát từ việc crawl web bên thứ ba nên quyền phân phối lại dưới dạng MIT là **`UNVERIFIED`**.
- **Xác nhận**: Khẳng định rõ dataset này **`NON-COMPLIANT` (Không đáp ứng)** yêu cầu tự crawl dữ liệu của CLB AI.

### D. Hiệu chỉnh nhận định về Chợ Tốt Xe
- **Trước khi sửa**: Xem endpoint `gateway.chotot.com/v1/public/ad-listing` như một API công khai có thể khai thác.
- **Hiệu chỉnh**: Đây là endpoint nội bộ quan sát được trong luồng mạng của ứng dụng, **không phải public developer API có tài liệu chính thức**. Nhóm không được cấp quyền sử dụng, không được gửi request kiểm tra, và không thử vượt WAF.
- **Trạng thái chuẩn hóa**: Quyền sử dụng là **`UNVERIFIED`**, phân loại nguồn là **`NO-GO`**.

### E. Hiệu chỉnh chỉ số về tính tái lập (Reproducibility)
- **Trước khi sửa**: Tuyên bố tệp dữ liệu tĩnh Kaggle có tính tái lập *"tuyệt đối"*.
- **Hiệu chỉnh**: Phân tách 3 khía cạnh: (1) Tái sử dụng tệp đã lưu: Cao; (2) Tái tạo đúng phiên bản dữ liệu: Cần mã băm SHA-256; (3) Tái lập quy trình thu thập từ web nguồn: `UNVERIFIED` hoặc rất thấp do mã spider của tác giả không được kiểm chứng và web nguồn đã thay đổi.
- **Trạng thái chuẩn hóa**: Ghi nhận là **`PARTIAL`**.

---

## 2. Danh Mục Các Tuyên Bố Chưa Thể Xác Minh (Unverified Claims Checklist)

Nhóm công khai danh sách các thông tin hiện chưa đủ bằng chứng để kết luận:

1. **`UNVERIFIED` - Khả năng phản hồi từ Nextgen Vietnam**: Chưa gửi thư chính thức và chưa nhận được văn bản chấp thuận cho phép thu thập học thuật.
2. **`UNVERIFIED` - Hành vi phòng vệ của hệ thống WAF/Cloudflare**: Chưa gửi request chuỗi nên chưa biết ngưỡng kích hoạt CAPTCHA hay khóa IP của Oto.com.vn.
3. **`UNVERIFIED` - Số dòng và số cột thực tế của Kaggle Dataset**: Con số ~5.000 dòng mới chỉ là thông tin tham khảo trên mạng; tệp `data.csv` chưa được tải về theo quy định an toàn nên chưa thể đo đạc chính xác.
4. **`UNVERIFIED` - Quyền phát hành dữ liệu gốc của Kaggle Dataset**: Chưa có bằng chứng xác nhận uploader được phép phân phối lại dữ liệu cào từ web ô tô.
5. **`NOT MEASURED` - Tỷ lệ missing trường `seats` trên toàn bộ sàn Oto.com.vn**: Mới chỉ quan sát thấy thiếu trong bảng thông số chuẩn của 2 trang mẫu chi tiết; chưa đo lường trên quy mô toàn sàn.

---

## 3. Các Nguồn Bằng Chứng Thực Tế Đã Sử Dụng (Actual Evidence Sources)

Mọi nhận định trong báo cáo đều được đối chiếu từ các nguồn bằng chứng thực tế sau:

1. **Mã nguồn HTML & Endpoint quan sát được**:
   - Mẫu danh sách và 2 trang chi tiết (ID 23442555 và ID 23444950) của Oto.com.vn.
   - Endpoint backend `gateway.chotot.com/v1/public/ad-listing` của Chợ Tốt.
2. **Quy chế hoạt động & Văn bản pháp lý công khai**:
   - [Quy chế hoạt động Sàn TMĐT Oto.com.vn](https://oto.com.vn/quy-che-hoat-dong) (Mục 10.1 về Bản quyền nội dung; Mục 7.1 về PII theo Nghị định 13/2023/NĐ-CP).
   - Quy chế hoạt động Sàn TMĐT Chợ Tốt (Quy định cấm trích xuất dữ liệu tự động).
   - Tệp chính sách robot: `https://oto.com.vn/robots.txt` (Chỉ là quy chuẩn kỹ thuật cho search indexers).
3. **Trang siêu dữ liệu Kaggle**:
   - Thẻ thông tin dataset `quocvinhduong/vietnam-automobile-dataset` (ID 4441964), dung lượng ~5.13 MB, nhãn hiển thị MIT.
4. **Kiểm thử logic mã nguồn nội bộ**:
   - Kết quả thực thi `pytest -v`: **36 passed in 0.06s** trong workspace, kiểm chứng logic của `price_parser.py` và `validation.py` trên 37 ca kiểm thử giá và 8 fixtures bản ghi xe.

---

## 4. Danh Sách Tệp Đã Cập Nhật (Updated Files)

1. [docs/data_source_audit.md](file:///d:/ai-club-end-training/docs/data_source_audit.md) (v2.1): Chuẩn hóa bảng so sánh đa tiêu chí độc lập, cập nhật trạng thái `NOT MEASURED`, phân định rõ ràng 4 điều kiện kích hoạt pilot.
2. [docs/mentor_data_source_decision.md](file:///d:/ai-club-end-training/docs/mentor_data_source_decision.md) (v2.1): Bản trình ngắn gọn, tập trung chuẩn xác vào 5 câu hỏi quyết định gửi Mentor, không tự trả lời thay Mentor.
3. [docs/data_pilot_plan.md](file:///d:/ai-club-end-training/docs/data_pilot_plan.md) (v3.1): Cập nhật 4 điều kiện kích hoạt độc lập, giữ quy mô pilot ở 30–50 tin, khẳng định dự án đang chờ Mentor quyết định.
4. [README.md](file:///d:/ai-club-end-training/README.md): Đồng bộ thông tin tiến độ Phase 2.1, giải thích rõ sự khác biệt giữa unit test logic và data quality.
5. [reports/phase2_1_evidence_review.md](file:///d:/ai-club-end-training/reports/phase2_1_evidence_review.md): Báo cáo nghiệm thu liêm chính bằng chứng (tài liệu này).

---

## 5. Bảng Nghiệm Thu Tiêu Chí (Acceptance Checklist)

| Tiêu chí nghiệm thu | Trạng thái | Bằng chứng thực tế trong workspace |
| :--- | :---: | :--- |
| **1. Đọc và kiểm tra workspace trước khi làm** | **PASS** | Chạy `git status` xác nhận working tree sạch, không commit tự động, không reset repo. |
| **2. Phân biệt Unit Test và Data Quality** | **PASS** | Sửa triệt để mọi khẳng định; ghi nhận chất lượng dữ liệu thật là `NOT MEASURED` trong toàn bộ tài liệu. |
| **3. Xác định điều kiện kích hoạt Pilot** | **PASS** | Phân tách 4 điều kiện độc lập; loại bỏ cơ chế "Mentor duyệt HOẶC Chủ web duyệt". |
| **4. Hiệu chỉnh nhận định về Kaggle Dataset** | **PASS** | Đánh dấu quyền phát hành nguồn là `UNVERIFIED`; khẳng định không đạt yêu cầu tự crawl của CLB. |
| **5. Hiệu chỉnh nhận định về Chợ Tốt** | **PASS** | Xác nhận endpoint là backend nội bộ, không có phép sử dụng; không gọi live request, đánh dấu `NO-GO`. |
| **6. Hiệu chỉnh chỉ số về tính tái lập** | **PASS** | Phân định 3 khía cạnh (reusability, versioning, source repeatability); gán nhãn `PARTIAL`. |
| **7. Chuẩn hóa bảng đánh giá nguồn** | **PASS** | Bảng audit trong `docs/data_source_audit.md` có đầy đủ 6 tiêu chí độc lập, không dùng điểm số gộp. |
| **8. Chuẩn bị 5 quyết định cho Mentor** | **PASS** | Tạo tệp `docs/mentor_data_source_decision.md` ngắn gọn, đúng 5 câu hỏi, không trả lời thay Mentor. |
| **9. Đồng bộ kế hoạch pilot và README** | **PASS** | Pilot giữ nguyên 30–50 tin; ghi rõ dự án đang chờ quyết định từ Mentor; README đồng bộ 100%. |
| **10. Không crawl và không tải dữ liệu** | **PASS** | Thư mục `data/raw/` hoàn toàn sạch; không gửi bất kỳ HTTP request tải dữ liệu nào. |
| **11. Không tự động commit Git** | **PASS** | Kiểm tra `git status`: Toàn bộ thay đổi nằm ở working tree sẵn sàng để người dùng xem xét. |

---

## 6. Năm Câu Hỏi Cần Mentor Quyết Định Trước Khi Bước Vào Phase 3

Trước khi triển khai Phase 3 (Thu thập dữ liệu thử nghiệm hoặc chuẩn bị Ingestion Pipeline), Mentor cần cho ý kiến định hướng trên 5 câu hỏi cốt lõi:

1. **CLB có bắt buộc dữ liệu chính phải do sinh viên tự thu thập (crawl/extract) từ internet hay không?**
2. **Mentor có thể giới thiệu website, API nghiên cứu hoặc nguồn dữ liệu phù hợp đã được phép thu thập cho mục đích đào tạo không?**
3. **Nếu sử dụng website bên ngoài (như Oto.com.vn), nhóm cần bằng chứng chấp thuận nào (văn bản từ doanh nghiệp hay phê duyệt bảo trợ từ Mentor) trước khi thu thập mẫu pilot 30–50 tin?**
4. **Nếu dùng dataset mở có sẵn (như trên Kaggle), dataset này được phép dùng làm nguồn dữ liệu chính thay thế hoàn toàn hay chỉ được dùng làm nguồn đối chiếu (benchmark)?**
5. **Mentor muốn định hướng quy mô dữ liệu tối thiểu, phạm vi phân tích EDA và số lượng/chủng loại mô hình Machine Learning cần so sánh như thế nào?**
