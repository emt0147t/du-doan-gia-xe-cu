# Báo Cáo Đánh Giá Khả Thi Nguồn Dữ Liệu (Data Source Feasibility Audit)

- **Nguồn dữ liệu khảo sát**: Oto.com.vn (Đơn vị chủ quản: Công ty Cổ phần Nextgen Việt Nam)
- **Thời gian thực hiện**: 18/10/2026, 15:10:39 (Múi giờ: Asia/Ho_Chi_Minh)
- **Người thực hiện**: Senior Data Scientist & ML Engineer Mentor
- **Mục đích**: Đánh giá tính pháp lý, đạo đức dữ liệu, cấu trúc kỹ thuật và chất lượng dữ liệu để ra quyết định nguồn cho bài toán Machine Learning.

---

## 1. Bằng Chứng Khảo Sát & Phạm Vi Kiểm Tra Thực Tế

Khảo sát được thực hiện trực tiếp trên môi trường live bằng công cụ HTTP client tại các điểm truy cập chính thức của website:

1. **Chính sách robot**: `https://oto.com.vn/robots.txt`
2. **Quy định & Chính sách**: `https://oto.com.vn/quy-dinh-chinh-sach`
3. **Quy chế hoạt động sàn TMĐT**: `https://oto.com.vn/quy-che-hoat-dong`
4. **Trang danh sách tin đăng xe cũ**: `https://oto.com.vn/mua-ban-xe-cu`
5. **Trang chi tiết tin đăng mẫu 1**: `https://oto.com.vn/mua-ban-xe-mercedes-benz-c200-ha-noi/mercedes-exclusive-2021-aidxc23442555` (ID: 23442555)
6. **Trang chi tiết tin đăng mẫu 2**: `https://oto.com.vn/mua-ban-xe-kia-carnival-hcm/chiec-xe-quoc-dan-sieu-luot-aidxc23444950` (ID: 23444950)

---

## 2. Khảo Sát & Phân Loại Các Trường Dữ Liệu

Dựa trên việc bóc tách thực tế mã nguồn HTML của trang danh sách và các trang chi tiết, ma trận trạng thái các trường dữ liệu được xác định như sau:

| Tên trường dự kiến | Trạng thái xác minh | Vị trí quan sát thực tế | Bằng chứng mã nguồn / Dữ liệu thực tế | Đánh giá rủi ro |
| :--- | :--- | :--- | :--- | :--- |
| **`price_vnd`** (Giá rao bán) | **Đã xác minh có thể quan sát** | - Thẻ `<p class="price">`<br>- Thuộc tính `data-call`<br>- Thẻ `<span class="price">` (trang chi tiết) | Ví dụ: `899 triệu`, `1 tỉ 169 triệu`, `2 tỉ 539 triệu` | Giá sử dụng đơn vị chuỗi hỗn hợp ("triệu", "tỉ"), cần logic quy đổi chính xác, có thể có tin để giá "Thỏa thuận". |
| **`brand`** (Hãng xe) | **Đã xác minh có thể quan sát** | - Thuộc tính `data-tinrao`<br>- Thuộc tính `data-call`<br>- Breadcrumb, thẻ tiêu đề | Ví dụ: `Mercedes-Benz`, `Kia`, `Toyota`, `Audi` | Độ chuẩn hóa cao, được website phân loại theo danh mục. |
| **`model`** (Dòng xe) | **Đã xác minh có thể quan sát** | - Thuộc tính `data-tinrao`<br>- Thuộc tính `data-call` | Ví dụ: `C200`, `Carnival`, `Camry`, `Q8` | Cần tách giữa Model gốc và Trim/Phiên bản (vd: `Carnival 2.2D Signature`). |
| **`year`** (Năm sản xuất) | **Đã xác minh có thể quan sát** | - Thuộc tính `data-call`<br>- Thẻ `<ul class="list-info">` | Ví dụ: `2021`, `2024`, `2019` | Định dạng năm 4 chữ số, ít sai lệch. |
| **`mileage_km`** (Số km đã đi) | **Đã xác minh có thể quan sát** | - Thẻ `<ul class="tag-list"> > li`<br>- Bảng thông số trang chi tiết | Ví dụ: `49.000 km`, `40.000 km`, `28.000 km` | Chứa ký tự phân cách dấu chấm và chữ `km`. Một số xe siêu lướt có thể điền 0 hoặc người bán gõ bừa. |
| **`fuel_type`** (Nhiên liệu) | **Đã xác minh có thể quan sát** | - Thẻ `<ul class="tag-list"> > li`<br>- Bảng thông số trang chi tiết | Ví dụ: `Máy xăng`, `Máy dầu`, `Hybrid` | Danh mục tương đối chuẩn hóa (xăng, dầu, hybrid, điện). |
| **`transmission`** (Hộp số) | **Đã xác minh có thể quan sát** | - Thẻ `<ul class="tag-list"> > li`<br>- Bảng thông số trang chi tiết | Ví dụ: `Số tự động`, `Số sàn` | Chuẩn hóa cao, thường có 2 giá trị chính. |
| **`location_province`** (Tỉnh/Thành) | **Đã xác minh có thể quan sát** | - Thẻ `<li class="seller-location">`<br>- Bảng thông số trang chi tiết | Ví dụ: `Hà Nội`, `Tp.HCM`, `Ba Đình - Hà Nội`, `Thủ Đức - Tp.HCM` | Cần regex để trích xuất cấp tỉnh/thành phố chuẩn (bỏ quận/huyện). |
| **`body_type`** (Kiểu dáng) | **Đã xác minh có thể quan sát** | - Thuộc tính `data-call`<br>- Bảng thông số trang chi tiết | Ví dụ: `Sedan`, `SUV`, `MPV`, `Hatchback` | Có sẵn trong thuộc tính tracking metadata của tin đăng. |
| **`origin`** (Xuất xứ) | **Đã xác minh có thể quan sát** | - Thuộc tính `data-call`<br>- Bảng thông số trang chi tiết | Ví dụ: `Trong nước`, `Nhập khẩu` | Phân loại nhị phân rõ ràng. |
| **`seats`** (Số chỗ ngồi) | **Chỉ xuất hiện ở một số tin đăng / Không có trong bảng chuẩn** | - Không tìm thấy trong `box-info-detail` chuẩn<br>- Chỉ xuất hiện ngẫu nhiên trong phần mô tả tự do hoặc đường dẫn gợi ý SEO | Kiểm tra chi tiết 2 xe Mercedes C200 và Kia Carnival: Bảng thông số không có trường "Số chỗ". Trong văn bản tự do: "Kia Carnival 7 chỗ". | **Rủi ro cao**: Đây là biến missing rất lớn nếu thu thập tự động từ metadata có cấu trúc. Phải đánh dấu `provisional` và lập chiến lược suy diễn (mapping từ Model/Body Type) hoặc loại bỏ khỏi feature set ban đầu. |
| **`listing_id`** (Mã tin đăng) | **Đã xác minh có thể quan sát** | - Thuộc tính `data-autoid`<br>- Hậu tố URL (`aidxc...`) | Ví dụ: `23442555`, `23444950`, `23444973` | Khóa định danh kỹ thuật cực tốt để lọc trùng lặp bản ghi. |
| **`source_url`** (Đường dẫn tin) | **Đã xác minh có thể quan sát** | - Thuộc tính `href` của thẻ tiêu đề | Đường dẫn URL tương đối hoặc tuyệt đối | Đảm bảo tính kiểm chứng lại của dữ liệu. |
| **`crawl_date`** | **Trường sinh tự động** | - Timestamp của hệ thống thu thập | Ví dụ: `2026-10-18T15:10:39` | Cần thiết để tính toán khấu hao và tuổi xe (`car_age = crawl_year - year`). |

---

## 3. Đánh Giá Phương Thức Truy Cập & Giới Hạn Kỹ Thuật

### 3.1. Phân tích Robots.txt

Tệp `https://oto.com.vn/robots.txt` quy định:
- Dành cho mọi user-agent thông thường (`User-agent: *`): Áp dụng `Allow: /`.
- Đường dẫn bị Disallow cụ thể: `/upgrade.html`, `/diendan/seolink/`, `/viewcount/`, `/member/`, `/diendan/`, `/banner-click`, `/oto-wiki`, cùng các trang lọc SEO dạng `/*/*-nam-2020$`, `/hang-xe-*$`.
- Chặn tuyệt đối một số bot SEO và công cụ thu thập thương mại quy mô lớn: `SentiOne`, `MegaIndex.ru`, `SemrushBot`, `MJ12bot`, `AhrefsBot/DotBot`,...
- **Nhận định**: Đường dẫn `/mua-ban-xe-cu` và các trang danh sách xe cũ `/mua-ban-xe/p2` không nằm trong danh mục cấm truy cập của `robots.txt` đối với crawler thông thường. Tuy nhiên, việc tuân thủ robots.txt chỉ là điều kiện cần tối thiểu, không đồng nghĩa với việc được phép khai thác tự do dữ liệu bản quyền.

### 3.2. Cơ chế Render & Cấu trúc kỹ thuật

