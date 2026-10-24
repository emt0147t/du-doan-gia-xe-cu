# Báo Cáo Trạng Thái Bàn Giao Dự Án (Delivery Status Report)
*(Used Car Price Prediction in Vietnam: An End-to-End Machine Learning System)*

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam
- **Thời gian lập**: 24/10/2026, 12:40:00 (Múi giờ: Asia/Ho_Chi_Minh)
- **Người kiểm toán**: Senior Machine Learning Engineer & Repository Maintainer
- **Mục tiêu**: Chuẩn bị bàn giao và nộp đồ án cho buổi phỏng vấn AI Club

---

## 1. Kết Quả Kiểm Thử Toàn Trình (Test Suite Verification)

- **Lệnh thực thi**: `pytest -v --tb=short`
- **Môi trường**: Python 3.11.9, pytest 9.1.1, 100% Offline (Không phụ thuộc mạng Internet).
- **Kết quả đo lường**:
  - **Tổng số bài test**: **87 bài test**
  - **Số bài test thành công**: **87/87 PASSED (100%)**
  - **Số bài test thất bại / lỗi**: **0 FAILED, 0 ERROR**
  - **Thời gian thực thi**: **~4.21 giây**
- **Các module kiểm thử**:
  - `tests/test_price_parser.py`: 17 tests (Bóc tách giá tiếng Việt sang VND, xử lý số âm, tỷ, triệu, chữ số, ngoại tệ).
  - `tests/test_validation.py`: 19 tests (Kiểm tra hợp đồng dữ liệu, kiểu dữ liệu, ràng buộc biên, trùng lặp).
  - `tests/test_load_dataset.py`: 8 tests (Nạp dữ liệu cục bộ, đối soát mã băm SHA-256, schema mapping).
  - `tests/test_crawler.py`: 6 tests (Kiểm thử bộ bóc tách DOM, bộ lọc khử PII số điện thoại).
  - `tests/test_cleaning.py`: 7 tests (Làm sạch giá, năm, ODO, phân loại và kỹ nghệ đặc trưng).
  - `tests/test_preprocessing.py`: 7 tests (ColumnTransformer pipeline, an toàn rò rỉ, xử lý unseen categories).
  - `tests/test_split_data.py`: 5 tests (Tỷ lệ phân chia 80/10/10, tính rời rạc 100% ID, phân tầng deciles).
  - `tests/test_duplicate_groups.py`: 6 tests (Gom cụm 4 cấp độ, cách ly 0% rò rỉ nhóm).
  - `tests/test_modeling.py`: 7 tests (Hàm nghịch đảo log, thước đo hồi quy, tính tái lập seed).
  - `tests/test_predict.py`: 4 tests (Chuẩn bị đặc trưng, định dạng VND, tích hợp suy luận CLI).

---

## 2. Trạng Thái Thực Thi Của Notebook Trung Tâm (Notebook Execution Status)

- **Đường dẫn tệp**: [`notebooks/used_car_price_prediction.ipynb`](../notebooks/used_car_price_prediction.ipynb)
- **Trạng thái kiểm tra định dạng**: **JSON hợp lệ (nbformat v4.5)**.
- **Trạng thái thực thi**: **ĐÃ CHẠY TOÀN TRÌNH THÀNH CÔNG (END-TO-END VERIFIED)** với `nbconvert.preprocessors.ExecutePreprocessor`.
- **Tổng số cells**: **27 cells** (15 Markdown cells giải thích chi tiết tiếng Việt + 12 Code cells có outputs thực tế).
- **Phân bổ 13 phần nội dung**:
  1. *Phần 1 — Project Overview*: Đặt vấn đề, bài toán hồi quy có giám sát, asking vs transaction price.
  2. *Phần 2 — Environment & Data Loading*: Import thư viện, kiểm tra phiên bản, nạp dữ liệu bằng đường dẫn tương đối.
  3. *Phần 3 — Exploratory Data Analysis (EDA)*: Phân phối giá thô, skewness, log price, ODO, trực quan hóa.
  4. *Phần 4 — Data Cleaning & Cohort A*: Quy tắc lọc giá, xử lý ODO ngoại lai bằng median, cờ zero-mileage, đối soát dòng 30,652 $\rightarrow$ 23,510.
  5. *Phần 5 — Feature Engineering & Target*: 15 đặc trưng, chặn 9 cột rò rỉ, phân tích rủi ro target leakage.
  6. *Phần 6 — Train/Validation/Test Splits*: Giao thức 80/10/10 phân tầng deciles, seed 42, fit duy nhất trên Train.
  7. *Phần 7 — Preprocessing Pipelines*: ColumnTransformer cho Tree (không scale) và Linear (có scale), OHE ignore unseen.
  8. *Phần 8 — Baseline & Model Training*: Dummy Baselines, Ridge/Lasso, Random Forest, HistGBM, Raw vs Log Target.
  9. *Phần 9 — Validation Leaderboard & Model Selection*: So sánh 10 mô hình, Champion RF Tuned Log Target, Test Phase 6 (MAE 111.8M, R² 0.9448, MdAPE 4.29%), giải mã ngoại lai 39 tỷ ở Val.
  10. *Phần 10 — Champion Model & Inference*: Nạp `models/champion_random_forest.joblib`, dự đoán thực tế cho 3 xe mẫu.
  11. *Phần 11 — Group-Aware Evaluation (Phase 6.2)*: Audit rò rỉ cross-posting 9.15%, gom cụm 4 cấp độ, StratifiedGroupKFold 0% rò rỉ, MdAPE giữ vững 4.29% tuyệt đối, phân rã +27 xe siêu sang.
  12. *Phần 12 — Feature Importance*: MDI (Variance Reduction) vs Permutation, `is_luxury_brand` (43.1%) và `engine_displacement_l` (26.35%) phản ánh thuế TTĐB, giải mã ODO toàn cục vs cục bộ.
  13. *Phần 13 — Conclusion*: Tóm lược kết quả, giới hạn đề tài, định hướng tương lai.

