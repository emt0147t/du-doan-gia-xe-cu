# Bảng Quy Chuẩn Ánh Xạ Dữ Liệu (Schema Mapping Specification)

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam (Used Car Price Prediction in Vietnam)
- **Phiên bản tài liệu**: 1.0
- **Thời gian lập**: 19/10/2026, 01:15:00 (Múi giờ: Asia/Ho_Chi_Minh)
- **Người thực hiện**: Senior Data Engineer & ML Mentor
- **Tài liệu liên quan**: [Data Dictionary](file:///d:/ai-club-end-training/docs/data_dictionary.md), [Data Pilot Plan](file:///d:/ai-club-end-training/docs/data_pilot_plan.md)

---

## 1. Nguyên Tắc Ánh Xạ Schema

Để đảm bảo tính nhất quán giữa hai nhánh tiếp nhận dữ liệu (Track A: External Dataset và Track B: Website Crawler), mọi trường dữ liệu thô khi đưa vào pipeline đều phải được đối chiếu theo bảng phân loại trạng thái ánh xạ:

1. **Directly Mapped (Ánh xạ trực tiếp)**: Kiểu dữ liệu và ý nghĩa đã khớp hoàn toàn với schema dự án, không cần xử lý thêm ngoài việc đổi tên cột.
2. **Needs Normalization (Cần chuẩn hóa)**: Kiểu dữ liệu hoặc danh mục cần làm sạch (bỏ khoảng trắng, chuẩn hóa chữ hoa/thường, chuẩn hóa tên tỉnh thành hoặc phân loại hộp số).
3. **Needs Unit Conversion (Cần chuyển đổi đơn vị)**: Cần đi qua module xử lý nghiệp vụ riêng (ví dụ: `price_parser.py` để chuyển chuỗi tiếng Việt hoặc số thập phân sang số nguyên VND).
4. **Not Present in Source (Không có trong nguồn)**: Nguồn không cung cấp trường này; trường nhận giá trị `None` / `NaN`, tuyệt đối không tự bịa đặt giá trị.
5. **Unverified (Chưa xác minh)**: Nguồn có thể có trường này nhưng chưa thể kiểm chứng trên quy mô thực tế.

---

## 2. Bảng Đối Chiếu Ánh Xạ Chi Tiết 14 Trường Chuẩn

| Trường chuẩn dự án (`target_field`) | Kiểu dữ liệu đích | Tính chất | Phân loại ánh xạ từ Track A (Dataset ngoài) | Phân loại ánh xạ từ Track B (Crawler Web) | Quy tắc chuyển đổi kỹ thuật |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`price_vnd`** | `int` (int64) | **Required** (Target $y$) | **Needs Unit Conversion** | **Needs Unit Conversion** | Nạp qua `parse_vietnamese_price_to_vnd()`. Bỏ qua tin "Thỏa thuận" hoặc giá $\le 0$. Ngưỡng: 30 triệu $\le$ price $\le$ 50 tỷ VND. |
| **`brand`** | `str` | **Required** (Feature $X$) | **Needs Normalization** | **Needs Normalization** | Chuẩn hóa trim khoảng trắng, chuẩn hóa chữ hoa/thường (`Toyota`, `Mercedes-Benz`, `Kia`...). |
| **`model`** | `str` | **Required** (Feature $X$) | **Needs Normalization** | **Needs Normalization** | Chuẩn hóa chuỗi, tách tên dòng xe cơ bản khỏi phiên bản chi tiết (`Vios`, `C200`, `Carnival`...). |
| **`year`** | `int` (int32) | **Required** (Feature $X$) | **Directly Mapped / Needs Normalization** | **Directly Mapped** | Chuyển đổi về kiểu số nguyên 4 chữ số. Ngưỡng: 2010 $\le$ year $\le$ 2026. |
| **`mileage_km`** | `float` (float64) | **Optional** (Feature $X$) | **Needs Unit Conversion** | **Needs Unit Conversion** | Bóc tách số kilomet từ chuỗi (vd: `"49.000 km"` $\rightarrow$ `49000.0`). Cho phép `None` nếu người bán không khai báo. |
| **`fuel_type`** | `str` | **Optional** (Feature $X$) | **Needs Normalization** | **Needs Normalization** | Chuẩn hóa về tập danh mục chuẩn: `{'Máy xăng', 'Máy dầu', 'Hybrid', 'Điện'}`. |
| **`transmission`** | `str` | **Optional** (Feature $X$) | **Needs Normalization** | **Needs Normalization** | Chuẩn hóa về tập danh mục chuẩn: `{'Số tự động', 'Số sàn'}` (chuyển đổi AT $\rightarrow$ Số tự động, MT $\rightarrow$ Số sàn). |
| **`location_province`** | `str` | **Optional** (Feature $X$) | **Needs Normalization** | **Needs Normalization** | Tách và chuẩn hóa về danh mục tỉnh/thành phố cấp 1 (loại bỏ quận/huyện, chuẩn hóa `Tp.HCM`, `Hà Nội`...). |
| **`body_type`** | `str` | **Optional** (Feature $X$) | **Needs Normalization** | **Directly Mapped** | Chuẩn hóa kiểu dáng (`Sedan`, `SUV`, `MPV`, `Hatchback`, `Bán tải`...). |
| **`origin`** | `str` | **Optional** (Feature $X$) | **Needs Normalization** | **Directly Mapped** | Chuẩn hóa xuất xứ: `{'Trong nước', 'Nhập khẩu'}`. |
| **`seats`** | `int` (int32) | **Optional / Provisional** | **Unverified / Optional** | **Not Present in Source** | Không có trong bảng thông số chuẩn của Oto.com.vn. Mặc định nhận giá trị `None` / `NaN`; có thể suy diễn từ `model` ở Phase 4/6. |
| **`listing_id`** | `str` | **Required** (Tracking ID) | **Directly Mapped / Generated** | **Directly Mapped** | Trích xuất từ `data-autoid`. Phục vụ kiểm tra khử trùng lặp (Deduplication). |
| **`source_url`** | `str` | **Optional** (Audit Metadata) | **Not Present in Source / Optional** | **Directly Mapped** | Đường dẫn bài đăng gốc phục vụ kiểm chứng thực tế. |
| **`crawl_date`** | `str` (ISO 8601) | **Required** (Audit Metadata) | **Needs Normalization / Generated** | **Directly Mapped** | Thời điểm thu thập dữ liệu (UTC/ISO 8601 string) để tính tuổi xe (`car_age`). |

---

## 3. Cấu Hình Ánh Xạ Trong Code Python (`src/data/load_dataset.py`)

Khi nạp tệp bảng từ bên ngoài thông qua hàm `map_raw_to_project_schema(df, column_mapping)`, từ điển ánh xạ chuẩn được định nghĩa như sau:

```python
STANDARD_EXTERNAL_MAPPING: dict[str, str] = {
    "price_raw": "price_vnd",
    "brand_raw": "brand",
    "model_raw": "model",
    "year_raw": "year",
    "mileage_raw": "mileage_km",
    "fuel_raw": "fuel_type",
    "transmission_raw": "transmission",
    "location_raw": "location_province",
    "origin_raw": "origin",
    "body_raw": "body_type",
    "seats_raw": "seats",
    "listing_id": "listing_id",
}
```

Mọi trường không xuất hiện trong tệp nguồn sẽ không bị ép giá trị mặc định tùy tiện mà được giữ nguyên trạng thái khuyết thiếu (`None` / `np.nan`) để module validation xử lý khách quan.
