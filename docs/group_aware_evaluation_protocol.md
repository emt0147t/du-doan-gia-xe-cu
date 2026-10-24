# Đề Cương Đánh Giá Độ Bền Chia Nhóm (Group-Aware Evaluation & Robustness Protocol)
*(Phase 6.2 — Protocol for Group-Aware Robustness Evaluation)*

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam (*Used Car Price Prediction in Vietnam*)
- **Giai đoạn**: **Phase 6.2 — Group-Aware Robustness Evaluation**
- **Thời gian lập**: 19/10/2026, 21:15:00 (Múi giờ: Asia/Ho_Chi_Minh)
- **Người thực hiện**: Senior Data Scientist & Independent ML Evaluation Reviewer
- **Tài liệu tham chiếu**: [`docs/modeling_protocol.md`](file:///d:/ai-club-end-training/docs/modeling_protocol.md), [`reports/phase6_2_duplicate_group_audit.md`](file:///d:/ai-club-end-training/reports/phase6_2_duplicate_group_audit.md)

---

## 1. Mục Tiêu Đánh Giá & Bản Chất Của Phép Thử Nghiệm (Objective & Scope)

1. **Mục tiêu**:
   - Thẩm định độ bền (robustness) của mô hình học máy khi triệt tiêu hoàn toàn rủi ro rò rỉ tin đăng trùng/đăng chéo (cross-posting leakage) giữa các tập dữ liệu.
   - Trả lời câu hỏi phương pháp luận then chốt: *Liệu kết quả Test ấn tượng ở Phase 6 (MAE 111.8M, R² 0.9448) có bị thổi phồng do mô hình ghi nhớ các tin đăng trùng lặp giữa Train và Test hay không?*
2. **Tuyên bố minh bạch về bản chất phép thử (Revised Robustness Evaluation)**:
   > [!IMPORTANT]
   > Do dữ liệu đã được khảo sát qua các Phase trước, siêu tham số đã được thăm dò trên tập Validation cũ, và kết quả Phase 6 đã được công bố, đợt đánh giá này được xác định rõ ràng là một **Đánh giá độ bền hiệu chỉnh (Revised Robustness Evaluation)**. Tập Test mới này **không được tuyên bố là một tập kiểm thử hoàn toàn mù (blind unseen test) ở mọi khía cạnh**, mà là một thước đo đối chuẩn khoa học để kiểm tra độ nhạy của mô hình trước hiện tượng rò rỉ cụm.

---

## 2. Phương Pháp Phát Hiện Nhóm & Phân Chia Tập (Grouping & Split Procedure)

1. **Phương pháp gom nhóm (`record_group_id`)**:
   - Áp dụng module [`src/data/duplicate_groups.py`](file:///d:/ai-club-end-training/src/data/duplicate_groups.py).
   - Chỉ gộp các bản ghi thuộc cấp độ **`HIGH_CONFIDENCE_DUPLICATE`**:
     - Có văn bản mô tả chuẩn hóa dài $\ge 50$ ký tự trùng khớp tuyệt đối (`desc_fingerprint`).
     - Có cùng thương hiệu (`brand`), dòng xe (`model`) và năm sản xuất (`year`).
   - Các xe mới tại showroom (`SIMILAR_SPEC_ONLY`) và xe cũ trùng 5 thông số nhưng khác mô tả (`POSSIBLE_DUPLICATE`) **tuyệt đối không bị gộp chung** nhằm kiểm soát rủi ro dương tính giả.
   - Mỗi tin đăng độc lập được gán một mã định danh nhóm riêng biệt (`SINGLE_{listing_id}`).
2. **Quy trình phân chia (Group-Aware Splitting)**:
   - Thuật toán: `StratifiedGroupKFold(n_splits=10, shuffle=True, random_state=42)` trên 10 phân vị của biến mục tiêu `price_vnd` kết hợp ràng buộc `record_group_id`.
   - Phân bổ:
     - **Train (80.00%)**: 18,809 dòng (17,583 groups).
     - **Validation (10.00%)**: 2,351 dòng (2,200 groups).
     - **Test (10.00%)**: 2,350 dòng (2,200 groups).
   - **Cam kết không rò rỉ**: 100% `record_group_id` hoàn toàn rời rạc giữa 3 tập (0 nhóm bị chia cắt).
   - Lưu trữ độc lập tại: [`data/processed/splits_grouped_v1/`](file:///d:/ai-club-end-training/data/processed/splits_grouped_v1/).

---

## 3. Cố Định Cấu Hình Mô Hình (Frozen Model Configuration)

Tuân thủ nghiêm ngặt nguyên tắc **đóng băng (Freeze)**, tuyệt đối không tinh chỉnh lại siêu tham số dựa trên kết quả test:

1. **Mô hình chiến thắng đã chọn từ Phase 6**:
   - Tên cấu hình: **`Tree_RandomForest_Tuned_LogTarget`**
   - Loại thuật toán: `RandomForestRegressor`
   - Siêu tham số cố định:
     ```python
     hyperparameters = {
         "n_estimators": 150,
         "max_depth": 24,
         "min_samples_leaf": 1,
         "random_state": 42,
         "n_jobs": -1
     }
     ```
   - Target transformation: `target_type = "log"` ($\ln(\text{price\_vnd})$)
   - Preprocessor: `preprocessor_type = "tree"` (Không scaling, One-Hot Encoding bỏ qua danh mục lạ, SimpleImputer trung vị kèm missing indicator).
2. **Các mô hình đối chuẩn (Baselines)**:
   - `Baseline_Dummy_Median`: Dự đoán trung vị tập Train.
   - `Baseline_Dummy_Mean`: Dự đoán trung bình tập Train.

---

## 4. Quản Trị Đặc Trưng & Loại Trừ Cột Rò Rỉ

- **Ma trận $X$**: Sử dụng đúng 15 đặc trưng tiêu chuẩn đã xác lập tại Phase 5:
  - 8 định lượng: `year`, `car_age`, `mileage_km`, `is_zero_mileage`, `engine_displacement_l`, `seats`, `doors`, `is_luxury_brand`.
  - 7 phân loại: `brand`, `model`, `condition`, `transmission`, `origin`, `body_type`, `fuel_type`.
- **Ràng buộc an toàn**: Các cột `record_group_id`, `duplicate_category`, `desc_fingerprint`, `norm_desc`, `Mô tả`, `Tên xe`, `price_vnd`, `log_price` **tuyệt đối không được phép đi vào ma trận $X$**.

---

## 5. Các Chỉ Số Đánh Giá & Thang Đo (Metrics & Scale)

Toàn bộ dự đoán $\hat{y}_{\text{log}}$ phải được nghịch đảo hàm mũ về đơn vị VND thực tế:
$$\hat{y}_{\text{VND}} = \text{np.clip}(\exp(\hat{y}_{\text{log}}), 30\,000\,000, 100\,000\,000\,000)$$

Các chỉ số đánh giá được tính toán trực tiếp trên **đơn vị VND**:
1. **MAE (Mean Absolute Error)**: Sai số tuyệt đối trung bình (VND).
2. **RMSE (Root Mean Squared Error)**: Căn bậc hai sai số bình phương trung bình (VND).
3. **$R^2$ (Coefficient of Determination)**: Hệ số xác định.
4. **MdAPE (Median Absolute Percentage Error)**: Sai số phần trăm tuyệt đối trung vị (%).
5. **MAPE (Mean Absolute Percentage Error)**: Sai số phần trăm tuyệt đối trung bình (%).

---

## 6. Giới Hạn Của Phép Đánh Giá (Remaining Limitations)

1. **Thiếu định danh số khung xe (VIN)**: Không thể phát hiện các trường hợp cùng một chiếc xe cũ được nhiều người bán khác nhau đăng với thông số làm tròn và văn bản viết lại hoàn toàn.
2. **Specification Overlap tự nhiên**: Việc chia nhóm giải quyết triệt để rò rỉ tin đăng trùng lặp (`listing/cross-posting leakage`), nhưng không nhằm loại bỏ việc các dòng xe cùng đời (ví dụ: Vios 2020) xuất hiện ở cả Train và Test. Đây là đặc tính tự nhiên của bài toán định giá xe thị trường.
"""

    out_doc = Path("docs/group_aware_evaluation_protocol.md")
    with open(out_doc, "w", encoding="utf-8") as f:
        f.write(CodeContent)
    print(f"Đã tạo: {out_doc}")

if __name__ == "__main__":
    pass
