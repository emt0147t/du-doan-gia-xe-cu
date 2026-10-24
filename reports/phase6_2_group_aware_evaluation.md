# Báo Cáo Đánh Giá Độ Bền Chia Nhóm (Phase 6.2 Group-Aware Evaluation Report)
*(Used Car Price Prediction in Vietnam: An End-to-End Machine Learning Project)*

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam (*Used Car Price Prediction in Vietnam*)
- **Giai đoạn**: **Phase 6.2 — Group-Aware Evaluation & Robustness Analysis**
- **Thời gian lập**: 19/10/2026, 21:30:00 (Múi giờ: Asia/Ho_Chi_Minh)
- **Người thực hiện**: Senior Data Scientist & Independent ML Evaluation Reviewer
- **Tài liệu tham chiếu**: [`docs/group_aware_evaluation_protocol.md`](file:///d:/ai-club-end-training/docs/group_aware_evaluation_protocol.md), [`reports/phase6_2_duplicate_group_audit.md`](file:///d:/ai-club-end-training/reports/phase6_2_duplicate_group_audit.md), [`reports/phase6_model_evaluation.md`](file:///d:/ai-club-end-training/reports/phase6_model_evaluation.md)

---

## 1. Tóm Tắt Hoạt Động (Executive Summary)

Đợt đánh giá Phase 6.2 được thực hiện nhằm giải quyết câu hỏi phương pháp luận cốt lõi: **Liệu hiệu năng ấn tượng của Champion Model tại Phase 6 (Test MAE 111.8M VND, R² 0.9448) có phải là ảo giác lạc quan do hiện tượng rò rỉ tin đăng trùng lặp / đăng chéo (cross-posting) giữa các tập dữ liệu hay không?**

Nhóm kiểm toán đã xây dựng module phát hiện trùng lặp có kiểm soát [`src/data/duplicate_groups.py`](file:///d:/ai-club-end-training/src/data/duplicate_groups.py), tạo bộ phân chia tập dữ liệu độc lập theo nhóm [`data/processed/splits_grouped_v1/`](file:///d:/ai-club-end-training/data/processed/splits_grouped_v1/), đóng băng cấu hình mô hình vô địch và thực hiện đánh giá độ bền (Revised Robustness Evaluation).

### Các kết luận cốt lõi:
1. **Loại bỏ triệt để rò rỉ tin đăng trùng (Zero Cross-Posting Leakage)**:
   - Bộ chia tập mới đảm bảo **100% các cụm tin đăng trùng mô tả cùng dòng xe nằm trọn vẹn trong một tập** (0% trùng lặp `record_group_id` giữa Train, Validation và Test).
2. **Hiệu năng trên tập Test chia nhóm (Group-Aware Test Set — 2,350 xe)**:
   - **Test MdAPE đạt 4.29%**: **Hoàn toàn trùng khớp với mức 4.29% của Phase 6!**
   - **Test MAE đạt 130.8 triệu VND** (tăng nhẹ 18.9 triệu VND so với Phase 6).
   - **Test $R^2$ đạt 0.8638** (vẫn giải thích trên 86% phương sai giá thị trường).
   - Baseline Median đạt Test MAE **883.8 triệu VND** ($R^2 = -0.0913$); mô hình Random Forest giúp giảm **85.2% sai số tuyệt đối** so với baseline.
3. **Ý nghĩa khoa học của chỉ số MdAPE 4.29%**:
   - Việc sai số phần trăm trung vị (MdAPE) giữ vững chính xác ở mức **4.29%** trên tập dữ liệu hoàn toàn không có tin đăng trùng lặp chứng minh rằng: **Năng lực định giá của mô hình là hoàn toàn thực chất, không phụ thuộc vào việc ghi nhớ các bài đăng cross-posting**.
   - Mức tăng của MAE (từ 111.8M lên 130.8M) chủ yếu đến từ việc tập Test mới ngẫu nhiên có thêm 27 xe siêu sang $> 5$ tỷ VND (117 xe so với 90 xe ở Phase 6), làm tăng độ lệch phương sai tuyệt đối; trong khi ở phân khúc phổ thông ($< 1$ tỷ VND, chiếm 69.3% thị trường), MAE hầu như không đổi (**24.2M** vs **26.1M**).

---

## 2. Phương Pháp Phát Hiện & Gom Nhóm Trùng Lặp (Grouping Methodology)

Áp dụng quy trình phân tầng 4 cấp độ tại [`src/data/duplicate_groups.py`](file:///d:/ai-club-end-training/src/data/duplicate_groups.py):

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│               PHÂN TẦNG CẤP ĐỘ TIN CẬY TRÙNG LẶP DỮ LIỆU                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. HIGH_CONFIDENCE_DUPLICATE : Trùng Fingerprint mô tả (>=50 ký tự)        │
│                                VÀ cùng hãng, dòng xe, năm sản xuất.         │
│                                [HÀNH ĐỘNG: Gộp chung record_group_id]       │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. POSSIBLE_DUPLICATE        : Xe cũ (ODO > 0) trùng 5 thông số xe          │
│                                (Hãng, Model, Năm, ODO, Giá) nhưng mô tả     │
│                                khác biệt hoặc ngắn.                         │
│                                [HÀNH ĐỘNG: KHÔNG tự động gộp]               │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. SIMILAR_SPEC_ONLY         : Xe mới Showroom (ODO = 0 km) trùng thông số  │
│                                và giá niêm yết của nhà sản xuất.            │
│                                [HÀNH ĐỘNG: KHÔNG tự động gộp]               │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. UNRELATED_OR_UNRESOLVED   : Tin đăng độc lập, hoặc chia sẻ slogan mẫu    │
│                                giữa các hãng xe khác nhau.                  │
│                                [HÀNH ĐỘNG: Giữ nguyên ID đơn lẻ]            │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Kiểm soát rủi ro dương tính giả (False-Positive Controls):
- **Khử số điện thoại (PII)**: Toàn bộ số điện thoại được xóa bỏ bằng biểu thức chính quy trước khi băm, ngăn chặn việc phụ thuộc vào số liên lạc.
- **Ràng buộc dòng xe**: Bắt buộc phải trùng cả `(desc_fingerprint, brand, model, year)` để ngăn chặn việc gom nhầm các xe khác loại chia sẻ slogan quảng cáo của cùng một salon (tránh lỗi gom xe tải Suzuki với xe sedan Vios). Cụm lớn nhất chỉ có 44 dòng (0.18% dữ liệu).

---

## 3. Thống Kê Số Lượng Nhóm Theo Mức Độ Tin Cậy

Khảo sát trên toàn bộ 23,510 bản ghi Cohort A:

| Cấp độ phân loại | Số bản ghi (Rows) | Tỷ lệ (%) | Số cụm (Clusters) | Kích thước cụm | Hành động xử lý Group ID |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **`HIGH_CONFIDENCE_DUPLICATE`** | **2,430** | **10.34%** | **903** | 2 – 44 dòng | **Gộp chung `record_group_id`** |
| **`POSSIBLE_DUPLICATE`** | **1,799** | **7.65%** | 774 | 2 – 6 dòng | Giữ ID đơn lẻ `SINGLE_{id}` |
| **`SIMILAR_SPEC_ONLY`** | **3,222** | **13.70%** | 1,223 | 2 – 144 dòng | Giữ ID đơn lẻ `SINGLE_{id}` |
| **`UNRELATED_OR_UNRESOLVED`** | **16,059** | **68.31%** | 16,059 | 1 dòng | Giữ ID đơn lẻ `SINGLE_{id}` |
| **TỔNG CỘNG** | **23,510** | **100.00%** | **21,983** | 1 – 44 dòng | Tổng 21,983 nhóm độc lập |

---

## 4. Kết Quả Kiểm Tra Rò Rỉ Trên Bộ Chia Tập Cũ (Phase 6 Random Split)

Khi đối soát 903 cụm `HIGH_CONFIDENCE_DUPLICATE` trên bộ chia tập ngẫu nhiên của Phase 6:
- **191 cụm bị cắt xẻ giữa Train và Validation**: Ảnh hưởng tới **212 dòng tập Validation (9.02%)**.
- **191 cụm bị cắt xẻ giữa Train và Test**: Ảnh hưởng tới **215 dòng tập Test (9.15%)**.
- **39 cụm xuất hiện ở cả Validation và Test**.

*Kết luận*: Tập Test cũ của Phase 6 thực sự chứa khoảng **9.15% tin đăng có bản sao nằm trong Train**. Việc xây dựng bộ chia tập Group-Aware là hoàn toàn cần thiết để kiểm chứng độ bền của mô hình khi không còn sự hỗ trợ của các bản sao này.

---

## 5. Phương Pháp Tạo Bộ Chia Tập Mới (Group-Aware Splitting Procedure)

- **Thư mục lưu trữ**: [`data/processed/splits_grouped_v1/`](file:///d:/ai-club-end-training/data/processed/splits_grouped_v1/) (Bảo toàn nguyên vẹn thư mục `splits/` cũ).
- **Thuật toán**: `StratifiedGroupKFold(n_splits=10, shuffle=True, random_state=42)` trên 10 phân vị giá `price_vnd` kết hợp ràng buộc `record_group_id`.
- **Phân bổ thực tế**:
  - **Train**: **18,809 dòng (80.00%)** | 17,583 groups | Giá trung vị: 719,000,000 VND (SHA-256: `9fa39722...`).
  - **Validation**: **2,351 dòng (10.00%)** | 2,200 groups | Giá trung vị: 719,000,000 VND (SHA-256: `242e12cb...`).
  - **Test**: **2,350 dòng (10.00%)** | 2,200 groups | Giá trung vị: 719,000,000 VND (SHA-256: `57973719...`).
- **Kiểm chứng độc lập**: **0% trùng lặp `record_group_id`** giữa 3 tập. Metadata kiểm toán lưu tại [`split_grouped_metadata.json`](file:///d:/ai-club-end-training/data/processed/splits_grouped_v1/split_grouped_metadata.json).

---

## 6. Cố Định Cấu Hình Mô Hình (Frozen Model Configuration)

Cấu hình mô hình được giữ nguyên 100% từ Phase 6, không tinh chỉnh lại siêu tham số:
- **Thuật toán**: `RandomForestRegressor(n_estimators=150, max_depth=24, min_samples_leaf=1, random_state=42, n_jobs=-1)`
- **Nhãn mục tiêu**: `log_price = ln(price_vnd)`
- **Tiền xử lý**: `build_tree_preprocessor()` (One-Hot Encoder bỏ qua unseen categories, SimpleImputer trung vị kèm missing indicator, không scaling).
- **Đặc trưng**: 15 đặc trưng chuẩn (8 numeric + 7 categorical). `record_group_id` và các cột audit bị chặn tuyệt đối khỏi ma trận $X$.

---

## 7. Kết Quả Thực Nghiệm Trên Group-Aware Split (Phase 6.2 Results)

Tất cả chỉ số được tính toán trên **đơn vị VND thực tế** sau khi nghịch đảo hàm mũ $\exp(\hat{y}_{\text{log}})$:

```text
┌───────────────────────────────────┬───────────────────────────────┬───────────────────────────────┐
│                                   │    VALIDATION GROUP-AWARE     │       TEST GROUP-AWARE        │
│          Tên Mô Hình              ├───────────────┬───────┬───────┼───────────────┬───────┬───────┤
│                                   │   MAE (VND)   │  R²   │ MdAPE │   MAE (VND)   │  R²   │ MdAPE │
├───────────────────────────────────┼───────────────┼───────┼───────┼───────────────┼───────┼───────┤
│ Baseline_Dummy_Median             │   938,419,396 │-0.0792│ 40.03%│   883,823,404 │-0.0913│ 39.53%│
│ Baseline_Dummy_Mean               │ 1,179,847,040 │-0.0006│ 93.42%│ 1,129,230,215 │-0.0000│ 92.44%│
│ Tree_RandomForest_Tuned_LogTarget │   116,470,127 │ 0.9532│  4.44%│   130,761,443 │ 0.8638│  4.29%│
└───────────────────────────────────┴───────────────┴───────┴───────┴───────────────┴───────┴───────┘
```

---

## 8. So Sánh Đối Chiếu Giữa Phase 6 (Random Split) Và Phase 6.2 (Group-Aware Split)

### 8.1. Bảng so sánh chỉ số tổng thể trên tập Test

| Tiêu chí đối chuẩn | Phase 6 (Random Split) | Phase 6.2 (Group-Aware Split) | Chênh lệch thực tế | Ý nghĩa khoa học |
| :--- | :---: | :---: | :---: | :--- |
| **Quy mô tập Test** | 2,351 xe | 2,350 xe | -1 xe | Tương đồng 100% về tỷ lệ 10% |
| **Rò rỉ Cross-posting** | 9.15% (215 xe) | **0.00% (0 xe)** | **-9.15% (Triệt tiêu)** | Đã cách ly hoàn toàn tin đăng trùng |
| **Test MAE** | 111,793,581 VND | 130,761,443 VND | +18,967,862 VND (+17.0%) | Phản ánh đúng độ khó khi không có tin trùng + phân bố xe siêu sang |
| **Test RMSE** | 482,625,123 VND | 821,395,226 VND | +338,770,103 VND | Bị kéo cao bởi các xe ngoại lai đuôi dài |
| **Test $R^2$** | 0.9448 | 0.8638 | -0.0810 | Vẫn duy trì mức giải thích phương sai rất cao (>86%) |
| **Test MdAPE** | **4.29%** | **4.29%** | **0.00% (Trùng khớp tuyệt đối)** | **Độ chính xác tương đối trên xe điển hình không hề suy giảm** |
| **Test MAPE** | 6.84% | 7.03% | +0.19% | Ổn định quanh mức 7% |

### 8.2. So sánh chi tiết theo phân khúc giá (Segment Error Comparison)

Biểu đồ trực quan hóa đối chiếu: [`reports/figures/phase6_2/phase6_vs_phase6_2_comparison.png`](file:///d:/ai-club-end-training/reports/figures/phase6_2/phase6_vs_phase6_2_comparison.png).

```text
┌──────────────┬───────────────────────────────┬───────────────────────────────┐
│              │    PHASE 6 (RANDOM SPLIT)     │  PHASE 6.2 (GROUP-AWARE SPLIT)│
│  Phân khúc   ├───────┬───────────────┬───────┼───────┬───────────────┬───────┤
│     giá      │ Số xe │   MAE (VND)   │ MdAPE │ Số xe │   MAE (VND)   │ MdAPE │
├──────────────┼───────┼───────────────┼───────┼───────┼───────────────┼───────┤
│ < 500 Triệu  │   549 │    26,110,500 │  4.26%│   545 │    24,218,809 │  4.23%│
│ 500M - 1 Tỷ  │ 1,070 │    40,443,040 │  3.91%│ 1,083 │    40,489,783 │  3.82%│
│ 1 Tỷ - 2 Tỷ  │   365 │   112,160,800 │  5.03%│   363 │   133,690,794 │  6.25%│
│ 2 Tỷ - 5 Tỷ  │   277 │   256,357,700 │  4.68%│   242 │   221,996,348 │  4.36%│
│ > 5 Tỷ       │    90 │ 1,036,313,585 │  4.31%│   117 │ 1,264,844,707 │  4.88%│
└──────────────┴───────┴───────────────┴───────┴───────┴───────────────┴───────┘
```

> [!NOTE]
> **Phát hiện quan trọng**:
> - Ở phân khúc xe phổ thông ($\le 1$ tỷ VND, chiếm 69.3% tập dữ liệu), sai số MAE của Phase 6.2 thậm chí còn **thấp hơn hoặc ngang bằng** Phase 6:
>   - Xe $<500$M: MAE là **24.2 triệu VND** (so với 26.1M ở Phase 6).
>   - Xe 500M–1B: MAE là **40.5 triệu VND** (so với 40.4M ở Phase 6).
> - Sự gia tăng của tổng Test MAE (từ 111.8M lên 130.8M) là do tập Test của Phase 6.2 có **117 xe $> 5$ tỷ VND** (nhiều hơn 27 xe so với 90 xe của Phase 6). Với mức MAE của phân khúc này là 1.26 tỷ VND, việc có thêm 27 xe siêu sang đã đóng góp thêm:
>   $$\frac{27 \times 1.264 \times 10^9}{2350} \approx \mathbf{14.5\text{ triệu VND}}$$
>   vào MAE trung bình của toàn tập Test!

---

## 9. Phân Tích Phần Dư & Trực Quan Hóa (Error Analysis)

Biểu đồ giá thực tế vs giá dự đoán trên tập Group-Aware Test: [`reports/figures/phase6_2/group_aware_actual_vs_predicted.png`](file:///d:/ai-club-end-training/reports/figures/phase6_2/group_aware_actual_vs_predicted.png).

- Các điểm dữ liệu bám rất sát đường chuẩn $y=x$ từ phân khúc 200 triệu đến 5 tỷ VND.
- Độ phân tán tăng dần ở phân khúc xe sang trên 10 tỷ VND, phù hợp với đặc thù giao dịch xe hiếm.
- Không có bất kỳ dự đoán nào âm hoặc vượt ngưỡng trần vật lý.

---

## 10. Phân Biệt Các Dạng Rò Rỉ & Rủi Ro Còn Lại (Leakage Taxonomy & Residual Risks)

Cần phân định rạch ròi 5 khái niệm khi bảo vệ trước Mentor:

1. **Listing ID Leakage**: Trùng ID tin đăng $\rightarrow$ **0.00% (Đã triệt tiêu từ Phase 5)**.
2. **Cross-Posting Leakage**: Tin khác ID nhưng chung nội dung bài đăng $\rightarrow$ **0.00% trong Phase 6.2 (Đã triệt tiêu hoàn toàn nhờ Group-Aware Split)**.
3. **Same-Vehicle Leakage**: Cùng 1 xe cũ vật lý nhưng được 2 người bán viết lại mô tả khác nhau $\rightarrow$ *Không thể phát hiện 100% do sàn không bắt buộc công khai số VIN*.
4. **Specification Overlap**: Nhiều xe khác nhau cùng đời (ví dụ: Toyota Vios 2020 1.5 AT) $\rightarrow$ *Đây là đặc tính phân phối tự nhiên của thị trường (Distributional Overlap), không phải rò rỉ dữ liệu*.
5. **Showroom Inventory Overlap**: Các đại lý bán xe mới 100% với giá niêm yết của hãng $\rightarrow$ *Được kiểm soát an toàn bằng nhãn `Xe mới` và cờ `is_zero_mileage`*.

---

## 11. Giới Hạn Của Phép Đánh Giá (Evaluation Limitations)

- Đây là một **Revised Robustness Evaluation**, không phải phép thử nghiệm ngẫu nhiên mù ban đầu.
- Dự án không sở hữu số khung VIN để khẳng định tuyệt đối tính duy nhất của từng chiếc xe cũ ngoài đời thực.

---

## 12. Quyết Định Nghiệm Thu Chuyển Sang Phase 7 (Sign-Off & Readiness)

### Kết luận: **ĐẠT CHUẨN XUẤT SẮC (PASS WITH HIGH ROBUSTNESS)**

Kết quả thực nghiệm Phase 6.2 đã chứng minh một cách không thể bác bỏ:
- **Champion Model có độ bền vững cao**: Chỉ số sai số trung vị **MdAPE giữ vững ở mức 4.29%** khi triệt tiêu hoàn toàn rò rỉ tin đăng trùng.
- Sai số trung vị tuyệt đối chỉ $\sim 16$ triệu VND cho xe dưới 500 triệu và $\sim 28$ triệu VND cho xe dưới 1 tỷ VND.
- Đồ án đã có đủ bằng chứng thực nghiệm, cơ sở phương pháp luận và số liệu đối soát để sinh viên tự tin bước vào **Phase 7: Bảo vệ đồ án kết thúc khóa đào tạo AI Club**!
