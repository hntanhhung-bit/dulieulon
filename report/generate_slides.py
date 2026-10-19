# -*- coding: utf-8 -*-
"""
CHƯƠNG TRÌNH TỰ ĐỘNG TẠO SLIDE THUYẾT MINH BÀI TẬP LỚN XỬ LÝ DỮ LIỆU LỚN (CTKU122)
TRƯỜNG ĐẠI HỌC TÀI NGUYÊN VÀ MÔI TRƯỜNG HÀ NỘI - HUNRE
KHOA CÔNG NGHỆ THÔNG TIN - BỘ MÔN CÔNG NGHỆ THÔNG TIN

Đề tài: XÂY DỰNG HỆ THỐNG PHÂN TÍCH VÀ GIÁM SÁT CHẤT LƯỢNG MẠNG VIỄN THÔNG
(TELECOM QUALITY OF SERVICE ANALYTICS) TRÊN NỀN TẢNG HADOOP, SPARK VÀ R
"""

import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

output_pptx_path = r"c:\dulieulon\Slide.pptx"
img_dir = r"c:\dulieulon\report"

prs = Presentation()
prs.slide_width = Inches(13.333)  # 16:9 widescreen
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Theme Colors
C_NAVY_DARK = RGBColor(0x0F, 0x17, 0x2A)   # #0F172A
C_NAVY_LIGHT = RGBColor(0x1E, 0x29, 0x3B)  # #1E293B
C_BLUE = RGBColor(0x25, 0x63, 0xEB)        # #2563EB
C_BLUE_LIGHT = RGBColor(0xDB, 0xEA, 0xFE)  # #DBEAFE
C_GOLD = RGBColor(0xD9, 0x77, 0x06)        # #D97706
C_EMERALD = RGBColor(0x05, 0x96, 0x69)     # #059669
C_RED = RGBColor(0xDC, 0x26, 0x26)         # #DC2626
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
C_SLATE_TEXT = RGBColor(0x33, 0x41, 0x55)  # #334155
C_GRAY_BG = RGBColor(0xF8, 0xFA, 0xFC)     # #F8FAFC
C_BORDER = RGBColor(0xCB, 0xD5, 0xE1)      # #CBD5E1

def create_header(slide, title_text, category_text="BÁO CÁO BÀI TẬP LỚN XỬ LÝ DỮ LIỆU LỚN (CTKU122)"):
    # Header background strip
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
    shape.fill.solid()
    shape.fill.fore_color.rgb = C_NAVY_DARK
    shape.line.fill.background()

    # Category tracker
    tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.5), Inches(0.3))
    p_c = tb_cat.text_frame.paragraphs[0]
    p_c.text = category_text.upper()
    p_c.font.size = Pt(11)
    p_c.font.bold = True
    p_c.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)

    # Title
    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.42), Inches(11.5), Inches(0.6))
    p_t = tb_title.text_frame.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = C_WHITE

    # Bottom accent line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.06))
    line.fill.solid()
    line.fill.fore_color.rgb = C_BLUE
    line.line.fill.background()

def add_card(slide, x, y, w, h, bg_color=C_WHITE, border_color=C_BORDER):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1.5)
    return card

# ==============================================================================
# SLIDE 1: TRANG TIÊU ĐỀ
# ==============================================================================
slide1 = prs.slides.add_slide(blank_layout)
bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg1.fill.solid()
bg1.fill.fore_color.rgb = C_NAVY_DARK
bg1.line.fill.background()

# University header
tb1 = slide1.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.333), Inches(1.0))
tf1 = tb1.text_frame
tf1.word_wrap = True
p = tf1.paragraphs[0]
p.text = "TRƯỜNG ĐẠI HỌC TÀI NGUYÊN VÀ MÔI TRƯỜNG HÀ NỘI (HUNRE)"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)
p.alignment = PP_ALIGN.CENTER

p2 = tf1.add_paragraph()
p2.text = "KHOA CÔNG NGHỆ THÔNG TIN • HỌC PHẦN: XỬ LÝ DỮ LIỆU LỚN (CTKU122)"
p2.font.size = Pt(13)
p2.font.color.rgb = RGBColor(0xE2, 0xE8, 0xF0)
p2.alignment = PP_ALIGN.CENTER

# Main Title
tb_m = slide1.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.333), Inches(2.2))
tf_m = tb_m.text_frame
tf_m.word_wrap = True
p_dt = tf_m.paragraphs[0]
p_dt.text = "BÁO CÁO BÀI TẬP LỚN • ĐỀ TÀI SỐ 01"
p_dt.font.size = Pt(16)
p_dt.font.bold = True
p_dt.font.color.rgb = C_GOLD
p_dt.alignment = PP_ALIGN.CENTER

p_tt = tf_m.add_paragraph()
p_tt.text = "XÂY DỰNG HỆ THỐNG PHÂN TÍCH VÀ GIÁM SÁT\nCHẤT LƯỢNG MẠNG VIỄN THÔNG (TELECOM QOS ANALYTICS)\nTRÊN NỀN TẢNG HADOOP, SPARK VÀ R"
p_tt.font.size = Pt(26)
p_tt.font.bold = True
p_tt.font.color.rgb = C_WHITE
p_tt.alignment = PP_ALIGN.CENTER

# Team info card
info_card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.8), Inches(4.9), Inches(9.733), Inches(1.8))
info_card.fill.solid()
info_card.fill.fore_color.rgb = RGBColor(0x1E, 0x29, 0x3B)
info_card.line.color.rgb = RGBColor(0x3B, 0x82, 0xF6)
info_card.line.width = Pt(1.5)

tb_i = slide1.shapes.add_textbox(Inches(2.0), Inches(5.0), Inches(9.333), Inches(1.6))
tf_i = tb_i.text_frame
tf_i.word_wrap = True
p_sv1 = tf_i.paragraphs[0]
p_sv1.text = "Sinh viên thực hiện:  1. Hoàng Ngọc Thi (Nhóm trưởng)   2. Nguyễn Viết Hoàng Anh   3. Nguyễn Việt Hòa   4. Nguyễn Quốc Anh"
p_sv1.font.size = Pt(12)
p_sv1.font.bold = True
p_sv1.font.color.rgb = C_WHITE

