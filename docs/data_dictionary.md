# Từ Điển Dữ Liệu Dự Án (Data Dictionary)

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam (Used Car Price Prediction in Vietnam)
- **Phiên bản Schema**: 1.0 (Provisional & Verified Fields for Phase 0)
- **Tài liệu liên quan**: [Data Source Audit](file:///d:/ai-club-end-training/docs/data_source_audit.md), [Project Charter](file:///d:/ai-club-end-training/docs/project_charter.md)

---

## 1. Nguyên Tắc Thiết Kế Schema

1. **Phân tách Rõ Ràng giữa Dữ Liệu Thô (Raw) và Dữ Liệu Đã Chuẩn Hóa (Processed/Engineered)**:
   - Dữ liệu thô lưu giữ chuỗi gốc từ website để đảm bảo tính truy vết (Audit Trail).
   - Dữ liệu chuẩn hóa chuyển đổi về kiểu dữ liệu số học, nhị phân hoặc phân loại có cấu trúc phục vụ cho thuật toán Machine Learning.
2. **Quản Trị Rủi Ro Dữ Liệu Thiếu**:
   - Chỉ có biến mục tiêu (`price_vnd`) và các định danh cơ sở (`brand`, `model`, `year`) là bắt buộc (Required).
   - Các trường khác được coi là tùy chọn (Optional) hoặc tạm thời (Provisional) nhằm tránh việc loại bỏ dữ liệu quá tay trong giai đoạn thu thập.
3. **Phân Biệt Trạng Thái Xác Minh**:
   - Các trường đã kiểm chứng trên HTML thực tế được ghi chú rõ vị trí trích xuất.
   - Các trường chưa xác minh trong bảng thông số chuẩn (như `seats`) được gắn nhãn `Provisional / Unverified in standard spec box`.

---

## 2. Bảng Đặc Tả Schema Chi Tiết (Detailed Data Schema Table)

| Field Name | Data Type | Meaning | Example Format | Unit | Required / Optional | Expected Missing-data Risks | Validation Rules | Usage in ML | Original Source Field |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`price_vnd`** | `Integer` (int64) | Giá rao bán của chiếc xe đã được chuẩn hóa | `899000000`, `1169000000` | Đồng (VND) | **Required** (Cho tập Supervised Train) | Tin để giá "Thỏa thuận", "Liên hệ" hoặc thiếu giá. | Giá trị phải là số nguyên dương: `50_000_000 <= price_vnd <= 30_000_000_000` | **Target variable ($y$)** cho mô hình hồi quy | Trích xuất từ `<p class="price">` (vd: `"899 triệu"`) hoặc `data-call` |
| **`brand`** | `String` / `Categorical` | Thương hiệu sản xuất xe ô tô | `"Mercedes-Benz"`, `"Toyota"`, `"Kia"` | Không | **Required** | Rất thấp (hầu hết tin đều nằm trong danh mục hãng). | Phải thuộc danh sách hãng xe hợp lệ; không chứa ký tự đặc biệt lạ. | **Feature ($X$)**: One-Hot Encoding hoặc Target Encoding | Thuộc tính `data-tinrao` / `data-call` (vd: `"Mercedes-Benz"`) |
| **`model`** | `String` / `Categorical` | Dòng xe / Tên mẫu xe cơ bản | `"C200"`, `"Camry"`, `"Carnival"`, `"Vios"` | Không | **Required** | Thấp trên metadata sàn; có thể lẫn tên phiên bản (Trim). | Độ dài chuỗi từ 1 đến 50 ký tự; viết hoa chữ cái đầu. | **Feature ($X$)**: High-cardinality Categorical (Target Encoding hoặc Grouping) | Thuộc tính `data-tinrao` / `data-call` (vd: `"C200"`) |
| **`year`** | `Integer` (int32) | Năm sản xuất của chiếc xe | `2021`, `2024`, `2019` | Năm (Year) | **Required** | Rất thấp trên metadata chuẩn. | Số nguyên 4 chữ số: `2010 <= year <= 2026` | **Feature ($X$)**: Dùng trực tiếp hoặc chuyển đổi thành `car_age = current_year - year` | Thuộc tính `data-call` hoặc mục "Năm SX" trong `box-info-detail` |
| **`mileage_km`** | `Float` (float64) | Số kilomet đã vận hành (ODO) | `49000.0`, `28000.0` | Kilomet (km) | **Optional** (Khuyến nghị cao) | Người bán bỏ trống, điền số tượng trưng (vd: 1 km, 999999 km), hoặc xe mới chưa chạy. | Số thực không âm: `0 <= mileage_km <= 500_000`. Kiểm tra ngoại lai nếu ODO = 0 với xe cũ > 3 năm. | **Feature ($X$)**: Numerical Feature quan trọng, kết hợp tính `mileage_per_year` | Thẻ `<ul class="tag-list"> > li` hoặc mục "Km đã đi" trong `box-info-detail` |
| **`fuel_type`** | `String` / `Categorical` | Loại nhiên liệu xe sử dụng | `"Máy xăng"`, `"Máy dầu"`, `"Hybrid"`, `"Điện"` | Không | **Optional** | Thiếu trên một số tin đăng sơ sài. | Phải thuộc tập giá trị chuẩn: `{'Xăng', 'Dầu', 'Hybrid', 'Điện'}` | **Feature ($X$)**: One-Hot Encoding | Thẻ `<ul class="tag-list"> > li` hoặc mục "Nhiên liệu" trong `box-info-detail` |
| **`transmission`** | `String` / `Categorical` | Loại hộp số điều khiển | `"Số tự động"`, `"Số sàn"` | Không | **Optional** | Thấp trên sàn Oto.com.vn. | Phải thuộc tập giá trị chuẩn: `{'Số tự động', 'Số sàn'}` | **Feature ($X$)**: Binary / One-Hot Encoding | Thẻ `<ul class="tag-list"> > li` hoặc mục "Hộp số" trong `box-info-detail` |
| **`location_province`** | `String` / `Categorical` | Tỉnh hoặc Thành phố trực thuộc TW nơi xe được rao bán | `"Hà Nội"`, `"Tp.HCM"`, `"Đà Nẵng"` | Không | **Optional** | Người bán chỉ ghi chung chung hoặc ghi sai địa chỉ. | Phải khớp với danh mục 63 tỉnh thành Việt Nam sau khi chuẩn hóa. | **Feature ($X$)**: One-Hot Encoding cho các tỉnh lớn (Hà Nội, TP.HCM, Khác) | Thẻ `<li class="seller-location">` hoặc mục "Tỉnh thành" trong `box-info-detail` |
| **`body_type`** | `String` / `Categorical` | Kiểu dáng thân vỏ của xe | `"Sedan"`, `"SUV"`, `"MPV"`, `"Hatchback"`, `"Bán tải"` | Không | **Optional** | Người bán cá nhân có thể phân loại sai (nhầm SUV với CUV/MPV). | Phải thuộc danh mục kiểu dáng ô tô chuẩn. | **Feature ($X$)**: One-Hot Encoding | Thuộc tính `data-call` hoặc mục "Kiểu dáng" trong `box-info-detail` |
| **`origin`** | `String` / `Categorical` | Nguồn gốc xuất xứ của xe | `"Trong nước"`, `"Nhập khẩu"` | Không | **Optional** | Có thể bị bỏ trống ở một số tin đăng tự do. | Phải thuộc tập giá trị chuẩn: `{'Trong nước', 'Nhập khẩu'}` | **Feature ($X$)**: Binary Encoding (1: Nhập khẩu, 0: Trong nước) | Thuộc tính `data-call` hoặc mục "Xuất xứ" trong `box-info-detail` |
| **`seats`** | `Integer` (int32) | Số lượng chỗ ngồi thiết kế của xe | `5`, `7`, `4` | Chỗ | **Optional / Provisional** | **RẤT CAO**: Không tồn tại trong bảng thông số kỹ thuật chuẩn (`box-info-detail`) của Oto.com.vn. | Nếu có: `2 <= seats <= 16`. Nếu thiếu: Phải dùng phương pháp suy diễn từ `model` hoặc chấp nhận `NaN`. | **Feature ($X$)**: Có thể đưa vào sau khi hoàn thiện bảng mapping theo Model; Phase 0 gắn nhãn dự phòng | Chỉ có rải rác trong văn bản tự do hoặc đường dẫn gợi ý SEO |
| **`listing_id`** | `String` | Mã định danh kỹ thuật duy nhất của tin đăng trên hệ thống nguồn | `"23442555"`, `"23444950"` | Không | **Required** (Khóa định danh kỹ thuật) | Gần như không thiếu trên web Oto.com.vn nhờ `data-autoid`. | Chuỗi ký số nguyên dương duy nhất. | **Không dùng làm Feature học máy** (Metadata phục vụ Deduplication và Tracking) | Thuộc tính `data-autoid="23442555"` |
| **`source_url`** | `String` | Đường dẫn URL truy cập tin đăng gốc | `"https://oto.com.vn/mua-ban-xe-mercedes-benz-c200-ha-noi/mercedes-exclusive-2021-aidxc23442555"` | URL | **Optional** | Thiếu nếu crawler chỉ cào từ card mà không bóc tách thẻ `<a>`. | Bắt đầu bằng `http://` hoặc `https://`, trỏ đúng domain. | **Không dùng làm Feature** (Phục vụ kiểm chứng và audit tính trung thực) | Thuộc tính `href` của thẻ tiêu đề tin đăng |
| **`crawl_date`** | `Datetime` (ISO 8601) | Thời điểm hệ thống thực hiện cào dữ liệu | `"2026-10-18T15:10:39"` | Thời gian | **Required** (Hệ thống tự sinh) | Không có rủi ro thiếu (do script tự ghi nhận). | Định dạng chuẩn ISO 8601; không được ở tương lai so với thời điểm chạy. | **Phục vụ tính toán Feature**: Dùng để tính tuổi xe chính xác theo tháng/năm | Timestamp hệ thống khi chạy crawler |

---

## 3. Các Biến Đặc Trưng Dự Kiến Tạo Thêm (Engineered Features)

Trong Phase 6 (Feature Engineering), các biến phái sinh sau sẽ được xây dựng dựa trên các trường gốc:

1. **`car_age`** (`Integer`):
   $$\text{car\_age} = \text{crawl\_year} - \text{year}$$
   *Ý nghĩa*: Số năm xe đã xuất xưởng, đại diện cho mức độ khấu hao công nghệ và cơ khí.
2. **`mileage_per_year`** (`Float`):
   $$\text{mileage\_per\_year} = \frac{\text{mileage\_km}}{\max(\text{car\_age}, 0.5)}$$
   *Ý nghĩa*: Cường độ sử dụng xe trung bình hàng năm (km/năm). Giúp phân biệt xe chạy dịch vụ (ODO cao bất thường) với xe gia đình đi ít ("xe lướt").
3. **`is_major_city`** (`Binary`):
   $$\text{is\_major\_city} = \mathbb{I}(\text{location\_province} \in \{\text{'Hà Nội'}, \text{'Tp.HCM'}\})$$
   *Ý nghĩa*: Phản ánh sự chênh lệch giá do chi phí ra biển số và thị trường tiêu thụ tại 2 trung tâm kinh tế lớn.
4. **`log_price`** (`Float` - Phục vụ huấn luyện mô hình):
   $$\text{log\_price} = \ln(\text{price\_vnd})$$
   *Ý nghĩa*: Biến đổi Logarit giúp đưa phân phối giá xe bị lệch phải (right-skewed) về dạng gần phân phối chuẩn, ổn định phương sai cho các mô hình hồi quy tuyến tính.

---

## 4. Giải Trình Quyết Định Kỹ Thuật (Mentorship Notes)

1. **Vì sao tách riêng `price_vnd` và chuỗi giá gốc?**
   - Giúp kiểm chứng lại logic chuyển đổi đơn vị ("triệu", "tỉ") khi phát hiện các giá trị ngoại lai bất thường mà không cần crawl lại trang web.
2. **Tại sao không loại bỏ ngay trường `seats` khi phát hiện nó không có trong bảng thông số chuẩn?**
   - Số chỗ ngồi là một đặc trưng nghiệp vụ quan trọng trong việc phân khúc ô tô (xe 5 chỗ vs xe 7 chỗ). Thay vì vội vàng xóa bỏ, việc ghi nhận ở trạng thái `Provisional` cho phép nhóm kỹ thuật xây dựng từ điển đối chiếu (lookup dictionary) theo `model` (ví dụ: Toyota Innova -> 7/8 chỗ, Mazda 3 -> 5 chỗ) ở giai đoạn Data Cleaning.
3. **Mentor có thể chất vấn gì về Data Dictionary này?**
   - *"Nếu ODO bị thiếu thì có nên loại bỏ luôn bản ghi đó không?"*
   - *Trả lời*: Không nên loại bỏ ngay lập tức ở tầng thu thập. Trong Phase 6, ta sẽ phân tích tỷ lệ missing của `mileage_km`. Nếu tỷ lệ thiếu thấp (< 5-10%), ta có thể áp dụng kỹ thuật Imputation dựa trên trung vị theo từng nhóm `(brand, model, year)`. Loại bỏ quá nhiều sẽ gây mất mát dữ liệu quý giá.
