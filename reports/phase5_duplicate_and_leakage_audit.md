# Báo Cáo Kiểm Toán Trùng Lặp & Rò Rỉ Dữ Liệu
*(Phase 5 — Duplicate and Data Leakage Audit Report)*

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam (Used Car Price Prediction in Vietnam)
- **Giai đoạn**: Phase 5 — Data Cleaning, Feature Engineering & Preprocessing Pipeline
- **Thời gian lập**: 19/10/2026, 03:00:00 (Múi giờ: Asia/Ho_Chi_Minh)
- **Người thực hiện**: Senior Data Scientist, ML Engineer & AI Student
- **Tài liệu đối chiếu**: [Data Dictionary](file:///d:/ai-club-end-training/docs/data_dictionary.md), [Cleaning Policy](file:///d:/ai-club-end-training/docs/eda_findings_and_cleaning_policy.md)

---

## 1. Kết Quả Kiểm Toán Trùng Lặp (Duplication Audit)

Nhóm đã tiến hành kiểm toán trùng lặp đa tầng trên toàn bộ 30,652 dòng dữ liệu thô của [car_detail.csv](file:///d:/ai-club-end-training/data/raw/external/mquaan_car_price/car_detail.csv):

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                 KẾT QUẢ KIỂM TOÁN TRÙNG LẶP ĐA CẤP ĐỘ                      │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ 1. Trùng lặp tuyệt đối (Tất cả 21 cột)│ 0 bản ghi (0.00%)                    │
│ 2. Trùng lặp mã định danh (Mã tin)   │ 0 bản ghi (100.00% duy nhất 30,652 ID)│
│ 3. Trùng lặp thông số kỹ thuật       │ 4,907 bản ghi (16.01% tổng số tin)   │
│    (Hãng, Dòng, Năm, ODO, Giá, Màu)  │                                      │
│    - Trong đó: Xe mới tại showroom   │ 2,764 xe (56.33% nhóm trùng thông số)│
│    - Trong đó: ODO = 0 km            │ 3,121 xe (63.60% nhóm trùng thông số)│
│ 4. Trùng lặp thông số VÀ bài mô tả   │ 633 bản ghi (2.07% tổng số tin)      │
│    (Cross-posting / Tin làm mới)     │                                      │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

### Phân tích nghiệp vụ sâu sắc & Cảnh báo False Positive:
> [!WARNING]
> **Không được phép xóa bỏ bản ghi chỉ dựa trên việc trùng thông số kỹ thuật (`brand`, `model`, `year`, `price`, `mileage`)**:
> - Trong số 4,907 tin trùng thông số kỹ thuật cơ bản, có tới **2,764 tin là xe mới 100% tại các đại lý chính hãng**. Đại lý Toyota hoặc Hyundai nhập về 10–20 chiếc Corolla Cross hoặc Accent cùng màu, cùng năm 2023, cùng ODO = 0 km và niêm yết theo giá niêm yết đề xuất của hãng (MSRP). Đây là các thực thể xe có thật trong kho hàng của doanh nghiệp, không phải tin cào trùng lặp.
> - Nếu tự động deduplicate theo thông số, ta sẽ xóa nhầm (False Positive) hơn 2,000 xe hợp lệ, làm méo mó phân phối xe mới trên thị trường.
> - **Chỉ có 633 tin (2.07%)** là trùng cả thông số kỹ thuật lẫn toàn văn bài viết mô tả chi tiết (`Mô tả`). Đây là dấu hiệu của các tin đăng chéo (Cross-posting) hoặc cùng một salon làm mới tin (Refresh ad) cho cùng một chiếc xe cũ. Nhóm sẽ ghi nhận nhóm này để kiểm soát rò rỉ khi phân chia tập Train/Test (Task H).

---

## 2. Kiểm Toán Rò Rỉ Dữ Liệu Mục Tiêu (Target Leakage Audit)

Nhóm rà soát toàn bộ các cột trong tập dữ liệu để xác định ranh giới cách ly thông tin nghiêm ngặt trước khi đưa vào ma trận đặc trưng ($X$):

### 2.1. Danh sách các cột CẤM ĐƯA VÀO FEATURE MATRIX ($X$):

1. **`Giá` (Raw Price String)**: Chứa trực tiếp nhãn mục tiêu cần dự đoán dưới dạng chuỗi tiếng Việt.
2. **`price_vnd` (Normalized Target)**: Biến mục tiêu chính thức ($y$).
3. **`price_billion`, `log_price`, `log1p_price`**: Các dạng biến đổi suy diễn trực tiếp từ $y$.
4. **`Mã tin` (Listing ID)**: Khóa định danh của hệ thống cơ sở dữ liệu sàn Bonbanh.com. Trường này tăng dần theo thời gian tạo bài đăng, có thể tương quan giả tạo với mức giá do lạm phát thị trường nếu đưa vào mô hình.
5. **`URL` (Article URL)**: Chứa trực tiếp mã tin và tên định danh xe.
6. **`Mô tả` (Free Text Description)**: Chứa văn bản chào bán của người bán. Kiểm tra thực nghiệm cho thấy hơn 40% bài mô tả chứa trực tiếp số tiền bán xe hoặc số tiền trả góp (ví dụ: *"giao ngay chỉ với 80t5r"*, *"giá bán 1 tỷ 220 triệu"*). Nếu trích xuất n-grams hoặc TF-IDF từ cột này mà không lọc giá, mô hình sẽ học thuộc lòng giá từ mô tả thay vì học từ thông số xe.
7. **Thông tin liên hệ người bán / PII**: Tệp `seller.csv` đã được loại bỏ hoàn toàn từ Phase 3.2 để bảo vệ dữ liệu cá nhân theo Nghị định 13/2023/NĐ-CP.

### 2.2. Danh sách các cột AN TOÀN ĐƯA VÀO ĐẶC TRƯNG ($X$):

- **Thông số kỹ thuật cốt lõi**: `brand`, `model`, `year`, `car_age`, `mileage_km`, `is_zero_mileage`, `transmission`, `fuel_type`, `origin`, `body_type`, `seats`, `doors`, `engine_displacement_l`, `condition`.
- **Thông tin bổ trợ**: `location_province` (nếu kiểm chứng được khóa liên kết) hoặc mã vùng kinh tế.

---

## 3. Chiến Lược Ngăn Ngừa Rò Rỉ Tuyệt Đối Trong Preprocessing

1. **Nguyên tắc "Fit on Train Only"**:
   - Mọi phép biến đổi dữ liệu có trạng thái học (Stateful Transformers): `SimpleImputer` (học median), `StandardScaler` (học mean và std), `OneHotEncoder` (học danh mục), `TargetEncoder` **tuyệt đối chỉ được gọi `.fit()` trên tập huấn luyện (Train Set)**.
   - Tập kiểm định (Validation Set) và tập kiểm thử (Test Set) chỉ được gọi `.transform()` bằng các tham số đã học từ Train.
2. **Chiến lược phân chia dữ liệu (Data Splitting Strategy)**:
   - Dữ liệu sẽ được phân tách thành 3 tập độc lập: **Train (80%)**, **Validation (10%)**, **Test (10%)** trước khi bất kỳ bước tiền xử lý hay chuẩn hóa dữ liệu nào được khởi tạo.
   - Để ngăn chặn việc các tin đăng trùng nội dung (633 tin cross-posting) xuất hiện đồng thời ở cả Train và Test, bước phân chia dữ liệu sẽ kiểm tra và phân bổ các tin gần trùng theo cùng một cụm (Group-aware partition) hoặc loại bỏ chúng khỏi Test set.
