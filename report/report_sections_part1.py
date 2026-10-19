# -*- coding: utf-8 -*-
"""
PHẦN 1: TRANG BÌA, MỤC LỤC CHUẨN MẪU ẢNH, DANH MỤC, MỞ ĐẦU, CHƯƠNG 1 VÀ CHƯƠNG 2
Đề tài: PHÂN TÍCH CHẤT LƯỢNG MẠNG VIỄN THÔNG (CTKU122 - HUNRE)
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT

from build_baocao2_reformatted import (
    add_p, add_bullet, add_h1, add_h2, add_h3, add_tbl, add_fig, add_code, add_callout, add_toc_item
)

# ==============================================================================
# TRANG BÌA, MỤC LỤC, DANH MỤC VÀ LỜI NÓI ĐẦU
# ==============================================================================
def build_frontmatter_and_toc(doc):
    # Cấu hình lề trang theo chuẩn: Trái 3cm, Phải 2cm, Trên 2cm, Dưới 2cm
    for section in doc.sections:
        section.top_margin = Inches(2.0 / 2.54)
        section.bottom_margin = Inches(2.0 / 2.54)
        section.left_margin = Inches(3.0 / 2.54)
        section.right_margin = Inches(2.0 / 2.54)

    # 1. CẬP NHẬT TRANG BÌA & BẢNG THÔNG TIN MẪU
    doc.paragraphs[6].text = "ĐỀ TÀI SỐ 01"
    doc.paragraphs[6].runs[0].font.name = "Times New Roman"
    doc.paragraphs[6].runs[0].font.size = Pt(14)
    doc.paragraphs[6].runs[0].font.bold = True

    doc.paragraphs[7].text = "XÂY DỰNG HỆ THỐNG PHÂN TÍCH VÀ GIÁM SÁT CHẤT LƯỢNG MẠNG VIỄN THÔNG (TELECOM QUALITY OF SERVICE ANALYTICS) TRÊN NỀN TẢNG HADOOP, SPARK VÀ R"
    doc.paragraphs[7].runs[0].font.name = "Times New Roman"
    doc.paragraphs[7].runs[0].font.size = Pt(16)
    doc.paragraphs[7].runs[0].font.bold = True
    doc.paragraphs[7].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.paragraphs[8].text = "Lớp học phần: ĐH13C2 - Xử lý Dữ liệu lớn"
    doc.paragraphs[8].runs[0].font.name = "Times New Roman"
    doc.paragraphs[8].runs[0].font.size = Pt(13)

    doc.paragraphs[9].text = "Giảng viên giảng dạy: Trần Thị Hương"
    doc.paragraphs[9].runs[0].font.name = "Times New Roman"
    doc.paragraphs[9].runs[0].font.size = Pt(13)

    # Table 0: Danh sách sinh viên thực hiện
    sv_list = [
        ("1", "211101001", "Hoàng Ngọc Thi (Nhóm trưởng)", "ĐH13C2"),
        ("2", "211101002", "Nguyễn Viết Hoàng Anh", "ĐH13C2"),
        ("3", "211101003", "Nguyễn Việt Hòa", "ĐH13C2"),
        ("4", "211101004", "Nguyễn Quốc Anh", "ĐH13C2"),
    ]
    if len(doc.tables[0].rows) > 5:
        doc.tables[0]._element.remove(doc.tables[0].rows[5]._tr)

    for idx, (tt, msv, hoten, lop) in enumerate(sv_list):
        r_cells = doc.tables[0].rows[idx + 1].cells
        r_cells[0].text, r_cells[1].text, r_cells[2].text, r_cells[3].text = tt, msv, hoten, lop
        for c in r_cells:
            for p in c.paragraphs:
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(11)

    # Table 3: Bảng tổng hợp điểm
    score_sv_list = [
        ("1", "211101001", "Hoàng Ngọc Thi"),
        ("2", "211101002", "Nguyễn Viết Hoàng Anh"),
        ("3", "211101003", "Nguyễn Việt Hòa"),
        ("4", "211101004", "Nguyễn Quốc Anh"),
    ]
    if len(doc.tables[3].rows) > 5:
        doc.tables[3]._element.remove(doc.tables[3].rows[5]._tr)

    for idx, (tt, msv, hoten) in enumerate(score_sv_list):
        r_cells = doc.tables[3].rows[idx + 1].cells
        r_cells[0].text, r_cells[1].text, r_cells[2].text = tt, msv, hoten
        for c in r_cells:
            for p in c.paragraphs:
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(10.5)

    # Table 5: Phân công nhiệm vụ (100% chia đều 25%)
    tasks_list = [
        ("1", "211101001", "Hoàng Ngọc Thi", "Quản trị dự án; thiết kế kiến trúc hệ thống Lambda Architecture; thiết lập hạ tầng HDFS và cấu hình Flume Ingestion", "25%"),
        ("2", "211101002", "Nguyễn Viết Hoàng Anh", "Thiết kế & lập trình thuật toán MapReduce Java (Custom Composite Key, Partitioner, Combiner); đóng gói JAR và benchmark YARN", "25%"),
        ("3", "211101003", "Nguyễn Việt Hòa", "Xây dựng pipeline Apache Spark DataFrame & Spark SQL (tối ưu cache/persist); phát triển kịch bản phân cụm dữ liệu với Apache Pig Latin", "25%"),
        ("4", "211101004", "Nguyễn Quốc Anh", "Thiết kế cơ sở dữ liệu NoSQL HBase độ trễ thấp; xây dựng mô hình Học máy Logistic Regression bằng R & SQLite; trực quan hóa và tổng hợp báo cáo", "25%"),
    ]
    if len(doc.tables[5].rows) > 5:
        doc.tables[5]._element.remove(doc.tables[5].rows[5]._tr)

    for idx, (tt, msv, hoten, nv, tl) in enumerate(tasks_list):
        r_cells = doc.tables[5].rows[idx + 1].cells
        r_cells[0].text, r_cells[1].text, r_cells[2].text, r_cells[3].text, r_cells[4].text = tt, msv, hoten, nv, tl
        for c in r_cells:
            for p in c.paragraphs:
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(10.5)

    # Cắt bỏ các đoạn outline mẫu sau Table 5 để điền nội dung toàn diện
    body = doc._body._element
    children = list(body)
    cut_index = -1
    tbl_count = 0
    for i, el in enumerate(children):
        if el.tag.endswith('tbl'):
            tbl_count += 1
            if tbl_count == 6:  # Sau Table 5
                cut_index = i
                break

    for el in children[cut_index + 2:]:
        if el.tag.endswith('sectPr'):
            continue
        body.remove(el)

    # ==========================================================================
    # MỤC LỤC CHUẨN XÁC 100% THEO MẪU HÌNH ẢNH
    # ==========================================================================
    doc.add_page_break()
    p_toc_title = doc.add_paragraph()
    p_toc_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc_title.paragraph_format.space_before = Pt(12)
    p_toc_title.paragraph_format.space_after = Pt(14)
    r_toc = p_toc_title.add_run("MỤC LỤC")
    r_toc.font.name = "Times New Roman"
    r_toc.font.size = Pt(16)
    r_toc.font.bold = True
    r_toc.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    toc_entries = [
        ("MỞ ĐẦU", 5, 1),
        ("1. Lý do chọn đề tài", 5, 2),
        ("2. Mục tiêu nghiên cứu", 6, 2),
        ("3. Đối tượng và phạm vi nghiên cứu", 7, 2),
        ("4. Phương pháp thực hiện", 8, 2),
        ("5. Cấu trúc báo cáo", 10, 2),
        ("CHƯƠNG 1: TỔNG QUAN BÀI TOÁN VÀ CÔNG CỤ XỬ LÝ DỮ LIỆU LỚN", 13, 1),
        ("1.1 Bối cảnh bài toán và đặc trưng 5V của dữ liệu mạng viễn thông", 13, 2),
        ("1.1.1 Bối cảnh và mục tiêu bài toán phân tích chất lượng mạng viễn thông (QoS)", 13, 3),
        ("1.1.2 Phân tích đặc trưng 5V (Volume, Velocity, Variety, Veracity, Value)", 13, 3),
        ("1.1.3 Phân loại dữ liệu (Structured, Semi-structured, Streaming)", 15, 3),
        ("1.1.4 Xác định phương pháp xử lý (Batch Processing vs. Streaming/Near Real-Time)", 15, 3),
        ("1.2 Kiến trúc tổng quan và sơ đồ luồng dữ liệu (Data Pipeline)", 16, 2),
        ("1.3 Giới thiệu chi tiết các công cụ trong hệ thống", 18, 2),
        ("1.3.1 Nguồn dữ liệu (CSV, Syslog, SQLite)", 18, 3),
        ("1.3.2 Apache Flume", 18, 3),
        ("1.3.3 Hadoop HDFS và YARN", 19, 3),
        ("1.3.4 Apache Pig (Pig Latin)", 20, 3),
        ("1.3.5 Hadoop MapReduce", 20, 3),
        ("1.3.6 Apache Spark (DataFrame, Spark SQL)", 21, 3),
        ("1.3.7 Apache HBase", 21, 3),
        ("1.3.8 Mô phỏng BigSheets bằng Spark", 22, 3),
        ("1.3.9 Ngôn ngữ R và CSDL SQLite (DBI, RSQLite, dplyr, ggplot2)", 22, 3),
        ("1.3.10 Python và Matplotlib Dashboard", 22, 3),
        ("1.3.11 Định dạng Parquet và Power BI", 23, 3),

        ("CHƯƠNG 2. DỮ LIỆU VÀ QUY TRÌNH TIỀN XỬ LÝ", 24, 1),
        ("2.1 Nguồn dữ liệu, quy mô và cấu trúc thuộc tính", 24, 2),
        ("2.1.1 Bảng sự kiện đo kiểm KPI viễn thông (network_kpi_events.csv)", 25, 3),
        ("2.1.2 Danh mục trạm BTS (bts_towers.csv) và cấu hình Cell (cells_catalog.csv)", 25, 3),
        ("2.1.3 Luồng sự kiện mô phỏng (bts_syslog.log / network_kpi_events)", 26, 3),
        ("2.1.4 Cơ sở dữ liệu quan hệ đối chiếu (telecom_network.sqlite / customer_complaints.csv)", 27, 3),
        ("2.2 Đánh giá chất lượng dữ liệu và các cờ cảnh báo (quality_flag)", 28, 2),
        ("2.3 Quy trình tiền xử lý và làm sạch dữ liệu (Data Cleaning & Normalization)", 29, 2),

        ("CHƯƠNG 3. XÂY DỰNG HỆ THỐNG XỬ LÝ DỮ LIỆU LỚN", 32, 1),
        ("3.1 Cấu hình và thu nạp dữ liệu bằng Apache Flume", 32, 2),
        ("3.1.1 Kịch bản 1: Thu nạp dữ liệu lô CSV (Spooling Directory & FileChannel)", 32, 3),
        ("3.1.2 Kịch bản 2: Thu nạp luồng sự kiện thời gian thực (Netcat & MemoryChannel)", 35, 3),
        ("3.2 Lưu trữ và tổ chức dữ liệu trên HDFS", 38, 2),
        ("3.2.1 Thiết kế 4 vùng dữ liệu HDFS (Raw, Staging, Curated, Output)", 38, 3),
        ("3.2.2 Cấu trúc phân vùng dữ liệu (Partitioning by Year/Month/Day/Technology)", 39, 3),
        ("3.2.3 Tính toán dung lượng lưu trữ với hệ số nhân bản (Replication Factor = 3)", 39, 3),
        ("3.2.4 Vai trò của NameNode, DataNode, YARN và cơ chế chịu lỗi (Fault Tolerance)", 40, 3),
        ("3.3 Xử lý và tổng hợp dữ liệu bằng Pig Latin", 41, 2),
        ("3.3.1 Kịch bản Pig Latin chi tiết (LOAD, SPLIT, FILTER, JOIN, GROUP, FOREACH, STORE)", 41, 3),
        ("3.3.2 Minh họa kết quả thực thi và giải thích các hàm tổng hợp", 43, 3),
        ("3.4 Thiết kế thuật toán MapReduce tính KPI, thông lượng, độ trễ và tỷ lệ rớt cuộc gọi", 44, 2),
        ("3.4.1 Xác định các cặp Key - Value (Input, Map Output, Reducer Output)", 44, 3),
        ("3.4.2 Thiết kế Combiner, Custom Partitioner và Shuffle & Sort", 46, 3),
        ("3.4.3 Mã giả thuật toán và các kịch bản kiểm thử (Test Cases)", 47, 3),
        ("3.5 Pipeline phân tích chỉ số KPI và phát hiện trạm suy hao/nguy cơ rớt mạng bằng Apache Spark", 48, 2),
        ("3.5.1 Quy trình xử lý PySpark DataFrame và Spark SQL", 48, 3),
        ("3.5.2 Phân tích chỉ số KPI, làm sạch dữ liệu và liên kết danh mục", 49, 3),
        ("3.5.3 Thống kê xếp hạng trạm suy hao và phân loại cảnh báo quá tải vô tuyến", 50, 3),
        ("3.6 Thiết kế CSDL NoSQL Apache HBase phục vụ truy cập ngẫu nhiên", 52, 2),
        ("3.6.1 Cấu trúc RowKey tối ưu (reverse(tower_id)#technology#timestamp)", 52, 3),
        ("3.6.2 Định nghĩa Column Families (kpi_metrics, cell_info, status_flags) và Versioning", 53, 3),
        ("3.6.3 Lệnh thao tác Shell (create, put, get, scan, delete)", 54, 3),
        ("3.6.4 Cấu hình nâng cao: Pre-splitting, TTL, Compression và Backup Snapshot", 55, 3),

        ("CHƯƠNG 4. KẾT QUẢ VÀ ĐÁNH GIÁ", 58, 1),
        ("4.1 Mô phỏng quy trình BigSheets bằng Spark DataFrame & Trực quan hóa Dashboard", 58, 2),
        ("4.2 Phân tích chuyên sâu bằng R, SQL JOIN/GROUP BY và SQLite", 61, 2),
        ("4.2.1 Liên kết bảng network_kpi_events, bts_towers, cells_catalog, customer_complaints trong SQLite", 61, 3),
        ("4.2.2 Đánh giá mô hình Logistic dự báo khiếu nại và phân bố QoS theo công nghệ và trạm BTS", 62, 3),
        ("4.2.3 Xuất biểu đồ ggplot2 và ghi kết quả trở lại SQLite", 63, 3),
        ("4.3 Tổng hợp kết quả kinh doanh/nghiệp vụ từ bộ dữ liệu gốc", 71, 2),
        ("4.3.1 Bảng đối soát số liệu (12.000 phiên đo kiểm hợp lệ, 85 trạm BTS, 340 cells)", 71, 3),
        ("4.3.2 Xếp hạng 8 trạm phát sóng suy giảm chất lượng nặng nề nhất (Top Worst Towers)", 73, 3),
        ("4.3.3 Phân bố chất lượng dịch vụ (Tốt, Khá, Kém) và cảnh báo trạm suy hao/quá tải", 78, 3),
        ("4.4 Đánh giá Pig, MapReduce và Spark", 78, 2),
        ("4.5 Khuyến nghị căn cứ trên kết quả", 79, 2),

        ("CHƯƠNG 5. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", 80, 1),
        ("5.1 Kết luận các kết quả đạt được của hệ thống", 80, 2),
        ("5.2 Hạn chế còn tồn tại", 81, 2),
        ("5.3 Hướng phát triển và mở rộng đề tài (Kafka, Spark Streaming, Machine Learning)", 83, 2),
        ("KẾT LUẬN", 85, 1),
        ("TÀI LIỆU THAM KHẢO", 86, 1),
        ("PHỤ LỤC", 88, 1),
        ("Phụ lục A: Hướng dẫn cài đặt và vận hành hệ thống", 88, 2),
        ("Phụ lục B: Trích đoạn mã nguồn cốt lõi", 90, 2),
        ("Phụ lục C: Nhật ký thực thi và ảnh chụp màn hình kiểm chứng", 94, 2),
    ]

    for title, pg, lvl in toc_entries:
        add_toc_item(doc, title, pg, lvl)

    # DANH MỤC HÌNH VẼ
    doc.add_page_break()
    add_h1(doc, "DANH MỤC HÌNH VẼ")
    figures_list = [
        ("Hình 1.1", "Sơ đồ kiến trúc tổng thể hệ thống (Lambda Architecture)", 16),
        ("Hình 2.1", "Sơ đồ thực thể quan hệ dữ liệu viễn thông (ERD Schema)", 27),
        ("Hình 3.1", "Pipeline luồng dữ liệu đầu cuối từ Ingestion đến Analytics", 33),
        ("Hình 3.2", "Sơ đồ luồng thuật toán MapReduce với Composite Key và Custom Partitioner", 46),
        ("Hình 4.1", "Giao diện mô phỏng Dashboard phân tích nghiệp vụ BigSheets", 59),
        ("Hình 4.2", "Ảnh chụp màn hình môi trường thực thi và phân tích mô hình học máy trên RStudio", 64),
        ("Hình 4.3", "Biểu đồ hộp phân bố độ trễ theo thế hệ công nghệ mạng (3G, 4G, 5G)", 74),
        ("Hình 4.4", "Biểu đồ tương quan giữa Tỷ lệ mất gói (%) và Tỷ lệ rớt cuộc gọi (%)", 75),
        ("Hình 4.5", "Biểu đồ tỷ lệ rớt cuộc gọi theo Tỉnh thành và Công nghệ mạng", 76),
        ("Hình 4.6", "Biểu đồ bong bóng đa chiều tương quan Độ trễ và Mất gói theo Trạm BTS", 77),
        ("Hình 4.7", "Biểu đồ xếp hạng cảnh báo Top 10 trạm BTS chất lượng kém nhất cần bảo trì", 77),
    ]
    for h_id, h_name, h_pg in figures_list:
        add_toc_item(doc, f"{h_id}: {h_name}", h_pg, level=2)

    # DANH MỤC BẢNG BIỂU
    doc.add_page_break()
    add_h1(doc, "DANH MỤC BẢNG BIỂU")
    tables_list = [
        ("Bảng 2.1", "Khảo sát cấu trúc 4 tập dữ liệu viễn thông thực nghiệm", 25),
        ("Bảng 2.2", "Ma trận rủi ro và phương án xử lý chất lượng dữ liệu đo kiểm", 28),
        ("Bảng 3.1", "Thiết kế bảng Apache HBase lưu trữ chỉ số KPI viễn thông độ trễ thấp", 53),
        ("Bảng 4.1", "Bảng tổng hợp KPI Top 10 trạm phát sóng suy giảm chất lượng nghiêm trọng", 72),
        ("Bảng 4.2", "Bảng đối chiếu định lượng hiệu năng và tài nguyên giữa Pig, MapReduce, Spark và R", 78),
        ("Bảng 4.3", "Ma trận 5 khuyến nghị hành động kỹ thuật tối ưu hóa mạng viễn thông", 79),
    ]
    for b_id, b_name, b_pg in tables_list:
        add_toc_item(doc, f"{b_id}: {b_name}", b_pg, level=2)

    # DANH MỤC TỪ VIẾT TẮT
    doc.add_page_break()
    add_h1(doc, "DANH MỤC TỪ VIẾT TẮT")
    abbrs = [
        ("BTS", "Base Transceiver Station - Trạm thu phát sóng di động mặt đất"),
        ("CDR / xDR", "Call Detail Record / Data Detail Record - Bản ghi chi tiết cuộc gọi và dữ liệu"),
        ("KPI", "Key Performance Indicator - Chỉ số đo lường hiệu quả hoạt động cốt lõi"),
        ("QoS / QoE", "Quality of Service / Quality of Experience - Chất lượng dịch vụ và trải nghiệm người dùng"),
        ("SLA", "Service Level Agreement - Cam kết chất lượng dịch vụ"),
        ("HDFS", "Hadoop Distributed File System - Hệ thống tệp phân tán Hadoop"),
        ("YARN", "Yet Another Resource Negotiator - Hệ thống quản lý tài nguyên phân tán Hadoop"),
        ("RDD", "Resilient Distributed Dataset - Tập dữ liệu phân tán có khả năng phục hồi"),
        ("NoSQL", "Not Only SQL - Cơ sở dữ liệu phi quan hệ phân tán"),
        ("SON", "Self-Organizing Networks - Mạng tự tối ưu hóa vô tuyến"),
        ("NOC / SOC", "Network Operations Center / Service Operations Center - Trung tâm điều hành mạng và dịch vụ"),
        ("MEC", "Multi-access Edge Computing - Tính toán biên đa truy cập"),
        ("AQM / WRED", "Active Queue Management / Weighted Random Early Detection - Kiểm soát hàng đợi chủ động"),
    ]
    for ab, desc in abbrs:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        r_a = p.add_run(f"{ab:<12} : ")
        r_a.font.name = "Times New Roman"
        r_a.font.size = Pt(12)
        r_a.font.bold = True
        r_d = p.add_run(desc)
        r_d.font.name = "Times New Roman"
        r_d.font.size = Pt(12)

    # MỞ ĐẦU
    doc.add_page_break()
    add_h1(doc, "MỞ ĐẦU")

    add_h2(doc, "1. Lý do chọn đề tài")
    add_p(doc, "Trong kỷ nguyên bùng nổ của cuộc Cách mạng Công nghiệp lần thứ tư và công cuộc chuyển đổi số toàn diện, ngành công nghiệp viễn thông di động đóng vai trò là mạch máu thông tin huyết mạch của toàn bộ nền kinh tế số. Sự phát triển vũ bão của các mạng di động băng rộng thế hệ thứ tư (4G LTE), thế hệ thứ năm (5G NR), kết hợp cùng sự gia tăng đột biến của hàng triệu thiết bị Internet vạn vật (IoT), xe tự hành và các dịch vụ nội dung số độ phân giải cao (Video Streaming 4K/8K, hội nghị truyền hình trực tuyến, game thực tế ảo VR/AR) đã tạo ra áp lực lưu lượng chưa từng có đối với hạ tầng mạng vô tuyến tế bào của các nhà khai thác viễn thông.")
    add_p(doc, "Tại Việt Nam, một mạng viễn thông quy mô quốc gia thông thường quản lý từ 30.000 đến hơn 60.000 trạm phát sóng di động (Base Transceiver Station - BTS) trải dài trên khắp 63 tỉnh, thành phố. Mỗi trạm BTS gồm từ 3 đến 6 sector cell vô tuyến phát sóng liên tục ghi nhận các dòng dữ liệu đo kiểm telemetry, bản ghi chi tiết cuộc gọi (Call Detail Record - CDR), bản ghi phiên dữ liệu (Data Detail Record - xDR) và nhật ký hoạt động hệ thống (Syslog) với tần suất hàng trăm nghìn sự kiện mỗi giây. Khối lượng dữ liệu thô sinh ra dao động từ 10 đến 25 Terabyte mỗi ngày, mang đầy đủ các đặc trưng kinh điển của Dữ liệu lớn (Big Data 5V): Khối lượng khổng lồ (Volume), Tốc độ sinh và truyền tức thời (Velocity), Đa dạng về chủng loại định dạng (Variety), Độ nhiễu và bất định cao (Veracity), cùng tiềm năng khai thác Giá trị to lớn (Value).")
    add_p(doc, "Trong môi trường cạnh tranh khốc liệt hiện nay, chất lượng dịch vụ (Quality of Service - QoS) và chất lượng trải nghiệm của khách hàng (Quality of Experience - QoE) là yếu tố sống còn quyết định sự thành bại và thương hiệu của nhà mạng. Các sự cố nghẽn mạng, suy hao truyền dẫn Backhaul hoặc can nhiễu vô tuyến kéo dài không chỉ dẫn đến tình trạng rớt cuộc gọi và chậm mạng mà còn làm gia tăng đột biến các cuộc khiếu nại gay gắt gửi về tổng đài CSKH, đe dọa trực tiếp đến tỷ lệ rời mạng của thuê bao (Churn Rate). Trong khi đó, các hệ thống cơ sở dữ liệu quan hệ truyền thống (RDBMS) hoàn toàn bất lực và sụp đổ trước khối lượng dữ liệu khổng lồ này, không thể mở rộng quy mô linh hoạt và mất hàng giờ để tổng hợp số liệu, khiến Trung tâm Điều hành Mạng (NOC) luôn ở thế bị động.")
    add_p(doc, "Xuất phát từ thực tiễn cấp bách đó, việc ứng dụng các nền tảng xử lý dữ liệu lớn như Apache Hadoop, Apache Spark kết hợp ngôn ngữ phân tích chuyên sâu R là một giải pháp tối ưu và tất yếu. Vì vậy, nhóm nghiên cứu đã lựa chọn thực hiện đề tài: \"Xây dựng hệ thống phân tích và giám sát chất lượng mạng viễn thông (Telecom Quality of Service Analytics) trên nền tảng Hadoop, Spark và R\".")

    add_h2(doc, "2. Mục tiêu nghiên cứu")
    add_p(doc, "Đề tài xác định rõ hệ thống mục tiêu nghiên cứu tổng quát và mục tiêu kỹ thuật cụ thể như sau:", bold_prefix="Định hướng mục tiêu: ")
    add_bullet(doc, "Nghiên cứu, thiết kế và triển khai một hệ thống kỹ nghệ dữ liệu lớn hoàn chỉnh theo Kiến trúc Lambda (Lambda Architecture), tích hợp luồng xử lý lô (Batch Layer) chính xác và luồng tốc độ cao (Speed Layer) tức thời, phục vụ việc thu nạp, lưu trữ, xử lý phân tán và giám sát đa chiều các chỉ số chất lượng dịch vụ (QoS) trên toàn bộ mạng lưới viễn thông di động.", bold_prefix="• Mục tiêu tổng quát: ")
    add_p(doc, "Mục tiêu kỹ thuật và nghiệp vụ cụ thể bao gồm:", bold_prefix="• Mục tiêu cụ thể: ")
    add_bullet(doc, "Xây dựng hạ tầng Data Lake và tầng thu nạp luồng: Ứng dụng Apache Flume để thu nạp dữ liệu đo kiểm lô (Spooling Directory) và luồng sự kiện socket tức thời; tổ chức lưu trữ phân tán 4 vùng trên Hadoop HDFS với hệ số nhân bản RF=3 đảm bảo khả năng chịu lỗi và tính toàn vẹn dữ liệu tuyệt đối.", bold_prefix="1. ")
    add_bullet(doc, "Tối ưu hóa các thuật toán xử lý phân tán quy mô lớn: Thiết kế thuật toán MapReduce Java với Khóa phức hợp (Composite Key) và Bộ phân vùng tùy biến (Custom Partitioner) nhằm triệt tiêu hiện tượng lệch dữ liệu (Data Skew); xây dựng pipeline Apache Spark DataFrame & Spark SQL tận dụng tính toán trong bộ nhớ (In-Memory) và Catalyst Optimizer để tổng hợp đa chiều KPI với tốc độ vượt trội.", bold_prefix="2. ")
    add_bullet(doc, "Giải quyết triệt để 3 bài toán chỉ số viễn thông cốt lõi: (a) Giảm thiểu độ trễ mạng (Latency) qua việc phát hiện chính xác các trạm nghẽn đường truyền Backhaul; (b) Giảm tỷ lệ mất gói (Packet Loss) qua việc cô lập các cell vô tuyến bị can nhiễu đồng kênh; (c) Kéo giảm tỷ lệ rớt cuộc gọi (Call Drop Rate - CDR) về dưới ngưỡng cam kết chất lượng dịch vụ SLA (2.0%).", bold_prefix="3. ")
    add_bullet(doc, "Thiết kế cơ sở dữ liệu NoSQL truy cập ngẫu nhiên độ trễ thấp: Xây dựng bảng Apache HBase với cấu trúc RowKey tối ưu reverse(tower_id)#technology#timestamp, cho phép kỹ sư NOC tra cứu tức thời thông tin trạng thái trạm với độ trễ dưới 10 mili-giây.", bold_prefix="4. ")
    add_bullet(doc, "Ứng dụng Khoa học dữ liệu và Học máy dự báo khiếu nại: Kết nối ngôn ngữ R với CSDL SQLite, huấn luyện mô hình Hồi quy Logistic (Logistic Regression) để lượng hóa xác suất khách hàng khiếu nại dựa trên các tham số mạng, giúp nhà mạng chuyển dịch từ quy trình ứng phó bị động sang chăm sóc khách hàng chủ động.", bold_prefix="5. ")
    add_bullet(doc, "Mô phỏng quy trình bảng tính nghiệp vụ và trực quan hóa: Xây dựng ứng dụng Web tương tác mô phỏng 6 bước của IBM BigSheets kết nối Spark, kết xuất các biểu đồ khoa học trực quan (ggplot2, Matplotlib) và bộ số liệu kết nối Power BI Dashboard điều hành.", bold_prefix="6. ")

    add_h2(doc, "3. Đối tượng và phạm vi nghiên cứu")
    add_p(doc, "Để đảm bảo tính khoa học và khả thi, đề tài giới hạn rõ đối tượng và phạm vi nghiên cứu như sau:")
    add_bullet(doc, "Dữ liệu đo kiểm viễn thông và nhật ký hệ thống: Tập dữ liệu đo kiểm phiên telemetry di động (network_kpi_events.csv), danh mục trạm BTS (bts_towers.csv), danh mục cấu hình phần cứng cell (cells_catalog.csv), nhật ký sự kiện trạm (bts_syslog.log) và dữ liệu khiếu nại khách hàng (customer_complaints.csv).", bold_prefix="• Đối tượng dữ liệu: ")
    add_bullet(doc, "Hệ thống chỉ số chất lượng dịch vụ QoS viễn thông: Thông lượng (Throughput - Mbps), Độ trễ mạng (Latency - ms), Tỷ lệ mất gói (Packet Loss - %), Tỷ lệ rớt cuộc gọi (Call Drop Rate - CDR %), Số thuê bao phục vụ đồng thời (Active Users) và Điểm chất lượng dịch vụ tổng hợp (QoS Score).", bold_prefix="• Đối tượng chỉ số viễn thông: ")
    add_bullet(doc, "Hệ sinh thái công nghệ dữ liệu lớn: Apache Hadoop (HDFS, YARN), Apache Flume, Apache Pig (Pig Latin), Hadoop MapReduce (Java), Apache Spark (PySpark, Spark SQL), Apache HBase NoSQL, IBM BigSheets (mô phỏng), ngôn ngữ R và CSDL SQLite.", bold_prefix="• Đối tượng công nghệ: ")
    add_bullet(doc, "Phạm vi không gian và dữ liệu thực nghiệm: Mô phỏng mạng tế bào vô tuyến tại 3 đô thị trọng điểm của Việt Nam (Hà Nội, TP. Hồ Chí Minh, Đà Nẵng) với 20 trạm BTS đại diện, 80 sector cell thuộc 3 thế hệ mạng (3G WCDMA 2100MHz, 4G LTE 1800/2600MHz, 5G NR 3500MHz). Bộ dữ liệu thực nghiệm gồm 12.001 dòng (12.000 phiên đo kiểm) và 250 bản ghi khiếu nại khách hàng.", bold_prefix="• Phạm vi không gian & dữ liệu: ")
    add_bullet(doc, "Phạm vi môi trường kỹ thuật: Nghiên cứu, cài đặt và thực nghiệm trên môi trường máy chủ cục bộ và cụm phân tán giả lập (Pseudo-distributed / Single-node Cluster), tối ưu hóa cấu hình tài nguyên RAM và CPU; tập trung vào kiến trúc kỹ nghệ dữ liệu đầu cuối từ thu nạp, lưu trữ, tính toán phân tán, mô hình hóa đến trực quan hóa báo cáo.", bold_prefix="• Phạm vi kỹ thuật: ")

    add_h2(doc, "4. Phương pháp thực hiện")
    add_p(doc, "Nhóm nghiên cứu đã kết hợp đồng bộ các phương pháp kỹ nghệ dữ liệu, tính toán phân tán và khoa học dữ liệu hiện đại:")
    add_bullet(doc, "Phương pháp thu thập và làm sạch dữ liệu (Data Ingestion & Cleansing): Sử dụng Apache Flume với cơ chế Spooling Directory Source nạp tệp CSV định kỳ và Netcat Source nhận luồng thời gian thực qua TCP socket. Thiết lập bộ lọc logic xác thực dữ liệu loại bỏ các giá trị dị thường vật lý (độ trễ âm, thông lượng âm, mất gói > 100%, bản ghi mồ côi khuyết khóa ngoại), gắn cờ quality_flag bảo đảm độ sạch 99.6%.", bold_prefix="1. Thu thập & Tiền xử lý: ")
    add_bullet(doc, "Phương pháp kiến trúc hệ thống (Lambda Architecture): Tổ chức hệ thống theo hai luồng song song: Batch Layer (HDFS, MapReduce, Pig, Spark SQL) đảm bảo tính toàn vẹn và độ chính xác cao cho báo cáo SLA dài hạn; Speed Layer và Serving Layer (HBase NoSQL) tiếp nhận luồng sự kiện nóng để cảnh báo trạm suy hao tức thời.", bold_prefix="2. Kiến trúc phân tầng: ")
    add_bullet(doc, "Phương pháp tính toán và xử lý phân tán (Distributed Computing): Hiện thực thuật toán MapReduce thuần Java với Khóa phức hợp WritableComparable và Custom Partitioner; kết hợp xây dựng pipeline PySpark DataFrame và Spark SQL áp dụng Catalyst Optimizer và nén Snappy Parquet, giúp tăng tốc độ tính toán gấp 15 lần so với MapReduce truyền thống.", bold_prefix="3. Tính toán phân tán: ")
    add_bullet(doc, "Phương pháp lưu trữ và truy xuất ngẫu nhiên NoSQL: Ứng dụng Apache HBase, thiết kế cấu trúc RowKey đảo chuỗi reverse(tower_id)#technology#reverse_timestamp nhằm chống hiện tượng thắt cổ chai ghi tập trung (Write Hotspotting), tối ưu hóa việc đọc/ghi ngẫu nhiên với độ trễ < 10 ms.", bold_prefix="4. Cơ sở dữ liệu NoSQL: ")
    add_bullet(doc, "Phương pháp Khoa học dữ liệu và Mô hình hóa học máy (Data Science & Machine Learning): Sử dụng ngôn ngữ R kết nối CSDL SQLite qua DBI/RSQLite, khai thác gói thư viện tidyverse/dplyr để tổng hợp dữ liệu; xây dựng mô hình Hồi quy Logistic (Logistic Regression) để lượng hóa mối quan hệ giữa các tham số mạng và xác suất khách hàng khiếu nại (p < 0.001); trực quan hóa biểu đồ phân bố bằng ggplot2.", bold_prefix="5. Khoa học dữ liệu & ML: ")
    add_bullet(doc, "Phương pháp mô phỏng bảng tính nghiệp vụ No-Code (Spreadsheet Analytics): Xây dựng ứng dụng Web tương tác mô phỏng 6 bước thao tác của IBM BigSheets, liên kết chặt chẽ với động cơ Spark DataFrame phía sau.", bold_prefix="6. Mô phỏng nghiệp vụ: ")

    add_h2(doc, "5. Cấu trúc báo cáo")
    add_p(doc, "Báo cáo bài tập lớn được trình bày mạch lạc thành 5 chương nội dung chính, phần kết luận, tài liệu tham khảo và các phụ lục kỹ thuật:")
    add_bullet(doc, "Chương 1: Tổng quan bài toán và công cụ xử lý dữ liệu lớn - Giới thiệu bối cảnh viễn thông, phân tích đặc trưng 5V, phân loại dữ liệu, xác định phương pháp xử lý lô và thời gian thực, thiết kế kiến trúc tổng thể Lambda Architecture và tổng quan chi tiết 11 công nghệ trong hệ thống.", bold_prefix="• ")
    add_bullet(doc, "Chương 2: Dữ liệu và quy trình tiền xử lý - Khảo sát cấu trúc 4 tập dữ liệu viễn thông thực nghiệm, thiết kế sơ đồ thực thể quan hệ ERD Schema, ma trận rủi ro chất lượng, cơ chế cờ cảnh báo quality_flag và quy trình kỹ thuật tạo đặc trưng (Feature Engineering).", bold_prefix="• ")
    add_bullet(doc, "Chương 3: Xây dựng hệ thống xử lý dữ liệu lớn - Trình bày chi tiết cấu hình thu nạp Flume (2 kịch bản), tổ chức 4 vùng lưu trữ và tính toán dung lượng HDFS (RF=3), kịch bản Pig Latin, thiết kế thuật toán MapReduce Java với Composite Key, pipeline PySpark DataFrame & Spark SQL, và thiết kế NoSQL Apache HBase.", bold_prefix="• ")
    add_bullet(doc, "Chương 4: Kết quả và đánh giá - Trình bày kết quả mô phỏng BigSheets, phân tích chuyên sâu bằng R và mô hình học máy Logistic Regression, bảng đối soát số liệu 12.000 phiên đo kiểm, cô lập Top 8 trạm suy hao nghiêm trọng nhất, bảng đối chiếu định lượng hiệu năng giữa Pig, MapReduce, Spark, R và Ma trận 5 khuyến nghị kỹ thuật gửi NOC.", bold_prefix="• ")
    add_bullet(doc, "Chương 5: Kết luận và hướng phát triển - Đánh giá tổng kết các thành quả kỹ thuật đạt được, phân tích các điểm hạn chế còn tồn tại và đề xuất định hướng phát triển mở rộng hệ thống với Apache Kafka, Apache Flink và Trí tuệ nhân tạo AIOps.", bold_prefix="• ")
    add_bullet(doc, "Phần Kết luận, Tài liệu tham khảo và Phụ lục - Tổng kết ý nghĩa thực tiễn của đề tài; danh mục 10 tài liệu tham khảo chuẩn học thuật; Phụ lục A (Hướng dẫn cài đặt vận hành), Phụ lục B (Trích đoạn mã nguồn cốt lõi) và Phụ lục C (Nhật ký thực thi kiểm chứng).", bold_prefix="• ")


# ==============================================================================
# CHƯƠNG 1: TỔNG QUAN BÀI TOÁN VÀ CÔNG CỤ XỬ LÝ DỮ LIỆU LỚN
# ==============================================================================
def build_chapter_1(doc):
    doc.add_page_break()
    add_h1(doc, "CHƯƠNG 1: TỔNG QUAN BÀI TOÁN VÀ CÔNG CỤ XỬ LÝ DỮ LIỆU LỚN")

    add_h2(doc, "1.1 Bối cảnh bài toán và đặc trưng 5V của dữ liệu mạng viễn thông")

    add_h3(doc, "1.1.1 Bối cảnh và mục tiêu bài toán phân tích chất lượng mạng viễn thông (QoS)")
    add_p(doc, "Trong thời đại số hóa toàn diện, ngành công nghiệp viễn thông đang đóng vai trò là hạ tầng kết nối nền tảng cho sự phát triển của xã hội số và kinh tế số. Sự chuyển dịch mạnh mẽ từ các dịch vụ thoại/SMS truyền thống sang các dịch vụ dữ liệu băng rộng tốc độ cao (Data Services) như video streaming độ phân giải cao 4K/8K, điện toán đám mây, hội nghị truyền hình trực tuyến, game thực tế ảo và xe tự hành đã tạo nên một làn sóng bùng nổ lưu lượng truy cập trên các mạng vô tuyến di động.")
    add_p(doc, "Một doanh nghiệp viễn thông tiêu biểu tại Việt Nam quản lý từ 30,000 đến hơn 60,000 trạm BTS phân bố trải dài trên khắp 63 tỉnh thành cả nước. Mỗi trạm phát sóng bao gồm từ 3 đến 6 cell vô tuyến phủ sóng ở các dải tần số khác nhau (900 MHz, 1800 MHz, 2100 MHz, 2600 MHz) phục vụ đồng thời hàng triệu thuê bao di động. Tại mỗi cell, các cảm biến phần cứng và phần mềm nhúng liên tục đo kiểm và ghi nhận hàng trăm tham số chất lượng dịch vụ (Quality of Service - QoS) theo chu kỳ từng giây.")
    add_p(doc, "Mục tiêu bài toán đặt ra bao gồm: (1) Tự động hóa giám sát chất lượng toàn mạng theo chu kỳ gần thời gian thực; (2) Khoanh vùng chính xác các điểm nóng nghẽn mạng và suy hao đường truyền; (3) Cung cấp công cụ phân tích tương tác trực quan cho các kỹ sư điều hành mạng NOC.")

    add_h3(doc, "1.1.2 Phân tích đặc trưng 5V (Volume, Velocity, Variety, Veracity, Value)")
    add_p(doc, "Dữ liệu vận hành mạng viễn thông tế bào phản ánh trung thực và toàn diện 5 đặc trưng kinh điển của Dữ liệu lớn (Big Data 5V):")
    add_bullet(doc, "Volume phản ánh quy mô dữ liệu khổng lồ. Với một mạng lưới quản lý khoảng 50,000 trạm BTS, mỗi trạm có trung bình 4 cell vô tuyến đo kiểm liên tục theo chu kỳ 5 giây/lần, toàn mạng sinh ra xấp xỉ 3.5 tỷ sự kiện đo kiểm mỗi ngày. Kèm theo đó là hàng trăm triệu bản ghi chi tiết cuộc gọi (CDR) và phiên truy cập Internet (xDR). Khối lượng dữ liệu thô sinh ra dao động từ 10 đến 25 Terabyte mỗi ngày, tích lũy qua các năm lên tới quy mô hàng chục Petabyte.", bold_prefix="1. Volume (Khối lượng dữ liệu khổng lồ): ")
    add_bullet(doc, "Velocity phản ánh tốc độ sinh ra, truyền tải và yêu cầu xử lý dữ liệu cực cao. Dữ liệu từ các trạm BTS được truyền liên tục về máy chủ trung tâm qua các luồng stream thời gian thực với thông lượng vượt mức 500,000 sự kiện/giây vào các khung giờ cao điểm (19h00 - 22h00). Hệ thống giám sát NOC đòi hỏi khả năng tiếp nhận, xử lý và kích hoạt cảnh báo trạm mất sóng hoặc rớt cuộc gọi đột biến trong vòng dưới 1 giây để các kỹ sư kịp thời can thiệp.", bold_prefix="2. Velocity (Tốc độ sinh và truyền dữ liệu tức thời): ")
    add_bullet(doc, "Variety thể hiện ở sự đa dạng phức tạp về nguồn gốc và định dạng dữ liệu. Hệ sinh thái viễn thông là sự pha trộn của nhiều công nghệ mạng (2G/3G kế thừa, 4G LTE băng rộng, 5G độ trễ cực thấp) đến từ nhiều nhà cung cấp phần cứng khác nhau (Ericsson, Huawei, Nokia, ZTE). Định dạng dữ liệu bao gồm: dữ liệu có cấu trúc (bảng danh mục trạm BTS, danh mục cell, tọa độ GPS), dữ liệu bán cấu trúc (file nhật ký Syslog chuẩn RFC-5424, file cấu hình tham số vô tuyến định dạng XML/JSON), và dữ liệu luồng phi cấu trúc (luồng gói tin NetFlow/IPFIX, telemetry đo kiểm lớp vật lý).", bold_prefix="3. Variety (Đa dạng về chủng loại và định dạng dữ liệu): ")
    add_bullet(doc, "Veracity thể hiện tính xác thực, độ tin cậy và mức độ nhiễu của dữ liệu. Do tín hiệu vô tuyến truyền lan trong môi trường không gian tự do chịu ảnh hưởng nặng nề bởi thời tiết mưa bão, che chắn địa hình đô thị, can nhiễu đồng kênh và suy hao đa đường (multipath fading), dữ liệu đo kiểm viễn thông thường xuyên xuất hiện các giá trị ngoại lai dị thường (outliers). Bên cạnh đó, hiện tượng lệch xung đồng hồ NTP giữa trạm BTS và máy chủ trung tâm có thể dẫn đến các bản ghi đo kiểm có độ trễ âm hoặc thông lượng âm vô lý. Khâu làm sạch và xác thực dữ liệu là điều kiện tiên quyết trước khi đưa vào tính toán KPI.", bold_prefix="4. Veracity (Tính xác thực và độ nhiễu của dữ liệu): ")
    add_bullet(doc, "Value là giá trị kinh tế và vận hành to lớn mà hệ thống mang lại. Khai thác hiệu quả nguồn dữ liệu này giúp nhà mạng: (1) Nâng cao chất lượng trải nghiệm mạng QoE cho người dùng; (2) Kéo giảm tỷ lệ rời mạng của thuê bao (Churn Reduction); (3) Chủ động chăm sóc khách hàng trước khi phát sinh khiếu nại gay gắt; (4) Tối ưu hóa chi phí đầu tư vốn (CAPEX/OPEX) bằng cách chỉ nâng cấp đúng các trạm bị nghẽn thực sự.", bold_prefix="5. Value (Giá trị nghiệp vụ và kinh tế cốt lõi): ")

    add_h3(doc, "1.1.3 Phân loại dữ liệu (Structured, Semi-structured, Streaming)")
    add_p(doc, "Để xử lý hiệu quả nguồn tài nguyên Big Data trong viễn thông, việc phân loại dữ liệu theo cấu trúc hình học và đặc tính luồng dữ liệu là tiền đề quan trọng:")
    add_bullet(doc, "Dữ liệu có cấu trúc (Structured Data): Là các tập dữ liệu có lược đồ (schema) cố định, định dạng bảng rõ ràng và tuân thủ các ràng buộc toàn vẹn khóa chính - khóa ngoại. Điển hình gồm: Bảng danh mục trạm BTS (bts_towers.csv), Bảng danh mục các sector cell vô tuyến (cells_catalog.csv), và Bảng quản lý khiếu nại khách hàng (customer_complaints.csv). Dữ liệu này được lưu trữ trong các cơ sở dữ liệu quan hệ quản lý tài sản viễn thông (RDBMS Inventory) và được đồng bộ định kỳ vào Data Lake.", bold_prefix="1. Dữ liệu có cấu trúc: ")
    add_bullet(doc, "Dữ liệu bán cấu trúc (Semi-structured Data): Là dữ liệu không tuân theo lược đồ bảng cứng nhắc nhưng có cấu trúc tự mô tả nội tại (self-describing structure) thông qua các thẻ hoặc cặp khóa-giá trị. Điển hình là: File nhật ký hệ thống của trạm BTS (bts_syslog.log theo chuẩn RFC-5424) chứa thông tin tiến trình nhúng và mức độ cảnh báo (Severity Level); Các tệp cấu hình tham số vô tuyến định dạng XML/JSON (ran_config.xml) mô tả góc ngửa anten (antenna tilt), công suất phát (power_dbm) và ngưỡng chuyển giao (handover_margin_db).", bold_prefix="2. Dữ liệu bán cấu trúc: ")
    add_bullet(doc, "Dữ liệu luồng đo kiểm (Streaming Telemetry Data): Là dòng dữ liệu phiên đo kiểm chất lượng mạng (network_kpi_events) sinh ra từ các giao diện vô tuyến với tần suất đo 1s - 5s trên từng cell. Dữ liệu này mang tính chất biến động liên tục theo chuỗi thời gian (Time-series Stream), chứa các chỉ số đo kiểm lớp vật lý và phiên người dùng: thông lượng (throughput_mbps), độ trễ (latency_ms), tỷ lệ mất gói (packet_loss_pct), cờ rớt cuộc gọi (call_dropped) và số người dùng đồng thời (num_active_users).", bold_prefix="3. Dữ liệu luồng: ")

    add_h3(doc, "1.1.4 Xác định phương pháp xử lý (Batch Processing vs. Streaming/Near Real-Time)")
    add_p(doc, "Hệ thống phân định ranh giới xử lý rành mạch giữa hai mô hình điện toán bổ trợ nhau:")
    add_bullet(doc, "Xử lý gần thời gian thực (Near Real-Time - Độ trễ < 1s đến 5s): Áp dụng cho các cảnh báo khẩn cấp, phát hiện trạm mất sóng đột ngột (outage), bão lưu lượng (flash crowds), rớt cuộc gọi tăng vọt > 5%, kích hoạt mạng tự tối ưu (SON) và cân bằng tải động. Công nghệ sử dụng: Flume, Kafka, Spark Streaming và Apache HBase NoSQL.", bold_prefix="• Phân hệ Gần thời gian thực: ")
    add_bullet(doc, "Phân tích tĩnh theo lô (Batch Processing - Chu kỳ giờ/ngày/tuần): Áp dụng cho báo cáo SLA toàn diện, đánh giá xu hướng suy thoái phần cứng, phân tích đối soát khiếu nại, quy hoạch năng lực trạm (capacity planning) và huấn luyện mô hình Machine Learning. Công nghệ sử dụng: Hadoop HDFS, MapReduce, Pig Latin, Spark SQL, BigSheets và R Studio.", bold_prefix="• Phân hệ Xử lý theo lô: ")

    add_h2(doc, "1.2 Kiến trúc tổng quan và sơ đồ luồng dữ liệu (Data Pipeline)")
    add_p(doc, "Hệ thống được thiết kế dựa trên mô hình Kiến trúc Lambda (Lambda Architecture) chuẩn mực trong kỹ nghệ dữ liệu lớn, phối hợp luồng xử lý lô (Batch Layer) chính xác và luồng tốc độ cao (Speed Layer) tức thời.")

    add_fig(
        doc,
        img_name="hinh_1_1_kien_truc_tong_the.png",
        caption="Hình 1.1: Sơ đồ kiến trúc tổng thể hệ thống (Lambda Architecture)",
        width_in=6.5
    )

    add_p(doc, "Kiến trúc hệ thống bao gồm 5 phân tầng chức năng liên hoàn thể hiện trong Hình 1.1:", bold_prefix="Phân tích kiến trúc Hình 1.1: ")
    add_bullet(doc, "Tầng Nguồn dữ liệu (Data Sources Layer): Tiếp nhận luồng dữ liệu thô đa dạng từ hơn 50,000 trạm BTS vô tuyến 3G/4G/5G, các bản ghi cước phiên CDR/xDR và dữ liệu phản ánh khiếu nại từ hệ thống Chăm sóc khách hàng CRM.")
    add_bullet(doc, "Tầng Thu thập & Lưu trữ (Ingestion & Storage Layer): Apache Flume đóng vai trò là cổng thu nhận trung tâm, sử dụng FileChannel bền vững để nạp dữ liệu an toàn vào kho lưu trữ phân tán Hadoop HDFS (Data Lake) với kích thước khối 128 MB và hệ số nhân bản 3 lần.")
    add_bullet(doc, "Tầng Tính toán (Compute Layer): Chia làm hai nhánh xử lý song song. Nhánh Batch Layer vận hành các tác vụ MapReduce Java, Pig Latin và Spark Batch chạy định kỳ theo giờ/ngày để tính toán các chỉ số KPI dài hạn. Nhánh Speed Layer sử dụng Spark Streaming tiếp nhận luồng sự kiện nóng để phát hiện cell nghẽn tức thời.")
    add_bullet(doc, "Tầng Phục vụ (Serving Layer): Apache HBase NoSQL lưu trữ các chỉ số KPI thời gian thực phục vụ truy vấn ngẫu nhiên độ trễ thấp (< 10 ms). Cơ sở dữ liệu SQLite lưu trữ dữ liệu tổng hợp phục vụ các mô hình phân tích R.")
    add_bullet(doc, "Tầng Báo cáo & Phân tích (Analytics & BI Layer): Cung cấp giao diện BigSheets Dashboard tương tác cho người dùng nghiệp vụ và môi trường RStudio cho các nhà khoa học dữ liệu huấn luyện mô hình dự báo khiếu nại.")

    add_callout(
        doc,
        "Ý nghĩa kỹ thuật của Kiến trúc Lambda trong đề tài",
        "Kiến trúc Lambda giúp hệ thống giải quyết đồng thời hai bài toán tưởng chừng mâu thuẫn: xử lý hàng Terabyte dữ liệu lịch sử với độ chính xác tuyệt đối (thông qua Spark/MapReduce) nhưng vẫn duy trì khả năng cảnh báo sự cố viễn thông tức thời với độ trễ dưới 1 giây (thông qua HBase/Speed Layer)."
    )

    add_h2(doc, "1.3 Giới thiệu chi tiết các công cụ trong hệ thống")
    add_p(doc, "Hệ thống tích hợp một chuỗi công cụ Big Data hoàn chỉnh, phân bổ chính xác theo từng giai đoạn xử lý:")

    add_h3(doc, "1.3.1 Nguồn dữ liệu (CSV, Syslog, SQLite)")
    add_p(doc, "Nguồn dữ liệu đầu vào bao gồm: tệp CSV chuẩn hóa chứa số liệu đo kiểm và danh mục thiết bị vô tuyến; tệp nhật ký sự kiện bts_syslog.log chuẩn RFC-5424; và cơ sở dữ liệu quan hệ cục bộ SQLite (telecom_network.sqlite) dùng làm kho đối chiếu cấu hình và thông tin khiếu nại khách hàng.")

    add_h3(doc, "1.3.2 Apache Flume")
    add_p(doc, "Apache Flume là hệ thống phân tán chuyên dụng để thu nạp và tổng hợp dữ liệu nhật ký luồng vào HDFS. Hoạt động theo cơ chế Source - Channel - Sink với mô hình giao dịch 2 pha (Two-Phase Commit), bảo đảm không bao giờ mất mát sự kiện đo kiểm ngay cả khi máy chủ gặp sự cố sập nguồn.")

    add_h3(doc, "1.3.3 Hadoop HDFS và YARN")
    add_p(doc, "Hệ thống tệp phân tán HDFS (Hadoop Distributed File System) đóng vai trò kho lưu trữ trung tâm (Data Lake). HDFS chia tệp thành các khối 128 MB và nhân bản 3 lần (Replication Factor = 3). Hệ thống YARN (Yet Another Resource Negotiator) điều phối và cấp phát động tài nguyên tính toán (CPU, RAM) cho các Container thực thi.")

    add_h3(doc, "1.3.4 Apache Pig (Pig Latin)")
    add_p(doc, "Apache Pig cung cấp môi trường xử lý luồng dữ liệu cấp cao với ngôn ngữ khai báo Pig Latin. Pig biên dịch các câu lệnh thành chuỗi đồ thị có hướng (DAG) MapReduce ngầm định, giúp rút ngắn thời gian phát triển kịch bản trích xuất, biến đổi và lọc dữ liệu (ETL).")

    add_h3(doc, "1.3.5 Hadoop MapReduce")
    add_p(doc, "Mô hình tính toán phân tán MapReduce (Java) chuẩn mực của Hadoop được áp dụng cho các tác vụ xử lý lô quy mô lớn chạy qua đêm. Trong đề tài, thuật toán được tùy biến nâng cao với Khóa phức hợp (Composite Key), Bộ phân vùng tùy biến (Custom Partitioner) và Bộ gộp cục bộ (Combiner) để triệt tiêu hiện tượng lệch dữ liệu (Data Skew).")

    add_h3(doc, "1.3.6 Apache Spark (DataFrame, Spark SQL)")
    add_p(doc, "Apache Spark là động cơ tính toán phân tán In-Memory thế hệ mới. Nhờ trình tối ưu hóa truy vấn Catalyst Optimizer và động cơ sinh mã bytecode nhị phân Tungsten Engine, Spark DataFrame và Spark SQL thực thi các phép biến đổi, Join đa bảng và tính toán thống kê KPI nhanh hơn MapReduce truyền thống từ 10 đến 50 lần.")

    add_h3(doc, "1.3.7 Apache HBase")
    add_p(doc, "Apache HBase là hệ quản trị cơ sở dữ liệu NoSQL phân tán hướng cột, vận hành trên nền HDFS. HBase tổ chức dữ liệu theo cây cấu trúc LSM-Tree và bộ nhớ đệm MemStore/BlockCache, mang lại khả năng truy cập ngẫu nhiên hàng triệu bản ghi theo RowKey với độ trễ cực thấp (< 10 ms).")

    add_h3(doc, "1.3.8 Mô phỏng BigSheets bằng Spark")
    add_p(doc, "IBM BigSheets là giải pháp phân tích dữ liệu lớn trên giao diện bảng tính (Spreadsheet No-Code). Đề tài xây dựng một ứng dụng Web tương tác mô phỏng toàn diện quy trình BigSheets 6 bước và ánh xạ tương đương 1-1 với các thao tác Spark DataFrame (Collection -> DataFrame, Filter Sheet -> filter, Group Sheet -> groupBy).")

    add_h3(doc, "1.3.9 Ngôn ngữ R và CSDL SQLite (DBI, RSQLite, dplyr, ggplot2)")
    add_p(doc, "Ngôn ngữ R kết hợp cơ sở dữ liệu SQLite đảm nhiệm khâu Khoa học dữ liệu chuyên sâu: kết nối CSDL qua DBI/RSQLite, tiền xử lý qua dplyr/tidyr, huấn luyện mô hình Học máy Hồi quy Logistic (Logistic Regression) dự báo nguy cơ khiếu nại khách hàng và xuất đồ thị trực quan bằng ggplot2.")

    add_h3(doc, "1.3.10 Python và Matplotlib Dashboard")
    add_p(doc, "Python đóng vai trò là ngôn ngữ gắn kết linh hoạt toàn bộ hệ thống, từ điều phối pipeline PySpark, xử lý chuyển đổi dữ liệu đến tự động sinh các biểu đồ trực quan hóa chuyên sâu (Boxplot phân bố độ trễ, Bubble chart tương quan đa chiều) bằng Matplotlib và Seaborn.")

    add_h3(doc, "1.3.11 Định dạng Parquet và Power BI")
    add_p(doc, "Dữ liệu sau khi xử lý sạch được lưu trữ dưới định dạng cột Snappy Parquet (tiết kiệm 65% dung lượng lưu trữ so với CSV) và xuất ra tệp telecom_kpi_summary_powerbi.csv để kết nối trực tiếp vào phần mềm Microsoft Power BI, phục vụ xây dựng Dashboard điều hành cho Ban Giám đốc và Trung tâm NOC.")


# ==============================================================================
# CHƯƠNG 2: DỮ LIỆU VÀ QUY TRÌNH TIỀN XỬ LÝ
# ==============================================================================
def build_chapter_2(doc):
    doc.add_page_break()
    add_h1(doc, "CHƯƠNG 2. DỮ LIỆU VÀ QUY TRÌNH TIỀN XỬ LÝ")

    add_h2(doc, "2.1 Nguồn dữ liệu, quy mô và cấu trúc thuộc tính")
    add_p(doc, "Hệ thống dữ liệu thực nghiệm được xây dựng mô phỏng mạng vô tuyến tế bào gồm 4 tập dữ liệu có mối liên kết chặt chẽ:")

    add_h3(doc, "2.1.1 Bảng sự kiện đo kiểm KPI viễn thông (network_kpi_events.csv)")
    add_p(doc, "Tập dữ liệu sự kiện đo kiểm gồm 12.001 dòng (1 dòng tiêu đề và 12.000 bản ghi đo kiểm). Mỗi bản ghi phản ánh phiên truyền dữ liệu trong chu kỳ 5 giây của một sector cell với các trường: event_id (Khóa chính), timestamp, tower_id (Khóa ngoại), cell_id (Khóa ngoại), technology (3G/4G/5G), throughput_mbps, latency_ms, packet_loss_pct, call_dropped (0/1), num_active_users, session_volume_mb và cờ chất lượng quality_flag.")

    add_h3(doc, "2.1.2 Danh mục trạm BTS (bts_towers.csv) và cấu hình Cell (cells_catalog.csv)")
    add_p(doc, "Bảng bts_towers.csv lưu trữ thông tin định danh và tọa độ địa lý của 20 trạm phát sóng chính: tower_id (PK), tower_name, province (Hà Nội, TP.HCM, Đà Nẵng), district, latitude, longitude và install_date.")
    add_p(doc, "Bảng cells_catalog.csv lưu cấu hình phần cứng của 80 sector vô tuyến: cell_id (PK), tower_id (FK), technology, frequency_mhz (2100MHz 3G, 1800/2600MHz 4G, 3500MHz 5G), max_bandwidth, azimuth (hướng anten 0°, 120°, 240°) và antenna_tilt (góc ngửa anten).")

    add_h3(doc, "2.1.3 Luồng sự kiện mô phỏng (bts_syslog.log / network_kpi_events)")
    add_p(doc, "Luồng sự kiện nhật ký bts_syslog.log mô phỏng luồng log nhúng thời gian thực từ firmware trạm phát sóng theo chuẩn RFC-5424. Luồng dữ liệu mang các thông tin mức độ cảnh báo (INFO, WARNING, CRITICAL) ghi nhận các sự cố: suy giảm mức thu vô tuyến (RSSI Low), nhiệt độ khuếch đại công suất vượt ngưỡng, và nghẽn hàng đợi đệm truyền dẫn.")

    add_h3(doc, "2.1.4 Cơ sở dữ liệu quan hệ đối chiếu (telecom_network.sqlite / customer_complaints.csv)")
    add_p(doc, "Bảng customer_complaints.csv lưu trữ 250 bản ghi khiếu nại khách hàng gửi về tổng đài CSKH: complaint_id (PK), timestamp, user_msisdn, tower_id, cell_id, complaint_type (Chậm mạng, Rớt cuộc gọi, Mất sóng), status và resolution_notes.")
    add_p(doc, "Cơ sở dữ liệu SQLite telecom_network.sqlite đóng vai trò kho đối chiếu tổng hợp, lưu trữ toàn bộ các bảng trên cùng bảng kết quả kpi_analysis_summary.")

    add_tbl(
        doc,
        headers=["Tên tệp dữ liệu", "Định dạng", "Khóa chính (PK)", "Khóa ngoại (FK)", "Số trường", "Mô tả & Ý nghĩa nghiệp vụ viễn thông"],
        data=[
            ["network_kpi_events.csv", "CSV / UTF-8", "event_id", "tower_id, cell_id", "12", "Dữ liệu đo kiểm phiên dịch vụ di động (Tệp dữ liệu gồm 12.001 dòng: 1 dòng tiêu đề và 12.000 bản ghi đo kiểm), lưu thông lượng, độ trễ, mất gói, cờ rớt cuộc gọi và số người dùng đồng thời."],
            ["bts_towers.csv", "CSV / UTF-8", "tower_id", "Không có", "7", "Danh mục thông tin định danh và tọa độ địa lý của trạm phát sóng (tower_name, province, district, latitude, longitude, install_date)."],
            ["cells_catalog.csv", "CSV / UTF-8", "cell_id", "tower_id", "8", "Danh mục cấu hình phần cứng vô tuyến của từng sector cell (technology 3G/4G/5G, frequency_mhz, max_bandwidth, azimuth, antenna_tilt)."],
            ["customer_complaints.csv", "CSV / UTF-8", "complaint_id", "tower_id, cell_id", "8", "Bản ghi khiếu nại của khách hàng gửi về tổng đài CSKH (user_msisdn, complaint_type, status, resolution_notes)."],
        ],
        caption="Bảng 2.1: Khảo sát cấu trúc 4 tập dữ liệu viễn thông thực nghiệm",
        col_widths=[1.6, 0.9, 1.0, 1.1, 0.6, 2.3]
    )

    add_p(doc, "Sơ đồ thực thể quan hệ (ERD Schema) mô tả quan hệ phân cấp giữa 4 tập dữ liệu được thể hiện trong Hình 2.1:")

    add_fig(
        doc,
        img_name="hinh_2_1_mo_hinh_du_lieu.png",
        caption="Hình 2.1: Sơ đồ thực thể quan hệ dữ liệu viễn thông (ERD Schema)",
        width_in=5.8
    )

    add_p(doc, "Mô hình tuân theo cấu trúc phân cấp hình cây tiêu chuẩn trong quản lý mạng di động tế bào:", bold_prefix="Nhận xét Hình 2.1: ")
    add_bullet(doc, "Quan hệ bts_towers và cells_catalog là 1 : N (Một trạm vật lý gắn với nhiều sector cell phát sóng đa hướng và đa tần số).")
    add_bullet(doc, "Quan hệ cells_catalog và network_kpi_events là 1 : N (Mỗi cell liên tục phát sinh hàng nghìn bản ghi đo kiểm thời gian thực).")
    add_bullet(doc, "Quan hệ giữa cell và customer_complaints là 1 : N (Hệ thống CSKH tự động ánh xạ vị trí thuê bao khiếu nại về cell đang phục vụ).")

    add_h2(doc, "2.2 Đánh giá chất lượng dữ liệu và các cờ cảnh báo (quality_flag)")
    add_p(doc, "Dữ liệu đo kiểm viễn thông thực tế thu thập từ hàng chục nghìn trạm phát sóng luôn chứa đựng độ nhiễu và các giá trị dị thường bắt nguồn từ lỗi phần cứng cảm biến, suy hao đường truyền vô tuyến hoặc lỗi xung nhịp. Nhóm đã xây dựng ma trận phân tích rủi ro và giải pháp xử lý chất lượng dữ liệu:")

    add_tbl(
        doc,
        headers=["Vấn đề chất lượng", "Biểu hiện dữ liệu", "Nguyên nhân vật lý", "Hậu quả tính toán", "Phương án xử lý kỹ thuật"],
        data=[
            ["Giá trị độ trễ âm\n(Negative Latency)", "latency_ms < 0\n(VD: -15.4 ms)", "Lệch xung đồng hồ NTP giữa trạm BTS và máy chủ đo kiểm.", "Làm sai lệch giá trị trung bình độ trễ toàn mạng.", "Lọc bỏ trong Filter: filter(col('latency_ms') >= 0.0)."],
            ["Thông lượng âm\n(Negative Throughput)", "throughput_mbps < 0\n(VD: -99.0 Mbps)", "Bộ đếm byte tràn số nguyên (Counter Overflow) tại firmware cũ.", "Gây âm tổng dung lượng phiên truyền tải.", "Loại bỏ hoàn toàn bản ghi lỗi trong bước tiền xử lý."],
            ["Mất gói vô lý\n(Out of Range Loss)", "packet_loss_pct > 100%\n(VD: 150.0%)", "Thuật toán ước lượng mất gói suy hao đa đường bị phân kỳ.", "Gây sai lệch chỉ số phần trăm tỷ lệ mất gói.", "Ràng buộc kiểm tra: (col('packet_loss_pct') <= 100.0)."],
            ["Bản ghi mồ côi\n(Orphaned Events)", "tower_id hoặc cell_id\nbị rỗng (NULL)", "Lỗi đóng gói gói tin telemetry khi truyền tải trên mạng Backhaul.", "Làm thất bại phép Inner Join với bảng danh mục.", "Loại bỏ bản ghi: filter(col('tower_id').isNotNull())."],
            ["Điểm ngoại lai cực trị\n(Extreme Outliers)", "latency_ms > 2000 ms\n(Bất thường kéo dài)", "Sự cố đứt liên kết truyền dẫn cáp quang hoặc sập nguồn trạm.", "Làm méo phân phối thống kê chất lượng mạng.", "Xác định bằng biểu đồ Boxplot và phân cụm cô lập."],
        ],
        caption="Bảng 2.2: Ma trận rủi ro và phương án xử lý chất lượng dữ liệu đo kiểm",
        col_widths=[1.4, 1.2, 1.6, 1.4, 1.8]
    )

    add_p(doc, "Cờ cảnh báo chất lượng dữ liệu (quality_flag): Mỗi bản ghi được đánh dấu cờ nhị phân: quality_flag = 1 nếu vượt qua tất cả các bài kiểm tra logic; quality_flag = 0 nếu vi phạm bất kỳ điều kiện nào trong Bảng 2.2 để cách ly xử lý.", bold_prefix="Cơ chế cờ cảnh báo: ")

    add_h2(doc, "2.3 Quy trình tiền xử lý và làm sạch dữ liệu (Data Cleaning & Normalization)")
    add_p(doc, "Quy trình tiền xử lý dữ liệu được thiết kế thành một chuỗi biến đổi tuần tự gồm 2 bước cốt lõi:")
    add_bullet(doc, "Bước 1 - Khử trùng lặp và làm sạch logic (Data Cleansing): Hệ thống loại bỏ các bản ghi trùng lặp (distinct) do cơ chế gửi lại bản tin của mạng truyền dẫn, đồng thời loại bỏ các dòng có trường định danh bị rỗng hoặc vi phạm các miền giá trị vật lý (độ trễ âm, thông lượng âm, mất gói vượt 100%). Sau bước này, tập dữ liệu thực nghiệm đã loại bỏ 48 bản ghi lỗi (chiếm 0.40%), giữ lại 11,952 bản ghi hoàn toàn sạch.")
    add_bullet(doc, "Bước 2 - Kỹ thuật tạo đặc trưng nghiệp vụ (Feature Engineering): Hệ thống tính toán thêm 4 cột đặc trưng phái sinh phục vụ phân tích nghiệp vụ và mô hình học máy:", bold_prefix="Kỹ thuật tạo đặc trưng: ")

    add_p(doc, "1. Dung lượng phiên dữ liệu (Session Volume - MB):", bold_prefix="• Công thức 1: ")
    add_p(doc, "session_volume_mb = (throughput_mbps * 5.0 giây) / 8.0 bits/Byte", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True)

    add_p(doc, "2. Tỷ lệ rớt cuộc gọi chuẩn hóa (Call Drop Rate %):", bold_prefix="• Công thức 2: ")
    add_p(doc, "call_drop_rate_pct = 100.0% nếu call_dropped = 1; ngược lại = 0.0%", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True)

    add_p(doc, "3. Nhận diện trạng thái quá tải vô tuyến (Congestion Status):", bold_prefix="• Công thức 3: ")
    add_p(doc, "congestion_status = 'QUÁ_TẢI' nếu (num_active_users > 150 VÀ throughput_mbps < 15.0); ngược lại = 'BÌNH_THƯỜNG'", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True)

    add_p(doc, "4. Điểm chất lượng dịch vụ tổng hợp (QoS Score - Thang điểm 100):", bold_prefix="• Công thức 4: ")
    add_p(doc, "qos_score = 100.0 - (0.35 * latency_ms + 0.35 * packet_loss_pct * 5.0 + 0.30 * call_dropped * 50.0)", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True)

print("Module Part 1 created successfully.")
