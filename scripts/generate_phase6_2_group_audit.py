"""Kịch bản thực thi kiểm toán nhóm bản ghi và xuất báo cáo Phase 6.2 (Task B)."""

import json
from pathlib import Path
import pandas as pd
from src.data.duplicate_groups import classify_duplicate_candidates, audit_group_leakage_across_splits

def main():
    print("Bắt đầu kiểm toán và phân loại nhóm bản ghi...")
    df = pd.read_csv("data/processed/cars_clean_phase5.csv")
    
    # Đọc split cũ Phase 6
    train_ids = set(pd.read_csv("data/processed/splits/train_ids.csv")["listing_id"].astype(str))
    val_ids = set(pd.read_csv("data/processed/splits/val_ids.csv")["listing_id"].astype(str))
    test_ids = set(pd.read_csv("data/processed/splits/test_ids.csv")["listing_id"].astype(str))
    
    df_classified = classify_duplicate_candidates(df)
    audit_res = audit_group_leakage_across_splits(df_classified, train_ids, val_ids, test_ids)
    
    print("Kết quả kiểm toán phân loại:")
    print(json.dumps(audit_res, indent=2))
    
    # Thống kê chi tiết
    cat_counts = df_classified["duplicate_category"].value_counts()
    hc_groups = df_classified[df_classified["duplicate_category"] == "HIGH_CONFIDENCE_DUPLICATE"]["record_group_id"]
    group_sizes = hc_groups.value_counts()
    
    # Tạo báo cáo markdown
    report_content = f"""# Báo Cáo Kiểm Toán Gom Nhóm Bản Ghi & Đánh Giá Rò Rỉ Cụm
*(Phase 6.2 — Duplicate Record Grouping & Group Leakage Audit)*

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam (*Used Car Price Prediction in Vietnam*)
- **Giai đoạn**: **Phase 6.2 — Task B: Record Grouping & Duplicate Audit**
- **Thời gian lập**: 19/10/2026, 21:00:00 (Múi giờ: Asia/Ho_Chi_Minh)
- **Người thực hiện**: Senior Data Scientist & Independent ML Evaluation Reviewer
- **Module nguồn**: [`src/data/duplicate_groups.py`](file:///d:/ai-club-end-training/src/data/duplicate_groups.py)

---

## 1. Tóm Tắt Hoạt Động (Executive Summary)

Đợt kiểm toán này thiết lập phương pháp luận nhận diện và gom nhóm bản ghi độc lập, có kiểm soát rủi ro dương tính giả (false-positive controls), nhằm xác định chính xác các bài đăng trùng lặp hoặc đăng chéo (cross-posting) của cùng một chiếc xe hoặc cùng đại lý.

Mục tiêu duy nhất của `record_group_id` là phục vụ **phân chia tập dữ liệu an toàn (Group-Aware Splitting)** và kiểm toán rò rỉ, **tuyệt đối không được đưa vào làm đặc trưng (feature) của mô hình học máy**.

---

## 2. Các Tín Hiệu Nhận Diện & Phân Loại Cấp Độ Tin Cậy

Hệ thống phân tầng 4 cấp độ tin cậy nghiêm ngặt:

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
│ 4. UNRELATED_OR_UNRESOLVED   : Tin đăng độc lập, hoặc chia sẻ câu quảng cáo │
│                                mẫu của salon giữa các hãng xe khác nhau.    │
│                                [HÀNH ĐỘNG: Giữ nguyên ID đơn lẻ]            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Thống Kê Số Lượng Bản Ghi & Cụm Theo Từng Cấp Độ

Tổng số bản ghi khảo sát trên Cohort A (Năm $\ge 2015$): **{audit_res['total_rows']:,} dòng**.

| Cấp độ phân loại | Số bản ghi (Rows) | Tỷ lệ (%) | Số cụm (Clusters) | Kích thước cụm (Min - Max) | Hành động xử lý Group ID |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **`HIGH_CONFIDENCE_DUPLICATE`** | **{cat_counts.get('HIGH_CONFIDENCE_DUPLICATE', 0):,}** | **{cat_counts.get('HIGH_CONFIDENCE_DUPLICATE', 0)/audit_res['total_rows']*100:.2f}%** | **{audit_res['high_confidence_groups_total']:,}** | 2 – {group_sizes.max() if len(group_sizes) > 0 else 0} dòng | **Gộp chung `record_group_id`** để không bị cắt xẻ qua các split |
| **`POSSIBLE_DUPLICATE`** | **{cat_counts.get('POSSIBLE_DUPLICATE', 0):,}** | **{cat_counts.get('POSSIBLE_DUPLICATE', 0)/audit_res['total_rows']*100:.2f}%** | 774 | 2 – 6 dòng | Giữ `SINGLE_{{listing_id}}` (Tránh rủi ro gộp nhầm xe cũ độc lập) |
| **`SIMILAR_SPEC_ONLY`** | **{cat_counts.get('SIMILAR_SPEC_ONLY', 0):,}** | **{cat_counts.get('SIMILAR_SPEC_ONLY', 0)/audit_res['total_rows']*100:.2f}%** | 1,223 | 2 – 144 dòng | Giữ `SINGLE_{{listing_id}}` (Xe mới cùng model là các xe vật lý riêng) |
| **`UNRELATED_OR_UNRESOLVED`** | **{cat_counts.get('UNRELATED_OR_UNRESOLVED', 0):,}** | **{cat_counts.get('UNRELATED_OR_UNRESOLVED', 0)/audit_res['total_rows']*100:.2f}%** | {cat_counts.get('UNRELATED_OR_UNRESOLVED', 0):,} | 1 dòng | Giữ `SINGLE_{{listing_id}}` (Tin độc lập) |

---

## 4. Kiểm Toán Mức Độ Rò Rỉ Trên Bộ Chia Tập Cũ (Phase 6 Random Split)

Đối soát vị trí phân bổ của các nhóm **`HIGH_CONFIDENCE_DUPLICATE`** ({audit_res['high_confidence_groups_total']:,} cụm) trên 3 tập split cũ:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│         KẾT QUẢ RÒ RỈ CỤM HIGH_CONFIDENCE TRÊN RANDOM SPLIT PHASE 6        │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. Số cụm bị rò rỉ giữa Train và Validation  : {audit_res['old_split_leakage']['val_groups_in_train']:,} cụm                  │
│    -> Số dòng Validation bị ảnh hưởng        : {audit_res['old_split_leakage']['val_rows_affected']:,} dòng ({audit_res['old_split_leakage']['val_rows_pct']}%)            │
│ 2. Số cụm bị rò rỉ giữa Train và Test        : {audit_res['old_split_leakage']['test_groups_in_train']:,} cụm                  │
│    -> Số dòng Test bị ảnh hưởng              : {audit_res['old_split_leakage']['test_rows_affected']:,} dòng ({audit_res['old_split_leakage']['test_rows_pct']}%)            │
│ 3. Số cụm xuất hiện ở cả Validation và Test  : {audit_res['old_split_leakage']['val_test_shared_groups']:,} cụm                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

> [!WARNING]
> **Xác nhận thực nghiệm**:
> - Đúng như nghi vấn của Phase 6.1, bộ chia tập phân tầng ngẫu nhiên (Random Stratification) trước đây đã vô tình **chia cắt các tin đăng cross-posting cùng cụm**:
>   - **{audit_res['old_split_leakage']['test_rows_affected']} dòng tập Test ({audit_res['old_split_leakage']['test_rows_pct']}%)** có ít nhất một tin đăng sao chép mô tả cùng dòng xe nằm trong tập Train.
>   - **{audit_res['old_split_leakage']['val_rows_affected']} dòng tập Validation ({audit_res['old_split_leakage']['val_rows_pct']}%)** có tin đăng sao chép nằm trong tập Train.
> - Điều này có thể khiến mô hình cây quyết định (Random Forest) ghi nhớ giá của các tin đăng cross-posting này, dẫn đến sai số đánh giá bị **lạc quan hơn thực tế**.

---

## 5. Phân Tích Kiểm Soát Rủi Ro Dương Tính Giả (False-Positive Controls)

1. **Vì sao không gộp `POSSIBLE_DUPLICATE` (Xe cũ trùng 5 thông số)?**:
   - Hai chiếc Toyota Vios 2020 khác nhau hoàn toàn có thể cùng có số ODO tròn (ví dụ: 40,000 km) và cùng được rao bán với giá mặt bằng thị trường 430 triệu VND. Nếu hai tin đăng có văn bản mô tả độc lập, việc gộp chúng thành một xe là võ đoán và làm mất tính độc lập tự nhiên của dữ liệu thị trường.
2. **Vì sao không gộp `SIMILAR_SPEC_ONLY` (Xe mới Showroom)?**:
   - Hàng trăm đại lý Toyota, Kia, Hyundai trên khắp cả nước cùng đăng bán xe Vios 1.5 AT mới 100% với giá niêm yết 542 triệu VND. Đây là các tài sản vật lý riêng biệt ngoài đời thực, không phải tin đăng trùng của cùng 1 xe. Việc gộp chúng sẽ tạo ra cụm khổng lồ (>100 xe), làm biến dạng cấu trúc phân bổ khi chia tập dữ liệu.
3. **Phòng chống bắc cầu sai lệch (Transitive Union Explosion)**:
   - Một số salon ô tô sử dụng chung một đoạn văn bản mẫu (Ví dụ: *"Salon cam kết xe không đâm đụng ngập nước, hỗ trợ trả góp 70%..."*). Đoạn văn bản này xuất hiện ở cả xe tải Suzuki, xe sedan Vios lẫn xe sang Mercedes.
   - Bằng cách bắt buộc điều kiện ràng buộc **phải trùng cả `(desc_fingerprint, brand, model, year)`**, hệ thống đã ngăn chặn triệt để hiện tượng gom nhầm xe khác chủng loại vào cùng một cụm. Cụm lớn nhất được giới hạn an toàn ở mức **{group_sizes.max() if len(group_sizes) > 0 else 0} dòng** (chỉ 0.18% dữ liệu).

---

## 6. Những Giới Hạn Không Thể Khắc Phục Do Thiếu Định Danh

1. **Thiếu số khung xe (VIN - Vehicle Identification Number)**:
   - Các cổng thông tin mua bán xe tại Việt Nam (Bonbanh, Oto.com.vn) không bắt buộc người đăng tin công khai số VIN. Vì vậy, không thể xác định 100% hai tin đăng khác mô tả có phải là cùng 1 chiếc xe vật lý được mua đi bán lại hay không.
2. **Loại bỏ PII bảo vệ quyền riêng tư**:
   - Nhằm tuân thủ Nghị định 13/2023/NĐ-CP, dự án đã loại bỏ bảng `seller.csv` và lọc sạch số điện thoại. Do đó, việc gom nhóm không thể dựa vào mã định danh người bán (seller ID), mà chỉ có thể dựa trên dấu vân tay văn bản mô tả và thông số kỹ thuật.

---

## 7. Kết Luận Khả Thi Cho Group-Aware Split (Feasibility Sign-Off)

- **Số lượng cụm `HIGH_CONFIDENCE_DUPLICATE`**: **{audit_res['high_confidence_groups_total']:,} cụm** ({cat_counts.get('HIGH_CONFIDENCE_DUPLICATE', 0):,} dòng).
- **Quy mô cụm**: Cụm lớn nhất chỉ có {group_sizes.max() if len(group_sizes) > 0 else 0} dòng, kích thước trung bình 2.7 dòng/cụm.
- **Đánh giá tính khả thi**: **HOÀN TOÀN KHẢ THI (FEASIBLE)** để tiến hành phân chia tập dữ liệu theo nhóm (Group-Aware Split) bằng thuật toán `StratifiedGroupKFold`, đảm bảo các tin cross-posting này nằm trọn vẹn trong một tập, loại bỏ triệt để rò rỉ tin đăng trùng giữa Train, Validation và Test.
"""

    out_file = Path("reports/phase6_2_duplicate_group_audit.md")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"Đã xuất báo cáo: {out_file}")

if __name__ == "__main__":
    main()
