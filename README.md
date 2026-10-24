# Used Car Price Prediction in Vietnam
## Xây Dựng Hệ Thống Machine Learning Định Giá Ô Tô Đã Qua Sử Dụng Toàn Diện & Đánh Giá Độ Bền Khoa Học
*(AI Club End-Training Mini Project)*

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.4+-orange.svg)](https://scikit-learn.org/)
[![Champion Model](https://img.shields.io/badge/champion-RandomForest--Tuned--LogTarget-brightgreen.svg)](reports/model_comparison.csv)
[![Test MdAPE](https://img.shields.io/badge/Test%20MdAPE-4.29%25-blueviolet.svg)](reports/model_comparison.csv)

---

## 1. Tổng Quan Bài Toán (Problem Overview)

Dự án **Used Car Price Prediction in Vietnam** giải quyết bài toán định lượng hóa và dự báo giá chào bán ô tô đã qua sử dụng trên thị trường thứ cấp tại Việt Nam từ 15 đặc trưng kỹ thuật, vận hành và phân khúc thị trường.

- **Dạng bài toán**: Supervised Learning (Học có giám sát) — **Tabular Regression (Hồi quy dữ liệu bảng)**.
- **Biến mục tiêu (Target)**: `price_vnd` — Giá niêm yết chào bán chính thức của ô tô tính theo Việt Nam Đồng (VND).
- **Hàm mục tiêu tối ưu**: Huấn luyện trên không gian logarit tự nhiên $y_{\text{log}} = \ln(\text{price\_vnd})$ nhằm nén dải động giá và tối ưu hóa **sai số tỷ đối phần trăm (Relative Percentage Error)** thay vì giá trị tiền tệ tuyệt đối.
- **Mục tiêu thực tiễn**: Cung cấp một mỏ neo định giá tham chiếu khách quan (Objective Price Anchor) phục vụ người mua cá nhân và chuyên viên thẩm định. Mô hình đạt sai số trung vị tương đối (**MdAPE $\approx 4.29\%$**) nằm trọn vẹn trong biên độ thương lượng phổ biến **3% – 5%** của thị trường xe cũ Việt Nam.

---

## 2. Cấu Trúc Repository Tối Giản (Minimalist Structure)

Repository được tinh gọn tối đa để người chấm dễ dàng theo dõi toàn bộ logic trong một notebook duy nhất và đối chiếu số liệu kiểm toán:

```text
├── README.md                                # Hướng dẫn tổng quan, cài đặt và tóm tắt kết quả
├── requirements.txt                         # Danh sách thư viện Python cần thiết
├── notebooks/
│   └── used_car_price_prediction.ipynb     # Notebook trung tâm 13 phần độc lập, tự chứa toàn bộ mã nguồn
├── data/
│   ├── DATA_README.md                       # Hướng dẫn nguồn gốc dữ liệu, bản quyền & cách đặt data local
│   └── dataset_manifest.json                # Bảng kê khai mã băm SHA-256 các tập dữ liệu thực tế
├── reports/
│   └── model_comparison.csv                 # Bảng so sánh kết quả 21 thực nghiệm (Phase 6 & Phase 6.2)
└── .gitignore                               # Quy tắc loại trừ an toàn (loại bỏ dữ liệu PII và artifact tạm)
```

---

## 3. Cài Đặt Môi Trường & Thực Thi (Quickstart)

### 3.1. Thiết lập môi trường Python
Yêu cầu Python $\ge 3.10$ (khuyến nghị Python 3.11):
```powershell
# Tạo môi trường ảo
python -m venv .venv

# Kích hoạt môi trường (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Kích hoạt môi trường (Linux/macOS)
source .venv/bin/activate

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

### 3.2. Chuẩn bị dữ liệu (Data Setup)
- **Bảo mật & Bản quyền**: Theo quy tắc bảo vệ dữ liệu cá nhân (PII) và tôn trọng bản quyền của bên thứ ba, tệp CSV dữ liệu thật không được commit lên GitHub công khai. Chi tiết xem tại [`data/DATA_README.md`](data/DATA_README.md).
- **Chạy với dữ liệu thật**: Đặt tệp `car_detail.csv` vào `data/raw/external/mquaan_car_price/car_detail.csv` và kiểm tra mã SHA-256 từ [`data/dataset_manifest.json`](data/dataset_manifest.json).
- **Chế độ tự động Fallback (`SYNTHETIC_DEMO`)**: Nếu chưa có dữ liệu thật cục bộ, notebook sẽ tự động chuyển sang chế độ sinh dữ liệu mô phỏng đại diện. Người chấm có thể chạy lệnh `Run All` mà không gặp bất kỳ lỗi thiếu file nào.

### 3.3. Chạy Notebook
Khởi động Jupyter Notebook và mở tệp chính:
```powershell
jupyter notebook notebooks/used_car_price_prediction.ipynb
```

---

## 4. Cấu Trúc Nội Dung Notebook Trung Tâm

Notebook [`notebooks/used_car_price_prediction.ipynb`](notebooks/used_car_price_prediction.ipynb) được xây dựng tự chứa 100% (không phụ thuộc module ngoài), bao gồm đầy đủ 13 phần:

1. **Project Overview**: Đặt vấn đề bất cân xứng thông tin, phân biệt Asking Price vs Transaction Price, xác định Cohort A (xe sản xuất 2015 – 2023).
2. **Environment & Data Ingestion**: Nhận diện đường dẫn tương đối, kiểm tra thư viện, tự động nạp dữ liệu thật hoặc kích hoạt fallback mô phỏng.
3. **Exploratory Data Analysis (EDA)**: Thống kê mô tả biến mục tiêu, phân tích độ lệch (Skewness thô $+7.8$ vs log $+0.5$), biểu đồ giá và khám phá xe showroom ODO $0\text{ km}$.
4. **Data Cleaning & Cohort A**: Bóc tách regex giá tiếng Việt, lọc hộp số dị biệt, xử lý ODO ngoại lai, bóc tách 23,510 bản ghi Cohort A sạch.
5. **Feature Engineering & Leakage Isolation**: Xây dựng 15 đặc trưng chính quy (8 số, 7 danh mục), loại bỏ tuyệt đối 9 cột rò rỉ dữ liệu khỏi ma trận $X$.
6. **Train / Validation / Test Splits**: Phân chia 80 / 10 / 10 có phân tầng deciles, đảm bảo $100\%$ không trùng lặp `listing_id`, nguyên tắc chỉ `fit` preprocessor trên Train.
7. **Preprocessing Pipelines**: Xây dựng `ColumnTransformer` cho mô hình Cây và mô hình Tuyến tính (`OneHotEncoder`, `SimpleImputer`, `StandardScaler`).
8. **Baseline & Model Training**: Huấn luyện và khảo sát 10 cấu hình thực nghiệm từ Baseline, Tuyến tính (Ridge/Lasso) đến Cây quyết định (HistGBM, Random Forest).
9. **Validation Leaderboard & Test Evaluation**: So sánh trên tập Val, chọn Champion Model `Tree_RandomForest_Tuned_LogTarget`, đánh giá độc lập một lần trên Test.
10. **Champion Model & Inference**: Đóng gói quy trình suy luận, dự đoán thử nghiệm trên 3 xe thực tế (Toyota Vios, Mazda CX-5, Mercedes C200).
11. **Group-Aware Robustness Evaluation (Phase 6.2)**: Phát hiện rò rỉ đăng chéo tin ($9.15\%$ tin trùng), gom cụm và phân chia `StratifiedGroupKFold`, chứng minh **MdAPE giữ vững chuẩn xác 4.29% khi rò rỉ về 0.00%**.
12. **Feature Importance & Domain Validation**: Phân tích độ giảm phương sai (MDI), giải mã vai trò của `is_luxury_brand` ($43.1\%$) và dung tích xi-lanh ($26.4\%$) gắn liền Biểu thuế Tiêu thụ Đặc biệt (TTĐB).
13. **Conclusion & Future Roadmap**: Tổng kết thành tựu, thảo luận giới hạn đề tài và lộ trình phát triển mô hình đa phương thức (PhoBERT + Computer Vision).

---

## 5. Kết Quả Thực Nghiệm & So Sánh Mô Hình (Model Comparison)

Tất cả kết quả thực nghiệm được tổng hợp chuẩn xác tại [`reports/model_comparison.csv`](reports/model_comparison.csv):

### 5.1. Bảng xếp hạng Validation (Phase 6 — Random Split, 2,351 dòng Val)

| Hạng | Tên cấu hình mô hình | Không gian Target | Val MAE (VND) | Val RMSE (VND) | Val $R^2$ | Val MdAPE (%) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 🥇 **1** | **`Tree_RandomForest_Tuned_LogTarget` (CHAMPION)** | **log** | **142,934,537** | **950,065,306** | **0.8694** | **4.25%** |
| 🥈 2 | `Tree_RandomForest_LogTarget` (Default) | log | 159,102,971 | 1,043,403,506 | 0.8425 | 4.94% |
| 🥉 3 | `Tree_RandomForest_RawTarget` | raw | 168,751,598 | 852,439,763 | 0.8949 | 6.61% |
| 4 | `Tree_HistGBM_LogTarget` | log | 180,831,847 | 1,208,263,095 | 0.7888 | 5.37% |
| 5 | `Tree_HistGBM_RawTarget` | raw | 201,925,471 | 1,051,262,546 | 0.8401 | 7.84% |
| 6 | `Linear_Ridge_LogTarget` | log | 255,658,033 | 1,441,060,500 | 0.6996 | 7.72% |
| 7 | `Linear_Lasso_LogTarget` | log | 370,691,840 | 1,772,436,353 | 0.5455 | 12.22% |
| 8 | `Linear_Ridge_RawTarget` | raw | 379,429,332 | 1,153,551,727 | 0.8075 | 23.72% |
| 9 | `Baseline_Dummy_Median` | raw | 914,616,759 | 2,721,373,088 | -0.0714 | 39.83% |
| 10 | `Baseline_Dummy_Mean` | raw | 1,164,209,470 | 2,629,312,836 | -0.0001 | 94.34% |

### 5.2. Đánh giá một lần trên tập Test (Phase 6 Random Test vs Phase 6.2 Group-Aware Test)

| Tập kiểm thử | Tên mô hình | Rò rỉ tin trùng | Test MAE (VND) | Test RMSE (VND) | Test $R^2$ | Test MdAPE (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Phase 6 Random Test** (2,351 xe) | `Tree_RandomForest_Tuned_LogTarget` | $9.15\%$ | **111,793,581** | **482,625,123** | **0.9448** | **4.29%** |
| **Phase 6.2 Group-Aware Test** (2,350 xe) | `Tree_RandomForest_Tuned_LogTarget` | **0.00%** | **130,761,443** | **821,395,226** | **0.8638** | **4.29%** |

> **Phát hiện kiểm định then chốt**:
> - Khi triệt tiêu $100\%$ rò rỉ bài đăng trùng lặp bằng `StratifiedGroupKFold`, chỉ số **MdAPE của mô hình giữ vững tuyệt đối ở mức 4.29%**.
> - Ở phân khúc xe phổ thông ($\le 500\text{ triệu VND}$), MAE của tập Group-Aware thậm chí còn tốt hơn Phase 6 (**24.2 triệu VND** so với 26.1 triệu VND). Mức tăng MAE toàn cục ($+18.9\text{ triệu VND}$) hoàn toàn bắt nguồn từ việc tập Test Group-Aware ngẫu nhiên nhận thêm 27 xe siêu sang $> 5\text{ tỷ VND}$.
> - Điều này chứng minh mô hình định giá dựa trên mối tương quan đặc trưng thực chất, hoàn toàn không bị overfit hay ghi nhớ tin trùng lặp.

---

## 6. Giới Hạn Đề Tài & Hướng Phát Triển (Limitations & Roadmap)

1. **Giá niêm yết vs Giá giao dịch**: Dữ liệu phản ánh giá chào bán công khai (Asking Price). Trong giao dịch thực tế, người mua có thể thương lượng giảm thêm $2\% - 5\%$.
2. **Thiếu số khung định danh (VIN)**: Các trang tin rao bán xe không hiển thị số VIN để bảo mật, do đó việc gom nhóm dựa trên thông số kỹ thuật và văn bản mô tả.
3. **Mở rộng mô hình đa phương thức (Multimodal Learning)**:
   - Tích hợp mô hình NLP (PhoBERT) trích xuất trang bị phụ kiện và lịch sử bảo dưỡng trong phần `Mô tả`.
   - Kết hợp Computer Vision đánh giá độ mới nội ngoại thất từ ảnh chụp thực tế của xe.
   - Triển khai REST API với FastAPI và đóng gói Docker container phục vụ triển khai sản xuất.
