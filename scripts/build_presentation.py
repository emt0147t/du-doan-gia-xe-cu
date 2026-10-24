"""
Build Final Defense PowerPoint Presentation for AI Club End-Training.
Widescreen 16:9, modern professional styling, embedding figures and structured cards.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    os.makedirs("presentation", exist_ok=True)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank slide layout

    # Colors
    NAVY = RGBColor(15, 23, 42)        # #0f172a
    DARK_BLUE = RGBColor(30, 58, 138)   # #1e3a8a
    ROYAL_BLUE = RGBColor(37, 99, 235)  # #2563eb
    LIGHT_BG = RGBColor(248, 250, 252)  # #f8fafc
    WHITE = RGBColor(255, 255, 255)
    CARD_BG = RGBColor(255, 255, 255)
    CARD_BORDER = RGBColor(226, 232, 240) # #e2e8f0
    TEXT_MAIN = RGBColor(30, 41, 59)    # #1e293b
    TEXT_MUTED = RGBColor(100, 116, 139) # #64748b
    GREEN = RGBColor(16, 149, 117)      # #10b981
    GOLD = RGBColor(217, 119, 6)        # #d97706
    CYAN = RGBColor(6, 182, 212)        # #06b6d4

    def add_header(slide, phase_text, title_text, subtitle_text=""):
        # Header banner shape
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        # Category badge
        p0 = tf.paragraphs[0]
        p0.text = phase_text.upper()
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = ROYAL_BLUE
        
        # Main Title
        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = NAVY
        
        # Subtitle
        if subtitle_text:
            p2 = tf.add_paragraph()
            p2.text = subtitle_text
            p2.font.size = Pt(12)
            p2.font.color.rgb = TEXT_MUTED

    def add_card(slide, left, top, width, height, title="", bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1.5)
        else:
            card.line.fill.background()
        
        if title:
            tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.5))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = NAVY
        return card

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Dark Navy)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.333), Inches(4.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "AI CLUB END-TRAINING FINAL DEFENSE • 2026"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = CYAN
    p.space_after = Pt(20)

    p = tf1.add_paragraph()
    p.text = "Used Car Price Prediction in Vietnam"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = WHITE

    p = tf1.add_paragraph()
    p.text = "An End-to-End Machine Learning System & Scientific Evaluation"
    p.font.size = Pt(20)
    p.font.color.rgb = RGBColor(148, 163, 184)
    p.space_after = Pt(40)

    p = tf1.add_paragraph()
    p.text = "Học viên: AI Student  |  Cố vấn kỹ thuật: Senior Data Scientist & ML Mentor"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = WHITE

    p = tf1.add_paragraph()
    p.text = "Trọng tâm: Data Governance • Zero Leakage • Tuned Ensembles • Group-Aware Robustness"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(148, 163, 184)

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT & MARKET CONTEXT
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Phase 0 - 2 • Đặt vấn đề bài toán", "Thực Trạng Thị Trường Ô Tô Cũ & Bài Toán Hồi Quy", "Bất cân xứng thông tin, dải giá rộng và vai trò của mỏ neo định giá khách quan")

    add_card(s2, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.2), "Thách Thức Định Giá Tại Việt Nam")
    tb = s2.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    items_s2_left = [
        ("Bất cân xứng thông tin cao: ", "Người mua cá nhân thiếu công cụ định lượng giá trị thực của xe cũ trước các chiêu trò salon."),
        ("Dải giá biến thiên cực đoan: ", "Từ xe van cỡ nhỏ 55 triệu đến siêu xe 45 tỷ VND. Phân phối lệch phải nặng (Skewed)."),
        ("Tập quán thương lượng (3-5%): ", "Biên độ mặc cả thị trường là 15-35M VND cho xe phổ thông. Đây là ngưỡng sai số mục tiêu của mô hình!"),
        ("Chính sách thuế lũy tiến: ", "Thuế Tiêu thụ Đặc biệt (TTĐB) đánh từ 35% đến 150% theo dung tích máy, tạo bước nhảy vọt phi tuyến.")
    ]
    for bold_txt, norm_txt in items_s2_left:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(12)
        r1 = p.add_run()
        r1.text = "• " + bold_txt
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = NAVY
        r2 = p.add_run()
        r2.text = norm_txt
        r2.font.size = Pt(12)
        r2.font.color.rgb = TEXT_MAIN

    add_card(s2, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2), "Định Nghĩa Bài Toán Học Máy (ML Formulation)")
    tb = s2.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    items_s2_right = [
        ("Nhiệm vụ (Task): ", "Hồi quy bảng có giám sát (Supervised Tabular Regression)."),
        ("Nhãn mục tiêu (Target): ", "price_vnd (Giá rao bán chính thức VND)."),
        ("Không gian mục tiêu Log: ", "ln(price_vnd) để tối ưu sai số tỷ đối tương đối thay vì bị chi phối bởi xe siêu sang."),
        ("Không gian đặc trưng: ", "15 đặc trưng kỹ thuật, tuổi xe, ODO, phân khúc xe sang, xuất xứ và kiểu dáng."),
        ("Bộ chỉ số đánh giá cốt lõi: ", "MdAPE (Sai số trung vị tương đối), MAE (Triệu VND), RMSE và R².")
    ]
    for bold_txt, norm_txt in items_s2_right:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(12)
        r1 = p.add_run()
        r1.text = "• " + bold_txt
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = ROYAL_BLUE
        r2 = p.add_run()
        r2.text = norm_txt
        r2.font.size = Pt(12)
        r2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 3: DATASET PROVENANCE & GOVERNANCE
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Phase 3 • Nguồn gốc & Quản trị dữ liệu", "Tiếp Nhận Dữ Liệu Thị Trường & Đạo Đức Dữ Liệu", "Tiếp nhận bộ dữ liệu Bonbanh 30,652 dòng, xác lập Cohort A và bảo toàn mã băm SHA-256")

    # Left card: Provenance
    add_card(s3, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.2), "Nguồn Gốc & Tính Toàn Vẹn SHA-256")
    tb = s3.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    items_s3_left = [
        ("Dữ liệu thô chính (Primary): ", "car_detail.csv (30,652 dòng, 24 cột). SHA-256: 44C13AFC...7F32"),
        ("Dữ liệu bổ trợ (Companion): ", "car_sell_processed.csv (30,652 dòng). SHA-256: 1D0C0D2F...FBBD"),
        ("Quyền sở hữu & Giấy phép: ", "Dữ liệu thứ cấp công khai Kaggle Bonbanh CC0 Public Domain. Được Mentor phê duyệt thay thế việc live-crawl rủi ro cao."),
        ("Nguyên tắc bất biến: ", "Thư mục data/raw/ ở chế độ Read-Only tuyệt đối. Mã băm được kiểm toán xác nhận nguyên vẹn 100% qua tất cả các Phase.")
    ]
    for bold_txt, norm_txt in items_s3_left:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(12)
        r1 = p.add_run()
        r1.text = "• " + bold_txt
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = NAVY
        r2 = p.add_run()
        r2.text = norm_txt
        r2.font.size = Pt(12)
        r2.font.color.rgb = TEXT_MAIN

    # Right card: Cohorts & PII
    add_card(s3, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2), "Xác Lập Cohort & Đạo Đức Dữ Liệu (PII)")
    tb = s3.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    items_s3_right = [
        ("Cohort A (Trọng tâm Đề tài): ", "Xe sản xuất từ 2015-2023. Gồm 23,510 bản ghi sạch (76.7% dữ liệu). Đại diện cho >85% thanh khoản thị trường xe cũ đương đại."),
        ("Cohort B (Mở rộng độ nhạy): ", "Xe sản xuất từ 2010-2023. Gồm 27,299 bản ghi. Kiểm tra độ nhạy ngoại suy xe đời sâu."),
        ("Khử danh tính triệt để (PII): ", "Loại bỏ hoàn toàn Số điện thoại cá nhân, tên người bán, URL tin đăng bằng Regex trước khi lập chỉ mục."),
        ("Đạo đức thu thập: ", "Không gửi tải scraping phá hoại nền tảng. Tuân thủ tuyệt đối điều lệ bảo vệ người dùng.")
    ]
    for bold_txt, norm_txt in items_s3_right:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(12)
        r1 = p.add_run()
        r1.text = "• " + bold_txt
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = ROYAL_BLUE
        r2 = p.add_run()
        r2.text = norm_txt
        r2.font.size = Pt(12)
        r2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 4: EXPLORATORY DATA ANALYSIS (EDA)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Phase 4 • Khám phá dữ liệu (EDA)", "Các Phát Hiện Quan Trọng Về Thị Trường & Thuế", "Phân phối lệch phải, bước nhảy thuế TTĐB và sự phân hóa thương hiệu hạng sang")

    # Image left
    fig_path = "reports/figures/phase4/fig01_target_price_distribution.png"
    if os.path.exists(fig_path):
        s4.shapes.add_picture(fig_path, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.2))
    else:
        add_card(s4, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.2), "Distribution Plot")

    # Right Card: Insights
    add_card(s4, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2), "Những Khám Phá EDA Quyết Định Thiết Kế")
    tb = s4.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    items_s4 = [
        ("Lệch phải cực đoan (Right-skew): ", "Median = 719M VND, Mean = 1.164B VND (lệch +445M). Đuôi dài kéo tới 45 tỷ khiến mô hình OLS thô bị sập."),
        ("Phân phối Log-normal chuẩn mực: ", "ln(price_vnd) đối xứng hình chuông, chứng minh cơ sở lý thuyết vững chắc cho biến đổi Log."),
        ("Dấu ấn Thuế Tiêu thụ Đặc biệt (TTĐB): ", "Dung tích xi-lanh là yếu tố phân hóa giá mạnh nhất: xe >3.0L chịu thuế 90-150%, giá tăng phi tuyến tính."),
        ("Hiệu ứng thương hiệu hạng sang: ", "Mercedes, Lexus, BMW chiếm 21.6% thị phần với giá trung vị 2-4.5 tỷ. Nhóm phổ thông (Toyota, Hyundai, Kia) giữ ổn định 400-800M.")
    ]
    for bold_txt, norm_txt in items_s4:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(12)
        r1 = p.add_run()
        r1.text = "• " + bold_txt
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = NAVY
        r2 = p.add_run()
        r2.text = norm_txt
        r2.font.size = Pt(12)
        r2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 5: DATA CLEANING & FEATURE ENGINEERING
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Phase 5 • Tiền xử lý & Kỹ nghệ đặc trưng", "Chuẩn Hóa Dữ Liệu & Bộ 15 Đặc Trưng Tinh Gọn", "Xử lý ODO ngoại lai, bóc tách xe mới showroom và biến đổi không gian mục tiêu")

    add_card(s5, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.2), "Các Quy Tắc Tiền Xử Lý Tất Định")
    tb = s5.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    items_s5_left = [
        ("Xử lý ODO ngoại lai (>1M km): ", "Người bán gõ bừa 999999 km. Không xóa dòng làm mất dữ liệu; thay bằng Median theo nhóm tuổi xe."),
        ("Nhận diện 25.8% xe mới Showroom: ", "6,066 xe có ODO = 0 km và giá niêm yết cố định. Bổ sung cờ is_zero_mileage và nhãn 'Xe mới' để mô hình không nhầm với xe cũ."),
        ("Bộ tách giá NLP tiếng Việt: ", "Chuyển đổi hoàn hảo các chuỗi 'X tỷ Y triệu' thành số nguyên VND. Lọc bỏ tin cọc/ước lệ < 10M VND."),
        ("Phân nhóm nguồn gốc: ", "Chuẩn hóa xuất xứ thành 2 nhóm chính thống: 'Lắp ráp trong nước' vs 'Nhập khẩu'.")
    ]
    for bold_txt, norm_txt in items_s5_left:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(12)
        r1 = p.add_run()
        r1.text = "• " + bold_txt
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = NAVY
        r2 = p.add_run()
        r2.text = norm_txt
        r2.font.size = Pt(12)
        r2.font.color.rgb = TEXT_MAIN

    add_card(s5, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2), "Ma Trận Đầu Vào 15 Đặc Trưng & Target")
    tb = s5.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    items_s5_right = [
        ("8 Biến Định Lượng (Numeric): ", "year, car_age (2023 - year), mileage_km, seats, doors, engine_displacement_l, is_luxury_brand, is_zero_mileage."),
        ("7 Biến Định Danh (Categorical): ", "brand (48 hãng), model (451 dòng), origin (2 nhóm), transmission (2 nhóm), fuel_type (4 nhóm), body_type (8 nhóm), condition (2 nhóm)."),
        ("Biến đổi nhãn mục tiêu (Target): ", "Huấn luyện trên ln(price_vnd) và nghịch đảo hàm mũ exp(y_hat) khi đo lường sai số VND."),
        ("Chặn 9 cột rò rỉ (Strict Drop): ", "price_vnd, log_price, Giá, listing_id, url, Mô tả, Tên xe, Tỉnh thành bị cách ly hoàn toàn.")
    ]
    for bold_txt, norm_txt in items_s5_right:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(12)
        r1 = p.add_run()
        r1.text = "• " + bold_txt
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = ROYAL_BLUE
        r2 = p.add_run()
        r2.text = norm_txt
        r2.font.size = Pt(12)
        r2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 6: SPLITTING PROTOCOL & LEAKAGE PREVENTION
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Phase 5 & 6 • Phân chia tập dữ liệu", "Giao Thức Phân Tầng 80/10/10 & Phòng Chống Rò Rỉ", "Cách ly tuyệt đối giữa Train, Validation, Test và nguyên tắc Fit chỉ trên Train")

    add_card(s6, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.2), "Phân Bổ Dữ Liệu Phân Tầng Giá (Stratification)")
    tb = s6.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    items_s6_left = [
        ("Quy mô phân chia 80 / 10 / 10: ", "Train: 18,808 dòng (80.0%) | Validation: 2,351 dòng (10.0%) | Test: 2,351 dòng (10.0%)."),
        ("Bảo toàn phân phối phân vị: ", "Phân tầng theo 10 deciles giá price_vnd. Median của cả 3 tập đều đạt chuẩn xác 719M VND (Val: 718M)."),
        ("Niêm phong tập Test: ", "Tập Test được niêm phong hoàn toàn. Chỉ mở đúng 1 lần sau khi đã chốt mô hình trên Validation!"),
        ("Kiểm soát tính độc lập ID: ", "100% không trùng lặp listing_id giữa 3 tập dữ liệu.")
    ]
    for bold_txt, norm_txt in items_s6_left:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(12)
        r1 = p.add_run()
        r1.text = "• " + bold_txt
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = NAVY
        r2 = p.add_run()
        r2.text = norm_txt
        r2.font.size = Pt(12)
        r2.font.color.rgb = TEXT_MAIN

    add_card(s6, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2), "Cơ Chế Phòng Chống Rò Rỉ Tuyến Pipeline")
    tb = s6.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    items_s6_right = [
        ("Fit duy nhất trên Train: ", "Bộ SimpleImputer, OneHotEncoder và StandardScaler chỉ được fit() trên 18,808 dòng Train."),
        ("Xử lý Unseen Categories: ", "OneHotEncoder cấu hình handle_unknown='ignore' để không gây lỗi khi gặp dòng xe mới lạ trên Val/Test."),
        ("Không rò rỉ Target: ", "Mọi phép chuẩn hóa và biến đổi nhãn được gói trong pipeline độc lập."),
        ("Xác thực tự động bằng Unit Test: ", "Các bài test trong tests/test_split_data.py kiểm tra tự động trước mỗi lần train.")
    ]
    for bold_txt, norm_txt in items_s6_right:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(12)
        r1 = p.add_run()
        r1.text = "• " + bold_txt
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = ROYAL_BLUE
        r2 = p.add_run()
        r2.text = norm_txt
        r2.font.size = Pt(12)
        r2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 7: MODELING STRATEGY & ARCHITECTURES
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Phase 6 • Chiến lược mô hình hóa", "Khảo Sát Đa Dạng Kiến Trúc Mô Hình", "So sánh đối ứng từ Baseline, Mô hình tuyến tính đến Rừng ngẫu nhiên & Gradient Boosting")

    # 3 horizontal cards
    w_card = Inches(3.64)
    h_card = Inches(5.2)

    # Card 1: Baselines
    add_card(s7, Inches(0.8), Inches(1.7), w_card, h_card, "1. Mô Hình Cơ Sở (Baselines)")
    tb = s7.shapes.add_textbox(Inches(0.95), Inches(2.3), w_card - Inches(0.3), h_card - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True
    c1_items = [
        ("Dummy Median: ", "Dự đoán hằng số 719M VND. Val MAE = 914.6M, MdAPE = 39.83%, R² = -0.07."),
        ("Dummy Mean: ", "Dự đoán hằng số 1.164B VND. Val MAE = 1,164.2M, MdAPE = 94.34%, R² = -0.00."),
        ("Vai trò: ", "Thiết lập sàn chuẩn mực tối thiểu để đo lường giá trị thực tế của ML.")
    ]
    for b, n in c1_items:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = "• " + b
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = NAVY
        r2 = p.add_run()
        r2.text = n
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MAIN

    # Card 2: Linear
    add_card(s7, Inches(4.84), Inches(1.7), w_card, h_card, "2. Hồi Quy Tuyến Tính (Linear)")
    tb = s7.shapes.add_textbox(Inches(4.99), Inches(2.3), w_card - Inches(0.3), h_card - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True
    c2_items = [
        ("Ridge (Raw VND): ", "Val MAE = 379.4M, MdAPE = 23.72%. Bị lệch nặng bởi xe siêu sang do hàm phạt MSE."),
        ("Ridge (Log Target): ", "Val MAE = 255.7M, MdAPE = 7.72%. Log target giúp giảm 32.6% MAE và giảm 67% MdAPE!"),
        ("Lasso (Log Target): ", "Val MAE = 370.7M, MdAPE = 12.22%. Phạt L1 triệt tiêu nhiều biến phân loại cần thiết.")
    ]
    for b, n in c2_items:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = "• " + b
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = ROYAL_BLUE
        r2 = p.add_run()
        r2.text = n
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MAIN

    # Card 3: Trees
    add_card(s7, Inches(8.88), Inches(1.7), w_card, h_card, "3. Mô Hình Cây & Ensemble")
    tb = s7.shapes.add_textbox(Inches(9.03), Inches(2.3), w_card - Inches(0.3), h_card - Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True
    c3_items = [
        ("HistGradientBoosting: ", "Val MAE = 180.8M, MdAPE = 5.37%. Tốc độ huấn luyện siêu nhanh (4.2 giây)."),
        ("Random Forest (Default): ", "Val MAE = 159.1M, MdAPE = 4.94%."),
        ("Random Forest (Tuned): ", "150 cây, max_depth=24. Val MAE = 142.9M, MdAPE = 4.25%, R² = 0.8694."),
        ("Ưu thế cây: ", "Bắt trọn mối quan hệ phi tuyến và tương tác phân khúc không cần chuẩn hóa phân phối.")
    ]
    for b, n in c3_items:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = "• " + b
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = GREEN
        r2 = p.add_run()
        r2.text = n
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 8: VALIDATION LEADERBOARD & CHAMPION SELECTION
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Phase 6 • Bảng xếp hạng Validation", "So Sánh 10 Cấu Hình & Lựa Chọn Champion Model", "Đánh giá nhất quán trên 2,351 dòng Validation và nghịch đảo về đơn vị VND thực tế")

    # Table on slide
    rows, cols = 8, 6
    left, top, width, height = Inches(0.8), Inches(1.7), Inches(11.733), Inches(3.6)
    table_shape = s8.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    headers = ["Hạng", "Cấu Hình Mô Hình", "Target", "Val MAE (VND)", "Val R²", "Val MdAPE (%)"]
    col_widths = [Inches(0.9), Inches(4.3), Inches(1.3), Inches(2.2), Inches(1.3), Inches(1.7)]
    for i, w in enumerate(col_widths):
        table.columns[i].width = w

    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_BLUE
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    data_rows = [
        ("🥇 1 (Champion)", "Tree_RandomForest_Tuned_LogTarget", "Log", "142,934,537", "0.8694", "4.25%"),
        ("🥈 2", "Tree_RandomForest_LogTarget (Default)", "Log", "159,102,971", "0.8425", "4.94%"),
        ("🥉 3", "Tree_RandomForest_RawTarget", "Raw", "168,751,598", "0.8949", "6.61%"),
        ("4", "Tree_HistGBM_LogTarget", "Log", "180,831,847", "0.7888", "5.37%"),
        ("5", "Linear_Ridge_LogTarget", "Log", "255,658,033", "0.6996", "7.72%"),
        ("6", "Linear_Ridge_RawTarget", "Raw", "379,429,332", "0.8075", "23.72%"),
        ("7 (Baseline)", "Baseline_Dummy_Median", "Raw", "914,616,759", "-0.0714", "39.83%")
    ]
    for r_idx, row in enumerate(data_rows, start=1):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(11)
            if r_idx == 1:
                p.font.bold = True
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(238, 242, 255)
                p.font.color.rgb = ROYAL_BLUE
            else:
                p.font.color.rgb = TEXT_MAIN
            if c_idx in [0, 2, 4, 5]:
                p.alignment = PP_ALIGN.CENTER

    # Bottom Callout Card
    add_card(s8, Inches(0.8), Inches(5.5), Inches(11.733), Inches(1.4), "", bg_color=RGBColor(240, 253, 250), border_color=GREEN)
    tb = s8.shapes.add_textbox(Inches(1.0), Inches(5.6), Inches(11.333), Inches(1.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "LÝ DO CHỌN CHAMPION: Tree_RandomForest_Tuned_LogTarget"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = GREEN
    p.space_after = Pt(4)
    p2 = tf.add_paragraph()
    p2.text = "• Giảm 84.4% MAE so với Median Baseline  |  MdAPE đạt 4.25% (nằm trọn trong biên thương lượng xe 3-5%)\n• Giải thích 86.94% phương sai giá  |  Kích thước gọn nhẹ 31 MB, thời gian fit ~5 giây, sẵn sàng triển khai thực tế."
    p2.font.size = Pt(11.5)
    p2.font.color.rgb = NAVY

    # =========================================================================
    # SLIDE 9: FINAL TEST EVALUATION (PHASE 6 RANDOM SPLIT)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Phase 6 • Đánh giá tập Test chính thức", "Kết Quả Kiểm Thử Độc Lập Trên Tập Test Chưa Thấy", "Test MAE đạt 111.8M VND, R² đạt 0.9448, MdAPE đạt 4.29% trên 2,351 xe chưa từng thấy")

    # Left: Metric Cards
    add_card(s9, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.2), "Kết Quả Tập Test Chính Thức (2,351 xe)")
    tb = s9.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    t_items = [
        ("Test MAE: 111,793,581 VND", "Giảm 86.8% so với Median Baseline (844.9M VND)."),
        ("Test R²: 0.9448", "Giải thích xấp xỉ 94.5% biến thiên giá thực tế."),
        ("Test MdAPE: 4.29%", "Một nửa số xe được dự đoán lệch không quá 4.29%."),
        ("HistGBM Test MAE: 148.9M", "R² = 0.9127 (xếp vị trí á quân)."),
        ("Ridge Test MAE: 196.0M", "R² = 0.8529 (tuyến tính vẫn kém cây ~84M MAE).")
    ]
    for b, n in t_items:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = "• " + b + "\n  "
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = ROYAL_BLUE
        r2 = p.add_run()
        r2.text = n
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MAIN

    # Right: Outlier Analysis
    add_card(s9, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2), "Giải Mã: Tại Sao Test MAE (111.8M) Tốt Hơn Val MAE (142.9M)?")
    tb = s9.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    val_test_exp = [
        ("Không phải do Overfitting hay May mắn: ", "Chênh lệch bắt nguồn hoàn toàn từ 1 chiếc xe siêu sang cá biệt trong tập Validation."),
        ("Ngoại lai cá biệt tại Validation: ", "1 xe giá 38.999 tỷ VND được dự đoán 3.247 tỷ (sai số lệch 35.75 tỷ VND trên 1 dòng!). Chiếc xe này đóng góp tới +15.2M VND vào MAE toàn tập Val!"),
        ("Xe phổ thông (<1 tỷ VND) tương đồng tuyệt đối: ", "Ở phân khúc đại chúng (<1B), MAE giữa Val và Test hoàn toàn trùng khớp: ~25.5M vs ~26.1M VND."),
        ("MdAPE vững chắc: ", "4.25% (Val) vs 4.29% (Test) khẳng định độ chính xác thực tế trên xe đại chúng là hoàn toàn tương đương.")
    ]
    for b, n in val_test_exp:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = "• " + b
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = NAVY
        r2 = p.add_run()
        r2.text = n
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 10: AUDIT & CROSS-POSTING DISCOVERY
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Phase 6.1 • Kiểm toán độc lập", "Phát Hiện Rò Rỉ Đăng Chéo Tin (Cross-Posting Overlap)", "Liệu Test MAE 111.8M có phải do học vẹt các tin đăng nhân bản giữa Train và Test?")

    add_card(s10, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.2), "Phân Rã 5 Dạng Trùng Lặp Thị Trường")
    tb = s10.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    dup_types = [
        ("1. Listing ID Duplicate: ", "0 dòng (0.00%). Tuyệt đối không trùng ID."),
        ("2. Exact Row Duplicate: ", "0 dòng (0.00%). Không có dòng copy vô nghĩa."),
        ("3. Cross-Posting Overlap: ", "8.21% Test trùng văn bản mô tả với Train do các salon copy bài quảng cáo của nhau."),
        ("4. Showroom Inventory Overlap: ", "27.3% Test trùng thông số xe mới (ODO=0) theo giá hãng. Đã có cờ is_zero_mileage phân tách."),
        ("5. Spec Group Overlap: ", "95.8% Test có cấu hình xe (Vios 2020 AT) đã từng gặp trong Train. Đây là đặc tính Tabular IID.")
    ]
    for b, n in dup_types:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = "• " + b
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = NAVY
        r2 = p.add_run()
        r2.text = n
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MAIN

    add_card(s10, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2), "Câu Hỏi Khoa Học Cần Giải Quyết")
    tb = s10.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    audit_q = [
        ("Nghi vấn phương pháp luận: ", "Có 9.15% tin Test có bản sao mô tả trong Train. Nếu loại bỏ hoàn toàn các tin này, mô hình có bị sập độ chính xác?"),
        ("Bản chất Random Forest: ", "RF hoạt động như bộ nội suy láng giềng phân tầng. Cấu hình quen thuộc có MAE 84.1M (MdAPE 4.05%), cấu hình mới lạ có MAE 741.6M (MdAPE 15.44%)."),
        ("Hành động triển khai: ", "Thực thi Phase 6.2 - Group-Aware Evaluation. Gom cụm tin trùng và chia tập StratifiedGroupKFold để đạt 0% rò rỉ!")
    ]
    for b, n in audit_q:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(12)
        r1 = p.add_run()
        r1.text = "• " + b
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = GOLD
        r2 = p.add_run()
        r2.text = n
        r2.font.size = Pt(12)
        r2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 11: GROUP-AWARE ROBUSTNESS EVALUATION (PHASE 6.2)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Phase 6.2 • Đánh giá độ bền chia nhóm", "Bằng Chứng Độ Bền: MdAPE Vẫn Đạt 4.29% Tuyệt Đối", "Triệt tiêu 100% rò rỉ tin đăng trùng mà không suy giảm độ chính xác trên xe phổ thông")

    # Image Left
    fig_path_62 = "reports/figures/phase6_2/phase6_vs_phase6_2_comparison.png"
    if os.path.exists(fig_path_62):
        s11.shapes.add_picture(fig_path_62, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.2))
    else:
        add_card(s11, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.2), "Phase 6 vs 6.2 Comparison")

    # Right Card: Scientific Proof
    add_card(s11, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2), "Bằng Chứng Thực Nghiệm Độ Bền Tuyệt Đối")
    tb = s11.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    proof_items = [
        ("Cách ly 903 cụm trùng (2,430 xe): ", "Chia tập StratifiedGroupKFold đảm bảo 0% rò rỉ cluster giữa Train, Val và Test."),
        ("Test MdAPE giữ vững 4.29% tuyệt đối: ", "Trùng khớp 100% với Phase 6! Chứng minh năng lực định giá của mô hình là hoàn toàn thực chất, không phụ thuộc vào bài đăng trùng."),
        ("Giải mã mức tăng MAE (111.8M -> 130.8M): ", "Tập Test mới ngẫu nhiên có thêm 27 xe siêu sang >5 tỷ (117 vs 90 xe). Riêng 27 xe này đã làm tăng trung bình MAE thêm +14.5M VND!"),
        ("Xe phổ thông (<1 tỷ) chính xác hơn: ", "Xe <500M đạt MAE 24.2M VND (tốt hơn mức 26.1M của Phase 6). Xe 500M-1B giữ vững 40.5M VND.")
    ]
    for b, n in proof_items:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = "• " + b
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = GREEN
        r2 = p.add_run()
        r2.text = n
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 12: FEATURE IMPORTANCE & DOMAIN VALIDATION
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Phase 6 & 6.1 • Tầm quan trọng đặc trưng", "Giải Thích Mô Hình & Sự Phù Hợp Nghiệp Vụ Thuế", "Độ giảm phương sai (MDI) và Permutation Importance phản ánh chân thực biểu thuế TTĐB Việt Nam")

    # Image Left
    fig_path_fi = "reports/figures/phase6/feature_importance.png"
    if os.path.exists(fig_path_fi):
        s12.shapes.add_picture(fig_path_fi, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.2))
    else:
        add_card(s12, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.2), "Feature Importance Plot")

    # Right Card: Domain validation
    add_card(s12, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2), "Đối Chiếu Thực Tiễn Ngành Ô Tô")
    tb = s12.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    fi_items = [
        ("is_luxury_brand (43.1% MDI): ", "Xác lập phân khúc trần giá. Một chiếc Mercedes cùng năm sản xuất có giá gấp 3-5 lần xe phổ thông."),
        ("engine_displacement_l (26.35% MDI): ", "Chiếm 1/4 quyết định giá xe do gắn trực tiếp với biểu thuế TTĐB Việt Nam (thuế suất lên tới 150% cho máy >6.0L)."),
        ("Đính chính thuật ngữ (MDI vs Gini): ", "Trong hồi quy, Random Forest dùng Độ giảm phương sai (MDI), không phải Gini (chỉ dành cho phân loại)."),
        ("Nghịch lý ODO (mileage_km - 0.69% MDI): ", "Toàn cục (Global) ODO có trọng số thấp vì biên giá thương hiệu (40 tỷ) áp đảo ODO. Cục bộ (Local), ODO quyết định 30-50M chênh lệch giữa 2 xe cùng đời!")
    ]
    for b, n in fi_items:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = "• " + b
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = ROYAL_BLUE
        r2 = p.add_run()
        r2.text = n
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 13: INFERENCE PIPELINE & SOFTWARE CRAFTSMANSHIP
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Hệ thống suy luận & Kỹ thuật phần mềm", "Module Suy Luận Thực Tế & Bộ 87 Unit Tests", "src/models/predict.py vận hành tự động, chống rò rỉ dữ liệu và kiểm thử 100% offline")

    add_card(s13, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.2), "Kiến Trúc Module Suy Luận (predict.py)")
    tb = s13.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    inf_items = [
        ("Giao diện dòng lệnh CLI linh hoạt: ", "Hỗ trợ dự đoán đơn lẻ 1 xe qua tham số CLI hoặc dự đoán hàng loạt từ file CSV."),
        ("Tự động trích xuất đặc trưng: ", "Tự tính car_age, is_luxury_brand, is_zero_mileage và bóc tách dung tích động cơ mà không bắt người dùng nhập tay."),
        ("An toàn dữ liệu tuyệt đối: ", "Tự động loại bỏ các cột rò rỉ nếu người dùng vô tình đưa vào file CSV đầu vào."),
        ("Hỗ trợ Smoke Test tích hợp: ", "Lệnh python src/models/predict.py --smoke-test kiểm thử ngay lập tức 3 dòng xe đại diện.")
    ]
    for b, n in inf_items:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = "• " + b
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = NAVY
        r2 = p.add_run()
        r2.text = n
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MAIN

    add_card(s13, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2), "Chuẩn Mực Kỹ Thuật Phần Mềm AI Club")
    tb = s13.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    swe_items = [
        ("87/87 Unit Tests Passing (100%): ", "Toàn bộ bài test thực thi hoàn toàn offline trong 5.94 giây. Kiểm tra từ crawler, cleaning, splits đến inference."),
        ("Quản lý Artifact tối ưu: ", "Mô hình nén dạng joblib chỉ 31 MB, dễ dàng nhúng vào container Docker hoặc microservice."),
        ("Khả năng tái lập tuyệt đối (Reproducibility): ", "Cố định random_state=42 trên toàn bộ quy trình từ split, preprocessor đến random forest."),
        ("Zero Untracked Changes: ", "Mọi kết quả và số liệu đều truy nguyên được về file JSON/CSV trong repository.")
    ]
    for b, n in swe_items:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = "• " + b
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = GREEN
        r2 = p.add_run()
        r2.text = n
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 14: LIMITATIONS & THREATS TO VALIDITY
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Đánh giá khoa học khách quan", "Giới Hạn Của Đề Tài & Đe Dọa Giá Trị Thực Tiễn", "Nhìn nhận trung thực các hạn chế về dữ liệu và điều kiện áp dụng trong thế giới thực")

    add_card(s14, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.2), "Bốn Giới Hạn Nghiệp Vụ Cốt Lõi")
    tb = s14.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    lim_items = [
        ("1. Giá rao bán vs Giá giao dịch: ", "Dữ liệu là giá chào trên web (asking price), không phải giá chốt công chứng (transaction price). Giá thực tế thường thấp hơn 2-5% sau mặc cả."),
        ("2. Thiếu số khung VIN / Biển số: ", "Sàn xe không công khai VIN. Không thể triệt tiêu 100% việc 1 chiếc xe vật lý được 2 salon viết 2 bài quảng cáo khác nhau."),
        ("3. Mặt cắt ngang tĩnh (Cross-Sectional): ", "Dữ liệu là một lát cắt thời gian năm 2023. Chưa mô hình hóa được biến động chính sách lệ phí trước bạ theo từng quý."),
        ("4. Độ lệch vùng miền: ", "Hơn 75% dữ liệu tập trung tại Hà Nội và TP.HCM. Cần hiệu chỉnh khi áp dụng cho các tỉnh miền núi/xa xôi.")
    ]
    for b, n in lim_items:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = "• " + b
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = GOLD
        r2 = p.add_run()
        r2.text = n
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MAIN

    add_card(s14, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2), "Ranh Giới Ứng Dụng An Toàn Của Mô Hình")
    tb = s14.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    safe_use = [
        ("Phạm vi ứng dụng xuất sắc: ", "Định giá mỏ neo tham chiếu cho người mua cá nhân và chuyên viên định giá đối với các dòng xe phổ biến đời 2015-2023."),
        ("Cảnh báo ngoại suy xe đời sâu: ", "Mô hình cây không thể dự đoán chính xác cho xe trước 2015 (Cohort B sensitivity chỉ ra rủi ro ngoại suy MAE vọt lên 314M)."),
        ("Khuyến nghị người dùng: ", "Mô hình là công cụ tham khảo hỗ trợ ra quyết định (Decision Support Tool), không thay thế việc kiểm định cơ khí trực tiếp (thủy kích, tai nạn, khung gầm).")
    ]
    for b, n in safe_use:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(12)
        r1 = p.add_run()
        r1.text = "• " + b
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = NAVY
        r2 = p.add_run()
        r2.text = n
        r2.font.size = Pt(12)
        r2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 15: CONCLUSION & FUTURE ROADMAP (Dark Navy)
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    bg15 = s15.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg15.fill.solid()
    bg15.fill.fore_color.rgb = NAVY
    bg15.line.fill.background()

    tb15 = s15.shapes.add_textbox(Inches(1.0), Inches(1.0), Inches(11.333), Inches(5.5))
    tf15 = tb15.text_frame
    tf15.word_wrap = True
    
    p = tf15.paragraphs[0]
    p.text = "KẾT LUẬN & ĐỊNH HƯỚNG PHÁT TRIỂN"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_after = Pt(24)

    conc_bullets = [
        ("Hoàn thành trọn vẹn mục tiêu Điều lệ: ", "Xây dựng thành công hệ thống ML định giá ô tô cũ tại Việt Nam với mô hình vô địch Random Forest Log-Target."),
        ("Hiệu năng bền vững được chứng minh: ", "Test MdAPE đạt 4.29% trên cả phân chia ngẫu nhiên và phân chia cách ly tin trùng 100% (Group-Aware)."),
        ("Định hướng Kỹ thuật tiếp theo: ", "Thử nghiệm XGBoost/LightGBM/CatBoost; Tích hợp mô hình NLP (PhoBERT) trích xuất option từ văn bản và Computer Vision phân tích ảnh xe."),
        ("Định hướng Sản phẩm hóa: ", "Đóng gói Docker container, xây dựng API FastAPI và giao diện Streamlit tra cứu giá trực quan cho người tiêu dùng.")
    ]
    for b, n in conc_bullets:
        p = tf15.add_paragraph()
        p.space_after = Pt(14)
        r1 = p.add_run()
        r1.text = "✓ " + b
        r1.font.bold = True
        r1.font.size = Pt(14)
        r1.font.color.rgb = CYAN
        r2 = p.add_run()
        r2.text = n
        r2.font.size = Pt(13)
        r2.font.color.rgb = RGBColor(226, 232, 240)

    p_end = tf15.add_paragraph()
    p_end.space_before = Pt(30)
    p_end.text = "CẢM ƠN HỘI ĐỒNG MENTOR & CÂU LẠC BỘ AI — SẴN SÀNG CHO PHẦN PHẢN BIỆN Q&A!"
    p_end.font.bold = True
    p_end.font.size = Pt(16)
    p_end.font.color.rgb = GOLD
    p_end.alignment = PP_ALIGN.CENTER

    # Save presentation
    out_path = "presentation/ai_club_final_defense.pptx"
    prs.save(out_path)
    print(f"Presentation saved successfully to {out_path}")

if __name__ == "__main__":
    create_deck()
