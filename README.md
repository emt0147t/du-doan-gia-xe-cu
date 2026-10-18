# Used Car Price Prediction in Vietnam: An End-to-End Machine Learning Project

> **Dự án cuối khóa đào tạo AI Club**  
> **Bài toán**: Hồi quy có giám sát (Supervised Regression) nhằm dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam (`price_vnd`).  
> **Trạng thái hiện tại**: **Phase 0 — Project Definition & Data Source Feasibility (ĐÃ HOÀN THÀNH)**  
> **Quyết định nguồn dữ liệu ban đầu**: **CONDITIONAL GO** (Chấp thuận thử nghiệm có điều kiện trên Oto.com.vn)

---

## 1. Giới Thiệu Dự Án

Dự án này được thiết kế và thực hiện bởi thành viên Câu lạc bộ AI dưới sự hướng dẫn phương pháp luận của Senior Data Scientist & ML Engineer Mentor. Toàn bộ quy trình tuân thủ nghiêm ngặt chuẩn mực công nghiệp và nghiên cứu khoa học:
- **Tính chính xác & trung thực**: Không bịa đặt số liệu, không sinh dữ liệu giả mạo (no fake CSVs/metrics), mọi nhận định kỹ thuật đều đi kèm bằng chứng có thể kiểm chứng.
- **Đạo đức dữ liệu (Data Ethics)**: Tuân thủ quy định `robots.txt`, điều khoản hoạt động sàn, tuyệt đối không thu thập thông tin định danh cá nhân (PII như số điện thoại, tên người bán) và giới hạn tải truy vấn lên máy chủ nguồn.
- **Khả năng giải trình (Explainability)**: Từng quyết định kỹ thuật từ thiết kế schema, tiền xử lý, lựa chọn mô hình đến phân tích sai số đều được lập luận rõ ràng.

---

## 2. Cấu Trúc Thư Mục Dự Án (Project Structure)

```text
ai-club-end-training/
├── .gitignore                     # Cấu hình loại trừ Git (dữ liệu thô, venv, cache)
├── requirements.txt               # Danh sách thư viện Python tinh gọn, đúng nhu cầu
├── README.md                      # Tài liệu tổng quan dự án
├── docs/                          # Hệ thống tài liệu kỹ thuật dự án
│   ├── workspace_audit.md         # Báo cáo kiểm tra môi trường workspace & công cụ
│   ├── data_source_audit.md       # Báo cáo đánh giá tính khả thi nguồn dữ liệu Oto.com.vn
│   ├── project_charter.md         # Điều lệ dự án (Problem, Scope, Research Questions, DoD)
│   ├── data_dictionary.md         # Từ điển dữ liệu & đặc tả schema 14 trường
│   └── data_pilot_plan.md         # Kế hoạch thử nghiệm thu thập mẫu nhỏ (30-50 tin)
├── data/
│   ├── raw/                       # Chứa dữ liệu thô (được ignore trên Git)
│   └── processed/                 # Chứa dữ liệu sạch sau xử lý (được ignore trên Git)
├── notebooks/                     # Jupyter Notebooks nghiên cứu (EDA, Modeling)
├── src/                           # Module mã nguồn Python tái sử dụng
│   ├── __init__.py
│   ├── data/                      # Scripts thu thập & kiểm tra dữ liệu
│   ├── features/                  # Pipeline tiền xử lý & biến đổi đặc trưng
│   └── models/                    # Huấn luyện & đánh giá mô hình
├── reports/                       # Báo cáo kỹ thuật và hình ảnh
│   └── figures/                   # Biểu đồ EDA, phân tích phần dư, feature importance
└── tests/                         # Unit tests kiểm thử code (parser, feature transformer)
    └── __init__.py
```

---

## 3. Tóm Tắt Kết Quả Phase 0 (Phase 0 Key Findings)

1. **Workspace Audit**:
   - Môi trường Windows, Python 3.11.9 đạt chuẩn. Đã khởi tạo Git repository và cấu hình `.gitignore` chuẩn Data Science.
2. **Khảo sát nguồn dữ liệu (Oto.com.vn)**:
   - **Kỹ thuật**: Hệ thống hiển thị Server-Side Rendering (SSR). Thuộc tính thẻ tin đăng (`data-call`, `data-tinrao`, `data-autoid`) cung cấp 10/11 trường nghiệp vụ cốt lõi mà không cần cào sâu vào trang chi tiết.
   - **Trường dữ liệu**: Xác minh rõ ràng 10 trường (`price_vnd`, `brand`, `model`, `year`, `mileage_km`, `fuel_type`, `transmission`, `location_province`, `body_type`, `origin`). Trường `seats` (số chỗ) **không có trong bảng thông số chuẩn**, đã được đưa vào diện `Provisional` cần suy diễn từ dòng xe.
   - **Pháp lý & Đạo đức**: Điều khoản sàn giao dịch bảo lưu bản quyền nội dung. Website thu thập PII người bán để phục vụ liên hệ.
   - **Quyết định nguồn**: **CONDITIONAL GO** — Chỉ cho phép pilot mẫu nhỏ (30–50 tin) với tốc độ chậm (delay 2s), loại bỏ triệt để PII, và phải được Mentor duyệt trước khi mở rộng quy mô.

---

## 4. Hướng Dẫn Cài Đặt Môi Trường (Setup Guide)

Khi bước vào Phase 1, các bước thiết lập môi trường ảo được thực hiện như sau:

```powershell
# 1. Di chuyển vào thư mục dự án
cd D:\ai-club-end-training

# 2. Khởi tạo môi trường ảo Python 3.11
python -m venv .venv

# 3. Kích hoạt môi trường ảo (PowerShell)
.\.venv\Scripts\Activate.ps1

# 4. Cài đặt các gói phụ thuộc
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 5. Lộ Trình & Bước Tiếp Theo (Next Steps)

Theo [Project Charter](file:///d:/ai-club-end-training/docs/project_charter.md), dự án sẽ tiến hành theo lộ trình 10 bước:
- **Bước tiếp theo ngay lập tức (Phase 1 — Small-scale Data Pilot)**:
  1. Thảo luận và chốt các ngưỡng đánh giá Pilot với Mentor dựa trên [Data Pilot Plan](file:///d:/ai-club-end-training/docs/data_pilot_plan.md).
  2. Triển khai script `src/data/pilot_sampler.py` để lấy thử nghiệm 30–50 tin đăng trải đều các phân khúc.
  3. Kiểm chứng thực tế hàm parse giá `price_vnd` và tỷ lệ missing của các trường.
  4. Lập báo cáo chất lượng mẫu Pilot và trình Mentor phê duyệt quyết định tiếp tục thu thập hay chuyển hướng sang dataset thứ cấp.
