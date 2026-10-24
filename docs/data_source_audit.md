# Báo Cáo Đánh Giá Khả Thi Nguồn Dữ Liệu (Data Source Feasibility Audit)

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam (Used Car Price Prediction in Vietnam)
- **Phiên bản tài liệu**: 3.0 (Cập nhật kết quả thẩm định nguồn tại Phase 3)
- **Thời gian cập nhật**: 19/10/2026, 01:25:00 (Múi giờ: Asia/Ho_Chi_Minh)
- **Người thực hiện**: Senior Data Scientist, Data Engineer & ML Mentor
- **Mục đích**: Đánh giá khách quan, thực chứng tính pháp lý, quyền truy cập, cấu trúc kỹ thuật và chất lượng dữ liệu của các nguồn ứng viên; cập nhật trạng thái theo quyết định mới từ Mentor.

---

## 1. Trạng Thái Hiện Tại Của Dự Án

Trạng thái chính thức về nguồn dữ liệu của dự án tại Phase 3:

```text
STATUS: AUTOMATED_COLLECTION_PENDING_PERMISSION_CLARIFICATION
```

> [!IMPORTANT]
> **Quyết định mới từ Mentor & Ý nghĩa thực thi**:
> - **Mentor đã chấp thuận về mặt sư phạm**: Cho phép nhóm triển khai song song cả hai hướng (Track A: Khai thác dataset có sẵn và Track B: Tự thu thập dữ liệu từ website).
> - **Tuy nhiên**: Sự chấp thuận của Mentor **không tự động cấp quyền pháp lý** để cào dữ liệu từ một website thương mại có điều khoản bảo lưu quyền nội dung.
> - **Nguyên tắc an toàn Phase 3**: Tiếp tục duy trì Crawler Gate (`dry_run=True`), chưa gửi HTTP request cào live đến Oto.com.vn; đồng thời chưa tải dataset ngoài khi quyền phát hành gốc chưa được xác minh (`PENDING_LICENSE_OR_PROVENANCE`).

---

## 2. Phân Định Rạch Ròi Giữa Logic Code & Chất Lượng Dữ Liệu

- **49 unit tests đạt 100%** trong thư mục `tests/` chỉ chứng minh: Logic của `price_parser.py`, `validation.py`, `load_dataset.py`, và `crawler.py` hoạt động hoàn hảo trên các tệp fixture tổng hợp ngoại tuyến.
- **Chất lượng dữ liệu (Data Quality) trên diện rộng**: Tiếp tục duy trì trạng thái **`NOT MEASURED` (Chưa đo lường)** cho đến khi có dữ liệu thật được phép sử dụng.
- Tuyệt đối **không tự tạo số liệu giả** về missing rate hay phân phối giá để điền vào báo cáo.

---

## 3. Điều Kiện Độc Lập Để Kích Hoạt Thu Thập Thực Tế (Pilot Gate)

Để một đợt thu thập thử nghiệm (pilot 30–50 tin) được kích hoạt, dự án phải thỏa mãn đồng thời **4 điều kiện độc lập**, không điều kiện nào được thay thế cho điều kiện khác:

1. **Mentor chấp thuận phạm vi & phương pháp đồ án**: Đã đạt được tại Phase 3 (Mentor đã phê duyệt cả hai hướng).
2. **Nguồn dữ liệu có điều kiện sử dụng phù hợp**: ToS của nguồn cho phép hoặc không cấm đoán.
3. **Đơn vị sở hữu / kiểm soát dữ liệu chấp thuận khi ToS cấm**: Có văn bản / email chấp thuận từ Nextgen Vietnam. *(Sự phê duyệt của Mentor không thay thế được quyền sở hữu trí tuệ của doanh nghiệp).*
4. **Nhóm đáp ứng yêu cầu kỹ thuật & an toàn**: Độ trễ tối thiểu `time.sleep(3.0)`, chạy đơn luồng, bộ lọc khử PII triệt để (không đọc/lưu SĐT, tên người bán).

---

## 4. Tái Thẩm Định Các Nguồn Dữ Liệu Ứng Viên Tại Phase 3

