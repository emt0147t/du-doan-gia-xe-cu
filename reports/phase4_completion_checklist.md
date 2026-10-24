# Bảng Nghiệm Thu Hoàn Thành Giai Đoạn Phase 4
*(Phase 4 — Exploratory Data Analysis & Data Quality Investigation Completion Checklist)*

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam (Used Car Price Prediction in Vietnam)
- **Giai đoạn**: Phase 4 — Exploratory Data Analysis & Data Quality Investigation
- **Thời gian lập**: 19/10/2026, 02:40:00 (Múi giờ: Asia/Ho_Chi_Minh)
- **Người thực hiện**: Senior Data Scientist, ML Engineer & AI Student
- **Trạng thái tổng thể Phase 4**: **`COMPLETED / PASS (100% HOÀN THÀNH)`**

---

## 1. Bảng Tiêu Chí Nghiệm Thu Chi Tiết (Acceptance Criteria Matrix)

| Hạng mục tiêu chí kiểm thử | Trạng thái | Minh chứng kỹ thuật thực tế |
| :--- | :---: | :--- |
| **1. Định danh dữ liệu & Checksum SHA-256** | **PASS** | Tệp `car_detail.csv` đạt SHA-256 `44c13afc...` khớp 100% với sidecar `.sha256` và `ingestion_mquaan_car_price.json`. |
| **2. Bảo toàn dữ liệu thô (Immutability)** | **PASS** | Tệp raw trong `data/raw/external/mquaan_car_price/` giữ nguyên trạng, kích thước và hash không thay đổi. |
| **3. Notebook EDA có thể tái lập** | **PASS** | [notebooks/04_eda.ipynb](file:///d:/ai-club-end-training/notebooks/04_eda.ipynb) được xây dựng và thực thi thành công toàn bộ 29 cells qua `jupyter nbconvert`. |
| **4. Báo cáo khuyết thiếu từ dữ liệu thực** | **PASS** | Đo lường chi tiết trên 30,652 dòng: `Năm sản xuất` khuyết 32 dòng (0.10%), `Hệ thống nạp nhiên liệu` khuyết 77.99%. |
| **5. Tính toán lại tỷ lệ parse giá** | **PASS** | `parse_vietnamese_price_to_vnd` đạt tỷ lệ parse thành công chính xác **100.00% (30,652/30,652 bản ghi)**. |
| **6. Khám phá Target, Year, Mileage, Brand** | **PASS** | Phân tích toàn diện giá (Median 620M, Mean 1.18B), năm (1990–2023), ODO (34% mốc 0 km), 76 hãng xe (Toyota 18.2%). |
| **7. Tạo tối thiểu 10 biểu đồ hữu ích** | **PASS** | Đã tạo và lưu thành công **19 biểu đồ kỹ thuật** chất lượng cao tại [reports/figures/phase4/](file:///d:/ai-club-end-training/reports/figures/phase4). |
| **8. Diễn giải ma trận tương quan chuẩn xác** | **PASS** | Phân tích tương quan Pearson với lưu ý phương pháp luận: Correlation $\ne$ Causation, giải thích vì sao ODO đơn biến có $r$ thấp. |
| **9. Tái thẩm định chính sách Validation** | **PASS** | Phân biệt rõ Data Validity, Project Scope và Modeling Eligibility; không xóa mù 3,423 dòng vi phạm hợp đồng ban đầu. |
| **10. Đề xuất Cleaning Policy có căn cứ** | **PASS** | Hoàn thành [docs/eda_findings_and_cleaning_policy.md](file:///d:/ai-club-end-training/docs/eda_findings_and_cleaning_policy.md) với 7 chính sách chi tiết. |
| **11. Toàn bộ test suite được chạy lại** | **PASS** | Đạt **51/51 unit tests passed** (100% Pass trong 0.54s). |
| **12. Không có kết quả giả hoặc claim vô căn cứ** | **PASS** | Mọi số liệu và nhận định đều dẫn xuất từ dữ liệu thực và biểu đồ thực tế. |
| **13. Chưa huấn luyện mô hình Machine Learning** | **PASS** | Tuân thủ triệt để phạm vi: Phase 4 dừng lại ở EDA & Data Quality; không chạy model. |
| **14. Không tự động commit Git** | **PASS** | Kiểm tra `git status`: Toàn bộ thay đổi nằm an toàn trên working tree để học viên tự rà soát. |

---

## 2. Danh Mục Các Tệp Mới & Cập Nhật Trong Phase 4

### Tệp Notebooks & Dữ liệu trung gian:
1. `notebooks/04_eda.ipynb`: Notebook Jupyter hoàn chỉnh, đã thực thi và lưu đầy đủ outputs trực quan (kích thước ~655 KB).
2. `data/processed/cars_clean_phase4.csv`: Tệp dữ liệu trung gian đã chuẩn hóa trường phục vụ EDA và Phase 5 (kích thước ~26.2 MB, được ignore tự động bởi Git).

### Tệp Tài liệu Kỹ thuật & Báo cáo:
3. `reports/figures/phase4/fig01_target_price_distribution.png` đến `fig19_missing_rate_by_column.png`: Hệ thống 19 biểu đồ kỹ thuật.
4. `docs/eda_findings_and_cleaning_policy.md`: Quy chuẩn 7 chính sách làm sạch dữ liệu và tái đánh giá validation.
5. `reports/phase4_eda_report.md`: Báo cáo kỹ thuật EDA chuyên sâu gồm 12 mục hoàn chỉnh.
6. `reports/phase4_completion_checklist.md`: Bảng nghiệm thu hoàn thành giai đoạn Phase 4 này.

---

## 3. Điều Kiện Chuyển Giao Sang Phase 5 (Transition Gates to Phase 5)

Dự án đã thỏa mãn đầy đủ các điều kiện tiên quyết để chuyển giao sang **Phase 5: Feature Engineering & Data Preprocessing Pipeline**:
1. Tập dữ liệu đã được đo lường và làm rõ cấu trúc 100%.
2. Chính sách làm sạch dữ liệu đã được định nghĩa chi tiết với 7 quy tắc cụ thể, dự kiến tạo ra tập dữ liệu sạch gồm **27,229 bản ghi chuẩn mực (88.83%)**.
3. Rủi ro pháp lý về xuất xứ dữ liệu nguồn tiếp tục được ghi nhận là `PENDING_LICENSE_OR_PROVENANCE` (chỉ phục vụ nghiên cứu học thuật nội bộ, không phát hành thương mại).
4. Nhánh cào website Oto.com.vn tiếp tục được bảo vệ bởi chốt an toàn `dry_run=True`.
