# Báo Cáo Quyết Định Phạm Vi Nghiên Cứu (Cohort Scope Decision Report)
*(Phase 5 — Project Scope Reconciliation & Cohort Decision)*

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam (Used Car Price Prediction in Vietnam)
- **Giai đoạn**: Phase 5 — Data Cleaning, Feature Engineering & Preprocessing Pipeline
- **Thời gian lập**: 19/10/2026, 02:50:00 (Múi giờ: Asia/Ho_Chi_Minh)
- **Người thực hiện**: Senior Data Scientist, ML Engineer & AI Student
- **Tài liệu đối chiếu**: [Project Charter](file:///d:/ai-club-end-training/docs/project_charter.md), [Data Cleaning Policy](file:///d:/ai-club-end-training/docs/eda_findings_and_cleaning_policy.md), [EDA Report](file:///d:/ai-club-end-training/reports/phase4_eda_report.md)

---

## 1. Bối Cảnh Đối Chiếu Phạm Vi (Scope Reconciliation Context)

1. **Quy định trong Điều lệ dự án (Project Charter Section 3.1)**:
   > *"Phạm vi năm sản xuất dự kiến: 2015 – 2025 (nhằm đảm bảo tính đại diện và hạn chế xe quá cũ có mức độ hao mòn cơ khí khó kiểm chứng)."*
2. **Đề xuất trong Báo cáo EDA (Phase 4)**:
   > *"Mở rộng giữ lại các xe có năm sản xuất $\ge 2010$ để tận dụng 27,229 bản ghi (88.83% dữ liệu)."*
3. **Nguyên tắc kỹ thuật Phase 5**:
   Không tự ý thay đổi phạm vi đã được Mentor và Hội đồng phê duyệt trong Project Charter. Nhóm thực hiện so sánh đối chứng thực nghiệm giữa 2 Cohorts để đưa ra quyết định có căn cứ khoa học.

---

## 2. Bảng So Sánh Đối Chứng Thực Nghiệm Định Lượng (Empirical Cohort Comparison)

Dữ liệu được trích xuất trực tiếp từ [car_detail.csv](file:///d:/ai-club-end-training/data/raw/external/mquaan_car_price/car_detail.csv) (30,652 dòng thô, năm nhỏ nhất: 1990, lớn nhất: 2023, thiếu năm: 32 dòng):

| Chỉ số kỹ thuật & Nghiệp vụ | **Cohort A (Năm $\ge 2015$)**<br>*(Phạm vi chuẩn Project Charter)* | **Cohort B (Năm $\ge 2010$)**<br>*(Phạm vi mở rộng theo EDA)* | Mức độ chênh lệch (Giai đoạn 2010 - 2014) |
| :--- | :---: | :---: | :---: |
| **Số lượng bản ghi thô (Raw)** | **23,524 dòng** (76.75% raw) | **27,317 dòng** (89.12% raw) | +3,793 dòng (+12.37%) |
| **Số lượng bản ghi sạch (Clean)** | **23,510 dòng** (76.70% raw) | **27,299 dòng** (89.06% raw) | +3,789 dòng (+12.36%) |
| **Bản ghi loại do lỗi dữ liệu thật** | 14 dòng (1 giá <30M, 13 hộp số bất thường) | 18 dòng (1 giá <30M, 17 hộp số bất thường) | Phân lập chính xác theo từng bước lọc |
| **Bản ghi loại do ngoài Scope** | **7,115 dòng** (23.21% raw sau lọc giá) | **3,322 dòng** (10.84% raw sau lọc giá) | 3,793 xe đời 2010–2014 |
| **Giá nhỏ nhất (Min Price)** | 72,000,000 VND | 33,000,000 VND | Xe đời 2010 có giá sàn thấp hơn |
| **Phân vị 25% (Q1 Price)** | 520,000,000 VND | 470,000,000 VND | -50,000,000 VND |
| **Trung vị giá (Median Price)** | **719,000,000 VND** | **669,000,000 VND** | -50,000,000 VND |
| **Giá trung bình (Mean Price)** | 1,390,000,000 VND | 1,291,000,000 VND | -99,000,000 VND |
| **Phân vị 75% (Q3 Price)** | 1,209,000,000 VND | 1,130,000,000 VND | -79,000,000 VND |
| **Độ lệch chuẩn (Std Dev)** | 2,237,000,000 VND | 2,138,000,000 VND | Phân tán giá tương đồng |
| **Tỷ lệ Xe đã qua sử dụng** | 74.18% (17,440 xe) | 77.76% (21,229 xe) | +3.58% xe cũ |
| **Tỷ lệ Xe mới tại Showroom** | 25.82% (6,070 xe) | 22.24% (6,070 xe) | Xe mới 100% giữ nguyên số lượng |
| **Cơ cấu Top 5 hãng xe** | Toyota (16.2%), Hyundai (12.5%), Ford (11.8%), Mercedes (11.8%), Kia (9.1%) | Toyota (17.2%), Hyundai (12.0%), Ford (11.5%), Mercedes (11.1%), Kia (9.8%) | Cơ cấu thị phần hãng xe gần như giữ nguyên tuyệt đối |

---

## 3. Đánh Giá Tác Động Nghiệp Vụ & Rủi Ro Mô Hình

1. **Về quy mô mẫu huấn luyện**:
   - Mục tiêu ban đầu trong Project Charter (Mục 2.1) là hướng tới quy mô **~1.000 bản ghi**.
   - Cả hai Cohort đều vượt xa ngưỡng tối thiểu này: Cohort A đạt **23,472 bản ghi (vượt gấp 23 lần)**; Cohort B đạt **27,229 bản ghi (vượt gấp 27 lần)**. Do đó, việc tuân thủ Charter không gây bất kỳ sự thiếu hụt dữ liệu nào cho mô hình học máy.
2. **Về độ tin cậy của hao mòn cơ khí và ODO**:
   - Xe đời 2010–2014 (10–14 năm tuổi) tại Việt Nam thường đã qua nhiều đời chủ, tỷ lệ bị tua số công-tơ-mét (ODO tampering) hoặc đại tu động cơ cao hơn, dẫn đến độ phân tán giá lớn hơn quanh cùng một mức ODO.
   - Xe đời 2015–2023 (dưới 9 năm tuổi) có hồ sơ lịch sử bảo dưỡng và thanh khoản thị trường minh bạch hơn, phù hợp với giả định khấu hao của bài toán định giá đại chúng.
3. **Về phân phối biến mục tiêu**:
   - Tỷ trọng các hãng xe dẫn đầu giữa hai Cohort chênh lệch chưa tới 1%.
   - Trung vị giá của Cohort A (719 triệu) cao hơn Cohort B (669 triệu) do không chứa các xe đời sâu giá rẻ (30M - 200M).

---

## 4. Quyết Định Thống Nhất Phạm Vi & Thiết Kế Kiến Trúc (Architecture Decision)

Tuân thủ nguyên tắc chỉ đạo: *"Nếu không có quyết định mới từ mentor, lựa chọn cohort chính dựa trên charter đã được phê duyệt; cohort còn lại có thể được giữ như một phân tích độ nhạy."*

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       QUYẾT ĐỊNH PHẠM VI DỮ LIỆU PHASE 5                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. COHORT CHÍNH (PRIMARY MODELING COHORT):                                  │
│    - Tiêu chí: Năm sản xuất từ 2015 đến 2023 (year >= 2015).                │
│    - Quy mô chuẩn: 23,510 bản ghi sạch (76.70% dữ liệu raw).                │
│    - Căn cứ: Tuân thủ 100% phạm vi đã cam kết trong Project Charter.        │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. COHORT MỞ RỘNG (EXTENDED SENSITIVITY COHORT):                            │
│    - Tiêu chí: Năm sản xuất từ 2010 đến 2023 (year >= 2010).                │
│    - Quy mô chuẩn: 27,299 bản ghi sạch (89.06% dữ liệu raw).                │
│    - Mục đích: Dùng trong Phase 6 để kiểm tra độ nhạy (Sensitivity Analysis) │
│      và đánh giá năng lực suy luận của mô hình trên xe đời sâu.            │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. THIẾT KẾ MÃ NGUỒN PIPELINE:                                              │
│    - Module `src/data/cleaning.py` và `prepare_modeling_data.py` cung cấp    │
│      tham số `min_year=2015` mặc định (Primary), nhưng hỗ trợ tham số       │
│      `min_year=2010` linh hoạt cho phân tích độ nhạy.                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

> [!NOTE]
> **Phân định dứt khoát**:
> 7,128 bản ghi không thuộc Cohort A **không phải là dữ liệu sai**. Chúng chỉ được phân loại là **`OUT_OF_STUDY_SCOPE`** nhằm phục vụ đúng câu hỏi nghiên cứu của đồ án.
