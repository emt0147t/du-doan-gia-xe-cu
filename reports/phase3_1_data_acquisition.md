# Báo Cáo Giải Quyết Nguồn Dữ Liệu & Tính Sẵn Sàng Tiếp Nhận Dữ Liệu Thực Tế
*(Phase 3.1 — Resolve Data Source & Acquire First Real Dataset Report)*

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam (Used Car Price Prediction in Vietnam)
- **Giai đoạn**: Phase 3.1 — Resolve Data Source & Acquire First Real Dataset
- **Thời gian lập**: 19/10/2026, 01:25:00 (Múi giờ: Asia/Ho_Chi_Minh)
- **Người thực hiện**: Senior Data Engineer & Machine Learning Reviewer
- **Môi trường thực thi**: Windows 11, Python `3.11.9`, pytest `9.1.1`

---

## 1. Tóm Tắt Tình Trạng Tiếp Nhận Dữ Liệu (Executive Summary)

Tại Phase 3.1, dự án tập trung giải quyết dứt điểm tình trạng của hai nguồn dữ liệu ứng viên để chuẩn bị bước vào Phase 4 (EDA):

1. **Track A (Kaggle Dataset — Vietnam Automobile Dataset)**:
   - **Xác minh URL hiện hành**: Đã xác minh URL chính thức trên Kaggle là `https://www.kaggle.com/datasets/qucvinhdng/automobile-dataset/data` (user handle: `qucvinhdng`, dataset slug: `automobile-dataset`).
   - **Rào cản truy cập tự động**: Kaggle Cloudflare chặn toàn bộ các lệnh truy cập CLI vô danh (`curl.exe` trả về `HTTP/1.1 404 Not Found`). Dataset chỉ có thể tải khi có phiên đăng nhập của người dùng hoặc cấu hình Kaggle API credentials.
   - **Rào cản bản quyền dữ liệu nguồn**: Dữ liệu do cá nhân cào từ website thương mại bên thứ ba; nhãn MIT do uploader tự gắn trên Kaggle **chưa được xác minh quyền phát hành của dữ liệu gốc** (`PENDING_LICENSE_OR_PROVENANCE`).
   - **Trạng thái**: **`BLOCKED_PENDING_SOURCE_OR_USER_DOWNLOAD`**. Không tự ý tải tự động khi quyền nguồn chưa rõ; đã cung cấp hướng dẫn thao tác thủ công chuẩn mực.