---

## 3. Trạng Thái Dữ Liệu Thực Tế & Quyền Chia Sẻ (Dataset Status & Governance)

- **Trạng thái quyền chia sẻ**: **CHƯA ĐƯỢC XÁC MINH TOÀN DIỆN CHO PUBLIC REPOSITORY**.
  - Dữ liệu thô cào từ `bonbanh.com` chứa thông tin mô tả có thể lẫn số điện thoại người bán cá nhân (PII) và sàn gốc chưa cấp phép mở.
- **Hành động quản trị đã thực thi**:
  - **Tất cả các tệp CSV thật (`data/raw/` và `data/processed/`) được GIỮ NGOÀI REPOSITORY (Excluded via `.gitignore`)**.
  - Đã xuất bản [`data/DATA_README.md`](../data/DATA_README.md) hướng dẫn cách đặt tệp dữ liệu cục bộ.
  - Đã xuất bản [`data/dataset_manifest.json`](../data/dataset_manifest.json) lưu trữ mã băm SHA-256, dung lượng và số dòng để người dùng đối soát.
  - Đã tạo [`data/synthetic_demo_data.csv`](../data/synthetic_demo_data.csv) (40 dòng, 100% nhân tạo độc lập, gắn nhãn `SYNTHETIC_DEMO_ONLY`) cho phép chạy smoke-test mà không cần dữ liệu thật.

---

## 4. Trạng Thái Mô Hình (Model Artifact Status)

- **Mô hình Vô địch**: `models/champion_random_forest.joblib`
- **Dung lượng**: **30,984,932 bytes (~29.55 MB)** (Phù hợp giới hạn GitHub 100 MB).
- **Siêu dữ liệu kiểm toán**: [`models/champion_model_metadata.json`](../models/champion_model_metadata.json)
- **Khả năng nạp và suy luận**: Đã kiểm tra thành công với `python src/models/predict.py --demo` và kiểm thử trong notebook.
- **Quyết định**: **ĐƯỢC COMMIT VÀO GIT REPOSITORY** để người dùng có thể chạy suy luận dự đoán ngay lập tức sau khi clone repository.

---

## 5. Trạng Thái Git & Đích Đến (Git Status & Remote Destination)

- **Local Branch**: `main` (chuyển từ `master`).
- **Remote Target**: `origin` $\rightarrow$ `https://github.com/emt0147t/du-doan-gia-xe-cu.git`
- **Tình trạng Remote ban đầu**: Repository công khai, trống rỗng (0 commits, 0 branches).
- **Các tệp được commit**: Toàn bộ mã nguồn `src/`, unit tests `tests/`, báo cáo `reports/`, slide `presentation/`, notebook `notebooks/`, cấu hình môi trường, manifest dữ liệu và model artifact đã kiểm toán.
- **Các tệp bị loại trừ khỏi Git**:
  - `data/raw/*`: Dữ liệu thô chứa PII và chưa có bản quyền chia sẻ công khai.
  - `data/processed/*`: Các ma trận bảng sạch chứa dữ liệu thực tế.
  - `staging/`, `dist/`: Các tệp build tạm và tệp nén trung gian.
  - `__pycache__/`, `.pytest_cache/`, `.ipynb_checkpoints/`: Bộ nhớ đệm biên dịch.

---

## 6. Phân Định Rõ Ràng: Đã Chạy Kiểm Nghiệm vs Hướng Dẫn Tài Liệu

| Nội dung | Tình trạng thực tế | Bằng chứng kiểm toán |
| :--- | :---: | :--- |
| **87 Unit Tests** | Đã chạy thực tế 100% | `pytest` chạy pass 87/87 trong 4.21s |
| **Notebook used_car_price_prediction.ipynb** | Đã chạy thực tế end-to-end | `ExecutePreprocessor` chạy thành công toàn bộ 27 cells |
| **Model Inference CLI** | Đã chạy thực tế | `predict.py --demo` dự đoán thành công 3 xe |
| **PowerPoint Deck Builder** | Đã chạy thực tế | `build_presentation.py` tạo slide 15 trang 479 KB |
| **Đối soát số liệu Phase 6 & Phase 6.2** | Đã đối soát chéo 100% | Khớp mã băm và số liệu với `experiment_results.csv` |
| **Tái huấn luyện toàn bộ 10 mô hình từ đầu** | Đã chạy trong Phase 6 | Kết quả được ghi nhận tại `experiment_results.csv` |
| **Live Crawling từ website bonbanh** | KHÔNG chạy live | Giữ chốt an toàn `dry_run=True` tuân thủ đạo đức dữ liệu |
