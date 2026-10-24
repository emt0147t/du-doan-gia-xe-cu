# Báo Cáo Thẩm Định Ứng Viên Dữ Liệu & Tiếp Nhận Dữ Liệu Thực Tế
*(Phase 3.2 — Verify Dataset Candidate & Prepare Real Data Ingestion Report)*

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam (Used Car Price Prediction in Vietnam)
- **Giai đoạn**: Phase 3.2 — Verify Dataset Candidate & Prepare Real Data Ingestion
- **Thời gian lập**: 19/10/2026, 02:20:00 (Múi giờ: Asia/Ho_Chi_Minh)
- **Người thực hiện**: Senior Data Engineer & ML Reviewer
- **Môi trường thực thi**: Windows 11, Python `3.11.9`, pytest `9.1.1`, pandas `2.2.3`
- **Tài liệu đối chiếu**: [Data Source Audit v3.2](file:///d:/ai-club-end-training/docs/data_source_audit.md), [Dataset Initial Audit](file:///d:/ai-club-end-training/reports/dataset_initial_audit.md), [Ingestion Metadata](file:///d:/ai-club-end-training/data/metadata/ingestion_mquaan_car_price.json)

---

## 1. Tóm Tắt Kết Quả Thẩm Định (Executive Summary)

Tại Phase 3.2, dự án đã thực hiện kiểm định độc lập và tiếp nhận thành công ứng viên dữ liệu thị trường thực tế:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                 KẾT QUẢ QUYẾT ĐỊNH CỔNG PHASE 3.2 (DECISION GATE)           │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ Ứng viên dữ liệu khảo sát            │ https://github.com/mquaan/Car_price_ │
│                                      │ analysis                             │
│ Trạng thái Cổng Quyết Định           │ TECHNICALLY_AVAILABLE_LICENSE_       │
│                                      │ PENDING                              │
│ Số lượng bản ghi thị trường thực tế  │ 30,652 dòng x 21 cột                 │
│ Tỷ lệ bóc tách giá thành công        │ 100.00% (30,652/30,652 bản ghi)      │
│ Tỷ lệ bản ghi đạt chuẩn Validation   │ 88.83% (27,229 bản ghi hợp lệ)       │
│ Tình trạng kiểm soát mã nguồn        │ 51/51 Unit Tests PASSED (0.54s)      │
│ Tình trạng an toàn Crawler Web       │ Crawler Gate `dry_run=True` BẢO LƯU  │
│ Tình trạng Git Version Control       │ 0 auto-commit; working tree bảo toàn │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

---

## 2. Thẩm Định Chi Tiết Repository & Cấu Trúc Tệp Ứng Viên

### 2.1. Thông tin định danh Repository
- **Chủ sở hữu (Owner)**: `mquaan` (Nguyễn Minh Quân - Sinh viên khoa CNTT, Trường ĐH Khoa học Tự nhiên, ĐHQG-HCM).
- **Tên Repository**: `Car_price_analysis`.
- **URL**: `https://github.com/mquaan/Car_price_analysis`.
- **Ngày khởi tạo**: 15/08/2024.
- **Bối cảnh học thuật**: Đồ án môn học Trực quan hóa dữ liệu (Data Visualization with Tableau) dưới sự hướng dẫn của các giảng viên Bùi Tiến Lên, Lê Ngọc Thành, Lê Nguyễn Nhựt Trường.

### 2.2. Danh mục tệp & Cấu trúc thư mục được khảo sát qua GitHub API

```text
mquaan/Car_price_analysis/
├── Readme.md                          # Tài liệu giới thiệu, mô tả 30,652 dòng x 21 cột
├── data/
│   ├── Data_source.txt                # Ghi nhận URL nguồn gốc trên Kaggle
│   ├── Vietnam_province_info.csv      # Tọa độ và thông tin 63 tỉnh/thành (2.5 KB)
│   ├── car_sell_processed.csv         # Tệp bảng đã xử lý cơ bản (6.45 MB)
│   └── data_original/
│       ├── car_detail.csv             # Dữ liệu tin rao thô nguyên bản (21.35 MB)
│       ├── car_detail_en.csv          # Dữ liệu tin rao dịch tiếng Anh (19.37 MB)
│       ├── seller.csv                 # Dữ liệu người bán (3.17 MB - CHỨA PII)
│       └── seller_en.csv              # Dữ liệu người bán tiếng Anh (2.96 MB - CHỨA PII)
├── docs/                              # Tài liệu phân tích biểu đồ
└── source/                            # Mã nguồn phân tích & xử lý
```

---

## 3. Thẩm Định Xuất Xứ Dữ Liệu (Provenance) & Bản Quyền (License Analysis)

### 3.1. Truy vết nguồn gốc dữ liệu ban đầu (Ground Truth Provenance)
Qua việc giải mã trực tiếp tệp `car_detail.csv` và `seller.csv`, nhóm đã tìm thấy bằng chứng không thể bác bỏ về nguồn gốc thực tế của tập dữ liệu:
1. Cột `URL` trong `car_detail.csv` chứa các liên kết trực tiếp:
   `https://bonbanh.com/xe-suzuki-super_carry_truck-1.0-mt-2022-17042`
2. Cột `Website` trong `seller.csv` trỏ đến các salon phụ trên sàn Bonbanh:
   `https://suzukivietanh.bonbanh.com`, `https://toyotaphapvan.bonbanh.com`.
3. Tệp `Data_source.txt` xác nhận chuỗi tiếp nhận:
   `Bonbanh.com` $\rightarrow$ cào dữ liệu bởi user `nguynthanhlun` $\rightarrow$ chia sẻ trên Kaggle `vietnamese-car-price` $\rightarrow$ nhóm sinh viên `mquaan` tải về làm đồ án Tableau.

### 3.2. Đánh giá tính pháp lý của giấy phép Apache 2.0 được khai báo
- **Trên GitHub Repository**: API trả về `license: None`. Repository hoàn toàn không có tệp `LICENSE` chuẩn.
- **Trong `Readme.md`**: Tác giả ghi dòng chữ `Giấy phép: Apache 2.0` (sao chép lại từ nhãn chọn trên giao diện Kaggle).
- **Đánh giá pháp lý độc lập**:
  > [!WARNING]
  > Giấy phép Apache 2.0 chỉ có hiệu lực đối với **mã nguồn và các sản phẩm sáng tạo do chính tác giả tạo ra** (code Python, dashboard Tableau).
  > Người cào dữ liệu hoặc người đăng tải **không có thẩm quyền pháp lý để cấp phép Apache 2.0 cho cơ sở dữ liệu thương mại** gồm các tin đăng, hình ảnh và thông tin của sàn giao dịch Bonbanh.com và các salon ô tô.
- **Phạm vi sử dụng hợp pháp**:
  - Dữ liệu được phép sử dụng nội bộ cho mục đích học tập, nghiên cứu khoa học, làm bài tập lớn và huấn luyện mô hình trong môi trường câu lạc bộ AI (theo nguyên tắc Fair Dealing / Educational Research).
  - Tuyệt đối **không được thương mại hóa**, không đóng gói bán lại và không triển khai thành dịch vụ công cộng khi chưa có văn bản cấp phép của đơn vị sở hữu dữ liệu gốc.

### 3.3. Kiểm soát dữ liệu cá nhân (PII Compliance - Nghị định 13/2023/NĐ-CP)
- Tệp `seller.csv` chứa trực tiếp số điện thoại cá nhân người bán (`Điện thoại 1`, `Điện thoại 2`) và địa chỉ cá nhân.
- **Hành động kỹ thuật**: Nhóm **CHỦ ĐỘNG KHÔNG TẢI tệp `seller.csv`** vào workspace của dự án.
- Tệp `car_detail.csv` chỉ được tiếp nhận vào vùng staging để kiểm thử bóc tách giá và validation.
- Tệp `car_sell_processed.csv` đã được loại bỏ toàn bộ thông tin liên hệ cá nhân, bảo đảm tuân thủ quy chuẩn dữ liệu.

---

## 4. Quá Trình Tiếp Nhận, Băm Toàn Vẹn & Quản Lý Dữ Liệu (Ingestion)

Tập dữ liệu được tiếp nhận vào workspace thông qua script tự động tuân thủ chuẩn [data/metadata/README.md](file:///d:/ai-club-end-training/data/metadata/README.md):

```text
D:\ai-club-end-training\data\raw\external\mquaan_car_price\
├── car_sell_processed.csv             (SHA-256: 1d0c0d2f5a920f19eee09cffc84f30c7bc7496ac5bcb35260ccfbbd93c89437c)
├── car_sell_processed.csv.sha256
├── car_detail.csv                     (SHA-256: 44c13afc5982f7abc51611fc56eeefd02df8e47f3224112f51b76514a7328f08)
├── car_detail.csv.sha256
└── Data_source.txt                    (SHA-256: 91b56f1d5235a4ae3cddb2315a8e939fff24f94f)
```

- **Siêu dữ liệu tiếp nhận**: Đã lưu trữ chi tiết tại [data/metadata/ingestion_mquaan_car_price.json](file:///d:/ai-club-end-training/data/metadata/ingestion_mquaan_car_price.json).
- **Kiểm tra `.gitignore`**: Toàn bộ thư mục `data/raw/*` được bỏ qua khỏi Git tracking; `git status` xác nhận không có tệp dữ liệu thô nào bị đưa vào Git index.

---

## 5. Kết Quả Đo Lường Chất Lượng Dữ Liệu Thực Tế (Empirical Data Quality Audit)

### 5.1. Bóc tách nhãn mục tiêu `price_vnd` bằng `src/data/price_parser.py`
Toàn bộ 30,652 chuỗi giá trong `car_detail.csv` được nạp qua hàm `parse_vietnamese_price_to_vnd`:
- **Tỷ lệ parse thành công**: **100.00% (30,652/30,652)**. Không có chuỗi nào trả về `None` hoặc lỗi ngoại lệ.
- **Thống kê mô tả (VND)**:
  - Giá thấp nhất: **18,000,000 VND** (18 triệu).
  - Phân vị 25% ($Q_1$): **410,000,000 VND** (410 triệu).
  - Trung vị 50% ($Q_2$): **620,000,000 VND** (620 triệu).
  - Giá trung bình: **1,180,744,682 VND** (~1.18 tỷ).
  - Phân vị 75% ($Q_3$): **1,030,000,000 VND** (1.03 tỷ).
  - Giá cao nhất: **54,000,000,000 VND** (54 tỷ - Rolls-Royce Phantom).
  - Độ lệch chuẩn: **2,068,362,485 VND** (~2.07 tỷ).
- **Ngoại lai biên nghiệp vụ**:
  - Dưới ngưỡng sàn ($< 30$ triệu): **13 bản ghi (0.04%)**.
  - Trên ngưỡng trần ($> 50$ tỷ): **1 bản ghi (0.003%)**.
  - Nằm trong ngưỡng hợp lệ $[30\text{M}, 50\text{B}]$: **30,638 bản ghi (99.95%)**.

### 5.2. Kiểm định theo Hợp đồng chất lượng dữ liệu (`src/data/validation.py`)
Khi chạy `validate_car_record` với `ValidationConfig(min_year=2010, max_year=2026, min_price=30M, max_price=50B, max_mileage=1M)`:
- **Bản ghi hợp lệ (Valid)**: **27,229 bản ghi (88.83%)** $\rightarrow$ Sẵn sàng 100% cho Phase 4 & Phase 5.
- **Bản ghi không hợp lệ (Invalid)**: **3,423 bản ghi (11.17%)**.
  - `YEAR_OUT_OF_BOUNDS`: **3,303 bản ghi (10.78%)** — Các dòng xe sản xuất từ 1990 đến 2009 (quá 16 năm tuổi, thuộc diện xe cũ sâu/xe cổ không phù hợp bài toán định giá đại chúng).
  - `MILEAGE_EXCEEDS_MAX`: **124 bản ghi (0.40%)** — Số ODO khai báo trên 1,000,000 km hoặc giá trị tràn số $2^{32}-1$.
  - `MISSING_YEAR`: **32 bản ghi (0.10%)** — Bị thiếu thông tin năm sản xuất.
  - `INVALID_TRANSMISSION`: **17 bản ghi (0.06%)** — Ghi ký tự '-' hoặc 'Số hỗn hợp'.
  - `TARGET_OUT_OF_BOUNDS`: **14 bản ghi (0.05%)** — 13 xe $< 30$ triệu và 1 xe $> 50$ tỷ.

### 5.3. Trùng lặp dữ liệu (Deduplication)
- Theo khóa chính `Mã tin`: **100.00% duy nhất** (30,652 tin đăng không trùng mã).
- Trùng lặp dòng dữ liệu tuyệt đối: **0 dòng** trong `car_detail.csv`; **248 dòng (0.81%)** trong `car_sell_processed.csv`.

---

## 6. Phân Tích Thiên Lệch Dữ Liệu & Rủi Ro Rò Rỉ (Data Leakage & Bias)

1. **Thiên lệch địa bàn (Geographical Bias)**:
   - Hà Nội chiếm **47.7% (14,612 xe)** và TP.HCM chiếm **18.5% (5,681 xe)**. Hai thành phố lớn chiếm tới **66.2%** dữ liệu.
   - Các tỉnh vùng cao hoặc miền Tây chiếm tỷ lệ rất nhỏ ($< 1\%$).
   - *Tác động đến mô hình*: Mô hình sẽ định giá rất chuẩn tại Hà Nội và TP.HCM, nhưng có thể kém nhạy bén ở các tỉnh địa phương. Phase 4 cần phân nhóm theo vùng kinh tế.
2. **Hiện tượng ODO bằng 0 (Zero-Mileage Inflation)**:
   - Có tới **10,442 xe có ODO = 0 km (34.07%)**.
   - Phân tích sâu cho thấy tập dữ liệu bao gồm cả xe mới 100% tại showroom đại lý (6,070 xe mới) và một số xe đã sử dụng nhưng người bán không khai báo ODO nên bị gán về 0.
   - *Khuyến nghị tiền xử lý*: Phân tách rõ ràng biến phân loại `is_new_car` hoặc chỉ giữ xe cũ có ODO $> 0$ cho bài toán Used Car.
3. **Giá trị ODO tràn số (Corrupted Outliers)**:
   - Cột `Số Km đã đi` trong tệp processed có giá trị cực đại là `4,294,967,295` ($2^{32}-1$). Bộ lọc validation của dự án đã nhận diện và cô lập thành công 124 bản ghi ngoại lai này.

---

## 7. Quyết Định Cổng & Điều Kiện Áp Dụng (Decision Gate Determination)

```text
STATUS: TECHNICALLY_AVAILABLE_LICENSE_PENDING
```

### Điều kiện sử dụng:
1. **Phạm vi được phép**: Sử dụng làm tập dữ liệu huấn luyện mẫu (Offline Benchmark Dataset) cho toàn bộ quy trình EDA (Phase 4), Feature Engineering & Data Preparation (Phase 5), và Huấn luyện mô hình (Phase 6–7) của mini project kết thúc khóa đào tạo AI.
2. **Phạm vi bị hạn chế**: Không sử dụng để xây dựng sản phẩm thương mại hoặc phát hành API thương mại ra bên ngoài.
3. **Đối với Track B (Crawler Oto.com.vn)**: Vẫn giữ nguyên trạng thái chờ phản hồi văn bản từ đơn vị sở hữu trước khi kích hoạt cào live. Nhánh Crawler đã có đầy đủ logic bóc tách và khử PII sẵn sàng hoạt động độc lập khi có phép.

---

## 8. Kế Hoạch Triển Khai Tiếp Theo (Roadmap for Phase 4)

Khi chuyển sang **Phase 4 (Exploratory Data Analysis - EDA)**:
1. Viết script làm sạch và chuẩn hóa dữ liệu từ `data/raw/external/mquaan_car_price/car_detail.csv` vào `data/processed/cars_clean.csv`.
2. Áp dụng các quy tắc tiền xử lý:
   - Lọc bỏ 3,423 bản ghi vi phạm hợp đồng validation (`year < 2010`, ODO ảo, thiếu năm).
   - Chuẩn hóa cột `Hãng` (sửa `'Mercedes Benz'` thành `'Mercedes-Benz'`).
   - Tách đặc trưng tuổi xe (`car_age = 2026 - year`).
   - Mã hóa các biến phân loại danh mục (`brand`, `transmission`, `fuel_type`, `origin`, `body_type`, `location_province`).
3. Khảo sát trực quan hóa:
   - Phân phối biến mục tiêu $\ln(y)$ để xử lý độ lệch phải (Right-skewness).
   - Ma trận tương quan giữa giá với tuổi xe, số ODO, dung tích động cơ.
   - Phân tích ANOVA để đánh giá ảnh hưởng của thương hiệu đến giá bán.
