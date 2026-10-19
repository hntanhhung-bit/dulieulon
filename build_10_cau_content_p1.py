# -*- coding: utf-8 -*-
"""
NỘI DUNG CHI TIẾT CÂU 1, CÂU 2, CÂU 3
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from build_10_cau_helpers import (
    add_header_paragraph, add_body_paragraph, add_bullet_point,
    add_callout_box, add_code_snippet, add_image_with_caption,
    format_custom_table
)

def add_cau_1(doc):
    add_header_paragraph(doc, "CÂU 1 (1,0 ĐIỂM): PHÂN TÍCH ĐẶC TRƯNG BIG DATA 5V VÀ PHÂN LOẠI DỮ LIỆU VIỄN THÔNG", level=1)
    
    add_callout_box(doc, "Câu 1 (1,0 điểm)", 
        "Phân tích đặc trưng Big Data của bài toán Viễn thông theo tối thiểu 5V. "
        "Phân loại các tệp và trường dữ liệu thành dữ liệu có cấu trúc, bán cấu trúc và dữ liệu luồng; "
        "chỉ rõ phần nào phù hợp phân tích tĩnh và phần nào cần xử lý gần thời gian thực.")
    
    add_header_paragraph(doc, "1.1. Phân tích 5 đặc trưng Big Data (5V) trong bài toán Viễn thông", level=2)
    add_body_paragraph(doc, 
        "Hệ thống giám sát và vận hành mạng viễn thông (Network Operations Center - NOC) quản lý hàng chục nghìn "
        "trạm thu phát sóng (BTS) và phục vụ hàng triệu thuê bao di động. Bài toán phân tích chất lượng mạng (QoS/QoE) "
        "mang đầy đủ 5 đặc trưng cốt lõi của dữ liệu lớn (Big Data):")
    
    add_bullet_point(doc, "1. Volume (Khối lượng dữ liệu khổng lồ)", 
        "Một nhà mạng quy mô quốc gia quản lý khoảng 50.000 trạm BTS. Mỗi trạm sở hữu từ 3 đến 6 cell vô tuyến thuộc các dải tần 3G, 4G LTE và 5G NR. "
        "Với chu kỳ đo kiểm telemetry 5 giây/lần trên từng cell, toàn mạng sinh ra xấp xỉ 3,5 tỷ sự kiện đo kiểm mỗi ngày. Kèm theo đó là hàng trăm triệu "
        "bản ghi chi tiết cuộc gọi (CDR) và phiên truy cập Internet (xDR). Khối lượng dữ liệu thô sinh ra dao động từ 10 đến 25 Terabyte/ngày, "
        "tích lũy qua các năm lên tới quy mô hàng chục Petabyte.")
    
    add_bullet_point(doc, "2. Velocity (Tốc độ sinh và truyền dữ liệu tức thời)", 
        "Dữ liệu đo kiểm lớp vật lý và phiên người dùng được trạm phát sóng gửi liên tục về trung tâm qua các kết nối streaming thời gian thực. "
        "Vào khung giờ cao điểm (19h00 - 22h00), thông lượng tiếp nhận trên toàn mạng vượt mức 500.000 sự kiện/giây. "
        "Hệ thống NOC đòi hỏi khả năng xử lý và kích hoạt cảnh báo trạm mất sóng hoặc rớt cuộc gọi đột biến trong thời gian dưới 1 giây để kỹ sư kịp thời can thiệp.")
    
    add_bullet_point(doc, "3. Variety (Đa dạng về chủng loại và định dạng dữ liệu)", 
        "Hệ sinh thái viễn thông là sự kết hợp đa thế hệ mạng (2G/3G kế thừa, 4G băng rộng, 5G độ trễ cực thấp) từ nhiều nhà sản xuất thiết bị (Ericsson, Huawei, Nokia, ZTE). "
        "Định dạng dữ liệu gồm: Bảng dữ liệu có cấu trúc (RDBMS) lưu danh mục trạm BTS và cell; Nhật ký bán cấu trúc (Syslog chuẩn RFC-5424) từ hệ điều hành nhúng; "
        "Tệp cấu hình tham số vô tuyến định dạng XML/JSON (ran_config.xml); và Dữ liệu luồng đo kiểm telemetry (Time-series stream).")
    
    add_bullet_point(doc, "4. Veracity (Tính xác thực và độ nhiễu của dữ liệu)", 
        "Do sóng vô tuyến truyền lan trong không gian tự do chịu ảnh hưởng nặng nề bởi thời tiết mưa bão, địa hình che chắn, can nhiễu đồng kênh và suy hao đa đường, "
        "dữ liệu viễn thông thường xuyên xuất hiện giá trị ngoại lai (outliers). Hiện tượng lệch xung đồng hồ NTP giữa BTS và máy chủ trung tâm có thể sinh ra bản ghi độ trễ âm vô lý "
        "(latency < 0). Khâu tiền xử lý, kiểm tra tính hợp lệ và khử nhiễu là điều kiện bắt buộc trước khi tính toán KPI.")
    
    add_bullet_point(doc, "5. Value (Giá trị nghiệp vụ và kinh tế cốt lõi)", 
        "Khai thác hiệu quả nguồn dữ liệu này giúp nhà mạng: (1) Nâng cao chất lượng trải nghiệm mạng QoE cho người dùng; (2) Kéo giảm tỷ lệ rời mạng của thuê bao (Churn Reduction); "
        "(3) Chủ động hỗ trợ khách hàng trước khi phát sinh khiếu nại gay gắt; (4) Tối ưu hóa chi phí đầu tư vốn (CAPEX) bằng cách nâng cấp chính xác các trạm bị nghẽn thực sự.")

    add_header_paragraph(doc, "1.2. Phân loại các tệp và trường dữ liệu thực nghiệm trong dự án", level=2)
    add_body_paragraph(doc, "Dựa trên bộ dữ liệu thực nghiệm 12.001 dòng của đề tài, các nguồn dữ liệu được phân chia thành 3 nhóm rõ rệt:")
    
    tbl_data = doc.add_table(rows=1, cols=4)
    headers = ["Phân loại", "Tên tệp / Nguồn", "Các trường dữ liệu chính", "Mô tả & Ý nghĩa"]
    rows = [
        ["Dữ liệu có cấu trúc\n(Structured)", "bts_towers.csv", "tower_id, tower_name, province, district, latitude, longitude, install_date", "Bảng danh mục thông tin định danh và tọa độ địa lý trạm BTS."],
        ["Dữ liệu có cấu trúc\n(Structured)", "cells_catalog.csv", "cell_id, tower_id, technology (3G/4G/5G), frequency_mhz, max_bandwidth_mbps, azimuth", "Cấu hình tham số phần cứng vô tuyến của từng sector cell."],
        ["Dữ liệu có cấu trúc\n(Structured)", "customer_complaints.csv", "complaint_id, timestamp, tower_id, user_msisdn, complaint_type, status", "Bản ghi khiếu nại của khách hàng gửi về tổng đài chăm sóc khách hàng."],
        ["Dữ liệu bán cấu trúc\n(Semi-structured)", "bts_syslog.log", "syslog_pri, timestamp, hostname, process_id, message_text, severity_level", "Nhật ký hệ điều hành nhúng của trạm BTS theo chuẩn RFC-5424."],
        ["Dữ liệu bán cấu trúc\n(Semi-structured)", "ran_config.xml", "<antenna tilt='2.5'>, <power_dbm>43</power_dbm>, <handover_margin_db>3.0</handover_margin_db>", "Tệp cấu hình tham số chuyển giao (handover) và góc ngửa anten vô tuyến."],
        ["Dữ liệu luồng\n(Streaming Data)", "network_kpi_events.csv\n(12.001 dòng)", "event_id, timestamp, tower_id, cell_id, technology, throughput_mbps, latency_ms, packet_loss_pct, call_dropped, num_active_users", "Luồng sự kiện đo kiểm chất lượng mạng tức thời sinh ra liên tục theo chu kỳ."]
    ]
    format_custom_table(tbl_data, [Inches(1.5), Inches(1.3), Inches(2.2), Inches(1.5)], headers, rows)
    
    add_image_with_caption(doc, r"c:\dulieulon\report\hinh_2_1_mo_hinh_du_lieu.png", "Hình 1.1: Sơ đồ thực thể liên kết (ERD) mô tả quan hệ giữa các tập dữ liệu có cấu trúc và bán cấu trúc", width=Inches(6.2))

    add_header_paragraph(doc, "1.3. Phân định ranh giới xử lý: Phân tích tĩnh (Batch) vs Gần thời gian thực (Near Real-Time)", level=2)
    add_body_paragraph(doc, "Hệ thống cần phân định rõ ràng ranh giới xử lý theo kiến trúc Lambda:")
    
    add_bullet_point(doc, "1. Xử lý gần thời gian thực (Near Real-Time: Độ trễ < 1s - 5s)",
        "Áp dụng cho dữ liệu luồng sự kiện đo kiểm (network_kpi_events) và nhật ký Syslog. "
        "Mục đích: Phát hiện tức thời sự cố đứt gãy truyền dẫn (Outage), cell bị quá tải nghiêm trọng (> 150 người dùng), tỷ lệ rớt cuộc gọi tăng vọt (> 2.0%) "
        "hoặc độ trễ vượt ngưỡng cam kết SLA (> 80ms). Dữ liệu được đưa qua Apache Flume và lưu trữ vào Apache HBase để kỹ sư NOC tra cứu tức thì.")
        
    add_bullet_point(doc, "2. Phân tích tĩnh theo lô (Batch Analytics: Chu kỳ Giờ / Ngày / Tuần)",
        "Áp dụng cho toàn bộ dữ liệu lịch sử tích lũy trên HDFS kết hợp với bảng danh mục trạm BTS, cell và khiếu nại khách hàng. "
        "Mục đích: Tổng hợp báo cáo KPI định kỳ tuần/tháng, đánh giá hiệu quả vùng phủ sóng, quy hoạch phân bổ vốn đầu tư trạm mới (CAPEX), "
        "và huấn luyện mô hình Machine Learning phân loại thuê bao có nguy cơ rời mạng.")


def add_cau_2(doc):
    doc.add_page_break()
    add_header_paragraph(doc, "CÂU 2 (1,0 ĐIỂM): KIẾN TRÚC THU THẬP & LƯU TRỮ ĐẦU-CUỐI VỚI APACHE FLUME (2 KỊCH BẢN)", level=1)
    
    add_callout_box(doc, "Câu 2 (1,0 điểm)", 
        "Đề xuất kiến trúc thu thập và lưu trữ dữ liệu đầu-cuối. "
        "Thiết kế ít nhất hai kịch bản Flume: (i) nạp tệp CSV theo lô vào HDFS; "
        "(ii) nhận sự kiện network_kpi_event từ HTTP/Netcat/Kafka vào HDFS hoặc HBase. "
        "Viết cấu hình Source–Channel–Sink, giải thích lựa chọn MemoryChannel/FileChannel và cơ chế chống mất dữ liệu.")
    
    add_header_paragraph(doc, "2.1. Đề xuất kiến trúc thu thập và lưu trữ dữ liệu đầu-cuối (End-to-End Pipeline)", level=2)
    add_body_paragraph(doc, 
        "Kiến trúc đề xuất được xây dựng theo mô hình Lambda Architecture, phân tách thành hai luồng xử lý độc lập: "
        "Luồng tốc độ cao (Speed Layer) tiếp nhận luồng sự kiện đo kiểm thời gian thực đẩy vào HBase phục vụ tra cứu ngẫu nhiên; "
        "Luồng xử lý theo lô (Batch Layer) thu thập tệp nhật ký đẩy vào HDFS Data Lake để phục vụ phân tích chuyên sâu với MapReduce, Pig và Spark.")
    
    add_image_with_caption(doc, r"c:\dulieulon\report\hinh_3_1_pipeline_xu_ly.png", "Hình 2.1: Sơ đồ kiến trúc pipeline xử lý dữ liệu đầu-cuối (End-to-End Data Pipeline)", width=Inches(6.4))

    add_header_paragraph(doc, "2.2. Kịch bản 1: Nạp tệp CSV theo lô vào HDFS (Spooling Directory + FileChannel + HDFS Sink)", level=2)
    add_body_paragraph(doc, 
        "Kịch bản này được thiết kế để tự động quét thư mục chỉ định trên máy chủ trạm (/telecom/spool_dir). "
        "Khi có tệp CSV đo kiểm mới xuất hiện, Agent Flume sẽ đọc toàn bộ tệp, đệm qua FileChannel để chống mất mát và ghi vào HDFS theo đường dẫn phân vùng ngày:")
    
    code_flume_1 = """# ==============================================================================
