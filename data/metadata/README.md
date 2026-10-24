# Quy Chuẩn Quản Lý Dữ Liệu Thô & Khả Năng Tái Lập (Raw Data Governance & Reproducibility)

Tài liệu này quy định các chuẩn mực kỹ thuật bắt buộc nhằm quản lý dữ liệu an toàn, minh bạch và có thể kiểm chứng độc lập trong toàn bộ dự án.

---

## 1. Cấu Trúc Phân Tách Thư Mục Dữ Liệu

Dữ liệu trong dự án được phân cấp nghiêm ngặt thành các tầng độc lập:

```text
data/
├── raw/                               # DỮ LIỆU THÔ BẤT BIẾN (IMMUTABLE RAW DATA)
│   ├── external/                      # Dữ liệu từ các nguồn mở/dataset bên ngoài
│   │   └── <source_name>/             # Thư mục riêng cho từng nguồn (ví dụ: kaggle/)
│   └── website/                       # Dữ liệu thu thập thử nghiệm từ web (nếu được phép)
├── processed/                         # DỮ LIỆU ĐÃ LÀM SẠCH & CHUẨN HÓA (CLEANED DATA)
│   └── (Được sinh tự động từ pipeline, không sửa tay)
└── metadata/                          # SIÊU DỮ LIỆU & BẰNG CHỨNG KIỂM ĐỊNH (METADATA)
    ├── README.md                      # Tài liệu quy chuẩn này
    └── (Các tệp ghi nhận checksum, audit log)
```

> [!IMPORTANT]
> **Nguyên tắc bất biến (Immutability)**:
> Mọi tệp nằm trong `data/raw/` sau khi tiếp nhận **tuyệt đối không được chỉnh sửa trực tiếp, không ghi đè**. Mọi biến đổi dữ liệu (làm sạch, bóc tách giá, lọc ngoại lai) phải lưu vào tệp mới tại `data/processed/`.

---

## 2. Quy Tắc Đặt Tên Tệp (File Naming Conventions)

1. **Dữ liệu thô từ nguồn ngoài**:
   `data/raw/external/<source_name>/<original_filename>_<YYYYMMDD>.csv`
   *(Ví dụ: `data/raw/external/kaggle_vietnam_auto/data_20261019.csv`)*
2. **Dữ liệu mẫu pilot từ crawler**:
   `data/raw/website/pilot_<source_domain>_<sample_size>_<YYYYMMDDTHHMMSS>.jsonl`
   *(Ví dụ: `data/raw/website/pilot_oto_vn_30items_20261019T011500Z.jsonl`)*
3. **Dữ liệu sạch sau tiền xử lý**:
   `data/processed/cars_clean_<version>_<YYYYMMDD>.csv`

---

## 3. Quy Tắc Ghi Nhận Siêu Dữ Liệu & Mã Băm SHA-256 (Checksum Rules)

Mỗi khi một tệp dữ liệu thô được tiếp nhận vào hệ thống:
1. **Bắt buộc tạo tệp checksum**: Cùng tên với tệp dữ liệu, thêm phần mở rộng `.sha256`.
   - Cú pháp: `<sha256_hex_string>  <filename>`
   - Được sinh tự động thông qua hàm `compute_sha256()` trong [src/data/load_dataset.py](file:///d:/ai-club-end-training/src/data/load_dataset.py).
2. **Ghi nhật ký tiếp nhận (Ingestion Log)** với các trường bắt buộc:
   - `source_name`: Tên nguồn gốc.
   - `source_url`: URL truy cập nguồn.
   - `publisher`: Cá nhân hoặc tổ chức công bố.
   - `retrieval_timestamp`: Thời điểm tải theo chuẩn ISO 8601.
   - `sha256_hash`: Mã băm toàn vẹn.
   - `license_declared`: Giấy phép công bố trên nền tảng.
   - `provenance_notes`: Ghi chú về nguồn gốc dữ liệu ban đầu.

---

## 4. Quy Tắc Bảo Vệ Dữ Liệu Nhạy Cảm & Khử PII (PII Scrubbing)

Theo Nghị định 13/2023/NĐ-CP về bảo vệ dữ liệu cá nhân tại Việt Nam:
1. **Không thu thập & không lưu trữ**:
   - Số điện thoại của người bán hoặc chủ xe (`phone`, `seller_phone`, `contact_number`).
   - Tên cá nhân người bán (`seller_name`, `contact_name`).
   - Địa chỉ nhà riêng cụ thể (chỉ lưu cấp Tỉnh / Thành phố trực thuộc Trung ương).
2. **Kiểm tra tự động trước khi lưu**:
   - Mọi hàm trích xuất trong [src/data/crawler.py](file:///d:/ai-club-end-training/src/data/crawler.py) đều áp dụng bộ lọc regex số điện thoại Việt Nam (`(0|\+84)[3|5|7|8|9][0-9]{8}`) để đảm bảo không một chuỗi số liên lạc nào lọt vào tệp raw.

---

## 5. Quy Trình Tái Lập & Kiểm Tra Toàn Vẹn Dữ Liệu (Reproduction Steps)

Để kiểm chứng tính toàn vẹn của bất kỳ tệp dữ liệu nào trong dự án:

```powershell
# 1. Tính toán mã SHA-256 của tệp cục bộ
python -c "from src.data.load_dataset import compute_sha256; print(compute_sha256('data/raw/external/source/file.csv'))"

# 2. Chạy test kiểm tra toàn vẹn
pytest -v tests/test_load_dataset.py
```