p_sv2 = tf_i.add_paragraph()
p_sv2.text = "Lớp học phần:         ĐH13C2 • Khoa Công nghệ Thông tin"
p_sv2.font.size = Pt(12)
p_sv2.font.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)

p_sv3 = tf_i.add_paragraph()
p_sv3.text = "Giảng viên giảng dạy: ThS. / TS. Giảng viên phụ trách học phần"
p_sv3.font.size = Pt(12)
p_sv3.font.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)

p_sv4 = tf_i.add_paragraph()
p_sv4.text = "Hà Nội, Năm học 2025 - 2026"
p_sv4.font.size = Pt(12)
p_sv4.font.italic = True
p_sv4.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)
p_sv4.alignment = PP_ALIGN.RIGHT

# ==============================================================================
# SLIDE 2: ĐẶT VẤN ĐỀ & 3 MỤC TIÊU CỐT LÕI
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
create_header(s2, "1. ĐẶT VẤN ĐỀ & BA MỤC TIÊU KỸ THUẬT CỐT LÕI")

# Left Column: Problem context
add_card(s2, 0.8, 1.5, 5.6, 5.4, C_WHITE)
tb = s2.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(5.0))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "THÁCH THỨC VẬN HÀNH MẠNG VIỄN THÔNG"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = C_RED

bullets = [
    "Hàng chục nghìn trạm BTS: 50,000+ trạm phát sóng, mỗi trạm gồm 3-6 cell vô tuyến (3G, 4G, 5G).",
    "Áp lực dữ liệu bùng nổ: Hàng trăm nghìn bản ghi telemetry/giây; sinh ra từ 10 - 25 Terabyte log/ngày.",
    "Bất lực của RDBMS truyền thống: Cơ sở dữ liệu quan hệ bị nghẽn, sập nguồn khi truy vấn và tổng hợp theo thời gian thực.",
    "Phát hiện sự cố muộn màng: Khách hàng gặp rớt cuộc gọi nhiều lần và khiếu nại gay gắt mới phát hiện được cell quá tải.",
    "Chi phí đầu tư CAPEX tốn kém: Thiếu căn cứ định lượng để nâng cấp trạm nghẽn thực sự hay điều chỉnh vô tuyến."
]
for b in bullets:
    p = tf.add_paragraph()
    p.text = f"• {b}"
    p.font.size = Pt(13)
    p.font.color.rgb = C_SLATE_TEXT
    p.space_after = Pt(8)

# Right Column: 3 Core Objectives
add_card(s2, 6.8, 1.5, 5.7, 5.4, RGBColor(0xF0, 0xFD, 0xFA), RGBColor(0x0D, 0x94, 0x88))
tb_r = s2.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(5.0))
tf_r = tb_r.text_frame
tf_r.word_wrap = True
p = tf_r.paragraphs[0]
p.text = "BA MỤC TIÊU KỸ THUẬT CỐT LÕI CỦA ĐỀ TÀI"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = C_EMERALD

objs = [
    ("MỤC TIÊU 1: GIẢM ĐỘ TRỄ MẠNG (LATENCY)", "Phát hiện chính xác các trạm BTS bị nghẽn đường truyền Backhaul và hàng đợi giao diện vô tuyến. Hỗ trợ định tuyến tối ưu lưu lượng để đưa độ trễ toàn mạng về mức chuẩn viễn thông < 50 ms."),
    ("MỤC TIÊU 2: GIẢM TỶ LỆ MẤT GÓI (PACKET LOSS)", "Cô lập các cell vô tuyến bị can nhiễu đồng kênh, lỗi công suất phát hoặc tràn bộ đệm định tuyến khi phục vụ trên 150 người dùng đồng thời, giữ tỷ lệ mất gói < 1.0%."),
    ("MỤC TIÊU 3: GIẢM TỶ LỆ RỚT CUỘC GỌI (CALL DROP RATE)", "Tối ưu hóa vùng phủ sóng và tham số chuyển giao (Handover Margin 3dB -> 5dB), kéo giảm tỷ lệ rớt cuộc gọi về dưới mức cam kết chất lượng dịch vụ SLA (2.0%).")
]
for t_obj, d_obj in objs:
    p = tf_r.add_paragraph()
    p.text = f"🎯 {t_obj}"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_DARK
    p.space_before = Pt(8)
    p_d = tf_r.add_paragraph()
    p_d.text = d_obj
    p_d.font.size = Pt(12)
    p_d.font.color.rgb = C_SLATE_TEXT
    p_d.space_after = Pt(8)

# ==============================================================================
# SLIDE 3: ĐẶC TRƯNG BIG DATA 5V TRONG VIỄN THÔNG
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
create_header(s3, "2. PHÂN TÍCH 5 ĐẶC TRƯNG DỮ LIỆU LỚN (BIG DATA 5V)")

v_cards = [
    ("VOLUME (Quy mô)", "3.5 tỷ sự kiện/ngày\n10 - 25 GB log/ngày\nHàng chục Terabyte/năm\nĐòi hỏi lưu trữ HDFS phân tán", C_BLUE, RGBColor(0xEF, 0xF6, 0xFF)),
    ("VELOCITY (Tốc độ)", "Chu kỳ đo 1s - 5s/lần\n500,000 sự kiện/giây cao điểm\nYêu cầu cảnh báo < 1s\nFlume & HBase độ trễ thấp", C_GOLD, RGBColor(0xFE, 0xF3, 0xC7)),
    ("VARIETY (Đa dạng)", "Có cấu trúc: Danh mục BTS, Cell\nBán cấu trúc: Syslog RFC-5424, XML\nDữ liệu luồng: CDR/xDR, KPI Stream\nPha trộn mạng 3G, 4G, 5G", C_EMERALD, RGBColor(0xEC, 0xFD, 0xF5)),
    ("VERACITY (Độ tin cậy)", "Nhiễu vô tuyến, thời tiết mưa bão\nLệch đồng hồ NTP gây trễ âm\nTràn bộ đếm gây thông lượng âm\nCần lọc sạch và xác thực kỹ", C_RED, RGBColor(0xFE, 0xF2, 0xF2)),
    ("VALUE (Giá trị)", "Giảm rớt cuộc gọi & giảm độ trễ\nKéo giảm tỷ lệ rời mạng Churn\nChăm sóc khách hàng chủ động\nTối ưu hóa chi phí đầu tư CAPEX", RGBColor(0x7C, 0x3A, 0xED), RGBColor(0xF5, 0xF3, 0xFF)),
]