# KỊCH BẢN 1: NẠP TỆP CSV THEO LÔ VÀO HDFS (flume_csv_to_hdfs.conf)
# ==============================================================================
csvAgent.sources = r_spool
csvAgent.channels = c_file
csvAgent.sinks = k_hdfs

# CẤU HÌNH SOURCE: Quét thư mục Spooling Directory
csvAgent.sources.r_spool.type = spooldir
csvAgent.sources.r_spool.spoolDir = /home/hadoop/dulieulon/spool_kpi_csv
csvAgent.sources.r_spool.fileHeader = true
csvAgent.sources.r_spool.basenameHeader = true
csvAgent.sources.r_spool.deserializer = LINE
csvAgent.sources.r_spool.deserializer.maxLineLength = 2048

# CẤU HÌNH CHANNEL: FileChannel bền vững trên đĩa cứng
csvAgent.channels.c_file.type = file
csvAgent.channels.c_file.checkpointDir = /home/hadoop/dulieulon/flume_chk/csv
csvAgent.channels.c_file.dataDirs = /home/hadoop/dulieulon/flume_data/csv
csvAgent.channels.c_file.capacity = 1000000
csvAgent.channels.c_file.transactionCapacity = 10000

# CẤU HÌNH SINK: HDFS Sink ghi dữ liệu dạng Sequence/Text
csvAgent.sinks.k_hdfs.type = hdfs
csvAgent.sinks.k_hdfs.hdfs.path = hdfs://masternode:9000/telecom/raw/batch_kpi/%Y-%m-%d
csvAgent.sinks.k_hdfs.hdfs.filePrefix = telecom_kpi_batch
csvAgent.sinks.k_hdfs.hdfs.fileType = DataStream
csvAgent.sinks.k_hdfs.hdfs.writeFormat = Text
csvAgent.sinks.k_hdfs.hdfs.rollInterval = 300
csvAgent.sinks.k_hdfs.hdfs.rollSize = 134217728
csvAgent.sinks.k_hdfs.hdfs.rollCount = 0
csvAgent.sinks.k_hdfs.hdfs.useLocalTimeStamp = true

