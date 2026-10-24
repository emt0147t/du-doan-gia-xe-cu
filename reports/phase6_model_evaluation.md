# Báo Cáo Kỹ Thuật Đánh Giá Mô Hình Học Máy (Phase 6 Model Evaluation Report)
*(Used Car Price Prediction in Vietnam: An End-to-End Machine Learning Project)*

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam
- **Giai đoạn**: **Phase 6 — Model Training, Comparison & Evaluation**
- **Thời gian lập**: 19/10/2026, 05:30:00 (Múi giờ: Asia/Ho_Chi_Minh)
- **Người thực hiện**: Senior Data Scientist, ML Engineer & AI Student
- **Tài liệu tham chiếu**: [Đề cương mô hình hóa](file:///d:/ai-club-end-training/docs/modeling_protocol.md), [Từ điển dữ liệu](file:///d:/ai-club-end-training/reports/phase5_data_dictionary.md), [Kiểm toán trùng lặp & rò rỉ](file:///d:/ai-club-end-training/reports/phase5_duplicate_and_leakage_audit.md)

---

## 1. Tóm Tắt Hoạt Động (Executive Summary)

Trong Phase 6, nhóm nghiên cứu đã triển khai toàn diện quy trình huấn luyện, tinh chỉnh, so sánh và đánh giá các mô hình học máy theo nguyên tắc **Zero Data Leakage** nghiêm ngặt.

### Các kết quả nổi bật:
1. **Thiết lập chuẩn mực cơ sở (Baselines)**: Xác lập mức sai số cơ sở với `DummyRegressor(median)` có MAE đạt **914.6 triệu VND** và `DummyRegressor(mean)` có MAE đạt **1.164 tỷ VND**.
2. **Khảo sát đa dạng 10 cấu hình mô hình**: Huấn luyện thành công các mô hình Tuyến tính có điều chuẩn (Ridge, Lasso), Mô hình rừng ngẫu nhiên (Random Forest) và Mô hình Gradient Boosting (HistGradientBoosting) trên cả hai không gian nhãn mục tiêu (Giá thô VND và Biến đổi Logarit $\ln(\text{price\_vnd})$).
3. **Mô hình vô địch trên tập Validation (Champion Model)**:
   - Kiến trúc: **`Tree_RandomForest_Tuned_LogTarget`** (Random Forest 150 cây, độ sâu tối đa 24, lá tối thiểu 1, huấn luyện trên không gian Log).
   - **Validation MAE: 142.9 triệu VND** (giảm **84.4% sai số** so với Baseline Median và giảm **87.7%** so với Baseline Mean).
   - **Validation $R^2$: 0.8694** (giải thích 86.94% phương sai giá xe).
   - **Validation MdAPE: 4.25%** (một nửa số xe được dự đoán với độ lệch dưới 4.25% giá thị trường).
4. **Kiểm định độc lập trên tập Test chưa từng thấy (Unseen Test Set — 2,351 xe)**:
   - Chạy kiểm định **đúng một lần duy nhất** sau khi chốt mô hình trên Validation.
   - **Test MAE đạt 111.8 triệu VND**, **Test $R^2$ đạt 0.9448**, và **Test MdAPE đạt 4.29%**, khẳng định năng lực tổng quát hóa xuất sắc, không xảy ra hiện tượng overfitting.
5. **Phân tích độ nhạy Cohort B (2010–2023)**:
   - Mô hình huấn luyện trên Cohort A (2015+) khi áp dụng trực tiếp cho xe đời sâu (2010–2014) có MAE là 314.1 triệu VND và $R^2=0.5438$ (do mô hình cây không thể ngoại suy ngoài miền năm đã học).
   - Khi tái huấn luyện trên toàn bộ Cohort B (27,299 dòng), mô hình đạt **Test MAE 110.6 triệu VND** và **Test $R^2=0.9567$**, chứng minh kiến trúc có độ bền vững cao khi mở rộng phạm vi thời gian.

---

## 2. Dữ Liệu, Cohort & Phân Chia Tập (Dataset, Cohort & Splits)

- **Dữ liệu huấn luyện**: [data/processed/cars_clean_phase5.csv](file:///d:/ai-club-end-training/data/processed/cars_clean_phase5.csv) (23,510 bản ghi sạch, Cohort A: năm $\ge 2015$, tuân thủ Điều lệ dự án).
- **Phân chia tập (80/10/10)**:
  - **Tập Huấn luyện (Train)**: **18,808 dòng (80.0%)** — Giá trung vị: 719,000,000 VND.
  - **Tập Kiểm định (Validation)**: **2,351 dòng (10.0%)** — Giá trung vị: 718,000,000 VND.
  - **Tập Kiểm thử (Test)**: **2,351 dòng (10.0%)** — Giá trung vị: 719,000,000 VND.
- **Tính độc lập & Chống rò rỉ**:
  - 100% không trùng lặp `listing_id` giữa 3 tập (Strict Disjointness).
  - Toàn bộ 9 cột gây rò rỉ (`price_vnd`, `log_price`, `Giá`, `listing_id`, `url`, `Mô tả`,...) bị loại bỏ hoàn toàn khỏi ma trận đặc trưng $X$ (15 đặc trưng: 8 định lượng + 7 phân loại).

---

## 3. Bảng Tổng Hợp So Sánh 10 Cấu Hình Trên Tập Validation (Validation Leaderboard)

Toàn bộ 10 cấu hình được huấn luyện trên cùng tập Train (18,808 dòng) và đánh giá trên cùng tập Validation (2,351 dòng). Mọi chỉ số sai số đều được nghịch đảo hàm mũ và tính toán theo **đơn vị VND thực tế**:

| Hạng | Tên thí nghiệm (Experiment Name) | Nhãn mục tiêu | Preprocessor | MAE (VND) | RMSE (VND) | $R^2$ | MAPE (%) | MdAPE (%) | Thời gian Fit (s) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 🥇 1 | **Tree_RandomForest_Tuned_LogTarget** | **log** | **tree** | **142,934,537** | **950,065,306** | **0.8694** | **7.06%** | **4.25%** | 4.94s |
| 🥈 2 | `Tree_RandomForest_LogTarget` | log | tree | 159,102,971 | 1,043,403,506 | 0.8425 | 8.15% | 4.94% | 8.45s |
| 🥉 3 | `Tree_RandomForest_RawTarget` | raw | tree | 168,751,598 | 852,439,800 | 0.8949 | 10.60% | 6.61% | 8.36s |
| 4 | `Tree_HistGBM_LogTarget` | log | tree | 180,831,847 | 1,208,263,000 | 0.7888 | 8.34% | 5.37% | 4.20s |
| 5 | `Tree_HistGBM_RawTarget` | raw | tree | 201,925,471 | 1,051,263,000 | 0.8401 | 12.10% | 7.84% | 7.01s |
| 6 | `Linear_Ridge_LogTarget` | log | linear | 255,658,033 | 1,441,061,000 | 0.6996 | 10.66% | 7.72% | 0.14s |
| 7 | `Linear_Lasso_LogTarget` | log | linear | 370,691,840 | 1,772,436,000 | 0.5455 | 16.30% | 12.22% | 1.23s |
| 8 | `Linear_Ridge_RawTarget` | raw | linear | 379,429,332 | 1,153,552,000 | 0.8075 | 34.87% | 23.72% | 0.17s |
| 9 | `Baseline_Dummy_Median` | raw | tree | 914,616,759 | 2,721,373,000 | -0.0714 | 48.88% | 39.83% | 0.09s |
| 10 | `Baseline_Dummy_Mean` | raw | tree | 1,164,209,470 | 2,629,313,000 | -0.0001 | 123.46% | 94.34% | 0.06s |

---

## 4. Phân Tích Chuyên Sâu Từng Dòng Mô Hình (Model Analysis & Insights)

### 4.1. Phân tích Mô hình Tuyến tính (Ridge vs Lasso)
- **Hồi quy Ridge**:
  - Với nhãn Raw VND: Đạt $R^2=0.8075$ nhưng MAE lên tới 379.4 triệu VND và MdAPE lên tới 23.72%. Nguyên nhân là do hàm mất mát bình phương tối thiểu (MSE) trên giá trị tiền lớn bị chi phối bởi các xe 5–40 tỷ, khiến mô hình hy sinh độ chính xác trên phân khúc xe phổ thông (300M–700M).
  - Với nhãn Log target: Biến đổi logarit nén dải động của giá, giúp Ridge giảm MAE từ 379.4M xuống **255.7M VND** và giảm MdAPE từ 23.72% xuống **7.72%**.
- **Hồi quy Lasso ($L_1$)**:
  - Co nhiều trọng số về 0 giúp chọn lọc biến, nhưng năng lực dự đoán ($R^2=0.5455$, MAE 370.7M) thấp hơn Ridge do bỏ qua nhiều tương tác danh mục phân tán của các dòng xe hiếm.

### 4.2. Phân tích Mô hình Cây & Ensemble (Random Forest vs HistGradientBoosting)
- **Random Forest**:
  - Thể hiện sự vượt trội toàn diện nhờ khả năng nắm bắt các mối quan hệ phi tuyến và tương tác giữa thương hiệu (`brand`), phiên bản (`model`), dung tích động cơ và phân khúc xe sang mà không cần giả định phân phối.
  - Cấu hình tuned (`max_depth=24`, `min_samples_leaf=1`, `n_estimators=150`) trên không gian Log đạt đỉnh cao về độ chính xác: MAE **142.9 triệu VND**, MdAPE **4.25%**.
- **HistGradientBoosting**:
  - Tốc độ huấn luyện ấn tượng (3–4 giây), cạnh tranh trực tiếp với Random Forest (MAE 180.8M trên Log target), là ứng viên phù hợp cho các môi trường có hạn chế tài nguyên tính toán.

---

## 5. Phân Tích Sai Số (Error Analysis)

Các biểu đồ phân tích lỗi được kết xuất tại [`reports/figures/phase6/`](file:///d:/ai-club-end-training/reports/figures/phase6/):

### 5.1. Tương quan Giá thực tế vs Giá dự đoán & Phân phối phần dư
- **Actual vs Predicted Plot** ([`reports/figures/phase6/actual_vs_predicted.png`](file:///d:/ai-club-end-training/reports/figures/phase6/actual_vs_predicted.png)):
  - Đa số các điểm dữ liệu tập trung bám sát đường lý tưởng $y=x$ trong khoảng giá từ 300 triệu đến 5 tỷ VND.
  - Phân tán bắt đầu tăng nhẹ ở phân khúc trên 10 tỷ VND (xe siêu sang hiếm gặp như Bentley, Rolls-Royce).
- **Residual Distribution Plot** ([`reports/figures/phase6/residual_distribution.png`](file:///d:/ai-club-end-training/reports/figures/phase6/residual_distribution.png)):
  - Phân phối phần dư đối xứng chuẩn, tập trung cao độ quanh điểm 0. Hơn 85% các dự đoán có sai số nằm trong khoảng $[-100\text{ triệu}, +100\text{ triệu}]$.

### 5.2. Sai số theo Phân khúc giá & Năm sản xuất
- **Error by Price Segment** ([`reports/figures/phase6/error_by_price_segment.png`](file:///d:/ai-club-end-training/reports/figures/phase6/error_by_price_segment.png)):
  - **Dưới 500 triệu (n=708)**: MdAPE đạt **4.2%** (sai số trung vị chỉ ~16 triệu VND).
  - **500M – 1 Tỷ (n=912)**: MdAPE đạt **3.8%** (sai số trung vị chỉ ~28 triệu VND).
  - **1 Tỷ – 2 Tỷ (n=452)**: MdAPE đạt **4.5%** (sai số trung vị ~60 triệu VND).
  - **Trên 2 Tỷ (n=279)**: MdAPE đạt **5.9%** (sai số trung vị ~180 triệu VND).
- **Error by Year** ([`reports/figures/phase6/error_by_year.png`](file:///d:/ai-club-end-training/reports/figures/phase6/error_by_year.png)):
  - Sai số trung vị (Median Absolute Error) qua các năm 2015–2023 duy trì ổn định trong khoảng **25 – 45 triệu VND**. MAE trung bình bị kéo cao ở các năm gần đây (2021–2023) do sự xuất hiện của các dòng xe lướt siêu sang giá 20–45 tỷ.

### 5.3. Sai số theo Hãng xe dẫn đầu thị trường
- **Error by Brand** ([`reports/figures/phase6/error_by_brand.png`](file:///d:/ai-club-end-training/reports/figures/phase6/error_by_brand.png)):
  - Các hãng xe đại chúng có thanh khoản cao (Toyota, Hyundai, Kia, Mazda, Ford) đạt sai số trung vị tuyệt đối chỉ **18 – 35 triệu VND**.
  - Mercedes-Benz có sai số trung bình cao hơn (~160 triệu VND) do độ rộng phổ giá giữa dòng C-Class (1.2 tỷ) và Maybach/G63 (8–13 tỷ).

---

## 6. Phân Tích Tầm Quan Trọng Của Đặc Trưng (Feature Importance & Interpretability)

Trích xuất tầm quan trọng đặc trưng dựa trên độ giảm phương sai (Mean Decrease in Impurity - MDI) từ mô hình vô địch Random Forest ([`reports/figures/phase6/feature_importance.png`](file:///d:/ai-club-end-training/reports/figures/phase6/feature_importance.png)):

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                 TẦM QUAN TRỌNG ĐẶC TRƯNG GỘP (MDI / GIẢM PHƯƠNG SAI)        │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. is_luxury_brand       : 43.10% (Phân khúc xe sang vs phổ thông)          │
│ 2. engine_displacement_l : 26.35% (Dung tích xi-lanh gắn liền thuế TTĐB)     │
│ 3. brand                 :  5.72% (Uy tín & thương hiệu)                    │
│ 4. model                 :  5.63% (Dòng xe / Trim cụ thể)                   │
│ 5. car_age               :  4.41% (Tuổi xe / Thời gian hao mòn)             │
│ 6. year                  :  3.52% (Năm sản xuất)                            │
│ 7. transmission          :  2.38% (Số tự động vs Số sàn)                    │
│ 8. seats                 :  2.31% (Số chỗ ngồi - 5 chỗ vs 7 chỗ)            │
│ 9. fuel_type             :  2.12% (Nhiên liệu - Máy dầu, Xăng, Hybrid)      │
│ 10. body_type            :  1.87% (Kiểu dáng SUV, Sedan, Pickup)            │
│ 11. origin               :  1.48% (Nhập khẩu vs Lắp ráp trong nước)         │
│ 12. mileage_km           :  0.69% (Số ODO thực tế)                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

> [!NOTE]
> **Giải thích nghiệp vụ thực tiễn**:
> - Tại Việt Nam, **`is_luxury_brand` (43.1%)** và **`engine_displacement_l` (26.35%)** chiếm gần 70% tổng trọng số quyết định giá xe. Điều này phản ánh chính xác cấu trúc biểu thuế tiêu thụ đặc biệt (TTĐB) tại Việt Nam: xe có động cơ trên 3.0L đến 6.0L bị áp thuế suất từ 90% đến 150%, khiến dung tích động cơ trở thành biến dự báo giá trị tuyệt đối mạnh nhất.
> - `mileage_km` có tỷ trọng tương đối thấp (0.69%) trong phân định giá toàn thị trường vì sự phân hóa giữa các phân khúc xe (Vios vs Lexus) lớn hơn rất nhiều so với độ chênh lệch do ODO mang lại. Tuy nhiên, trong cùng một dòng xe (ví dụ cùng Vios 2020), ODO vẫn đóng vai trò điều chỉnh giá cục bộ.

---

## 7. Kết Quả Kiểm Định Cuối Cùng Trên Tập Test Độc Lập (Final Test Evaluation)

Tuân thủ nguyên tắc chỉ đạo: **Tập Test được giữ kín hoàn toàn và chỉ đánh giá đúng một lần sau khi đã chốt mô hình chiến thắng**.

Kết quả ghi nhận tại [`reports/model_experiments/final_test_results.csv`](file:///d:/ai-club-end-training/reports/model_experiments/final_test_results.csv) trên 2,351 xe chưa từng thấy:

| Mô hình kiểm thử | Test MAE (VND) | Test RMSE (VND) | Test $R^2$ | Test MAPE (%) | Test MdAPE (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| 🏆 **Tree_RandomForest_Tuned_LogTarget (CHAMPION)** | **111,793,581** | **482,625,123** | **0.9448** | **6.84%** | **4.29%** |
| `Tree_HistGBM_LogTarget` | 148,862,299 | 606,933,188 | 0.9127 | 8.23% | 5.58% |
| `Linear_Ridge_LogTarget` | 195,991,014 | 787,720,525 | 0.8529 | 11.02% | 7.96% |
| `Baseline_Dummy_Median` | 844,852,403 | 2,148,985,444 | -0.0947 | 49.93% | 39.83% |
| `Baseline_Dummy_Mean` | 1,090,786,463 | 2,054,291,879 | -0.0004 | 125.07% | 94.07% |

### So sánh Hiệu năng Khái quát hóa (Validation vs Test):
- **Validation MAE**: 142.9 triệu VND $\rightarrow$ **Test MAE**: **111.8 triệu VND**.
- **Validation $R^2$**: 0.8694 $\rightarrow$ **Test $R^2$**: **0.9448**.
- **Validation MdAPE**: 4.25% $\rightarrow$ **Test MdAPE**: **4.29%**.
- *Ghi chú kiểm toán độ phân tán ngoại lai*: Việc Test MAE thấp hơn Validation MAE không phải do mô hình tổng quát hóa vượt trội hơn, mà bắt nguồn từ phân phối xe siêu sang (>5 tỷ VND) có độ lệch phương sai lớn (Validation có 1 xe siêu sang sai số cá biệt lên tới 35.75 tỷ VND, kéo MAE toàn tập tăng thêm ~15.2 triệu VND; trong khi ở phân khúc đại chúng <1 tỷ VND, MAE giữa Validation và Test hoàn toàn tương đồng ở mức ~25.5 triệu và ~40.5 triệu VND). Sai số trung vị phần trăm (MdAPE) đạt 4.25% (Val) và 4.29% (Test) khẳng định độ chính xác thực chất trên đa số xe là tương đương.

---

## 8. Phân Tích Độ Nhạy Trên Cohort B (Cohort B Sensitivity Analysis)

Tài liệu kết quả: [`reports/model_experiments/cohort_b_sensitivity_results.json`](file:///d:/ai-club-end-training/reports/model_experiments/cohort_b_sensitivity_results.json)

1. **Khả năng ngoại suy của Model Cohort A trên xe đời cũ (2010–2014, 3,789 dòng)**:
   - Khi áp dụng trực tiếp mô hình Cohort A vào các xe đời 2010–2014, MAE đạt 314.1 triệu VND, $R^2=0.5438$ và MdAPE là 29.64%.
   - *Kết luận*: Cảnh báo rủi ro ngoại suy (extrapolation risk) — mô hình cây quyết định không thể dự đoán chính xác cho các năm sản xuất nằm ngoài khoảng giá trị đã học trong tập Train.
2. **Hiệu năng khi huấn luyện trực tiếp trên toàn bộ Cohort B (2010–2023, 27,299 dòng)**:
   - Khi mở rộng tập huấn luyện gồm cả xe từ 2010: **Validation MAE đạt 106.7 triệu VND ($R^2=0.9500$)** và **Test MAE đạt 110.6 triệu VND ($R^2=0.9567$)**.
   - *Kết luận*: Kiến trúc Random Forest tuned trên Log target có tính tổng quát hóa rất cao khi được cung cấp đầy đủ dữ liệu lịch sử xe đời sâu.

---

## 9. Ý Nghĩa Nghiệp Vụ & Giới Hạn Của Mô Hình (Business Value & Limitations)

### 9.1. Ý nghĩa kinh tế của chỉ số MAE 111.8 triệu & MdAPE 4.29%
- **Trong giao dịch thực tế**: Đối với một chiếc xe cũ tầm trung (giá 500 – 700 triệu VND), biên độ thương lượng (mặc cả) giữa người mua và showroom tại Việt Nam thông thường dao động từ 15 – 30 triệu VND (~3 – 5% giá trị xe). Mức sai số trung vị **4.29%** của mô hình nằm trọn trong biên độ thương lượng thị trường, cho phép ứng dụng mô hình như một công cụ tham chiếu giá độc lập, khách quan cho người tiêu dùng và chuyên viên định giá xe cũ.

### 9.2. Giới hạn kỹ thuật & Rủi ro rò rỉ dữ liệu (Limitations & Risks)
1. **Xe mới tại showroom (Dealer Inventory)**: Khoảng 25.8% dữ liệu là xe mới tại showroom có ODO = 0 km và giá niêm yết cố định. Dù đã phân tách cờ `condition` và `is_zero_mileage`, sự xuất hiện của các tin rao xe mới có thể làm giảm sai số nhân tạo đối với phân khúc xe nguyên bản.
2. **Cross-posting**: Có khoảng 633 tin rao có mô tả trùng khớp giữa các salon khác nhau. Do thiếu số khung (VIN) bắt buộc, việc gom nhóm chỉ có thể thực hiện ở mức độ tin đăng cá lẻ.
3. **Phân khúc xe siêu sang (>10 tỷ VND)**: Số lượng mẫu ít (dưới 150 xe trên toàn quốc) khiến phương sai dự đoán ở phân khúc này lớn hơn phân khúc đại chúng.

---

## 10. Danh Mục Artifact Đã Xuất Bản (Artifact Outputs)

```text
d:\ai-club-end-training\
├── docs/
│   └── modeling_protocol.md                  (Đề cương giao thức mô hình hóa chuẩn)
├── models/
│   ├── champion_random_forest.joblib         (Artifact mô hình chiến thắng - 31 MB, ignored git)
│   └── champion_model_metadata.json          (Siêu dữ liệu kiểm toán và kiến trúc mô hình)
├── reports/
│   ├── model_experiments/
│   │   ├── experiment_results.csv            (Bảng kết quả 10 thí nghiệm trên Validation)
│   │   ├── validation_predictions.csv        (Bảng giá trị dự đoán chi tiết 2,351 dòng Val)
│   │   ├── experiment_metadata.json          (Metadata băm SHA-256 các thí nghiệm)
│   │   ├── final_test_results.csv            (Bảng kết quả đánh giá cuối cùng trên Test)
│   │   ├── final_test_predictions.csv        (Bảng giá trị dự đoán chi tiết 2,351 dòng Test)
│   │   └── cohort_b_sensitivity_results.json (Kết quả phân tích độ nhạy Cohort B)
│   ├── figures/phase6/
│   │   ├── actual_vs_predicted.png           (Đồ thị tương quan thực tế vs dự đoán)
│   │   ├── residual_distribution.png         (Đồ thị phân phối chuẩn của phần dư)
│   │   ├── residual_vs_predicted.png         (Kiểm tra phương sai thay đổi Heteroscedasticity)
│   │   ├── error_by_year.png                 (Biểu đồ sai số theo năm sản xuất 2015-2023)
│   │   ├── error_by_price_segment.png        (Biểu đồ sai số tỷ đối theo phân khúc giá)
│   │   ├── error_by_brand.png                (Biểu đồ sai số theo Top 6 hãng xe)
│   │   └── feature_importance.png            (Biểu đồ tầm quan trọng đặc trưng gộp và chi tiết)
│   └── phase6_model_evaluation.md            (Báo cáo kỹ thuật tổng hợp toàn diện Phase 6)
└── tests/
    └── test_modeling.py                      (7 unit tests cho hệ thống mô hình hóa)
```

---

## 11. Kiểm Thử Tự Động Toàn Diện (Automated Test Suite)

Toàn bộ **77 unit tests** (bao gồm 7 test mới cho module mô hình hóa) đều chạy thành công 100% trong **1.99 giây** (0 fail, 0 warning):

```powershell
pytest -v --tb=short
# ============================= 77 passed in 1.99s ==============================
```
- Đã xác minh: Tính bất biến của dữ liệu thô, an toàn rò rỉ feature matrix, kiểm thử hàm nghịch đảo logarit, kiểm định tính tái lập của seed ngẫu nhiên.
- Chưa tạo bất kỳ commit Git tự động nào; toàn bộ thay đổi được lưu trữ an toàn trên working tree sẵn sàng cho Mentor và Hội đồng nghiệm thu.
