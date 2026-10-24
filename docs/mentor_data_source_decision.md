# Bản Trình Quyết Định Nguồn Dữ Liệu Gửi Mentor (Mentor Decision Brief)

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam (Used Car Price Prediction in Vietnam)
- **Giai đoạn**: Phase 2.1 — Source Decision Finalization
- **Thời gian lập**: 19/10/2026, 00:35:00 (Múi giờ: Asia/Ho_Chi_Minh)
- **Người thực hiện**: Nhóm Học Viên AI (với sự cố vấn của Senior Data Scientist & Technical Reviewer)
- **Mục đích**: Báo cáo tóm tắt tình trạng khảo sát nguồn dữ liệu thực tế và xin quyết định định hướng từ Mentor trên 5 vấn đề then chốt trước khi bước vào Phase 3.

---

## 1. Tóm Tắt Tình Trạng Thực Tế Của Dự Án

1. **Chuẩn bị kỹ thuật ngoại tuyến (Offline Readiness)**:
   - Đã hoàn thành bộ bóc tách giá ([src/data/price_parser.py](file:///d:/ai-club-end-training/src/data/price_parser.py)) và hợp đồng kiểm định chất lượng ([src/data/validation.py](file:///d:/ai-club-end-training/src/data/validation.py)).
   - Toàn bộ **36 unit tests đạt 100%** trên dữ liệu giả lập (synthetic fixtures).
   - *Lưu ý*: Chất lượng dữ liệu thực tế (missing values, tỷ lệ lỗi parse thật, độ lệch ngoại lai) hiện tại ở trạng thái **`NOT MEASURED`** vì chưa có dữ liệu thật được phép sử dụng.
2. **Trạng thái pháp lý & tiếp cận nguồn**:
   - Tất cả các website thương mại được khảo sát (Oto.com.vn, Chợ Tốt Xe, Bonbanh) đều có điều khoản dịch vụ (ToS) nghiêm cấm hành vi trích xuất tự động khi chưa có thỏa thuận bằng văn bản.
   - Nhóm duy trì trạng thái: **`AUTOMATED_COLLECTION_PENDING_PERMISSION_CLARIFICATION`** và **chưa thực hiện bất kỳ hành vi cào dữ liệu live nào**.
   - Đã soạn thảo sẵn thư xin phép sử dụng học thuật gửi Nextgen Vietnam ([docs/permission_request_draft.md](file:///d:/ai-club-end-training/docs/permission_request_draft.md)).
3. **Nguồn dữ liệu mở dự phòng (Kaggle)**:
   - Tồn tại tệp `data.csv` (~5.13 MB) có tên *Vietnam Automobile Dataset* do tác giả Quốc Vinh Dương đăng tải với nhãn MIT.
   - Tuy nhiên, quyền phát hành dữ liệu nguồn là **`UNVERIFIED`** (do dữ liệu gốc được crawl từ web bên thứ ba), và việc sử dụng tệp này **không đáp ứng yêu cầu tự crawl dữ liệu (self-crawling)** của CLB.

---

## 2. Bảng Tóm Tắt Trạng Thái 4 Nguồn Khảo Sát

| Nguồn dữ liệu | Khả thi kỹ thuật | Ủy quyền sử dụng | Đáp ứng yêu cầu tự crawl của CLB | Khả năng tái lập quy trình | Quyết định đề xuất |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Oto.com.vn** | FEASIBLE | PENDING *(Chờ phản hồi thư xin phép)* | **ĐẠT** *(Tự crawl & parse)* | CONDITIONAL | **`CONDITIONAL GO`** |
| **Chợ Tốt Xe** | FEASIBLE | UNVERIFIED *(Endpoint nội bộ, không có phép)* | **ĐẠT** *(Tự gọi API)* | CONDITIONAL | **`NO-GO`** |
| **Bonbanh.com** | FEASIBLE | NO-GO *(Quy chế cấm trích xuất)* | **ĐẠT** | CONDITIONAL | **`NO-GO`** |
| **Kaggle Dataset** | FEASIBLE | UNVERIFIED *(Nhãn MIT từ web crawl bên thứ ba)* | **KHÔNG ĐẠT** *(Dataset có sẵn)* | PARTIAL | **`CONDITIONAL GO (BACKUP ONLY)`** |

---

## 3. Năm Câu Hỏi Cần Quyết Định Từ Mentor (5 Key Decisions Needed)

Để đảm bảo dự án triển khai đúng mục tiêu đào tạo và tuân thủ chuẩn mực nghiên cứu, nhóm kính đề nghị Mentor cho ý kiến quyết định trên 5 câu hỏi sau:

### Câu hỏi 1: Yêu cầu tự thu thập dữ liệu của CLB
> **CLB có bắt buộc dữ liệu chính của đồ án phải do sinh viên tự thu thập (crawl/extract) từ internet hay không?**
> - *Nếu BẮT BUỘC*: Dự án phải tập trung vào việc xin cấp phép thu thập hợp pháp từ website (Nhánh A).
> - *Nếu KHÔNG BẮT BUỘC*: Nhóm có thể được phép chuyển sang khai thác dataset có sẵn để tập trung thời gian vào EDA và Modeling (Nhánh B).

### Câu hỏi 2: Nguồn dữ liệu hoặc API phù hợp
> **Mentor có thể giới thiệu một website, API nghiên cứu hoặc nguồn dữ liệu ô tô đã qua sử dụng nào đã được đơn vị quản lý cấp phép thu thập cho mục đích đào tạo không?**

### Câu hỏi 3: Bằng chứng chấp thuận trước khi thu thập dữ liệu ngoài
> **Nếu tiếp tục phương án thu thập từ website bên ngoài (như Oto.com.vn), nhóm cần cung cấp bằng chứng chấp thuận nào trước khi được phép kích hoạt đợt thu thập thử nghiệm (Pilot 30–50 tin)?**
> - *Lựa chọn a*: Bắt buộc phải có phản hồi đồng ý chính thức bằng văn bản/email từ doanh nghiệp sở hữu website.
> - *Lựa chọn b*: Văn bản phê duyệt và bảo trợ phương pháp luận từ Mentor là đủ để chạy thử nghiệm với tốc độ chậm (delay $\ge$ 3 giây/request, có User-Agent định danh).

### Câu hỏi 4: Vai trò của dataset có sẵn (nếu sử dụng)
> **Trong trường hợp Mentor cho phép sử dụng dataset mở có sẵn (như Vietnam Automobile Dataset từ Kaggle), tệp dữ liệu này được phép dùng làm nguồn dữ liệu chính thay thế hoàn toàn khâu crawl, hay chỉ được dùng làm nguồn đối chiếu (benchmark/validation)?**

### Câu hỏi 5: Kỳ vọng về quy mô và chiều sâu mô hình
> **Mentor có định hướng thế nào về:**
> - Quy mô dữ liệu tối thiểu cần đạt cho tập huấn luyện (ví dụ: 1.000 bản ghi hay quy mô khác)?
> - Phạm vi phân tích dữ liệu khám phá (EDA) và Feature Engineering?
> - Số lượng và chủng loại mô hình Machine Learning cần thử nghiệm so sánh (Baseline Linear Models, Tree-based Models, Gradient Boosting như XGBoost/LightGBM/CatBoost)?

---

## 4. Tình Trạng Chờ Hiện Tại
Nhóm cam kết **không tự ý kích hoạt bất kỳ tiến trình thu thập live nào hoặc tải dataset** cho đến khi nhận được hướng dẫn và phản hồi chính thức từ Mentor đối với các câu hỏi trên.
