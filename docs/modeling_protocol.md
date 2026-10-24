# Đề Cương Giao Thức Mô Hình Hóa Học Máy (Machine Learning Modeling Protocol)
*(Phase 6 — Model Training, Comparison & Evaluation Protocol)*

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam (Used Car Price Prediction in Vietnam)
- **Giai đoạn**: Phase 6 — Model Training, Comparison & Evaluation
- **Thời gian lập**: 19/10/2026, 04:00:00 (Múi giờ: Asia/Ho_Chi_Minh)
- **Người thực hiện**: Senior Data Scientist, ML Engineer & AI Student
- **Tài liệu tham chiếu**: [Project Charter](file:///d:/ai-club-end-training/docs/project_charter.md), [Data Dictionary](file:///d:/ai-club-end-training/reports/phase5_data_dictionary.md), [Duplicate & Leakage Audit](file:///d:/ai-club-end-training/reports/phase5_duplicate_and_leakage_audit.md)

---

## 1. Mục Tiêu & Định Nghĩa Biến Mục Tiêu (Objective & Target Variable)

- **Bài toán**: Hồi quy có giám sát (Supervised Regression).
- **Biến mục tiêu chính ($y$)**: `price_vnd` — Giá rao bán xe ô tô tính theo Đồng Việt Nam (VND).
- **Thử nghiệm mở rộng**: `log_price = ln(price_vnd)` nhằm ổn định phương sai cho các mô hình nhạy cảm với độ lệch phải (positive skewness). Khi đánh giá, mọi dự đoán trên thang đo log **bắt buộc phải được nghịch đảo hàm mũ ($\exp(\hat{y})$)** về đơn vị VND trước khi tính các chỉ số MAE, RMSE so sánh.

---

## 2. Phạm Vi Tập Dữ Liệu & Phân Chia Tập (Scope & Dataset Splits)

### 2.1. Phân định Cohorts
1. **Cohort chính (Primary Modeling Cohort — Cohort A)**:
   - Điều kiện: Năm sản xuất $\ge 2015$ (`year >= 2015`).
   - Quy mô: **23,510 bản ghi sạch** (khớp 100% Điều lệ dự án Section 3.1).
   - Tệp nguồn: [`data/processed/cars_clean_phase5.csv`](file:///d:/ai-club-end-training/data/processed/cars_clean_phase5.csv).
2. **Cohort phụ (Extended Sensitivity Cohort — Cohort B)**:
   - Điều kiện: Năm sản xuất $\ge 2010$ (`year >= 2010`).
   - Quy mô: **27,299 bản ghi sạch**.
   - Mục đích: Đánh giá độ nhạy của mô hình trên xe đời sâu (2010–2014) sau khi đã chốt mô hình trên Cohort A.

### 2.2. Chiến lược phân chia (Data Splitting Strategy)
- Tỷ lệ phân chia: **80% Train (18,808 dòng) / 10% Validation (2,351 dòng) / 10% Test (2,351 dòng)**.
- Phương pháp: Phân tầng theo 10 phân vị giá (`Target Quantile Stratification`) với `random_state=42`.
- Tính rời rạc: Trùng lặp `listing_id` giữa các tập đạt **0 bản ghi (100% độc lập)**.
- Lưu trữ: Thư mục [`data/processed/splits/`](file:///d:/ai-club-end-training/data/processed/splits/).

---

## 3. Quy Tắc Lựa Chọn Đặc Trưng & Chống Rò Rỉ (Feature Governance & Zero Leakage)

### 3.1. Danh mục đặc trưng được phép đưa vào ma trận $X$
- **Numeric Features (8 đặc trưng)**:
  - `year`: Năm sản xuất (2015–2023).
  - `car_age`: Tuổi xe tính từ mốc cố định $2024 - \text{year}$.
  - `mileage_km`: Số km đã đi (ODO).
  - `is_zero_mileage`: Cờ nhị phân (1 nếu ODO = 0, 0 nếu ODO > 0).
  - `engine_displacement_l`: Dung tích động cơ (L).
  - `seats`: Số chỗ ngồi.
  - `doors`: Số cửa.
  - `is_luxury_brand`: Cờ xe sang (Mercedes, BMW, Lexus, Porsche,...).
- **Categorical Features (7 đặc trưng)**:
  - `brand`: Thương hiệu xe (51 hãng).
  - `model`: Dòng xe / Model chi tiết (586 nhãn).
  - `condition`: Tình trạng (`Xe mới`, `Xe đã dùng`).
  - `transmission`: Hộp số (`Tự động`, `Số tay`).
  - `origin`: Xuất xứ (`Trong nước`, `Nhập khẩu`).
  - `body_type`: Kiểu dáng (SUV, Sedan, Hatchback, Pickup,...).
  - `fuel_type`: Nhiên liệu (`Xăng`, `Dầu`, `Điện`, `Hybrid`).

### 3.2. Danh mục biến tuyệt đối bị loại trừ (Excluded Leakage Columns)
Mã nguồn [`src/data/preprocessing.py`](file:///d:/ai-club-end-training/src/data/preprocessing.py) chặn tự động 9 cột:
- `price_vnd`, `log_price`, `Giá`: Target và các biến thể của target.
- `listing_id`, `Mã tin`: Định danh tin rao.
- `url`, `URL`: Địa chỉ web chứa slug giá.
- `Mô tả`, `Tên xe`: Chứa văn bản giá bán trực tiếp hoặc PII.
- `Hệ thống nạp nhiên liệu`: Khuyết >78.5%.

---

## 4. Kiến Trúc Pipeline Tiền Xử Lý (Preprocessing Architectures)

Pipeline được khởi tạo bằng `ColumnTransformer` chưa fit và **chỉ được fit trên dữ liệu Train**:

1. **Linear Pipeline ([`build_linear_preprocessor`](file:///d:/ai-club-end-training/src/data/preprocessing.py#L118-L157))**:
   - Numeric: `SimpleImputer(strategy='median', add_indicator=True)` $\rightarrow$ `StandardScaler()`.
   - Categorical: `SimpleImputer(strategy='constant', fill_value='missing')` $\rightarrow$ `OneHotEncoder(handle_unknown='ignore', sparse_output=True)`.
2. **Tree Pipeline ([`build_tree_preprocessor`](file:///d:/ai-club-end-training/src/data/preprocessing.py#L160-L197))**:
   - Numeric: `SimpleImputer(strategy='median', add_indicator=True)` (Không cần scaling vì mô hình cây bất biến với biến đổi đơn điệu).
   - Categorical: `SimpleImputer(strategy='constant', fill_value='missing')` $\rightarrow$ `OneHotEncoder(handle_unknown='ignore', sparse_output=True)`.

---

## 5. Danh Sách Mô Hình Thử Nghiệm (Models to Train)

### 5.1. Mô hình cơ sở (Baselines)
1. **Dummy Median**: Dự đoán giá trị trung vị của tập Train cho mọi quan sát.
2. **Dummy Mean**: Dự đoán giá trị trung bình của tập Train cho mọi quan sát.

### 5.2. Mô hình máy học (Machine Learning Models)
1. **Mô hình tuyến tính có điều chuẩn (Regularized Linear Models)**:
   - **Ridge Regression ($L_2$)**: Khảo sát các mức $\alpha \in [0.1, 1.0, 10.0, 100.0]$.
   - **Lasso Regression ($L_1$)**: Khảo sát khả năng co hệ số (sparsity) và chọn lọc đặc trưng.
2. **Mô hình cây phân tán (Tree Ensembles)**:
   - **Random Forest Regressor**: Mô hình rừng ngẫu nhiên phi tuyến, bắt quan hệ tương tác đặc trưng phức tạp.
3. **Mô hình Gradient Boosting**:
   - **HistGradientBoostingRegressor / LightGBM**: Mô hình boosting dựa trên biểu đồ tần suất (histogram-based), tối ưu tốc độ và độ chính xác cao trên dữ liệu bảng lớn.

---

## 6. Chỉ Số Đo Lường & Tiêu Chí Lựa Chọn Mô Hình (Metrics & Decision Protocol)

### 6.1. Các chỉ số đánh giá chuẩn mực
- **MAE (Mean Absolute Error — Đơn vị: VND)**: **Chỉ số quyết định chính (Primary Metric)**. Biểu diễn trực quan sai số trung bình bằng tiền thực tế, không bị phóng đại quá mức bởi vài chiếc siêu xe ngoại lai.
- **RMSE (Root Mean Squared Error — Đơn vị: VND)**: Phạt nặng các sai số lớn; đo lường độ phân tán của phần dư.
- **$R^2$ (Coefficient of Determination)**: Tỷ lệ phương sai của biến mục tiêu được giải thích bởi mô hình.
- **MAPE / MdAPE (Median Absolute Percentage Error — %)**: Đo lường sai số tỷ đối tương đối giữa các phân khúc giá.

### 6.2. Giao thức lựa chọn mô hình (Model Selection Protocol)
1. **Nguyên tắc "Tập Test là Bất Khả Xâm Phạm"**:
   - Mọi so sánh, tinh chỉnh siêu tham số và lựa chọn mô hình **chỉ được diễn ra trên Validation Set**.
   - Tuyệt đối không dùng Test set để chọn mô hình, chọn feature hay điều chỉnh ngưỡng.
2. **Tiêu chuẩn kết luận mô hình chiến thắng**:
   - Mô hình có Validation MAE thấp nhất đồng thời có $R^2$ cao nhất và thời gian dự đoán hợp lý.
3. **Final Evaluation**:
   - Sau khi chốt mô hình chiến thắng trên Validation set, mô hình này và các baseline được đánh giá **đúng một lần duy nhất** trên Test set để báo cáo năng lực tổng quát hóa khách quan.

---

## 7. Giao Thức Phân Tích Lỗi (Error Analysis Protocol)

Với mô hình tốt nhất trên tập Validation:
1. Tính phần dư $e_i = y_i - \hat{y}_i$.
2. Vẽ các biểu đồ kỹ thuật:
   - Actual vs Predicted Scatter Plot.
   - Residual Distribution (Histogram & KDE).
   - Residual vs Predicted Plot (kiểm tra hiện tượng phương sai thay đổi Heteroscedasticity).
3. Phân rã sai số theo các lát cắt nghiệp vụ:
   - Sai số theo nhóm năm sản xuất (2015–2023).
   - Sai số theo phân khúc giá (Dưới 500M, 500M–1B, 1B–2B, Trên 2B).
   - Sai số theo Top 5 hãng xe dẫn đầu thị trường (Toyota, Hyundai, Ford, Mercedes-Benz, Kia).
4. Phân tích Feature Importance (hệ số mô hình tuyến tính hoặc Permutation Importance).