# KẾT NỐI SOURCE VÀ SINK QUA CHANNEL
csvAgent.sources.r_spool.channels = c_file
csvAgent.sinks.k_hdfs.channel = c_file"""
    add_code_snippet(doc, code_flume_1, "Cấu hình Flume Agent nạp lô CSV vào HDFS (flume_csv_to_hdfs.conf)")

    add_header_paragraph(doc, "2.3. Kịch bản 2: Nhận sự kiện Realtime Netcat/Socket đồng thời vào HDFS và HBase (Fan-out Pattern)", level=2)
    add_body_paragraph(doc, 
        "Kịch bản này thiết kế mô hình Fan-out (một nguồn phát cho nhiều đích đến). Nguồn Netcat tiếp nhận luồng sự kiện đo kiểm "
        "tại cổng 8888, sau đó nhân bản sự kiện qua 2 Channel độc lập để ghi đồng thời vào HDFS (phục vụ phân tích lịch sử) "
        "và Apache HBase (phục vụ tra cứu ngẫu nhiên thời gian thực):")
    
    code_flume_2 = """# ==============================================================================
# KỊCH BẢN 2: LUỒNG SỰ KIỆN THỜI GIAN THỰC VÀO HDFS & HBASE (flume_events_to_hbase.conf)
# ==============================================================================
streamAgent.sources = r_netcat
streamAgent.channels = c_mem_hdfs c_mem_hbase
streamAgent.sinks = k_hdfs_stream k_hbase_sink