for idx, (v_name, v_desc, col_hdr, col_bg) in enumerate(v_cards):
    x_pos = 0.8 + idx * 2.4
    card = add_card(s3, x_pos, 1.6, 2.2, 5.2, col_bg, col_hdr)
    tb = s3.shapes.add_textbox(Inches(x_pos + 0.1), Inches(1.8), Inches(2.0), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = v_name
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = col_hdr
    p.alignment = PP_ALIGN.CENTER
    
    p_d = tf.add_paragraph()
    p_d.text = "\n" + v_desc
    p_d.font.size = Pt(12)
    p_d.font.color.rgb = C_SLATE_TEXT
    p_d.alignment = PP_ALIGN.CENTER

# ==============================================================================
# SLIDE 4: KIẾN TRÚC TỔNG THỂ HỆ THỐNG (LAMBDA ARCHITECTURE)
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
create_header(s4, "3. KIẾN TRÚC TỔNG THỂ HỆ THỐNG (LAMBDA ARCHITECTURE)")

img_arch = os.path.join(img_dir, "hinh_1_1_kien_truc_tong_the.png")
if os.path.exists(img_arch):
    s4.shapes.add_picture(img_arch, Inches(0.8), Inches(1.4), width=Inches(11.733))

# ==============================================================================
# SLIDE 5: MÔ HÌNH DỮ LIỆU VIỄN THÔNG (ERD SCHEMA)
# ==============================================================================
s5 = prs.slides.add_slide(blank_layout)
create_header(s5, "4. MÔ HÌNH DỮ LIỆU & QUAN HỆ CÁC THỰC THỂ (ERD SCHEMA)")

img_erd = os.path.join(img_dir, "hinh_2_1_mo_hinh_du_lieu.png")
if os.path.exists(img_erd):
    s5.shapes.add_picture(img_erd, Inches(0.8), Inches(1.4), width=Inches(11.733))

# ==============================================================================
# SLIDE 6: TỔNG QUAN 4 TẬP DỮ LIỆU & TIỀN XỬ LÝ
# ==============================================================================
s6 = prs.slides.add_slide(blank_layout)
create_header(s6, "5. KHẢO SÁT DỮ LIỆU, MA TRẬN RỦI RO & LÀM SẠCH")

add_card(s6, 0.8, 1.5, 5.6, 5.4, C_WHITE)
tb = s6.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(5.0))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "KHẢO SÁT 4 TẬP DỮ LIỆU THỰC NGHIỆM"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = C_BLUE

dsets = [
    ("network_kpi_events.csv", "12,000 bản ghi đo kiểm phiên; lưu thông lượng, độ trễ, mất gói, cờ rớt cuộc gọi, active users."),
    ("bts_towers.csv", "Danh mục 500 trạm BTS; mã trạm, tên trạm, tỉnh thành, quận huyện, kinh độ, vĩ độ, ngày lắp đặt."),
    ("cells_catalog.csv", "Danh mục sector cell vô tuyến; công nghệ 3G/4G/5G, dải tần MHz, băng thông tối đa, góc ngửa azimuth."),
    ("customer_complaints.csv", "Bản ghi khiếu nại khách hàng; số thuê bao msisdn, loại sự cố rớt mạng, trạng thái xử lý.")
]
for dname, ddesc in dsets:
    p = tf.add_paragraph()
    p.text = f"📁 {dname}: "
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_DARK
    p.space_before = Pt(4)
    p_d = tf.add_paragraph()
    p_d.text = ddesc
    p_d.font.size = Pt(11)
    p_d.font.color.rgb = C_SLATE_TEXT
    p_d.space_after = Pt(4)

add_card(s6, 6.8, 1.5, 5.7, 5.4, RGBColor(0xFE, 0xF2, 0xF2), C_RED)
tb_r = s6.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(5.0))
tf_r = tb_r.text_frame
tf_r.word_wrap = True
p = tf_r.paragraphs[0]
p.text = "MA TRẬN LỖI DỊ THƯỜNG & LÀM SẠCH"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = C_RED

risks = [
    ("Độ trễ âm (latency < 0 ms)", "Do lệch xung đồng hồ NTP giữa BTS và server -> Lọc bỏ hoàn toàn bằng filter."),
    ("Thông lượng âm (throughput < 0)", "Do tràn bộ đếm byte phần mềm nhúng cũ -> Loại bỏ trong bước làm sạch."),
    ("Mất gói vô lý (packet_loss > 100%)", "Do suy hao đa đường phân kỳ -> Ràng buộc miền giá trị [0, 100%]."),
    ("Bản ghi mồ côi (tower_id NULL)", "Do lỗi đóng gói telemetry trên Backhaul -> Lọc bỏ trước khi Join."),
    ("Hiệu quả làm sạch", "12,000 bản ghi thô -> Loại bỏ 48 bản ghi rác (0.40%) -> Giữ lại 11,952 bản ghi sạch 100%.")
]
for rname, rdesc in risks:
    p = tf_r.add_paragraph()
    p.text = f"⚠️ {rname}"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_DARK
    p.space_before = Pt(4)
    p_d = tf_r.add_paragraph()
    p_d.text = rdesc
    p_d.font.size = Pt(11)
    p_d.font.color.rgb = C_SLATE_TEXT
    p_d.space_after = Pt(4)

