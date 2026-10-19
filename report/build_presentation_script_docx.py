# -*- coding: utf-8 -*-
"""
CHƯƠNG TRÌNH TỰ ĐỘNG TẠO FILE WORD: KỊCH BẢN THUYẾT TRÌNH BẢO VỆ BÀI TẬP LỚN
MÔN: XỬ LÝ DỮ LIỆU LỚN (CTKU122) - TRƯỜNG ĐẠI HỌC TÀI NGUYÊN VÀ MÔI TRƯỜNG HÀ NỘI
ĐỀ TÀI: PHÂN TÍCH CHẤT LƯỢNG MẠNG VIỄN THÔNG (HADOOP, SPARK, R)
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

output_path = r"c:\dulieulon\Kich_Ban_Thuyet_Trinh_Bao_Ve_BTL.docx"

doc = docx.Document()

# Margins: Left 3cm, Right 2cm, Top 2cm, Bottom 2cm
for section in doc.sections:
    section.top_margin = Inches(2.0 / 2.54)
    section.bottom_margin = Inches(2.0 / 2.54)
    section.left_margin = Inches(3.0 / 2.54)
    section.right_margin = Inches(2.0 / 2.54)

# Color Constants
C_NAVY = RGBColor(0x0F, 0x17, 0x2A)
C_BLUE = RGBColor(0x1E, 0x3A, 0x8A)
C_DARK_SLATE = RGBColor(0x1E, 0x29, 0x3B)
C_TEXT = RGBColor(0x33, 0x41, 0x55)
C_GOLD = RGBColor(0xB4, 0x53, 0x09)
C_EMERALD = RGBColor(0x04, 0x78, 0x57)
C_RED = RGBColor(0xDC, 0x26, 0x26)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_p(doc, text="", bold_prefix=None, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=5, line_spacing=1.25, italic=False, color=C_TEXT):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.font.name = 'Times New Roman'
        r_b.font.size = Pt(12)
        r_b.font.bold = True
        r_b.font.color.rgb = C_DARK_SLATE
    if text:
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.italic = italic
        r.font.color.rgb = color
    return p

def add_speech(doc, speaker, text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = 'Table Grid'
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=100, bottom=100, left=140, right=140)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.25
    r_spk = p.add_run(f"🎙️ Lời thoại [{speaker}]:\n")
    r_spk.font.name = 'Times New Roman'
    r_spk.font.size = Pt(11.5)
    r_spk.font.bold = True
    r_spk.font.color.rgb = C_BLUE

    r_txt = p.add_run(f'"{text}"')
    r_txt.font.name = 'Times New Roman'
    r_txt.font.size = Pt(11.5)
    r_txt.font.italic = True
    r_txt.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)

def add_callout(doc, title, text, bg_color="EFF6FF", border_title_color=C_BLUE):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = 'Table Grid'
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=90, bottom=90, left=130, right=130)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.2
    r_t = p.add_run(f"📌 {title}: ")
    r_t.font.name = 'Times New Roman'
    r_t.font.size = Pt(11)
    r_t.font.bold = True
    r_t.font.color.rgb = border_title_color

    r_txt = p.add_run(text)
    r_txt.font.name = 'Times New Roman'
    r_txt.font.size = Pt(11)
    r_txt.font.color.rgb = C_DARK_SLATE

    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)

def add_bullet(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.2
    p.paragraph_format.left_indent = Inches(0.25)
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.font.name = 'Times New Roman'
        r_b.font.size = Pt(12)
        r_b.font.bold = True
        r_b.font.color.rgb = C_DARK_SLATE
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.color.rgb = C_TEXT
    return p

def add_h1(doc, text):
    p = doc.add_paragraph(style='Heading 1')
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = C_NAVY
    return p

def add_h2(doc, text):
    p = doc.add_paragraph(style='Heading 2')
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = C_BLUE
    return p

def add_tbl(doc, headers, data, caption=None, col_widths=None):
    if caption:
        cp = doc.add_paragraph()
        cp.paragraph_format.space_before = Pt(8)
        cp.paragraph_format.space_after = Pt(3)
        cp.paragraph_format.keep_with_next = True
        c_run = cp.add_run(caption)
        c_run.font.name = 'Times New Roman'
        c_run.font.size = Pt(11)
        c_run.font.italic = True
        c_run.font.bold = True
        c_run.font.color.rgb = C_BLUE

    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    hdr_cells = table.rows[0].cells
    for idx, header_text in enumerate(headers):
        hdr_cells[idx].text = header_text
        set_cell_background(hdr_cells[idx], "1E3A8A")
        set_cell_margins(hdr_cells[idx], top=80, bottom=80, left=100, right=100)
        p = hdr_cells[idx].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for r_idx, row_data in enumerate(data):
        row_cells = table.rows[r_idx + 1].cells
        bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, cell_value in enumerate(row_data):
            row_cells[c_idx].text = str(cell_value)
            set_cell_background(row_cells[c_idx], bg_color)
            set_cell_margins(row_cells[c_idx], top=60, bottom=60, left=90, right=90)
            p = row_cells[c_idx].paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            if c_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(10)

    if col_widths:
        for row in table.rows:
            for idx, w in enumerate(col_widths):
                row.cells[idx].width = Inches(w)

    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)
    return table

print("Building Presentation Script Document...")

# ==============================================================================
# PHẦN 1: TRANG BÌA & THÔNG TIN CHUNG
# ==============================================================================
p_top = doc.add_paragraph()
p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
r1 = p_top.add_run("BỘ TÀI NGUYÊN VÀ MÔI TRƯỜNG\nTRƯỜNG ĐẠI HỌC TÀI NGUYÊN VÀ MÔI TRƯỜNG HÀ NỘI\nKHOA CÔNG NGHỆ THÔNG TIN • BỘ MÔN CÔNG NGHỆ THÔNG TIN\n")
r1.font.name = "Times New Roman"
r1.font.size = Pt(12)
r1.font.bold = True
r1.font.color.rgb = C_BLUE

p_line = doc.add_paragraph()
p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_line.paragraph_format.space_after = Pt(16)
r_line = p_line.add_run("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
r_line.font.bold = True
r_line.font.color.rgb = C_GOLD

p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_after = Pt(12)
r_sub = p_title.add_run("KỊCH BẢN THUYẾT MINH BẢO VỆ BÀI TẬP LỚN (ĐẠT ĐIỂM 10/10)\nHỌC PHẦN: XỬ LÝ DỮ LIỆU LỚN (MÃ HP: CTKU122)\n\n")
r_sub.font.name = "Times New Roman"
r_sub.font.size = Pt(13)
r_sub.font.bold = True
r_sub.font.color.rgb = C_DARK_SLATE

r_main = p_title.add_run("ĐỀ TÀI SỐ 01:\nXÂY DỰNG HỆ THỐNG PHÂN TÍCH VÀ GIÁM SÁT CHẤT LƯỢNG MẠNG VIỄN THÔNG (TELECOM QUALITY OF SERVICE ANALYTICS) TRÊN NỀN TẢNG HADOOP, SPARK VÀ R")
r_main.font.name = "Times New Roman"
r_main.font.size = Pt(15.5)
r_main.font.bold = True
r_main.font.color.rgb = C_BLUE

add_callout(
    doc,
    "HƯỚNG DẪN THỰC CHIẾN KHI BƯỚC VÀO PHÒNG BẢO VỆ",
    "Tài liệu này cung cấp kịch bản khẩu ngữ từng câu chữ khớp chính xác 100% với 20 Slide trình chiếu (Slide.pptx) và cấu trúc báo cáo 10 câu hỏi của môn Xử lý Dữ liệu lớn. Thời lượng thuyết trình chuẩn: 12 đến 15 phút trình bày (mỗi slide từ 30 đến 45 giây) + 5 đến 7 phút trả lời phản biện (Q&A). Nhóm có thể phân công 4 thành viên theo kịch bản phân vai hoặc 1 người làm đại diện thuyết trình toàn bộ.",
    bg_color="EFF6FF"
)

add_h1(doc, "I. BẢNG PHÂN BỔ THỜI GIAN VÀ PHÂN VAI THUYẾT TRÌNH (12 - 15 PHÚT)")

add_tbl(
    doc,
    headers=["Phần", "Slide", "Nội dung trọng tâm trình bày", "Thời lượng", "Người trình bày đề xuất"],
    data=[
        ["Phần 1", "Slide 1 - 4", "Giới thiệu, Đặt vấn đề, 3 Mục tiêu cốt lõi, Đặc trưng 5V & Kiến trúc Lambda", "3 phút", "Thành viên 1: Hoàng Ngọc Thi (Nhóm trưởng)"],
        ["Phần 2", "Slide 5 - 8", "Mô hình ERD, Tiền xử lý dữ liệu, HDFS Data Lake 4 vùng & Apache Flume Ingestion", "3 phút", "Thành viên 2: Nguyễn Viết Hoàng Anh"],
        ["Phần 3", "Slide 9 - 13", "Tính toán phân tán MapReduce Java, Pig Latin, Apache Spark In-Memory, HBase NoSQL & BigSheets", "4 phút", "Thành viên 3: Nguyễn Việt Hòa"],
        ["Phần 4", "Slide 14 - 18", "Khoa học dữ liệu R (Logistic Regression), Kết quả thực nghiệm Top trạm lỗi, Đối chiếu hiệu năng & 5 Khuyến nghị NOC", "3.5 phút", "Thành viên 4: Nguyễn Quốc Anh"],
        ["Phần 5", "Slide 19 - 20", "Kết luận, Định hướng mở rộng (AIOps, Kafka, Flink) & Chuyển sang phiên hỏi đáp phản biện", "1.5 phút", "Nhóm trưởng / Toàn đội phối hợp"],
    ],
    caption="Bảng 1: Kế hoạch phân bổ thời gian và phân công vai diễn thuyết minh bảo vệ",
    col_widths=[0.8, 0.9, 2.5, 0.9, 1.9]
)

add_p(doc, "Lưu ý quan trọng: Trong trường hợp giảng viên chỉ định 1 thành viên bất kỳ thuyết trình toàn bộ, thành viên đó sử dụng toàn bộ lời thoại liên tục từ Slide 1 đến Slide 20 dưới đây mà không cần chuyển lượt.", italic=True, color=C_GOLD)

# ==============================================================================
# PHẦN 2: KỊCH BẢN THUYẾT MINH CHI TIẾT TỪNG SLIDE (SLIDE 1 ĐẾN SLIDE 20)
# ==============================================================================
doc.add_page_break()
add_h1(doc, "II. KỊCH BẢN THUYẾT MINH KHẨU NGỮ CHI TIẾT (SLIDE 1 - 20)")

slides_data = [
    (
        "SLIDE 1: TRANG TIÊU ĐỀ & GIỚI THIỆU THÀNH VIÊN",
        "30 giây",
        "Tạo ấn tượng ban đầu chuyên nghiệp, giới thiệu trường, khoa, môn học và nhóm sinh viên thực hiện.",
        "Người 1 (Hoàng Ngọc Thi)",
        "Kính thưa Thầy/Cô trong Hội đồng chấm Bài tập lớn và toàn thể các bạn sinh viên! Em xin đại diện cho Nhóm 01 - Lớp ĐH13C2, Khoa Công nghệ Thông tin, Trường Đại học Tài nguyên và Môi trường Hà Nội xin được phép bắt đầu bài thuyết trình báo cáo kết quả Bài tập lớn môn Xử lý Dữ liệu lớn (Mã học phần: CTKU122). Đề tài của nhóm chúng em là: 'Xây dựng hệ thống phân tích và giám sát chất lượng mạng viễn thông (Telecom Quality of Service Analytics) trên nền tảng Hadoop, Spark và R'. Nhóm chúng em gồm có 4 thành viên: Em là Hoàng Ngọc Thi - Nhóm trưởng, cùng các bạn Nguyễn Viết Hoàng Anh, Nguyễn Việt Hòa và Nguyễn Quốc Anh. Chúng em xin trân trọng cảm ơn Thầy/Cô đã tận tình hướng dẫn nhóm trong suốt học phần vừa qua!",
        "Đứng thẳng, nét mặt tự tin, ánh mắt hướng về phía giảng viên, cúi đầu chào nhẹ trước khi mở lời.",
        "Không đọc rập khuôn mã sinh viên; giới thiệu tên rõ ràng, dứt khoát."
    ),
    (
        "SLIDE 2: ĐẶT VẤN ĐỀ & BA MỤC TIÊU KỸ THUẬT CỐT LÕI",
        "45 giây",
        "Làm rõ tính cấp thiết của đề tài và định vị 3 mục tiêu viễn thông sống còn: Latency, Packet Loss, Call Drop Rate.",
        "Người 1 (Hoàng Ngọc Thi)",
        "Kính thưa Thầy/Cô, một nhà mạng viễn thông quy mô quốc gia hiện nay quản lý trên 50.000 trạm phát sóng BTS. Mỗi giây, hàng trăm nghìn dòng dữ liệu đo kiểm telemetry phát sinh, tích lũy lên tới hàng chục Terabyte mỗi ngày. Trước khối lượng dữ liệu khổng lồ này, các cơ sở dữ liệu quan hệ truyền thống RDBMS hoàn toàn bất lực và sụp đổ, khiến nhà mạng chỉ phát hiện sự cố khi khách hàng đã phản ánh khiếu nại gay gắt. Để giải quyết triệt để bài toán này, đề tài của chúng em đặt ra 3 mục tiêu kỹ thuật cốt lõi: Thứ nhất, giảm thiểu độ trễ mạng (Latency) qua việc phát hiện trạm nghẽn truyền dẫn Backhaul; Thứ hai, giảm tỷ lệ mất gói (Packet Loss) bằng cách cô lập cell vô tuyến can nhiễu; Và thứ ba, kéo giảm tỷ lệ rớt cuộc gọi (Call Drop Rate) về dưới ngưỡng cam kết chất lượng dịch vụ SLA là 2.0%.",
        "Chỉ tay vào 3 ô mục tiêu trên slide, nhấn mạnh từ khóa 'Backhaul', 'Can nhiễu' và 'SLA 2.0%'.",
        "Phải nêu bật được SLA 2.0% vì đây là chỉ số chuẩn quốc tế của 3GPP."
    ),
    (
        "SLIDE 3: ĐẶC TRƯNG BIG DATA 5V TRONG BÀI TOÁN VIỄN THÔNG",
        "40 giây",
        "Chứng minh bài toán viễn thông thỏa mãn tuyệt đối 5 chữ V của Dữ liệu lớn và phân loại 3 dạng dữ liệu.",
        "Người 1 (Hoàng Ngọc Thi)",
        "Dữ liệu mạng viễn thông tế bào phản ánh trung thực và toàn diện 5 đặc trưng kinh điển của Big Data: Volume thể hiện ở hàng chục Terabyte log sinh ra mỗi ngày; Velocity đạt hơn 500.000 sự kiện/giây trong khung giờ cao điểm đòi hỏi phản ứng tức thời; Variety là sự pha trộn giữa dữ liệu có cấu trúc như bảng trạm BTS, bán cấu trúc như nhật ký Syslog RFC-5424, và dữ liệu luồng đo kiểm telemetry; Veracity thể hiện ở độ nhiễu cao do can nhiễu vô tuyến và lệch xung đồng hồ NTP dẫn đến các bản ghi độ trễ âm; Và cuối cùng là Value, giúp nhà mạng giảm 35% tỷ lệ rời mạng và tối ưu hóa chi phí đầu tư trạm. Chúng em phân định rõ: luồng dữ liệu thời gian thực dùng cho cảnh báo khẩn cấp, còn dữ liệu tĩnh theo lô dùng cho báo cáo SLA và huấn luyện Machine Learning.",
        "Nhấn mạnh chữ V thứ 4 - Veracity (Độ trễ âm do lỗi xung nhịp) để chứng minh hiểu sâu bản chất dữ liệu.",
        "Đây là nội dung trả lời trực tiếp Câu 1 trong đề bài."
    ),
    (
        "SLIDE 4: KIẾN TRÚC TỔNG THỂ HỆ THỐNG (LAMBDA ARCHITECTURE)",
        "45 giây",
        "Thuyết minh sơ đồ kiến trúc Lambda 5 tầng: Source -> Ingestion -> Storage -> Compute (Batch/Speed) -> Serving & BI.",
        "Người 1 (Hoàng Ngọc Thi)",
        "Để đáp ứng đồng thời cả hai yêu cầu: tính toán chính xác trên dữ liệu lịch sử và cảnh báo sự cố tức thời, hệ thống được thiết kế chuẩn mực theo Kiến trúc Lambda 5 phân tầng như trên hình 1.1: Tầng 1 thu nhận dữ liệu thô từ trạm BTS và hệ thống CRM; Tầng 2 sử dụng Apache Flume để thu nạp và đệm luồng bền vững; Tầng 3 lưu trữ tập trung trên Hadoop HDFS Data Lake với hệ số nhân bản 3 lần; Tầng 4 là tầng tính toán cốt lõi gồm 2 nhánh: Batch Layer chạy MapReduce, Pig và Spark để tính KPI dài hạn, song song với Speed Layer chạy HBase NoSQL truy xuất độ trễ dưới 10ms; Tầng 5 phục vụ người dùng qua giao diện tương tác BigSheets, môi trường RStudio và Dashboard Power BI điều hành.",
        "Chỉ vào hai nhánh rẽ Batch Layer và Speed Layer trên sơ đồ để giảng viên thấy rõ cấu trúc Lambda.",
        "Nhấn mạnh từ 'Serving Layer NoSQL' vì đây là điểm kết nối giữa dữ liệu lớn và người dùng."
    ),
    (
        "SLIDE 5: MÔ HÌNH DỮ LIỆU VIỄN THÔNG (ERD SCHEMA)",
        "35 giây",
        "Trình bày cấu trúc phân cấp hình cây chuẩn mực của mạng di động tế bào qua 4 thực thể quan hệ.",
        "Người 2 (Nguyễn Viết Hoàng Anh)",
        "Kính thưa Thầy/Cô, bước sang khâu thiết kế dữ liệu, sơ đồ thực thể quan hệ ERD được tổ chức theo cấu trúc phân cấp chuẩn của mạng tế bào vô tuyến: Một trạm vật lý bts_towers liên kết 1 - N với các sector cell phát sóng đa hướng và đa tần số trong cells_catalog; Mỗi cell này liên tục ghi nhận hàng nghìn bản ghi đo kiểm chuỗi thời gian trong network_kpi_events qua khóa ngoại tower_id và cell_id; Đồng thời, hệ thống tổng đài tự động ánh xạ các phản ánh khiếu nại của khách hàng customer_complaints về đúng cell và trạm đang phục vụ. Mô hình này đảm bảo tính toàn vẹn tham chiếu và tối ưu hóa cho các phép Join phân tán sau này.",
        "Chỉ vào mối quan hệ 1-N từ Trạm -> Cell -> Sự kiện đo kiểm.",
        "Nhấn mạnh rằng đây là cấu trúc thực tế của các nhà mạng lớn như Viettel, VNPT, MobiFone."
    ),
    (
        "SLIDE 6: TỔNG QUAN 4 TẬP DỮ LIỆU & QUY TRÌNH TIỀN XỬ LÝ LÀM SẠCH",
        "40 giây",
        "Cung cấp số liệu định lượng: 12.000 bản ghi, loại 48 bản ghi rác (0.4%), đạt độ sạch 99.6%, tạo 4 đặc trưng.",
        "Người 2 (Nguyễn Viết Hoàng Anh)",
        "Bộ dữ liệu thực nghiệm gồm 12.001 dòng đo kiểm của 20 trạm BTS và 80 sector cell tại 3 thành phố lớn: Hà Nội, Đà Nẵng và TP.HCM. Trong khâu tiền xử lý, nhóm đã xây dựng bộ lọc logic phát hiện và loại bỏ 48 bản ghi dị thường vật lý - chiếm 0.40% - gồm các lỗi trễ âm do lệch xung nhịp, thông lượng âm do tràn bộ đếm byte và mất gói vượt 100%, giữ lại 11.952 bản ghi hoàn toàn sạch đạt tỷ lệ 99.6%. Tiếp đó, chúng em thực hiện kỹ thuật Feature Engineering tạo ra 4 đặc trưng mới: Dung lượng phiên truyền tải session_volume, Tỷ lệ rớt cuộc gọi chuẩn hóa, Cờ cảnh báo quá tải vô tuyến và Điểm chất lượng dịch vụ tổng hợp QoS Score theo thang điểm 100.",
        "Chỉ vào công thức QoS Score trên slide: kết hợp có trọng số giữa Độ trễ, Mất gói và Rớt cuộc gọi.",
        "Nhắc chính xác con số: 12.000 bản ghi thô, 11.952 bản ghi sạch (loại bỏ 48 bản ghi lỗi)."
    ),
    (
        "SLIDE 7: HẠ TẦNG HDFS DATA LAKE, PHÂN VÙNG & KHẢ NĂNG CHỊU LỖI",
        "40 giây",
        "Trình bày thiết kế 4 vùng HDFS, công thức tính 13.58 TB đĩa lưu trữ cho 3 năm và cơ chế phục hồi khi DataNode chết.",
        "Người 2 (Nguyễn Viết Hoàng Anh)",
        "Trên kho lưu trữ phân tán HDFS, dữ liệu được phân định thành 4 vùng độc lập: Raw bất biến, Staging tạm thời, Curated sạch nén Snappy Parquet và Output chứa kết quả. Thư mục được phân vùng phân cấp theo năm, tháng, ngày, công nghệ mạng và mã trạm, giúp Spark loại bỏ hơn 90% dữ liệu thừa khi quét đĩa. Với mạng lưới 500 trạm thực tế sinh ra 34.5 triệu sự kiện mỗi ngày, nhóm đã tính toán chi tiết: sau khi nén Parquet và nhân bản 3 lần RF=3, hệ thống cần 10.22 GB HDFS/ngày, tương đương 13.58 Terabyte cho 3 năm hoạt động. Nếu một DataNode ngừng phản hồi quá 10 phút 30 giây, NameNode sẽ tự động phát hiện và sao chép nhân bản các block bị thiếu sang node khác để luôn bảo toàn đúng 3 bản sao chịu lỗi.",
        "Chỉ vào con số 13.58 Terabyte và công thức tính dung lượng lưu trữ.",
        "Nội dung này bảo vệ trọn vẹn điểm số của Câu 3."
    ),
    (
        "SLIDE 8: TẦNG THU THẬP LOG PHÂN TÁN VỚI APACHE FLUME",
        "40 giây",
        "Thuyết minh 2 kịch bản Flume: CSV Spooling Dir và Socket Netcat Fan-out, giải thích giao dịch 2 pha chống mất dữ liệu.",
        "Người 2 (Nguyễn Viết Hoàng Anh)",
        "Hệ thống triển khai Apache Flume với 2 kịch bản thu nạp chuyên biệt: Kịch bản 1 dùng Spooling Directory Source nạp lô tệp CSV định kỳ, qua FileChannel bền bỉ ghi xuống HDFS Sink với kích thước cắt file đúng 128 MB khớp với kích thước block HDFS; Kịch bản 2 tiếp nhận luồng sự kiện nóng qua cổng Netcat 8888, áp dụng cơ chế Fan-out nhân đôi luồng: một luồng đi qua MemoryChannel nạp nhanh vào HDFS, luồng còn lại qua FileChannel nạp vào HBase NoSQL. Flume vận hành theo cơ chế giao dịch 2 pha: sự kiện chỉ được xóa khỏi Channel khi Sink đã nhận được tín hiệu ACK ghi thành công xuống đĩa, bảo đảm dữ liệu đo kiểm không bao giờ bị thất lạc ngay cả khi mất điện đột ngột.",
        "Chỉ vào 2 luồng Fan-out trên sơ đồ kiến trúc Flume.",
        "Khẳng định rõ: Spooling Dir cắt tệp đúng 128 MB để tránh vấn đề tệp nhỏ (Small Files Problem) trên HDFS."
    ),
    (
        "SLIDE 9: THUẬT TOÁN HADOOP MAPREDUCE TỐI ƯU HÓA (JAVA)",
        "45 giây",
        "Trình bày chiều sâu kỹ thuật MapReduce: Khóa phức hợp, Custom Partitioner triệt tiêu Data Skew và Combiner giảm 80% I/O mạng.",
        "Người 3 (Nguyễn Việt Hòa)",
        "Kính thưa Thầy/Cô, trong chương trình MapReduce thuần Java TelecomKpiAnalysis, nhóm đã áp dụng 3 kỹ thuật tối ưu hóa then chốt: Thứ nhất, thiết kế Khóa phức hợp TowerTechKey gói gọn cả mã trạm và công nghệ mạng, hiện thực interface WritableComparable để sắp xếp tự nhiên; Thứ hai, xây dựng Custom Partitioner chỉ băm theo trường tower_id duy nhất, đảm bảo toàn bộ dữ liệu 3G, 4G, 5G của cùng một trạm BTS đều tập trung về đúng một Reducer, triệt tiêu hoàn toàn hiện tượng lệch dữ liệu Data Skew; Thứ ba, tích hợp Combiner chạy ngay tại DataNode để cộng dồn sơ bộ các chỉ số đo kiểm, giúp cắt giảm hơn 80% lưu lượng truyền tải trên mạng trong pha Shuffle & Sort. Kết quả xuất ra đúng định dạng phân tách tab lưu trên HDFS.",
        "Chỉ vào sơ đồ dòng chảy dữ liệu từ Map -> Combiner -> Partitioner -> Shuffle -> Reduce.",
        "Đây là phần chứng minh trình độ lập trình phân tán Java, trả lời Câu 5."
    ),
    (
        "SLIDE 10: XỬ LÝ VÀ PHÂN CỤM DỮ LIỆU BẰNG APACHE PIG LATIN",
        "35 giây",
        "Trình bày kịch bản khai báo luồng dữ liệu Pig Latin và trích xuất danh sách trạm suy thoái.",
        "Người 3 (Nguyễn Việt Hòa)",
        "Bên cạnh MapReduce Java, nhóm phát triển kịch bản Pig Latin telecom_kpi_analysis.pig để rút ngắn thời gian phát triển ETL. Kịch bản thực hiện chuỗi toán tử hoàn chỉnh: LOAD dữ liệu với schema tường minh; FILTER loại bỏ các bản ghi âm; JOIN dữ liệu đo kiểm với bảng danh mục trạm; GROUP theo bộ ba mã trạm, công nghệ và tỉnh thành; sau đó dùng FOREACH kết hợp 4 hàm tính toán COUNT, AVG độ trễ, AVG mất gói và SUM rớt cuộc gọi để tính tỷ lệ rớt mạng; cuối cùng dùng lệnh SPLIT lọc ra danh sách các trạm có tỷ lệ rớt mạng vượt ngưỡng SLA 2.0% và dùng STORE kết xuất trực tiếp vào thư mục HDFS.",
        "Nhấn mạnh cú pháp Pig Latin ngắn gọn chỉ 25 dòng nhưng sinh ra DAG MapReduce mạnh mẽ.",
        "Nội dung trả lời trực tiếp Câu 4."
    ),
    (
        "SLIDE 11: ĐỘNG CƠ TÍNH TOÁN PHÂN TÁN IN-MEMORY APACHE SPARK",
        "45 giây",
        "Thuyết minh Pipeline PySpark, giải thích việc dùng persist(MEMORY_AND_DISK), Catalyst Optimizer và tốc độ 2.3s.",
        "Người 3 (Nguyễn Việt Hòa)",
        "Đóng vai trò là trái tim tính toán của hệ thống, pipeline PySpark telecom_spark_pipeline.py tận dụng tối đa kiến trúc In-Memory để bứt phá hiệu năng. Chương trình thực thi 7 phép biến đổi Transformations và 4 hành động Actions. Đặc biệt, nhóm áp dụng kỹ thuật persist với cấp độ MEMORY_AND_DISK ngay sau phép Join 4 bảng, vì DataFrame này được tái sử dụng 3 lần liên tiếp cho Spark SQL, tổng hợp KPI và lọc cell quá tải. Nhờ trình tối ưu hóa Catalyst Optimizer và động cơ sinh mã nhị phân Tungsten, Spark thực thi toàn bộ luồng xử lý chỉ trong 2.3 giây, nhanh gấp 15.4 lần so với MapReduce truyền thống mất 35.4 giây. Dữ liệu sạch sau đó được ghi dưới định dạng Snappy Parquet phục vụ phân tích chuyên sâu.",
        "Nhấn mạnh con số ấn tượng: Spark chạy 2.3 giây vs MapReduce 35.4 giây (nhanh gấp 15.4 lần).",
        "Nội dung trả lời trực tiếp Câu 6."
    ),
    (
        "SLIDE 12: CƠ SỞ DỮ LIỆU NOSQL APACHE HBASE ĐỘ TRỄ THẤP (< 10MS)",
        "40 giây",
        "Giải thích RowKey đảo chuỗi chống Write Hotspotting, 3 Column Families và lệnh thao tác Shell.",
        "Người 3 (Nguyễn Việt Hòa)",
        "Để đáp ứng nhu cầu tra cứu thông tin trạm phát sóng tức thời dưới 10 mili-giây cho các kỹ sư trực ban NOC, nhóm đã thiết kế CSDL NoSQL Apache HBase với cấu trúc RowKey tối ưu: đảo chuỗi mã trạm kết hợp công nghệ mạng và dấu thời gian đảo ngược reverse_timestamp. Kỹ thuật đảo mã trạm giúp các trạm liên tiếp phân tán đều sang các RegionServer khác nhau, triệt tiêu hoàn toàn điểm nghẽn thắt cổ chai ghi tập trung Write Hotspotting; trong khi đảo thời gian giúp phiên đo kiểm mới nhất luôn nằm ở đầu bảng. Bảng telecom_kpi gồm 3 Column Families: cf_kpi lưu chỉ số đo kiểm có TTL 90 ngày, cf_cell lưu cấu hình vô tuyến và cf_alert lưu cờ cảnh báo sự cố, tích hợp Pre-splitting 4 phân vùng và nén Snappy.",
        "Chỉ vào cấu trúc RowKey: reverse(tower_id) + technology + reverse_timestamp.",
        "Nội dung trả lời trực tiếp Câu 7."
    ),
    (
        "SLIDE 13: MÔ PHỎNG QUY TRÌNH PHÂN TÍCH VỚI IBM BIGSHEETS",
        "40 giây",
        "Giới thiệu Web App mô phỏng BigSheets 6 bước ánh xạ 1-1 với Spark DataFrame cho người dùng không lập trình.",
        "Người 3 (Nguyễn Việt Hòa)",
        "Đối với đối tượng chuyên viên kinh doanh và quản lý mạng không có kỹ năng lập trình, giải pháp phân tích bảng tính No-Code của IBM BigSheets là vô cùng lý tưởng. Nhóm đã xây dựng một ứng dụng Web tương tác mô phỏng toàn diện quy trình BigSheets 6 bước và ánh xạ tương đương 1-1 với Spark DataFrame: Bước 1 Collection nạp CSV tương đương read.csv; Bước 2 Data Cleansing lọc bản ghi lỗi tương đương filter; Bước 3 Calculated Column tính dung lượng phiên tương đương withColumn; Bước 4 Dimension Join tương đương hàm join; Bước 5 Pivot Sheet tổng hợp KPI tương đương groupBy; Và Bước 6 xuất Dashboard trực quan đa chiều với các bộ lọc tương tác một chạm.",
        "Nhấn mạnh tính ứng dụng thực tế: người dùng nghiệp vụ chỉ cần kéo thả chuột như Excel trên Big Data.",
        "Nội dung trả lời trực tiếp Câu 8."
    ),
    (
        "SLIDE 14: KHOA HỌC DỮ LIỆU & HỌC MÁY BẰNG R VÀ CSDL SQLITE",
        "45 giây",
        "Trình bày mô hình Hồi quy Logistic bằng R dự báo khiếu nại khách hàng với p < 0.001 và xác suất khiếu nại 82%.",
        "Người 4 (Nguyễn Quốc Anh)",
        "Kính thưa Thầy/Cô, ở tầng Khoa học dữ liệu chuyên sâu, kịch bản R telecom_analysis.R kết nối với cơ sở dữ liệu SQLite qua thư viện DBI và RSQLite, thực thi truy vấn SQL có Join 4 bảng và Group By, sau đó dùng dplyr tổng hợp số liệu. Đóng góp nổi bật của nhóm là đã huấn luyện thành công mô hình Học máy Hồi quy Logistic (Logistic Regression) để dự báo xác suất phát sinh khiếu nại của khách hàng. Kết quả kiểm định thống kê cho thấy hệ số hồi quy của Độ trễ (beta=0.042) và Tỷ lệ mất gói (beta=0.385) đều đạt mức ý nghĩa vượt trội với p < 0.001. Mô hình chỉ ra rằng: khi một trạm có độ trễ vượt 120ms và mất gói trên 5%, xác suất khách hàng khiếu nại tăng vọt lên mức 82%. Toàn bộ kết quả dự báo được ghi ngược lại bảng kpi_analysis_summary trong CSDL SQLite.",
        "Chỉ vào phương trình hồi quy Logistic và giá trị p-value < 0.001.",
        "Nội dung bảo vệ điểm Câu 9."
    ),
    (
        "SLIDE 15: KẾT QUẢ THỰC NGHIỆM ĐỊNH LƯỢNG & TOP 10 TRẠM SỰ CỐ",
        "40 giây",
        "Công bố số liệu toàn mạng và cô lập chính xác Top 3 trạm phát sóng suy thoái nghiêm trọng: TOWER_003, 008, 015.",
        "Người 4 (Nguyễn Quốc Anh)",
        "Qua quá trình tính toán và đối soát dữ liệu trên 12.000 phiên đo kiểm, hệ thống ghi nhận các chỉ số bình quân toàn mạng: Độ trễ trung bình đạt 46.8 ms và Tỷ lệ rớt cuộc gọi đạt 1.85% - hoàn thành cam kết chất lượng dịch vụ SLA dưới 2.0%. Tuy nhiên, khi đi sâu vào xếp hạng từng trạm, hệ thống đã cô lập chính xác 3 trạm phát sóng gặp sự cố nghiêm trọng nhất: trạm TOWER_003 tại Hà Nội, TOWER_008 tại TP.HCM và TOWER_015 tại Đà Nẵng. Cả 3 trạm này đều có tỷ lệ rớt mạng trên 7.5% và độ trễ vọt lên trên 180 ms trên toàn bộ các dải tần 3G, 4G và 5G, khẳng định nguyên nhân cốt lõi không phải do vô tuyến mà do nghẽn đường truyền truyền dẫn Backhaul nối về mạng lõi.",
        "Chỉ vào 3 dòng đầu bảng KPI trên slide, nhấn mạnh tỷ lệ rớt mạng vọt lên 11.81% và trễ 181 ms.",
        "Đây là phát hiện nghiệp vụ đắt giá nhất của đề tài."
    ),
    (
        "SLIDE 16: TRỰC QUAN HÓA CHẤT LƯỢNG MẠNG & BIỂU ĐỒ BONG BÓNG",
        "35 giây",
        "Phân tích 5 biểu đồ trực quan: Boxplot công nghệ, Scatter plot tương quan mất gói vs rớt mạng, Bubble plot đa chiều.",
        "Người 4 (Nguyễn Quốc Anh)",
        "Kết quả phân tích được trực quan hóa sinh động qua chuỗi biểu đồ khoa học: Biểu đồ hộp Boxplot khẳng định mạng 5G có độ trễ trung bình siêu thấp chỉ 12.4 ms so với 3G là 78.5 ms; Đồ thị tương quan chỉ ra mối quan hệ đồng biến chặt chẽ giữa tỷ lệ mất gói và rớt cuộc gọi; Và đặc biệt là Biểu đồ bong bóng đa chiều tương quan giữa Độ trễ, Mất gói và Kích thước bong bóng là số thuê bao. 3 cụm bong bóng màu đỏ nằm tách biệt ở góc trên bên phải chính là 3 trạm suy thoái TOWER_003, 008 và 015, cung cấp cái nhìn trực quan tức thời cho các kỹ sư điều hành mạng NOC.",
        "Chỉ vào 3 quả bong bóng màu đỏ nổi bật ở góc trên bên phải biểu đồ.",
        "Chứng minh năng lực trực quan hóa dữ liệu lớn chuyên nghiệp."
    ),
    (
        "SLIDE 17: BẢNG ĐỐI CHIẾU HIỆU NĂNG CÔNG NGHỆ (PIG - MR - SPARK - R)",
        "40 giây",
        "So sánh định lượng 4 công nghệ theo thời gian chạy, I/O đĩa, RAM và độ phức tạp mã nguồn.",
        "Người 4 (Nguyễn Quốc Anh)",
        "Bảng 4.2 trên slide tổng hợp kết quả đối chiếu định lượng giữa 4 công nghệ trên cùng tập dữ liệu: Apache Spark bộc lộ sức mạnh vượt trội với thời gian thực thi chỉ 2.3 giây nhờ kiến trúc tính toán trên bộ nhớ RAM và trình tối ưu Catalyst; Pig Latin chạy mất 18.0 giây với cú pháp cực kỳ ngắn gọn phù hợp làm ETL trên Data Lake; Hadoop MapReduce mất 35.4 giây do chi phí ghi đĩa trung gian và đọc lại ở pha Shuffle, nhưng vẫn là giải pháp ổn định nhất cho các tác vụ xử lý lô cực lớn chạy qua đêm; Trong khi đó, ngôn ngữ R xử lý trong 1.8 giây, đảm nhận xuất sắc vai trò phân tích thống kê và huấn luyện mô hình học máy.",
        "Chỉ vào hàng 'Thời gian chạy' (2.3s vs 18s vs 35.4s vs 1.8s).",
        "Nội dung trực tiếp trả lời yêu cầu đối chiếu của Câu 10."
    ),
    (
        "SLIDE 18: MA TRẬN NĂM KHUYẾN NGHỊ HÀNH ĐỘNG CHO TRUNG TÂM ĐIỀU HÀNH NOC",
        "45 giây",
        "Đề xuất 5 giải pháp kỹ thuật có căn cứ dữ liệu định lượng: Can thiệp P1, Sunset 3G, Bật SON, Chăm sóc chủ động, Tối ưu Parquet.",
        "Người 4 (Nguyễn Quốc Anh)",
        "Căn cứ trên các bằng chứng dữ liệu định lượng, nhóm trân trọng đề xuất Ma trận 5 khuyến nghị kỹ thuật hành động gửi Trung tâm Điều hành Mạng NOC: Khuyến nghị 1 (Ưu tiên P1 - trong 48h): Điều động xe phát sóng lưu động COW và nâng cấp đường truyền Backhaul từ 100 Mbps lên 1 Gbps cho 3 trạm TOWER_003, 008 và 015 để kéo rớt mạng về dưới 2%; Khuyến nghị 2 (P2 - trong 6 tháng): Tắt sóng 3G và tái quy hoạch băng tần 2100 MHz sang cho 4G/5G nhằm tăng 40% dung lượng mạng; Khuyến nghị 3 (P3 - trong 2 tuần): Kích hoạt tính năng Mạng tự tối ưu SON để tự động san tải thuê bao giữa các cell lân cận; Khuyến nghị 4 (P4 - trong 1 tháng): Tích hợp mô hình Logistic R vào CRM để chủ động gửi tin nhắn xin lỗi kèm voucher data cho thuê bao gặp sự cố, giảm 35% tỷ lệ rời mạng; Khuyến nghị 5 (P5): Quy chuẩn hóa lưu trữ Snappy Parquet và đặt TTL 90 ngày trên HBase, giúp tiết kiệm 60% chi phí mở rộng ổ cứng.",
        "Nhấn mạnh lần lượt từng mức độ ưu tiên từ P1 đến P5.",
        "Khẳng định giải pháp có tính thực tiễn cao chứ không chỉ là lý thuyết trên giấy."
    ),
    (
        "SLIDE 19: KẾT LUẬN CÁC KẾT QUẢ ĐẠT ĐƯỢC & HƯỚNG PHÁT TRIỂN",
        "30 giây",
        "Tổng kết thành công của đề tài, nêu thẳng thắn hạn chế và vạch ra lộ trình mở rộng AIOps, Kafka, Flink.",
        "Người 1 (Hoàng Ngọc Thi)",
        "Tổng kết lại, đề tài đã hoàn thành xuất sắc 100% mục tiêu: làm chủ trọn vẹn hệ sinh thái Big Data đa nền tảng, tối ưu hóa thuật toán MapReduce, xây dựng pipeline Spark In-Memory tốc độ cao và ứng dụng mô hình học máy giải quyết triệt để 3 bài toán chỉ số viễn thông. Về hạn chế, hệ thống hiện thực nghiệm trên cụm giả lập máy đơn và mô hình dừng ở hồi quy tuyến tính. Hướng phát triển tiếp theo của nhóm là triển khai hàng đợi thông điệp Apache Kafka kết hợp Apache Flink để đạt độ trễ xử lý luồng dưới 50 mili-giây, và ứng dụng mạng nơ-ron học sâu LSTM để dự báo đứt gãy truyền dẫn trước 30 đến 60 phút.",
        "Chốt lại đầy tự tin, thể hiện tinh thần nghiên cứu khoa học nghiêm túc và cầu thị.",
        "Nêu hạn chế một cách trung thực là điểm cộng lớn trong mắt giảng viên."
    ),
    (
        "SLIDE 20: KẾT THÚC BÁO CÁO & SẴN SÀNG CHO PHIÊN PHẢN BIỆN (Q&A)",
        "20 giây",
        "Lời cảm ơn trang trọng và mời Thầy/Cô đặt câu hỏi phản biện.",
        "Người 1 (Hoàng Ngọc Thi)",
        "Bài thuyết trình báo cáo kết quả Bài tập lớn của Nhóm 01 đến đây xin được phép kết thúc. Chúng em xin chân thành cảm ơn sự chú ý lắng nghe và theo dõi của Quý Thầy/Cô và các bạn! Nhóm chúng em rất mong nhận được những ý kiến nhận xét quý báu, đóng góp chuyên môn và các câu hỏi phản biện từ Thầy/Cô để đề tài được hoàn thiện sâu sắc hơn nữa. Chúng em xin trân trọng cảm ơn!",
        "Cả nhóm cùng đứng nghiêm túc, cúi đầu cảm ơn Hội đồng, sẵn sàng chuyển sang phần demo hoặc hỏi đáp.",
        "Nụ cười tự tin, giữ phong thái bình tĩnh, cởi mở."
    )
]

for s_title, s_time, s_goal, s_spk, s_text, s_action, s_note in slides_data:
    add_h2(doc, f"{s_title} ({s_time})")
    add_p(doc, f"Mục tiêu truyền tải: {s_goal}", bold_prefix="🎯 ", color=C_DARK_SLATE)
    add_speech(doc, s_spk, s_text)
    add_callout(doc, "Hành động & Cử chỉ", s_action, bg_color="F0FDF4", border_title_color=C_EMERALD)
    add_callout(doc, "Mẹo ăn điểm & Lưu ý", s_note, bg_color="FFFBEB", border_title_color=C_GOLD)

# ==============================================================================
# PHẦN 3: KỊCH BẢN DEMO SẢN PHẨM TRỰC QUAN (LIVE DEMO 2 PHÚT "ĂN ĐIỂM")
# ==============================================================================
doc.add_page_break()
add_h1(doc, "III. KỊCH BẢN LIVE DEMO SẢN PHẨM THỰC TẾ (2 PHÚT ĂN ĐIỂM)")

add_p(doc, "Nếu Hội đồng yêu cầu: 'Các em hãy mở sản phẩm thực tế chạy demo cho Thầy/Cô xem', nhóm hãy thực hiện ngay quy trình 3 bước một chạm cực kỳ ấn tượng sau:")

add_h2(doc, "Bước 1: Demo Giao diện Web Dashboard BigSheets (Câu 8 - 45 giây)")
add_bullet(doc, "Thao tác: Vào thư mục gốc c:\\dulieulon, nhấp đúp chuột vào tệp start_bigsheets.bat (hoặc mở trực tiếp report/bigsheets_dashboard.html trên trình duyệt).", bold_prefix="1. ")
add_bullet(doc, "Lời thoại nói với giảng viên: 'Dạ thưa Thầy/Cô, đây là giao diện Web Dashboard mô phỏng chuẩn 6 bước phân tích của IBM BigSheets kết nối dữ liệu Spark DataFrame. Chuyên viên NOC chỉ cần chọn bộ lọc Tỉnh thành (ví dụ Hà Nội) và Công nghệ mạng (4G), hệ thống sẽ lập tức lọc động và hiển thị danh sách cảnh báo Top trạm suy thoái cùng các biểu đồ trực quan mà không cần viết bất kỳ dòng mã nào.'", bold_prefix="2. ")

add_h2(doc, "Bước 2: Demo Bảng CSDL SQLite & Kết quả Học máy R (Câu 9 - 45 giây)")
add_bullet(doc, "Thao tác: Nhấp đúp chuột vào tệp view_kpi_analysis_summary.bat (hoặc mở report/kpi_analysis_summary.html hoặc file CSV trong data/).", bold_prefix="1. ")
add_bullet(doc, "Lời thoại nói với giảng viên: 'Dạ thưa Thầy/Cô, đây là bảng kpi_analysis_summary gồm 60 dòng và 18 cột được kịch bản R huấn luyện và ghi ngược vào SQLite. Thầy/Cô có thể thấy cột predicted_complaint_prob và nhãn HIGH_RISK màu đỏ cảnh báo chính xác các trạm TOWER_003, TOWER_008 và TOWER_015 có xác suất khách hàng khiếu nại vọt lên 82% do độ trễ vượt 180ms.'", bold_prefix="2. ")

add_h2(doc, "Bước 3: Mở Source Code minh chứng (Nếu được hỏi vào mã nguồn - 30 giây)")
add_bullet(doc, "Mở mã nguồn MapReduce Java tại: mapreduce/TelecomKpiAnalysis.java (Chỉ vào lớp TowerTechKey, TowerPartitioner và KpiCombiner).", bold_prefix="• ")
add_bullet(doc, "Mở kịch bản Pig Latin tại: pig/telecom_kpi_analysis.pig (Chỉ vào các toán tử LOAD, FILTER, JOIN, GROUP, FOREACH).", bold_prefix="• ")
add_bullet(doc, "Mở pipeline Spark tại: spark/telecom_spark_pipeline.py (Chỉ vào hàm persist và các lệnh Spark SQL).", bold_prefix="• ")

# ==============================================================================
# PHẦN 4: KỊCH BẢN TRẢ LỜI PHẢN BIỆN (Q&A DEFENSE GUIDE - TOP 10 CÂU HỎI)
# ==============================================================================
doc.add_page_break()
add_h1(doc, "IV. BỘ CÂU HỎI PHẢN BIỆN BẢO VỆ VÀ ĐÁP ÁN ĐẠT ĐIỂM TỐI ĐA (TOP 10 CÂU)")

qa_list = [
    (
        "Câu hỏi 1: Tại sao trong dữ liệu viễn thông lại xuất hiện độ trễ âm và thông lượng âm? Các em xử lý như thế nào?",
        "Dạ thưa Thầy/Cô, độ trễ âm (ví dụ -15.4 ms) xuất hiện trong thực tế do hiện tượng lệch xung nhịp đồng hồ mạng NTP (Network Time Protocol) giữa trạm BTS và máy chủ đo kiểm trung tâm; còn thông lượng âm sinh ra do lỗi tràn số nguyên (Counter Overflow) tại firmware của thiết bị định tuyến cũ. Nhóm đã xây dựng bộ lọc logic tự động loại bỏ 48 bản ghi dị thường này (chiếm 0.40%) và gắn cờ quality_flag=0 để cách ly xử lý, đảm bảo tập dữ liệu đưa vào tính toán đạt độ sạch tuyệt đối 99.6%."
    ),
    (
        "Câu hỏi 2: Tại sao trong Apache Flume các em dùng cả MemoryChannel và FileChannel mà không dùng 1 loại?",
        "Dạ thưa Thầy/Cô, đây là chiến lược cân đối giữa tốc độ và độ an toàn: MemoryChannel lưu trên RAM có thông lượng xử lý cực cao (hàng trăm nghìn sự kiện/giây), rất phù hợp để nạp nhanh luồng log vào HDFS; tuy nhiên MemoryChannel có tính chất bốc hơi (volatile), nếu sập nguồn sẽ mất dữ liệu. Vì vậy với nhánh ghi vào HBase NoSQL phục vụ giám sát trọng yếu, nhóm sử dụng FileChannel bền vững ghi xuống Write-Ahead Log trên đĩa, kết hợp cơ chế giao dịch 2 pha (Two-Phase Commit) bảo đảm dữ liệu không bao giờ bị thất lạc."
    ),
    (
        "Câu hỏi 3: Hệ số nhân bản HDFS RF=3 có lãng phí đĩa không? Cơ chế phục hồi khi 1 DataNode bị hỏng diễn ra thế nào?",
        "Dạ thưa Thầy/Cô, RF=3 là chuẩn công nghiệp vàng của Hadoop: 2 bản sao lưu trên cùng một rack (cùng tủ mạng) để đọc nhanh nội bộ, và 1 bản sao lưu ở rack khác (khác tủ mạng) để phòng chống cháy nổ hoặc đứt nguồn toàn bộ một rack mạng. Nhờ nén Snappy Parquet tiết kiệm 65% đĩa, dung lượng 3 năm của 500 trạm chỉ tốn 13.58 TB, hoàn toàn kinh tế. Khi 1 DataNode chết sau 10 phút 30 giây không gửi Heartbeat, NameNode tự động quét danh mục block bị thiếu và ra lệnh cho các DataNode lành nhân bản sang node khác để luôn duy trì đủ 3 bản sao."
    ),
    (
        "Câu hỏi 4: Apache Pig khác gì so với Hadoop MapReduce thuần Java?",
        "Dạ thưa Thầy/Cô, Pig Latin là ngôn ngữ luồng dữ liệu khai báo bậc cao. Thay vì phải viết hơn 300 dòng mã Java phức tạp với Mapper, Reducer, Writable, lập trình viên chỉ cần viết khoảng 25 dòng lệnh Pig (LOAD, FILTER, GROUP, FOREACH). Trình biên dịch Pig sẽ tự động dịch các câu lệnh này thành một đồ thị có hướng DAG gồm chuỗi các MapReduce jobs tối ưu ngầm định, giúp rút ngắn thời gian phát triển ETL tới 70%."
    ),
    (
        "Câu hỏi 5: Trong thuật toán MapReduce, Custom Partitioner và Combiner của nhóm giải quyết bài toán gì?",
        "Dạ thưa Thầy/Cô, Custom Partitioner của nhóm chỉ băm theo mã trạm tower_id duy nhất, đảm bảo toàn bộ dữ liệu 3G, 4G, 5G của cùng một trạm BTS đều tập trung về đúng 1 Reducer, triệt tiêu hoàn toàn hiện tượng lệch dữ liệu (Data Skew) khiến 1 Reducer bị quá tải còn các Reducer khác ngồi chơi; Còn Combiner đóng vai trò như một Mini-Reducer chạy cục bộ trên DataNode sau pha Map để cộng dồn sơ bộ các chỉ số đo kiểm, giúp cắt giảm hơn 80% lưu lượng truyền tải trên mạng trong pha Shuffle & Sort."
    ),
    (
        "Câu hỏi 6: Tại sao Apache Spark lại chạy nhanh gấp 15 lần MapReduce (2.3s so với 35.4s)? Khi nào dùng persist?",
        "Dạ thưa Thầy/Cô, Spark nhanh hơn vượt trội nhờ 3 yếu tố: Thứ nhất là tính toán In-Memory trong bộ nhớ RAM, không phải ghi đĩa trung gian sau mỗi giai đoạn như MapReduce; Thứ hai là trình tối ưu Catalyst Optimizer tự động sắp xếp lại thứ tự các phép lọc trước khi Join (Predicate Pushdown); Thứ ba là động cơ Tungsten sinh mã bytecode nhị phân trực tiếp. Nhóm sử dụng persist(MEMORY_AND_DISK) ngay sau phép Join 4 bảng vì DataFrame này được tái sử dụng liên tiếp 3 lần cho Spark SQL, tổng hợp KPI và lọc cell quá tải, tránh việc Spark phải tính toán lại đồ thị DAG từ đầu."
    ),
    (
        "Câu hỏi 7: Cấu trúc RowKey trong Apache HBase của các em tại sao phải đảo chuỗi mã trạm?",
        "Dạ thưa Thầy/Cô, nếu đặt mã trạm bình thường (TOWER_001, TOWER_002...) thì các trạm cùng tiền tố sẽ bị lưu tập trung trên đúng 1 RegionServer duy nhất, gây ra hiện tượng thắt cổ chai ghi tập trung (Write Hotspotting). Việc đảo chuỗi mã trạm (100_REWOT, 200_REWOT...) kết hợp Pre-splitting 4 vùng giúp lưu lượng ghi phân tán đều khắp các node trên cụm; đồng thời việc đảo dấu thời gian reverse_timestamp giúp các phiên đo kiểm MỚI NHẤT luôn nằm ở đầu bảng, lệnh Scan chỉ cần quét phạm vi ngắn O(1) là lấy được dữ liệu thời gian thực."
    ),
    (
        "Câu hỏi 8: BigSheets có ưu điểm gì so với việc viết code Spark thông thường?",
        "Dạ thưa Thầy/Cô, BigSheets cung cấp giao diện bảng tính trực quan No-Code thân thiện như Microsoft Excel. Người dùng nghiệp vụ, chuyên viên kinh doanh và ban giám đốc có thể tự tay lọc dữ liệu, tạo cột tính toán, Join bảng danh mục và xem Dashboard mà không cần phải biết lập trình Python hay Java. Phía sau giao diện đó, hệ thống tự động biên dịch các thao tác bảng tính thành các tác vụ tính toán phân tán Spark DataFrame trên cụm Big Data."
    ),
    (
        "Câu hỏi 9: Mô hình Hồi quy Logistic trong R đem lại giá trị kinh tế gì cho nhà mạng viễn thông?",
        "Dạ thưa Thầy/Cô, mô hình lượng hóa chính xác mối quan hệ giữa các chỉ số mạng và hành vi khách hàng: khi độ trễ vượt 120ms và mất gói trên 5%, xác suất khách hàng khiếu nại tăng vọt lên mức 82% với độ tin cậy p < 0.001. Thay vì đợi khách hàng gọi điện phàn nàn mới xử lý, nhà mạng sử dụng mô hình này để chuyển sang chế độ chăm sóc khách hàng chủ động: tự động gửi tin nhắn SMS xin lỗi kèm voucher data ưu đãi cho các thuê bao bị ảnh hưởng ngay trong ngày, giúp kéo giảm 35% tỷ lệ thuê bao rời mạng (Churn Rate)."
    ),
    (
        "Câu hỏi 10: Căn cứ vào đâu mà nhóm đưa ra kết luận 3 trạm TOWER_003, 008 và 015 bị nghẽn đường truyền Backhaul?",
        "Dạ thưa Thầy/Cô, bằng chứng dữ liệu thực nghiệm chỉ ra rằng: cả 3 trạm này đều bị suy giảm chất lượng đồng thời trên toàn bộ các công nghệ mạng (3G, 4G và cả 5G), với tỷ lệ rớt cuộc gọi đều vọt lên trên 7.5% và độ trễ trên 180 ms. Nếu nguyên nhân là do vô tuyến (như anten lệch hướng hay can nhiễu tần số) thì thông thường chỉ bị ảnh hưởng trên một dải tần hoặc một sector cell cụ thể; nhưng việc toàn bộ các dải tần của cả trạm đều nghẽn chứng minh chắc chắn điểm nghẽn nằm ở đường truyền cáp quang Backhaul nối từ trạm BTS về mạng lõi."
    ),
]

for idx, (q, a) in enumerate(qa_list, 1):
    add_h2(doc, f"Câu hỏi {idx}: {q}")
    add_callout(doc, f"Đáp án sắc bén ăn điểm 10", a, bg_color="F8FAFC", border_title_color=C_BLUE)

# ==============================================================================
# PHẦN 5: CHECKLIST CHUẨN BỊ TRƯỚC GIỜ G
# ==============================================================================
doc.add_page_break()
add_h1(doc, "V. CHECKLIST CHUẨN BỊ TRƯỚC GIỜ BẢO VỆ")

checklist = [
    ("Tệp trình chiếu Slide.pptx", "Đã chép vào USB và lưu sẵn trên Desktop máy tính thuyết trình, kiểm tra hiển thị tỉ lệ 16:9 Widescreen không bị méo hình."),
    ("Tệp Báo cáo Word & PDF", "File BaoCao 2_updated.docx và BaoCao 2.pdf đã in đóng quyển gáy xoắn và mở sẵn trên máy tính để tra cứu mục lục khi cần."),
    ("Kiểm tra chạy thử file Batch Demo", "Nhấp đúp thử tệp start_bigsheets.bat và view_kpi_analysis_summary.bat trên máy trạm để đảm bảo trình duyệt mở mượt mà."),
    ("Phân công bấm Slide và cầm Mic", "Người thuyết trình đứng thẳng, tay cầm mic và chuột bay / bút bấm slide (nếu có), ánh mắt tự tin bao quát toàn bộ Hội đồng."),
    ("Tâm thế trả lời câu hỏi phản biện", "Lắng nghe hết câu hỏi của Thầy/Cô, ghi chép nhanh từ khóa ra giấy nháp, mỉm cười và bắt đầu bằng: 'Dạ, em xin cảm ơn câu hỏi rất hay của Thầy/Cô...', sau đó trả lời dứt khoát đúng trọng tâm theo kịch bản ở Phần IV."),
]

add_tbl(
    doc,
    headers=["Hạng mục kiểm tra", "Nội dung chuẩn bị chi tiết"],
    data=checklist,
    caption="Bảng 2: Danh mục công tác chuẩn bị trước giờ bước vào phòng bảo vệ",
    col_widths=[2.5, 4.5]
)

p_end = doc.add_paragraph()
p_end.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_end.paragraph_format.space_before = Pt(16)
r_end = p_end.add_run("🌟 CHÚC NHÓM 01 BẢO VỆ TỰ TIN, THÀNH CÔNG RỰC RỠ VÀ ĐẠT ĐIỂM SỐ 10/10 TUYỆT ĐỐI! 🌟")
r_end.font.name = "Times New Roman"
r_end.font.size = Pt(13)
r_end.font.bold = True
r_end.font.color.rgb = C_EMERALD

# Lưu tài liệu
doc.save(output_path)
print(f"SUCCESS: Đã tạo thành công tệp Word: {output_path}")
