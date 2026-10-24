# Hướng Dẫn Dữ Liệu & Bản Tuyên Bố Bản Quyền (Data README & Manifest)
*(Used Car Price Prediction in Vietnam: An End-to-End Machine Learning System)*

Tài liệu này giải thích chi tiết nguồn gốc, tình trạng pháp lý, đạo đức dữ liệu và hướng dẫn thiết lập dữ liệu cục bộ cho dự án **Dự đoán giá ô tô đã qua sử dụng tại Việt Nam**.

---

## 1. Nguồn Gốc Dữ Liệu & Tình Trạng Pháp Lý (Dataset Provenance & Legal Status)

### 1.1. Nguồn gốc bộ dữ liệu
Dữ liệu sử dụng trong nghiên cứu này bắt nguồn từ:
- **Nguồn upstream**: Tập dữ liệu thị trường ô tô Việt Nam đăng tải trên Kaggle ([Vietnamese Car Price](https://www.kaggle.com/datasets/nguynthanhlun/vietnamese-car-price)).
- **Kho lưu trữ thứ cấp**: [GitHub mquaan/Car_price_analysis](https://github.com/mquaan/Car_price_analysis) thuộc đề tài trực quan hóa dữ liệu tại Khoa Công nghệ Thông tin, Trường Đại học Khoa học Tự nhiên - ĐHQG TP.HCM.
- **Nguồn gốc thu thập gốc**: Dữ liệu tin rao bán từ nền tảng thương mại điện tử xe hơi `bonbanh.com`.

### 1.2. Lý do không đưa dữ liệu thực tế lên GitHub Public Repository
Theo nguyên tắc quản trị dữ liệu nghiêm ngặt của khóa đào tạo AI Club và quy định bảo vệ dữ liệu cá nhân:
1. **Quyền sở hữu trí tuệ bên thứ ba chưa được xác minh đầy đủ**: Dù tác giả Kaggle/GitHub khai báo giấy phép mở, nền tảng gốc `bonbanh.com` và các chủ xe/salon đăng tin chưa cấp quyền tái phân phối thương mại công khai cho bên thứ ba.
2. **Bảo vệ thông tin cá nhân (PII Protection)**: Tệp thô `car_detail.csv` và `seller.csv` gốc có chứa các đoạn văn bản mô tả của người bán thỉnh thoảng kèm số điện thoại liên hệ cá nhân, tên chủ salon và địa chỉ giao dịch.
3. **Quyết định kiểm toán**: **Toàn bộ tệp CSV dữ liệu thực tế (`data/raw/` và `data/processed/`) được giữ bảo mật trên máy cục bộ và được cấu hình trong `.gitignore`**, tuyệt đối không đưa lên kho lưu trữ GitHub công khai.

---

## 2. Hướng Dẫn Cung Cấp Dữ Liệu Cục Bộ (Local Setup Instructions)

Để chạy lại toàn bộ pipeline học máy trên máy tính của bạn với dữ liệu thật:

### Bước 1: Chuẩn bị tệp tin thô
Tải hoặc sao chép 2 tệp CSV gốc vào đúng thư mục sau:
```text
data/
└── raw/
    └── external/
        └── mquaan_car_price/
            ├── car_detail.csv            (Dung lượng ~21.3 MB, 30,652 dòng)
            └── car_sell_processed.csv    (Dung lượng ~6.4 MB, 30,652 dòng)
```

### Bước 2: Kiểm tra tính toàn vẹn (SHA-256 Checksum)
Trước khi chạy, hãy kiểm tra mã băm SHA-256 để đảm bảo dữ liệu khớp chuẩn mực với các báo cáo thực nghiệm:
- **`car_detail.csv`**:
  `44c13afc5982f7abc51611fc56eeefd02df8e47f3224112f51b76514a7328f08`
- **`car_sell_processed.csv`**:
  `1d0c0d2f5a920f19eee09cffc84f30c7bc7496ac5bcb35260ccfbbd93c89437c`

*(Xem thông tin chi tiết các tệp phân chia và làm sạch trong [`data/dataset_manifest.json`](dataset_manifest.json))*

### Bước 3: Tái tạo các tập dữ liệu sạch và tập chia
Khi dữ liệu thô đã được đặt đúng vị trí, bạn có thể chạy các script tự động:
```powershell
# Làm sạch dữ liệu và tạo Cohort A (23,510 dòng)
python src/data/cleaning.py

# Tạo các tập chia ngẫu nhiên 80/10/10 (Phase 6)
python src/data/split_data.py

# Tạo các tập chia nhóm cách ly tin trùng 100% (Phase 6.2)
python src/data/duplicate_groups.py
```

---

## 3. Dữ Liệu Mẫu Giả Lập (Synthetic Demo Data)

Để tạo điều kiện cho mentor và người đánh giá có thể kiểm tra luồng code mà không bắt buộc phải tải tệp dữ liệu thật 21 MB, dự án cung cấp sẵn tệp:
- **Đường dẫn**: [`data/synthetic_demo_data.csv`](synthetic_demo_data.csv)
- **Đặc điểm**: Dữ liệu nhân tạo độc lập (100% Synthetic), không chứa bất kỳ PII, số điện thoại hay thông tin cá nhân nào.
- **Mục đích**: **CHỈ DÙNG CHO DEMO & SMOKE TEST (SYNTHETIC DEMO ONLY)**.
- **Cảnh báo**: Tệp demo không dùng để tái tạo hay tuyên bố đạt được các chỉ số hiệu năng thực nghiệm của Phase 6 hay Phase 6.2.

---

## 4. Tóm Tắt Cấu Trúc Đặc Trưng (Feature Dictionary Summary)

Bộ dữ liệu Cohort A sạch (23,510 bản ghi xe từ năm 2015 trở lại đây) gồm 15 đặc trưng chính quy:

| STT | Tên đặc trưng | Loại | Diễn giải nghiệp vụ |
| :---: | :--- | :---: | :--- |
| 1 | `year` | Numeric | Năm sản xuất xuất xưởng [2015 - 2023] |
| 2 | `car_age` | Numeric | Tuổi của xe tính tới 2023 ($2023 - \text{year}$) |
| 3 | `mileage_km` | Numeric | Số km đã lăn bánh theo ODO (đã xử lý ngoại lai) |
| 4 | `is_zero_mileage` | Numeric | Cờ nhận diện xe mới 100% tại showroom (ODO = 0 km) |
| 5 | `seats` | Numeric | Số chỗ ngồi theo giấy tờ kiểm định [2 - 16] |
| 6 | `doors` | Numeric | Số cửa ra vào [2 - 5] |
| 7 | `engine_displacement_l`| Numeric | Dung tích xi-lanh động cơ (Lít) gắn liền thuế TTĐB |
| 8 | `is_luxury_brand` | Numeric | Cờ nhị phân phân khúc xe sang (Mercedes, Lexus, BMW,...) |
| 9 | `brand` | Categorical | Hãng sản xuất xe (48 thương hiệu) |
| 10 | `model` | Categorical | Tên dòng xe thương mại (451 dòng xe) |
| 11 | `origin` | Categorical | Nguồn gốc xuất xứ (Lắp ráp trong nước vs Nhập khẩu) |
| 12 | `transmission` | Categorical | Hộp số (Tự động vs Số tay) |
| 13 | `fuel_type` | Categorical | Nhiên liệu (Xăng, Dầu, Hybrid, Điện) |
| 14 | `body_type` | Categorical | Kiểu dáng xe (Sedan, SUV, Crossover, Hatchback,...) |
| 15 | `condition` | Categorical | Tình trạng xe (Xe đã dùng vs Xe mới) |

*Biến mục tiêu*: `price_vnd` (Giá chào bán niêm yết theo VND).