# ==============================================================================
# SLIDE 7: HẠ TẦNG HDFS DATA LAKE & DUNG LỖI
# ==============================================================================
s7 = prs.slides.add_slide(blank_layout)
create_header(s7, "6. TỔ CHỨC LƯU TRỮ PHÂN TÁN HDFS & CƠ CHẾ DUNG LỖI")

# 4 Zones
zones = [
    ("1. RAW ZONE (/telecom/raw/)", "Chứa 100% log thô bất biến (Immutable)\nChỉ cấp quyền ghi cho tiến trình Flume\nLưu trữ lâu dài phục vụ kiểm toán dữ liệu", C_BLUE),
    ("2. STAGING ZONE (/telecom/staging/)", "Vùng đệm trung chuyển tạm thời cho ETL\nGiải nén, kiểm tra hợp lệ, khử trùng lặp\nDữ liệu có vòng đời ngắn tự xóa sau 7 ngày", C_GOLD),
    ("3. CURATED ZONE (/telecom/curated/)", "Dữ liệu sạch chuẩn hóa Snappy Parquet\nPhân vùng theo ngày và mã trạm BTS\nNguồn dữ liệu Single Source of Truth", C_EMERALD),
    ("4. OUTPUT ZONE (/telecom/output/)", "Chứa bảng chỉ số KPI tổng hợp cấp cao\nDanh sách cảnh báo trạm suy thoái nghiêm trọng\nPhục vụ trực tiếp BI, BigSheets và R Studio", RGBColor(0x7C, 0x3A, 0xED))
]
for idx, (z_title, z_desc, z_col) in enumerate(zones):
    x_pos = 0.8 + idx * 2.95
    card = add_card(s7, x_pos, 1.5, 2.8, 2.6, RGBColor(0xF8, 0xFA, 0xFC), z_col)
    tb = s7.shapes.add_textbox(Inches(x_pos + 0.1), Inches(1.6), Inches(2.6), Inches(2.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = z_title
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = z_col
    p_d = tf.add_paragraph()
    p_d.text = "\n" + z_desc
    p_d.font.size = Pt(11)
    p_d.font.color.rgb = C_SLATE_TEXT

# Bottom Box: Replication & Fault Tolerance
add_card(s7, 0.8, 4.4, 11.733, 2.5, RGBColor(0xDB, 0xEA, 0xFE), C_BLUE)
tb_b = s7.shapes.add_textbox(Inches(1.0), Inches(4.5), Inches(11.333), Inches(2.3))
tf_b = tb_b.text_frame
tf_b.word_wrap = True
p = tf_b.paragraphs[0]
p.text = "CƠ CHẾ DUNG LỖI & TÍNH TOÁN DUNG LƯỢNG HDFS (REPLICATION FACTOR = 3)"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = C_NAVY_DARK

points = [
    "Cơ chế tự phục hồi (Auto Self-Healing): Heartbeat 3s giữa NameNode và DataNode. Nếu sau 10.5 phút mất tín hiệu, NameNode tuyên bố DataNode chết và tự động nhân bản các Under-replicated blocks sang DataNode khác để duy trì đúng RF = 3.",
    "Kích thước khối 128 MB: Giảm thiểu số lượng block và tải quản lý metadata trên bộ nhớ RAM của NameNode.",
    "Tính toán dung lượng cho 500 trạm BTS (2,000 cell): 34.56 triệu sự kiện/ngày = 8.85 GB thô/ngày. Nén Parquet Snappy (giảm 65%) + 10% metadata + RF=3 = 10.22 GB HDFS/ngày -> 3.73 Terabyte HDFS/năm (13.58 TB cho 3 năm)."
]
for pt in points:
    p = tf_b.add_paragraph()
    p.text = f"• {pt}"
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_NAVY_DARK
    p.space_after = Pt(3)

# ==============================================================================
# SLIDE 8: THU THẬP LOG VỚI APACHE FLUME
# ==============================================================================
s8 = prs.slides.add_slide(blank_layout)
create_header(s8, "7. KIẾN TRÚC THU THẬP ĐẦU-CUỐI VỚI APACHE FLUME")

img_pipe = os.path.join(img_dir, "hinh_3_1_pipeline_xu_ly.png")
if os.path.exists(img_pipe):
    s8.shapes.add_picture(img_pipe, Inches(0.8), Inches(1.4), width=Inches(11.733))

# ==============================================================================
# SLIDE 9: XỬ LÝ PHÂN TÁN VỚI APACHE SPARK
# ==============================================================================
s9 = prs.slides.add_slide(blank_layout)
create_header(s9, "8. PIPELINE XỬ LÝ IN-MEMORY VỚI APACHE SPARK & SPARK SQL")

add_card(s9, 0.8, 1.5, 5.6, 5.4, C_WHITE)
tb = s9.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(5.0))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "TỐI ƯU HÓA ĐỘNG CƠ SPARK"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = C_BLUE

spark_tech = [
    ("Catalyst Optimizer", "Tự động tối ưu hóa cây kế hoạch truy vấn logic và vật lý, tự động đẩy các điều kiện lọc (Predicate Pushdown) xuống tận tầng lưu trữ tệp."),
    ("Tungsten Engine", "Quản lý bộ nhớ off-heap trực tiếp, giải phóng áp lực rác Java GC, biên dịch mã bytecode tức thời (Whole-stage Code Generation)."),
    ("Chiến lược Persist()", "Áp dụng df_joined.persist(MEMORY_AND_DISK) ngay sau phép Join 4 bảng, giúp 2 nhánh phân tích tiếp theo không phải tính toán lại từ đầu."),
    ("Spark SQL Views", "Đăng ký bảng tạm v_kpi_telecom, cung cấp cú pháp ANSI SQL trực quan, gom nhóm theo trạm và công nghệ.")
]
for stitle, sdesc in spark_tech:
    p = tf.add_paragraph()
    p.text = f"⚡ {stitle}: "
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_DARK
    p.space_before = Pt(4)
    p_d = tf.add_paragraph()
    p_d.text = sdesc
    p_d.font.size = Pt(11)
    p_d.font.color.rgb = C_SLATE_TEXT
    p_d.space_after = Pt(4)

add_card(s9, 6.8, 1.5, 5.7, 5.4, RGBColor(0x0F, 0x17, 0x2A), C_NAVY_DARK)
tb_code = s9.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(5.0))
tf_code = tb_code.text_frame
tf_code.word_wrap = True
p = tf_code.paragraphs[0]
p.text = "TRÍCH ĐOẠN MÃ NGUỒN PYSPARK CỐT LÕI"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = RGBColor(0x38, 0xBD, 0xF8)

