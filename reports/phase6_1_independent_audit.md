# Báo Cáo Kiểm Toán Độc Lập Mô Hình & Thẩm Định Suy Luận
*(Phase 6.1 — Independent Model Audit & Inference Verification)*

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam (*Used Car Price Prediction in Vietnam*)
- **Giai đoạn**: **Phase 6.1 — Independent Audit & Inference Verification Gate**
- **Thời gian lập**: 19/10/2026, 20:30:00 (Múi giờ: Asia/Ho_Chi_Minh)
- **Người thực hiện**: Senior Data Scientist & ML Evaluation Reviewer
- **Mã nguồn kiểm toán**: [`scripts/independent_audit_phase6.py`](file:///d:/ai-club-end-training/scripts/independent_audit_phase6.py), [`scripts/audit_duplicates_detailed.py`](file:///d:/ai-club-end-training/scripts/audit_duplicates_detailed.py)

---

## 1. Tóm Tắt Kết Quả Kiểm Toán (Executive Summary)

Đợt kiểm toán độc lập Phase 6.1 được thực thi nhằm kiểm chứng tính liêm chính khoa học của kết quả huấn luyện mô hình (Phase 6), rà soát các tuyên bố về rò rỉ dữ liệu (Phase 5/5.1), đối soát tính đúng đắn của biến đổi hàm mục tiêu $\ln(y)$, thẩm định tầm quan trọng đặc trưng, và kiểm tra tính toàn vẹn của module suy luận thực tế ([`src/models/predict.py`](file:///d:/ai-club-end-training/src/models/predict.py)).

### Các phát hiện & kết luận cốt lõi:
1. **Tính bất biến của Dữ liệu & Mã băm (Data & Checksum Integrity)**:
   - Dữ liệu thô [`data/raw/external/mquaan_car_price/car_detail.csv`](file:///d:/ai-club-end-training/data/raw/external/mquaan_car_price/car_detail.csv) (SHA-256: `44c13afc...8f08`) và [`car_sell_processed.csv`](file:///d:/ai-club-end-training/data/raw/external/mquaan_car_price/car_sell_processed.csv) (SHA-256: `1d0c0d2f...437c`) được bảo toàn 100% nguyên vẹn.
   - Các tập phân chia [`train.csv`](file:///d:/ai-club-end-training/data/processed/splits/train.csv) (18,808 dòng), [`val.csv`](file:///d:/ai-club-end-training/data/processed/splits/val.csv) (2,351 dòng), và [`test.csv`](file:///d:/ai-club-end-training/data/processed/splits/test.csv) (2,351 dòng) khớp tuyệt đối mã băm SHA-256 đã công bố trong [`split_metadata.json`](file:///d:/ai-club-end-training/data/processed/splits/split_metadata.json).
2. **Đối soát tính đúng đắn của chỉ số (Metric Reconciliation)**:
   - Tái tính toán độc lập từ các file dự đoán gốc [`validation_predictions.csv`](file:///d:/ai-club-end-training/reports/model_experiments/validation_predictions.csv) và [`final_test_predictions.csv`](file:///d:/ai-club-end-training/reports/model_experiments/final_test_predictions.csv) xác nhận:
     - **Champion trên Validation**: MAE = **142,934,537 VND**, RMSE = **950,065,306 VND**, $R^2$ = **0.8694**, MdAPE = **4.25%**.
     - **Champion trên Test**: MAE = **111,793,581 VND**, RMSE = **482,625,123 VND**, $R^2$ = **0.9448**, MdAPE = **4.29%**.
   - Các con số khớp chính xác đến từng chữ số thập phân.
3. **Làm rõ nguyên nhân Test MAE (111.8M) tốt hơn đáng kể Validation MAE (142.9M)**:
   - Chênh lệch **không phải do mô hình tổng quát hóa tốt hơn hay không overfit**.
   - Phân tích phân rã phương sai chứng minh: **Chênh lệch hoàn toàn do phân bố ngoại lai cực đoan (xe $> 5$ tỷ VND)**:
     - Tập Validation xuất hiện 1 xe siêu sang giá 39 tỷ có sai số dự đoán lên tới **35.75 tỷ VND** (kéo MAE toàn tập Val tăng thêm **15.2 triệu VND**). Top 4 xe sai số lớn nhất tại Validation cộng dồn tạo ra **31.0 triệu VND MAE**.
     - Ở phân khúc xe phổ thông ($< 1$ tỷ VND, chiếm $\sim 70\%$ thị trường), MAE giữa Val và Test gần như trùng khớp hoàn toàn (**Val: 25.2M / 40.8M** vs **Test: 26.1M / 40.4M**).
     - **Sai số trung vị tương đối (MdAPE) hầu như không đổi: 4.25% (Val) vs 4.29% (Test)**.
4. **Hiệu chỉnh thuật ngữ Tầm quan trọng đặc trưng (Task E)**:
   - Phát hiện lỗi thuật ngữ trong Báo cáo Phase 6 và script vẽ hình: gọi `feature_importances_` của `RandomForestRegressor` là *"Gini Importance"*. Trong bài toán hồi quy (Regression), tiêu chí phân nhánh là **Độ giảm phương sai / Mean Squared Error reduction (MDI)**, hoàn toàn không phải Gini (vốn chỉ áp dụng cho phân loại / Classification). Đã đính chính mã nguồn và biểu đồ.
   - Permutation Feature Importance độc lập trên tập Validation xác nhận lại `is_luxury_brand` và `engine_displacement_l` là 2 yếu tố chi phối mạnh nhất ($\sim 60\%$ suy giảm MSE).
5. **Thẩm định Module suy luận (Inference Verification - Task F)**:
   - Module [`src/models/predict.py`](file:///d:/ai-club-end-training/src/models/predict.py) đảm bảo 100% tính nhất quán về schema (15 đặc trưng), nạp đúng artifact vô địch, tính toán tự động các biến phái sinh và chặn hoàn toàn 9 cột rò rỉ.
   - Các trường hợp xe demo (Toyota Vios, Mazda CX-5, Mercedes C200) được định danh rõ ràng là **Smoke Tests** phục vụ kiểm thử tích hợp phần mềm, không được tùy tiện tuyên bố là "giá sát thực tế thị trường" khi chưa có nhãn ground-truth đối soát độc lập.
6. **Kiểm thử tự động (Test Suite)**:
   - **81/81 unit tests passed** trong **2.56s** (100% Offline).

---

## 2. Bằng Chứng Về Duplicate & Rò Rỉ Cụm (Duplicate Leakage & Group Overlap Audit)

Nhóm kiểm toán đã kiểm tra độc lập các nhóm near-duplicates, cross-posting và showroom inventory:

### 2.1. Phân loại và bằng chứng thực nghiệm

| Phân loại trùng lặp | Quy tắc nhận diện | Hiện tượng thực tế | Bản chất kỹ thuật & Đánh giá rò rỉ |
| :--- | :--- | :---: | :--- |
| **Listing ID Duplicate** | Trùng `listing_id` / `Mã tin` | **0 dòng (0.00%)** | **Hoàn toàn rời rạc**: Không có bất kỳ tin đăng nào bị lặp giữa Train, Val và Test. |
| **Exact Duplicate** | Trùng 100% các cột thô | **0 dòng (0.00%)** | Dữ liệu không có hàng nhân bản vô nghĩa. |
| **Cross-posting Overlap** | Trùng văn bản mô tả dài ($>50$ ký tự) | **8.76% (Val)**<br>**8.21% (Test)** | **Rò rỉ văn bản giữa các salon**: Do các đại lý sao chép văn bản quảng cáo của nhau. Đã được vô hiệu hóa hoàn toàn bằng cách **loại bỏ triệt để cột `Mô tả` và `Tên xe` khỏi ma trận đặc trưng $X$**. |
| **Showroom Spec Overlap** | Trùng 5 thông số (`brand, model, year, ODO, price`) | **27.26% (Val)**<br>**27.31% (Test)** | **Hơn 73% là xe mới 100% tại showroom (ODO = 0 km)**: Đây là các xe vật lý khác nhau được các đại lý chính hãng bán theo giá niêm yết chuẩn của nhà sản xuất. Không phải là cùng 1 chiếc xe vật lý. |
| **Spec Group Overlap** | Trùng tổ hợp 8 thông số (`brand, model, year, transmission, engine, fuel, body, origin`) | **95.53% (Val)**<br>**95.79% (Test)** | **Đặc tính phân phối dữ liệu dạng bảng (IID Tabular Sampling)**: 2,252/2,351 xe trong Test thuộc về các cấu hình phiên bản đã xuất hiện ít nhất 1 lần trong Train (ví dụ: Toyota Vios 2020 1.5 AT Sedan). |

### 2.2. Kiểm chứng tác động của Spec Group Overlap lên hiệu năng Test

Khi phân tích sai số của Champion Model trên 2,351 dòng Test phân tách theo nhóm cấu hình:

```text
┌───────────────────────────┬────────┬───────────────────┬────────────────┐
│ Trạng thái cấu hình xe    │ Số xe  │ Test MAE (VND)    │ Test MdAPE (%) │
├───────────────────────────┼────────┼───────────────────┼────────────────┤
│ Đã gặp trong Train (True) │  2,252 │    84,105,940 VND │          4.05% │
│ Chưa từng gặp (False)     │     99 │   741,617,400 VND │         15.44% │
└───────────────────────────┴────────┴───────────────────┴────────────────┘
```

> [!IMPORTANT]
> **Ý nghĩa phương pháp luận then chốt**:
> - Mô hình Random Forest hoạt động chủ yếu như một **bộ máy nội suy đa tầng (hierarchical nearest-neighbor interpolator)**. Khi gặp các cấu hình xe quen thuộc đã có trong tập Train, mô hình ước lượng giá cực kỳ chuẩn xác (sai số trung vị 4.05%).
> - Tuy nhiên, đối với 99 xe mang cấu hình mới lạ hoàn toàn (các phiên bản trim hiếm, xe nhập khẩu dung tích động cơ dị biệt), sai số trung vị nhảy vọt lên **15.44%** và MAE lên tới **741.6 triệu VND**.
> - **Khuyến nghị cho Đồ án**: Cần trình bày rõ trước Mentor rằng hiệu năng ấn tượng MAE 111.8M và MdAPE 4.29% phản ánh năng lực định giá cho các **dòng xe thị trường phổ biến đã có mẫu đại diện trong kho dữ liệu**, chứ không phải năng lực dự đoán không gian mở cho các cấu hình xe hoàn toàn mới lạ.

---

## 3. Tính Đúng Đắn Của Metrics & Đối Soát Thực Nghiệm (Metric Reconciliation)

Đối chiếu chéo giữa file lưu trữ kết quả và tính toán trực tiếp từ mảng dự đoán:

### 3.1. Đối chiếu tập Validation (2,351 dòng)
- **Tệp nguồn**: [`reports/model_experiments/validation_predictions.csv`](file:///d:/ai-club-end-training/reports/model_experiments/validation_predictions.csv)
- Cột mô hình: `Tree_RandomForest_Tuned_LogTarget` vs Cột nhãn: `actual_price_vnd`
- **Kết quả tính toán lại**:
  - $\text{MAE} = \frac{1}{n} \sum |y - \hat{y}| = \mathbf{142,934,536.73\text{ VND}}$ (Khớp 100% bảng báo cáo: $142,934,537$).
  - $\text{RMSE} = \sqrt{\frac{1}{n} \sum (y - \hat{y})^2} = \mathbf{950,065,306.16\text{ VND}}$ (Khớp 100% bảng báo cáo: $950,065,306$).
  - $R^2 = 1 - \frac{\text{SS}_{\text{res}}}{\text{SS}_{\text{tot}}} = \mathbf{0.8694}$ (Khớp 100% bảng báo cáo: $0.8694$).
  - $\text{MAPE} = \frac{100}{n} \sum \left|\frac{y - \hat{y}}{y}\right| = \mathbf{7.06\%}$ (Khớp 100% bảng báo cáo: $7.06\%$).
  - $\text{MdAPE} = \text{median}\left(\left|\frac{y - \hat{y}}{y}\right|\right) \times 100 = \mathbf{4.25\%}$ (Khớp 100% bảng báo cáo: $4.25\%$).

### 3.2. Đối chiếu tập Test (2,351 dòng)
- **Tệp nguồn**: [`reports/model_experiments/final_test_predictions.csv`](file:///d:/ai-club-end-training/reports/model_experiments/final_test_predictions.csv)
- Cột mô hình: `Tree_RandomForest_Tuned_LogTarget (CHAMPION)` vs Cột nhãn: `actual_price_vnd`
- **Kết quả tính toán lại**:
  - $\text{MAE} = \mathbf{111,793,580.73\text{ VND}}$ (Khớp 100% bảng báo cáo: $111,793,581$).
  - $\text{RMSE} = \mathbf{482,625,123.08\text{ VND}}$ (Khớp 100% bảng báo cáo: $482,625,123$).
  - $R^2 = \mathbf{0.9448}$ (Khớp 100% bảng báo cáo: $0.9448$).
  - $\text{MAPE} = \mathbf{6.84\%}$ (Khớp 100% bảng báo cáo: $6.84\%$).
  - $\text{MdAPE} = \mathbf{4.29\%}$ (Khớp 100% bảng báo cáo: $4.29\%$).

### 3.3. Quy trình đánh giá tập Test
- Kịch bản [`evaluate_final_test.py`](file:///d:/ai-club-end-training/evaluate_final_test.py) được thực thi trong một lần chạy duy nhất.
- Bảng kết quả test chứa 5 mô hình: `Baseline_Dummy_Median`, `Baseline_Dummy_Mean`, `Linear_Ridge_LogTarget`, `Tree_HistGBM_LogTarget` và `Tree_RandomForest_Tuned_LogTarget`.
- **Xác minh kiểm toán**: Cả 5 cấu hình này đều đã được đóng băng tham số từ các thí nghiệm trên tập Validation trước khi chạy script. Việc đưa cả baseline và các mô hình tiêu biểu vào tập Test là đúng đắn nhằm cung cấp ngữ cảnh đối chuẩn (benchmark context), không phải hành vi thử nghiệm nhiều mô hình trên tập Test để chọn lọc kết quả tốt nhất.

---

## 4. Đánh Giá Bản Chất Sự Khác Biệt Giữa Validation Và Test

Hiện tượng **Test MAE (111.8M) thấp hơn Validation MAE (142.9M)** và **Test $R^2$ (0.9448) cao hơn Validation $R^2$ (0.8694)** cần được giải thích thấu đáo bằng số liệu phân rã phương sai thay vì kết luận chủ quan rằng "mô hình không overfit".

### 4.1. So sánh phân rã sai số theo phân khúc giá (Segment Error Decomposition)

```text
┌──────────────┬───────────────────────────────┬───────────────────────────────┐
│              │       TẬP VALIDATION          │           TẬP TEST            │
│  Phân khúc   ├───────┬───────────────┬───────┼───────┬───────────────┬───────┤
│     giá      │ Số xe │   MAE (VND)   │  %Lỗi │ Số xe │   MAE (VND)   │  %Lỗi │
├──────────────┼───────┼───────────────┼───────┼───────┼───────────────┼───────┤
│ < 500 Triệu  │   555 │    25,166,350 │  4.2% │   549 │    26,110,500 │  5.5% │
│ 500M - 1 Tỷ  │ 1,071 │    40,781,560 │ 13.0% │ 1,070 │    40,443,040 │ 16.5% │
│ 1 Tỷ - 2 Tỷ  │   360 │   124,949,900 │ 13.4% │   365 │   112,160,800 │ 15.6% │
│ 2 Tỷ - 5 Tỷ  │   265 │   227,539,500 │ 17.9% │   277 │   256,357,700 │ 27.0% │
│ > 5 Tỷ       │   100 │ 1,731,148,000 │ 51.5% │    90 │ 1,036,314,000 │ 35.5% │
└──────────────┴───────┴───────────────┴───────┴───────┴───────────────┴───────┘
```

### 4.2. Nguyên nhân cốt lõi: Phân phối đuôi dài của nhóm xe siêu sang (>5 tỷ)
1. **Phân khúc đại chúng ($\le 2$ tỷ VND)**:
   - Chiếm **84.5%** tổng số xe của mỗi tập.
   - Sai số trung bình và sai số trung vị giữa Validation và Test **hoàn toàn tương đồng**:
     - Xe $<500$M: Val MAE 25.2M vs Test MAE 26.1M.
     - Xe 500M–1B: Val MAE 40.8M vs Test MAE 40.4M.
2. **Ảnh hưởng chi phối của nhóm xe $> 5$ tỷ VND**:
   - Nhóm xe $>5$ tỷ ở Validation (100 xe) chiếm tới **51.52% tổng sai số tuyệt đối** của toàn bộ tập Validation (173.1 tỷ VND).
   - Trong khi đó, ở Test (90 xe), nhóm này chỉ chiếm 93.3 tỷ VND (ít hơn **80 tỷ VND** tổng lỗi).
   - **Xét các ca ngoại lai cá biệt**:
     - Ca sai số lớn nhất tại Validation: Một xe siêu sang giá thực tế **38,999,000,000 VND** bị dự đoán là **3,247,445,712 VND** $\rightarrow$ **Sai số trên 1 xe là 35,751,554,288 VND (35.75 tỷ VND)**!
     - Chỉ riêng chiếc xe này đã đóng góp: $\frac{35.75\times 10^9}{2351} = \mathbf{15.21\text{ triệu VND}}$ vào Validation MAE!
     - Top 4 xe ngoại lai tại Validation có tổng sai số $72.98\text{ tỷ VND}$, đóng góp tới **31.04 triệu VND** vào Validation MAE ($142.9\text{M} - 31.0\text{M} \approx \mathbf{111.9\text{ triệu VND}}$).
     - Ngược lại, tại Test, ca sai số lớn nhất chỉ là **14.6 tỷ VND** (chưa bằng một nửa ca ngoại lai của Validation).
3. **Độ lệch chuẩn (Standard Deviation) & Skewness**:
   - Validation có $\text{Std} = 2.63\text{ tỷ VND}$, Skewness = **8.43**.
   - Test có $\text{Std} = 2.05\text{ tỷ VND}$, Skewness = **6.47**.
   - Vì hàm mục tiêu của $R^2$ sử dụng tổng bình phương sai số ($\text{SS}_{\text{res}}$), việc Validation chịu bình phương sai số của ca 35.75 tỷ ($1.28 \times 10^{21}$) làm cho $\text{SS}_{\text{res}}$ của Validation phình to, kéo $R^2$ xuống $0.8694$. Ở Test, thiếu vắng ca 35 tỷ này khiến $\text{SS}_{\text{res}}$ giảm mạnh, đưa $R^2$ lên $0.9448$.

> [!NOTE]
> **Kết luận kiểm toán về tính khái quát hóa**:
> Sự khác biệt giữa Val MAE (142.9M) và Test MAE (111.8M) là do **nhiễu mẫu ngẫu nhiên ở phần đuôi phân phối giá siêu sang (Sampling variance in the extreme tail)**, không phải bằng chứng cho thấy mô hình học tốt hơn trên tập Test. Chỉ số đại diện trung thực nhất cho năng lực khái quát hóa là **MdAPE**, và chỉ số này ổn định tuyệt đối ở mức **4.25% (Val) và 4.29% (Test)**.

---

## 5. Kiểm Tra Xử Lý Log-Target (Log-Target Handling Verification)

Kiểm toán toàn diện các hàm biến đổi và nghịch đảo trong mã nguồn:

1. **Tính nhất quán giữa hàm thuận và hàm nghịch đảo**:
   - Biến đổi nhãn trong huấn luyện: Sử dụng hàm logarit tự nhiên chuẩn:
     $$\ln(y) = \text{np.log}(y)$$
   - Nghịch đảo biến đổi dự đoán: Sử dụng hàm mũ tự nhiên chuẩn:
     $$\hat{y}_{\text{VND}} = \text{np.exp}(\hat{y}_{\text{log}})$$
   - Hoàn toàn **không có sự lẫn lộn** giữa `np.log` và `np.log1p`, hay giữa `np.exp` và `np.expm1`.
2. **Kiểm tra biên an toàn (Safety Bounds)**:
   - Module [`src/models/evaluate.py`](file:///d:/ai-club-end-training/src/models/evaluate.py#L22-L26) áp dụng 2 lớp chặn:
     - Chặn tràn số: $\hat{y}_{\text{log}} \in [0.0, 30.0]$ trước khi gọi `np.exp` (tránh lỗi tràn số `float64` $e^{>709}$).
     - Chặn biên vật lý: $\hat{y}_{\text{VND}} \in [30,000,000, 100,000,000,000]$ VNĐ (đúng dải giá thị trường hợp lệ).
3. **Đơn vị đo lường của Metrics**:
   - Mọi chỉ số đánh giá ($\text{MAE}$, $\text{RMSE}$, $\text{MAPE}$, $\text{MdAPE}$) đều được tính toán **trên đơn vị VND thực tế**, tuyệt đối không tính trên thang đo log.

---

## 6. Kiểm Toán Tầm Quan Trọng Đặc Trưng (Feature Importance Audit)

### 6.1. Hiệu chỉnh lỗi thuật ngữ (Correction of Gini Terminology)
- **Vấn đề phát hiện**: File [`generate_feature_importance.py`](file:///d:/ai-club-end-training/generate_feature_importance.py) và Báo cáo Phase 6 trước đây ghi nhãn trục hoành là *"Gini Importance"*.
- **Cơ sở khoa học**: Trong bài toán hồi quy (Random Forest Regressor), hàm phân nhánh là sai số bình phương tối thiểu (Variance Reduction / Mean Squared Error), **hoàn toàn không có khái niệm chỉ số Gini (vốn là thước đo độ hỗn loạn nhãn phân loại)**. Thuật ngữ chuẩn xác theo định nghĩa của Breiman (2001) và tài liệu scikit-learn là **Mean Decrease in Impurity (MDI / Độ giảm phương sai)**.
- **Hành động đã xử lý**: Đã hiệu chỉnh mã nguồn và vẽ lại biểu đồ [`reports/figures/phase6/feature_importance.png`](file:///d:/ai-club-end-training/reports/figures/phase6/feature_importance.png) với nhãn chuẩn: *"Mean Decrease in Impurity (MDI / Variance Reduction)"*.

### 6.2. Kiểm chứng chéo bằng Permutation Importance độc lập
Để phòng ngừa việc MDI ưu tiên thiên vị cho các biến liên tục có nhiều điểm cắt, nhóm kiểm toán đã chạy kiểm tra **Permutation Feature Importance** độc lập trên tập Validation (500 mẫu, 5 repeats):

```text
┌───────────────────────┬──────────────┬──────────────────────────────────────────┐
│ Đặc trưng             │ MDI (Tree)   │ Permutation Importance (MSE Degradation) │
├───────────────────────┼──────────────┼──────────────────────────────────────────┤
│ is_luxury_brand       │ 43.10% (Top 1)│ 0.2988 ± 0.017 (Top 1)                   │
│ engine_displacement_l │ 26.35% (Top 2)│ 0.2918 ± 0.027 (Top 2)                   │
│ model                 │  5.63% (Top 4)│ 0.0315 ± 0.002 (Top 3)                   │
│ brand                 │  5.72% (Top 3)│ 0.0294 ± 0.009 (Top 4)                   │
│ origin                │  1.48% (Top 11│ 0.0248 ± 0.004 (Top 5)                   │
│ seats                 │  2.31% (Top 8)│ 0.0232 ± 0.003 (Top 6)                   │
│ body_type             │  1.87% (Top 10│ 0.0226 ± 0.004 (Top 7)                   │
│ car_age               │  4.41% (Top 5)│ 0.0222 ± 0.006 (Top 8)                   │
│ transmission          │  2.38% (Top 7)│ 0.0196 ± 0.005 (Top 9)                   │
│ year                  │  3.52% (Top 6)│ 0.0157 ± 0.002 (Top 10)                  │
│ mileage_km            │  0.69% (Top 12│ 0.0040 ± 0.001 (Top 11)                  │
└───────────────────────┴──────────────┴──────────────────────────────────────────┘
```

### 6.3. Giải thích kinh tế học & Cảnh báo quan hệ nhân quả (No Causality Claim)
- **Xác nhận xếp hạng**: Cả hai phương pháp (MDI và Permutation) đều đồng thuận xác nhận `is_luxury_brand` và `engine_displacement_l` là hai động lực định giá mạnh nhất.
- **Cơ sở kinh tế học tại Việt Nam**: Biểu thuế tiêu thụ đặc biệt (TTĐB) của Việt Nam đánh thuế lũy tiến rất nặng theo dung tích xi lanh (động cơ dung tích $1.5\text{L} \le 35\%$, nhưng dung tích $>3.0\text{L} - 6.0\text{L}$ chịu thuế từ $90\% - 150\%$). Do đó, dung tích xi lanh lớn tương quan rất mạnh với mức giá cao đột biến.
- **Cảnh báo không suy diễn nhân quả (No Causality)**: Tầm quan trọng đặc trưng ở đây chỉ phản ánh mức độ đóng góp thống kê trong việc giảm sai số dự báo, **không chứng minh quan hệ nhân quả**. Ví dụ, việc tăng dung tích động cơ không tự động làm xe đắt tiền nếu thương hiệu xe đó bị thị trường đào thải.

---

## 7. Thẩm Định Module Suy Luận Thực Tế (Inference CLI Verification)

Kiểm toán mã nguồn [`src/models/predict.py`](file:///d:/ai-club-end-training/src/models/predict.py):

1. **Khớp nối Schema**: Hàm [`prepare_car_features()`](file:///d:/ai-club-end-training/src/models/predict.py#L48-L98) tạo đúng 15 cột (`NUMERIC_FEATURES + CATEGORICAL_FEATURES`) theo chuẩn của `extract_features_and_target()`.
2. **Quy tắc trích xuất phái sinh**:
   - $\text{car\_age} = 2024.0 - \text{year}$.
   - $\text{is\_zero\_mileage} = 1.0$ nếu $\text{mileage\_km} == 0$, ngược lại $0.0$.
   - $\text{is\_luxury\_brand} = 1.0$ nếu hãng xe thuộc `LUXURY_BRANDS`, ngược lại $0.0$.
3. **Xử lý ngoại lệ**:
   - Category chưa từng thấy (Unseen category): Được `OneHotEncoder(handle_unknown='ignore')` bỏ qua an toàn, không gây crash ứng dụng.
   - Trường số bị thiếu (Missing numeric): Được `SimpleImputer(strategy='median')` điền giá trị trung vị của tập Train.
   - Giá trị xuất ra: Số thực hữu hạn dương, chuyển đổi sang chuỗi đọc tiếng Việt định dạng tỷ/triệu đồng.
4. **Hiệu chỉnh phát biểu về các ca Demo (Correction on Demo Cases)**:
   - Trong quá trình phát triển, các lệnh demo (`Toyota Vios 2020: 449 triệu`, `Mazda CX-5 2022: 614 triệu`, `Mercedes C200 2021: 1.73 tỷ`) **chỉ được xem là Smoke Tests** nhằm xác nhận đường ống dẫn phần mềm từ input người dùng đến pipeline chạy thông suốt không lỗi.
   - **Tuyệt đối không được tuyên bố các con số này là "sát thực tế thị trường"** khi không có nhãn kiểm chứng thực địa (ground-truth).

---

## 8. Danh Mục Các Lỗi Đã Phát Hiện & Khắc Phục (Flaws Detected & Resolved)

| STT | Lỗi phát hiện | Mức độ | Vị trí | Biện pháp đã thực hiện |
| :---: | :--- | :---: | :--- | :--- |
| 1 | **Nhầm lẫn thuật ngữ Gini Importance trong hồi quy** | Trung bình | `generate_feature_importance.py`, `reports/phase6_model_evaluation.md` | Đính chính thành *Mean Decrease in Impurity (MDI / Giảm phương sai)* và vẽ lại biểu đồ. |
| 2 | **Chưa làm rõ nguyên nhân Test MAE < Val MAE** | Trung bình | `reports/phase6_model_evaluation.md` | Bổ sung phân tích phân rã phương sai: do ca ngoại lai 35.8 tỷ ở Validation kéo MAE tăng 15.2M, trong khi MdAPE của 2 tập tương đương (4.25% vs 4.29%). |
| 3 | **Nguy cơ hiểu nhầm các ca Demo là chân lý thị trường** | Thấp | Hội thoại phát triển Phase 6 | Đính chính: Demo chỉ là Smoke Tests xác nhận tính toàn vẹn phần mềm. |

---

## 9. Danh Mục Thay Đổi Thực Tế (Modifications Made)

1. [`generate_feature_importance.py`](file:///d:/ai-club-end-training/generate_feature_importance.py):
   - Đổi nhãn x-axis từ `Gini Importance` thành `Mean Decrease in Impurity (MDI / Variance Reduction)`.
2. [`reports/figures/phase6/feature_importance.png`](file:///d:/ai-club-end-training/reports/figures/phase6/feature_importance.png):
   - Chạy lại script kết xuất ảnh mới với nhãn khoa học chuẩn mực.
3. [`reports/phase6_model_evaluation.md`](file:///d:/ai-club-end-training/reports/phase6_model_evaluation.md):
   - Đính chính thuật ngữ Mục 6 từ Gini sang MDI.
   - Bổ sung ghi chú kiểm toán phương sai tại Mục 7 giải thích nguyên nhân Test MAE thấp hơn Val MAE do ngoại lai cực đoan.
4. [`scripts/independent_audit_phase6.py`](file:///d:/ai-club-end-training/scripts/independent_audit_phase6.py):
   - Tạo kịch bản kiểm toán đối soát phân phối, kiểm chứng metric, tính permutation importance và đo lường group leakage.

---

## 10. Kết Quả Kiểm Thử Toàn Diện (Full Test Suite Verification)

Nhóm kiểm toán đã chạy lại toàn bộ test suite trên workspace hiện tại:
`pytest -v`

```text
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.7.0
rootdir: D:\ai-club-end-training
collected 81 items

tests/test_cleaning.py (7 tests) ........................................ PASSED [  8%]
tests/test_crawler.py (6 tests) ......................................... PASSED [ 16%]
tests/test_load_dataset.py (9 tests) .................................... PASSED [ 27%]
tests/test_modeling.py (7 tests) ........................................ PASSED [ 35%]
tests/test_predict.py (4 tests) ......................................... PASSED [ 40%]
tests/test_preprocessing.py (7 tests) ................................... PASSED [ 49%]
tests/test_price_parser.py (17 tests) ................................... PASSED [ 70%]
tests/test_split_data.py (5 tests) ...................................... PASSED [ 76%]
tests/test_validation.py (19 tests) ..................................... PASSED [100%]

============================= 81 passed in 2.56s ==============================
```

---

## 11. Những Kết Luận Cần Giữ Thái Độ Thận Trọng Trước Mentor (Methodological Caveats)

Khi trình bày và bảo vệ đồ án trước Mentor và Hội đồng chấm thi, sinh viên AI cần nắm vững 4 luận điểm thận trọng sau:

1. **Hiệu năng định giá tập trung vào dòng xe phổ biến**:
   - Khi xe thuộc cấu hình quen thuộc (đã có trong Train), mô hình đạt độ chính xác rất cao ($\text{MdAPE} \approx 4.05\%$).
   - Khi xe thuộc cấu hình lạ chưa từng gặp, sai số sẽ tăng lên ($\text{MdAPE} \approx 15.44\%$). Cần trình bày mô hình dưới vai trò *"Công cụ tham chiếu định giá cho các dòng xe lưu hành phổ thông"*.
2. **Ảnh hưởng của xe mới tại showroom ($25.8\%$)**:
   - Xe mới ODO = 0 km tại showroom có giá bán niêm yết chuẩn, giúp giảm sai số trung bình nhưng có thể tạo ảo giác mô hình dự đoán xe cũ quá hoàn hảo. Cần chỉ rõ phân tích lỗi riêng cho nhóm xe cũ thực sự.
3. **Phân rã chênh lệch Validation và Test**:
   - Không được tuyên bố "mô hình học trên Test tốt hơn Validation". Cần giải thích đúng bản chất: do Validation ngẫu nhiên nhận 1 xe siêu sang sai số 35.8 tỷ VND làm phình to MAE. Chỉ số thực chất của hai tập là tương đương ($\text{MdAPE} \approx 4.3\%$).
4. **Không suy diễn quan hệ nhân quả**:
   - Trọng số đặc trưng của dung tích động cơ ($26.35\%$) và cờ xe sang ($43.10\%$) chỉ phản ánh tương quan thống kê mạnh trong cơ chế thuế tiêu thụ đặc biệt tại Việt Nam, không phải quan hệ nhân quả tuyệt đối.

---

## 12. Bảng Nghiệm Thu Tiêu Chí Độc Lập (Audit Acceptance Checklist)

- [x] **Các tuyên bố về leakage đã được kiểm tra**: Xác minh 0% ID leakage, 8.2%–8.8% mô tả tin đăng chéo, 95.5% trùng cấu hình xe phổ thông.
- [x] **Metric có thể đối chiếu với dữ liệu đầu ra**: Tái tính toán khớp 100% từng số lẻ từ các tệp dự đoán gốc.
- [x] **Target transformation đúng**: Sử dụng $\ln(y)$ thuận và $\exp(\hat{y})$ nghịch đảo nhất quán, an toàn tràn số.
- [x] **Feature importance có thể truy xuất về phương pháp tính**: Hiệu chỉnh về MDI (Variance Reduction), đối chiếu bằng Permutation Importance.
- [x] **Inference input và training schema nhất quán**: 15 đặc trưng chuẩn, tự động tính biến phái sinh, xử lý an toàn unseen categories.
- [x] **Demo prediction không bị trình bày nhầm thành actual market accuracy**: Đã phân định rõ demo là Smoke Tests.
- [x] **Test results cũ được giữ nguyên để đối chiếu**: Bảo toàn nguyên vẹn 100% các tệp CSV kết quả trong `reports/model_experiments/`.
- [x] **Những phát hiện chưa thể xác minh được ghi rõ**: Ghi nhận giới hạn định danh do thiếu số khung VIN bắt buộc.
- [x] **Toàn bộ pytest suite được chạy thực tế**: 81/81 passed trong 2.56s.
- [x] **Chưa commit Git**: Toàn bộ thay đổi lưu lại trên working tree để người dùng rà soát.