# CẤU HÌNH SOURCE: Netcat lắng nghe cổng 8888
streamAgent.sources.r_netcat.type = netcat
streamAgent.sources.r_netcat.bind = 0.0.0.0
streamAgent.sources.r_netcat.port = 8888
streamAgent.sources.r_netcat.max-line-length = 2048

# CẤU HÌNH CHANNELS: MemoryChannel cho độ trễ cực thấp
streamAgent.channels.c_mem_hdfs.type = memory
streamAgent.channels.c_mem_hdfs.capacity = 500000
streamAgent.channels.c_mem_hdfs.transactionCapacity = 5000

streamAgent.channels.c_mem_hbase.type = memory
streamAgent.channels.c_mem_hbase.capacity = 500000
streamAgent.channels.c_mem_hbase.transactionCapacity = 5000

# CẤU HÌNH SINK 1: Ghi vào HDFS theo chu kỳ ngắn 30s
streamAgent.sinks.k_hdfs_stream.type = hdfs
streamAgent.sinks.k_hdfs_stream.hdfs.path = hdfs://masternode:9000/telecom/raw/stream_kpi/%Y-%m-%d
streamAgent.sinks.k_hdfs_stream.hdfs.filePrefix = stream_kpi
streamAgent.sinks.k_hdfs_stream.hdfs.rollInterval = 30
streamAgent.sinks.k_hdfs_stream.hdfs.rollSize = 67108864
streamAgent.sinks.k_hdfs_stream.hdfs.useLocalTimeStamp = true

