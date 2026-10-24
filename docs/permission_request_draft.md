# Bản Nháp Thư Đề Xuất Sử Dụng Dữ Liệu Cho Mục Đích Học Thuật (Permission Request Draft)

- **Người soạn thảo**: Nhóm sinh viên thực hiện Mini Project & Cố vấn CLB AI
- **Đối tượng gửi dự kiến**: Ban quản lý / Bộ phận Hỗ trợ khách hàng - Công ty Cổ phần Nextgen Việt Nam (Đơn vị vận hành website Oto.com.vn)
- **Kênh tiếp nhận chính thức theo công bố trên website**: `hotro@oto.com.vn`
- **Trạng thái tài liệu**: **BẢN NHÁP NỘI BỘ (DRAFT ONLY — CHƯA GỬI)**
- **Mục đích**: Xin ý kiến và làm rõ khả năng cấp phép thu thập / trích xuất dữ liệu công khai cho đề tài nghiên cứu học thuật của sinh viên.

---

## 1. Tiêu Đề Email Dự Kiến (Subject)

`[Đề xuất Học thuật] Xin phép trích xuất mẫu dữ liệu tin đăng ô tô công khai phục vụ nghiên cứu mô hình Machine Learning phi thương mại của sinh viên CLB AI`

---

## 2. Nội Dung Thư Dự Kiến (Body)

**Kính gửi:** Ban Quản Trị & Bộ Phận Hỗ Trợ Kỹ Thuật - Website Oto.com.vn  
*(Công ty Cổ phần Nextgen Việt Nam)*,

Em tên là [Họ và Tên sinh viên đại diện nhóm], hiện là sinh viên chuyên ngành Trí tuệ Nhân tạo / Khoa học Dữ liệu và là thành viên thuộc Câu lạc bộ AI tại [Tên trường Đại học].

Hiện tại, nhóm chúng em đang thực hiện một đồ án nghiên cứu nhỏ (Mini Capstone Project) kết thúc khóa huấn luyện nội bộ với đề tài: **"Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam bằng các mô hình Machine Learning"** (Used Car Price Prediction in Vietnam), dưới sự cố vấn chuyên môn của các Giảng viên và Kỹ sư dữ liệu (Mentors).

Qua tìm hiểu, chúng em nhận thấy Oto.com.vn là nền tảng thông tin ô tô uy tín và có dữ liệu phân loại thị trường rất phong phú, chuẩn mực tại Việt Nam. Để có nguồn dữ liệu thực tế phục vụ quá trình học tập và đánh giá các thuật toán học máy (Machine Learning Pipeline), nhóm em xin phép được gửi thư này để kính đề xuất và xin ý kiến quý Công ty về việc trích xuất một mẫu dữ liệu công khai từ website.

### 1. Mục đích sử dụng dữ liệu
- Hoàn toàn phục vụ **mục đích học tập, thực hành và nghiên cứu khoa học phi thương mại** trong phạm vi đồ án của sinh viên.
- Toàn bộ kết quả (nếu có công bố) sẽ chỉ dùng để trình bày báo cáo kỹ thuật nội bộ trước Hội đồng phản biện và Câu lạc bộ, tuyệt đối không sử dụng cho bất kỳ hoạt động kinh doanh, thương mại hay chuyển giao cho bên thứ ba.

### 2. Phạm vi và các trường dữ liệu đề xuất thu thập
Nếu được quý Công ty cho phép, nhóm chỉ mong muốn trích xuất các thông số kỹ thuật xe được hiển thị công khai bao gồm:
- Mức giá rao bán niêm yết (để làm biến mục tiêu hồi quy).
- Hãng sản xuất (Brand), Dòng xe (Model), Năm sản xuất (Year).
- Số kilomet đã vận hành (ODO / Mileage).
- Loại hộp số, Loại nhiên liệu, Kiểu dáng xe, Xuất xứ (Trong nước / Nhập khẩu).
- Khu vực địa lý ở mức Tỉnh/Thành phố (ví dụ: Hà Nội, TP.HCM).

> [!IMPORTANT]
> **Cam kết về dữ liệu cá nhân (PII)**:
> Nhóm chúng em **TUYỆT ĐỐI KHÔNG THU THẬP, KHÔNG LƯU TRỮ VÀ KHÔNG SỬ DỤNG** bất kỳ thông tin cá nhân nào của người đăng tin (bao gồm: Tên cá nhân, Số điện thoại người bán, Địa chỉ liên hệ chi tiết). Chúng em cam kết tuân thủ nghiêm ngặt Nghị định 13/2023/NĐ-CP về bảo vệ dữ liệu cá nhân.

### 3. Quy mô dự kiến và cam kết kỹ thuật
- **Giai đoạn thử nghiệm (Pilot)**: Nhóm chỉ dự kiến thu thập một mẫu nhỏ từ **30 đến 50 bản ghi** để kiểm tra tính tương thích của mã nguồn xử lý.
- **Quy mô mở rộng (nếu được phép)**: Dự kiến tối đa khoảng **1.000 bản ghi** hợp lệ.
- **Cam kết tài nguyên máy chủ**: Nhóm cam kết giới hạn tần suất truy vấn ở mức rất thấp (độ trễ tối thiểu 2 – 3 giây giữa các lượt truy cập, thực hiện đơn luồng, chạy vào các khung giờ thấp điểm) nhằm đảm bảo không gây bất kỳ ảnh hưởng nào đến hiệu năng máy chủ và trải nghiệm của người dùng trên website.
- **Trích dẫn và lưu trữ**: Luôn trích dẫn rõ ràng nguồn gốc dữ liệu từ Oto.com.vn và sẵn sàng xóa bỏ tập dữ liệu thô ngay khi đồ án học tập kết thúc theo yêu cầu của quý Công ty.

### 4. Đề nghị từ phía nhóm nghiên cứu
Nhóm chúng em kính mong nhận được phản hồi và hướng dẫn từ quý Ban Quản trị:
1. Việc trích xuất mẫu dữ liệu công khai với quy mô nhỏ như trên cho mục đích nghiên cứu học tập có được quý Công ty chấp thuận hay không?
2. Quý Công ty có sẵn cổng kết nối API phục vụ nghiên cứu, tập dữ liệu mẫu (Open Dataset), hoặc thỏa thuận học thuật nào phù hợp hơn cho sinh viên có thể tiếp cận hay không?
3. Các quy định, giới hạn hoặc yêu cầu cụ thể nào mà nhóm cần tuân thủ thêm trong quá trình thực hiện đồ án.

Nếu quý Công ty cần thêm thông tin chi tiết về đề cương nghiên cứu hoặc thư xác nhận từ phía Nhà trường / Câu lạc bộ AI, chúng em xin sẵn sàng cung cấp đầy đủ.

Chúng em xin chân thành cảm ơn sự quan tâm, hỗ trợ và đồng hành của Quý Công ty đối với cộng đồng học sinh, sinh viên nghiên cứu AI tại Việt Nam!

Kính chúc Quý Công ty và Ban Quản trị Oto.com.vn ngày càng phát triển vững mạnh.

Trân trọng,  
**Đại diện Nhóm Nghiên cứu Sinh viên**  
[Họ và tên sinh viên]  
Số điện thoại: [Số điện thoại liên hệ]  
Email: [Email sinh viên / trường đại học]  
Câu lạc bộ Trí tuệ Nhân tạo (AI Club) - [Tên Trường Đại học]
