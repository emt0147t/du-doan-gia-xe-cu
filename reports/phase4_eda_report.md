# Báo Cáo Khám Phá Dữ Liệu & Kiểm Toán Chất Lượng Dữ Liệu Thực Tế
*(Phase 4 — Exploratory Data Analysis & Data Quality Investigation Report)*

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam (Used Car Price Prediction in Vietnam)
- **Giai đoạn**: Phase 4 — Exploratory Data Analysis & Data Quality Investigation
- **Thời gian lập**: 19/10/2026, 02:35:00 (Múi giờ: Asia/Ho_Chi_Minh)
- **Người thực hiện**: Senior Data Scientist, ML Engineer & AI Student
- **Môi trường thực thi**: Windows 11, Python `3.11.9`, pandas `2.2.3`, numpy `2.2.6`, matplotlib `3.10.8`, seaborn `0.13.2`, scipy `1.17.1`
- **Tài liệu tham chiếu**: [Data Dictionary](file:///d:/ai-club-end-training/docs/data_dictionary.md), [Schema Mapping](file:///d:/ai-club-end-training/docs/schema_mapping.md), [Cleaning Policy](file:///d:/ai-club-end-training/docs/eda_findings_and_cleaning_policy.md), [Jupyter Notebook](file:///d:/ai-club-end-training/notebooks/04_eda.ipynb)

---

## 1. Tóm Tắt Kết Quả Điều Tra (Executive Summary)

Trong Phase 4, toàn bộ tập dữ liệu thị trường thực tế gồm **30,652 bản ghi** đã được nạp, kiểm định toàn vẹn mã băm SHA-256, và phân tích khám phá chuyên sâu (EDA) thông qua notebook tái lập [notebooks/04_eda.ipynb](file:///d:/ai-club-end-training/notebooks/04_eda.ipynb) và hệ thống **19 biểu đồ kỹ thuật** tại [reports/figures/phase4/](file:///d:/ai-club-end-training/reports/figures/phase4).

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                 BẢNG CHỈ SỐ KHÁM PHÁ DỮ LIỆU CỐT LÕI (PHASE 4 EDA)          │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ Quy mô tập dữ liệu thô               │ 30,652 dòng x 21 cột (car_detail.csv)│
│ Mã băm toàn vẹn SHA-256              │ 44c13afc5982f7abc51611fc56eeefd02df8e│
│                                      │ 47f3224112f51b76514a7328f08 (Khớp 100%│
│ Tỷ lệ bóc tách giá thành công        │ 100.00% (30,652 / 30,652 bản ghi)    │
│ Giá trị biến mục tiêu (Trung vị)     │ 620,000,000 VND (620 triệu VND)      │
│ Giá trị biến mục tiêu (Trung bình)   │ 1,180,744,682 VND (~1.18 tỷ VND)     │
│ Độ lệch phân phối giá (Skewness)     │ Thô: 7.82 (Lệch phải) -> Log: 0.68   │
│ Tỷ lệ xe đã qua sử dụng vs Xe mới    │ 80.2% Xe đã dùng vs 19.8% Xe mới     │
│ Tỷ trọng xe sản xuất từ năm 2010     │ 27,317 xe (89.21% tổng số tin)       │
│ Tỷ trọng 2 thị trường Hà Nội & TP.HCM│ 66.2% tổng lượng tin rao toàn quốc   │
│ Số lượng biểu đồ kỹ thuật được sinh  │ 19 biểu đồ chất lượng cao (Phase 4)   │
│ Quy mô tập dữ liệu sạch cho Phase 5  │ 27,229 bản ghi chuẩn mực (88.83%)    │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

---

## 2. Nguồn Gốc, Tính Toàn Vẹn & Phạm Vi Dữ Liệu

### 2.1. Xác minh tệp và mã băm SHA-256
Quá trình kiểm tra độc lập bằng module [src/data/load_dataset.py](file:///d:/ai-club-end-training/src/data/load_dataset.py) khẳng định tính toàn vẹn tuyệt đối:
- **Tệp chính `car_detail.csv`**: Kích thước 21,355,297 bytes. Mã SHA-256: `44c13afc5982f7abc51611fc56eeefd02df8e47f3224112f51b76514a7328f08` (khớp 100% với tệp sidecar `.sha256` và siêu dữ liệu tại [data/metadata/ingestion_mquaan_car_price.json](file:///d:/ai-club-end-training/data/metadata/ingestion_mquaan_car_price.json)).
- **Tệp phụ `car_sell_processed.csv`**: Kích thước 6,452,999 bytes. Mã SHA-256: `1d0c0d2f5a920f19eee09cffc84f30c7bc7496ac5bcb35260ccfbbd93c89437c` (khớp 100%).

### 2.2. Mối quan hệ giữa hai bảng dữ liệu & Nguyên tắc liêm chính
- **Bảng `car_detail.csv`** là dữ liệu tin rao gốc thu thập từ Bonbanh.com, chứa đầy đủ khóa định danh `Mã tin`, chuỗi giá tiếng Việt gốc, mô tả chi tiết và URL bài đăng.
- **Bảng `car_sell_processed.csv`** là bảng dẫn xuất do tác giả repository xử lý sơ bộ: đã lược bỏ `Mã tin`, URL, mô tả; làm sạch giá thành triệu VND và gán mã tỉnh thành.
- **Nguyên tắc kỹ thuật**: Nhóm không nối hai bảng theo vị trí dòng (Index-based join) nhằm tránh rủi ro lệch dòng tiềm ẩn. `car_detail.csv` được sử dụng làm **bảng phân tích chính**, trong khi trường `Tỉnh` từ bảng processed chỉ được khảo sát độc lập để đánh giá tính đại diện địa lý.

---

## 3. Rà Soát Schema & Từ Điển Dữ Liệu (Schema Mapping Review)

Đối chiếu 14 trường dữ liệu chuẩn theo [docs/schema_mapping.md](file:///d:/ai-club-end-training/docs/schema_mapping.md):

```text
Trường chuẩn dự án      Cột gốc (car_detail.csv)   Kiểu dữ liệu   Đánh giá trạng thái ánh xạ
─────────────────────────────────────────────────────────────────────────────────────────────
price_vnd               Giá                        str -> int64   Needs Unit Conversion (Parse 100%)
brand                   Hãng                       str -> str     Needs Normalization (Trim, gạch nối)
model                   Grade                      str -> str     Needs Normalization (Chuẩn hóa chuỗi)
year                    Năm sản xuất               float -> int   Directly Mapped (Khuyết 0.1%)
mileage_km              Số Km đã đi                str -> float   Needs Unit Conversion (Bỏ ' Km', ',')
fuel_type               Động cơ                    str -> str     Needs Normalization (Tách từ Động cơ)
transmission            Hộp số                     str -> str     Needs Normalization (Tự động vs Sàn)
origin                  Xuất xứ                    str -> str     Directly Mapped (Trong nước / Nhập)
body_type               Dòng xe                    str -> str     Directly Mapped (SUV, Sedan...)
seats                   Số chỗ ngồi                str -> int     Needs Unit Conversion (Bóc tách số)
listing_id              Mã tin                     int64          Directly Mapped (Khóa duy nhất)
location_province       (Tham chiếu df_proc)       str            Unverified in primary table
source_url              URL                        str            Directly Mapped (Kiểm chứng gốc)
crawl_date              (Không có trong bảng)      -              UNAVAILABLE (Mốc 2023-2024)
```

---

## 4. Hồ Sơ Chất Lượng Dữ Liệu (Data Quality Profile)

### 4.1. Khuyết thiếu dữ liệu (Missing Values)
- Xem [Hình 19: Tỷ lệ khuyết thiếu theo từng cột](file:///d:/ai-club-end-training/reports/figures/phase4/fig19_missing_rate_by_column.png).
- **Trường khuyết duy nhất trong các biến cốt lõi**: `Năm sản xuất` bị khuyết **32 dòng (0.10%)**.
- **Trường khuyết trong các biến tùy chọn**: `Hệ thống nạp nhiên liệu` bị khuyết **23,907 dòng (77.99%)**.
- Toàn bộ 19 trường còn lại trong `car_detail.csv` đều có tỷ lệ điền đầy **100.00%**.

### 4.2. Trùng lặp (Deduplication)
- Khóa chính `Mã tin`: Đạt **30,652 / 30,652 giá trị duy nhất (100.00%)**. Không có bất kỳ mã tin nào bị lặp lại.
- Trùng lặp toàn bộ dòng: `car_detail.csv` có **0 bản ghi trùng lặp tuyệt đối**.

### 4.3. Kiểm toán bóc tách giá (`price_vnd`)
- Hàm `parse_vietnamese_price_to_vnd` bóc tách thành công **30,652 / 30,652 tin đăng (100.00%)**.
- Số tin dưới 30 triệu VND: 13 tin (0.04%) — chủ yếu là tiền đặt cọc hoặc giá xác xe.
- Số tin trên 50 tỷ VND: 1 tin (0.003%) — xe Rolls-Royce Phantom 54 tỷ VND.
- Số tin nằm trong biên hợp lệ $[30\text{M}, 50\text{B}]$: **30,638 tin (99.95%)**.

### 4.4. Tính hợp lệ của các biến định lượng (Numeric Validity)
- **Năm sản xuất**: Dải năm từ **1990** đến **2023**.
  - Xe trước năm 2010: 3,303 xe (10.78%).
  - Xe từ năm 2010 đến 2023: 27,317 xe (89.21%).
- **Số kilomet đã đi (Mileage)**:
  - Giá trị nhỏ nhất: 0 km. Có **10,442 xe có ODO = 0 km (34.07%)**.
  - Xe có ODO $> 1,000,000$ km: 124 xe (0.40%). Trong bảng processed xuất hiện giá trị lính canh $4,294,967,295$ km ($2^{32}-1$).

---

## 5. Phân Tích Biến Mục Tiêu `price_vnd` (Target Variable Analysis)

- Xem [Hình 1: Phân phối giá niêm yết](file:///d:/ai-club-end-training/reports/figures/phase4/fig01_target_price_distribution.png), [Hình 2: Boxplot giá niêm yết](file:///d:/ai-club-end-training/reports/figures/phase4/fig02_target_price_boxplot.png) và [Hình 3: Phân phối Logarithm ln(price)](file:///d:/ai-club-end-training/reports/figures/phase4/fig03_target_log1p_distribution.png).

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                 THỐNG KÊ MÔ TẢ BIẾN MỤC TIÊU PRICE_VND                      │
├──────────────────────────────┬──────────────────────────────────────────────┤
│ Số lượng quan sát (Count)    │ 30,652 tin đăng                              │
│ Giá trị nhỏ nhất (Min)       │ 18,000,000 VND (18 triệu)                    │
│ Phân vị 25% (Q1)             │ 410,000,000 VND (410 triệu)                  │
│ Trung vị 50% (Median)        │ 620,000,000 VND (620 triệu)                  │
│ Giá trị trung bình (Mean)    │ 1,180,744,682 VND (~1.18 tỷ)                 │
│ Phân vị 75% (Q3)             │ 1,030,000,000 VND (1.03 tỷ)                  │
│ Giá trị lớn nhất (Max)       │ 54,000,000,000 VND (54 tỷ)                   │
│ Độ lệch chuẩn (Std)          │ 2,068,362,485 VND (~2.07 tỷ)                 │
│ Hệ số bất đối xứng (Skewness)│ Thô: 7.82 (Lệch phải nặng) -> ln(y): 0.68    │
└──────────────────────────────┴──────────────────────────────────────────────┘
```

### Nhận định chuyên sâu:
- **Quan sát (Observation)**: Mean (1.18 tỷ) cao gần gấp đôi Median (620 triệu). Đuôi phân phối kéo dài tới 54 tỷ VND do các dòng xe siêu sang (Rolls-Royce, Bentley, Maybach, Porsche).
- **Diễn giải (Interpretation)**: Thị trường ô tô Việt Nam có sự phân hóa giai tầng rất rõ: phân khúc phổ thông đại chúng (300M - 900M) chiếm đại đa số, trong khi phân khúc xe sang chiếm tỷ trọng nhỏ nhưng có giá trị cực cao, kéo dãn phân phối.
- **Giả thuyết mô hình hóa (Hypothesis)**: Huấn luyện trực tiếp trên $y$ thô sẽ khiến các thuật toán hồi quy bị chi phối mạnh bởi sai số bình phương lớn từ nhóm xe sang. Áp dụng biến đổi logarit $\ln(y)$ đưa Skewness từ $7.82$ về $0.68$ (phân phối chuẩn đối xứng, [Hình 3](file:///d:/ai-club-end-training/reports/figures/phase4/fig03_target_log1p_distribution.png)), sẽ cải thiện đáng kể độ hội tụ và giảm chỉ số sai số phần trăm tuyệt đối MAPE.

---

## 6. Phân Tích Các Đặc Trưng Nghiệp Vụ Cốt Lõi

### 6.1. Năm sản xuất và Tuổi xe (Year & Car Age)
- Xem [Hình 4: Phân phối giá theo năm](file:///d:/ai-club-end-training/reports/figures/phase4/fig04_price_distribution_by_year.png), [Hình 5: Xu hướng trung vị giá theo năm](file:///d:/ai-club-end-training/reports/figures/phase4/fig05_median_price_trend_by_year.png) và [Hình 6: Số lượng tin theo năm](file:///d:/ai-club-end-training/reports/figures/phase4/fig06_record_count_by_year.png).
- **Quan sát**: Trung vị giá tăng đơn điệu từ 2011 (320 triệu) đến 2022 (760 triệu) và 2023 (850 triệu). Lượng tin đăng tập trung dày đặc nhất ở các đời xe từ 2016 đến 2022 (chiếm hơn 65% thị trường).
- **Diễn giải**: Ô tô tại Việt Nam chịu mức độ khấu hao mạnh nhất trong 3–5 năm đầu tiên, sau đó tốc độ giảm giá chậm dần. Đối với xe sản xuất trước 2010, trung vị giá đi ngang quanh mốc 150M–250M VND.
- **Giả thuyết**: Đặc trưng `car_age = 2024 - year` có quan hệ phi tuyến dạng hàm mũ hoặc logarit với giá trị xe.

### 6.2. Thương hiệu xe (Brand Analysis)
- Xem [Hình 7: Top 12 thương hiệu](file:///d:/ai-club-end-training/reports/figures/phase4/fig07_top_brands_by_count.png), [Hình 8: Trung vị giá top thương hiệu](file:///d:/ai-club-end-training/reports/figures/phase4/fig08_median_price_by_top_brands.png) và [Hình 9: Hộp giá 8 thương hiệu dẫn đầu](file:///d:/ai-club-end-training/reports/figures/phase4/fig09_price_distribution_selected_brands.png).
- **Quan sát**:
  - Top 5 hãng xe áp đảo thị phần tin rao: **Toyota** (5,592 xe - 18.2%), **Hyundai** (3,555 xe - 11.6%), **Ford** (3,370 xe - 11.0%), **Mercedes-Benz** (3,191 xe - 10.4%), **Kia** (2,991 xe - 9.8%).
  - Trung vị giá có sự phân tầng rõ rệt:
    - Nhóm bình dân: Kia (515M), Hyundai (535M), Chevrolet (310M).
    - Nhóm trung cấp: Toyota (615M), Mazda (625M), Honda (620M), Ford (690M).
    - Nhóm cận sang & sang: Mercedes-Benz (1.49 tỷ), Lexus (2.19 tỷ).
- **Diễn giải**: Thương hiệu là một trong những yếu tố phân loại có sức mạnh giải thích phương sai giá lớn nhất.

### 6.3. Số Kilomet đã đi (Mileage Analysis)
- Xem [Hình 10: Phân phối số ODO](file:///d:/ai-club-end-training/reports/figures/phase4/fig10_mileage_distribution.png), [Hình 11: Scatter ODO vs Giá](file:///d:/ai-club-end-training/reports/figures/phase4/fig11_mileage_vs_price_scatter.png) và [Hình 12: Phân tích đa biến Giá - ODO - Năm](file:///d:/ai-club-end-training/reports/figures/phase4/fig12_year_mileage_price_multivariate.png).
- **Quan sát**:
  - Xuất hiện đỉnh nhọn bất thường tại mốc $0\text{ km}$ với **10,442 xe (34.07%)**.
  - Đối với các xe có ODO $> 0$, số kilomet phân bố tập trung từ 20,000 km đến 120,000 km (Trung vị: 50,000 km).
  - Tương quan tuyến tính đơn biến giữa ODO và giá là âm nhẹ ($r = -0.10$).
- **Diễn giải**: Hiện tượng ODO = 0 bắt nguồn từ hai nhóm: xe mới 100% tại đại lý showroom (6,070 xe) và xe cũ người bán bỏ trống trường ODO nên hệ thống tự điền 0. Khi xe có ODO = 0 thì giá lại cao (do xe mới), làm triệt tiêu mối tương quan nghịch đảo tự nhiên giữa số km và giá nếu không kiểm soát biến `is_new_car` hoặc `year`.
- **Giả thuyết**: Tương quan thực chất giữa ODO và giá chỉ bộc lộ rõ ràng khi xét *trong cùng một năm sản xuất và cùng một phân khúc xe*.

### 6.4. Các đặc trưng phân loại khác (Categorical Analysis)
- Xem [Hình 13: Giá theo tình trạng](file:///d:/ai-club-end-training/reports/figures/phase4/fig13_price_by_condition.png), [Hình 14: Giá theo hộp số](file:///d:/ai-club-end-training/reports/figures/phase4/fig14_price_by_transmission.png), [Hình 15: Giá theo xuất xứ](file:///d:/ai-club-end-training/reports/figures/phase4/fig15_price_by_origin.png) và [Hình 16: Giá theo kiểu dáng](file:///d:/ai-club-end-training/reports/figures/phase4/fig16_price_by_body_type.png).
- **Tình trạng xe (Condition)**: Xe mới có trung vị giá 860 triệu VND, cao hơn đáng kể so với xe đã qua sử dụng (585 triệu VND).
- **Hộp số (Transmission)**: Xe số tự động chiếm 82.0% với trung vị giá 680 triệu VND; xe số sàn chiếm 17.9% với trung vị giá chỉ 350 triệu VND (chủ yếu là xe dịch vụ, xe tải nhỏ hoặc xe hạng A).
- **Xuất xứ (Origin)**: Xe nhập khẩu có trung vị giá 790 triệu VND, cao hơn xe lắp ráp trong nước (550 triệu VND) do phải chịu thuế nhập khẩu và định vị ở các phân khúc cao cấp hơn.
- **Kiểu dáng (Body Type)**: SUV và Crossover có phân phối giá rộng và trung vị cao nhất (750M - 950M), theo sau là Sedan (550M), Hatchback (380M) và Truck (250M).

---

## 7. Phân Tích Địa Bàn & Thiên Lệch Chọn Mẫu (Geo-Source & Representativeness)

- Xem [Hình 18: Phân bố địa bàn và trung vị giá](file:///d:/ai-club-end-training/reports/figures/phase4/fig18_top_provinces_count_and_median_price.png).
- **Mức độ tập trung địa lý**:
  - **Hà Nội**: 14,612 xe (**47.7%**).
  - **TP. Hồ Chí Minh**: 5,681 xe (**18.5%**).
  - Hai đô thị đặc biệt chiếm tới **66.2%** tổng lượng tin đăng toàn quốc.
  - Các tỉnh thành tiếp theo: Hải Phòng (3.1%), Bình Dương (2.8%), Đồng Nai (2.0%), Đắk Lắk (1.8%), Đà Nẵng (1.4%).
- **Trung vị giá theo địa bàn**: Hà Nội và TP.HCM có trung vị giá tương đồng nhau (~640M - 650M VND); trong khi các tỉnh Tây Nguyên (Đắk Lắk) có trung vị giá thấp hơn (~520M) do tỷ lệ xe bán tải và xe phổ thông đời sâu cao hơn.

### Cảnh báo rủi ro thiên lệch chọn mẫu (Selection Bias Caveats):
1. **Thiên lệch nguồn tin trực tuyến**: Dữ liệu chỉ phản ánh hành vi rao bán trên internet; các giao dịch xe cũ truyền thống tại các vùng nông thôn hoặc qua người quen không được ghi nhận.
2. **Thiên lệch salon chuyên nghiệp**: Các salon lớn tại Hà Nội và TP.HCM có tần suất đăng tin dày đặc và bài bản hơn người bán cá nhân, khiến tỷ trọng xe lướt đời cao tại hai thành phố này bị phóng đại.
3. **Giá rao bán vs Giá giao dịch**: Giá trong tập dữ liệu là *Asking Price* (giá chào bán), thường có biên độ thương lượng giảm từ 2% đến 5% khi chốt hợp đồng thực tế.

---

## 8. Khảo Sát Tương Quan Định Lượng (Correlation Analysis)

- Xem [Hình 17: Ma trận tương quan Pearson](file:///d:/ai-club-end-training/reports/figures/phase4/fig17_correlation_heatmap.png).

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                 MA TRẬN HỆ SỐ TƯƠNG QUAN TUYẾN TÍNH PEARSON (r)             │
├─────────────────────────┬──────────────┬────────────┬───────────┬───────────┤
│ Biến số                 │ price_billion│ log_price  │ year      │ mileage_km│
├─────────────────────────┼──────────────┼────────────┼───────────┼───────────┤
│ price_billion           │     1.00     │    0.72    │    0.28   │   -0.08   │
│ log_price               │     0.72     │    1.00    │    0.52   │   -0.19   │
│ year (Năm sản xuất)     │     0.28     │    0.52    │    1.00   │   -0.41   │
│ car_age (Tuổi xe)       │    -0.28     │   -0.52    │   -1.00   │    0.41   │
│ mileage_km (Số ODO)     │    -0.08     │   -0.19    │   -0.41   │    1.00   │
│ engine_displacement_l   │     0.46     │    0.49    │    0.04   │    0.08   │
│ seats (Số chỗ ngồi)     │     0.11     │    0.14    │    0.02   │    0.07   │
└─────────────────────────┴──────────────┴────────────┴───────────┴───────────┘
```

> [!IMPORTANT]
> **Diễn giải phương pháp luận**:
> 1. Tương quan mạnh nhất với biến mục tiêu $\ln(y)$ là **Năm sản xuất** ($r = 0.52$) và **Dung tích động cơ** ($r = 0.49$). Xe càng mới và động cơ càng lớn thì giá trị càng cao.
> 2. Tương quan tuyến tính đơn biến của `mileage_km` với giá thấp ($r = -0.19$ với log_price) vì bị pha loãng bởi nhóm 34% xe ODO = 0 km và sự khác biệt giữa các thương hiệu (một chiếc Lexus đi 100,000 km vẫn đắt hơn nhiều một chiếc Kia mới đi 10,000 km).
> 3. Tương quan Pearson chỉ đo lường mối quan hệ tuyến tính; không phát hiện được các mối quan hệ phi tuyến phức tạp mà các mô hình cây quyết định (Random Forest, LightGBM) có thể khai thác.

---

## 9. Đề Xuất Chính Sách Làm Sạch Dữ Liệu Cho Phase 5

Chi tiết xem tại tài liệu quy chuẩn [docs/eda_findings_and_cleaning_policy.md](file:///d:/ai-club-end-training/docs/eda_findings_and_cleaning_policy.md):

1. **Phân đoạn năm sản xuất (Scope Definition)**: Giữ các xe có `year >= 2010` để phục vụ bài toán định giá xe đại chúng thương mại (loại bỏ 3,303 xe cổ từ 1990 - 2009 có cơ chế định giá sưu tầm phi chuẩn).
2. **Khử lỗi tràn số ODO**: Gán các giá trị ODO $> 1,000,000$ km và $4,294,967,295$ km ($2^{32}-1$) về `NaN` hoặc lọc bỏ 124 dòng lỗi kỹ thuật này.
3. **Xử lý hiện tượng ODO = 0**: Không xóa bỏ; sinh đặc trưng nhị phân `is_zero_mileage` kết hợp biến `condition` để mô hình tự học sự khác biệt giữa xe mới showroom và xe cũ thiếu ODO.
4. **Lọc biên giá mục tiêu**: Giữ các tin đăng trong khoảng $[30\text{ triệu}, 50\text{ tỷ VND}]$ (loại bỏ 13 tin đặt cọc ảo $< 30$M và 1 siêu xe cá biệt 54B).
5. **Chuẩn hóa danh mục**: Sửa `'Mercedes Benz'` thành `'Mercedes-Benz'`; xử lý 17 tin có hộp số `'-'` hoặc `'Số hỗn hợp'`.
6. **Quy mô dữ liệu chuẩn đầu ra**: Sau khi áp dụng đầy đủ chính sách, tập dữ liệu sạch đạt **27,229 bản ghi (88.83%)** hoàn toàn sẵn sàng cho Feature Engineering và Model Training.

---

## 10. Danh Mục 19 Biểu Đồ Kỹ Thuật Được Tạo Tại Phase 4

Toàn bộ các biểu đồ được lưu trữ tại thư mục [reports/figures/phase4/](file:///d:/ai-club-end-training/reports/figures/phase4):

1. [fig01_target_price_distribution.png](file:///d:/ai-club-end-training/reports/figures/phase4/fig01_target_price_distribution.png) - Histogram phân phối giá niêm yết (<= 5 tỷ).
2. [fig02_target_price_boxplot.png](file:///d:/ai-club-end-training/reports/figures/phase4/fig02_target_price_boxplot.png) - Boxplot phân vị giá thô và boxplot phóng to.
3. [fig03_target_log1p_distribution.png](file:///d:/ai-club-end-training/reports/figures/phase4/fig03_target_log1p_distribution.png) - Histogram sau biến đổi $\ln(\text{price})$.
4. [fig04_price_distribution_by_year.png](file:///d:/ai-club-end-training/reports/figures/phase4/fig04_price_distribution_by_year.png) - Phân phối giá theo từng năm sản xuất.
5. [fig05_median_price_trend_by_year.png](file:///d:/ai-club-end-training/reports/figures/phase4/fig05_median_price_trend_by_year.png) - Đường xu hướng trung vị giá theo năm.
6. [fig06_record_count_by_year.png](file:///d:/ai-club-end-training/reports/figures/phase4/fig06_record_count_by_year.png) - Số lượng quan sát theo từng năm.
7. [fig07_top_brands_by_count.png](file:///d:/ai-club-end-training/reports/figures/phase4/fig07_top_brands_by_count.png) - Top 12 thương hiệu có nhiều tin nhất.
8. [fig08_median_price_by_top_brands.png](file:///d:/ai-club-end-training/reports/figures/phase4/fig08_median_price_by_top_brands.png) - Trung vị giá theo top 12 thương hiệu.
9. [fig09_price_distribution_selected_brands.png](file:///d:/ai-club-end-training/reports/figures/phase4/fig09_price_distribution_selected_brands.png) - Boxplot phân phối giá 8 hãng lớn.
10. [fig10_mileage_distribution.png](file:///d:/ai-club-end-training/reports/figures/phase4/fig10_mileage_distribution.png) - Phân phối số kilomet và đỉnh ODO = 0.
11. [fig11_mileage_vs_price_scatter.png](file:///d:/ai-club-end-training/reports/figures/phase4/fig11_mileage_vs_price_scatter.png) - Scatter ODO vs Giá (lấy mẫu $n=5,000$).
12. [fig12_year_mileage_price_multivariate.png](file:///d:/ai-club-end-training/reports/figures/phase4/fig12_year_mileage_price_multivariate.png) - Phân tích đa biến Giá - ODO - Năm.
13. [fig13_price_by_condition.png](file:///d:/ai-club-end-training/reports/figures/phase4/fig13_price_by_condition.png) - Giá theo tình trạng (Xe mới vs Xe cũ).
14. [fig14_price_by_transmission.png](file:///d:/ai-club-end-training/reports/figures/phase4/fig14_price_by_transmission.png) - Giá theo hộp số (Tự động vs Sàn).
15. [fig15_price_by_origin.png](file:///d:/ai-club-end-training/reports/figures/phase4/fig15_price_by_origin.png) - Giá theo xuất xứ (Trong nước vs Nhập khẩu).
16. [fig16_price_by_body_type.png](file:///d:/ai-club-end-training/reports/figures/phase4/fig16_price_by_body_type.png) - Giá theo kiểu dáng xe (Body type).
17. [fig17_correlation_heatmap.png](file:///d:/ai-club-end-training/reports/figures/phase4/fig17_correlation_heatmap.png) - Ma trận tương quan Pearson các biến số.
18. [fig18_top_provinces_count_and_median_price.png](file:///d:/ai-club-end-training/reports/figures/phase4/fig18_top_provinces_count_and_median_price.png) - Tỷ trọng và trung vị giá theo tỉnh thành.
19. [fig19_missing_rate_by_column.png](file:///d:/ai-club-end-training/reports/figures/phase4/fig19_missing_rate_by_column.png) - Tỷ lệ khuyết thiếu trên 21 cột thô.

---

## 11. Các Câu Hỏi Nghiên Cứu Cần Kiểm Tra Tại Giai Đoạn Huấn Luyện Mô Hình (Phase 6)

1. **Hiệu quả biến đổi biến mục tiêu**: Liệu huấn luyện trên $\ln(y)$ có mang lại $R^2$ và MAPE tốt hơn vượt trội so với huấn luyện trực tiếp trên $y$ thô hay không?
2. **Đóng góp của thông tin ODO = 0**: Đặc trưng nhị phân `is_zero_mileage` có giúp cây quyết định phân biệt được xe mới tại showroom và xe cũ bị thiếu ODO hay không?
3. **Mức độ phi tuyến của khấu hao**: Giữa mô hình hồi quy tuyến tính có hiệu chỉnh (Ridge/Lasso) và các mô hình dựa trên cây (Random Forest, LightGBM, XGBoost), mô hình nào xử lý tốt hơn mối quan hệ phi tuyến giữa tuổi xe, dung tích động cơ và giá bán?
4. **Khả năng khái quát hóa địa phương**: Một mô hình được huấn luyện với 66.2% dữ liệu từ Hà Nội và TP.HCM có đạt sai số chấp nhận được khi dự đoán cho xe tại các tỉnh miền Trung và miền Tây hay không?