# CẤU HÌNH SINK 2: Ghi vào bảng HBase telecom_kpi qua AsyncHBaseSink
streamAgent.sinks.k_hbase_sink.type = asynchbase
streamAgent.sinks.k_hbase_sink.table = telecom_kpi
streamAgent.sinks.k_hbase_sink.columnFamily = cf_kpi
streamAgent.sinks.k_hbase_sink.serializer = org.apache.flume.sink.hbase.SimpleAsyncHbaseEventSerializer
streamAgent.sinks.k_hbase_sink.serializer.payloadColumn = kpi_raw_data

# GHÉP NỐI FAN-OUT: 1 Source đẩy vào 2 Channel
streamAgent.sources.r_netcat.channels = c_mem_hdfs c_mem_hbase
streamAgent.sinks.k_hdfs_stream.channel = c_mem_hdfs
streamAgent.sinks.k_hbase_sink.channel = c_mem_hbase"""
    add_code_snippet(doc, code_flume_2, "Cấu hình Flume Fan-out vào HDFS và HBase (flume_events_to_hbase.conf)")

    add_header_paragraph(doc, "2.4. So sánh kỹ thuật: MemoryChannel vs FileChannel", level=2)
    tbl_cmp = doc.add_table(rows=1, cols=4)
    headers_cmp = ["Tiêu chí so sánh", "MemoryChannel", "FileChannel", "Đánh giá lựa chọn trong đề tài"]
    rows_cmp = [
        ["Cơ chế lưu trữ", "Lưu trực tiếp trong bộ nhớ RAM của tiến trình JVM.", "Lưu trên đĩa cứng vật lý kèm tệp nhật ký Checkpoint & WAL.", "FileChannel an toàn tuyệt đối; MemoryChannel tối ưu độ trễ."],
        ["Tốc độ thông lượng", "Rất cao (> 100.000 sự kiện/giây).", "Trung bình (phụ thuộc tốc độ ghi I/O đĩa cứng HDD/SSD).", "MemoryChannel dùng cho luồng cảnh báo tức thời."],
        ["Độ tin cậy & Bền vững", "Không bền vững. Mất toàn bộ sự kiện trong hàng đợi nếu sập nguồn JVM.", "Bền vững 100%. Khôi phục đầy đủ dữ liệu sau khi tiến trình khởi động lại.", "FileChannel bắt buộc cho dữ liệu nạp lô quyết toán."],
        ["Mục đích áp dụng", "Phù hợp cho dữ liệu giám sát realtime chấp nhận mất mát nhỏ.", "Phù hợp cho dữ liệu nhạy cảm: cước, CDR, tài sản trạm BTS.", "Đề tài kết hợp cả hai kênh tùy theo từng kịch bản."]
    ]
    format_custom_table(tbl_cmp, [Inches(1.5), Inches(1.5), Inches(1.8), Inches(1.7)], headers_cmp, rows_cmp)

    add_header_paragraph(doc, "2.5. Cơ chế giao dịch chống mất dữ liệu (Reliability & Crash Recovery)", level=2)
    add_body_paragraph(doc, 
        "Apache Flume bảo đảm nguyên tắc truyền tải 'At-least-once' (ít nhất một lần) thông qua cơ chế giao dịch hai pha (Two-Phase Commit Transaction):")
    add_bullet_point(doc, "Pha nạp (Put Transaction)", 
        "Source nhận sự kiện từ trạm BTS, mở transaction với Channel. Sự kiện chỉ được đánh dấu là nạp thành công khi đã ghi trọn vẹn vào Channel buffer. "
        "Nếu bộ đệm bị tràn hoặc lỗi đường truyền, transaction rollback và trạm BTS được yêu cầu gửi lại.")
    add_bullet_point(doc, "Pha rút (Take Transaction)", 
        "Sink rút sự kiện từ Channel qua transaction.take(), sau đó ghi vào HDFS hoặc HBase. Chỉ khi HDFS NameNode/DataNode xác nhận ghi khối thành công (Flush & Sync), "
        "Sink mới phát lệnh transaction.commit() để xóa sự kiện khỏi Channel. Nếu máy chủ Flume sập nguồn giữa chừng, sự kiện vẫn nguyên vẹn trong Channel và được gửi lại khi khởi động.")


def add_cau_3(doc):
    doc.add_page_break()
    add_header_paragraph(doc, "CÂU 3 (1,0 ĐIỂM): THIẾT KẾ VÙNG DỮ LIỆU HDFS, DUNG LƯỢNG LƯU TRỮ & CƠ CHẾ DUNG LỖI", level=1)
    
    add_callout_box(doc, "Câu 3 (1,0 điểm)", 
        "Thiết kế vùng dữ liệu trên HDFS gồm raw, staging, curated và output. "
        "Đề xuất cấu trúc thư mục phân vùng theo thời gian và tower_id; "
        "tính dung lượng lưu trữ khi nhân bản 3 lần; "
        "mô tả vai trò NameNode, DataNode, YARN và phương án khôi phục khi một node hỏng.")
    
    add_header_paragraph(doc, "3.1. Thiết kế 4 vùng dữ liệu trên HDFS Data Lake", level=2)
    add_body_paragraph(doc, 
        "Hệ thống lưu trữ phân tán HDFS được tổ chức thành 4 phân tầng (Multi-tier Data Lake Architecture) rõ ràng:")
    
    tbl_tiers = doc.add_table(rows=1, cols=4)
    headers_t = ["Phân vùng HDFS", "Đường dẫn thư mục", "Định dạng lưu trữ", "Vai trò và Mục đích sử dụng"]
    rows_t = [
        ["Vùng Raw\n(Dữ liệu thô)", "/telecom/raw/batch_kpi/\n/telecom/raw/stream_kpi/", "CSV, Text, JSON thô\n(Bất biến - Immutable)", "Lưu trữ toàn bộ dữ liệu gốc thu nhận từ Flume và trạm BTS. Không chỉnh sửa dữ liệu tại vùng này."],
        ["Vùng Staging\n(Vùng đệm lọc)", "/telecom/staging/kpi_filtered/", "CSV tạm thời\n(Temporary Data)", "Nơi chứa dữ liệu đang trong quá trình tiền xử lý, lọc bỏ bản ghi lỗi, giá trị âm và tiêu đề."],
        ["Vùng Curated\n(Dữ liệu sạch)", "/telecom/curated/cell_kpi/\n/telecom/curated/dimension/", "Snappy Parquet\n(Columnar Storage)", "Dữ liệu đã được làm sạch, ép kiểu, join với danh mục trạm và nén tối ưu. Phục vụ truy vấn phân tích."],
        ["Vùng Output\n(Kết quả báo cáo)", "/telecom/output/mapreduce_kpi/\n/telecom/output/alerts/", "CSV, JSON, Báo cáo KPI", "Lưu trữ kết quả tính toán cuối cùng từ MapReduce, Pig, Spark sẵn sàng kết nối sang BI Dashboard."]
    ]
    format_custom_table(tbl_tiers, [Inches(1.3), Inches(1.8), Inches(1.4), Inches(2.0)], headers_t, rows_t)

    add_header_paragraph(doc, "3.2. Cấu trúc thư mục phân vùng tối ưu theo Thời gian và Mã trạm", level=2)
    add_body_paragraph(doc, 
        "Để tối ưu hóa hiệu năng truy vấn, cơ chế Partitioning Pruning (loại trừ phân vùng không cần thiết) được áp dụng. "
        "Dữ liệu được tổ chức phân cấp: Năm -> Tháng -> Ngày -> Mã trạm (tower_id):")
    
    code_part = """/telecom/curated/cell_kpi/
    ├── year=2026/
    │   └── month=10/
    │       ├── day=19/
    │       │   ├── tower_id=TOWER_001/
    │       │   │   ├── part-00000-snappy.parquet
    │       │   │   └── part-00001-snappy.parquet
    │       │   ├── tower_id=TOWER_002/
    │       │   │   └── part-00000-snappy.parquet
    │       │   └── tower_id=TOWER_003/
    │       │       └── part-00000-snappy.parquet
    │       └── day=20/
    └── dimension/
        ├── bts_towers.csv
        └── cells_catalog.csv"""
    add_code_snippet(doc, code_part, "Cấu trúc thư mục phân vùng tối ưu trên HDFS")

    add_header_paragraph(doc, "3.3. Bài toán tính toán dung lượng lưu trữ khi nhân bản RF=3", level=2)
    add_body_paragraph(doc, "Dự toán tài nguyên phần cứng lưu trữ cho hệ thống mạng viễn thông quy mô quốc gia:")
    add_bullet_point(doc, "Dữ liệu thô phát sinh mỗi ngày", "Khối lượng thô trung bình = 15 Terabyte/ngày.")
    add_bullet_point(doc, "Hệ số nhân bản mặc định (Replication Factor = 3)", "Dung lượng vật lý cần thiết = 15 TB * 3 = 45 Terabyte/ngày.")
    add_bullet_point(doc, "Hệ số dự phòng hệ thống (Overhead 30%)", 
        "Bao gồm: Không gian đệm cho NameNode lưu Block metadata, vùng đệm tạm thời cho pha Shuffle/Spill của MapReduce và Spark, "
        "chỉ mục tìm kiếm = 45 TB * 1.3 = 58.5 Terabyte/ngày.")
    add_bullet_point(doc, "Tổng dung lượng lưu trữ cần thiết cho 1 năm", 
        "Dung lượng lưu trữ 365 ngày = 58.5 TB * 365 = 21.352,5 Terabyte xấp xỉ 21,35 Petabyte. "
        "Nếu áp dụng chuẩn nén Snappy Parquet ở tầng Curated (tỷ lệ nén 4:1), dung lượng lưu trữ thực tế giảm xuống còn khoảng 8 Petabyte/năm.")

    add_header_paragraph(doc, "3.4. Vai trò của NameNode, DataNode và YARN trong cụm máy ảo", level=2)
    add_bullet_point(doc, "1. NameNode (Master Node - IP: 192.168.231.132)", 
        "Đóng vai trò quản lý toàn bộ hệ thống tệp phân tán HDFS. NameNode duy trì cây thư mục (Namespace) và bảng ánh xạ vị trí các khối dữ liệu (Block-to-DataNode Mapping) "
        "hoàn toàn trong bộ nhớ RAM để đáp ứng nhanh các yêu cầu mở, đọc, ghi tệp từ máy khách.")
        
    add_bullet_point(doc, "2. DataNode (Worker Nodes - IP: 192.168.231.137, 192.168.231.136)", 
        "Trực tiếp lưu trữ các khối dữ liệu vật lý (Block size = 128 MB) trên ổ đĩa cứng của máy tính cục bộ. "
        "Định kỳ mỗi 3 giây, DataNode gửi tín hiệu Heartbeat về NameNode để báo cáo tình trạng sống và báo cáo danh sách khối dữ liệu (Block Report).")
        
    add_bullet_point(doc, "3. YARN (Yet Another Resource Negotiator)", 
        "Hệ điều hành cụm phân tán gồm: ResourceManager đóng vai trò điều phối tổng thể tài nguyên CPU và RAM của toàn bộ máy ảo; "
        "NodeManager chạy trên từng máy Worker để giám sát các thùng chứa tài nguyên (Containers) thực thi tác vụ MapReduce và Spark.")

    add_header_paragraph(doc, "3.5. Phương án tự động phục hồi chịu lỗi khi một DataNode bị hỏng", level=2)
    add_body_paragraph(doc, 
        "Khi một máy chủ DataNode (ví dụ datanode2) gặp sự cố sập nguồn hoặc đứt cáp mạng vật lý, cơ chế tự phục hồi của HDFS diễn ra như sau:")
    add_bullet_point(doc, "Bước 1: Phát hiện sự cố (Dead Node Detection)", 
        "Nếu NameNode không nhận được tín hiệu Heartbeat từ DataNode trong khoảng thời gian cấu hình mặc định (dfs.heartbeat.interval * 10 + 2 * heartbeat.recheck.interval = 10 phút 30 giây), "
        "NameNode sẽ chính thức đánh dấu DataNode đó là 'Dead Node' và loại khỏi danh sách phục vụ.")
    add_bullet_point(doc, "Bước 2: Quét khối thiếu bản sao (Under-Replicated Blocks)", 
        "NameNode quét bảng ánh xạ Inode và phát hiện các khối dữ liệu lưu trên node hỏng bị giảm hệ số nhân bản xuống dưới mức an toàn (chỉ còn RF=2 thay vì RF=3).")
    add_bullet_point(doc, "Bước 3: Tái nhân bản phân tán (Automatic Re-replication)", 
        "NameNode chọn lọc các DataNode còn sống khỏe mạnh (datanode1) và ra lệnh sao chép các khối dữ liệu bị thiếu sang máy chủ khác trong cụm để đưa hệ số nhân bản trở lại đúng RF=3. "
        "Toàn bộ quá trình diễn ra hoàn toàn tự động trong suốt với người dùng, đảm bảo tính sẵn sàng cao và không gây gián đoạn các ứng dụng đang chạy.")

print("Module Part 1 (Cau 1 - 3) compiled successfully.")
