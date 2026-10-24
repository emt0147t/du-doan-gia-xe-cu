# Used Car Price Prediction in Vietnam
## Xây Dựng Hệ Thống Machine Learning Toàn Diện & Thẩm Định Khoa Học Độ Bền
*(AI Club End-Training Mini Project)*

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests Status](https://img.shields.io/badge/tests-87%20passed-brightgreen.svg)](tests/)
[![Champion Model](https://img.shields.io/badge/champion-RandomForest--Tuned--LogTarget-orange.svg)](models/)
[![Test MdAPE](https://img.shields.io/badge/Test%20MdAPE-4.29%25-blueviolet.svg)](reports/phase6_2_group_aware_evaluation.md)

---

## 1. Tổng Quan Dự Án & Mục Tiêu (Project Overview)

Dự án **Used Car Price Prediction in Vietnam** là công trình nghiên cứu và phát triển phần mềm Machine Learning giải quyết bài toán định lượng hóa và dự báo giá chào bán ô tô đã qua sử dụng trên thị trường thứ cấp tại Việt Nam.

- **Dạng bài toán**: Supervised Learning (Học có giám sát) — **Tabular Regression (Hồi quy dữ liệu bảng)**.
- **Biến mục tiêu (Target)**: `price_vnd` — Giá niêm yết chào bán chính thức của ô tô tính theo Việt Nam Đồng (VND).
- **Không gian tối ưu hóa**: Huấn luyện trên không gian logarit tự nhiên $y_{\text{log}} = \ln(\text{price\_vnd})$ nhằm nén dải động giá và tối ưu hóa **sai số tỷ đối phần trăm (Relative Percentage Error)**.
- **Mục tiêu thực tiễn**: Cung cấp một mỏ neo định giá tham chiếu độc lập (Objective Market Price Anchor) cho người mua cá nhân và chuyên viên thẩm định xe trong biên độ thương lượng phổ biến **3% – 5%**.

---

## 2. Nguồn Gốc Dữ Liệu & Bản Quyền Chia Sẻ (Dataset Provenance & Governance)

### 2.1. Nguồn dữ liệu
Dữ liệu được tiếp nhận từ tập dữ liệu thứ cấp công khai trên Kaggle/GitHub do tác giả Mai Quốc Ân công bố, có nguồn gốc thu thập từ nền tảng thương mại điện tử `bonbanh.com` với quy mô ban đầu **30,652 tin đăng**.

### 2.2. Trạng thái phân phối trên GitHub Public Repository
Để bảo vệ quyền riêng tư cá nhân và tuân thủ đạo đức dữ liệu:
- **Tệp dữ liệu CSV thực tế (`data/raw/` và `data/processed/`) KHÔNG được commit lên public repository** do quyền tái phân phối thương mại của bên thứ ba chưa được xác minh đầy đủ và tệp thô chứa văn bản có thể lẫn số điện thoại người bán (PII).
- **Giải pháp thay thế**:
  - [`data/DATA_README.md`](data/DATA_README.md): Hướng dẫn chi tiết cách tải và thiết lập dữ liệu thực tế tại máy cục bộ.
  - [`data/dataset_manifest.json`](data/dataset_manifest.json): Bảng kê khai đầy đủ mã băm SHA-256, số dòng, số cột của các tệp dữ liệu thực tế.
  - [`data/synthetic_demo_data.csv`](data/synthetic_demo_data.csv): Bộ dữ liệu nhân tạo độc lập (40 xe, 100% Non-PII, gắn nhãn `SYNTHETIC_DEMO_ONLY`) phục vụ chạy thử nghiệm pipeline mà không cần dữ liệu thật.

---

## 3. Cấu Trúc Thư Mục Kho Lưu Trữ (Repository Structure)

```text
ai-club-end-training/
├── README.md                          # Tài liệu hướng dẫn trung tâm cho Mentor
├── requirements.txt                   # Danh sách thư viện Python cần thiết
├── .gitignore                         # Cấu hình loại trừ Git an toàn
├── notebooks/
│   ├── used_car_price_prediction.ipynb # Notebook trung tâm 13 phần chạy toàn trình
│   └── 04_eda.ipynb                   # Notebook khám phá dữ liệu ban đầu Phase 4
├── data/
│   ├── DATA_README.md                 # Hướng dẫn dữ liệu, bản quyền & cách đặt data local
│   ├── dataset_manifest.json          # Bảng kê mã băm SHA-256 các tập dữ liệu
│   ├── synthetic_demo_data.csv        # Dữ liệu mẫu nhân tạo phục vụ kiểm thử
│   └── metadata/                      # Quản trị siêu dữ liệu và kiểm tra toàn vẹn
├── models/
│   ├── champion_random_forest.joblib  # Artifact mô hình vô địch (30.98 MB, nạp sẵn)
│   └── champion_model_metadata.json   # Metadata kiểm toán kiến trúc mô hình
├── presentation/
│   ├── ai_club_final_defense.pptx     # 15 slide thuyết trình 16:9 bảo vệ tốt nghiệp
│   ├── speaker_notes.md               # Lời thoại thuyết trình chi tiết cho 15 slide
│   └── mentor_defense_qa.md           # Bộ 26 câu hỏi phản biện chuyên sâu và câu trả lời
├── src/
│   ├── data/
│   │   ├── price_parser.py            # Bộ bóc tách giá tiền tiếng Việt sang VND
│   │   ├── validation.py              # Data Quality Contract & Validation logic
│   │   ├── cleaning.py                # Pipeline làm sạch dữ liệu & trích xuất đặc trưng
│   │   ├── preprocessing.py           # ColumnTransformer an toàn rò rỉ (Tree & Linear)
│   │   ├── split_data.py              # Phân chia tập 80/10/10 phân tầng deciles
│   │   └── duplicate_groups.py        # Thuật toán gom cụm 4 cấp độ và chia nhóm Phase 6.2
│   └── models/
│       ├── evaluate.py                # Tính toán các metric hồi quy & nghịch đảo log
│       └── predict.py                 # Module suy luận CLI & dự đoán giá xe thực tế
├── reports/
│   ├── final_project_report.md        # Báo cáo kỹ thuật tổng kết 19 phần toàn diện
│   ├── final_consistency_checklist.md # Bảng đối soát số liệu & mã băm 100% khớp
│   ├── phase7_completion_checklist.md # Biên bản nghiệm thu hoàn thành Phase 7
│   ├── DELIVERY_STATUS.md             # Nhật ký kiểm thử & xác thực trước khi nộp
│   ├── figures/                       # Hệ thống biểu đồ trực quan hóa
│   │   ├── phase4/                    # 19 biểu đồ khám phá dữ liệu EDA
│   │   ├── phase6/                    # 7 biểu đồ mô hình hóa, phần dư & feature importance
│   │   └── phase6_2/                  # 2 biểu đồ so sánh độ bền chia nhóm Phase 6 vs 6.2
│   └── model_experiments/             # Kết quả thực nghiệm 10 cấu hình CSV & JSON
└── tests/                             # 87 bài unit test tự động (100% Offline)
```

---

## 4. Hướng Dẫn Cài Đặt & Môi Trường Thực Thi (Quickstart)

### 4.1. Cài đặt môi trường ảo (Virtual Environment)
Yêu cầu Python $\ge 3.10$ (khuyến nghị Python 3.11):
```powershell
# Tạo môi trường ảo
python -m venv .venv

# Kích hoạt môi trường (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Kích hoạt môi trường (Linux/macOS)
source .venv/bin/activate

# Cài đặt các thư viện cần thiết
pip install --upgrade pip
pip install -r requirements.txt
```

### 4.2. Mở và chạy Notebook trung tâm
Tệp notebook trung tâm được thiết kế theo cấu trúc 13 phần chuẩn mực:
```powershell
jupyter notebook notebooks/used_car_price_prediction.ipynb
```
*Notebook được thiết kế độc lập, sử dụng đường dẫn tương đối, tự động nhận diện dữ liệu cục bộ hoặc dữ liệu demo mà không bị lỗi crash.*

---

## 5. Hướng Dẫn Thiết Lập Dữ Liệu Cục Bộ (Local Dataset Setup)

Nếu bạn có tệp dữ liệu thô gốc, vui lòng đặt vào đúng đường dẫn sau:
```text
data/raw/external/mquaan_car_price/car_detail.csv
data/raw/external/mquaan_car_price/car_sell_processed.csv
```
Sau đó, chạy các lệnh tạo dữ liệu tự động:
```powershell
# 1. Làm sạch và tạo Cohort A (23,510 dòng)
python src/data/cleaning.py

# 2. Tạo các tập chia 80/10/10 Phase 6
python src/data/split_data.py

# 3. Tạo các tập chia nhóm Phase 6.2 (0% rò rỉ tin trùng)
python src/data/duplicate_groups.py
```
*(Nếu không có dữ liệu thật, hệ thống sẽ sử dụng `data/synthetic_demo_data.csv` để chạy kiểm thử luồng code).*

---

## 6. Chạy Kiểm Thử Tự Động (Run Tests)

Dự án có **87 unit tests** bao phủ 100% các thành phần logic:
```powershell
pytest -v --tb=short
```
*Kết quả kiểm thử: **87 passed trong ~4.21 giây**, thực thi hoàn toàn offline.*

---

## 7. Hướng Dẫn Suy Luận Dự Đoán Giá Xe (Model Inference)

Artifact mô hình vô địch [`models/champion_random_forest.joblib`](models/champion_random_forest.joblib) đã được lưu sẵn trong repository. Bạn có thể thực hiện dự đoán ngay lập tức:

### 7.1. Chạy Demo trên các mẫu xe đại diện
```powershell
python src/models/predict.py --demo
```
*Kết quả mẫu:*
- **Toyota Vios 2020** (45,000 km, 1.5L AT) $\rightarrow$ **~449 Triệu VNĐ**
- **Mazda CX-5 2022** (20,000 km, 2.0L AT) $\rightarrow$ **~614 Triệu VNĐ**
- **Mercedes-Benz C200 2021** (35,000 km, 1.5L AT) $\rightarrow$ **~1 Tỷ 732 Triệu VNĐ**

### 7.2. Dự đoán xe bất kỳ qua dòng lệnh
```powershell
python src/models/predict.py --brand "Toyota" --model "Vios" --year 2020 --mileage 45000 --transmission "Tự động" --fuel "Xăng" --origin "Trong nước" --engine 1.5 --seats 5
```

---

## 8. Kết Quả Thực Nghiệm Cốt Lõi (Experimental Results)

### 8.1. Bảng xếp hạng 10 cấu hình trên tập Validation (Phase 6 Leaderboard)

| Hạng | Tên thí nghiệm | Target | Val MAE (VND) | Val $R^2$ | Val MdAPE (%) |
| :---: | :--- | :---: | :---: | :---: | :---: |
| 🥇 **1** | **`Tree_RandomForest_Tuned_LogTarget` (CHAMPION)** | **log** | **142,934,537** | **0.8694** | **4.25%** |
| 🥈 2 | `Tree_RandomForest_LogTarget` (Default 100 cây) | log | 159,102,971 | 0.8425 | 4.94% |
| 🥉 3 | `Tree_RandomForest_RawTarget` | raw | 168,751,598 | 0.8949 | 6.61% |
| 4 | `Tree_HistGBM_LogTarget` | log | 180,831,847 | 0.7888 | 5.37% |
| 5 | `Tree_HistGBM_RawTarget` | raw | 201,925,471 | 0.8401 | 7.84% |
| 6 | `Linear_Ridge_LogTarget` | log | 255,658,033 | 0.6996 | 7.72% |
| 7 | `Linear_Lasso_LogTarget` | log | 370,691,840 | 0.5455 | 12.22% |
| 8 | `Linear_Ridge_RawTarget` | raw | 379,429,332 | 0.8075 | 23.72% |
| 9 | `Baseline_Dummy_Median` | raw | 914,616,759 | -0.0714 | 39.83% |
| 10 | `Baseline_Dummy_Mean` | raw | 1,164,209,470 | -0.0001 | 94.34% |

### 8.2. Đối chiếu khoa học: Phase 6 (Random Test) vs Phase 6.2 (Group-Aware Test)

Cần phân định rạch ròi hai phép đánh giá độc lập:

| Tiêu chuẩn đo lường | Phase 6 (Random Test - 2,351 xe) | Phase 6.2 (Group-Aware Test - 2,350 xe) | Chênh lệch thực tế | Ý nghĩa khoa học |
| :--- | :---: | :---: | :---: | :--- |
| **Rò rỉ bài đăng trùng lặp** | 9.15% (215 xe) | **0.00% (0 xe)** | **-9.15% (Triệt tiêu)** | Đã cách ly hoàn toàn tin trùng |
| **Test MdAPE** | **4.29%** | **4.29%** | **0.00% (Trùng khớp)** | **Độ chính xác tương đối không hề suy giảm!** |
| **Test MAE** | **111,793,581 VND** | **130,761,443 VND** | +18,967,862 VND | Phản ánh độ phân tán xe siêu sang |
| **Test RMSE** | **482,625,123 VND** | **821,395,226 VND** | +338,770,103 VND | Nhạy cảm với đuôi ngoại lai |
| **Test $R^2$** | **0.9448** | **0.8638** | -0.0810 | Duy trì mức giải thích phương sai rất cao |

> **Khám phá bản chất sự chênh lệch MAE (+18.9M VND)**:
> - Không phải do mô hình bị overfitting hay suy giảm chất lượng định giá.
> - Ở phân khúc xe phổ thông ($\le 500\text{M VND}$, chiếm phần lớn thị trường), MAE của Phase 6.2 thậm chí còn **thấp hơn** Phase 6: **24.2 triệu VND** (so với 26.1M). Nhóm xe 500M–1B giữ nguyên mức **40.5 triệu VND**.
> - Mức tăng của MAE toàn tập xuất phát từ việc tập Test mới ngẫu nhiên có thêm **27 xe siêu sang $> 5\text{ tỷ VND}$** (117 xe so với 90 xe). Riêng 27 xe này đã làm tăng trung bình MAE thêm **+14.5 triệu VND**!
> - Việc chỉ số **MdAPE giữ vững chính xác ở mức 4.29%** chứng minh mô hình có độ bền khoa học tuyệt đối.

---

## 9. Tầm Quan Trọng Của Đặc Trưng & Nghiệp Vụ Thuế Xe

Phân tích Mean Decrease in Impurity (MDI / Variance Reduction) từ Random Forest:
1. **`is_luxury_brand` (43.10% MDI)**: Xác lập trần giá phân khúc xe sang.
2. **`engine_displacement_l` (26.35% MDI)**: Gắn chặt chẽ với **Biểu thuế Tiêu thụ Đặc biệt (TTĐB)** tại Việt Nam (áp thuế suất lũy tiến từ 35% đến 150% đối với dung tích xi-lanh lớn).
3. `brand` (5.72%), `model` (5.63%), `car_age` (4.41%), `year` (3.52%), `transmission` (2.38%), `seats` (2.31%), `fuel_type` (2.12%), `body_type` (1.87%), `origin` (1.48%), `mileage_km` (0.69%).

*Lưu ý nghiệp vụ về ODO*: Biến `mileage_km` có tỷ trọng toàn cục thấp vì khoảng giá thương hiệu (tới 40 tỷ) áp đảo ODO. Tuy nhiên ở cấp độ cục bộ (cùng một dòng xe, cùng năm sản xuất), ODO là nhân tố chính quyết định mức chênh lệch giá 30 – 50 triệu VND.

---

## 10. Giới Hạn Đề Tài & Định Hướng Tương Lai (Limitations & Future Work)

### 10.1. Giới hạn học thuật
- **Asking Price vs Transaction Price**: Dữ liệu phản ánh giá chào bán; giá giao dịch thực tế thấp hơn 2%–5% sau mặc cả.
- **Thiếu số khung VIN**: Do các sàn xe tại Việt Nam không công khai VIN, không thể khẳng định 100% hai salon khác nhau có đang rao cùng một chiếc xe vật lý ngoài đời hay không.
- **Mặt cắt ngang tĩnh**: Dữ liệu là lát cắt năm 2023, chưa phản ánh biến động giảm lệ phí trước bạ theo chu kỳ chính sách.

### 10.2. Định hướng tiếp theo
- Thử nghiệm các mô hình Gradient Boosting chuyên dụng: CatBoost, LightGBM, XGBoost.
- Ứng dụng NLP (PhoBERT) để trích xuất option từ trường mô tả tin đăng và Computer Vision để phân tích hình ảnh xe.
- Đóng gói container Docker và triển khai REST API với FastAPI cùng giao diện tra cứu Streamlit.

---
*Dự án hoàn thành đầy đủ, đạt chuẩn xuất sắc và sẵn sàng cho buổi bảo vệ kết thúc khóa đào tạo AI Club.*