p_c = tf_code.add_paragraph()
p_c.text = """# Đọc, lọc sạch và tính cột phái sinh
df_clean = spark.read.csv(events_path, header=True) \\
    .filter((col("latency_ms") >= 0) & 
            (col("packet_loss_pct") <= 100)) \\
    .withColumn("session_mb", (col("throughput")*5)/8)

# Join 4 bảng: Events, Towers, Cells, Complaints
df_joined = df_clean.join(df_towers, "tower_id") \\
    .join(df_cells, ["tower_id", "cell_id"]) \\
    .join(df_complaints, ["tower_id", "cell_id"], "left")

# Tính toán chỉ số KPI bằng Spark SQL
df_summary = spark.sql(\"\"\"
    SELECT tower_id, province, technology,
           COUNT(event_id) AS total_sessions,
           ROUND(AVG(latency_ms), 2) AS avg_lat,
           ROUND((SUM(call_dropped)/COUNT(1))*100, 2) AS cdr_pct,
           CASE WHEN AVG(latency_ms) > 80 THEN 'DEGRADED'
                ELSE 'NORMAL' END AS status
    FROM v_telecom GROUP BY tower_id, province, technology
\"\"\")"""
p_c.font.size = Pt(10)
p_c.font.name = "Consolas"
p_c.font.color.rgb = RGBColor(0xE2, 0xE8, 0xF0)

# ==============================================================================
# SLIDE 10: THUẬT TOÁN MAPREDUCE TỐI ƯU
# ==============================================================================
s10 = prs.slides.add_slide(blank_layout)
create_header(s10, "9. THUẬT TOÁN MAPREDUCE TỐI ƯU (COMPOSITE KEY & PARTITIONER)")

img_mr = os.path.join(img_dir, "hinh_3_2_luong_mapreduce.png")
if os.path.exists(img_mr):
    s10.shapes.add_picture(img_mr, Inches(0.8), Inches(1.4), width=Inches(11.733))

# ==============================================================================
# SLIDE 11: KỊCH BẢN PIG LATIN
# ==============================================================================
s11 = prs.slides.add_slide(blank_layout)
create_header(s11, "10. KỊCH BẢN ETL & PHÂN CỤM TRẠM LỖI VỚI APACHE PIG LATIN")

add_card(s11, 0.8, 1.5, 5.6, 5.4, C_WHITE)
tb = s11.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(5.0))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "CÁC BƯỚC XỬ LÝ PIG LATIN"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = C_GOLD

pig_steps = [
    ("Khai báo Schema tường minh", "LOAD dữ liệu với định dạng chuẩn PigStorage(',') và kiểu dữ liệu chính xác (double, int, chararray)."),
    ("Lọc và Khử trùng lặp", "Áp dụng mệnh đề FILTER loại bỏ dữ liệu âm, lỗi cảm biến và DISTINCT để đảm bảo tính duy nhất."),
    ("Join 3 bảng", "JOIN giữa sự kiện với bts_catalog theo tower_id và cells_catalog theo cell_id."),
    ("Gom nhóm đa chiều", "GROUP BY theo (tower_id, technology) để tính toán KPI trên từng băng tần."),
    ("Tối ưu hóa Nested ORDER", "Giải pháp vượt qua lỗi Deserialization trên Hadoop 3.3.6: GROUP ALL và ORDER/LIMIT 10 cục bộ trong Reducer."),
    ("Kết quả thực thi YARN (Job 0027)", "Hoàn thành trong 18.0 giây; cấp phát 62,755 MB-seconds; trích xuất chính xác Top 10 trạm suy thoái.")
]
for pst, pdesc in pig_steps:
    p = tf.add_paragraph()
    p.text = f"🐖 {pst}: "
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_DARK
    p.space_before = Pt(4)
    p_d = tf.add_paragraph()
    p_d.text = pdesc
    p_d.font.size = Pt(11)
    p_d.font.color.rgb = C_SLATE_TEXT
    p_d.space_after = Pt(4)

add_card(s11, 6.8, 1.5, 5.7, 5.4, RGBColor(0x0F, 0x17, 0x2A), C_NAVY_DARK)
tb_code = s11.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(5.0))
tf_code = tb_code.text_frame
tf_code.word_wrap = True
p = tf_code.paragraphs[0]
p.text = "KỊCH BẢN PIG LATIN THỰC THI (Job 0027)"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = RGBColor(0xFB, 0xBF, 0x24)

p_c = tf_code.add_paragraph()
p_c.text = """-- Nạp và lọc dữ liệu sạch
events_clean = FILTER raw_events BY 
    (latency_ms >= 0.0) AND (throughput_mbps >= 0.0);

-- Join 3 bảng và gom nhóm
joined = JOIN events_clean BY tower_id, towers BY tower_id;
grp = GROUP joined BY (events_clean::tower_id, events_clean::technology);

-- Tính toán KPI
kpi_summary = FOREACH grp GENERATE group.tower_id, group.technology,
    COUNT(joined) AS total_events,
    ROUND_TO(AVG(joined.events_clean::latency_ms), 2) AS avg_lat,
    ROUND_TO((SUM(joined.events_clean::call_dropped)*100.0/COUNT(joined)), 3) AS cdr_pct;

-- Tách trạm suy thoái & Lấy Top 10
degraded_towers = FILTER kpi_summary BY (cdr_pct > 2.0) OR (avg_lat > 80.0);
grouped_all = GROUP degraded_towers ALL;
top10 = FOREACH grouped_all {
    sorted = ORDER degraded_towers BY cdr_pct DESC;
    LIMIT sorted 10;
};
STORE top10 INTO '/telecom/output/top10_pig';"""
p_c.font.size = Pt(9.5)
p_c.font.name = "Consolas"
p_c.font.color.rgb = RGBColor(0xE2, 0xE8, 0xF0)

