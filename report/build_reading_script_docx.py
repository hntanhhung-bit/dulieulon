# -*- coding: utf-8 -*-
"""
CHƯƠNG TRÌNH TẠO FILE WORD: KỊCH BẢN ĐỌC THUYẾT MINH BẢO VỆ BÀI TẬP LỚN
MÔN: XỬ LÝ DỮ LIỆU LỚN - ĐỀ TÀI: TELECOM BIG DATA (HADOOP, SPARK, R)
Tài liệu tối ưu hóa 100% để cầm tay đọc liền mạch trước Hội đồng chấm thi.
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

output_path = r"c:\dulieulon\Kich_Ban_Doc_Thuyet_Trinh.docx"

doc = docx.Document()

# Căn lề chuẩn văn bản: Trái 3cm, Phải 2cm, Trên 2cm, Dưới 2cm
for section in doc.sections:
    section.top_margin = Inches(2.0 / 2.54)
    section.bottom_margin = Inches(2.0 / 2.54)
    section.left_margin = Inches(3.0 / 2.54)
    section.right_margin = Inches(2.0 / 2.54)

# Bảng màu chuyên nghiệp
C_NAVY = RGBColor(0x0F, 0x17, 0x2A)
C_BLUE = RGBColor(0x1E, 0x3A, 0x8A)
C_DARK_SLATE = RGBColor(0x1E, 0x29, 0x3B)
C_TEXT = RGBColor(0x1E, 0x29, 0x3B)
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
    p.paragraph_format.line_spacing = 1.25
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

# ==============================================================================
# TRANG TIÊU ĐỀ
# ==============================================================================
p_top = doc.add_paragraph()
p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
r1 = p_top.add_run("BỘ TÀI NGUYÊN VÀ MÔI TRƯỜNG\nTRƯỜNG ĐẠI HỌC TÀI NGUYÊN VÀ MÔI TRƯỜNG HÀ NỘI\nKHOA CÔNG NGHỆ THÔNG TIN • HỌC PHẦN: XỬ LÝ DỮ LIỆU LỚN\n")
r1.font.name = "Times New Roman"
r1.font.size = Pt(12)
r1.font.bold = True
r1.font.color.rgb = C_BLUE

p_line = doc.add_paragraph()
p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_line.paragraph_format.space_after = Pt(12)
r_line = p_line.add_run("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
r_line.font.bold = True
r_line.font.color.rgb = C_GOLD

p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_after = Pt(14)
r_sub = p_title.add_run("TÀI LIỆU CẦM TAY DÀNH CHO NGƯỜI THUYẾT TRÌNH\n")
r_sub.font.name = "Times New Roman"
r_sub.font.size = Pt(13)
r_sub.font.bold = True
r_sub.font.color.rgb = C_DARK_SLATE

r_main = p_title.add_run("KỊCH BẢN LỜI ĐỌC THUYẾT MINH BẢO VỆ BÀI TẬP LỚN\nĐỀ TÀI: HỆ THỐNG PHÂN TÍCH VÀ GIÁM SÁT CHẤT LƯỢNG MẠNG VIỄN THÔNG (HADOOP, SPARK, R)")
r_main.font.name = "Times New Roman"
r_main.font.size = Pt(15)
r_main.font.bold = True
r_main.font.color.rgb = C_BLUE

add_callout(
    doc,
    "HƯỚNG DẪN CÁCH SỬ DỤNG TÀI LIỆU NÀY",
    "Đây là bản kịch bản ĐỌC THUẦN LỜI THOẠI được biên soạn riêng để bạn in ra cầm tay hoặc để trên màn hình máy tính đọc trực tiếp trước Hội đồng. Toàn bộ câu từ đã được chau chuốt mượt mà, ngắt nhịp tự nhiên, in đậm các số liệu quan trọng để bạn tự động nhấn giọng. Thời gian toàn bài: 12 - 14 phút.",
    bg_color="EFF6FF"
)

# ==============================================================================
# PHẦN 1: KỊCH BẢN ĐỌC CHI TIẾT TỪ SLIDE 1 ĐẾN SLIDE 20
# ==============================================================================

speech_slides = [
    (
        "SLIDE 1: MỞ ĐẦU & GIỚI THIỆU THÀNH VIÊN",
        "30 giây",
        [
            ("Kính thưa Quý Thầy/Cô trong Hội đồng chấm Bài tập lớn và toàn thể các bạn sinh viên!\n\n", False, C_NAVY),
            ("Em xin đại diện cho ", False, C_TEXT),
            ("Nhóm 01 - Lớp ĐH13C2, Khoa Công nghệ Thông tin, Trường Đại học Tài nguyên và Môi trường Hà Nội", True, C_BLUE),
            (" xin được phép bắt đầu bài thuyết trình báo cáo kết quả Bài tập lớn môn ", False, C_TEXT),
            ("Xử lý Dữ liệu lớn (Mã học phần: CTKU122)", True, C_DARK_SLATE),
            (".\n\nĐề tài nghiên cứu và xây dựng của nhóm chúng em là: ", False, C_TEXT),
            ("'XÂY DỰNG HỆ THỐNG PHÂN TÍCH VÀ GIÁM SÁT CHẤT LƯỢNG MẠNG VIỄN THÔNG TRÊN NỀN TẢNG HADOOP, SPARK VÀ R'", True, C_BLUE),
            (".\n\nNhóm chúng em gồm có 4 thành viên: Em là ", False, C_TEXT),
            ("Hoàng Ngọc Thi", True, C_DARK_SLATE),
            (" - giữ vai trò Nhóm trưởng, cùng các bạn ", False, C_TEXT),
            ("Nguyễn Viết Hoàng Anh, Nguyễn Việt Hòa và Nguyễn Quốc Anh", True, C_DARK_SLATE),
            (". Chúng em xin trân trọng cảm ơn Thầy/Cô đã tận tình hướng dẫn và đồng hành cùng nhóm trong suốt học phần vừa qua!", False, C_TEXT)
        ],
        "Chuyển sang Slide 2"
    ),
    (
        "SLIDE 2: ĐẶT VẤN ĐỀ & BA MỤC TIÊU KỸ THUẬT CỐT LÕI",
        "45 giây",
        [
            ("Kính thưa Thầy/Cô, trong kỷ nguyên số hiện nay, một nhà mạng viễn thông quy mô quốc gia quản lý trên ", False, C_TEXT),
            ("50.000 trạm phát sóng BTS", True, C_BLUE),
            (". Mỗi giây trôi qua, hàng trăm nghìn dòng dữ liệu đo kiểm telemetry liên tục phát sinh, tích lũy lên tới hàng chục Terabyte mỗi ngày.\n\n", False, C_TEXT),
            ("Trước khối lượng dữ liệu khổng lồ này, các hệ quản trị cơ sở dữ liệu quan hệ truyền thống ", False, C_TEXT),
            ("RDBMS hoàn toàn quá tải và bất lực", True, C_RED),
            (", dẫn đến việc nhà mạng chỉ phát hiện ra sự cố khi khách hàng đã phản ánh khiếu nại gay gắt.\n\n", False, C_TEXT),
            ("Để giải quyết triệt để bài toán này, đề tài của chúng em đặt ra ", False, C_TEXT),
            ("3 mục tiêu kỹ thuật cốt lõi", True, C_DARK_SLATE),
            (":\n", False, C_TEXT),
            ("• Thứ nhất: ", True, C_BLUE),
            ("Giảm thiểu độ trễ mạng (Latency) thông qua việc phát hiện chính xác các trạm bị nghẽn truyền dẫn Backhaul;\n", False, C_TEXT),
            ("• Thứ hai: ", True, C_BLUE),
            ("Giảm tỷ lệ mất gói (Packet Loss) bằng giải pháp cô lập các sector cell vô tuyến bị can nhiễu;\n", False, C_TEXT),
            ("• Thứ ba: ", True, C_BLUE),
            ("Kéo giảm tỷ lệ rớt cuộc gọi (Call Drop Rate) về dưới ngưỡng cam kết chất lượng dịch vụ ", False, C_TEXT),
            ("SLA chuẩn quốc tế là 2.0%", True, C_EMERALD),
            (".", False, C_TEXT)
        ],
        "Chuyển sang Slide 3"
    ),
    (
        "SLIDE 3: ĐẶC TRƯNG BIG DATA 5V TRONG BÀI TOÁN VIỄN THÔNG",
        "40 giây",
        [
            ("Bài toán giám sát chất lượng mạng tế bào phản ánh trung thực và toàn diện ", False, C_TEXT),
            ("5 đặc trưng kinh điển của Big Data", True, C_BLUE),
            (":\n", False, C_TEXT),
            ("1. Volume: ", True, C_DARK_SLATE),
            ("Quy mô dữ liệu đạt hàng chục Terabyte log sinh ra mỗi ngày từ hàng chục nghìn trạm;\n", False, C_TEXT),
            ("2. Velocity: ", True, C_DARK_SLATE),
            ("Tốc độ phát sinh vượt ", False, C_TEXT),
            ("500.000 sự kiện/giây", True, C_GOLD),
            (" trong khung giờ cao điểm, đòi hỏi hệ thống phải xử lý cảnh báo tức thời;\n", False, C_TEXT),
            ("3. Variety: ", True, C_DARK_SLATE),
            ("Đa dạng định dạng từ dữ liệu có cấu trúc như bảng trạm BTS, bán cấu trúc như nhật ký Syslog RFC-5424, đến dữ liệu luồng đo kiểm telemetry;\n", False, C_TEXT),
            ("4. Veracity: ", True, C_DARK_SLATE),
            ("Độ nhiễu cao do can nhiễu vô tuyến và lệch xung đồng hồ NTP dẫn đến ", False, C_TEXT),
            ("các bản ghi có độ trễ âm hoặc thông lượng âm", True, C_RED),
            (" cần được lọc sạch;\n", False, C_TEXT),
            ("5. Value: ", True, C_DARK_SLATE),
            ("Giá trị mang lại là giúp nhà mạng ", False, C_TEXT),
            ("giảm 35% tỷ lệ khách hàng rời mạng", True, C_EMERALD),
            (" và tối ưu hóa hàng triệu USD chi phí đầu tư hạ tầng.\n\n", False, C_TEXT),
            ("Nhóm phân định rõ: luồng dữ liệu thời gian thực dùng cho cảnh báo khẩn cấp, còn dữ liệu tĩnh theo lô dùng cho báo cáo SLA và huấn luyện Machine Learning.", False, C_TEXT)
        ],
        "Chuyển sang Slide 4"
    ),
    (
        "SLIDE 4: KIẾN TRÚC TỔNG THỂ HỆ THỐNG (LAMBDA ARCHITECTURE)",
        "45 giây",
        [
            ("Kính thưa Thầy/Cô, để giải quyết đồng thời cả hai bài toán: tính toán toàn diện trên dữ liệu lịch sử và phát hiện sự cố tức thời, hệ thống của nhóm được xây dựng chuẩn mực theo ", False, C_TEXT),
            ("Kiến trúc Lambda 5 phân tầng", True, C_BLUE),
            (":\n\n", False, C_TEXT),
            ("• Tầng 1 - Nguồn dữ liệu (Data Sources): ", True, C_DARK_SLATE),
            ("Thu nhận log đo kiểm từ 20 trạm BTS, 80 cell và hệ thống tiếp nhận khiếu nại khách hàng CRM;\n", False, C_TEXT),
            ("• Tầng 2 - Thu nạp dữ liệu (Ingestion Layer): ", True, C_DARK_SLATE),
            ("Sử dụng ", False, C_TEXT),
            ("Apache Flume", True, C_BLUE),
            (" với cơ chế đệm luồng và giao dịch 2 pha chống mất tin;\n", False, C_TEXT),
            ("• Tầng 3 - Lưu trữ phân tán (Storage Layer): ", True, C_DARK_SLATE),
            ("Lưu trữ tập trung trên ", False, C_TEXT),
            ("Hadoop HDFS Data Lake với hệ số nhân bản RF=3", True, C_EMERALD),
            (";\n", False, C_TEXT),
            ("• Tầng 4 - Xử lý cốt lõi (Processing Layer): ", True, C_DARK_SLATE),
            ("Gồm 2 nhánh rẽ: ", False, C_TEXT),
            ("Batch Layer", True, C_BLUE),
            (" chạy MapReduce, Pig và Spark để tính KPI dài hạn; song song với ", False, C_TEXT),
            ("Speed Layer", True, C_GOLD),
            (" sử dụng CSDL NoSQL Apache HBase truy xuất độ trễ dưới 10 mili-giây;\n", False, C_TEXT),
            ("• Tầng 5 - Trực quan hóa & Phục vụ (Serving & Analytics): ", True, C_DARK_SLATE),
            ("Cung cấp giao diện bảng tính trực quan ", False, C_TEXT),
            ("IBM BigSheets, môi trường RStudio", True, C_BLUE),
            (" và Dashboard giám sát cho kỹ sư NOC.", False, C_TEXT)
        ],
        "Chuyển sang Slide 5"
    ),
    (
        "SLIDE 5: MÔ HÌNH DỮ LIỆU VIỄN THÔNG (ERD SCHEMA)",
        "35 giây",
        [
            ("Bước sang khâu thiết kế dữ liệu, sơ đồ thực thể quan hệ ERD được tổ chức theo cấu trúc phân cấp hình cây chuẩn mực của mạng di động tế bào:\n\n", False, C_TEXT),
            ("Mỗi trạm vật lý trong bảng ", False, C_TEXT),
            ("bts_towers", True, C_BLUE),
            (" liên kết 1 - N với các sector cell phát sóng đa hướng trong ", False, C_TEXT),
            ("cells_catalog", True, C_BLUE),
            (" qua khóa ngoại tower_id. Mỗi cell này liên tục ghi nhận hàng nghìn bản ghi đo kiểm chuỗi thời gian trong bảng ", False, C_TEXT),
            ("network_kpi_events", True, C_BLUE),
            (".\n\nĐồng thời, hệ thống tổng đài tự động ánh xạ các phản ánh của khách hàng trong bảng ", False, C_TEXT),
            ("customer_complaints", True, C_BLUE),
            (" về đúng cell và trạm đang phục vụ. Thiết kế quan hệ này đảm bảo tính toàn vẹn tham chiếu và tối ưu hóa tối đa cho các phép Join phân tán sau này.", False, C_TEXT)
        ],
        "Chuyển sang Slide 6"
    ),
    (
        "SLIDE 6: TẬP DỮ LIỆU & QUY TRÌNH TIỀN XỬ LÝ LÀM SẠCH",
        "40 giây",
        [
            ("Bộ dữ liệu thực nghiệm của đề tài gồm ", False, C_TEXT),
            ("12.001 dòng đo kiểm", True, C_BLUE),
            (" của 20 trạm BTS và 80 cell phát sóng tại 3 thành phố lớn: Hà Nội, Đà Nẵng và TP.HCM.\n\n", False, C_TEXT),
            ("Trong khâu tiền xử lý, nhóm đã xây dựng thuật toán lọc logic phát hiện và loại bỏ ", False, C_TEXT),
            ("48 bản ghi dị thường vật lý - chiếm tỷ lệ 0.40%", True, C_RED),
            (" - gồm các lỗi trễ âm do lệch xung nhịp NTP, thông lượng âm do tràn bộ đếm và mất gói vượt 100%, giữ lại ", False, C_TEXT),
            ("11.952 bản ghi hoàn toàn sạch, đạt độ tinh khiết 99.6%", True, C_EMERALD),
            (".\n\nTiếp đó, nhóm tiến hành tạo 4 đặc trưng kỹ thuật mới: Dung lượng phiên truyền tải session_volume, Tỷ lệ rớt cuộc gọi chuẩn hóa, Cờ cảnh báo quá tải và Điểm chất lượng dịch vụ tổng hợp ", False, C_TEXT),
            ("QoS Score thang điểm 100", True, C_GOLD),
            (".", False, C_TEXT)
        ],
        "Chuyển sang Slide 7"
    ),
    (
        "SLIDE 7: HẠ TẦNG HDFS DATA LAKE & PHÂN VÙNG DỮ LIỆU",
        "40 giây",
        [
            ("Trên kho lưu trữ phân tán Hadoop HDFS, dữ liệu được phân chia thành ", False, C_TEXT),
            ("4 vùng dữ liệu độc lập", True, C_BLUE),
            (": Vùng Raw lưu trữ bất biến; Vùng Staging đệm nạp; Vùng Curated chứa dữ liệu sạch nén Snappy Parquet; và Vùng Output chứa kết quả tính toán.\n\n", False, C_TEXT),
            ("Cấu trúc thư mục được phân vùng phân cấp theo năm, tháng, ngày, công nghệ mạng và mã trạm, giúp Spark loại bỏ hơn ", False, C_TEXT),
            ("90% dữ liệu thừa", True, C_EMERALD),
            (" khi quét đĩa.\n\nVới quy mô mạng lưới 500 trạm thực tế sinh ra 34.5 triệu sự kiện mỗi ngày, nhóm đã tính toán chi tiết: sau khi nén Parquet và nhân bản 3 lần (RF=3), hệ thống cần ", False, C_TEXT),
            ("13.58 Terabyte đĩa HDFS cho 3 năm hoạt động", True, C_BLUE),
            (". Nếu một DataNode bị sự cố quá 10 phút 30 giây, NameNode sẽ tự động phát hiện qua Heartbeat và sao chép nhân bản các block bị thiếu sang node khác để luôn bảo toàn đúng 3 bản sao chịu lỗi.", False, C_TEXT)
        ],
        "Chuyển sang Slide 8"
    ),
    (
        "SLIDE 8: THU THẬP LOG PHÂN TÁN VỚI APACHE FLUME",
        "40 giây",
        [
            ("Để thu nạp dữ liệu bền vững, hệ thống cấu hình ", False, C_TEXT),
            ("Apache Flume với 2 kịch bản chuyên biệt", True, C_BLUE),
            (":\n\n", False, C_TEXT),
            ("• Kịch bản 1: ", True, C_DARK_SLATE),
            ("Sử dụng Spooling Directory Source nạp lô tệp CSV định kỳ, qua FileChannel bền bỉ ghi xuống HDFS Sink với kích thước cắt file đúng ", False, C_TEXT),
            ("128 MB khớp với kích thước block HDFS", True, C_EMERALD),
            (" để triệt tiêu hoàn toàn vấn đề tệp nhỏ;\n", False, C_TEXT),
            ("• Kịch bản 2: ", True, C_DARK_SLATE),
            ("Tiếp nhận luồng sự kiện nóng qua cổng Netcat 8888, áp dụng cơ chế ", False, C_TEXT),
            ("Fan-out nhân đôi luồng", True, C_GOLD),
            (": một nhánh qua MemoryChannel nạp nhanh vào HDFS, nhánh còn lại qua FileChannel nạp an toàn vào HBase NoSQL.\n\n", False, C_TEXT),
            ("Flume vận hành theo ", False, C_TEXT),
            ("cơ chế giao dịch 2 pha (Two-Phase Commit)", True, C_BLUE),
            (": sự kiện chỉ được xóa khỏi Channel khi Sink đã nhận tín hiệu ACK ghi thành công xuống đĩa, đảm bảo dữ liệu không bao giờ bị thất lạc.", False, C_TEXT)
        ],
        "Chuyển sang Slide 9"
    ),
    (
        "SLIDE 9: THUẬT TOÁN HADOOP MAPREDUCE TỐI ƯU HÓA (JAVA)",
        "45 giây",
        [
            ("Kính thưa Thầy/Cô, trong chương trình MapReduce thuần Java TelecomKpiAnalysis, nhóm đã áp dụng ", False, C_TEXT),
            ("3 kỹ thuật tối ưu hóa chuyên sâu", True, C_BLUE),
            (":\n\n", False, C_TEXT),
            ("1. Khóa phức hợp TowerTechKey: ", True, C_DARK_SLATE),
            ("Gói gọn cả mã trạm và công nghệ mạng, hiện thực interface WritableComparable để sắp xếp tự nhiên dữ liệu;\n", False, C_TEXT),
            ("2. Custom Partitioner: ", True, C_DARK_SLATE),
            ("Chỉ băm theo trường tower_id duy nhất, đảm bảo toàn bộ dữ liệu 3G, 4G, 5G của cùng một trạm BTS đều tập trung về đúng một Reducer, ", False, C_TEXT),
            ("triệt tiêu hoàn toàn hiện tượng lệch dữ liệu (Data Skew)", True, C_RED),
            (";\n", False, C_TEXT),
            ("3. Combiner: ", True, C_DARK_SLATE),
            ("Đóng vai trò như Mini-Reducer chạy ngay tại DataNode để cộng dồn sơ bộ các chỉ số đo kiểm, giúp ", False, C_TEXT),
            ("cắt giảm hơn 80% lưu lượng truyền tải trên mạng", True, C_EMERALD),
            (" trong pha Shuffle & Sort. Kết quả tính toán được ghi ra file phân tách tab trên HDFS.", False, C_TEXT)
        ],
        "Chuyển sang Slide 10"
    ),
    (
        "SLIDE 10: XỬ LÝ VÀ PHÂN CỤM DỮ LIỆU BẰNG APACHE PIG LATIN",
        "35 giây",
        [
            ("Song song với MapReduce Java, nhóm phát triển kịch bản Pig Latin telecom_kpi_analysis.pig để rút ngắn thời gian phát triển ETL. Kịch bản thực hiện chuỗi toán tử hoàn chỉnh:\n\n", False, C_TEXT),
            ("Lệnh ", False, C_TEXT),
            ("LOAD", True, C_BLUE),
            (" nạp dữ liệu với schema rõ ràng; ", False, C_TEXT),
            ("FILTER", True, C_BLUE),
            (" loại bỏ bản ghi lỗi; ", False, C_TEXT),
            ("JOIN", True, C_BLUE),
            (" dữ liệu đo kiểm với danh mục trạm; ", False, C_TEXT),
            ("GROUP", True, C_BLUE),
            (" theo bộ ba trạm, công nghệ và tỉnh thành; dùng ", False, C_TEXT),
            ("FOREACH", True, C_BLUE),
            (" kết hợp các hàm COUNT, AVG độ trễ, AVG mất gói để tính tỷ lệ rớt mạng; và dùng lệnh ", False, C_TEXT),
            ("SPLIT", True, C_GOLD),
            (" phân luồng lọc ra danh sách các trạm vượt ngưỡng ", False, C_TEXT),
            ("SLA 2.0%", True, C_RED),
            (" rồi ghi thẳng xuống HDFS.", False, C_TEXT)
        ],
        "Chuyển sang Slide 11"
    ),
    (
        "SLIDE 11: ĐỘNG CƠ TÍNH TOÁN IN-MEMORY APACHE SPARK",
        "45 giây",
        [
            ("Đóng vai trò là trái tim tính toán của hệ thống, pipeline PySpark telecom_spark_pipeline.py tận dụng tối đa kiến trúc In-Memory để bứt phá hiệu năng. Chương trình thực thi 7 phép biến đổi Transformations và 4 hành động Actions.\n\n", False, C_TEXT),
            ("Đặc biệt, nhóm áp dụng kỹ thuật ", False, C_TEXT),
            ("persist với cấp độ MEMORY_AND_DISK", True, C_BLUE),
            (" ngay sau phép Join 4 bảng, vì DataFrame này được tái sử dụng 3 lần liên tiếp cho Spark SQL, tổng hợp KPI và lọc cell quá tải.\n\n", False, C_TEXT),
            ("Nhờ trình tối ưu hóa Catalyst Optimizer và động cơ Tungsten sinh mã nhị phân, Spark thực thi toàn bộ luồng xử lý chỉ trong ", False, C_TEXT),
            ("2.3 giây, nhanh gấp 15.4 lần", True, C_EMERALD),
            (" so với MapReduce truyền thống mất ", False, C_TEXT),
            ("35.4 giây", True, C_RED),
            (". Dữ liệu sau đó được xuất ra định dạng Snappy Parquet tối ưu dung lượng.", False, C_TEXT)
        ],
        "Chuyển sang Slide 12"
    ),
    (
        "SLIDE 12: CƠ SỞ DỮ LIỆU NOSQL APACHE HBASE ĐỘ TRỄ THẤP (< 10MS)",
        "40 giây",
        [
            ("Để đáp ứng nhu cầu tra cứu thông tin trạm phát sóng tức thời dưới 10 mili-giây cho kỹ sư trực ban NOC, nhóm đã thiết kế CSDL NoSQL Apache HBase với cấu trúc RowKey tối ưu: ", False, C_TEXT),
            ("đảo chuỗi mã trạm kết hợp công nghệ mạng và dấu thời gian đảo ngược reverse_timestamp", True, C_BLUE),
            (".\n\n", False, C_TEXT),
            ("Kỹ thuật đảo mã trạm giúp các trạm liên tiếp phân tán đều sang các RegionServer khác nhau, ", False, C_TEXT),
            ("triệt tiêu hoàn toàn điểm nghẽn ghi tập trung (Write Hotspotting)", True, C_RED),
            ("; trong khi đảo thời gian giúp phiên đo kiểm mới nhất luôn nằm ở đầu bảng.\n\n", False, C_TEXT),
            ("Bảng telecom_kpi gồm 3 Column Families: ", False, C_TEXT),
            ("cf_kpi", True, C_BLUE),
            (" lưu chỉ số đo kiểm có TTL 90 ngày, ", False, C_TEXT),
            ("cf_cell", True, C_BLUE),
            (" lưu cấu hình vô tuyến và ", False, C_TEXT),
            ("cf_alert", True, C_BLUE),
            (" lưu cảnh báo sự cố, tích hợp Pre-splitting 4 phân vùng.", False, C_TEXT)
        ],
        "Chuyển sang Slide 13"
    ),
    (
        "SLIDE 13: QUY TRÌNH PHÂN TÍCH VỚI IBM BIGSHEETS",
        "40 giây",
        [
            ("Đối với chuyên viên kinh doanh và cán bộ quản lý mạng không có kỹ năng lập trình, giải pháp phân tích bảng tính No-Code của ", False, C_TEXT),
            ("IBM BigSheets", True, C_BLUE),
            (" là vô cùng đắc lực. Nhóm đã xây dựng một ứng dụng Web tương tác mô phỏng toàn diện quy trình BigSheets 6 bước và ánh xạ tương đương 1-1 với Spark DataFrame:\n\n", False, C_TEXT),
            ("• Bước 1 Collection nạp CSV tương đương read.csv;\n", False, C_TEXT),
            ("• Bước 2 Data Cleansing lọc bản ghi lỗi tương đương filter;\n", False, C_TEXT),
            ("• Bước 3 Calculated Column tính dung lượng phiên tương đương withColumn;\n", False, C_TEXT),
            ("• Bước 4 Dimension Join tương đương hàm join;\n", False, C_TEXT),
            ("• Bước 5 Pivot Sheet tổng hợp KPI tương đương groupBy;\n", False, C_TEXT),
            ("• Bước 6 xuất Dashboard trực quan đa chiều với các bộ lọc tương tác một chạm.", False, C_TEXT)
        ],
        "Chuyển sang Slide 14"
    ),
    (
        "SLIDE 14: KHOA HỌC DỮ LIỆU & HỌC MÁY BẰNG R VÀ CSDL SQLITE",
        "45 giây",
        [
            ("Kính thưa Thầy/Cô, ở tầng Khoa học dữ liệu chuyên sâu, kịch bản R telecom_analysis.R kết nối với cơ sở dữ liệu SQLite qua thư viện DBI và RSQLite, thực thi truy vấn SQL có Join 4 bảng và Group By, sau đó dùng dplyr tổng hợp số liệu.\n\n", False, C_TEXT),
            ("Đóng góp nổi bật của nhóm là đã huấn luyện thành công ", False, C_TEXT),
            ("mô hình Học máy Hồi quy Logistic (Logistic Regression)", True, C_BLUE),
            (" để dự báo xác suất phát sinh khiếu nại của khách hàng. Kết quả kiểm định thống kê cho thấy hệ số hồi quy của Độ trễ và Mất gói đều đạt mức ý nghĩa vượt trội với ", False, C_TEXT),
            ("p < 0.001", True, C_EMERALD),
            (".\n\nMô hình chỉ ra rằng: khi một trạm có độ trễ vượt 120ms và mất gói trên 5%, ", False, C_TEXT),
            ("xác suất khách hàng khiếu nại tăng vọt lên mức 82%", True, C_RED),
            (". Toàn bộ kết quả dự báo được ghi ngược lại bảng kpi_analysis_summary trong CSDL SQLite.", False, C_TEXT)
        ],
        "Chuyển sang Slide 15"
    ),
    (
        "SLIDE 15: KẾT QUẢ THỰC NGHIỆM ĐỊNH LƯỢNG & TOP 3 TRẠM SỰ CỐ",
        "40 giây",
        [
            ("Qua quá trình tính toán và đối soát dữ liệu trên 12.000 phiên đo kiểm, hệ thống ghi nhận các chỉ số bình quân toàn mạng: Độ trễ trung bình đạt 46.8 ms và Tỷ lệ rớt cuộc gọi đạt 1.85% - hoàn thành cam kết chất lượng dịch vụ SLA dưới 2.0%.\n\n", False, C_TEXT),
            ("Tuy nhiên, khi đi sâu vào xếp hạng từng trạm, hệ thống đã cô lập chính xác ", False, C_TEXT),
            ("3 trạm phát sóng gặp sự cố nghiêm trọng nhất: trạm TOWER_003 tại Hà Nội, TOWER_008 tại TP.HCM và TOWER_015 tại Đà Nẵng", True, C_RED),
            (".\n\nCả 3 trạm này đều có tỷ lệ rớt mạng trên ", False, C_TEXT),
            ("7.5% (đặc biệt TOWER_003 lên tới 11.81%)", True, C_RED),
            (" và độ trễ vọt lên trên 180 ms trên toàn bộ các dải tần 3G, 4G và 5G, khẳng định nguyên nhân cốt lõi không phải do anten vô tuyến mà do ", False, C_TEXT),
            ("nghẽn đường truyền cáp quang Backhaul nối về mạng lõi", True, C_BLUE),
            (".", False, C_TEXT)
        ],
        "Chuyển sang Slide 16"
    ),
    (
        "SLIDE 16: TRỰC QUAN HÓA CHẤT LƯỢNG MẠNG & BIỂU ĐỒ BONG BÓNG",
        "35 giây",
        [
            ("Kết quả phân tích được trực quan hóa sinh động qua chuỗi biểu đồ khoa học: Biểu đồ hộp Boxplot khẳng định mạng 5G có độ trễ trung bình siêu thấp chỉ 12.4 ms so với 3G là 78.5 ms; Đồ thị tương quan chỉ ra mối quan hệ đồng biến chặt chẽ giữa tỷ lệ mất gói và rớt cuộc gọi.\n\n", False, C_TEXT),
            ("Và đặc biệt là ", False, C_TEXT),
            ("Biểu đồ bong bóng đa chiều", True, C_BLUE),
            (" tương quan giữa Độ trễ, Mất gói và Kích thước bong bóng là số thuê bao. ", False, C_TEXT),
            ("3 cụm bong bóng màu đỏ nằm tách biệt ở góc trên bên phải chính là 3 trạm suy thoái TOWER_003, 008 và 015", True, C_RED),
            (", cung cấp cái nhìn trực quan tức thời cho các kỹ sư điều hành mạng NOC.", False, C_TEXT)
        ],
        "Chuyển sang Slide 17"
    ),
    (
        "SLIDE 17: BẢNG ĐỐI CHIẾU HIỆU NĂNG CÔNG NGHỆ (SPARK - PIG - MR - R)",
        "40 giây",
        [
            ("Bảng 4.2 tổng hợp kết quả đối chiếu định lượng giữa 4 công nghệ trên cùng tập dữ liệu:\n\n", False, C_TEXT),
            ("• Apache Spark: ", True, C_BLUE),
            ("Thời gian thực thi chỉ ", False, C_TEXT),
            ("2.3 giây", True, C_EMERALD),
            (" nhờ kiến trúc tính toán trên bộ nhớ RAM và trình tối ưu Catalyst;\n", False, C_TEXT),
            ("• Apache Pig Latin: ", True, C_BLUE),
            ("Chạy mất ", False, C_TEXT),
            ("18.0 giây", True, C_GOLD),
            (" với cú pháp cực kỳ ngắn gọn phù hợp làm ETL trên Data Lake;\n", False, C_TEXT),
            ("• Hadoop MapReduce: ", True, C_BLUE),
            ("Mất ", False, C_TEXT),
            ("35.4 giây", True, C_RED),
            (" do chi phí ghi đĩa trung gian và đọc lại ở pha Shuffle, nhưng vẫn là giải pháp ổn định nhất cho các tác vụ xử lý lô cực lớn chạy qua đêm;\n", False, C_TEXT),
            ("• Ngôn ngữ R: ", True, C_BLUE),
            ("Xử lý trong ", False, C_TEXT),
            ("1.8 giây", True, C_EMERALD),
            (", đảm nhận xuất sắc vai trò phân tích thống kê chuyên sâu và huấn luyện mô hình học máy.", False, C_TEXT)
        ],
        "Chuyển sang Slide 18"
    ),
    (
        "SLIDE 18: MA TRẬN 5 KHUYẾN NGHỊ HÀNH ĐỘNG CHO TRUNG TÂM NOC",
        "45 giây",
        [
            ("Căn cứ trên các bằng chứng dữ liệu định lượng, nhóm trân trọng đề xuất ", False, C_TEXT),
            ("Ma trận 5 khuyến nghị kỹ thuật hành động", True, C_BLUE),
            (" gửi Trung tâm Điều hành Mạng NOC:\n\n", False, C_TEXT),
            ("• Khuyến nghị 1 (Ưu tiên P1 - trong 48h): ", True, C_RED),
            ("Điều động xe phát sóng lưu động COW và nâng cấp đường truyền Backhaul từ 100 Mbps lên 1 Gbps cho 3 trạm TOWER_003, 008 và 015 để kéo rớt mạng về dưới 2%;\n", False, C_TEXT),
            ("• Khuyến nghị 2 (P2 - trong 6 tháng): ", True, C_GOLD),
            ("Tắt sóng 3G và tái quy hoạch băng tần 2100 MHz sang cho 4G/5G nhằm tăng 40% dung lượng mạng;\n", False, C_TEXT),
            ("• Khuyến nghị 3 (P3 - trong 2 tuần): ", True, C_BLUE),
            ("Kích hoạt tính năng Mạng tự tối ưu SON để tự động san tải thuê bao giữa các cell lân cận;\n", False, C_TEXT),
            ("• Khuyến nghị 4 (P4 - trong 1 tháng): ", True, C_EMERALD),
            ("Tích hợp mô hình Logistic R vào CRM để chủ động gửi tin nhắn xin lỗi kèm voucher data cho thuê bao gặp sự cố, giảm 35% tỷ lệ rời mạng;\n", False, C_TEXT),
            ("• Khuyến nghị 5 (P5): ", True, C_DARK_SLATE),
            ("Quy chuẩn hóa lưu trữ Snappy Parquet và đặt TTL 90 ngày trên HBase, giúp tiết kiệm 60% chi phí mở rộng ổ cứng.", False, C_TEXT)
        ],
        "Chuyển sang Slide 19"
    ),
    (
        "SLIDE 19: KẾT LUẬN CÁC KẾT QUẢ ĐẠT ĐƯỢC & HƯỚNG PHÁT TRIỂN",
        "30 giây",
        [
            ("Tổng kết lại, đề tài đã hoàn thành xuất sắc 100% mục tiêu đề ra: làm chủ trọn vẹn hệ sinh thái Big Data đa nền tảng, tối ưu hóa thuật toán MapReduce, xây dựng pipeline Spark In-Memory tốc độ cao và ứng dụng mô hình học máy giải quyết triệt để 3 bài toán chỉ số viễn thông.\n\n", False, C_TEXT),
            ("Về hạn chế, hệ thống hiện thực nghiệm trên cụm giả lập máy đơn và mô hình dừng ở hồi quy tuyến tính. ", False, C_TEXT),
            ("Hướng phát triển tiếp theo của nhóm là triển khai hàng đợi thông điệp Apache Kafka kết hợp Apache Flink để đạt độ trễ xử lý luồng dưới 50 mili-giây, và ứng dụng mạng nơ-ron học sâu LSTM để dự báo đứt gãy truyền dẫn trước 30 đến 60 phút.", True, C_BLUE)
        ],
        "Chuyển sang Slide 20"
    ),
    (
        "SLIDE 20: KẾT THÚC BÁO CÁO & SẴN SÀNG CHO PHIÊN PHẢN BIỆN",
        "20 giây",
        [
            ("Bài thuyết trình báo cáo kết quả Bài tập lớn của Nhóm 01 đến đây xin được phép kết thúc.\n\n", False, C_NAVY),
            ("Chúng em xin chân thành cảm ơn sự chú ý lắng nghe và theo dõi của Quý Thầy/Cô và các bạn! Nhóm chúng em rất mong nhận được những ý kiến nhận xét quý báu, đóng góp chuyên môn và các câu hỏi phản biện từ Thầy/Cô để đề tài được hoàn thiện sâu sắc hơn nữa.\n\n", False, C_TEXT),
            ("Chúng em xin trân trọng cảm ơn!", True, C_BLUE)
        ],
        "Kết thúc thuyết trình, chuyển sang Demo và Hỏi đáp"
    ),
]

for title, duration, content_runs, next_action in speech_slides:
    p_h = doc.add_paragraph()
    p_h.paragraph_format.space_before = Pt(14)
    p_h.paragraph_format.space_after = Pt(4)
    p_h.paragraph_format.keep_with_next = True
    r_h = p_h.add_run(f"🎙️ {title} (Thời lượng: {duration})")
    r_h.font.name = "Times New Roman"
    r_h.font.size = Pt(13)
    r_h.font.bold = True
    r_h.font.color.rgb = C_BLUE

    # Khung đọc lời thoại
    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = 'Table Grid'
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=100, bottom=100, left=140, right=140)

    p_c = cell.paragraphs[0]
    p_c.paragraph_format.space_before = Pt(2)
    p_c.paragraph_format.space_after = Pt(2)
    p_c.paragraph_format.line_spacing = 1.3

    for txt, is_bold, col in content_runs:
        r = p_c.add_run(txt)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
        r.font.bold = is_bold
        r.font.color.rgb = col

    p_act = doc.add_paragraph()
    p_act.paragraph_format.space_before = Pt(3)
    p_act.paragraph_format.space_after = Pt(6)
    r_act = p_act.add_run(f"👉 Hành động kế tiếp: {next_action}")
    r_act.font.name = "Times New Roman"
    r_act.font.size = Pt(10.5)
    r_act.font.italic = True
    r_act.font.color.rgb = C_GOLD

# ==============================================================================
# PHẦN 2: LỜI ĐỌC THAO TÁC LIVE DEMO (2 PHÚT)
# ==============================================================================
doc.add_page_break()
p_demo = doc.add_paragraph()
p_demo.paragraph_format.space_before = Pt(16)
p_demo.paragraph_format.space_after = Pt(8)
r_dm = p_demo.add_run("II. LỜI ĐỌC KHI THAO TÁC LIVE DEMO TRỰC TIẾP (2 PHÚT)")
r_dm.font.name = "Times New Roman"
r_dm.font.size = Pt(14)
r_dm.font.bold = True
r_dm.font.color.rgb = C_NAVY

demo_steps = [
    (
        "Bước 1: Mở giao diện Web Dashboard BigSheets (start_bigsheets.bat)",
        "Dạ thưa Thầy/Cô, đây là giao diện Web Dashboard mô phỏng chuẩn 6 bước phân tích của IBM BigSheets được nhóm xây dựng và kết nối trực tiếp với dữ liệu Spark DataFrame. Chuyên viên NOC chỉ cần chọn bộ lọc Tỉnh thành (ví dụ Hà Nội) và Công nghệ mạng (4G), hệ thống sẽ lập tức lọc động và hiển thị danh sách cảnh báo Top trạm suy thoái cùng các biểu đồ trực quan mà không cần viết bất kỳ dòng mã nào."
    ),
    (
        "Bước 2: Mở bảng CSDL SQLite & Kết quả Học máy R (view_kpi_analysis_summary.bat)",
        "Dạ thưa Thầy/Cô, đây là bảng kpi_analysis_summary gồm 60 dòng và 18 cột được kịch bản R huấn luyện và ghi ngược vào SQLite. Thầy/Cô có thể thấy cột predicted_complaint_prob và nhãn HIGH_RISK màu đỏ cảnh báo chính xác các trạm TOWER_003, TOWER_008 và TOWER_015 có xác suất khách hàng khiếu nại vọt lên 82% do độ trễ vượt 180ms."
    ),
    (
        "Bước 3: Mở Source Code minh chứng (Khi Thầy/Cô hỏi vào mã lệnh)",
        "Dạ thưa Thầy/Cô, đây là mã nguồn MapReduce Java tại thư mục mapreduce/TelecomKpiAnalysis.java, nhóm đã hiện thực lớp TowerPartitioner để băm theo mã trạm chống lệch dữ liệu. Và đây là pipeline PySpark tại spark/telecom_spark_pipeline.py sử dụng persist(MEMORY_AND_DISK) để đạt tốc độ 2.3 giây."
    )
]

for d_title, d_speech in demo_steps:
    p_dt = doc.add_paragraph()
    p_dt.paragraph_format.space_before = Pt(8)
    p_dt.paragraph_format.space_after = Pt(2)
    r_dt = p_dt.add_run(f"🖥️ {d_title}")
    r_dt.font.name = "Times New Roman"
    r_dt.font.size = Pt(12)
    r_dt.font.bold = True
    r_dt.font.color.rgb = C_BLUE

    p_ds = doc.add_paragraph()
    p_ds.paragraph_format.space_before = Pt(2)
    p_ds.paragraph_format.space_after = Pt(6)
    p_ds.paragraph_format.line_spacing = 1.25
    r_spk = p_ds.add_run(f'Lời đọc nói với giảng viên: "{d_speech}"')
    r_spk.font.name = "Times New Roman"
    r_spk.font.size = Pt(11.5)
    r_spk.font.italic = True
    r_spk.font.color.rgb = C_TEXT

# ==============================================================================
# PHẦN 3: LỜI ĐỌC TRẢ LỜI PHẢN BIỆN (TOP 10 CÂU HỎI Q&A)
# ==============================================================================
doc.add_page_break()
p_qa = doc.add_paragraph()
p_qa.paragraph_format.space_before = Pt(16)
p_qa.paragraph_format.space_after = Pt(8)
r_qa = p_qa.add_run("III. LỜI ĐỌC KHI TRẢ LỜI 10 CÂU HỎI PHẢN BIỆN CỦA HỘI ĐỒNG")
r_qa.font.name = "Times New Roman"
r_qa.font.size = Pt(14)
r_qa.font.bold = True
r_qa.font.color.rgb = C_NAVY

qa_read = [
    ("Câu 1: Tại sao có độ trễ âm và thông lượng âm trong dữ liệu viễn thông?",
     "Dạ thưa Thầy/Cô, độ trễ âm xuất hiện do hiện tượng lệch xung nhịp đồng hồ mạng NTP giữa trạm BTS và máy chủ trung tâm; còn thông lượng âm do lỗi tràn số nguyên (Counter Overflow) tại firmware của router cũ. Nhóm đã xây dựng bộ lọc logic tự động loại bỏ 48 bản ghi dị thường này (chiếm 0.40%) và gắn cờ quality_flag=0 để cách ly xử lý, đảm bảo tập dữ liệu đưa vào tính toán đạt độ sạch tuyệt đối 99.6%."),
    ("Câu 2: Tại sao trong Apache Flume dùng cả MemoryChannel và FileChannel?",
     "Dạ thưa Thầy/Cô, đây là chiến lược cân đối giữa tốc độ và độ an toàn: MemoryChannel lưu trên RAM có thông lượng cực cao rất phù hợp để nạp nhanh luồng log vào HDFS; tuy nhiên MemoryChannel có tính chất bốc hơi, nếu sập nguồn sẽ mất tin. Vì vậy với nhánh ghi vào HBase NoSQL phục vụ giám sát trọng yếu, nhóm sử dụng FileChannel ghi xuống đĩa, kết hợp giao dịch 2 pha bảo đảm dữ liệu không bao giờ bị thất lạc."),
    ("Câu 3: Hệ số nhân bản HDFS RF=3 có lãng phí đĩa không? Khi DataNode chết xử lý thế nào?",
     "Dạ thưa Thầy/Cô, RF=3 là chuẩn công nghiệp vàng của Hadoop: 2 bản sao lưu cùng rack để đọc nhanh, và 1 bản sao lưu ở rack khác để phòng chống cháy nổ hay đứt nguồn cả tủ mạng. Nhờ nén Snappy Parquet tiết kiệm 65% dung lượng, 3 năm của 500 trạm chỉ tốn 13.58 TB, hoàn toàn kinh tế. Khi 1 DataNode chết sau 10 phút 30 giây không gửi Heartbeat, NameNode tự động quét danh mục block bị thiếu và ra lệnh nhân bản sang node khác để luôn duy trì đủ 3 bản sao."),
    ("Câu 4: Apache Pig khác gì so với Hadoop MapReduce thuần Java?",
     "Dạ thưa Thầy/Cô, Pig Latin là ngôn ngữ luồng dữ liệu khai báo bậc cao. Thay vì phải viết hơn 300 dòng mã Java phức tạp với Mapper, Reducer, Writable, lập trình viên chỉ cần viết khoảng 25 dòng lệnh Pig. Trình biên dịch Pig sẽ tự động dịch các câu lệnh này thành một đồ thị có hướng DAG gồm chuỗi các MapReduce jobs tối ưu ngầm định, giúp rút ngắn thời gian phát triển ETL tới 70%."),
    ("Câu 5: Trong MapReduce, Custom Partitioner và Combiner giải quyết bài toán gì?",
     "Dạ thưa Thầy/Cô, Custom Partitioner của nhóm chỉ băm theo mã trạm tower_id duy nhất, đảm bảo toàn bộ dữ liệu 3G, 4G, 5G của cùng một trạm BTS đều tập trung về đúng 1 Reducer, triệt tiêu hoàn toàn hiện tượng lệch dữ liệu (Data Skew) khiến 1 Reducer quá tải còn các Reducer khác ngồi chơi; Còn Combiner đóng vai trò như một Mini-Reducer chạy cục bộ trên DataNode sau pha Map để cộng dồn sơ bộ các chỉ số đo kiểm, giúp cắt giảm hơn 80% lưu lượng truyền tải trên mạng trong pha Shuffle & Sort."),
    ("Câu 6: Tại sao Apache Spark lại chạy nhanh gấp 15 lần MapReduce? Khi nào dùng persist?",
     "Dạ thưa Thầy/Cô, Spark nhanh hơn vượt trội nhờ tính toán In-Memory trên RAM, trình tối ưu hóa Catalyst Optimizer tự động đẩy các phép lọc xuống trước khi Join, và động cơ Tungsten sinh mã bytecode nhị phân trực tiếp. Nhóm sử dụng persist(MEMORY_AND_DISK) ngay sau phép Join 4 bảng vì DataFrame này được tái sử dụng liên tiếp 3 lần cho Spark SQL, tổng hợp KPI và lọc cell quá tải, tránh việc Spark phải tính toán lại đồ thị DAG từ đầu."),
    ("Câu 7: Cấu trúc RowKey trong Apache HBase tại sao phải đảo chuỗi mã trạm?",
     "Dạ thưa Thầy/Cô, nếu đặt mã trạm bình thường thì các trạm cùng tiền tố sẽ bị lưu tập trung trên đúng 1 RegionServer duy nhất, gây ra nghẽn ghi tập trung (Write Hotspotting). Việc đảo chuỗi mã trạm kết hợp Pre-splitting 4 vùng giúp lưu lượng ghi phân tán đều khắp các node trên cụm; đồng thời việc đảo dấu thời gian reverse_timestamp giúp các phiên đo kiểm MỚI NHẤT luôn nằm ở đầu bảng, lệnh Scan chỉ cần quét phạm vi ngắn O(1) là lấy được dữ liệu thời gian thực."),
    ("Câu 8: BigSheets có ưu điểm gì so với việc viết code Spark thông thường?",
     "Dạ thưa Thầy/Cô, BigSheets cung cấp giao diện bảng tính trực quan No-Code thân thiện như Microsoft Excel. Người dùng nghiệp vụ, chuyên viên kinh doanh và ban giám đốc có thể tự tay lọc dữ liệu, tạo cột tính toán, Join bảng danh mục và xem Dashboard mà không cần phải biết lập trình Python hay Java. Phía sau giao diện đó, hệ thống tự động biên dịch các thao tác bảng tính thành các tác vụ tính toán phân tán Spark DataFrame trên cụm Big Data."),
    ("Câu 9: Mô hình Hồi quy Logistic trong R đem lại giá trị kinh tế gì cho nhà mạng?",
     "Dạ thưa Thầy/Cô, mô hình lượng hóa chính xác mối quan hệ giữa các chỉ số mạng và hành vi khách hàng: khi độ trễ vượt 120ms và mất gói trên 5%, xác suất khách hàng khiếu nại tăng vọt lên mức 82% với độ tin cậy p < 0.001. Thay vì đợi khách hàng gọi điện phàn nàn mới xử lý, nhà mạng sử dụng mô hình này để chuyển sang chế độ chăm sóc khách hàng chủ động: tự động gửi tin nhắn SMS xin lỗi kèm voucher data ưu đãi cho các thuê bao bị ảnh hưởng ngay trong ngày, giúp kéo giảm 35% tỷ lệ thuê bao rời mạng."),
    ("Câu 10: Căn cứ vào đâu kết luận 3 trạm TOWER_003, 008, 015 bị nghẽn truyền dẫn Backhaul?",
     "Dạ thưa Thầy/Cô, bằng chứng dữ liệu thực nghiệm chỉ ra rằng: cả 3 trạm này đều bị suy giảm chất lượng đồng thời trên toàn bộ các công nghệ mạng (3G, 4G và cả 5G), với tỷ lệ rớt cuộc gọi đều vọt lên trên 7.5% và độ trễ trên 180 ms. Nếu nguyên nhân là do vô tuyến (như anten lệch hướng hay can nhiễu tần số) thì thông thường chỉ bị ảnh hưởng trên một dải tần hoặc một sector cell cụ thể; nhưng việc toàn bộ các dải tần của cả trạm đều nghẽn chứng minh chắc chắn điểm nghẽn nằm ở đường truyền cáp quang Backhaul nối từ trạm BTS về mạng lõi.")
]

for q_title, a_speech in qa_read:
    p_qt = doc.add_paragraph()
    p_qt.paragraph_format.space_before = Pt(8)
    p_qt.paragraph_format.space_after = Pt(2)
    p_qt.paragraph_format.keep_with_next = True
    r_qt = p_qt.add_run(f"❓ {q_title}")
    r_qt.font.name = "Times New Roman"
    r_qt.font.size = Pt(12)
    r_qt.font.bold = True
    r_qt.font.color.rgb = C_RED

    p_qa_ans = doc.add_paragraph()
    p_qa_ans.paragraph_format.space_before = Pt(2)
    p_qa_ans.paragraph_format.space_after = Pt(6)
    p_qa_ans.paragraph_format.line_spacing = 1.25
    r_ans = p_qa_ans.add_run(f'Lời đọc trả lời: "{a_speech}"')
    r_ans.font.name = "Times New Roman"
    r_ans.font.size = Pt(11.5)
    r_ans.font.color.rgb = C_DARK_SLATE

doc.save(output_path)
print(f"SUCCESS: Da tao thanh cong tep Word: {output_path}")
