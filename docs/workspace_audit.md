# Báo Cáo Kiểm Tra Workspace (Workspace Audit)

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam (Used Car Price Prediction in Vietnam)
- **Thời gian thực hiện**: 18/10/2026, 15:10:39 (Múi giờ: Asia/Ho_Chi_Minh)
- **Người thực hiện**: Senior Data Scientist, ML Engineer & Python Mentor
- **Đối tượng thụ hưởng**: Sinh viên thành viên AI Club

---

## 1. Thông Tin Chung Về Môi Trường

| Tiêu chí | Trạng thái ghi nhận thực tế | Ghi chú kỹ thuật |
| :--- | :--- | :--- |
| **Thư mục Root** | `D:\ai-club-end-training` | Ổ đĩa D:, hệ điều hành Windows 11 / Windows Server |
| **Trạng thái ban đầu** | Thư mục rỗng hoàn toàn (0 file, 0 thư mục) | Không phát hiện mã nguồn cũ hoặc tệp rác |
| **Hệ thống Git** | Chưa khởi tạo (Not a git repository) | Git binary có sẵn trên máy: version `2.45.1.windows.1` |
| **Python Runtime** | `Python 3.11.9` tại `C:\Users\DELL\AppData\Local\Programs\Python\Python311\python.exe` | Đạt chuẩn cho toàn bộ stack Scikit-learn, Pandas, Requests |
| **Các Python khác trên PATH** | Python 3.14, Python 3.13, MSYS64 Python | Cần chỉ định tường minh Python 3.11 để tránh xung đột phiên bản |
| **Môi trường ảo (Virtualenv)** | Chưa khởi tạo môi trường ảo chuyên biệt trong workspace | Chưa có `.venv` cục bộ |

---

## 2. Kiểm Tra Các Thành Phần Hiện Hữu & Khả Năng Tái Sử Dụng

1. **Mã nguồn và dữ liệu có sẵn**:
   - Không có file code, file cấu hình hoặc dữ liệu nào tồn tại trước thời điểm audit.
   - Lợi thế: Tránh được nguy cơ xung đột mã nguồn (code conflicts), dữ liệu bẩn (dirty cache) hoặc cấu hình sai lệch từ các lần chạy trước.
2. **Công cụ dòng lệnh hệ thống**:
   - `git` version `2.45.1.windows.1` hoạt động bình thường qua PowerShell.
   - Trình thông dịch `python` mặc định trỏ tới Python 3.11.9, tương thích hoàn toàn với hệ sinh thái Data Science hiện đại.

---

## 3. Các Quyết Định Kỹ Thuật Khi Thiết Lập Workspace

Theo nguyên tắc cố vấn (Mentorship Guidelines), mọi quyết định thiết lập đều được phân tích theo 6 câu hỏi cốt lõi:

### 3.1. Quyết định khởi tạo Git và xây dựng `.gitignore` chặt chẽ

1. **Chúng ta đang giải quyết vấn đề gì?**
   - Quản lý phiên bản mã nguồn, tài liệu dự án và ngăn ngừa việc vô tình commit dữ liệu thô (raw data), dữ liệu định danh cá nhân (PII), tệp mô hình dung lượng lớn hoặc môi trường ảo lên repository.
2. **Vì sao cần giải quyết vấn đề đó?**
   - Trong các dự án Data Science & ML, dữ liệu crawl hoặc preprocessed data có thể nặng hàng chục MB đến hàng GB, nếu commit vào Git tree sẽ làm phình repository, gây chậm chạp và đặc biệt có thể làm lộ thông tin cá nhân (vi phạm quy định bảo mật dữ liệu).
3. **Có những lựa chọn nào?**
   - *Lựa chọn 1*: Không dùng Git, chỉ lưu file cục bộ.
   - *Lựa chọn 2*: Dùng Git nhưng không có `.gitignore`, commit toàn bộ.
   - *Lựa chọn 3 (Được chọn)*: Khởi tạo Git repository và cấu hình `.gitignore` chuẩn quy định rõ loại trừ `.venv`, `data/raw/*`, `data/processed/*`, `.ipynb_checkpoints`, credentials.
4. **Vì sao lựa chọn hiện tại hợp lý?**
   - Đảm bảo tính chuyên nghiệp, khả năng truy vết lịch sử thay đổi (version control) nhưng vẫn bảo vệ an toàn cho repository bằng các quy tắc `.gitignore` nghiêm ngặt.
5. **Rủi ro hoặc hạn chế của lựa chọn này là gì?**
   - Khi cộng tác nhiều người hoặc chuyển máy, dữ liệu không nằm trong Git nên cần quy trình tài liệu hóa (data pipeline / pilot plan) rõ ràng để tái hiện dữ liệu.
6. **Mentor có thể hỏi gì về quyết định đó?**
   - *"Tại sao trong thư mục `data/raw/` chỉ có file `.gitkeep` mà không đẩy trực tiếp file CSV đã tải lên Git?"*
   - *Trả lời*: Dữ liệu thô và dữ liệu lớn thuộc danh mục không phiên bản hóa bằng Git thông thường (Git LFS hoặc script thu thập độc lập được ưu tiên). Ngoài ra, raw data có thể chứa các trường nhạy cảm chưa được làm sạch, việc không đưa vào Git là tuân thủ Data Governance và bảo mật.

---

## 4. Các Vấn Đề Cần Xử Lý Trước Khi Sang Phase 1

1. **Khởi tạo Virtual Environment (`.venv`)**:
   - Cần tạo môi trường ảo độc lập bằng lệnh `python -m venv .venv` trước khi cài đặt các thư viện trong `requirements.txt`.
   - Lưu ý kích hoạt venv bằng `.\.venv\Scripts\Activate.ps1`.
2. **Cấu hình Encoding UTF-8 trên môi trường Windows**:
   - PowerShell và CMD trên Windows mặc định sử dụng code page CP1252 hoặc CP437, dễ gây lỗi font `UnicodeEncodeError` khi làm việc với tiếng Việt (ví dụ khi parse văn bản từ website tiếng Việt).
   - Cần đảm bảo các script Python thiết lập `sys.stdout.reconfigure(encoding='utf-8')` hoặc đặt biến môi trường `PYTHONIOENCODING=utf-8`.

---

## 5. Kết Luận Kiểm Tra Workspace

- Workspace đã sẵn sàng ở trạng thái chuẩn mực, sạch sẽ, không có file thừa hoặc mã nguồn lỗi thời.
- Cấu trúc thư mục nền tảng được định hình theo chuẩn dự án Machine Learning thực tế.