# ==============================================================================
# SLIDE 12: THIẾT KẾ HBASE NOSQL
# ==============================================================================
s12 = prs.slides.add_slide(blank_layout)
create_header(s12, "11. THIẾT KẾ CƠ SỞ DỮ LIỆU NOSQL APACHE HBASE (< 10ms)")

add_card(s12, 0.8, 1.5, 5.6, 5.4, C_WHITE)
tb = s12.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(5.0))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "THIẾT KẾ ROWKEY & COLUMN FAMILIES"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = C_BLUE

hb_tech = [
    ("Thiết kế RowKey", "reverse(tower_id) + '_' + reverse_timestamp (VD: '100_REWOT_9223372036854775807'). Đảo ngược timestamp giúp sự kiện MỚI NHẤT luôn nằm ở ĐẦU TIÊN, truy vấn NOC Scan lấy ngay dữ liệu nóng không phải duyệt lịch sử."),
    ("Chống Hotspotting", "Đảo ngược chuỗi tower_id kết hợp Pre-splitting phân tán đều khóa ghi trên các RegionServer, triệt tiêu nghẽn cổ chai ghi."),
    ("Column Family 1: kpi_metrics", "Lưu avg_throughput, avg_latency, avg_packet_loss, call_drop_rate, active_users. VERSIONS = 3, TTL = 90 ngày (7776000s)."),
    ("Column Family 2: status_flags", "Lưu cờ cảnh báo health_category, has_complaint, degradation_flag. VERSIONS = 1."),
    ("Nén Snappy", "Kích hoạt nén Snappy trên toàn bộ Column Families, giảm 60% dung lượng HDFS mà không suy giảm tốc độ CPU.")
]
for hbt, hbdesc in hb_tech:
    p = tf.add_paragraph()
    p.text = f"🧱 {hbt}: "
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_DARK
    p.space_before = Pt(4)
    p_d = tf.add_paragraph()
    p_d.text = hbdesc
    p_d.font.size = Pt(11)
    p_d.font.color.rgb = C_SLATE_TEXT
    p_d.space_after = Pt(4)

add_card(s12, 6.8, 1.5, 5.7, 5.4, RGBColor(0xEC, 0xFD, 0xF5), C_EMERALD)
tb_r = s12.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(5.0))
tf_r = tb_r.text_frame
tf_r.word_wrap = True
p = tf_r.paragraphs[0]
p.text = "CƠ CHẾ LƯU TRỮ LSM-TREE & BẢO MẬT"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = C_EMERALD

hb_adv = [
    ("LSM-Tree & MemStore", "Dữ liệu ghi vào WAL và MemStore trên RAM trước khi flush xuống HFile trên đĩa. Thao tác ghi đạt tốc độ hàng trăm nghìn event/s."),
    ("Độ trễ truy cập tức thời", "HBase cung cấp API Get/Scan ngẫu nhiên với độ trễ < 10 mili-giây, đáp ứng tiêu chuẩn cho Dashboard điều hành NOC thời gian thực."),
    ("Cơ chế Snapshot không gián đoạn", "Lệnh snapshot 'telecom_kpi', 'telecom_kpi_snap' chụp ảnh metadata trong 1-2s mà không cần disable bảng, bảo toàn liên tục dịch vụ."),
    ("Phân quyền bảo mật ACL", "Cấp quyền RW cho đội NOC/SOC (telecom_ops), quyền R cho đội phân tích BI (telecom_analysts), và RWCA cho quản trị viên hệ thống.")
]
for hat, hadesc in hb_adv:
    p = tf_r.add_paragraph()
    p.text = f"🛡️ {hat}: "
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_DARK
    p.space_before = Pt(4)
    p_d = tf_r.add_paragraph()
    p_d.text = hadesc
    p_d.font.size = Pt(11)
    p_d.font.color.rgb = C_SLATE_TEXT
    p_d.space_after = Pt(4)

# ==============================================================================
# SLIDE 13: MÔ PHỎNG PHÂN TÍCH VỚI BIGSHEETS
# ==============================================================================
s13 = prs.slides.add_slide(blank_layout)
create_header(s13, "12. MÔ PHỎNG PHÂN TÍCH NGHIỆP VỤ NO-CODE VỚI BIGSHEETS")

img_bs = os.path.join(img_dir, "bigsheets_dashboard_preview.jpg")
if os.path.exists(img_bs):
    s13.shapes.add_picture(img_bs, Inches(0.8), Inches(1.4), width=Inches(11.733))

# ==============================================================================
# SLIDE 14: KHOA HỌC DỮ LIỆU & HỌC MÁY BẰNG R VÀ SQLITE
# ==============================================================================
s14 = prs.slides.add_slide(blank_layout)
create_header(s14, "13. KHOA HỌC DỮ LIỆU & MÔ HÌNH HỒI QUY LOGISTIC BẰNG R")

img_r = os.path.join(img_dir, "rstudio_execution_preview.png")
if os.path.exists(img_r):
    s14.shapes.add_picture(img_r, Inches(0.8), Inches(1.4), width=Inches(11.733))

# ==============================================================================
# SLIDE 15: KẾT QUẢ THỰC NGHIỆM TOP 10 TRẠM LỖI
# ==============================================================================
s15 = prs.slides.add_slide(blank_layout)
create_header(s15, "14. KẾT QUẢ THỰC NGHIỆM: TOP 10 TRẠM BTS CHẤT LƯỢNG KÉM NHẤT")

