# Kịch Bản Thuyết Trình Bảo Vệ Đồ Án Cuối Khóa (Speaker Notes)
*(Used Car Price Prediction in Vietnam: An End-to-End Machine Learning System)*

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam
- **Người trình bày**: AI Student
- **Đối tượng lắng nghe**: Hội đồng Mentor & Thành viên CLB AI
- **Thời lượng dự kiến**: 10 – 12 phút (khoảng 40 – 50 giây / slide)
- **Tài liệu slide đi kèm**: [`presentation/ai_club_final_defense.pptx`](file:///d:/ai-club-end-training/presentation/ai_club_final_defense.pptx)

---

## Cấu Trúc Thời Gian Tổng Thể (Presentation Timeline)

```text
┌─────────────────────────────────────────────────────────────┬──────────────┐
│ Phân đoạn nội dung                                          │ Thời lượng   │
├─────────────────────────────────────────────────────────────┼──────────────┤
│ 1. Mở đầu & Bối cảnh bài toán (Slide 1 – 3)                 │ 2.0 phút     │
│ 2. EDA, Tiền xử lý & Kỹ nghệ đặc trưng (Slide 4 – 6)        │ 2.5 phút     │
│ 3. Mô hình hóa & Bảng xếp hạng Validation (Slide 7 – 8)     │ 2.0 phút     │
│ 4. Kiểm định Test & Phân tích Ngoại lai (Slide 9)           │ 1.5 phút     │
│ 5. Kiểm toán Rò rỉ & Đánh giá Độ bền Nhóm (Slide 10 – 11)   │ 2.0 phút     │
│ 6. Giải thích Mô hình, Kỹ thuật Phần mềm & Giới hạn (12–14) │ 1.5 phút     │
│ 7. Kết luận & Định hướng Tương lai (Slide 15)               │ 0.5 phút     │
├─────────────────────────────────────────────────────────────┼──────────────┤
│ TỔNG THỜI GIAN THUYẾT TRÌNH                                 │ 12.0 phút    │
└─────────────────────────────────────────────────────────────┴──────────────┘
```

---

## Chi Tiết Lời Thoại & Hướng Dẫn Từng Slide

### Slide 1: Trang Tiêu Đề (Title Slide)
- **Thời lượng**: 30 giây
- **Thông điệp cốt lõi**: Giới thiệu bản thân, đề tài và định vị đây là một công trình học máy hoàn chỉnh từ dữ liệu thô, phòng chống rò rỉ đến thẩm định độ bền khoa học.
- **Lời thoại trình bày**:
  > *"Kính thưa các anh chị Mentor và các bạn thành viên Câu lạc bộ AI. Em xin đại diện nhóm trình bày đồ án tốt nghiệp khóa đào tạo với đề tài: **'Dự đoán giá ô tô đã qua sử dụng tại Việt Nam: Xây dựng hệ thống học máy toàn diện và thẩm định khoa học'**.*
  >
  > *Trong đồ án này, mục tiêu của em không dừng lại ở việc tinh chỉnh ra một mô hình có điểm số cao, mà tập trung giải quyết bài toán cốt lõi: Làm sao xây dựng một quy trình dữ liệu sạch tất định, kiểm soát nghiêm ngặt rò rỉ dữ liệu (Zero Data Leakage), và chứng minh được mô hình có độ bền thực sự khi đối mặt với các tin đăng trùng lặp trên thị trường thực tế."*
- **Điểm kỹ thuật nhấn mạnh**: Nhắc đến 4 trụ cột: Data Governance, Zero Leakage, Tuned Ensembles và Group-Aware Robustness.
- **Câu chuyển slide**:
  > *"Để bắt đầu, em xin trình bày về thực trạng thị trường xe hơi cũ tại Việt Nam và cách chúng em phát biểu bài toán học máy."*

---

### Slide 2: Thực Trạng Thị Trường & Bài Toán Hồi Quy
- **Thời lượng**: 45 giây
- **Thông điệp cốt lõi**: Bất cân xứng thông tin, dải giá rộng từ 55 triệu đến 45 tỷ, và biên độ thương lượng 3-5% làm mốc đánh giá mô hình.
- **Lời thoại trình bày**:
  > *"Thị trường ô tô cũ tại Việt Nam là một thị trường phân mảnh với mức độ bất cân xứng thông tin rất lớn. Người mua xe cá nhân thường thiếu công cụ khách quan để định giá xe trước các mức giá chào bán đầy biến động của các salon.*
  >
  > *Về mặt dữ liệu, giá xe có dải động cực kỳ rộng — từ những chiếc xe van 55 triệu cho đến siêu xe 45 tỷ VND — và phân phối lệch phải nghiêm trọng. Đặc biệt, trong ngành ô tô Việt Nam, biên độ thương lượng phổ biến giữa người mua và người bán thường dao động từ **3% đến 5%** giá trị xe. Đây chính là mỏ neo nghiệp vụ quan trọng: nếu mô hình của chúng em đạt sai số tương đối dưới 5%, nó hoàn toàn có thể trở thành một công cụ tham chiếu giá độc lập đáng tin cậy.*
  >
  > *Chúng em phát biểu bài toán dưới dạng Hồi quy bảng có giám sát (Supervised Tabular Regression), với nhãn mục tiêu là giá VND, nhưng được huấn luyện trên không gian logarit để tối ưu hóa sai số phần trăm."*
- **Điểm kỹ thuật nhấn mạnh**: Giải thích tại sao tối ưu $\ln(y)$ tương đương với tối ưu hóa sai số tỷ đối (proportional error).
- **Dự đoán câu hỏi Mentor**: *"Tại sao không phân loại theo khoảng giá mà lại dùng hồi quy liên tục?"*
- **Câu chuyển slide**:
  > *"Để giải bài toán này, bước đầu tiên chúng em thực hiện là thẩm định nguồn dữ liệu và thiết lập quy trình quản trị dữ liệu nghiêm ngặt."*

---

### Slide 3: Tiếp Nhận Dữ Liệu & Quản Trị Dữ Liệu
- **Thời lượng**: 45 giây
- **Thông điệp cốt lõi**: Dữ liệu thô 30,652 dòng được bảo toàn nguyên vẹn với mã băm SHA-256; xác lập Cohort A 23,510 dòng; loại bỏ PII.
- **Lời thoại trình bày**:
  > *"Về nguồn dữ liệu, ban đầu chúng em đã xây dựng một module crawler tự động. Tuy nhiên, sau khi kiểm toán an toàn và phân tích rủi ro WAF cũng như giới hạn tần suất của các website, chúng em đã báo cáo Mentor và được phê duyệt sử dụng bộ dữ liệu thứ cấp từ nền tảng Bonbanh gồm 30,652 tin đăng công khai trên Kaggle.*
  >
  > *Toàn bộ dữ liệu thô được bảo vệ ở chế độ Read-Only tuyệt đối với mã băm SHA-256 bất biến. Chúng em xác lập **Cohort A** gồm 23,510 xe sản xuất từ năm 2015 trở lại đây làm tập đối tượng trọng tâm, bởi phân khúc xe dưới 10 năm tuổi này chiếm hơn 85% thanh khoản thị trường và có tính ổn định cao về mặt kỹ thuật.*
  >
  > *Đồng thời, về mặt đạo đức dữ liệu, toàn bộ số điện thoại cá nhân, tên người bán và URL đều được bóc tách và loại bỏ triệt để trước khi đưa vào pipeline."*
- **Điểm kỹ thuật nhấn mạnh**: Mã băm SHA-256 được kiểm toán độc lập qua các giai đoạn, không thay đổi 1 byte.
- **Câu chuyển slide**:
  > *"Sau khi tiếp nhận dữ liệu, chúng em tiến hành khám phá chuyên sâu (EDA) để tìm ra các đặc thù nghiệp vụ chi phối giá xe."*

---

### Slide 4: Khám Phá Dữ Liệu (EDA) & Biểu Thuế TTĐB
- **Thời lượng**: 50 giây
- **Thông điệp cốt lõi**: Phân phối lệch phải được giải quyết bằng logarit; Dung tích động cơ gắn liền Thuế Tiêu thụ Đặc biệt (TTĐB); Phân hóa thương hiệu hạng sang.
- **Lời thoại trình bày**:
  > *"Trên màn hình là đồ thị phân phối giá xe mà chúng em trích xuất từ Phase 4 EDA. Như các anh chị có thể thấy ở hình bên trái, giá xe thực tế lệch phải rất nặng: trung vị là 719 triệu nhưng giá trung bình bị kéo vọt lên 1.164 tỷ VND do cái đuôi dài của nhóm xe siêu sang. Tuy nhiên, khi biến đổi sang hàm logarit, dữ liệu phân bố đối xứng chuẩn mực hình chuông Gauss.*
  >
  > *Đặc biệt, khám phá quan trọng nhất của chúng em nằm ở mối liên hệ giữa **Dung tích động cơ (`engine_displacement_l`)** và **Biểu thuế Tiêu thụ Đặc biệt (TTĐB) của Việt Nam**. Luật thuế quy định xe có dung tích xi-lanh trên 3.0L đến 6.0L bị áp thuế suất lũy tiến từ 90% đến 150%. Điều này lý giải tại sao dung tích động cơ tạo ra bước nhảy vọt phi tuyến về giá và trở thành biến dự báo mạnh hàng đầu của mô hình.*
  >
  > *Bên cạnh đó, yếu tố thương hiệu hạng sang (`is_luxury_brand`) cũng phân tách rõ rệt phổ giá giữa nhóm xe phổ thông (Toyota, Hyundai) và nhóm xe sang (Mercedes, Lexus)."*
- **Điểm kỹ thuật nhấn mạnh**: Phân tích biểu thuế TTĐB chứng minh sự am hiểu sâu sắc về nghiệp vụ thị trường Việt Nam.
- **Câu chuyển slide**:
  > *"Dựa trên những phát hiện từ EDA, chúng em thiết kế đường ống làm sạch và kỹ nghệ đặc trưng tại Phase 5."*

---

### Slide 5: Tiền Xử Lý Dữ Liệu & Bộ 15 Đặc Trưng Tinh Gọn
- **Thời lượng**: 50 giây
- **Thông điệp cốt lõi**: Xử lý ODO ngoại lai bằng median thay vì drop; tách biệt 25.8% xe mới showroom; ma trận 15 đặc trưng chuẩn hóa; chặn 9 cột rò rỉ.
- **Lời thoại trình bày**:
  > *"Trong quá trình làm sạch dữ liệu, chúng em quán triệt nguyên tắc: 'Không loại bỏ bản ghi bừa bãi'. Cụ thể với trường ODO, có những bản ghi người bán gõ phím ảo như 999,999 km. Thay vì xóa hàng làm méo mó phân bố, chúng em gán giá trị trung vị có điều kiện theo nhóm tuổi xe.*
  >
  > *Một phát hiện rất thú vị là có tới **25.8% dữ liệu là xe mới 100% tại showroom** với ODO = 0 km và bán đúng giá niêm yết của hãng. Nếu không xử lý cẩn thận, mô hình sẽ bị nhầm lẫn giữa xe mới tinh và xe cũ lướt ít. Chúng em đã chủ động tạo cờ `is_zero_mileage` và nhãn `Xe mới` để cô lập nhóm này.*
  >
  > *Kết quả, chúng em thu được ma trận đầu vào gồm **15 đặc trưng chuẩn hóa**: 8 biến số và 7 biến phân loại. Đồng thời, 9 cột tiềm ẩn nguy cơ rò rỉ như `Mô tả`, `Tên xe`, `Giá` gốc bị chặn hoàn toàn khỏi ma trận X."*
- **Điểm kỹ thuật nhấn mạnh**: Việc tạo biến cờ `is_zero_mileage` giúp xử lý hiện tượng spike tại 0 của biến ODO.
- **Câu chuyển slide**:
  > *"Để đảm bảo tính khách quan trong đánh giá, chúng em thiết lập quy trình phân chia tập dữ liệu nghiêm ngặt."*

---

### Slide 6: Giao Thức Phân Chia Tập 80/10/10 & Chống Rò Rỉ Tuyến Tính
- **Thời lượng**: 45 giây
- **Thông điệp cốt lõi**: Chia 80/10/10 phân tầng theo 10 deciles giá; niêm phong tập Test; fit tiền xử lý duy nhất trên Train.
- **Lời thoại trình bày**:
  > *"Chúng em áp dụng giao thức phân chia 80/10/10 với 18,808 dòng tập Train, 2,351 dòng Validation và 2,351 dòng Test.*
  >
  > *Để tránh việc các tập lệch pha về phân phối giá, chúng em phân tầng (Stratified) dựa trên 10 phân vị giá. Kết quả là giá trung vị của cả 3 tập đều đạt mức chuẩn xác 719 triệu VND.*
  >
  > *Về mặt chống rò rỉ (Leakage Prevention), toàn bộ các bộ biến đổi như Imputer, OneHotEncoder và Scaler chỉ được gọi hàm `fit()` duy nhất trên tập Train. Đối với tập Validation và Test, chúng chỉ được gọi hàm `transform()`. Tùy chọn `handle_unknown='ignore'` được bật để hệ thống không bị crash khi gặp các dòng xe hiếm trong tương lai.*
  >
  > *Tập Test được niêm phong hoàn toàn và chỉ được mở ra đánh giá một lần duy nhất sau khi đã chốt mô hình trên Validation."*
- **Điểm kỹ thuật nhấn mạnh**: Nhấn mạnh nguyên tắc bất biến của tập Test trong khoa học dữ liệu.
- **Câu chuyển slide**:
  > *"Bước sang Phase 6, chúng em tiến hành huấn luyện và so sánh 10 cấu hình mô hình học máy."*

---

### Slide 7: Khảo Sát Đa Dạng Kiến Trúc Mô Hình
- **Thời lượng**: 50 giây
- **Thông điệp cốt lõi**: So sánh từ Dummy Baselines, Linear có điều chuẩn (Ridge/Lasso) đến các dòng Cây quyết định; tác động kỳ diệu của Log-Target.
- **Lời thoại trình bày**:
  > *"Để không bị rơi vào bẫy 'ảo tưởng sức mạnh' của mô hình phức tạp, chúng em xây dựng hai mô hình Baseline cơ sở: Median Baseline có MAE 914.6 triệu và Mean Baseline có MAE 1.164 tỷ VND.*
  >
  > *Khi thử nghiệm dòng Hồi quy Tuyến tính Ridge trên giá thô (Raw VND), mô hình đạt R² 0.80 nhưng MAE lên tới 379 triệu và MdAPE lên tới 23.7%. Lý do là hàm tổn thất bình phương MSE bị chi phối bởi các xe 30-40 tỷ, khiến mô hình hy sinh độ chính xác của xe cỏ 400 triệu.*
  >
  > *Tuy nhiên, khi chuyển sang huấn luyện trên **Log Target**, một bước ngoặt đã xảy ra: Ridge giảm MAE xuống 255.7 triệu và MdAPE giảm sâu từ 23.7% xuống còn **7.72%**. Điều này khẳng định sức mạnh của việc tối ưu hóa tỷ lệ thay vì giá trị tuyệt đối.*
  >
  > *Bên cạnh đó, các mô hình cây như HistGradientBoosting và Random Forest cho thấy ưu thế vượt trội khi tự động học được các mối tương tác phi tuyến phức tạp."*
- **Điểm kỹ thuật nhấn mạnh**: Phân tích toán học tại sao hàm tổn thất MSE trên Log Target xấp xỉ sai số tỷ đối bình phương.
- **Câu chuyển slide**:
  > *"Kết quả tổng hợp của 10 cấu hình này được thể hiện rõ ràng trên Bảng xếp hạng Validation."*

---

### Slide 8: Bảng Xếp Hạng Validation & Lựa Chọn Mô Hình Vô Địch
- **Thời lượng**: 50 giây
- **Thông điệp cốt lõi**: Bảng so sánh 10 mô hình; Champion `Tree_RandomForest_Tuned_LogTarget` chiến thắng áp đảo (MAE 142.9M, R² 0.8694, MdAPE 4.25%).
- **Lời thoại trình bày**:
  > *"Đây là Bảng xếp hạng tổng thể trên 2,351 dòng Validation, với toàn bộ sai số đã được nghịch đảo hàm mũ về đơn vị VND thực tế.*
  >
  > *Mô hình giành vị trí Quán quân là **`Tree_RandomForest_Tuned_LogTarget`** — cấu hình Rừng ngẫu nhiên 150 cây, độ sâu tối đa 24, lá tối thiểu 1.*
  >
  > *Mô hình đạt các chỉ số ấn tượng:
  > - **MAE đạt 142.9 triệu VND**, giúp cắt giảm tới **84.4% sai số** so với Median Baseline.
  > - **Hệ số R² đạt 0.8694**, giải thích gần 87% biến thiên giá thị trường.
  > - Đặc biệt, **MdAPE đạt 4.25%**, nghĩa là một nửa số xe trên thị trường được mô hình dự đoán với độ lệch dưới 4.25% — nằm trọn vẹn trong biên độ mặc cả của người mua xe.*
  >
  > *Với thời gian huấn luyện chỉ 5 giây và kích thước xuất bản 31 MB, chúng em chính thức lựa chọn cấu hình này làm Champion Model của đồ án."*
- **Điểm kỹ thuật nhấn mạnh**: Nhấn mạnh chỉ số MdAPE 4.25% gắn liền với nghiệp vụ thực tế.
- **Câu chuyển slide**:
  > *"Sau khi đã đóng băng Champion Model, chúng em tiến hành mở niêm phong tập Test độc lập."*

---

### Slide 9: Đánh Giá Tập Test Chính Thức & Phân Tích Ngoại Lai
- **Thời lượng**: 50 giây
- **Thông điệp cốt lõi**: Test MAE 111.8M VND, R² 0.9448, MdAPE 4.29%; giải mã tại sao Test MAE lại tốt hơn Val MAE dựa trên xe siêu sang 39 tỷ.
- **Lời thoại trình bày**:
  > *"Trên 2,351 xe của tập Test chưa từng thấy, Champion Model đạt kết quả xuất sắc: **Test MAE đạt 111.8 triệu VND**, **R² đạt 0.9448**, và **MdAPE đạt 4.29%**.*
  >
  > *Tuy nhiên, một câu hỏi kiểm toán quan trọng được đặt ra: **Tại sao Test MAE (111.8M) lại tốt hơn Validation MAE (142.9M)? Liệu có sự bất thường ở đây?**
  >
  > *Chúng em đã tiến hành phân rã phương sai và phát hiện sự thật: Sự chênh lệch này hoàn toàn không phải do mô hình 'may mắn', mà do tập Validation ngẫu nhiên chứa một chiếc xe siêu sang giá **38.999 tỷ VND**, nhưng mô hình chỉ dự đoán là 3.2 tỷ — gây ra sai số lệch 35.75 tỷ trên một dòng duy nhất, tự nó đã kéo MAE toàn tập Val tăng thêm 15.2 triệu VND!*
  >
  > *Khi xét trên phân khúc xe phổ thông dưới 1 tỷ VND (chiếm 70% dữ liệu), MAE giữa Validation và Test hoàn toàn trùng khớp ở mức 25.5 triệu và 26.1 triệu VND. Chỉ số MdAPE 4.25% và 4.29% cũng chứng minh độ chính xác thực tế giữa hai tập là hoàn toàn tương đương."*
- **Điểm kỹ thuật nhấn mạnh**: Bằng chứng phân rã sai số xóa tan nghi ngờ về việc đánh giá thiên vị hay rò rỉ.
- **Câu chuyển slide**:
  > *"Dù kết quả rất tốt, tại Phase 6.1, nhóm kiểm toán độc lập đã phát hiện ra một nguy cơ tiềm ẩn về rò rỉ đăng chéo tin."*

---

### Slide 10: Kiểm Toán Độc Lập & Phát Hiện Rò Rỉ Đăng Chéo Tin
- **Thời lượng**: 50 giây
- **Thông điệp cốt lõi**: Phân rã 5 dạng trùng lặp; phát hiện 8.21% Test trùng văn bản mô tả với Train (Cross-Posting); đặt ra bài toán Group-Aware.
- **Lời thoại trình bày**:
  > *"Trong đợt kiểm toán Phase 6.1, chúng em rà soát lại toàn bộ các định nghĩa về trùng lặp dữ liệu:*
  > - *Trùng Listing ID và Trùng tuyệt đối cả dòng là **0%**.*
  > - *Tuy nhiên, có khoảng **8.21% xe tập Test có văn bản mô tả trùng khớp với tập Train** do các salon ô tô sao chép bài đăng của nhau (Cross-posting).*
  > - *Đồng thời, 95.8% xe Test có tổ hợp thông số (ví dụ Vios 2020 AT) đã từng xuất hiện trong Train.*
  >
  > *Một câu hỏi phản biện rất sắc bén được đặt ra: **Liệu mức MAE 111.8M có phải là do mô hình 'học vẹt' các tin đăng trùng lặp giữa Train và Test hay không?**
  >
  > *Để trả lời dứt khoát câu hỏi này, chúng em không dừng lại ở báo cáo lý thuyết mà quyết định bước vào Phase 6.2: Triển khai một đợt đánh giá độ bền chia nhóm (Group-Aware Evaluation) độc lập."*
- **Điểm kỹ thuật nhấn mạnh**: Phân biệt rạch ròi giữa Specification Overlap (IID Tabular) và Cross-Posting Leakage.
- **Câu chuyển slide**:
  > *"Chúng em đã giải quyết bài toán này như thế nào? Kính mời các anh chị theo dõi kết quả ở Slide 11."*

---

### Slide 11: Đánh Giá Độ Bền Nhận Thức Nhóm (Phase 6.2)
- **Thời lượng**: 60 giây
- **Thông điệp cốt lõi**: Gom 903 cụm trùng, chia `StratifiedGroupKFold` 0% rò rỉ; Test MdAPE giữ vững 4.29% tuyệt đối; MAE xe phổ thông thậm chí tốt hơn.
- **Lời thoại trình bày**:
  > *"Tại Phase 6.2, chúng em xây dựng thuật toán gom nhóm 4 cấp độ, phát hiện 903 cụm tin trùng mô tả gồm 2,430 xe. Sau đó, chúng em sử dụng `StratifiedGroupKFold` để chia lại tập dữ liệu, đảm bảo **toàn bộ các bài đăng trùng nằm trọn vẹn trong một tập — tỷ lệ rò rỉ nhóm giữa Train, Val và Test là 0.00% tuyệt đối!**
  >
  > *Sau đó, chúng em lấy nguyên mô hình Champion đã đóng băng để đánh giá lại trên tập Test mới không còn bất kỳ tin trùng nào. Kết quả thực nghiệm đã đem lại một bằng chứng khoa học không thể bác bỏ:
  > - **Test MdAPE giữ vững tuyệt đối ở mức 4.29% — hoàn toàn trùng khớp với Phase 6!**
  > - Test MAE đạt 130.8 triệu VND (tăng 18.9 triệu).
  >
  > *Tại sao MAE tăng mà MdAPE không đổi? Đồ thị bên trái đã chỉ rõ: Ở phân khúc xe phổ thông dưới 500 triệu, MAE của tập chia nhóm thậm chí còn tốt hơn (24.2M so với 26.1M VND). Việc tổng MAE tăng là do tập Test mới ngẫu nhiên có thêm **27 chiếc xe siêu sang trên 5 tỷ VND**, và riêng 27 chiếc xe này đã kéo MAE trung bình toàn tập tăng thêm 14.5 triệu VND!
  >
  > *Kết quả này khẳng định năng lực định giá của mô hình là hoàn toàn thực chất và bền vững, không hề phụ thuộc vào các tin đăng trùng."*
- **Điểm kỹ thuật nhấn mạnh**: Phép toán phân rã 27 xe siêu sang đóng góp 14.5M MAE là điểm nhấn thuyết phục nhất.
- **Câu chuyển slide**:
  > *"Tiếp theo, chúng em giải thích cơ chế ra quyết định của mô hình thông qua phân tích tầm quan trọng đặc trưng."*

---

### Slide 12: Tầm Quan Trọng Đặc Trưng & Nghiệp Vụ Thuế
- **Thời lượng**: 50 giây
- **Thông điệp cốt lõi**: MDI (Variance Reduction) và Permutation; `is_luxury_brand` (43.1%) và `engine_displacement_l` (26.35%) phản ánh thuế TTĐB; giải thích nghịch lý ODO.
- **Lời thoại trình bày**:
  > *"Trên màn hình là biểu đồ Tầm quan trọng đặc trưng. Ở đây, em xin đính chính một thuật ngữ: Đối với bài toán hồi quy, tiêu chí phân nhánh của Random Forest là **Độ giảm phương sai (MDI)** chứ không phải Gini (vốn chỉ dùng cho phân loại).
  >
  > *Hai đặc trưng chi phối mạnh nhất là **`is_luxury_brand` (43.1%)** và **`engine_displacement_l` (26.35%)**, chiếm gần 70% tổng trọng số quyết định. Điều này hoàn toàn tương thích với thực tế: xe sang xác lập trần giá, còn dung tích động cơ quyết định mức thuế TTĐB khổng lồ tại Việt Nam.
  >
  > *Một thắc mắc thường gặp là: **Tại sao số km lăn bánh (ODO) chỉ chiếm 0.69% MDI? Có phải ODO không quan trọng?**
  >
  > *Câu trả lời là: Trên quy mô toàn thị trường, khoảng giá giữa xe cỏ và xe siêu sang cách nhau 40 tỷ, nên thương hiệu và dung tích máy áp đảo ODO (một chiếc Lexus cũ đi 15 vạn vẫn đắt gấp 8 lần một chiếc Vios mới tinh 0 km). Nhưng ở góc độ cục bộ giữa 2 xe cùng đời 2020, ODO chính là biến số quyết định mức chênh lệch 30-50 triệu VND."*
- **Điểm kỹ thuật nhấn mạnh**: Sự phân biệt rạch ròi giữa Global Importance và Local Sensitivity của biến ODO.
- **Câu chuyển slide**:
  > *"Để đưa mô hình vào ứng dụng thực tiễn, chúng em đã đóng gói module suy luận và thiết lập quy chuẩn kiểm thử phần mềm."*

---

### Slide 13: Hệ Thống Suy Luận & Kỹ Thuật Phần Mềm
- **Thời lượng**: 45 giây
- **Thông điệp cốt lõi**: Module `predict.py` an toàn schema; hỗ trợ CLI & CSV batch; bộ 87 unit tests chạy 100% offline trong 5.94s.
- **Lời thoại trình bày**:
  > *"Về mặt kỹ thuật phần mềm, chúng em đã đóng gói toàn bộ quy trình thành module suy luận độc lập [`src/models/predict.py`](file:///d:/ai-club-end-training/src/models/predict.py). Module này cho phép dự đoán đơn lẻ qua dòng lệnh CLI hoặc dự đoán hàng loạt từ file CSV. Hệ thống tự động tính toán các biến phái sinh như tuổi xe, cờ xe sang và tự động loại bỏ các cột rò rỉ nếu người dùng đưa vào.
  >
  > *Artifact mô hình được tối ưu hóa chỉ nặng 31 MB, rất thuận tiện để đóng gói vào Docker container.
  >
  > *Đặc biệt, toàn bộ dự án được bảo vệ bởi **87 unit tests chạy tự động 100% offline trong 5.94 giây**, bao phủ toàn bộ các module từ kiểm tra mã băm, làm sạch, phân chia tập đến kiểm thử suy luận, đảm bảo tính tái lập tuyệt đối của mã nguồn."*
- **Điểm kỹ thuật nhấn mạnh**: Không phụ thuộc kết nối mạng; tính tái lập 100% với fixed seeds.
- **Câu chuyển slide**:
  > *"Là những người làm khoa học dữ liệu nghiêm túc, chúng em luôn nhìn nhận thẳng thắn vào các giới hạn của đề tài."*

---

### Slide 14: Giới Hạn Đề Tài & Ranh Giới Ứng Dụng
- **Thời lượng**: 45 giây
- **Thông điệp cốt lõi**: 4 giới hạn: Asking vs Transaction price; thiếu VIN; mặt cắt ngang tĩnh; độ lệch vùng miền.
- **Lời thoại trình bày**:
  > *"Chúng em xin nêu rõ 4 giới hạn chính của đề tài để người dùng áp dụng đúng cách:
  > 1. **Giá rao bán vs Giá giao dịch**: Dữ liệu là giá chào trên website, trong khi giá chốt thực tế thường thấp hơn từ 2% đến 5% sau thương lượng.
  > 2. **Thiếu số khung VIN**: Do các sàn xe tại Việt Nam không bắt buộc công khai số VIN, chúng em không thể triệt tiêu 100% trường hợp cùng một chiếc xe vật lý nhưng được 2 salon mô tả khác nhau.
  > 3. **Mặt cắt ngang tĩnh**: Dữ liệu là một lát cắt năm 2023, chưa phản ánh được các biến động vĩ mô như chính sách giảm lệ phí trước bạ theo từng quý.
  > 4. **Cảnh báo ngoại suy xe đời sâu**: Khảo sát độ nhạy trên Cohort B cho thấy mô hình cây không thể ngoại suy cho xe sản xuất trước năm 2015.
  >
  > *Vì vậy, mô hình đóng vai trò là một **Hệ thống hỗ trợ ra quyết định (Decision Support Tool)** định giá mỏ neo tham khảo, chứ không thay thế việc kiểm tra cơ khí trực tiếp ngoài đời thực."*
- **Điểm kỹ thuật nhấn mạnh**: Tính trung thực học thuật (Academic Honesty) khi bảo vệ trước Hội đồng.
- **Câu chuyển slide**:
  > *"Cuối cùng, em xin tóm lược các kết quả đạt được và định hướng phát triển trong tương lai."*

---

### Slide 15: Kết Luận & Định Hướng Phát Triển
- **Thời lượng**: 30 giây
- **Thông điệp cốt lõi**: Hoàn thành trọn vẹn điều lệ; độ bền vững đã được chứng minh; lộ trình tích hợp NLP/Vision và đưa lên Web API.
- **Lời thoại trình bày**:
  > *"Tóm lại, dự án đã hoàn thành xuất sắc tất cả các mục tiêu đề ra:
  > - Xây dựng thành công hệ thống học máy định giá ô tô cũ tại Việt Nam với mô hình vô địch Random Forest Log-Target.
  > - Đạt sai số trung vị MdAPE 4.29% và chứng minh được độ bền vững tuyệt đối qua đợt kiểm định chia nhóm Group-Aware.
  >
  > *Trong tương lai, chúng em định hướng sẽ:
  > 1. Thử nghiệm thêm các thuật toán chuyên sâu như CatBoost và XGBoost.
  > 2. Tích hợp mô hình NLP PhoBERT để đọc option trong bài viết và mô hình Computer Vision để thẩm định ngoại thất xe từ hình ảnh.
  > 3. Đóng gói REST API bằng FastAPI và giao diện Streamlit phục vụ người dùng thực tế.
  >
  > *Em xin chân thành cảm ơn các anh chị Mentor và Hội đồng đã lắng nghe. Em rất sẵn sàng nhận các câu hỏi phản biện từ Hội đồng!"*
- **Điểm kỹ thuật nhấn mạnh**: Phong thái tự tin, tôn trọng Hội đồng, sẵn sàng cho phần Q&A.

---
*Tài liệu kịch bản thuyết trình được thiết kế chuẩn mực, bám sát từng slide và từng giây trình bày, hỗ trợ học viên đạt điểm xuất sắc trong buổi bảo vệ.*
