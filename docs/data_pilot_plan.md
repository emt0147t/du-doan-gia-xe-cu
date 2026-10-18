# Kế Hoạch Thử Nghiệm Thu Thập Dữ Liệu Nhỏ (Data Pilot Plan)

- **Quy mô dự kiến**: 30 – 50 tin đăng rao bán xe ô tô đã qua sử dụng
- **Nguồn khảo sát**: Oto.com.vn
- **Giai đoạn**: Phase 1 — Small-scale Data Pilot (Chỉ thực hiện sau khi có sự đồng thuận từ Mentor)
- **Tài liệu tham chiếu**: [Data Source Audit](file:///d:/ai-club-end-training/docs/data_source_audit.md), [Data Dictionary](file:///d:/ai-club-end-training/docs/data_dictionary.md)

---

## 1. Phương Pháp Lấy Mẫu Tránh Lệch Phân Khúc (Stratified / Multi-page Sampling)

### 1.1. Vấn đề lệch mẫu trên sàn rao vặt
Nếu crawler chỉ lấy 2–3 trang đầu tiên của mục "Mua bán xe cũ", dữ liệu sẽ bị lệch nghiêm trọng:
- Toàn bộ là xe "VIP" (các gói quảng cáo V5, V3) thường do các salon xe cũ lớn đăng bán.
- Thiên vị mạnh về các phân khúc xe sang hoặc xe phổ thông bán chạy tại 2 đô thị lớn (Hà Nội, TP.HCM).
- Thiếu vắng các dòng xe từ người bán cá nhân hoặc các tỉnh thành khác.

### 1.2. Chiến lược lấy mẫu đề xuất cho Pilot (30 – 50 bản ghi)
Lấy mẫu trải đều qua 3 lát cắt chính:
1. **Lấy mẫu theo phân trang có bước nhảy (Jump-paging)**:
   - Thay vì lấy liên tiếp trang 1, 2, 3, crawler sẽ lấy 10–15 tin từ Trang 1, 10–15 tin từ Trang 5, 10–15 tin từ Trang 15, và 10 tin từ Trang 25.
2. **Lấy mẫu theo danh mục thương hiệu đa dạng**:
   - Nhóm xe phổ thông Nhật - Hàn (Toyota, Hyundai, Kia, Mazda, Honda): chiếm ~50% mẫu.
   - Nhóm xe phổ thông Mỹ/châu Âu (Ford): chiếm ~20% mẫu.
   - Nhóm xe cao cấp / hạng sang (Mercedes-Benz, BMW, Lexus, Audi): chiếm ~20% mẫu.
   - Nhóm xe điện / thương hiệu Việt (VinFast): chiếm ~10% mẫu.
3. **Phân bổ địa lý**: Không tập trung 100% tại Hà Nội; phân bổ tối thiểu 30% tại miền Nam (TP.HCM, Đồng Nai, Bình Dương) và các tỉnh thành khác.

---

## 2. Quy Trình Kiểm Tra Các Trường Dữ Liệu (Field Inspection Pipeline)

Quy trình kiểm tra trên từng bản ghi thô được thực hiện tuần tự qua các bước:

```text
[Raw HTML Card] 
       │
       ▼
[Extraction Check] ──► Kiểm tra xem thẻ HTML/thuộc tính metadata có tồn tại?
       │
       ▼
[Type & Pattern Check] ──► Kiểm tra regex số km, năm sản xuất, đơn vị giá
       │
       ▼
[Normalization Check] ──► Thử nghiệm hàm parse giá sang VND, làm sạch text
       │
       ▼
[PII Scrubbing Check] ──► Xác minh không có số điện thoại / tên người bán lọt vào
```

---

## 3. Cơ Chế Phát Hiện Bản Ghi Thiếu, Trùng Lặp & Sai Định Dạng

### 3.1. Phát hiện trùng lặp (Deduplication)
- **Cấp độ 1 (Technical Duplicate)**: So sánh trường `listing_id` (trích xuất từ `data-autoid`). Nếu xuất hiện 2 bản ghi có cùng `listing_id`, loại bỏ ngay lập tức ở tầng thu thập.
- **Cấp độ 2 (Semantic / Physical Duplicate)**: Tìm kiếm các bản ghi có sự trùng khớp toàn bộ: `brand`, `model`, `year`, `mileage_km`, `transmission`, `fuel_type`, `location_province` và độ chênh lệch giá < 2%. Đây là dấu hiệu cùng một chiếc xe được đăng nhiều lần bởi các tài khoản khác nhau.

### 3.2. Phát hiện dữ liệu thiếu (Missingness Check)
- Đếm số lượng giá trị `NULL`, rỗng (`""`), hoặc `NA` trên từng cột.
- Phân biệt 2 cấp độ:
  - **Trường cốt lõi bắt buộc (Mandatory)**: `price_vnd`, `brand`, `model`, `year`. Nếu thiếu -> Bản ghi không thể dùng cho hồi quy có giám sát.
  - **Trường bổ trợ (Auxiliary / Optional)**: `mileage_km`, `body_type`, `transmission`, `origin`, `fuel_type`.
  - **Trường provisional**: `seats`.

### 3.3. Phát hiện sai định dạng (Format & Schema Validation)
- Regex kiểm tra định dạng năm: `^(19|20)\d{2}$`.
- Regex kiểm tra số km: định dạng chuỗi số có dấu chấm và đơn vị km (vd: `^\d{1,3}(\.\d{3})*\s*km$`).
- Regex kiểm tra giá: chứa các từ khóa định lượng "triệu", "tỉ", "tỷ", hoặc "thỏa thuận".

---

## 4. Thuật Toán Chuẩn Hóa Đơn Vị Giá (`price_vnd`) Không Sai Lệch

### 4.1. Bản chất vấn đề
Chuỗi giá từ website Việt Nam rất đa dạng:
- Dạng 1 đơn vị triệu: `"899 triệu"` -> $899 \times 10^6 = 899.000.000$ VND.
- Dạng 1 đơn vị tỷ: `"2 tỉ"` hoặc `"2 tỷ"` -> $2 \times 10^9 = 2.000.000.000$ VND.
- Dạng hỗn hợp tỷ và triệu: `"1 tỉ 169 triệu"` -> $1 \times 10^9 + 169 \times 10^6 = 1.169.000.000$ VND.
- Dạng số thập phân: `"1.2 tỉ"`, `"1,2 tỷ"` -> $1.2 \times 10^9 = 1.200.000.000$ VND.
- Dạng không định lượng: `"Thỏa thuận"`, `"Giá liên hệ"`, `""` -> Không có giá trị số (Missing / Non-target).

### 4.2. Đặc tả thuật toán Parser (Được hiện thực hóa trong Python)
```python
import re
from typing import Optional

def parse_vietnamese_price_to_vnd(price_str: str) -> Optional[int]:
    """
    Chuẩn hóa chuỗi giá tiếng Việt sang số nguyên VND (đồng).
    Trả về None nếu giá trị không hợp lệ hoặc ở dạng thỏa thuận.
    """
    if not price_str or not isinstance(price_str, str):
        return None
        
    s = price_str.lower().strip()
    if "thỏa thuận" in s or "liên hệ" in s or "thuong luong" in s:
        return None
        
    # Chuẩn hóa từ vựng: thay 'tỉ' thành 'tỷ', dấu phẩy thập phân thành dấu chấm
    s = s.replace("tỉ", "tỷ").replace(",", ".")
    
    total_vnd = 0.0
    matched = False
    
    # 1. Bóc tách phần tỷ
    ty_match = re.search(r'([\d\.]+)\s*tỷ', s)
    if ty_match:
        try:
            val_ty = float(ty_match.group(1))
            total_vnd += val_ty * 1_000_000_000
            matched = True
        except ValueError:
            return None
            
    # 2. Bóc tách phần triệu
    trieu_match = re.search(r'([\d\.]+)\s*triệu', s)
    if trieu_match:
        try:
            val_trieu = float(trieu_match.group(1))
            total_vnd += val_trieu * 1_000_000
            matched = True
        except ValueError:
            return None
            
    if not matched or total_vnd <= 0:
        return None
        
    return int(round(total_vnd))
```

### 4.3. Kiểm thử đơn vị (Unit Test) cho Parser
Bộ test case tối thiểu bắt buộc:
- `"899 triệu"` -> `899000000`
- `"1 tỉ 169 triệu"` -> `1169000000`
- `"2.5 tỷ"` -> `2500000000`
- `"Giá thỏa thuận"` -> `None`
- `""` -> `None`

---

## 5. Thống Kê Đánh Giá Chất Lượng Mẫu Pilot (Data Quality Metrics)

Sau khi thu thập 30–50 bản ghi mẫu, chạy bảng thống kê tổng hợp:
1. **Tỷ lệ hoàn chỉnh trường (Completeness Rate)** trên từng cột:
   $$\text{Completeness}_j = \frac{\sum_{i=1}^N \mathbb{I}(x_{ij} \text{ hợp lệ})}{N} \times 100\%$$
2. **Tỷ lệ Target hợp lệ**: Tỷ lệ tin đăng có `price_vnd` chuyển đổi thành công sang số nguyên dương.
3. **Tỷ lệ trùng lặp (Duplicate Rate)**: Số `listing_id` trùng lặp chia cho tổng số tin quét.
4. **Phân phối thống kê mô tả sơ bộ**:
   - Giá (`price_vnd`): Min, Median, Mean, Max, IQR.
   - Năm (`year`): Min, Max, phân phối các năm.
   - ODO (`mileage_km`): Min, Median, Max.

---

## 6. Tiêu Chí Tiếp Tục, Điều Chỉnh Hoặc Dừng Nguồn (Đề Xuất Để Thảo Luận Với Mentor)

> [!IMPORTANT]
> Các tỷ lệ dưới đây là **ngưỡng đề xuất kỹ thuật** từ góc độ Data Science để nhóm và Mentor xem xét, không phải quy định cứng nhắc.

| Quyết định | Điều kiện đề xuất xem xét | Hành động tương ứng |
| :--- | :--- | :--- |
| **TIẾP TỤC (Proceed to Full Crawl)** | - Tỷ lệ hợp lệ của `price_vnd` > 95%<br>- Tỷ lệ đầy đủ của các biến cốt lõi (`brand`, `model`, `year`, `mileage`) > 85%<br>- Website phản hồi ổn định với rate limit 2s/req, không phát sinh CAPTCHA/WAF block | Thiết kế pipeline thu thập mở rộng (~1.000 bản ghi) theo batch an toàn. |
| **ĐIỀU CHỈNH (Adjust Pipeline / Schema)** | - Trường `seats` bị missing > 80% (đã dự báo trước)<br>- Xuất hiện các biến thể giá mới chưa parse được (chiếm 5–15%)<br>- Phân bổ hãng xe bị lệch quá mức về 1 thương hiệu | Điều chỉnh bộ Parser Regex; chuyển `seats` thành biến phái sinh hoặc loại khỏi mô hình cơ sở; bổ sung lọc theo chuyên mục hãng xe. |
| **DỪNG NGUỒN (Stop & Pivot to Backup Source)** | - Website áp dụng cơ chế chặn IP (HTTP 403 / 429 liên tục, Cloudflare Turnstile, CAPTCHA)<br>- Tỷ lệ tin đăng "Giá thỏa thuận" chiếm > 30% mẫu<br>- Phát hiện vi phạm bản quyền dữ liệu nghiêm ngặt từ đơn vị quản lý | Dừng thu thập ngay lập tức; chuyển sang phương án dữ liệu thay thế (Secondary Open Dataset từ Kaggle hoặc API học thuật). |

---

## 7. Các Tạo Tác (Artifacts) Cần Lưu Để Đảm Bảo Tính Tái Hiện (Reproducibility)

Để quy trình pilot có thể kiểm chứng độc lập bởi Mentor:
1. **Raw Pilot Dump**: Lưu tệp `data/raw/pilot_sample_raw.json` chứa các bản ghi JSON trích xuất nguyên trạng từ HTML (đã lược bỏ số điện thoại/tên người bán).
2. **Audit Report Log**: Tệp `reports/pilot_quality_summary.md` chứa bảng thống kê tỷ lệ missing, bảng phân phối min/median/max và danh sách các lỗi parser gặp phải.
3. **Pilot Script**: Script độc lập `src/data/pilot_sampler.py` có khả năng chạy lại với seed và danh sách URL kiểm tra rõ ràng.