- **Server-Side Rendering (SSR)**: Website trả về HTML chứa đầy đủ dữ liệu tin đăng trực tiếp trong response HTTP ban đầu. Không yêu cầu chạy trình duyệt headless (Selenium, Playwright) để render JavaScript nặng.
- **Dữ liệu cấu trúc ẩn có giá trị cao**: Mỗi thẻ tin đăng `<div class="item-car">` đều chứa thuộc tính metadata nội bộ rất sạch:
  ```html
  data-autoid="23442555"
  data-tinrao="Mercedes-Benz.C200.Xe cũ.23442555.V5."
  data-call="Mercedes-Benz.C200.Xe cũ.Nhập khẩu.2021.899 triệu.Sedan.Trắng.F0.V5.23442555."
  ```
  Điều này cho phép thu thập hầu hết các biến đặc trưng cốt lõi (Hãng, Dòng xe, Năm, Giá, Kiểu dáng, Màu sắc, Xuất xứ) ngay từ trang danh sách mà không nhất thiết phải gửi thêm hàng nghìn request vào từng trang chi tiết.
- **Cơ chế phân trang**: Sử dụng URL thân thiện `/mua-ban-xe/p2`, `/mua-ban-xe/p3`,... Quy mô ghi nhận: 5.267 tin đăng bán xe cũ toàn quốc tại thời điểm kiểm tra. Mỗi trang hiển thị khoảng 15 tin.

### 3.3. Chính sách Bản quyền & Điều khoản Hoạt động Sàn

Theo kiểm tra tài liệu `https://oto.com.vn/quy-che-hoat-dong` (Mục 10.1):
> *"Oto.com.vn giữ bản quyền sử dụng dịch vụ và các nội dung trên Sàn giao dịch Oto.com.vn theo các quy định của pháp luật về bảo hộ sở hữu trí tuệ tại Việt Nam... Nghiêm cấm mọi hành vi sao chép, sử dụng và phổ biến bất hợp pháp các quyền sở hữu trên."*

Và tại Mục 10.2:
> *"Do thị trường ô tô rất phong phú và đa dạng... chúng tôi không thể bảo đảm hoàn toàn tính chính xác của các thông tin, cũng như mô tả của các loại tin đăng... người rao bán có thể chủ quan khi mô tả sản phẩm của họ."*

**Ý nghĩa pháp lý & phương pháp luận**:
- Không được phép thực hiện thu thập tự động ồ ạt (bulk scraping) gây áp lực lên máy chủ hoặc thương mại hóa tập dữ liệu.
- Trong khuôn khổ dự án học tập, nghiên cứu phi thương mại, việc khảo sát mẫu dữ liệu nhỏ (pilot 30–50 tin) cần tuân thủ nghiêm ngặt:
  - Tần suất truy vấn chậm (rate limiting: 2–3 giây/request).
  - Khai báo User-Agent minh bạch danh tính học thuật.
  - **Tuyệt đối không thu thập dữ liệu cá nhân (PII)**: Tên người bán (`seller-name`), số điện thoại (`seller-phone`, `data-phone`).

---

## 4. Phân Tích Rủi Ro Chất Lượng Dữ Liệu (Data Quality Risks)

Dựa trên thực tế khảo sát sàn rao vặt, các rủi ro sau đây là hiện hữu và bắt buộc phải có phương án kiểm soát:

1. **Rủi ro định dạng giá (`price_vnd`)**:
   - Giá có thể xuất hiện dưới nhiều dạng: `899 triệu`, `1 tỉ 169 triệu`, `3 tỉ 400 triệu`, hoặc `Giá thỏa thuận` / `Liên hệ`.
   - Các tin đăng "Giá thỏa thuận" không chứa giá trị số cụ thể, nếu cố ép về 0 sẽ làm sai lệch phân phối nghiêm trọng. Bắt buộc phải loại bỏ khỏi tập huấn luyện hồi quy.
2. **Rủi ro thiếu trường `seats` (Số chỗ ngồi)**:
   - Qua kiểm tra chi tiết, bảng thông số kỹ thuật chuẩn không cung cấp trường `seats`. Nếu coi đây là trường bắt buộc thì tỷ lệ missing có thể lên tới 90–100% nếu chỉ trích xuất metadata chuẩn.
3. **Rủi ro tin đăng trùng lặp (Duplicates & Multi-listing)**:
   - Một chiếc xe có thể được chủ xe hoặc các môi giới (salon) đăng nhiều lần với các mức giá chênh lệch nhẹ hoặc hình ảnh khác nhau.
   - Nhờ có `data-autoid`, ta loại bỏ được trùng mã tin, nhưng với trùng xe thực tế (cùng hãng, model, năm, odo, màu, địa bàn) cần cơ chế heuristic matching.