img_top10 = os.path.join(img_dir, "chart_bigsheets_top10_worst_towers.png")
if os.path.exists(img_top10):
    s15.shapes.add_picture(img_top10, Inches(0.8), Inches(1.4), width=Inches(11.733))

# ==============================================================================
# SLIDE 16: TRỰC QUAN HÓA CHẤT LƯỢNG MẠNG
# ==============================================================================
s16 = prs.slides.add_slide(blank_layout)
create_header(s16, "15. TRỰC QUAN HÓA CHUYÊN SÂU: ĐỘ TRỄ, MẤT GÓI & RỚT MẠNG")

img_ch1 = os.path.join(img_dir, "chart1_latency_by_tech.png")
img_ch2 = os.path.join(img_dir, "chart2_packet_loss_vs_drop_rate.png")

if os.path.exists(img_ch1) and os.path.exists(img_ch2):
    s16.shapes.add_picture(img_ch1, Inches(0.8), Inches(1.5), width=Inches(5.7))
    s16.shapes.add_picture(img_ch2, Inches(6.8), Inches(1.5), width=Inches(5.7))

# ==============================================================================
# SLIDE 17: ĐỐI CHIẾU HIỆU NĂNG CÔNG NGHỆ
# ==============================================================================
s17 = prs.slides.add_slide(blank_layout)
create_header(s17, "16. ĐỐI CHIẾU ĐỊNH LƯỢNG HIỆU NĂNG: SPARK VS MAPREDUCE VS PIG VS R")

add_card(s17, 0.8, 1.5, 11.733, 5.4, C_WHITE)
tb = s17.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(11.333), Inches(5.2))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "MA TRẬN SO SÁNH ĐỊNH LƯỢNG HIỆU NĂNG & TÀI NGUYÊN"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = C_NAVY_DARK

table_data = [
    ("Tiêu chí đánh giá", "Apache Spark & SQL", "Hadoop MapReduce (Java)", "Apache Pig Latin", "R & SQLite Analysis"),
    ("Thời gian chạy (Runtime)", "2.3 giây (Nhanh nhất)", "35.4 giây (Chậm nhất)", "18.0 giây (Trung bình)", "1.8 giây (Đơn máy)"),
    ("Cơ chế tính toán", "Đồ thị DAG In-Memory RAM", "2 pha đĩa cứng Map -> Reduce", "Dịch sang MapReduce/Tez", "Xử lý Vector hóa trong RAM"),
    ("Lưu lượng Disk I/O", "Rất thấp (Giảm 85% I/O)", "Rất lớn (Spill map, merge sort)", "Trung bình (Ghi đĩa sau Map)", "Rất thấp (Đọc file SQLite)"),
    ("Bộ tối ưu ngầm định", "Catalyst Optimizer & Tungsten", "Thủ công (Combiner, Partitioner)", "Pig Logical Optimizer", "SQLite B-Tree Index"),
    ("Độ phức tạp mã nguồn", "Ngắn gọn, dễ đọc (50 dòng PySpark)", "Dài, phức tạp (300+ dòng Java)", "Rất ngắn (25 dòng Pig Latin)", "Chuyên sâu thống kê (80 dòng R)"),
    ("Vai trò kiến trúc", "Xử lý phân tán chính & Streaming", "Batch job cực lớn qua đêm", "ETL chuyển đổi nhanh Data Lake", "Data Science, ML dự báo & Visual")
]

for row in table_data:
    p = tf.add_paragraph()
    is_hdr = (row[0] == "Tiêu chí đánh giá")
    p.text = f"{row[0]:<28} | {row[1]:<24} | {row[2]:<24} | {row[3]:<20} | {row[4]}"
    p.font.size = Pt(11)
    p.font.name = "Consolas"
    p.font.bold = is_hdr
    p.font.color.rgb = C_BLUE if is_hdr else C_SLATE_TEXT
    p.space_after = Pt(4)

# ==============================================================================
# SLIDE 18: NĂM KHUYẾN NGHỊ HÀNH ĐỘNG CHO TRUNG TÂM NOC
# ==============================================================================
s18 = prs.slides.add_slide(blank_layout)
create_header(s18, "17. NĂM KHUYẾN NGHỊ HÀNH ĐỘNG TỐI ƯU HÓA MẠNG NOC")

recs = [
    ("KHUYẾN NGHỊ 1 (Ưu tiên P1 - 48 giờ)", "Can thiệp khẩn cấp Top 3 trạm lỗi TOWER_003, TOWER_008, TOWER_015:", "Điều xe phát sóng COW chia tải vô tuyến; nâng cấp cáp quang Backhaul từ 100Mbps lên 1Gbps.", C_RED),
    ("KHUYẾN NGHỊ 2 (Ưu tiên P2 - 6 tháng)", "Tắt sóng 3G (Sunset 3G) và Tái quy hoạch băng tần:", "CDR của 3G gấp 8 lần 5G. Tái quy hoạch tần số 2100MHz sang cho mạng 4G/5G để tăng 40% dung lượng.", C_GOLD),
    ("KHUYẾN NGHỊ 3 (Ưu tiên P3 - 2 tuần)", "Kích hoạt tính năng Mạng tự tối ưu (SON):", "Bật tính năng Mobility Load Balancing tự động san tải thuê bao từ cell quá tải sang cell rảnh rỗi.", C_BLUE),
    ("KHUYẾN NGHỊ 4 (Ưu tiên P4 - 1 tháng)", "Chăm sóc khách hàng chủ động (Proactive CSKH):", "Tích hợp kết quả dự báo R vào CRM; tự động gửi SMS xin lỗi kèm voucher data khi thuê bao rớt mạng.", C_EMERALD),
    ("KHUYẾN NGHỊ 5 (Ưu tiên P5 - 3 tháng)", "Tối ưu hóa Data Lake & Định dạng Parquet:", "Lưu trữ Snappy Parquet tiết kiệm 65% đĩa; đặt chính sách TTL 90 ngày trên HBase dọn dẹp log cũ.", RGBColor(0x7C, 0x3A, 0xED)),
]

