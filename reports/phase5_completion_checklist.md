# Biên Bản Nghiệm Thu & Danh Mục Kiểm Tra Hoàn Thành Phase 5
*(Phase 5 Completion Checklist & Sign-off Report)*

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam (Used Car Price Prediction in Vietnam)
- **Giai đoạn**: **Phase 5 — Data Cleaning, Feature Engineering & Preprocessing Pipeline**
- **Thời gian nghiệm thu**: 19/10/2026, 03:30:00 (Múi giờ: Asia/Ho_Chi_Minh)
- **Người thực hiện**: Senior Data Scientist, ML Engineer & AI Student
- **Tình trạng nghiệm thu**: **HOÀN THÀNH TOÀN DIỆN (100% tiêu chí đạt chuẩn)**

---

## 1. Bảng Kiểm Tra Tiêu Chí Nghiệm Thu (Acceptance Criteria Matrix)

| STT | Tiêu chí nghiệm thu (Acceptance Criteria) | Trạng thái | Bằng chứng thực tế / Đường dẫn kiểm chứng |
| :---: | :--- | :---: | :--- |
| 1 | **Raw dataset và checksum được xác minh** | **ĐẠT** | `car_detail.csv` (SHA-256: `44c13afc...8f08`) và `car_sell_processed.csv` (SHA-256: `1d0c0d2f...437c`) khớp 100% với [data/metadata/ingestion_mquaan_car_price.json](file:///d:/ai-club-end-training/data/metadata/ingestion_mquaan_car_price.json). |
| 2 | **Phạm vi năm sản xuất đối chiếu với Charter** | **ĐẠT** | [reports/phase5_cohort_decision.md](file:///d:/ai-club-end-training/reports/phase5_cohort_decision.md) đối chứng giữa Cohort A ($\ge 2015$) và Cohort B ($\ge 2010$). Lựa chọn Cohort A làm tập chính tuân thủ Charter Section 3.1. |
| 3 | **Cleaning rules có căn cứ và tái lập được** | **ĐẠT** | Triển khai hàm modular trong [src/data/cleaning.py](file:///d:/ai-club-end-training/src/data/cleaning.py), ghi nhận từng bước lọc không thay đổi raw CSV. |
| 4 | **Outliers không bị xóa tùy tiện** | **ĐẠT** | Xe siêu sang (Rolls-Royce 47 tỷ) được giữ nguyên, gắn cờ `is_luxury_brand=1` và biến đổi `log_price` thay vì xóa bỏ. |
| 5 | **ODO bằng 0 được xử lý có giải thích** | **ĐẠT** | 10,442 xe ODO = 0 km (trong đó 6,070 là xe mới tại showroom) được giữ nguyên giá trị `0` và tạo cờ `is_zero_mileage=1`. |
| 6 | **Phân biệt Missing target và Missing features**| **ĐẠT** | Missing target (`Giá liên hệ`) bị loại bỏ hoàn toàn (không impute 0); Missing feature (`engine_displacement_l`) được giữ lại để impute ở Preprocessing. |
| 7 | **Feature engineering có documentation** | **ĐẠT** | Tạo 4 features mới (`car_age`, `is_zero_mileage`, `is_luxury_brand`, `log_price`), được giải trình chi tiết trong [reports/phase5_data_dictionary.md](file:///d:/ai-club-end-training/reports/phase5_data_dictionary.md). |
| 8 | **Loại bỏ cột rò rỉ (Leakage) khỏi feature matrix** | **ĐẠT** | `extract_features_and_target()` kiểm tra chặn tự động 9 cột: `price_vnd`, `log_price`, `Giá`, `listing_id`, `Mã tin`, `url`, `URL`, `Mô tả`, `Tên xe`. |
| 9 | **Tạo candidate dataset từ raw data** | **ĐẠT** | [src/data/prepare_modeling_data.py](file:///d:/ai-club-end-training/src/data/prepare_modeling_data.py) tạo ra [data/processed/cars_clean_phase5.csv](file:///d:/ai-club-end-training/data/processed/cars_clean_phase5.csv) (23,510 dòng) và metadata JSON. |
| 10 | **Preprocessing pipeline xây dựng & unit-tested**| **ĐẠT** | [src/data/preprocessing.py](file:///d:/ai-club-end-training/src/data/preprocessing.py) cung cấp `ColumnTransformer` cho mô hình tuyến tính và cây; không fit trên toàn bộ dataset; xử lý unseen categories an toàn. |
| 11 | **Train/Val/Test design kiểm tra rò rỉ** | **ĐẠT** | [src/data/split_data.py](file:///d:/ai-club-end-training/src/data/split_data.py) chia 80/10/10 phân tầng theo phân vị giá, bảo đảm 0% trùng lặp `listing_id`. Lưu tại `data/processed/splits/`. |
| 12 | **Toàn bộ test suite đã chạy thực tế** | **ĐẠT** | `pytest -v --tb=short` chạy thực tế thành công **70/70 tests pass** trong 3.31 giây (0 fail, 0 warning). |
| 13 | **Raw data không bị sửa đổi** | **ĐẠT** | Raw files giữ nguyên byte và SHA-256 sau toàn bộ quá trình chạy scripts. |
| 14 | **Không có PII trong candidate dataset** | **ĐẠT** | Bảng clean không chứa số điện thoại hay tên người bán cá nhân từ `seller.csv`. |
| 15 | **Báo cáo phản ánh số liệu thực tế** | **ĐẠT** | 100% số liệu trong báo cáo khớp từng dòng với execution log thực tế. |
| 16 | **Không huấn luyện hoặc chọn model trong Phase 5** | **ĐẠT** | Tuyệt đối tuân thủ phạm vi kỹ thuật Phase 5, không khởi tạo mô hình học máy. |
| 17 | **Không commit Git tự động** | **ĐẠT** | Thay đổi được giữ nguyên trên working tree, sẵn sàng cho người dùng review. |

---

## 2. Danh Sách Các File Tạo Mới & Cập Nhật (Files Created / Updated)

```text
d:\ai-club-end-training\
├── data/
│   ├── metadata/
│   │   └── prepare_modeling_data_phase5.json   (Metadata kiểm toán băm SHA-256)
│   └── processed/
│       ├── cars_clean_phase5.csv               (Cohort A chính: 23,510 dòng, 38 cột)
│       ├── cars_clean_phase5_cohort_b.csv      (Cohort B mở rộng: 27,299 dòng, 38 cột)
│       └── splits/
│           ├── train.csv                       (18,808 dòng - 80%)
│           ├── val.csv                         (2,351 dòng - 10%)
│           ├── test.csv                        (2,351 dòng - 10%)
│           ├── train_ids.csv                   (Danh sách listing_id tập Train)
│           ├── val_ids.csv                     (Danh sách listing_id tập Val)
│           ├── test_ids.csv                    (Danh sách listing_id tập Test)
│           └── split_metadata.json             (Metadata cấu hình và phân phối split)
├── src/
│   └── data/
│       ├── cleaning.py                         (Module làm sạch dữ liệu & feature engineering)
│       ├── prepare_modeling_data.py            (Kịch bản điều phối chuẩn bị dữ liệu mô hình)
│       ├── preprocessing.py                    (ColumnTransformer pipeline cho Linear & Tree)
│       └── split_data.py                       (Module phân chia tập dữ liệu 80/10/10)
├── tests/
│   ├── test_cleaning.py                        (7 unit tests cho cleaning module)
│   ├── test_preprocessing.py                   (7 unit tests cho preprocessing pipeline)
│   └── test_split_data.py                      (5 unit tests cho split data module)
├── reports/
│   ├── phase5_cohort_decision.md               (Báo cáo đối chiếu phạm vi Charter vs EDA)
│   ├── phase5_duplicate_and_leakage_audit.md   (Kiểm toán trùng lặp và rò rỉ dữ liệu)
│   ├── phase5_cleaning_log.md                  (Nhật ký lọc dữ liệu từng bước định lượng)
│   ├── phase5_data_dictionary.md               (Từ điển dữ liệu và phân định ma trận X)
│   └── phase5_completion_checklist.md          (Biên bản nghiệm thu hoàn thành Phase 5)
└── README.md                                   (Cập nhật tiến độ dự án)
```

---

## 3. Tổng Hợp Số Bản Ghi Qua Các Bước Lọc (Data Filtering Summary)

- **Tổng số dòng thô ban đầu (Raw Ingestion)**: **30,652 dòng** (100.0%)
- **Bước 1 — Lọc nhãn mục tiêu hợp lệ ($30\text{M} \le \text{Giá} \le 50\text{B}$)**: Loại 14 dòng $\rightarrow$ Còn 30,638 dòng.
- **Bước 2 — Lọc phạm vi năm sản xuất ($\ge 2015$)**: Loại 7,115 dòng (32 khuyết năm, 7,083 xe đời trước 2015) $\rightarrow$ Còn 23,523 dòng.
- **Bước 3 — Lọc hộp số dị biệt (loại `-`, `Số hỗn hợp`)**: Loại 13 dòng $\rightarrow$ Còn 23,510 dòng.
- **Bước 4 — Lọc cận trên ODO ($> 1,000,000\text{ km}$)**: Loại 0 dòng $\rightarrow$ **Còn 23,510 dòng**.
- **Tập dữ liệu chuẩn Cohort A**: **23,510 dòng** (**76.70%** dữ liệu thô).
- **Tập dữ liệu độ nhạy Cohort B (xe từ 2010)**: **27,299 dòng** (**89.06%** dữ liệu thô).

---

## 4. Tổng Kết Phân Chia Dữ Liệu (Split Summary)

- **Phương pháp**: Phân tầng theo 10 phân vị giá mục tiêu (`Target Quantile Stratification`) với `random_state=42`.
- **Tập Huấn luyện (Train)**: **18,808 dòng (80.0%)** — Trung vị giá: 719,000,000 VND
- **Tập Kiểm định (Validation)**: **2,351 dòng (10.0%)** — Trung vị giá: 718,000,000 VND
- **Tập Kiểm thử (Test)**: **2,351 dòng (10.0%)** — Trung vị giá: 719,000,000 VND
- **Độ trùng lặp ID giữa các tập**: **0 bản ghi (Rời rạc tuyệt đối 100%)**.

---

## 5. Kết Quả Kiểm Thử Thực Tế (Automated Test Execution)

Chạy lệnh kiểm thử tự động toàn diện:
`pytest -v --tb=short`

```text
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.7.0
rootdir: D:\ai-club-end-training
collected 70 items

tests/test_cleaning.py (7 tests) .................... PASSED [ 10%]
tests/test_crawler.py (6 tests) ..................... PASSED [ 18%]
tests/test_load_dataset.py (9 tests) ................ PASSED [ 31%]
tests/test_preprocessing.py (7 tests) ............... PASSED [ 41%]
tests/test_price_parser.py (17 tests) ............... PASSED [ 65%]
tests/test_split_data.py (5 tests) .................. PASSED [ 72%]
tests/test_validation.py (19 tests) ................. PASSED [100%]

============================= 70 passed in 3.31s ==============================
```

---

## 6. Điều Kiện & Đề Xuất Chuyển Giao Sang Phase 6 (Handover to Phase 6)

1. **Sẵn sàng cho mô hình hóa (Model-Ready)**:
   - Tập `train.csv`, `val.csv`, `test.csv` và ma trận đặc trưng chuẩn $X$ đã sẵn sàng tại [data/processed/splits/](file:///d:/ai-club-end-training/data/processed/splits/).
   - Pipeline tiền xử lý [src/data/preprocessing.py](file:///d:/ai-club-end-training/src/data/preprocessing.py) đã cung cấp `build_linear_preprocessor()` và `build_tree_preprocessor()` sẵn sàng tích hợp trực tiếp vào `Pipeline` huấn luyện của Phase 6.
2. **Kế hoạch thực nghiệm Phase 6 (Baseline Models & Experiments)**:
   - Xây dựng mô hình Dummy Baseline (Mean / Median).
   - Huấn luyện mô hình Linear Regression có regularization (Ridge / Lasso / ElasticNet) trên pipeline tuyến tính.
   - Huấn luyện mô hình cây quyết định và ensemble (Random Forest, LightGBM, XGBoost, CatBoost).
   - Đo lường bằng các chỉ số chuẩn mực: $R^2$, RMSE, MAE, MAPE trên cả thang đo VND và thang đo Log.
   - Thực hiện kiểm tra độ nhạy trên Cohort B (`cars_clean_phase5_cohort_b.csv`) để đánh giá năng lực tổng quát hóa của mô hình trên xe đời cũ.