4. **Rủi ro ngoại lai do lỗi nhập liệu (Data Entry Errors & Outliers)**:
   - Người bán gõ nhầm số 0 vào số km (ví dụ `490.000 km` thay vì `49.000 km`, hoặc xe 10 năm tuổi nhưng để ODO `1.000 km`).
   - Giá ảo (đăng giá tượng trưng `100 triệu` để câu view trong khi giá xe là 1 tỷ).
5. **Rủi ro sai lệch phân khúc (Sampling Bias)**:
   - Các trang đầu có tỷ lệ xe VIP, xe salon cao cấp (`data-viptype="V5"`, `V3`) nhiều hơn xe của người dùng cá nhân. Nếu chỉ lấy 3–4 trang đầu sẽ gặp bias về phân khúc xe sang và salon.

---

## 5. Quyết Định Về Nguồn Dữ Liệu (Source Decision)

### Quyết định: **CONDITIONAL GO (Chấp Thuận Có Điều Kiện)**

### Lý do chi tiết:
1. **Mặt khả thi**:
   - Dữ liệu hoàn toàn có thể quan sát công khai qua HTML tĩnh (SSR).
   - Đã xác minh sự tồn tại của 10/11 trường thông tin nòng cốt (`price_vnd`, `brand`, `model`, `year`, `mileage_km`, `fuel_type`, `transmission`, `location_province`, `body_type`, `origin`, `listing_id`).
   - Có cơ chế định danh tin đăng tường minh (`data-autoid`) hỗ trợ chống trùng lặp.
2. **Mặt giới hạn và điều kiện tiên quyết**:
   - **Điều kiện 1 (Pháp lý & Đạo đức)**: Chỉ thực hiện ở phạm vi Pilot nhỏ (30–50 bản ghi) để đánh giá schema và parser; loại bỏ hoàn toàn PII (số điện thoại, tên người bán); áp dụng rate limiting tối thiểu 2 giây giữa các request.
   - **Điều kiện 2 (Xử lý trường `seats`)**: Không coi `seats` là trường bắt buộc ở raw level; chuyển sang trạng thái `provisional` và nghiên cứu mapping từ dòng xe ở Phase Cleaning.
   - **Điều kiện 3 (Phê duyệt của Mentor)**: Kết quả Pilot phải được mentor rà soát và đánh giá lại trước khi quyết định mở rộng thu thập quy mô lớn (~1.000 bản ghi) hoặc chuyển sang tập dữ liệu dự phòng (như tập dữ liệu thứ cấp đã đóng băng từ Kaggle/Dataset đối tác).

---

## 6. Góc Nhìn Sư Phạm & Quyết Định Kỹ Thuật

1. **Chúng ta đang giải quyết vấn đề gì?**
   - Xác định xem Oto.com.vn có đủ điều kiện kỹ thuật và pháp lý để làm nguồn dữ liệu cho bài toán dự đoán giá ô tô cũ hay không.
2. **Vì sao cần giải quyết vấn đề đó?**
   - Tránh việc viết crawler quy mô lớn rồi bị chặn IP, gặp vấn đề vi phạm điều khoản dịch vụ hoặc thu về dữ liệu rác không thể huấn luyện mô hình.
3. **Có những lựa chọn nào?**
   - *Lựa chọn 1 (Bỏ qua audit, crawl ngay)*: Nguy cơ cao bị chặn, vi phạm đạo đức dữ liệu.
   - *Lựa chọn 2 (Từ chối ngay - NO-GO)*: Quá khắt khe khi website không chặn robots.txt và dữ liệu cấu trúc rất tốt.
   - *Lựa chọn 3 (CONDITIONAL GO - Được chọn)*: Thử nghiệm pilot kiểm soát nghiêm ngặt về tốc độ và bảo mật, đánh giá chất lượng trước khi mở rộng.
4. **Vì sao lựa chọn hiện tại hợp lý?**
   - Đảm bảo tính thận trọng khoa học, tôn trọng máy chủ nguồn và tuân thủ các quy định về quyền riêng tư.
5. **Rủi ro hoặc hạn chế của lựa chọn này là gì?**
   - Nếu giai đoạn Pilot phát hiện website dựng rào cản WAF hoặc tỷ lệ nhiễu giá quá cao, dự án sẽ phải kích hoạt phương án dữ liệu dự phòng.
6. **Mentor có thể hỏi gì về quyết định đó?**
   - *"Tại sao không chọn quyết định GO hoàn toàn khi thấy dữ liệu trên web rất đẹp?"*
   - *Trả lời*: Một kỹ sư dữ liệu có trách nhiệm không bao giờ kết luận GO khi website có điều khoản bảo lưu quyền sở hữu nội dung và trường nghiệp vụ cốt lõi như `seats` chưa được xác minh trong bảng thông số chuẩn. Quyết định CONDITIONAL GO phản ánh sự cẩn trọng cần thiết.