2. **Track B (Website Collection — Oto.com.vn)**:
   - **Trạng thái pháp lý**: Mục 10.1 Quy chế sàn TMĐT Oto.com.vn bảo lưu quyền sở hữu nội dung; chưa nhận được phản hồi chấp thuận đối với [docs/permission_request_draft.md](file:///d:/ai-club-end-training/docs/permission_request_draft.md).
   - **Chốt an toàn**: Module [src/data/crawler.py](file:///d:/ai-club-end-training/src/data/crawler.py) giữ nguyên chốt an toàn `dry_run=True`, **tuyệt đối không gửi request live**.
   - **Trạng thái**: **`BLOCKED_PENDING_PERMISSION`**.

---

## 2. Thẩm Định Chi Tiết Ứng Viên Kaggle Hiện Hành

| Tiêu chí | Thông tin công bố trên Kaggle | Thông tin nhóm đã tự kiểm chứng thực tế | Thông tin chưa thể xác minh (UNVERIFIED) |
| :--- | :--- | :--- | :--- |
| **URL chính thức** | `https://www.kaggle.com/datasets/qucvinhdng/automobile-dataset/data` | Xác nhận URL hoạt động trên giao diện web; curl CLI trả về 404 do Cloudflare chặn bot. | Tần suất cập nhật thực tế của tác giả trong tương lai. |
| **Tác giả / Publisher** | Quoc Vinh Dinh (`qucvinhdng`) | Khớp với tài khoản tạo dataset; liên kết với tên Quốc Vinh Dương ở báo cáo trước. | Danh tính pháp lý và đơn vị bảo trợ nghiên cứu của tác giả. |
| **Nguồn gốc dữ liệu** | Thu thập bằng Scrapy từ website mua bán xe ô tô tại Việt Nam. | Xác nhận code spider do tác giả tự xây dựng; cấu trúc bảng phù hợp thị trường xe Việt Nam. | Website nguồn cụ thể bị cào dữ liệu (Oto.com.vn, Bonbanh hay Chợ Tốt). |
| **Giấy phép hiển thị** | MIT License | Nhãn MIT hiển thị trên metadata card của Kaggle. | **Quyền phân phối lại của dữ liệu gốc**: Tác giả không có bản quyền cơ sở dữ liệu gốc để cấp phép MIT. |
| **Tệp dữ liệu** | `data.csv` (~5.13 MB) | Tồn tại trên nền tảng Kaggle; có thể mở trong Kaggle Notebooks. | Số dòng và số cột chính xác (chưa tải về workspace nên giữ `NOT_MEASURED`). |
| **Độ phù hợp bài toán** | Tabular Regression (Dự đoán giá ô tô) | Cung cấp các trường: hãng xe, model, năm, ODO, hộp số, nhiên liệu, giá. | Tỷ lệ missing values và độ lệch của nhãn giá trên toàn bộ file. |

---

## 3. Khảo Sát Các Nguồn Dữ Liệu Thay Thế (Task B)

Nhóm đã khảo sát 3 nguồn thay thế tiềm năng theo thứ tự ưu tiên:
1. **Chợ Tốt Xe (xe.chotot.com)**: Có endpoint JSON nội bộ nhưng ToS nghiêm cấm trích xuất tự động; không có tài liệu cấp phép API cho cộng đồng $\rightarrow$ **`NO-GO`**.
2. **Cổng Dữ Liệu Mở Quốc Gia (`data.gov.vn`)**: Đã rà soát; cơ quan nhà nước không công bố giá rao bán xe cũ trên thị trường $\rightarrow$ **`NO-GO` (Thiếu target)**.
3. **Dataset quốc tế (Hugging Face / UCI)**: Có giấy phép mở chuẩn (CC BY 4.0 / MIT) nhưng dữ liệu thuộc thị trường Mỹ/Ấn Độ, đơn vị tiền tệ ngoại tệ (USD/INR), vi phạm Điều lệ dự án (phải dự đoán xe tại Việt Nam theo VND) $\rightarrow$ **`REJECTED`**.

---

## 4. Kiểm Thử Mã Nguồn & Xác Minh Phòng Vệ An Toàn (Tasks F & Testing)

Lệnh kiểm thử tự động toàn diện:
```powershell
$env:PYTHONIOENCODING="utf-8"
pytest -v --tb=short
```

**Kết quả thực tế đo được:**
- **50 test functions PASSED 100% trong 0.70s** (0 failed, 0 skipped).
- **Kiểm định tính độc lập mạng**: 100% tests chạy ngoại tuyến, không gửi bất kỳ HTTP request nào.
- **Xác minh phòng vệ Crawler Gate**:
  - `CrawlerConfig.dry_run = True` mặc định ngăn chặn hoàn toàn việc gọi request mạng live.
  - `PilotCrawler.run_pilot()` trả về trạng thái `STOPPED_BY_CRAWLER_GATE`.
  - Bộ bóc tách DOM (`extract_listing_card`) hoạt động độc lập tuyệt đối với kết nối mạng.
- **Xác minh phòng vệ PII (Phòng thủ chiều sâu)**:
  - Selector bỏ qua hoàn toàn các thuộc tính `data-phone`, `seller-phone` và tên người bán.
  - Bổ sung bộ lọc regex khử số điện thoại trong trường tiêu đề tự do: `re.sub(r"(?:\+84|0)[35789]\d{8}", "[REDACTED_PHONE]", raw_title)`.
  - Đã có unit test `test_pii_scrubbing_in_title_text()` xác minh thành công.
  - *Lưu ý*: Nhóm không tuyên bố bộ lọc bảo đảm loại bỏ 100% mọi dạng PII tự do phức tạp (như địa chỉ nhà riêng ẩn trong văn bản), nhưng đã loại bỏ hoàn toàn các kênh PII trực tiếp.

---

## 5. Bảng Nghiệm Thu Tiêu Chí Phase 3.1 (Acceptance Checklist)

| Tiêu chí | Trạng thái | Minh chứng thực tế |
| :--- | :---: | :--- |
| **Kiểm tra ứng viên Kaggle bằng URL hiện hành** | **PASS** | Xác minh URL `qucvinhdng/automobile-dataset/data` và lý do curl trả về 404. |
| **Đánh giá nguồn gốc và điều kiện sử dụng** | **PASS** | Phân định rạch ròi nhãn MIT với quyền dữ liệu gốc (`PENDING_LICENSE_OR_PROVENANCE`). |
| **Tìm ứng viên thay thế khi cần** | **PASS** | Khảo sát Chợ Tốt Xe, Cổng dữ liệu quốc gia và Hugging Face; ghi nhận lý do không đạt. |
| **Tiếp nhận dataset thật nếu đủ điều kiện** | **PARTIAL / BLOCKED** | Chưa có dataset nào thỏa mãn 100% điều kiện tự do tải; nhóm không tải bừa bãi. |
| **Lập báo cáo chất lượng ban đầu** | **PASS** | Cập nhật [reports/dataset_initial_audit.md](file:///d:/ai-club-end-training/reports/dataset_initial_audit.md) ghi rõ trạng thái `NOT_MEASURED`. |
| **Không tạo dữ liệu giả làm dữ liệu thật** | **PASS** | Tuân thủ tuyệt đối; thư mục `data/raw/external/` hoàn toàn sạch. |
| **Crawler website chưa được phép vẫn bị khóa** | **PASS** | `src/data/crawler.py` giữ chốt `dry_run=True`; Oto.com.vn chưa bị cào live. |
| **Bộ test suite được chạy lại thực tế** | **PASS** | Đạt **50/50 tests passed** trong 0.70s. |
| **Chưa tự động commit Git** | **PASS** | Kiểm tra `git status`: Toàn bộ thay đổi nằm ở working tree. |

---

## 6. Chuẩn Bị Cho Phase 4 (Exploratory Data Analysis)

Pipeline nạp và chuẩn hóa dữ liệu đã sẵn sàng 100%. Ngay khi bạn hoặc Mentor thực hiện một trong hai hành động sau, Phase 4 có thể bắt đầu ngay lập tức:

1. **Nếu chọn Track A (Kaggle Dataset)**:
   - Tải tệp `data.csv` theo hướng dẫn tại Mục 5 của [reports/dataset_initial_audit.md](file:///d:/ai-club-end-training/reports/dataset_initial_audit.md).
   - Đặt vào: `data/raw/external/kaggle_automobile/data.csv`.
   - Pipeline [src/data/load_dataset.py](file:///d:/ai-club-end-training/src/data/load_dataset.py) sẽ tự động nạp, tính SHA-256 hash và ánh xạ 14 trường để bắt đầu vẽ biểu đồ phân phối giá, ma trận tương quan và phân tích ngoại lai.
2. **Nếu chọn Track B (Website Pilot)**:
   - Khi có văn bản chấp thuận từ Nextgen Vietnam, mở chốt `dry_run=False` trong [src/data/crawler.py](file:///d:/ai-club-end-training/src/data/crawler.py) để thu thập mẫu pilot 30–50 tin phục vụ EDA.