for idx, (r_title, r_sub, r_act, r_col) in enumerate(recs):
    y_pos = 1.45 + idx * 1.15
    card = add_card(s18, 0.8, y_pos, 11.733, 1.05, RGBColor(0xF8, 0xFA, 0xFC), r_col)
    tb = s18.shapes.add_textbox(Inches(1.0), Inches(y_pos + 0.08), Inches(11.333), Inches(0.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = f"{r_title} - {r_sub}"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = r_col
    p_d = tf.add_paragraph()
    p_d.text = f"👉 Hành động kỹ thuật: {r_act}"
    p_d.font.size = Pt(11.5)
    p_d.font.color.rgb = C_NAVY_DARK

# ==============================================================================
# SLIDE 19: KẾT LUẬN & HƯỚNG PHÁT TRIỂN
# ==============================================================================
s19 = prs.slides.add_slide(blank_layout)
create_header(s19, "18. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN TIẾP THEO")

add_card(s19, 0.8, 1.5, 5.6, 5.4, RGBColor(0xF0, 0xFD, 0xF4), C_EMERALD)
tb = s19.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(5.0))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "CÁC KẾT QUẢ ĐẠT ĐƯỢC"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = C_EMERALD

achieves = [
    "Làm chủ hệ sinh thái Big Data: Tích hợp hoàn hảo Hadoop HDFS, YARN, Flume, Spark, Pig, HBase, BigSheets và R.",
    "Thuật toán tối ưu hóa sâu: Thiết kế Composite Key và Custom Partitioner triệt tiêu Data Skew; Combiner giảm 80% I/O.",
    "Giải quyết 3 mục tiêu cốt lõi: Định lượng nguyên nhân gây trễ cao, mất gói và rớt cuộc gọi; cô lập chính xác trạm nghẽn.",
    "Mô hình học máy thực tiễn: Hồi quy Logistic bằng R đạt độ tin cậy cao, lượng hóa nguy cơ khiếu nại khách hàng.",
    "Đóng gói bàn giao trọn vẹn: Đầy đủ Báo cáo Word/PDF, Slide thuyết minh, SourceCode, Data, Output và README.md."
]
for ac in achieves:
    p = tf.add_paragraph()
    p.text = f"✅ {ac}"
    p.font.size = Pt(12)
    p.font.color.rgb = C_NAVY_DARK
    p.space_after = Pt(6)

add_card(s19, 6.8, 1.5, 5.7, 5.4, RGBColor(0xEF, 0xF6, 0xFF), C_BLUE)
tb_r = s19.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(5.0))
tf_r = tb_r.text_frame
tf_r.word_wrap = True
p = tf_r.paragraphs[0]
p.text = "HƯỚNG PHÁT TRIỂN TƯƠNG LAI"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = C_BLUE

futures = [
    ("Kiến trúc Streaming Sub-second", "Triển khai cụm Apache Kafka phân tán độc lập và Apache Flink xử lý luồng sự kiện theo cửa sổ trượt (Sliding Windows) với độ trễ < 50ms."),
    ("Ứng dụng AIOps & Deep Learning", "Nghiên cứu áp dụng mạng nơ-ron đồ thị (GNN) và LSTM để tự động phát hiện bất thường trên toàn mạng và dự báo trước sự cố truyền dẫn 30 - 60 phút."),
    ("Mạng tự tối ưu vòng kín (Closed-Loop SON)", "Tự động gửi tham số điều chỉnh công suất phát và góc ngửa anten trực tiếp xuống bộ điều khiển RAN Controller không cần can thiệp thủ công."),
    ("Thử nghiệm cụm máy chủ vật lý đa Node", "Mở rộng kiểm thử tải thực tế trên cụm máy chủ vật lý phân tán quy mô 10 - 20 node trong môi trường nhà mạng.")
]
for ftitle, fdesc in futures:
    p = tf_r.add_paragraph()
    p.text = f"🚀 {ftitle}: "
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_DARK
    p.space_before = Pt(4)
    p_d = tf_r.add_paragraph()
    p_d.text = fdesc
    p_d.font.size = Pt(11)
    p_d.font.color.rgb = C_SLATE_TEXT
    p_d.space_after = Pt(4)

# ==============================================================================
# SLIDE 20: KẾT THÚC & Q&A
# ==============================================================================
s20 = prs.slides.add_slide(blank_layout)
bg20 = s20.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg20.fill.solid()
bg20.fill.fore_color.rgb = C_NAVY_DARK
bg20.line.fill.background()

tb20 = s20.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.333), Inches(3.0))
tf20 = tb20.text_frame
tf20.word_wrap = True

p_thx = tf20.paragraphs[0]
p_thx.text = "XIN TRÂN TRỌNG CẢM ƠN!"
p_thx.font.size = Pt(36)
p_thx.font.bold = True
p_thx.font.color.rgb = C_GOLD
p_thx.alignment = PP_ALIGN.CENTER

p_sub = tf20.add_paragraph()
p_sub.text = "CẢM ƠN QUÝ THẦY CÔ VÀ HỘI ĐỒNG ĐÃ LẮNG NGHE BÀI THUYẾT MINH"
p_sub.font.size = Pt(16)
p_sub.font.color.rgb = C_WHITE
p_sub.alignment = PP_ALIGN.CENTER

p_qa = tf20.add_paragraph()
p_qa.text = "\nKÍNH MỜI QUÝ THẦY CÔ VÀ CÁC BẠN ĐẶT CÂU HỎI (Q&A)"
p_qa.font.size = Pt(18)
p_qa.font.bold = True
p_qa.font.color.rgb = RGBColor(0x38, 0xBD, 0xF8)
p_qa.alignment = PP_ALIGN.CENTER

prs.save(output_pptx_path)
print(f"SUCCESS: Slide.pptx generated successfully with {len(prs.slides)} slides at: {output_pptx_path}")