### 4.1. Nguồn tự thu thập chính: Oto.com.vn (Nextgen Vietnam)
- **Technical Feasibility**: **`FEASIBLE`**. Giao diện SSR, thẻ `<div class="item-car">` chứa metadata cấu trúc (`data-call`, `data-autoid`), hỗ trợ trích xuất tốt.
- **Access Authorization**: **`PENDING`**. Điều khoản 10.1 Quy chế sàn cấm sao chép tự động; đang chờ gửi thư xin phép [docs/permission_request_draft.md](file:///d:/ai-club-end-training/docs/permission_request_draft.md).
- **Usage and Licensing Terms**: **`PROPRIETARY`**. Bản quyền thuộc Công ty Cổ phần Nextgen Việt Nam.
- **Personal-data Risk**: **`HIGH IF UNFILTERED / CONTROLLED BY REGEX`**. Website hiển thị SĐT người bán; module [src/data/crawler.py](file:///d:/ai-club-end-training/src/data/crawler.py) đã tích hợp bộ lọc regex chặn hoàn toàn PII.
- **Data Quality**: **`NOT MEASURED`** trên diện rộng.
- **Suitability for Self-Crawling**: **`COMPLIANT (100%)`**. Sinh viên tự xây dựng pipeline crawler, parser, và validation.
- **Current Decision**: **`CONDITIONAL GO`** (Chờ phản hồi văn bản từ đơn vị sở hữu trước khi mở chốt `dry_run`).

### 4.2. Nguồn tự thu thập thay thế: Chợ Tốt Xe (xe.chotot.com)
- **Technical Feasibility**: **`FEASIBLE (Kỹ thuật)`**. Tồn tại endpoint backend JSON `gateway.chotot.com/v1/public/ad-listing`.
- **Access Authorization**: **`UNVERIFIED / PROHIBITED BY TOS`**. Endpoint nội bộ quan sát được, không phải public API chính thức; ToS cấm trích xuất tự động; có WAF chặn IP.
- **Usage and Licensing Terms**: **`PROPRIETARY`**. Bản quyền thuộc Công ty TNHH Chợ Tốt.
- **Personal-data Risk**: Trung bình (API có thể chứa số điện thoại nếu không lọc).
- **Data Quality**: **`NOT MEASURED`**.
- **Suitability for Self-Crawling**: **`COMPLIANT`**.
- **Current Decision**: **`NO-GO`** (Không có thỏa thuận cấp phép sử dụng API; cấm gọi request).

### 4.3. Nguồn tự thu thập thay thế: Bonbanh.com (bonbanh.com)
- **Technical Feasibility**: **`FEASIBLE`** (HTML tĩnh cơ bản).
- **Access Authorization**: **`NO-GO`** (ToS bảo lưu quyền, cấm trích xuất).
- **Current Decision**: **`NO-GO`**.

### 4.4. Nguồn dataset mở dự phòng: Vietnam Automobile Dataset (Kaggle)
- **Technical Feasibility**: **`FEASIBLE`** (Tệp bảng `data.csv` ~5.13 MB).
- **Access Authorization**: **`UNAVAILABLE via CLI / ANONYMOUS BOT`** (Trả về HTTP 404; đòi hỏi phiên đăng nhập web Kaggle hoặc API token có xác thực).
- **Usage and Licensing Terms**: **`UNVERIFIED`** (Ghi nhãn MIT trên Kaggle, nhưng dữ liệu gốc do cá nhân cào từ web bên thứ ba; quyền cấp phép lại MIT chưa được xác minh).
- **Personal-data Risk**: Thấp (thông tin xe).
- **Data Quality**: **`NOT MEASURED`** (Chưa tải tệp về theo quy tắc an toàn Phase 3).
- **Suitability for Self-Crawling**: **`NON-COMPLIANT`** (Là tệp có sẵn, không đáp ứng tiêu chí sinh viên tự crawl).
- **Current Decision**: **`PENDING_LICENSE_OR_PROVENANCE`** (Chưa đủ căn cứ để tải làm dữ liệu chính).

### 4.5. Nguồn dataset GitHub ứng viên mới: Car_price_analysis (mquaan/Car_price_analysis)
- **Technical Feasibility**: **`FEASIBLE (Hoàn toàn khả thi)`**. Tệp dữ liệu lưu trữ trực tiếp trên GitHub repository, tải về ngoại tuyến qua URL raw không bị rào cản edge/Cloudflare.
- **Access Authorization**: **`TECHNICALLY_AVAILABLE`**. Không đòi hỏi tài khoản đăng nhập hay API token cá nhân.
- **Usage and Licensing Terms**: **`TECHNICALLY_AVAILABLE_LICENSE_PENDING`**. README ghi "Apache 2.0", nhưng GitHub repository không có tệp `LICENSE` chính thức (`license: None`). Bản quyền dữ liệu gốc do cá nhân cào từ website thương mại `bonbanh.com`; người đăng tải không có thẩm quyền pháp lý để tái cấp phép nội dung cào thương mại dưới dạng Apache 2.0. Phù hợp cho mục đích bài tập học thuật/nghiên cứu nội bộ (Fair Dealing/Educational Use), nhưng bị chặn đối với phát hành thương mại.
- **Personal-data Risk**: **`CONTROLLED`**. Nhóm chỉ tiếp nhận tệp thông số xe `car_sell_processed.csv` và `car_detail.csv`; chủ động **loại bỏ tệp `seller.csv`** (chứa SĐT và thông tin liên hệ cá nhân) để tuân thủ triệt để Nghị định 13/2023/NĐ-CP.
- **Data Quality**: **`MEASURED (Đã đo lường thực tế)`**. 30,652 bản ghi, tỷ lệ bóc tách giá thành công 100.00%, tỷ lệ bản ghi đạt chuẩn hợp đồng validation là 88.83% (27,229 bản ghi hợp lệ).
- **Suitability for Self-Crawling**: **`NON-COMPLIANT (Track A - External Dataset)`**.
- **Current Decision**: **`TECHNICALLY_AVAILABLE_LICENSE_PENDING`** (Đủ điều kiện staging cục bộ để thẩm định schema, chạy benchmark mô hình học máy; ghi nhận caveat bản quyền).


---

## 5. Bảng Chuẩn Hóa So Sánh Đa Nguồn Tại Phase 3.2

| Tiêu chí chuẩn hóa | Oto.com.vn (Track B) | Chợ Tốt Xe (xe.chotot.com) | Bonbanh.com (Trực tiếp) | Vietnam Automobile Dataset (Kaggle) | Car_price_analysis (mquaan GitHub) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Technical Feasibility** | **FEASIBLE** | **FEASIBLE** | **FEASIBLE** | **FEASIBLE** | **FEASIBLE** |
| **Access Authorization** | **PENDING** | **UNVERIFIED** | **NO-GO** | **UNAVAILABLE via CLI** | **TECHNICALLY_AVAILABLE** |
| **Usage and Licensing Terms**| **PROPRIETARY** | **PROPRIETARY** | **PROPRIETARY** | **UNVERIFIED** | **LICENSE_PENDING** *(Apache 2.0 unverified for data)* |
| **Personal-data Risk** | **CONTROLLED** *(regex)*| **UNVERIFIED** | **UNVERIFIED** | **LOW** | **CONTROLLED** *(seller.csv excluded)* |
| **Data Quality** | **NOT MEASURED** | **NOT MEASURED** | **NOT MEASURED** | **NOT MEASURED** | **MEASURED** *(88.83% valid, 30.6k rows)* |
| **Suitability for Self-Crawling** | **COMPLIANT** | **COMPLIANT** | **COMPLIANT** | **NON-COMPLIANT** | **NON-COMPLIANT** *(Track A)* |
| **Reproducibility** | **CONDITIONAL** | **CONDITIONAL** | **CONDITIONAL** | **PARTIAL** | **HIGH (SHA-256 fixed)** |
| **QUYẾT ĐỊNH HIỆN TẠI** | **`CONDITIONAL GO`**<br>*(Chờ phản hồi văn bản)* | **`NO-GO`**<br>*(Endpoint nội bộ)* | **`NO-GO`**<br>*(ToS cấm)* | **`BLOCKED_CLI`**<br>*(Kaggle Cloudflare)* | **`TECHNICALLY_AVAILABLE_LICENSE_PENDING`**<br>*(Staged cục bộ, kiểm định thực tế)* |


---

## 6. Kết Luận & Hướng Triển Khai Kỹ Thuật

1. **Về Track A (Dataset ngoài)**:
   - Đã xây dựng hoàn tất module nạp và kiểm tra toàn vẹn [src/data/load_dataset.py](file:///d:/ai-club-end-training/src/data/load_dataset.py) cùng quy chuẩn [docs/schema_mapping.md](file:///d:/ai-club-end-training/docs/schema_mapping.md) và [data/metadata/README.md](file:///d:/ai-club-end-training/data/metadata/README.md).
   - Tạm dừng tải tệp `data.csv` từ Kaggle cho đến khi có sự thống nhất từ Mentor về việc cấp tài khoản hoặc chấp nhận rủi ro bản quyền của nguồn scraped này.
2. **Về Track B (Website Crawler)**:
   - Đã xây dựng hoàn tất kiến trúc crawler ngoại tuyến [src/data/crawler.py](file:///d:/ai-club-end-training/src/data/crawler.py) có chốt an toàn `dry_run=True` và bộ lọc PII.
   - Sẵn sàng kích hoạt đợt thử nghiệm pilot 30–50 tin ngay khi nhận được văn bản chấp thuận từ Nextgen Vietnam.
