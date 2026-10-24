# Bộ Câu Hỏi Phản Biện & Câu Trả Lời Mẫu Trước Hội Đồng Mentor (Defense Q&A)
*(Used Car Price Prediction in Vietnam: An End-to-End Machine Learning System)*

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam
- **Học viên**: AI Student
- **Tài liệu phục vụ**: Buổi bảo vệ đồ án kết thúc khóa đào tạo AI Club
- **Cấu trúc**: 26 câu hỏi chuyên sâu chia thành 5 nhóm chủ đề kỹ thuật

---

## Mục Lục Các Nhóm Câu Hỏi (Q&A Categories)

- [Nhóm 1: Bài Toán, Dữ Liệu & Đạo Đức Dữ Liệu (5 câu)](#nhóm-1-bài-toán-dữ-liệu--đạo-đức-dữ-liệu)
- [Nhóm 2: EDA, Tiền Xử Lý & Kỹ Nghệ Đặc Trưng (5 câu)](#nhóm-2-eda-tiền-xử-lý--kỹ-nghệ-đặc-trưng)
- [Nhóm 3: Mô Hình Hóa, Thuật Toán & Thước Đo Đánh Giá (5 câu)](#nhóm-3-mô-hình-hóa-thuật-toán--thước-đo-đánh-giá)
- [Nhóm 4: Rò Rỉ Dữ Liệu, Trùng Lặp & Đánh Giá Độ Bền Nhóm (6 câu)](#nhóm-4-rò-rỉ-dữ-liệu-trùng-lặp--đánh-giá-độ-bền-nhóm)
- [Nhóm 5: Kỹ Thuật Phần Mềm, Giới Hạn & Triển Khai Thực Tiễn (5 câu)](#nhóm-5-kỹ-thuật-phần-mềm-giới-hạn--triển-khai-thực-tiễn)

---

## Nhóm 1: Bài Toán, Dữ Liệu & Đạo Đức Dữ Liệu

### Câu 1: Tại sao nhóm không tự crawl dữ liệu trực tiếp từ các website xe hơi mà lại sử dụng dataset thứ cấp từ Kaggle?
**Trả lời của học viên:**
> *"Thưa Mentor, ở các giai đoạn đầu (Phase 1 đến Phase 3.1), chúng em đã lập trình và hoàn thiện thành công bộ thu thập dữ liệu kiểm thử tại [`src/data/crawler.py`](file:///d:/ai-club-end-training/src/data/crawler.py) có kiểm thử đầy đủ.
>
> Tuy nhiên, khi phân tích an toàn kỹ thuật và tệp `robots.txt` của các sàn xe lớn tại Việt Nam, chúng em nhận thấy:
> 1. Các website áp dụng giải pháp tường lửa Cloudflare WAF với cơ chế chống bot và rate-limiting nghiêm ngặt; việc cào hàng chục ngàn tin đăng trong thời gian ngắn đối mặt với rủi ro bị chặn IP diện rộng.
> 2. Về mặt đạo đức mạng, việc gửi lượng lớn request liên tục gây quá tải hạ tầng của doanh nghiệp ngoài ý muốn.
> 3. Bộ dữ liệu Kaggle Bonbanh do tác giả Mai Quốc Ân công bố theo giấy phép CC0 Public Domain gồm 30,652 tin đăng có cấu trúc trường thông tin phong phú và tính lịch sử ổn định.
>
> Chúng em đã lập báo cáo đánh giá rủi ro kỹ thuật ([`docs/data_source_audit.md`](file:///d:/ai-club-end-training/docs/data_source_audit.md)) và đã được Mentor phê duyệt chính thức chuyển đổi sang nguồn thứ cấp. Module `crawler.py` vẫn được giữ nguyên trong kho lưu trữ với unit tests pass 100% để sẵn sàng kích hoạt khi có hạ tầng proxy chuyên dụng."*

---

### Câu 2: Tại sao lại chọn Cohort A là các xe từ năm 2015 trở lại đây ($\text{year} \ge 2015$) thay vì huấn luyện trên toàn bộ dữ liệu từ năm 1990?
**Trả lời của học viên:**
> *"Thưa Mentor, quyết định giới hạn Cohort A dựa trên 3 căn cứ khoa học và thực tiễn:
> 1. **Tính đại diện thanh khoản thị trường**: Theo khảo sát EDA tại Phase 4, các xe sản xuất từ năm 2015 đến 2023 chiếm tới **76.7% tập dữ liệu** (23,510 xe) và phản ánh hơn 85% lượng giao dịch thực tế trên thị trường xe cũ hiện nay.
> 2. **Tính đồng nhất cơ khí và công nghệ**: Xe từ 2015 trở lại đây có công nghệ động cơ, hộp số tự động, tiêu chuẩn khí thải (Euro 4/5) và trang bị an toàn tương đối đồng nhất. Đối với các xe đời quá sâu (trước 2010), mức độ thoái hóa linh kiện và lịch sử đâm đụng phụ thuộc vào từng xe cá biệt, khiến giá xe không còn tuân theo quy luật bảng thông số chuẩn.
> 3. **Kiểm chứng độ nhạy trên Cohort B**: Chúng em không bỏ rơi xe cũ mà đã thiết lập thí nghiệm độ nhạy độc lập trên Cohort B (2010–2023, 27,299 xe). Thí nghiệm này cho thấy khi áp dụng trực tiếp mô hình Cohort A vào xe đời 2010–2014, MAE vọt lên 314 triệu và MdAPE lên 29.6% do mô hình cây không thể ngoại suy ngoài miền năm đã học. Việc phân định rõ Cohort A giúp khoanh vùng ranh giới tin cậy cho bài toán."*

---

### Câu 3: Nhóm đã xử lý các vấn đề về Đạo đức Dữ liệu và Quyền riêng tư (PII) như thế nào trong dự án?
**Trả lời của học viên:**
> *"Thưa Mentor, chúng em áp dụng nguyên tắc 'Privacy by Design' xuyên suốt:
> 1. **Khử danh tính bằng Biểu thức chính quy (Regex De-identification)**: Toàn bộ số điện thoại cá nhân của chủ xe, tên người bán, đường link URL và địa chỉ chi tiết xuất hiện trong văn bản mô tả đều được bóc tách và loại bỏ trước khi dữ liệu được lập chỉ mục hoặc phân cụm.
> 2. **Chặn cột văn bản thô khỏi mô hình**: Các cột `Mô tả`, `Tên xe`, `url`, `listing_id` bị cấm tuyệt đối tham gia vào ma trận đặc trưng $X$, loại bỏ hoàn toàn khả năng mô hình ghi nhớ thông tin cá nhân.
> 3. **Bảo vệ mã nguồn mở**: Không lưu trữ các thông tin liên lạc nhạy cảm trong bất kỳ báo cáo, slide hay commit nào của dự án."*

---

### Câu 4: Trường `engine_displacement_l` bị khuyết thiếu ở 0.43% dòng. Cơ chế khuyết thiếu ở đây là gì (MCAR, MAR hay MNAR) và nhóm xử lý ra sao?
**Trả lời của học viên:**
> *"Thưa Mentor, cơ chế khuyết thiếu của `engine_displacement_l` ở đây là **Missing Not at Random (MNAR)** kết hợp với một tỷ lệ nhỏ **Missing at Random (MAR)**:
> 1. **MNAR (Khuyết thiếu do bản chất kỹ thuật)**: Khoảng 40% các trường hợp khuyết dung tích xi-lanh là **xe thuần điện (Electric Vehicles)** như Porsche Taycan, Tesla Model 3, VinFast VF8/VF9. Động cơ điện không có xi-lanh nên dung tích động cơ bằng 0 lít về mặt vật lý.
> 2. **MAR (Người bán không điền)**: Một số tin rao người bán chỉ ghi tên bản (ví dụ: 'Mazda 3 Luxury') mà quên chọn dung tích.
>
> Chúng em đã xử lý bằng cách:
> - Tách biệt dòng xe điện để gán giá trị 0.0L kèm cờ chỉ thị khuyết thiếu.
> - Đối với các dòng xe xăng/dầu truyền thống, `SimpleImputer(strategy='median', add_indicator=True)` được fit trên tập Train, vừa điền giá trị trung vị vừa tạo thêm một cột cờ nhị phân `missingindicator_engine_displacement_l` giúp mô hình cây nhận biết được việc người bán có cung cấp thông số hay không."*

---

### Câu 5: Bộ dữ liệu Kaggle Bonbanh này được thu thập tại thời điểm nào và có nguy cơ trôi dạt dữ liệu (Data Drift) theo thời gian không?
**Trả lời của học viên:**
> *"Thưa Mentor, bộ dữ liệu là một mặt cắt ngang (Cross-sectional snapshot) được thu thập vào khoảng quý 3 năm 2023.
> 
> Trong thế giới thực, dữ liệu này chắc chắn đối mặt với **Concept Drift** và **Data Drift**:
> - **Data Drift**: Tỷ trọng xe điện (VinFast, BYD) tại Việt Nam đang tăng nhanh từ cuối năm 2023 đến nay.
> - **Concept Drift**: Các đợt hỗ trợ giảm 50% lệ phí trước bạ của Chính phủ (ví dụ Nghị định 41/2023 và 109/2024) hoặc các đợt giảm giá kích cầu xe mới của hãng làm thay đổi mặt bằng giá xe cũ.
> 
> Chúng em đã ghi nhận đây là một trong các giới hạn học thuật hàng đầu của đề tài (Slide 14) và đề xuất giải pháp triển khai cơ chế thu thập dữ liệu định kỳ để cập nhật mô hình theo từng quý."*

---

## Nhóm 2: EDA, Tiền Xử Lý & Kỹ Nghệ Đặc Trưng

### Câu 6: Tại sao các giá trị ODO $> 1,000,000$ km lại được gán trung vị thay vì xóa bỏ khỏi tập dữ liệu?
**Trả lời của học viên:**
> *"Thưa Mentor, khi rà soát dữ liệu, chúng em phát hiện 70 dòng có ODO từ 1,000,000 km đến 9,999,999 km (ví dụ các dãy số `999999`, `1234567`). Đây rõ ràng là lỗi nhập liệu do người bán gõ phím cho nhanh hoặc cố tình giấu ODO thực.
> 
> Nếu chúng ta chọn giải pháp 'tiện tay xóa bỏ', chúng ta sẽ vi phạm tính toàn vẹn của tập mẫu, vì 70 chiếc xe này có đầy đủ các thông số quan trọng khác (Hãng, Model, Năm sản xuất, Giá rao bán hoàn toàn hợp lý). Hơn nữa, trong môi trường sản xuất thực tế khi người dùng nhập thông tin sai, mô hình không thể 'từ chối chạy'.
> 
> Do đó, chúng em áp dụng chính sách gán giá trị trung vị có điều kiện theo nhóm tuổi xe (`car_age`) và phân khúc. Điều này bảo toàn 100% kích thước mẫu Cohort A đạt 23,510 xe, đồng thời loại bỏ hoàn toàn ảnh hưởng của giá trị ngoại lai cực đoan lên hàm tính toán khoảng cách."*

---

### Câu 7: Tại sao lại cần tạo riêng cờ `is_zero_mileage` và nhãn `condition = 'Xe mới'`? Chúng có gây nhiễu cho bài toán xe cũ không?
**Trả lời của học viên:**
> *"Thưa Mentor, đây là một phát hiện nghiệp vụ rất quan trọng tại Phase 5:
> - Có tới **6,066 xe (25.8% tập dữ liệu)** có số ODO đúng bằng 0 km và được các showroom đăng bán dưới dạng xe mới 100% nguyên bản chưa lăn bánh theo giá niêm yết của hãng.
> - Nếu chúng ta để ODO = 0 mà không có biến cờ phân tách, mô hình sẽ coi đây là 'xe cũ đi siêu ít' và có thể nội suy sai lệch đường cong khấu hao (depreciation curve) của xe đã qua sử dụng.
> 
> Việc tạo cờ nhị phân `is_zero_mileage = 1` và gán nhãn `condition = 'Xe mới'` đóng vai trò như một cơ chế phân tầng (Stratification feature), giúp mô hình cây tạo ra một nhánh rẽ độc lập: nhánh dự đoán xe mới tại đại lý theo giá hãng, và nhánh dự đoán xe cũ theo mức độ hao mòn cơ học thực tế. Điều này giúp độ chính xác của cả hai phân khúc đều tăng lên rõ rệt."*

---

### Câu 8: Tại sao nhóm lại lựa chọn biến đổi Logarit $y_{\text{log}} = \ln(\text{price\_vnd})$ thay vì để mô hình học trực tiếp trên đơn vị VND?
**Trả lời của học viên:**
> *"Thưa Mentor, quyết định này dựa trên nền tảng toán học của hàm tối ưu hóa sai số:
> 1. **Ổn định phương sai (Variance Stabilization)**: Phân phối giá xe lệch phải nặng với dải giá từ 55 triệu đến 45 tỷ. Biến đổi logarit nén dải động khổng lồ này về khoảng giá trị hẹp $[17.8, 24.5]$, đưa phân phối về dạng chuẩn Gauss.
> 2. **Chuyển hóa sai số tuyệt đối sang sai số tỷ đối**: Khi mô hình tối ưu hóa hàm tổn thất Mean Squared Error trên không gian logarit:
>    $$\mathcal{L} = \frac{1}{n}\sum (\ln(y) - \ln(\hat{y}))^2 = \frac{1}{n}\sum \left(\ln\frac{y}{\hat{y}}\right)^2 \approx \frac{1}{n}\sum \left(\frac{y - \hat{y}}{y}\right)^2$$
>    sai số bình phương trên không gian log xấp xỉ bình phương sai số phần trăm tương đối!
> 3. **Bảo vệ phân khúc xe phổ thông**: Nếu huấn luyện trên giá thô VND, một sai số 2 tỷ trên chiếc xe siêu sang 40 tỷ sẽ tạo ra tổn thất $(2 \times 10^9)^2 = 4 \times 10^{18}$, áp đảo hoàn toàn tổn thất của một chiếc xe Vios 500 triệu. Kết quả là mô hình tuyến tính trên Raw VND bị lệch nặng (MdAPE lên tới 23.72%). Khi chuyển sang Log Target, MdAPE của Ridge lập tức giảm xuống chỉ còn 7.72%!"*

---

### Câu 9: Ma trận đặc trưng có 15 biến, trong đó biến `model` có tới 451 giá trị danh mục khác nhau (High Cardinality). Làm sao One-Hot Encoding không gây bùng nổ chiều dữ liệu (Curse of Dimensionality)?
**Trả lời của học viên:**
> *"Thưa Mentor, biến `model` quả thực có 451 giá trị danh mục. Khi áp dụng `OneHotEncoder`, ma trận thưa sau biến đổi mở rộng lên 506 cột.
> 
> Chúng em đã kiểm soát vấn đề này thông qua 3 giải pháp:
> 1. **Sử dụng ma trận thưa (Scipy CSR Sparse Matrix)**: Giúp tối ưu hóa bộ nhớ RAM, toàn bộ ma trận huấn luyện 18,808 dòng chỉ tốn chưa đầy 15 MB RAM.
> 2. **Kiểm soát độ sâu và kích thước lá của Random Forest**: Cấu hình `max_depth=24` và `min_samples_leaf=1` giúp cây quyết định không bị phân nhánh quá sâu vào các danh mục rác có số lượng mẫu dưới 2 dòng.
> 3. **Tùy chọn `handle_unknown='ignore'`**: Đảm bảo an toàn 100% khi tập Test xuất hiện các dòng xe trim mới lạ chưa từng gặp trong Train.
> 
> Trong tương lai, chúng em định hướng áp dụng Target Encoding hoặc CatBoost để mã hóa biến danh mục này gọn gàng hơn mà không cần tăng số chiều."*

---

### Câu 10: Nhóm đã xây dựng bộ phân tích cú pháp giá (Price Parser) như thế nào để xử lý các chuỗi văn bản giá phức tạp trong tiếng Việt?
**Trả lời của học viên:**
> *"Thưa Mentor, trong tệp thô, trường giá chứa các định dạng chuỗi tự do tiếng Việt như: `'720 Triệu'`, `'1 Tỷ 350 Triệu'`, `'2.45 Tỷ'`, `'Thương lượng'`, hoặc `'123 Triệu'`.
> 
> Chúng em đã thiết kế hàm tất định [`src/data/price_parser.py`](file:///d:/ai-club-end-training/src/data/cleaning.py) sử dụng biểu thức chính quy:
> 1. Nhận diện các từ khóa chỉ đơn vị tiền tệ `'tỷ'` hoặc `'tỉ'` $\rightarrow$ nhân với $10^9$; `'triệu'` hoặc `'tr'` $\rightarrow$ nhân với $10^6$.
> 2. Phân tách và cộng dồn phần nguyên và phần thập phân (ví dụ: `'1 Tỷ 350 Triệu'` $\rightarrow 1 \times 10^9 + 350 \times 10^6 = 1,350,000,000\text{ VND}$).
> 3. Lọc bỏ các chuỗi không chứa giá trị số (gán NaN) và loại bỏ các giá trị dưới 10 triệu VND (vốn là tiền đặt cọc hoặc số ảo).
> 
> Bộ phân tích này được kiểm thử tự động với 10 unit tests độc lập tại [`tests/test_price_parser.py`](file:///d:/ai-club-end-training/tests/test_price_parser.py) và đạt độ chính xác 100%."*

---

## Nhóm 3: Mô Hình Hóa, Thuật Toán & Thước Đo Đánh Giá

### Câu 11: Tại sao `Tree_RandomForest_Tuned_LogTarget` lại vượt trội hơn hẳn so với Hồi quy Tuyến tính Ridge và HistGradientBoosting?
**Trả lời của học viên:**
> *"Thưa Mentor, sự vượt trội của mô hình Random Forest tuned trên Log Target bắt nguồn từ bản chất bài toán định giá ô tô:
> 1. **Khả năng mô hình hóa quan hệ phi tuyến và tương tác bậc cao**: Giá ô tô phụ thuộc vào sự kết hợp chặt chẽ giữa các yếu tố: ví dụ cùng dung tích 2.0L nhưng nếu là Mercedes C300 thì giá 1.8 tỷ, còn nếu là Hyundai Tucson thì giá chỉ 800 triệu. Mô hình tuyến tính không thể học được tương tác này trừ khi ta sinh biến nhân chéo thủ công. Trong khi đó, Random Forest tự động tìm kiếm các điểm cắt tương tác thông qua cấu trúc phân nhánh cây.
> 2. **Cơ chế Ensemble giảm phương sai**: Rừng ngẫu nhiên với 150 cây kết hợp Bootstrap Aggregating (Bagging) giúp làm mượt các dự đoán và triệt tiêu phương sai cá biệt của từng cây đơn lẻ.
> 3. **So với HistGradientBoosting**: HistGBM sử dụng kỹ thuật ép giỏ (binning 256 bins) cho các biến số, giúp tăng tốc độ huấn luyện nhưng lại làm mất đi tính liên tục mịn của các biến ODO và Dung tích động cơ ở các vùng lân cận. Do đó, Random Forest đạt MdAPE 4.25% tốt hơn HistGBM (5.37%)."*

---

### Câu 12: Tại sao mô hình Hồi quy Tuyến tính Ridge trên Raw Target đạt $R^2 = 0.8075$ (khá cao) nhưng sai số MAE lại lên tới 379.4 triệu VND và MdAPE lên tới 23.72%?
**Trả lời của học viên:**
> *"Thưa Mentor, đây là một ví dụ kinh điển về **'Cạm bẫy của chỉ số R²'** trong phân phối lệch phải:
> - Hệ số $R^2 = 1 - \frac{\text{SS}_{\text{res}}}{\text{SS}_{\text{tot}}}$ đo lường tỷ lệ phương sai giải thích được. Do tổng phương sai $\text{SS}_{\text{tot}}$ bị phóng đại khổng lồ bởi các xe siêu sang (40 tỷ), mô hình Ridge chỉ cần dự đoán tương đối đúng xu hướng của vài chục chiếc xe siêu sang là đã đạt được $R^2 > 0.80$.
> - Tuy nhiên, hàm tổn thất bình phương của Ridge phạt cực nặng các sai số lớn tính bằng tiền tuyệt đối. Để giảm thiểu sai số của một chiếc xe 20 tỷ, mô hình chấp nhận kéo lệch đường hồi quy, dẫn tới việc dự đoán một chiếc Toyota Vios 500 triệu thành 700 triệu (lệch 200 triệu, tương đương 40% giá trị xe!).
> - Kết quả là sai số trung vị tương đối MdAPE vọt lên 23.72% — nghĩa là đối với đa số xe phổ thông trên thị trường, mô hình bị lệch tới gần 1/4 giá trị xe. Điều này chứng minh ta không bao giờ được dựa duy nhất vào $R^2$ để đánh giá mô hình định giá."*

---

### Câu 13: Tại sao nhóm lại lựa chọn MdAPE (Median Absolute Percentage Error) làm thước đo nghiệp vụ then chốt thay vì MAE hay RMSE?
**Trả lời của học viên:**
> *"Thưa Mentor, chúng em lựa chọn MdAPE làm mỏ neo nghiệp vụ hàng đầu vì 3 lý do:
> 1. **Kháng ngoại lai tuyệt đối (Robustness to Outliers)**: Trong tập dữ liệu có xe 55 triệu và xe 45 tỷ, chỉ số RMSE và MAE bị kéo lệch rất mạnh bởi một vài xe siêu sang hiếm gặp (như trường hợp 1 xe siêu sang ở tập Val kéo MAE toàn tập tăng thêm 15.2M VND). Chỉ số trung vị (Median) loại bỏ hoàn toàn ảnh hưởng của chiếc đuôi ngoại lai này.
> 2. **Tính công bằng giữa các phân khúc (Scale-Invariance)**: Sai số 50 triệu trên một chiếc Morning 300 triệu (sai số 16.7%) là không thể chấp nhận được với người mua; nhưng sai số 50 triệu trên một chiếc Porsche 5 tỷ (sai số 1%) lại là một dự đoán cực kỳ xuất sắc. Thước đo tỷ đối phần trăm giúp đánh giá công bằng chất lượng dự báo trên mọi dải phân khúc.
> 3. **Gắn liền trực tiếp với biên độ mặc cả thị trường**: Mức MdAPE **4.25% (Val)** và **4.29% (Test)** nằm trọn vẹn trong biên độ thương lượng 3%–5% của thị trường xe cũ Việt Nam, mang lại ý nghĩa kinh tế thiết thực cho người dùng cuối."*

---

### Câu 14: Tại sao Test MAE của Champion Model (111.8M VND) lại thấp hơn đáng kể so với Validation MAE (142.9M VND)? Liệu có hiện tượng 'may mắn' hoặc rò rỉ ở đây?
**Trả lời của học viên:**
> *"Thưa Mentor, nghi vấn này đã được nhóm kiểm toán độc lập thẩm định kỹ lưỡng tại Phase 6.1:
> - Sự chênh lệch **hoàn toàn không phải do mô hình tổng quát hóa vượt trội hay do rò rỉ dữ liệu**.
> - Nguyên nhân nằm ở **độ phân tán ngoại lai của các xe siêu sang $> 5$ tỷ VND**:
>   - Tập Validation ngẫu nhiên nhận 1 chiếc xe siêu sang có giá **38.999 tỷ VND**, nhưng mô hình chỉ dự đoán là **3.247 tỷ VND** (sai số lệch tới **35.75 tỷ VND** trên 1 dòng duy nhất). Chiếc xe cá biệt này tự nó đã đóng góp thêm:
>     $$\frac{35,752,000,000}{2,351} \approx \mathbf{15.2\text{ triệu VND}}$$
>     vào MAE trung bình của toàn bộ 2,351 xe trong tập Validation!
>   - Trong khi đó, ở tập Test, chiếc xe có sai số lớn nhất chỉ lệch 9.3 tỷ VND.
> - Bằng chứng quyết định: Khi chúng em bóc tách phân khúc xe phổ thông ($\le 1$ tỷ VND, chiếm 70% dữ liệu), MAE giữa Validation và Test hoàn toàn trùng khớp (**Val: 25.5M / 40.8M** vs **Test: 26.1M / 40.4M**).
> - Đồng thời, sai số trung vị tương đối MdAPE của hai tập gần như bằng nhau tuyệt đối: **4.25% (Val) vs 4.29% (Test)**. Điều này chứng minh hiệu năng thực chất của mô hình trên xe đại chúng là tương đương 100%."*

---

### Câu 15: Nếu áp dụng Champion Model này cho các xe sản xuất trước năm 2015 (ví dụ đời 2010–2012), chuyện gì sẽ xảy ra?
**Trả lời của học viên:**
> *"Thưa Mentor, đây chính là **Rủi ro Ngoại suy (Extrapolation Risk)** của họ mô hình cây quyết định:
> - Các mô hình cây (Random Forest, Decision Tree) phân chia không gian đặc trưng bằng các đường cắt trực giao song song với các trục tọa độ. Do đó, khi gặp một giá trị năm sản xuất nằm ngoài miền huấn luyện (ví dụ `year = 2011`, trong khi Train chỉ học từ $[2015, 2023]$), mô hình cây sẽ rơi vào lá ngoài cùng bên trái và dự đoán giá của năm 2015!
> - Thực nghiệm phân tích độ nhạy Cohort B tại Phase 6 đã chứng minh điều này: Khi áp dụng trực tiếp model Cohort A vào 3,789 xe đời 2010–2014, MAE vọt lên **314.1 triệu VND** và MdAPE lên tới **29.64%** (dự đoán đắt hơn nhiều so với giá trị thực tế của xe cũ đời sâu).
> - Tuy nhiên, nếu chúng ta tái huấn luyện Random Forest trên toàn bộ dữ liệu Cohort B (gồm cả các năm 2010–2014), Test MAE lại đạt mức xuất sắc **110.6 triệu VND** và $R^2 = 0.9567$.
> - Vì vậy, chúng em đưa ra khuyến cáo ranh giới sử dụng rõ ràng: Mô hình hiện tại chỉ an toàn cho xe sản xuất từ năm 2015 trở lại đây."*

---

## Nhóm 4: Rò Rỉ Dữ Liệu, Trùng Lặp & Đánh Giá Độ Bền Nhóm

### Câu 16: Nhóm đã thực hiện các biện pháp kỹ thuật nào để đảm bảo không xảy ra rò rỉ dữ liệu (Zero Data Leakage) trong toàn bộ quy trình?
**Trả lời của học viên:**
> *"Thưa Mentor, chúng em áp dụng nguyên tắc phòng vệ theo chiều sâu (Defense-in-Depth) với 4 lớp kiểm soát:
> 1. **Kiểm soát định danh**: 100% `listing_id` rời rạc giữa Train, Validation và Test (được xác thực bằng unit test).
> 2. **Chặn đặc trưng rò rỉ**: 9 cột nhạy cảm (`price_vnd`, `log_price`, `Giá`, `Mã tin`, `url`, `Mô tả`, `Tên xe`,...) bị loại bỏ khỏi ma trận đặc trưng $X$.
> 3. **Cách ly tuyến tiền xử lý (Pipeline Isolation)**: Toàn bộ các bước chuẩn hóa (Imputer, Scaler, One-Hot Encoder) chỉ được gọi `.fit()` duy nhất trên tập Train. Validation và Test chỉ được gọi `.transform()`.
> 4. **Đóng băng mô hình trước khi Test**: Siêu tham số được tinh chỉnh duy nhất trên Validation; tập Test được niêm phong kín và chỉ mở ra đánh giá duy nhất một lần sau khi đã chốt Champion Model."*

---

### Câu 17: Hiện tượng 'Rò rỉ Đăng chéo tin' (Cross-Posting Leakage) được phát hiện như thế nào tại Phase 6.1?
**Trả lời của học viên:**
> *"Thưa Mentor, tại Phase 6.1, khi thực hiện kiểm toán độc lập mã nguồn, chúng em không chỉ kiểm tra cột `listing_id` mà đã chạy thuật toán băm dấu vân tay văn bản (Text Fingerprint Hashing) trên cột `Mô tả`.
> 
> Kết quả kiểm toán phát hiện:
> - Khoảng **8.21% dòng trong tập Test và 8.76% dòng trong tập Validation có văn bản mô tả trùng khớp từng ký tự với một tin đăng trong tập Train**.
> - Nguyên nhân xuất phát từ hành vi thực tế của các salon ô tô: Một showroom tạo nhiều tài khoản khác nhau trên sàn Bonbanh để đăng cùng một chiếc xe nhằm tăng lượt tiếp cận, hoặc các showroom đối tác sao chép nguyên văn nội dung quảng cáo của nhau.
> - Mặc dù cột `Mô tả` đã bị loại khỏi ma trận $X$, nhưng sự tồn tại của các tin đăng gần như nhân bản giữa Train và Test đặt ra nghi vấn: Liệu mô hình có đang hưởng lợi từ việc học các cấu hình xe giống hệt nhau hay không? Đây là lý do Phase 6.2 được triển khai ngay sau đó."*

---

### Câu 18: Hãy phân biệt rạch ròi giữa 'Specification Overlap' và 'Cross-Posting Duplicate'. Cái nào là rò rỉ, cái nào là đặc tính phân phối?
**Trả lời của học viên:**
> *"Thưa Mentor, đây là điểm phương pháp luận tối quan trọng mà chúng em đã bảo vệ trong báo cáo:
> 1. **Cross-Posting Duplicate (Trùng lặp bài đăng)**: Là trường hợp hai tin đăng khác ID nhưng chung nội dung mô tả, chung số điện thoại hoặc chung một chiếc xe vật lý cụ thể ngoài đời thực. Đây là **Rò rỉ dữ liệu tiềm ẩn (Potential Leakage)** cần phải gom nhóm và cách ly.
> 2. **Specification Overlap (Trùng lặp thông số phiên bản)**: Là trường hợp hai chiếc xe khác nhau nhưng có cùng tổ hợp thông số kỹ thuật (ví dụ: cùng là Toyota Vios 2020 1.5 AT màu trắng). Tại Việt Nam, Toyota bán ra hơn 20,000 chiếc Vios 2020 mỗi năm, nên việc tập Test có 95.8% cấu hình phiên bản đã xuất hiện trong Train là **Đặc tính phân phối tự nhiên của dữ liệu dạng bảng (I.I.D. Tabular Distribution)**, hoàn toàn không phải rò rỉ dữ liệu!
> 
> Nếu chúng ta ép buộc tập Test chỉ được chứa các dòng xe chưa từng có trong Train, chúng ta đang biến bài toán thành Zero-Shot Cold-Start Prediction — một bài toán phi thực tế đối với ứng dụng định giá thị trường."*

---

### Câu 19: Thuật toán `StratifiedGroupKFold` trong Phase 6.2 đã hoạt động như thế nào để cách ly các cụm tin đăng trùng?
**Trả lời của học viên:**
> *"Thưa Mentor, quy trình chia nhóm tại Phase 6.2 diễn ra theo 3 bước:
> 1. **Gom cụm bằng thuật toán phân tầng 4 cấp độ**: Chúng em tạo mã định danh nhóm `record_group_id`. Với 903 cụm `HIGH_CONFIDENCE_DUPLICATE` (2,430 xe trùng fingerprint mô tả $\ge 50$ ký tự VÀ cùng Hãng, Dòng xe, Năm sản xuất), tất cả các xe trong cùng cụm được gán chung một `record_group_id`. Các tin độc lập giữ ID đơn lẻ. Tổng cộng có 21,983 nhóm độc lập.
> 2. **Phân chia bằng `StratifiedGroupKFold(n_splits=10, shuffle=True, random_state=42)`**:
>    - Thuật toán đảm bảo điều kiện ràng buộc nhóm: **Toàn bộ các xe có chung `record_group_id` bắt buộc phải nằm trọn vẹn trong một tập duy nhất** (hoặc toàn bộ trong Train, hoặc toàn bộ trong Val, hoặc toàn bộ trong Test).
>    - Đồng thời, thuật toán cố gắng cân bằng phân tầng theo 10 phân vị giá `price_vnd`.
> 3. **Xác minh mã băm và đối soát**: Sau khi chia thành công (Train: 18,809 dòng; Val: 2,351 dòng; Test: 2,350 dòng), chúng em kiểm tra giao của tập hợp group ID giữa 3 tập: **Tỷ lệ trùng lặp group ID đạt chuẩn xác 0.00% (0 cụm bị cắt xẻ)**."*

---

### Câu 20: Tại sao khi đánh giá trên tập Test Group-Aware (không còn tin trùng), chỉ số MdAPE vẫn giữ vững chuẩn xác ở mức 4.29%, trong khi MAE lại tăng từ 111.8M lên 130.8M VND?
**Trả lời của học viên:**
> *"Thưa Mentor, đây chính là phát hiện thực nghiệm mang giá trị khoa học cao nhất của đồ án:
> 
> 1. **Tại sao MdAPE giữ vững 4.29%?**
>    - MdAPE là thước đo trung vị. Việc MdAPE giữ nguyên không đổi (4.29% ở Phase 6 và đúng 4.29% ở Phase 6.2) chứng minh một cách không thể chối cãi rằng: **Độ chính xác của mô hình trên đa số xe phổ thông là hoàn toàn thực chất**, mô hình thực sự học được quy luật khấu hao và định giá, chứ không hề dựa dẫm vào việc học vẹt các tin đăng trùng!
> 
> 2. **Tại sao MAE lại tăng 18.9 triệu VND (từ 111.8M lên 130.8M)?**
>    - Khi phân rã sai số theo phân khúc giá (Slide 11), chúng em phát hiện: Ở phân khúc xe phổ thông dưới 500 triệu, MAE của tập chia nhóm thậm chí còn **thấp hơn** Phase 6: **24.2 triệu VND** (so với 26.1M). Xe từ 500M đến 1 tỷ giữ nguyên ở mức **40.5 triệu VND**.
>    - Mức tăng 18.9M của tổng MAE bắt nguồn hoàn toàn từ việc tập Test Group-Aware ngẫu nhiên nhận **thêm 27 chiếc xe siêu sang $> 5$ tỷ VND** (117 xe so với 90 xe của Phase 6).
>    - Do phân khúc xe siêu sang có sai số trung bình là 1.264 tỷ VND, việc có thêm 27 chiếc xe này đã đóng góp thêm:
>      $$\frac{27 \times 1,264,844,707}{2,350} \approx \mathbf{14.5\text{ triệu VND}}$$
>      vào MAE trung bình của toàn bộ tập Test!
>    - Phép tính phân rã này chứng minh mức tăng MAE là do đặc thù phân bổ xe ngoại lai cực đoan của phép chia cụm, không phải do mô hình bị suy giảm năng lực định giá."*

---

### Câu 21: Nếu có một người bán cố tình viết lại toàn bộ bài mô tả cho một chiếc xe cũ vật lý để đăng lên hai sàn khác nhau, hệ thống của nhóm có phát hiện được không?
**Trả lời của học viên:**
> *"Thưa Mentor, đây là một câu hỏi rất sâu sắc về bản chất dữ liệu:
> - Nếu người bán viết lại 100% bài mô tả với ngôn từ khác biệt hoàn toàn và thay đổi cả số điện thoại liên hệ, thì dựa trên các đặc trưng bảng hiện có, thuật toán gom cụm văn bản sẽ xếp trường hợp này vào nhóm `POSSIBLE_DUPLICATE` (nếu trùng 5 thông số: Hãng, Model, Năm, ODO, Giá) hoặc `UNRELATED`.
> - Do các sàn giao dịch ô tô trực tuyến tại Việt Nam không bắt buộc người bán công khai **Số khung (VIN)** hoặc **Biển kiểm soát**, về mặt lý thuyết thông tin, không có bất kỳ thuật toán NLP hay phân cụm nào có thể khẳng định chắc chắn 100% hai tin đăng đó là cùng một chiếc xe vật lý ngoài đời thực.
> - Chúng em đã nhìn nhận thẳng thắn đây là một 'Threat to Validity' mang tính khách quan của toàn ngành xe cũ (Slide 14) và đã kiểm soát bằng cách xây dựng quy trình kiểm toán 4 cấp độ thận trọng nhất có thể."*

---

## Nhóm 5: Kỹ Thuật Phần Mềm, Giới Hạn & Triển Khai Thực Tiễn

### Câu 22: Tại sao trong Báo cáo Phase 6.1 nhóm lại phải đính chính thuật ngữ 'Gini Importance' thành 'Mean Decrease in Impurity (MDI)'?
**Trả lời của học viên:**
> *"Thưa Mentor, đây là minh chứng cho tinh thần kiểm toán khoa học nghiêm túc của nhóm:
> - Trong một số tài liệu học tập sơ cấp, người ta thường quen miệng gọi thuộc tính `feature_importances_` của Scikit-Learn là 'Gini Importance'.
> - Tuy nhiên, về mặt toán học:
>   - **Gini Impurity** ($\sum p_k(1-p_k)$) chỉ tồn tại trong các bài toán **Phân loại (Classification)** để đo độ thuần khiết của các nhãn rời rạc.
>   - Trong bài toán **Hồi quy (Regression)**, hàm mục tiêu phân nhánh của cây quyết định là **Cực tiểu hóa phương sai (Variance Reduction / Mean Squared Error Reduction)**.
> - Do đó, việc gọi là 'Gini Importance' trong bài toán dự đoán giá xe là sai lệch bản chất toán học. Nhóm kiểm toán đã đính chính chính xác thuật ngữ thành **Mean Decrease in Impurity (MDI / Độ giảm phương sai)** và bổ sung thêm phép đo độc lập **Permutation Feature Importance** để đối chứng."*

---

### Câu 23: Tại sao biến ODO (`mileage_km`) chỉ chiếm 0.69% MDI trong cây ngẫu nhiên? Phải chăng số km lăn bánh không quan trọng khi mua xe cũ?
**Trả lời của học viên:**
> *"Thưa Mentor, ODO cực kỳ quan trọng, nhưng chúng ta cần phân biệt giữa **Tầm quan trọng toàn cục (Global Importance)** và **Độ nhạy cục bộ (Local Sensitivity)**:
> 1. **Góc nhìn toàn cục (Global Perspective)**: Dữ liệu bao trùm toàn bộ thị trường từ Kia Morning 300 triệu đến Lexus LX600 12 tỷ. Sự khác biệt về Thương hiệu (`is_luxury_brand` - 43.1%) và Dung tích máy (`engine_displacement_l` - 26.35%) tạo ra khoảng cách giá hàng tỷ đồng, áp đảo hoàn toàn sự biến thiên giá vài chục triệu tạo ra bởi số ODO. Một chiếc Lexus đi 150,000 km vẫn đắt gấp nhiều lần một chiếc Vios đi 0 km. Do đó, ở các tầng phân nhánh đầu tiên của cây, mô hình luôn chọn thương hiệu và động cơ để chia tách.
> 2. **Góc nhìn cục bộ (Local Perspective)**: Khi mô hình đã đi xuống các nhánh lá sâu — nơi phân khúc đã được cố định (ví dụ: cùng là Mazda CX-5 2.0 AT đời 2020) — ODO trở thành biến số quyết định mức chênh lệch 30 – 50 triệu VND giữa xe chạy gia đình 3 vạn km và xe chạy dịch vụ 12 vạn km.
> 
> Vì vậy, tỷ trọng MDI 0.69% phản ánh đúng vị thế của ODO là một biến số tinh chỉnh giá ở cấp độ chi tiết, chứ không phải biến phân tầng vĩ mô."*

---

### Câu 24: Giá trong tập dữ liệu là 'Giá chào bán' (Asking Price), trong khi giao dịch thực tế luôn có mặc cả. Làm sao mô hình giải quyết khoảng cách này?
**Trả lời của học viên:**
> *"Thưa Mentor, đây là một đặc thù lớn của bài toán định giá dựa trên web:
> - Giá niêm yết trên website là mốc giá kỳ vọng ban đầu của người bán (Asking Price).
> - Trong thực tế thị trường xe cũ Việt Nam, biên độ thương lượng (Negotiation Margin) thường dao động trong khoảng **2% đến 5%** tùy vào độ nhiệt tình của người mua và tình trạng thanh khoản của dòng xe.
> - Do mô hình đạt sai số trung vị **MdAPE là 4.29%**, dự đoán của mô hình đóng vai trò như một **Mỏ neo định giá thị trường (Market Price Anchor)**. Người mua cá nhân có thể lấy mức giá dự đoán của mô hình làm cơ sở để biết được salon có đang rao giá quá cao so với mặt bằng chung hay không, từ đó chủ động đàm phán giảm trừ từ 3%–5% để đạt được giá chốt hợp lý."*

---

### Câu 25: Hệ thống kiểm thử tự động của nhóm bao gồm những gì và được tổ chức như thế nào?
**Trả lời của học viên:**
> *"Thưa Mentor, toàn bộ dự án được bảo vệ bởi **87 unit tests** chia thành 8 module độc lập trong thư mục `tests/`:
> 1. `test_load_dataset.py`: Kiểm tra tính bất biến của dữ liệu thô và đối soát mã băm SHA-256.
> 2. `test_price_parser.py`: Kiểm thử bộ bóc tách ngôn ngữ tự nhiên giá tiền VND.
> 3. `test_cleaning.py`: Kiểm tra logic làm sạch, điền khuyết ODO và sinh cờ phân khúc xe sang.
> 4. `test_split_data.py`: Kiểm toán tính rời rạc 100% ID và bảo toàn phân tầng deciles giá.
> 5. `test_preprocessing.py`: Kiểm tra đường ống biến đổi dữ liệu không bị rò rỉ target.
> 6. `test_modeling.py`: Kiểm thử hàm biến đổi logarit, nghịch đảo hàm mũ và độ tái lập seed.
> 7. `test_duplicate_groups.py`: Kiểm thử thuật toán gom cụm 4 cấp độ và cách ly cluster.
> 8. `test_predict.py`: Kiểm thử toàn trình module suy luận CLI và phát hiện lỗi schema đầu vào.
> 
> Toàn bộ 87 bài test chạy **100% offline chỉ trong 5.94 giây**, không phụ thuộc mạng, đảm bảo chuẩn mực Continuous Integration (CI) của kỹ thuật phần mềm hiện đại."*

---

### Câu 26: Nếu đưa hệ thống này vào môi trường sản xuất thực tế (Production), kiến trúc triển khai sẽ như thế nào?
**Trả lời của học viên:**
> *"Thưa Mentor, kiến trúc triển khai sản xuất đã được thiết kế sẵn sàng:
> 1. **Đóng gói Service (Backend API)**: Sử dụng framework **FastAPI** bọc quanh module [`src/models/predict.py`](file:///d:/ai-club-end-training/src/models/predict.py). Do artifact Random Forest nén chỉ nặng 31 MB, mô hình được nạp sẵn vào RAM khi server khởi động (Warm Start), độ trễ suy luận (Inference Latency) cho một request chỉ mất dưới **15 mili-giây**.
> 2. **Kiểm tra Schema đầu vào**: Sử dụng thư viện **Pydantic** để xác thực kiểu dữ liệu của xe (năm sản xuất phải trong khoảng $[2015, 2026]$, ODO không được âm,...).
> 3. **Đóng gói Docker Container**: Tạo Dockerfile chuẩn hóa môi trường Python 3.11 với dung lượng image dưới 250 MB.
> 4. **Giao diện Người dùng (Frontend)**: Xây dựng dashboard tương tác bằng **Streamlit** cho phép người dùng chỉ cần chọn Hãng, Dòng xe qua dropdown và nhập số km là nhận ngay giá định giá ước tính kèm khoảng tin cậy (Confidence Interval)."*

---
*Bộ tài liệu phản biện bao gồm đầy đủ các khía cạnh từ toán học, code, đạo đức đến nghiệp vụ thị trường, giúp học viên tự tin làm chủ buổi bảo vệ.*
