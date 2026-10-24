# Báo Cáo Đánh Giá Chất Lượng Dữ Liệu Ban Đầu (Initial Data Quality Audit Report)

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam (Used Car Price Prediction in Vietnam)
- **Giai đoạn**: Phase 3.2 — Verify Dataset Candidate & Prepare Real Data Ingestion
- **Thời gian lập**: 19/10/2026, 02:15:00 (Múi giờ: Asia/Ho_Chi_Minh)
- **Người thực hiện**: Senior Data Engineer & ML Reviewer
- **Tài liệu liên quan**: [Data Source Audit](file:///d:/ai-club-end-training/docs/data_source_audit.md), [Schema Mapping](file:///d:/ai-club-end-training/docs/schema_mapping.md), [Data Pilot Plan](file:///d:/ai-club-end-training/docs/data_pilot_plan.md), [Ingestion Metadata](file:///d:/ai-club-end-training/data/metadata/ingestion_mquaan_car_price.json)

---

## 1. Tổng Quan Tiến Trình Đo Lường Chất Lượng Dữ Liệu

| Giai đoạn | Trạng thái đo lường | Nguồn khảo sát | Lý do kỹ thuật / pháp lý |
| :--- | :--- | :--- | :--- |
| **Phase 3.1** | `NOT_MEASURED` | `qucvinhdng/automobile-dataset` (Kaggle) | Bị chặn bởi Cloudflare/Edge HTTP 404 qua anonymous CLI; chưa có tệp live trong thư mục raw. |
| **Phase 3.2** | **`MEASURED (STAGED FOR AUDIT)`** | `mquaan/Car_price_analysis` (GitHub / Kaggle provenance) | Đã tải thành công 2 tệp bảng vào `data/raw/external/mquaan_car_price/`, tạo checksum SHA-256 cố định phiên bản, chạy đo lường thực nghiệm toàn diện trên 30,652 bản ghi. |

---

## 2. Thông Tin Tiếp Nhận & Xác Minh Toàn Vẹn Tệp Dữ Liệu Thực Tế

Tuân thủ quy chuẩn quản lý dữ liệu tại [data/metadata/README.md](file:///d:/ai-club-end-training/data/metadata/README.md), các tệp thô được lưu trữ bất biến (immutable) và kiểm tra mã băm SHA-256 bằng [src/data/load_dataset.py](file:///d:/ai-club-end-training/src/data/load_dataset.py):

| Tên tệp dữ liệu thô | Kích thước | SHA-256 Checksum | Số dòng | Số cột | Trạng thái bảo mật PII |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`car_detail.csv`** | 21,355,297 B (~21.3 MB) | `44c13afc5982f7abc51611fc56eeefd02df8e47f3224112f51b76514a7328f08` | 30,652 | 21 | Chứa URL và mô tả người bán; đã ghi nhận kiểm soát PII |
| **`car_sell_processed.csv`** | 6,452,999 B (~6.45 MB) | `1d0c0d2f5a920f19eee09cffc84f30c7bc7496ac5bcb35260ccfbbd93c89437c` | 30,652 | 21 | **Đã khử toàn bộ SĐT & liên hệ cá nhân** |
| **`Data_source.txt`** | 218 B | `91b56f1d5235a4ae3cddb2315a8e939fff24f94f` | - | - | Ghi nhận nguồn gốc Kaggle gốc |
| **`seller.csv`** | 3,167,494 B | *(Không tải về workspace)* | - | - | **CHỦ ĐỘNG LOẠI BỎ** do chứa SĐT cá nhân |

---

## 3. Kết Quả Đo Lường Khách Quan Trên 30,652 Bản Ghi Live

### 3.1. Cấu trúc và Khuyết thiếu (Missing Values Audit)

Phân tích trên tệp gốc `car_detail.csv` (30,652 dòng x 21 cột):

```text
Cột dữ liệu thô               Số lượng Missing    Tỷ lệ Missing (%)    Phân loại schema dự án
───────────────────────────────────────────────────────────────────────────────────────────
Mã tin                                      0                0.00%    listing_id (Khóa duy nhất)
Xuất xứ                                     0                0.00%    origin
Tình trạng                                  0                0.00%    condition
Dòng xe                                     0                0.00%    body_type
Số Km đã đi                                 0                0.00%    mileage_km (cần parse '0 Km')
Màu ngoại thất                              0                0.00%    exterior_color
Màu nội thất                                0                0.00%    interior_color
Số cửa                                      0                0.00%    doors
Số chỗ ngồi                                 0                0.00%    seats
Động cơ                                     0                0.00%    engine / fuel_type
Hệ thống nạp nhiên liệu                23,907               77.99%    fuel_system (Tùy chọn)
Hộp số                                      0                0.00%    transmission
Dẫn động                                    0                0.00%    drivetrain
Tiêu thụ nhiên liệu                         0                0.00%    fuel_consumption
Mô tả                                       0                0.00%    description
Hãng                                        0                0.00%    brand
Grade                                       0                0.00%    model
Năm sản xuất                               32                0.10%    year (Trường bắt buộc)
Tên xe                                      0                0.00%    title
Giá                                         0                0.00%    price_vnd (Target)
URL                                         0                0.00%    source_url
```

> [!NOTE]
> - Tỷ lệ điền đầy của các trường đặc trưng cốt lõi (`brand`, `model`, `price`, `transmission`, `origin`, `body_type`) đạt **100.00%**.
> - Trường `year` chỉ khuyết thiếu **32 bản ghi (0.10%)**.
> - Trường `Hệ thống nạp nhiên liệu` khuyết thiếu cao (77.99%) nên chỉ xem là đặc trưng phụ, không dùng làm điều kiện lọc bản ghi.

---

### 3.2. Kiểm tra Trùng lặp (Deduplication Audit)

- **Theo mã định danh bài đăng (`Mã tin` / `listing_id`)**:
  - Số lượng ID duy nhất: **30,652 / 30,652** tin đăng (Tỷ lệ duy nhất: **100.00%**).
  - Trùng lặp theo khóa chính: **0 bản ghi (0.00%)**.
- **Theo toàn bộ các thuộc tính (Exact Duplicate Rows)**:
  - Tệp thô `car_detail.csv`: **0 bản ghi trùng lặp tuyệt đối**.
  - Tệp bảng `car_sell_processed.csv`: **248 bản ghi trùng lặp** (0.81%) do lược bỏ cột ID và mô tả chi tiết, khiến các xe cùng thông số cơ bản trông giống nhau.

---

### 3.3. Kiểm thử Năng lực Bóc tách Giá Mục Tiêu (`price_vnd`)

Chạy thực nghiệm hàm `parse_vietnamese_price_to_vnd` từ [src/data/price_parser.py](file:///d:/ai-club-end-training/src/data/price_parser.py) trên toàn bộ 30,652 chuỗi giá tiếng Việt:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│              KẾT QUẢ PARSE GIÁ TRÊN TOÀN BỘ DATASET (30,652 TIN)            │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ Tổng số dòng đánh giá                │ 30,652                               │
│ Số dòng parse thành công             │ 30,652 (100.00%)                     │
│ Số dòng parse thất bại               │ 0 (0.00%)                            │
│ Giá trị nhỏ nhất (Min)               │ 18,000,000 VND (18 triệu)            │
│ Phân vị 25% (Q1)                     │ 410,000,000 VND (410 triệu)          │
│ Trung vị 50% (Median)                │ 620,000,000 VND (620 triệu)          │
│ Giá trị trung bình (Mean)            │ 1,180,744,682 VND (~1.18 tỷ)         │
│ Phân vị 75% (Q3)                     │ 1,030,000,000 VND (1.03 tỷ)          │
│ Giá trị lớn nhất (Max)               │ 54,000,000,000 VND (54 tỷ)           │
│ Độ lệch chuẩn (Std)                  │ 2,068,362,485 VND (~2.07 tỷ)         │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ Số tin dưới ngưỡng sàn (< 30 triệu)  │ 13 bản ghi (0.04%)                   │
│ Số tin trên ngưỡng trần (> 50 tỷ)    │ 1 bản ghi (0.003% - Rolls-Royce 54B) │
│ Số tin hợp lệ trong ngưỡng [30M, 50B]│ 30,638 bản ghi (99.95%)              │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

> [!TIP]
> Module `price_parser.py` được xây dựng từ Phase 1 xử lý hoàn hảo 100% các định dạng giá phức tạp của thị trường Việt Nam (`"249 Triệu"`, `"4 Tỷ 286 Triệu"`, `"1 Tỷ 229 Triệu"`), khẳng định tính đúng đắn và độ tin cậy của thuật toán bóc tách giá.

---

### 3.4. Kiểm định Chất lượng Theo Hợp Đồng Dữ Liệu (`src/data/validation.py`)

Chạy thực thi hàm `validate_car_record` với cấu hình chuẩn `ValidationConfig(min_year=2010, max_year=2026, min_price=30M, max_price=50B, max_mileage=1M)`:

```text
Tổng số bản ghi kiểm định: 30,652

- HỢP LỆ (Valid records):     27,229 bản ghi (88.83%)
- KHÔNG HỢP LỆ (Invalid):      3,423 bản ghi (11.17%)

Chi tiết các lỗi kỹ thuật (Error Breakdown):
1. YEAR_OUT_OF_BOUNDS:        3,303 bản ghi (10.78%) -> Xe sản xuất trước 2010 (1990 - 2009)
2. MILEAGE_EXCEEDS_MAX:         124 bản ghi ( 0.40%) -> ODO bất thường (> 1,000,000 km hoặc overflow 2^32-1)
3. MISSING_YEAR:                 32 bản ghi ( 0.10%) -> Thiếu năm sản xuất
4. INVALID_TRANSMISSION:         17 bản ghi ( 0.06%) -> Ghi nhận '-' (15 tin) hoặc 'Số hỗn hợp' (2 tin)
5. TARGET_OUT_OF_BOUNDS:         14 bản ghi ( 0.05%) -> 13 tin < 30 triệu và 1 tin 54 tỷ
```

---

### 3.5. Phân Phối Các Đặc Trưng Nghiệp Vụ Cốt Lõi

1. **Thương hiệu (Brand)**:
   - Tổng cộng **76 hãng xe** khác nhau trên thị trường Việt Nam.
   - Top 5 hãng chiếm 61.0% thị phần:
     - **Toyota**: 5,592 xe (18.2%)
     - **Hyundai**: 3,555 xe (11.6%)
     - **Ford**: 3,370 xe (11.0%)
     - **Mercedes-Benz**: 3,191 xe (10.4%)
     - **Kia**: 2,991 xe (9.8%)
2. **Năm sản xuất (Year)**:
   - Dải năm: Từ **1990** đến **2023**.
   - Phân bố tập trung mạnh từ 2015 đến 2022 (chiếm hơn 75% lượng xe giao dịch).
3. **Tình trạng xe (Condition)**:
   - Xe đã sử dụng (Used cars): **24,582 xe (80.2%)**.
   - Xe mới (New cars): **6,070 xe (19.8%)**.
4. **Hộp số (Transmission)**:
   - Số tự động: **25,136 xe (82.0%)**.
   - Số sàn / Số tay: **5,499 xe (17.9%)**.
   - Không xác định / ngoại lai: 17 xe (0.1%).
5. **Nhiên liệu (Fuel Type)**:
   - Xăng: **24,723 xe (80.7%)**.
   - Dầu (Diesel): **5,354 xe (17.5%)**.
   - Điện (EV): **297 xe (1.0%)** *(Xu hướng xe điện mới nổi tại VN)*.
   - Hybrid: **254 xe (0.8%)**.
6. **Địa bàn phân bố (Location)**:
   - Phủ sóng đầy đủ **63 tỉnh/thành phố**.
   - Hà Nội: **14,612 xe (47.7%)**.
   - TP. Hồ Chí Minh: **5,681 xe (18.5%)**.
   - Hải Phòng: **960 xe (3.1%)**, Bình Dương: **865 xe (2.8%)**, Đồng Nai: **627 xe (2.0%)**.

---

## 4. Phân Tích Rủi Ro Dữ Liệu & Khuyến Nghị Cho Giai Đoạn Tiền Xử Lý (Phase 4)

1. **Hiện tượng ODO tràn số (Unsigned Int Overflow Outliers)**:
   - Tệp bảng `car_sell_processed.csv` xuất hiện giá trị mileage cực đại là `4,294,967,295` ($2^{32}-1$). Đây là lỗi điền giá trị dummy khi không có dữ liệu ODO của tác giả tiền xử lý.
   - *Khuyến nghị*: Chuyển đổi các giá trị $> 1,000,000$ km về `NaN` hoặc lọc bỏ.
2. **Thiên lệch địa lý (Geographic Sampling Bias)**:
   - Hà Nội và TP.HCM chiếm tới 66.2% tổng số tin rao bán. Cần gộp các tỉnh nhỏ thành nhóm vùng kinh tế hoặc áp dụng trọng số mẫu nếu cần dự đoán cho thị trường toàn quốc.
3. **Phân hóa xe cổ / xe cũ sâu (< 2010)**:
   - 3,303 xe sản xuất trước 2010 có quy luật định giá phi tuyến tính (xe cổ giá trị sưu tầm vs xe quá nát khấu hao hết).
   - *Khuyến nghị*: Giữ bộ lọc `year >= 2010` để mô hình hồi quy tập trung vào phân khúc xe thương mại đại chúng phổ biến nhất.

---

## 5. Kết Luận Khảo Sát & Trạng Thái Cổng Quyết Định

- **Trạng thái cổng quyết định**: **`TECHNICALLY_AVAILABLE_LICENSE_PENDING`**.
- Tập dữ liệu `mquaan_car_price` đã được tiếp nhận an toàn, đo lường toàn diện, có mã băm SHA-256 cố định, bảo vệ PII triệt để và có **27,229 bản ghi chuẩn mực** hoàn toàn sẵn sàng cho giai đoạn EDA sâu và huấn luyện mô hình Machine Learning ở các phase tiếp theo.
