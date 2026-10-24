# Từ Điển Dữ Liệu Mô Hình Hóa (Phase 5 Data Dictionary)

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam (Used Car Price Prediction in Vietnam)
- **Giai đoạn**: Phase 5 — Data Cleaning, Feature Engineering & Preprocessing Pipeline
- **Tập dữ liệu áp dụng**: [data/processed/cars_clean_phase5.csv](file:///d:/ai-club-end-training/data/processed/cars_clean_phase5.csv)
- **Quy mô**: 23,510 bản ghi $\times$ 38 trường thông tin

---

## 1. Phân Loại Vai Trò Các Biến Trong Mô Hình Hóa (Modeling Role Taxonomy)

Tập dữ liệu ứng viên được chia thành 4 nhóm vai trò rõ ràng để ngăn chặn triệt để nguy cơ **Data Leakage**:

1. **Target ($y$)**: Biến mục tiêu cần dự đoán (`price_vnd`, `log_price`).
2. **Features ($X$)**: Các đặc trưng kỹ thuật và hành vi được đưa vào pipeline tiền xử lý để huấn luyện mô hình.
3. **Identifiers / Provenance**: Các trường định danh dùng cho việc kiểm toán vết dữ liệu, truy xuất nguồn gốc, hoặc phân nhóm split (không đưa vào feature matrix $X$).
4. **Excluded / Leakage Risk**: Các trường bị loại bỏ hoàn toàn khỏi mô hình do rủi ro rò rỉ thông tin giá, thông tin liên hệ PII, hoặc tỷ lệ khuyết quá cao.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       CƠ CẤU BIẾN DỮ LIỆU PHASE 5                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ TARGET (y)           : price_vnd (VND), log_price (ln(VND))                 │
│ NUMERIC FEATURES (X) : year, car_age, mileage_km, is_zero_mileage,          │
│                        engine_displacement_l, seats, doors, is_luxury_brand │
│ CATEGORICAL FEAT (X) : brand, model, condition, transmission, origin,       │
│                        body_type, fuel_type                                 │
│ IDENTIFIERS / AUDIT  : listing_id (Mã tin), url (URL), Tên xe               │
│ EXCLUDED / LEAKAGE   : Giá (raw), price_vnd, log_price, Mô tả,              │
│                        Hệ thống nạp nhiên liệu (>78% missing)               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Bảng Mô Tả Chi Tiết Từng Cột (Detailed Column Specifications)

### 2.1. Biến Mục Tiêu (Target Variables)

| Tên cột | Kiểu dữ liệu | Cột nguồn gốc | Vai trò mô hình | Định nghĩa & Ý nghĩa nghiệp vụ | Nguy cơ Leakage |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `price_vnd` | `float64` | `Giá` | **Primary Target ($y$)** | Giá rao bán xe tính theo Đồng Việt Nam (VND). Miền giá trị: 72,000,000 – 47,000,000,000 VND. | **Rất cao (Target)**. Cấm xuất hiện trong $X$. |
| `log_price` | `float64` | `price_vnd` | **Transformed Target** | $\ln(\text{price\_vnd})$, dùng làm nhãn mục tiêu cho hồi quy tuyến tính và gradient boosting để giảm skewness. | **Rất cao (Target)**. Cấm xuất hiện trong $X$. |

### 2.2. Đặc Trưng Định Lượng (Numeric Features - $X$)

| Tên cột | Kiểu dữ liệu | Cột nguồn gốc | Khoảng giá trị | Xử lý Missing trong Pipeline | Rủi ro Leakage |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `year` | `float64` | `Năm sản xuất`| $2015 - 2023$ | Không có missing trong Cohort A. | Không |
| `car_age` | `float64` | `Năm sản xuất`| $1 - 9$ (năm) | Tính bằng $\max(0, 2024 - \text{year})$. Mốc 2024 cố định theo thời gian cào dữ liệu. | Không |
| `mileage_km` | `float64` | `Số Km đã đi`| $0 - 780,000$ km| 0 km giữ nguyên; missing trong test impute bằng median của train set. | Không |
| `is_zero_mileage`| `int64` | `Số Km đã đi`| $0, 1$ | Nhị phân: 1 nếu ODO = 0 km, 0 nếu ODO > 0 km. | Không |
| `engine_displacement_l`| `float64`| `Động cơ` | $0.8 - 6.7$ L | Missing 4.28% -> `SimpleImputer(strategy='median', add_indicator=True)`. | Không |
| `seats` | `float64` | `Số chỗ ngồi` | $2 - 47$ chỗ | Bóc tách bằng regex. Fallback median nếu khuyết. | Không |
| `doors` | `float64` | `Số cửa` | $2 - 5$ cửa | Bóc tách bằng regex. Fallback median nếu khuyết. | Không |
| `is_luxury_brand` | `int64` | `Hãng` | $0, 1$ | 1 nếu thuộc danh mục xe sang (Mercedes, BMW, Lexus, Porsche,...), 0 nếu phổ thông. | Không |

### 2.3. Đặc Trưng Phân Loại (Categorical Features - $X$)

| Tên cột | Kiểu dữ liệu | Cột nguồn gốc | Số nhãn duy nhất | Ví dụ giá trị | Chuẩn hóa & Mã hóa |
| :--- | :--- | :--- | :---: | :--- | :--- |
| `brand` | `object` | `Hãng` | 51 hãng | Toyota, Hyundai, Mercedes-Benz, Kia, Mazda, Ford | One-Hot Encoding (`handle_unknown='ignore'`). |
| `model` | `object` | `Grade` | 586 dòng | Vios, Accent, CX-5, Ranger, GLC 300, Morning | One-Hot Encoding (`handle_unknown='ignore'`). |
| `condition` | `object` | `Tình trạng` | 2 nhãn | `Xe đã dùng`, `Xe mới` | One-Hot Encoding. Phân biệt xe lướt và xe nguyên bản. |
| `transmission` | `object` | `Hộp số` | 2 nhãn | `Tự động`, `Số tay` | One-Hot Encoding. |
| `origin` | `object` | `Xuất xứ` | 2 nhãn | `Trong nước`, `Nhập khẩu` | One-Hot Encoding. |
| `body_type` | `object` | `Dòng xe` | 9 nhãn | SUV, Sedan, Bán tải / Pickup, Crossover, Hatchback | One-Hot Encoding. |
| `fuel_type` | `object` | `Động cơ` | 4 nhãn | `Xăng`, `Dầu`, `Hybrid`, `Điện` | One-Hot Encoding. |

### 2.4. Trường Định Danh & Kiểm Toán Nguồn Gốc (Identifiers & Provenance - Excluded from $X$)

| Tên cột | Kiểu dữ liệu | Cột nguồn gốc | Mục đích sử dụng | Rủi ro Leakage nếu đưa vào $X$ |
| :--- | :--- | :--- | :--- | :--- |
| `listing_id` | `object` | `Mã tin` | Định danh tin rao; dùng để phân định train/val/test splits không trùng lặp. | **Cao**. ID có thể mã hóa thứ tự thời gian hoặc salon. **Cấm vào $X$**. |
| `url` | `object` | `URL` | Kiểm chứng nguồn gốc tin đăng trên sàn giao dịch. | **Cao**. Chuỗi URL chứa slug có thể hé lộ giá hoặc ID. **Cấm vào $X$**. |
| `Tên xe` | `object` | `Tên xe` | Tiêu đề tin đăng phục vụ người dùng đọc hiểu. | **Trung bình - Cao**. Có thể chứa từ ngữ gợi ý giá. **Cấm vào $X$**. |

### 2.5. Các Trường Bị Loại Bỏ Hoàn Toàn (Excluded Columns)

| Tên cột | Lý do loại bỏ khỏi ma trận đặc trưng $X$ |
| :--- | :--- |
| `Giá` (chuỗi thô) | Rò rỉ nhãn mục tiêu trực tiếp 100% (Target Leakage). |
| `Mô tả` | Chứa số điện thoại người bán (PII) và câu chữ chứa trực tiếp giá bán đàm phán. |
| `Hệ thống nạp nhiên liệu` | Tỷ lệ dữ liệu bị khuyết quá cao (>78.5%), gây nhiễu nếu thực hiện imputation. |
| `Màu ngoại thất`, `Màu nội thất` | Đa dạng màu sắc tự do nhưng tỷ lệ tương quan yếu với giá thị trường và chứa chuỗi không chuẩn hóa. |
| `Dẫn động`, `Tiêu thụ nhiên liệu` | Thiếu nhiều dữ liệu hoặc trùng lặp thông tin với dòng xe và động cơ. |

---

## 3. Quy Ước Lập Trình Tiếp Nhận (Developer Contract for Modeling)

Bất kỳ module nào xây dựng ma trận $X$ cho mô hình hóa trong Phase 6 **bắt buộc** phải tuân thủ danh sách đặc trưng được định nghĩa tại `src/data/preprocessing.py`:

```python
NUMERIC_FEATURES = [
    "year",
    "car_age",
    "mileage_km",
    "is_zero_mileage",
    "engine_displacement_l",
    "seats",
    "doors",
    "is_luxury_brand",
]

CATEGORICAL_FEATURES = [
    "brand",
    "model",
    "condition",
    "transmission",
    "origin",
    "body_type",
    "fuel_type",
]

EXCLUDED_LEAKAGE_COLUMNS = [
    "price_vnd",
    "log_price",
    "Giá",
    "listing_id",
    "Mã tin",
    "url",
    "URL",
    "Mô tả",
    "Tên xe",
]
```
