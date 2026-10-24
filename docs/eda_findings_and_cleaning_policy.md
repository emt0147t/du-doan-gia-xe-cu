# Quy Hoạch Làm Sạch Dữ Liệu & Tái Đánh Giá Chính Sách Kiểm Định
*(EDA Findings & Data Cleaning Policy Specification)*

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam (Used Car Price Prediction in Vietnam)
- **Giai đoạn**: Phase 4 — Exploratory Data Analysis & Data Quality Investigation
- **Thời gian lập**: 19/10/2026, 02:30:00 (Múi giờ: Asia/Ho_Chi_Minh)
- **Người thực hiện**: Senior Data Scientist & ML Engineer
- **Tài liệu đối chiếu**: [Data Dictionary](file:///d:/ai-club-end-training/docs/data_dictionary.md), [Schema Mapping](file:///d:/ai-club-end-training/docs/schema_mapping.md), [Initial Audit Report](file:///d:/ai-club-end-training/reports/dataset_initial_audit.md)

---

## 1. Nguyên Tắc Cốt Lõi: Phân Định Rạch Ròi 3 Cấp Độ Đánh Giá

Trước khi đề xuất bất kỳ thao tác lọc bỏ hay biến đổi dữ liệu nào cho Phase 5, nhóm xác định rõ ràng sự khác biệt bản chất giữa ba khái niệm:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. TÍNH HỢP LỆ DỮ LIỆU (DATA VALIDITY)                                      │
│    - Dữ liệu phản ánh một thực thể quan sát có thật hay bị lỗi kỹ thuật,    │
│      hư hỏng mã hóa, lỗi tràn số (overflow) hoặc chuỗi rác?                │
│    - Ví dụ: Số ODO = 4,294,967,295 km là INVALID do tràn số uint32.        │
│    - Ví dụ: Xe sản xuất năm 1995 giá 50 triệu là VALID (xe thật ngoài đời). │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. PHẠM VI DỰ ÁN (PROJECT SCOPE)                                            │
│    - Dữ liệu có thuộc phân khúc thị trường mà đồ án cam kết giải quyết?    │
│    - Điều lệ dự án (Project Charter) quy định bài toán: Định giá xe ô tô   │
│      đại chúng phổ biến tại Việt Nam (thường có tuổi đời từ 2010 đến nay).  │
│    - Xe cổ (1990 - 2009) tuy hợp lệ ngoài đời nhưng nằm ngoài phạm vi      │
│      mô hình thương mại đại chúng vì cơ chế khấu hao phi tuyến tính.       │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. TÍNH KHẢ DỤNG CHO MÔ HÌNH (MODELING ELIGIBILITY)                         │
│    - Bản ghi có đủ các biến đặc trưng quan trọng và nhãn mục tiêu tin cậy   │
│      để thuật toán học máy (Linear, Tree-based) học được quy luật chung     │
│      mà không bị nhiễu loạn bởi ngoại lai cực đoan?                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

> [!CAUTION]
> **Cam kết liêm chính kỹ thuật**:
> - Nhóm **tuyệt đối không tự động xóa bỏ 3,423 dòng** chỉ vì module `validation.py` gắn cờ vi phạm hợp đồng thử nghiệm.
> - Nhóm **tuyệt đối không sửa đổi mã nguồn `src/data/validation.py`** chỉ nhằm mục đích nâng khống tỷ lệ "Valid" lên 100%. Mọi điều chỉnh chính sách phải có bằng chứng thống kê thực nghiệm và đánh giá rủi ro mất mát thông tin.

---

## 2. Bảng Đối Chiếu Chi Tiết 7 Chính Sách Làm Sạch Dữ Liệu Đề Xuất Cho Phase 5

| Mã chính sách | Vấn đề quan sát được (Observed Issue) | Bằng chứng thực nghiệm (Empirical Evidence) | Quyết định đề xuất (Proposed Decision) | Số dòng ảnh hưởng (%) | Rủi ro mất mát thông tin (Information Loss Risk) | Phương pháp kiểm tra sau xử lý (Verification Method) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **POL-01: Filter Old Cars (< 2010)** | 3,303 xe sản xuất từ năm 1990 đến 2009. | Quan sát [Hình 5](file:///d:/ai-club-end-training/reports/figures/phase4/fig05_median_price_trend_by_year.png): Trung vị giá xe trước 2010 dao động hỗn loạn (100M - 400M), mẫu rất thưa thớt ($n < 50$ xe/năm). | **Lọc bỏ khỏi tập huấn luyện đại chúng**: Định nghĩa phạm vi mô hình chính $2010 \le \text{year} \le 2024$. | 3,303 dòng (10.78%) | **Thấp đối với mục tiêu đại chúng**: Mất 10.78% dữ liệu xe quá 15 năm tuổi, nhưng bảo vệ mô hình khỏi quy luật định giá phi chuẩn của xe cũ nát/xe sưu tầm. | `assert df_clean['year'].min() >= 2010` và kiểm tra phân phối $R^2$ không bị kéo lệch. |
| **POL-02: Handle Missing Year** | 32 bản ghi bị khuyết thiếu trường `Năm sản xuất`. | `car_detail.csv` có đúng 32 dòng `Năm sản xuất = NaN`. Tên xe có thể chứa năm nhưng không nhất quán. | **Loại bỏ bản ghi thiếu năm**: Năm sản xuất là biến số quan trọng bậc nhất quyết định giá trị xe ($r = 0.52$). | 32 dòng (0.10%) | **Cực thấp (0.10%)**: Số lượng quá nhỏ, không làm suy giảm tính đại diện của mẫu. | `assert df_clean['year'].isna().sum() == 0`. |
| **POL-03: Resolve Mileage Overflow & Corrupted Outliers** | 124 bản ghi có ODO $> 1,000,000$ km; xuất hiện giá trị tràn số $4,294,967,295$ km ($2^{32}-1$) trong bảng processed. | Giá trị $2^{32}-1$ là giá trị lính canh (sentinel) do lập trình viên cào gán khi thiếu ODO. Một số xe khác ghi $35,000,000$ km do gõ thừa số 0. | **Gán về `NaN` hoặc loại bỏ**: Các xe có ODO $> 1,000,000$ km coi là lỗi nhập liệu. | 124 dòng (0.40%) | **Không có rủi ro**: Loại bỏ hoàn toàn nhiễu loạn do lỗi nhập liệu thô. | `assert (df_clean['mileage_km'] > 1_000_000).sum() == 0`. |
| **POL-04: Address Zero-Mileage Inflation** | 10,442 xe có số ODO = 0 km (34.07% tổng số tin). | [Hình 10](file:///d:/ai-club-end-training/reports/figures/phase4/fig10_mileage_distribution.png) cho thấy đỉnh nhọn tại 0 km. Đối chiếu: 6,070 xe là `Xe mới` tại showroom; 4,372 xe là `Xe đã dùng` nhưng người bán không khai báo ODO. | **Không xóa bỏ**: Tạo đặc trưng cờ nhị phân `is_zero_mileage` (1 nếu ODO = 0, 0 nếu ODO > 0); đồng thời tách phân tích phân khúc xe mới vs xe cũ. | 0 dòng bị xóa (Bảo toàn 10,442 dòng) | **Không mất mát**: Giữ trọn vẹn 34% dữ liệu cho bài toán tổng thể. | Kiểm tra ma trận tương quan giữa `is_zero_mileage` và `price_vnd`. |
| **POL-05: Target Price Clipping / Bounding** | 13 xe có giá $< 30$ triệu VND (18M - 29M); 1 xe Rolls-Royce có giá 54 tỷ VND. | 13 xe $< 30$M là xe xác/đặt cọc hoặc điền giá tượng trưng. Xe 54B là siêu xe siêu sang cá biệt ([Hình 2a](file:///d:/ai-club-end-training/reports/figures/phase4/fig02_target_price_boxplot.png)). | **Lọc biên giá**: Giữ các tin rao có $30\text{ triệu} \le \text{price\_vnd} \le 50\text{ tỷ VND}$. | 14 dòng (0.05%) | **Cực thấp (0.05%)**: Loại trừ các tin đặt cọc ảo và siêu xe cá biệt làm phồng sai số RMSE. | `assert (df_clean['price_vnd'] < 30e6).sum() == 0` và `assert (df_clean['price_vnd'] > 50e9).sum() == 0`. |
| **POL-06: Standardize Categorical Anomalies** | Cột `Hộp số` có 15 tin ghi nhận ký tự `'-'` và 2 tin ghi `'Số hỗn hợp'`. Cột `Hãng` có `'Mercedes Benz'` viết thiếu gạch nối. | Kiểm tra phân phối: 17 tin hộp số dị biệt không thể khớp danh mục chuẩn. Thương hiệu `'Mercedes Benz'` (3,191 xe) cần chuẩn hóa thành `'Mercedes-Benz'`. | **Chuẩn hóa chuỗi & Gán mode/Loại bỏ**: Đổi tên `'Mercedes Benz'` $\rightarrow$ `'Mercedes-Benz'`; 17 tin dị biệt hộp số chuyển thành `NaN` (trường tùy chọn) hoặc loại bỏ. | 17 dòng (0.06%) | **Không mất mát thông tin**: Chuẩn hóa làm tăng chất lượng danh mục. | `assert 'Mercedes Benz' not in df_clean['brand'].unique()`. |
| **POL-07: Log Transformation of Target Variable** | Phân phối giá bị lệch phải cực kỳ nghiêm trọng (Skewness $= 7.82$, [Hình 1](file:///d:/ai-club-end-training/reports/figures/phase4/fig01_target_price_distribution.png)). | Sau khi lấy $\ln(\text{price\_vnd})$, phân phối trở nên đối xứng hoàn hảo dạng hình chuông (Skewness $= 0.68$, [Hình 3](file:///d:/ai-club-end-training/reports/figures/phase4/fig03_target_log1p_distribution.png)). | **Huấn luyện mô hình trên biến đổi $\ln(y)$**: Áp dụng $\hat{y} = \exp(\hat{z})$ khi dự đoán đầu ra thực tế. | 0 dòng bị xóa (Tác vụ biến đổi toán học) | **Không mất mát**: Giúp các mô hình tuyến tính và Gradient Boosting hội tụ nhanh và tối ưu sai số MAPE/RMSLE. | Kiểm tra độ đối xứng và chỉ số Skewness của $\ln(y)$. |

---

## 3. Tổng Kết Số Lượng Dòng Dữ Liệu Sau Khi Áp Dụng Chính Sách (Projected Sample Size)

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│               DỰ PHÓNG QUY MÔ TẬP DỮ LIỆU SẠCH CHO HUẤN LUYỆN (PHASE 5)     │
├──────────────────────────────────────────────────────┬──────────────────────┤
│ 1. Tổng số bản ghi thô ban đầu (car_detail.csv)      │ 30,652 dòng (100.0%) │
│ 2. Loại bỏ do thiếu Năm sản xuất (POL-02)            │ -32 dòng   ( -0.10%) │
│ 3. Loại bỏ do ngoài biên giá [30M, 50B] (POL-05)     │ -14 dòng   ( -0.05%) │
│ 4. Loại bỏ do dị biệt hộp số '-' (POL-06)            │ -17 dòng   ( -0.06%) │
│ 5. Loại bỏ do ODO tràn số corrupt (POL-03)           │ -124 dòng  ( -0.40%) │
│ 6. Phân đoạn xe đại chúng (Năm sản xuất >= 2010)     │ -3,236 dòng( -10.56%)│
├──────────────────────────────────────────────────────┼──────────────────────┤
│ TẬP DỮ LIỆU SẠCH TIÊU CHUẨN ĐẦU RA (CAR_CLEAN)       │ 27,229 dòng ( 88.83%)│
└──────────────────────────────────────────────────────┴──────────────────────┘
```

> [!TIP]
> **Nhận định của Mentor**:
> Quy mô **27,229 bản ghi chuẩn mực** là một tập dữ liệu cực kỳ lý tưởng cho một đồ án Machine Learning kết thúc khóa (vượt gấp 5 đến 9 lần mục tiêu tối thiểu 3,000 - 5,000 dòng đề ra trong Project Charter). 
> Tỷ lệ bảo toàn dữ liệu đạt **88.83%**, vừa loại bỏ triệt để các rủi ro nhiễu loạn toán học, vừa bảo đảm độ phong phú và tính tổng quát của mô hình.
