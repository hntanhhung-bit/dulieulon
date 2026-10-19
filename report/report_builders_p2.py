# -*- coding: utf-8 -*-
"""
MODULE 2: CHƯƠNG 2 (THIẾT KẾ DỮ LIỆU & TIỀN XỬ LÝ) VÀ CHƯƠNG 3 (XÂY DỰNG HỆ THỐNG XỬ LÝ)
Tuân thủ quy chuẩn học phần Xử lý dữ liệu lớn (CTKU122 - HUNRE)
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from report_builders_p1 import add_p, add_bullet, add_h1, add_h2, add_h3, add_tbl, add_fig, add_code, add_callout

# ==============================================================================
# CHƯƠNG 2: THIẾT KẾ DỮ LIỆU VÀ TIỀN XỬ LÝ
# ==============================================================================
def build_chapter_2(doc):
    doc.add_page_break()
    add_h1(doc, "CHƯƠNG 2. THIẾT KẾ DỮ LIỆU VÀ TIỀN XỬ LÝ")

    add_h2(doc, "2.1. Nguồn dữ liệu và phân loại dữ liệu viễn thông")
    add_p(doc, "Trong hạ tầng mạng viễn thông hiện đại, dữ liệu được sản sinh liên tục từ nhiều thành phần mạng phân tán, bao gồm mạng truy cập vô tuyến (Radio Access Network - RAN), mạng truyền dẫn Backhaul (IP/MPLS, vi ba, cáp quang) và mạng lõi chuyển mạch gói (Evolved Packet Core - EPC / 5G Core). Để xây dựng một hệ thống dữ liệu lớn hiệu quả, việc đầu tiên là phân loại dữ liệu theo cấu trúc và đặc tính luồng dữ liệu:")
    
    add_bullet(doc, "Dữ liệu có cấu trúc (Structured Data): Là các tập dữ liệu có lược đồ (schema) cố định, định dạng bảng rõ ràng và tuân thủ các ràng buộc toàn vẹn khóa chính - khóa ngoại. Điển hình gồm: Bảng danh mục trạm BTS (bts_towers.csv), Bảng danh mục các sector cell vô tuyến (cells_catalog.csv), và Bảng quản lý khiếu nại khách hàng (customer_complaints.csv). Dữ liệu này được lưu trữ trong các cơ sở dữ liệu quan hệ quản lý tài sản viễn thông (RDBMS Inventory) và được đồng bộ định kỳ vào Data Lake.", bold_prefix="1. Dữ liệu có cấu trúc: ")
    
    add_bullet(doc, "Dữ liệu bán cấu trúc (Semi-structured Data): Là dữ liệu không tuân theo lược đồ bảng cứng nhắc nhưng có cấu trúc tự mô tả nội tại (self-describing structure) thông qua các thẻ hoặc cặp khóa-giá trị. Điển hình là: File nhật ký hệ thống của trạm BTS (bts_syslog.log theo chuẩn RFC-5424) chứa thông tin tiến trình nhúng và mức độ cảnh báo (Severity Level); Các tệp cấu hình tham số vô tuyến định dạng XML/JSON (ran_config.xml) mô tả góc ngửa anten (antenna tilt), công suất phát (power_dbm) và ngưỡng chuyển giao (handover_margin_db).", bold_prefix="2. Dữ liệu bán cấu trúc: ")

    add_bullet(doc, "Dữ liệu luồng đo kiểm (Streaming Telemetry Data): Là dòng dữ liệu phiên đo kiểm chất lượng mạng (network_kpi_events) sinh ra từ các giao diện vô tuyến với tần suất đo 1s - 5s trên từng cell. Dữ liệu này mang tính chất biến động liên tục theo chuỗi thời gian (Time-series Stream), chứa các chỉ số đo kiểm lớp vật lý và phiên người dùng: thông lượng (throughput_mbps), độ trễ (latency_ms), tỷ lệ mất gói (packet_loss_pct), cờ rớt cuộc gọi (call_dropped) và số người dùng đồng thời (num_active_users).", bold_prefix="3. Dữ liệu luồng: ")

    add_h2(doc, "2.2. Phân định ranh giới xử lý: Gần thời gian thực vs Phân tích tĩnh")
    add_p(doc, "Một trong những quyết định kiến trúc quan trọng nhất của kỹ sư dữ liệu lớn là phân định rõ ràng những bài toán nào cần xử lý gần thời gian thực (Near Real-Time) và những bài toán nào phù hợp cho phân tích tĩnh theo lô (Batch Analytics):")

    add_bullet(doc, "Xử lý gần thời gian thực (Near Real-Time - Yêu cầu độ trễ xử lý < 1 giây đến 5 giây): Áp dụng cho các tác vụ mang tính chất phản ứng khẩn cấp để duy trì độ sẵn sàng của mạng lưới. Cụ thể bao gồm: (1) Phát hiện sự cố trạm BTS mất sóng đột ngột (Network Outage); (2) Phát hiện hiện tượng bão nghẽn lưu lượng bất thường (Flash Crowds) tại các sự kiện đông người (lễ hội, sân vận động) để kịp thời kích hoạt xe phát sóng lưu động (COW); (3) Cảnh báo tỷ lệ rớt cuộc gọi tăng vọt cục bộ vượt ngưỡng SLA > 5%; (4) Tự động kích hoạt thuật toán mạng tự tối ưu (Self-Organizing Networks - SON) để cân bằng tải sang cell lân cận. Công nghệ chủ đạo: Apache Kafka, Flume, Spark Streaming và Apache HBase NoSQL.", bold_prefix="• Phân hệ Gần thời gian thực: ")

    add_bullet(doc, "Phân tích tĩnh theo lô (Batch Analytics - Chu kỳ tính toán theo giờ, ngày hoặc tuần): Áp dụng cho các bài toán phân tích chiến lược, tối ưu hóa dài hạn và tổng hợp số liệu toàn diện. Cụ thể bao gồm: (1) Báo cáo tổng hợp chất lượng dịch vụ SLA định kỳ theo từng quận/huyện/tỉnh; (2) Phân tích đối chiếu giữa chỉ số kỹ thuật mạng và số lượng khiếu nại khách hàng; (3) Khảo sát xu hướng suy hao tín hiệu theo tuổi thọ thiết bị phần cứng; (4) Quy hoạch mở rộng hạ tầng và phân bổ vốn đầu tư trạm BTS (Capacity Planning) cho quý tiếp theo; (5) Huấn luyện các mô hình Machine Learning dự báo tỷ lệ rời mạng của thuê bao (Churn Prediction). Công nghệ chủ đạo: Hadoop HDFS, MapReduce, Apache Pig, Spark SQL, BigSheets và R Studio.", bold_prefix="• Phân hệ Phân tích tĩnh theo lô: ")

    add_h2(doc, "2.3. Khảo sát cấu trúc các tập dữ liệu thực nghiệm")
    add_p(doc, "Trong khuôn khổ thực nghiệm của đề tài, nhóm nghiên cứu đã xây dựng và sử dụng 4 tập dữ liệu viễn thông thực nghiệm chuẩn hóa, phản ánh trung thực môi trường vận hành của mạng vô tuyến tế bào:")

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

    add_p(doc, "Mối quan hệ tương hỗ và cấu trúc ràng buộc giữa 4 tập dữ liệu được mô hình hóa chi tiết trong Sơ đồ thực thể quan hệ (ERD Schema) thể hiện tại Hình 2.1 dưới đây:")

    add_fig(
        doc,
        img_name="hinh_2_1_mo_hinh_du_lieu.png",
        caption="Hình 2.1: Sơ đồ thực thể quan hệ dữ liệu viễn thông (ERD Schema)",
        width_in=5.8
    )

    add_p(doc, "Phân tích và nhận xét mô hình thực thể dữ liệu Hình 2.1:", bold_prefix="Nhận xét và phân tích chi tiết Hình 2.1: ")
    add_p(doc, "Mô hình dữ liệu tuân theo cấu trúc phân cấp hình cây tiêu chuẩn trong quản lý mạng di động tế bào:")
    add_bullet(doc, "Quan hệ giữa Bảng bts_towers và cells_catalog là quan hệ Một-Nhiều (1 : N). Một trạm phát sóng vật lý (tower_id) luôn gắn liền với nhiều cell vô tuyến phát sóng theo các hướng khác nhau (các sector có góc ngửa azimuth 0°, 120°, 240°) và các công nghệ khác nhau (3G tần số 2100MHz, 4G LTE tần số 1800MHz, 5G NR tần số 2600MHz).")
    add_bullet(doc, "Quan hệ giữa Bảng cells_catalog và network_kpi_events là quan hệ Một-Nhiều (1 : N). Mỗi sector cell theo chu kỳ đo liên tục sinh ra hàng nghìn bản ghi sự kiện đo kiểm (event_id). Khóa kết nối hai bảng bao gồm cặp khóa (tower_id, cell_id).")
    add_bullet(doc, "Quan hệ giữa Bảng bts_towers / cells_catalog và customer_complaints là quan hệ Một-Nhiều (1 : N). Khi khách hàng phản ánh chất lượng dịch vụ kém, hệ thống CSKH sẽ tự động ánh xạ vị trí thuê bao đến trạm BTS và cell mà thuê bao đang bắt sóng tại thời điểm xảy ra sự cố.")

    add_h2(doc, "2.4. Đánh giá chất lượng dữ liệu và các vấn đề dị thường")
    add_p(doc, "Dữ liệu đo kiểm viễn thông thực tế thu thập từ hàng chục nghìn trạm phát sóng luôn chứa đựng độ nhiễu và các giá trị dị thường bắt nguồn từ lỗi phần cứng cảm biến, suy hao đường truyền vô tuyến hoặc lỗi xung nhịp. Nhóm đã xây dựng ma trận phân tích rủi ro và giải pháp xử lý chất lượng dữ liệu như sau:")

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

    add_p(doc, "Nhận xét Bảng 2.2: Ma trận rủi ro đã chỉ rõ 5 nhóm lỗi điển hình trong thực tế khai thác mạng viễn thông. Việc áp dụng các bộ lọc kiểm tra tính hợp lệ dữ liệu ngay tại tầng Ingestion và tầng Staging là bắt buộc để ngăn chặn dữ liệu rác lan truyền vào các tầng tính toán nghiệp vụ cấp cao, bảo đảm tính trung thực cho các chỉ số KPI.", bold_prefix="Nhận xét Bảng 2.2: ")

    add_h2(doc, "2.5. Quy trình làm sạch dữ liệu và kỹ thuật tạo đặc trưng")
    add_p(doc, "Quy trình tiền xử lý dữ liệu được thiết kế thành một chuỗi biến đổi tuần tự gồm 2 bước cốt lõi:")
    
    add_bullet(doc, "Bước 1 - Khử trùng lặp và làm sạch logic (Data Cleansing): Hệ thống loại bỏ các bản ghi trùng lặp (distinct) do cơ chế gửi lại bản tin của mạng truyền dẫn, đồng thời loại bỏ các dòng có trường định danh bị rỗng hoặc vi phạm các miền giá trị vật lý (độ trễ âm, thông lượng âm, mất gói vượt 100%). Sau bước này, tập dữ liệu thực nghiệm đã loại bỏ 48 bản ghi lỗi (chiếm 0.40%), giữ lại 11,952 bản ghi hoàn toàn sạch.")

    add_bullet(doc, "Bước 2 - Kỹ thuật tạo đặc trưng nghiệp vụ (Feature Engineering): Để phục vụ các bài toán phân tích quản trị và huấn luyện mô hình học máy, hệ thống tính toán thêm 4 cột đặc trưng phái sinh:", bold_prefix="Kỹ thuật tạo đặc trưng (Feature Engineering): ")
    
    add_p(doc, "1. Dung lượng phiên dữ liệu (Session Volume - MB): Tính toán tổng dung lượng dữ liệu truyền tải thành công trong chu kỳ đo 5 giây:", bold_prefix="  • ")
    add_p(doc, "$$\\text{session\\_volume\\_mb} = \\frac{\\text{throughput\\_mbps} \\times 5.0 \\text{ giây}}{8.0 \\text{ bits/Byte}}$$", align=WD_ALIGN_PARAGRAPH.CENTER)

    add_p(doc, "2. Tỷ lệ rớt cuộc gọi chuẩn hóa (Call Drop Rate %): Chuyển đổi cờ rớt cuộc gọi nhị phân (0 hoặc 1) sang thang đo phần trăm:", bold_prefix="  • ")
    add_p(doc, "$$\\text{call\\_drop\\_rate\\_pct} = \\begin{cases} 100.0\\% & \\text{nếu } \\text{call\\_dropped} = 1 \\\\ 0.0\\% & \\text{nếu } \\text{call\\_dropped} = 0 \\end{cases}$$", align=WD_ALIGN_PARAGRAPH.CENTER)

    add_p(doc, "3. Nhận diện trạng thái quá tải vô tuyến (Congestion Status): Phân loại một phiên đo kiểm rơi vào tình trạng quá tải nghẽn mạng khi số người dùng đồng thời vượt quá 150 thuê bao nhưng thông lượng trung bình tụt xuống dưới 15 Mbps:", bold_prefix="  • ")
    add_p(doc, "$$\\text{congestion\\_status} = \\begin{cases} \\text{'QUÁ\\_TẢI'} & \\text{nếu } \\text{num\\_active\\_users} > 150 \\text{ và } \\text{throughput\\_mbps} < 15.0 \\\\ \\text{'BÌNH\\_THƯỜNG'} & \\text{trường hợp còn lại} \\end{cases}$$", align=WD_ALIGN_PARAGRAPH.CENTER)

    add_p(doc, "4. Điểm chất lượng dịch vụ tổng hợp (QoS Score - Thang điểm 100): Đánh giá chất lượng dịch vụ tổng thể của một trạm BTS thông qua hàm suy giảm tuyến tính kết hợp 3 trọng số kỹ thuật viễn thông (35% cho Độ trễ, 35% cho Mất gói và 30% cho Rớt cuộc gọi):", bold_prefix="  • ")
    add_p(doc, "$$\\text{qos\\_score} = 100.0 - \\left(0.35 \\times \\text{latency\\_ms} + 0.35 \\times \\text{packet\\_loss\\_pct} \\times 5.0 + 0.30 \\times \\text{call\\_dropped} \\times 50.0\\right)$$", align=WD_ALIGN_PARAGRAPH.CENTER)

# ==============================================================================
# CHƯƠNG 3: XÂY DỰNG HỆ THỐNG XỬ LÝ DỮ LIỆU LỚN
# ==============================================================================
def build_chapter_3(doc):
    doc.add_page_break()
    add_h1(doc, "CHƯƠNG 3. XÂY DỰNG HỆ THỐNG XỬ LÝ DỮ LIỆU LỚN")
    
    add_h2(doc, "3.1. Thiết lập môi trường triển khai thực nghiệm")
    add_p(doc, "Hệ thống được thiết kế và triển khai theo mô hình kiến trúc phân tán lai ghép (Hybrid Big Data Architecture) kết hợp giữa Cụm máy ảo Linux và Máy trạm Khoa học dữ liệu Windows:")
    add_bullet(doc, "Hạ tầng Cụm Big Data (Ubuntu Server 22.04 LTS): Đóng vai trò là cụm xử lý phân tán chính (masternode tại địa chỉ IP 192.168.231.132), cấp phát 4 vCPU, 8 GB RAM và 100 GB dung lượng lưu trữ trên nền tảng ảo hóa VMware Workstation Pro. Cụm vận hành đầy đủ hệ sinh thái: Apache Hadoop 3.3.6 (NameNode, DataNode, YARN ResourceManager, NodeManager), Apache Spark 3.5.0, Apache Flume 1.11.0, Apache Pig 0.17.0 và Apache HBase 2.5.5 trên nền Java OpenJDK 11 và Python 3.12.")
    add_bullet(doc, "Hạ tầng Máy trạm Phân tích (Windows 11 Host): Đóng vai trò là môi trường Khoa học dữ liệu (Data Science Workstation), vận hành R 4.6.1, RStudio Desktop 2026.09.0, Node.js 18+ và Power BI để kết nối dữ liệu từ xa, huấn luyện mô hình học máy và xây dựng Dashboard điều hành.")

    add_h2(doc, "3.2. Tổ chức lưu trữ phân tán và cơ chế dung lỗi trên HDFS")
    add_p(doc, "Hệ thống tệp phân tán HDFS đóng vai trò là kho lưu trữ dữ liệu trung tâm (Data Lake). Cây thư mục trên HDFS được tổ chức khoa học theo chuẩn kiến trúc dữ liệu doanh nghiệp:")
    add_bullet(doc, "/telecom/raw/: Chứa các tệp log thô được đẩy liên tục từ các trạm BTS thông qua Apache Flume. Vùng này có tính chất bất biến (Immutable), chỉ cấp quyền ghi cho tiến trình thu thập.")
    add_bullet(doc, "/telecom/staging/: Vùng đệm trung chuyển tạm thời phục vụ các tác vụ ETL hàng ngày, dữ liệu có vòng đời ngắn tự động xóa sau 7 ngày.")
    add_bullet(doc, "/telecom/curated/: Chứa dữ liệu sạch chuẩn hóa định dạng cột Snappy Parquet phân vùng theo ngày và mã trạm (year=2026/month=09/day=18/province=HaNoi/tower_id=TOWER_001/).")
    add_bullet(doc, "/telecom/output/: Thư mục lưu trữ kết quả tính toán phân tán của các job MapReduce, Pig và Spark.")

    add_callout(
        doc,
        "Cơ chế dung lỗi và độ tin cậy HDFS",
        "Kích thước khối (Block Size) được thiết lập ở mức 128 MB nhằm giảm thiểu số lượng block và tải quản lý metadata trên bộ nhớ RAM của NameNode. Hệ số nhân bản (Replication Factor) được đặt bằng 3 theo Chính sách nhận biết mạng (Rack Awareness): Bản sao 1 nằm trên Node cục bộ ghi dữ liệu, Bản sao 2 nằm trên một Node khác cùng Rack, và Bản sao 3 nằm trên một Node ở Rack khác. NameNode duy trì liên lạc với DataNode thông qua tín hiệu nhịp tim (Heartbeat 3s) và báo cáo khối (Block Report). Nếu một DataNode ngừng hoạt động sau 10 phút 30 giây, NameNode sẽ tự động khởi tạo tiến trình nhân bản các khối dữ liệu bị thiếu sang các DataNode còn lại, bảo đảm an toàn dữ liệu tuyệt đối."
    )

    add_p(doc, "Bài toán tính toán dung lượng lưu trữ HDFS cho 500 trạm BTS:", bold_prefix="Tính toán dung lượng lưu trữ thực tế: ")
    add_bullet(doc, "Số lượng trạm BTS: 500 trạm; Mỗi trạm có trung bình 4 cell vô tuyến => Toàn mạng có: 2,000 cell.")
    add_bullet(doc, "Chu kỳ đo kiểm: 5 giây/lần/cell => Tần suất sinh dữ liệu toàn mạng: 400 sự kiện/giây.")
    add_bullet(doc, "Tổng số sự kiện sinh ra trong 1 ngày (86,400 giây): 2,000 * (86,400 / 5) = 34,560,000 sự kiện/ngày.")
    add_bullet(doc, "Dung lượng dữ liệu thô chưa nén (kích thước trung bình 256 bytes/sự kiện): 34,560,000 * 256 bytes = 8.847 GB/ngày.")
    add_bullet(doc, "Dung lượng sau khi nén chuẩn Snappy Parquet (giảm 65% dung lượng): 8.847 GB * 0.35 = 3.097 GB/ngày.")
    add_bullet(doc, "Dung lượng thực tế cần lưu trữ trên HDFS mỗi ngày (kèm 10% metadata và Replication Factor = 3): 3.097 GB * 1.10 * 3 = 10.22 GB HDFS/ngày.")
    add_bullet(doc, "Dung lượng lưu trữ dự tính cho 1 năm (365 ngày): 10.22 GB * 365 = 3.73 Terabyte HDFS. Dung lượng cho 3 năm hoạt động (dự phòng mở rộng mạng lưới 20%/năm): xấp xỉ 13.58 Terabyte.")

    add_h2(doc, "3.3. Thiết kế pipeline luồng dữ liệu đầu cuối (End-to-End)")
    add_p(doc, "Pipeline xử lý dữ liệu được thiết kế thành một chu trình khép kín gồm 5 giai đoạn liên hoàn từ khâu thu thập log thô đến khi xuất ra các bảng điều khiển nghiệp vụ:")

    add_fig(
        doc,
        img_name="hinh_3_1_pipeline_xu_ly.png",
        caption="Hình 3.1: Pipeline luồng dữ liệu đầu cuối từ Ingestion đến Analytics",
        width_in=6.5
    )

    add_p(doc, "Phân tích và nhận xét chi tiết luồng dữ liệu Hình 3.1:", bold_prefix="Nhận xét và phân tích Hình 3.1: ")
    add_bullet(doc, "Giai đoạn 1 (Thu thập - Ingestion): Flume Agent cấu hình Spooling Directory Source quét liên tục thư mục /var/log/telecom/, nạp sự kiện vào FileChannel bền vững và đẩy theo từng khối batch 1000 sự kiện qua HDFS Sink. Đối với luồng sự kiện nóng, cấu hình Dual Channel đẩy đồng thời vào HBase.")
    add_bullet(doc, "Giai đoạn 2 (Lưu trữ - Storage): Dữ liệu cập cảng HDFS tại /telecom/input/, tự động băm thành các khối 128 MB và nhân bản 3 lần.")
    add_bullet(doc, "Giai đoạn 3 (Làm sạch & ETL): Spark DataFrame và Pig Latin đọc song song dữ liệu, thực hiện kiểm tra tính hợp lệ và loại bỏ các bản ghi có thông lượng âm, độ trễ âm hoặc mất gói > 100%.")
    add_bullet(doc, "Giai đoạn 4 (Tính toán KPI): Thuật toán MapReduce và Spark SQL thực thi các phép gom nhóm (Group By) theo trạm phát sóng và công nghệ mạng, tính toán chỉ số CDR %, phân loại trạm lỗi.")
    add_bullet(doc, "Giai đoạn 5 (Phục vụ & Phân tích): Kết quả được nạp vào Apache HBase NoSQL (cho truy cập ngẫu nhiên độ trễ < 10 ms), SQLite Database (cho mô hình học máy R) và hiển thị trên BigSheets Dashboard.")

    add_h2(doc, "3.4. Cài đặt pipeline phân tích bằng Apache Spark & Spark SQL")
    add_p(doc, "Apache Spark là thành phần tính toán cốt lõi đảm nhiệm xử lý biến đổi dữ liệu quy mô lớn trong bộ nhớ. Chương trình telecom_spark_pipeline.py tận dụng tối đa hai cơ chế tối ưu hóa ngầm định mạnh mẽ của Spark là Catalyst Optimizer (tối ưu hóa cây kế hoạch logic và vật lý) và Tungsten Engine (quản lý bộ nhớ off-heap và sinh mã bytecode thực thi tức thời Whole-stage Code Generation).")

    add_p(doc, "Đoạn mã xử lý cốt lõi bằng PySpark thực hiện làm sạch, tính toán cột phái sinh và kết nối 4 bảng dữ liệu:", bold_prefix="Mã nguồn thực thi Spark: ")
    add_code(
        doc,
'''# Khởi tạo Spark Session với Catalyst Optimizer
spark = SparkSession.builder \\
    .appName("TelecomNetworkKpiAnalytics") \\
    .config("spark.sql.shuffle.partitions", "4") \\
    .getOrCreate()

# 1. Đọc và lọc sạch dữ liệu đo kiểm
df_events_clean = spark.read.option("header", "true").csv("/telecom/input/network_kpi_events.csv") \\
    .filter((col("latency_ms") >= 0.0) & (col("throughput_mbps") >= 0.0) & 
            (col("packet_loss_pct") >= 0.0) & (col("packet_loss_pct") <= 100.0)) \\
    .withColumn("session_volume_mb", round((col("throughput_mbps") * 5.0) / 8.0, 2))

# 2. Join 4 tập dữ liệu: Events, Towers, Cells và Complaints
df_joined = df_events_clean \\
    .join(df_towers, "tower_id", "inner") \\
    .join(df_cells, ["tower_id", "cell_id"], "inner") \\
    .join(df_complaints, ["tower_id", "cell_id"], "left")

# 3. Gom nhóm và tính toán chỉ số KPI bằng Spark SQL
df_joined.createOrReplaceTempView("v_kpi_telecom")
df_summary = spark.sql("""
    SELECT tower_id, province, technology,
           COUNT(event_id) AS total_sessions,
           ROUND(AVG(throughput_mbps), 2) AS avg_throughput_mbps,
           ROUND(AVG(latency_ms), 2) AS avg_latency_ms,
           ROUND(AVG(packet_loss_pct), 2) AS avg_packet_loss_pct,
           ROUND((SUM(call_dropped) / COUNT(event_id)) * 100.0, 3) AS call_drop_rate_pct,
           CASE WHEN ROUND((SUM(call_dropped) / COUNT(event_id)) * 100.0, 3) > 2.0 
                  OR ROUND(AVG(latency_ms), 2) > 80.0 THEN 'DEGRADED_QUALITY'
                ELSE 'NORMAL' END AS status_flag
    FROM v_kpi_telecom
    GROUP BY tower_id, province, technology
    ORDER BY call_drop_rate_pct DESC
""")''',
        caption="Đoạn mã 3.1: Kịch bản PySpark làm sạch, kết nối dữ liệu và tính toán KPI mạng"
    )

    add_h2(doc, "3.5. Các thành phần và thuật toán chuyên biệt trong đề tài")

    add_h3(doc, "3.5.1. Thuật toán MapReduce tối ưu tính KPI viễn thông")
    add_p(doc, "Mặc dù Apache Spark có tốc độ vượt trội, thuật toán Hadoop MapReduce (Java) vẫn là nền tảng chuẩn mực cho các tác vụ xử lý lô khổng lồ không bị áp lực thời gian. Để tính toán KPI viễn thông chính xác và tối ưu đường truyền mạng, nhóm đã thiết kế một giải pháp kỹ thuật tối ưu hóa MapReduce gồm 3 cải tiến quan trọng:")

    add_fig(
        doc,
        img_name="hinh_3_2_luong_mapreduce.png",
        caption="Hình 3.2: Sơ đồ luồng thuật toán MapReduce với Composite Key và Custom Partitioner",
        width_in=6.2
    )

    add_bullet(doc, "1. Khóa phức hợp (Composite Key - TowerTechKey): Thay vì chỉ sử dụng một khóa đơn giản, lớp TowerTechKey gói gọn hai trường (tower_id, technology) và hiện thực giao diện WritableComparable. Điều này cho phép sắp xếp tự nhiên theo thứ tự trạm BTS trước, sau đó sắp xếp theo thế hệ công nghệ (3G -> 4G -> 5G).")
    add_bullet(doc, "2. Bộ phân vùng tùy biến (Custom TowerPartitioner): Trong mạng viễn thông, một trạm BTS luôn phát sóng đồng thời cả 3G, 4G và 5G. Nếu dùng bộ băm mặc định, các công nghệ của cùng một trạm có thể bị phân tán sang các Reducer khác nhau. Bộ phân vùng tùy biến TowerPartitioner chỉ băm theo tower_id duy nhất: (key.getTowerId().hashCode() & Integer.MAX_VALUE) % numPartitions. Cơ chế này bảo đảm toàn bộ dữ liệu của một trạm tập trung về cùng một Reducer, triệt tiêu hoàn toàn hiện tượng lệch dữ liệu (Data Skew).")
    add_bullet(doc, "3. Bộ gộp cục bộ (Combiner): Chạy trực tiếp trên từng DataNode ngay sau pha Map, thực hiện cộng dồn sơ bộ thông lượng, độ trễ và số cuộc gọi rớt trước khi phát ra mạng. Cải tiến này giúp cắt giảm hơn 80% lưu lượng mạng I/O trong pha Shuffle.")

    add_h3(doc, "3.5.2. Kịch bản ETL và phân cụm trạm lỗi với Apache Pig Latin")
    add_p(doc, "Apache Pig cung cấp ngôn ngữ kịch bản luồng dữ liệu Pig Latin, giúp viết các tác vụ trích xuất và biến đổi (ETL) một cách ngắn gọn mà không cần viết hàng trăm dòng code Java MapReduce. Kịch bản telecom_kpi_analysis.pig nạp dữ liệu từ HDFS, lọc bỏ các giá trị dị thường, liên kết với danh mục trạm BTS và lọc ra danh sách các trạm có tỷ lệ rớt cuộc gọi vượt ngưỡng 2.0%:")
    add_code(
        doc,
'''-- Nạp dữ liệu và lọc sạch bằng Pig Latin
events_raw = LOAD '/telecom/input/network_kpi_events.csv' USING PigStorage(',') AS (
    event_id:chararray, timestamp:chararray, tower_id:chararray, cell_id:chararray,
    technology:chararray, throughput:double, latency:double, loss:double, drop:int, users:int);

events_clean = FILTER events_raw BY (latency >= 0.0) AND (throughput >= 0.0) AND (loss <= 100.0);
towers = LOAD '/telecom/input/bts_towers.csv' USING PigStorage(',') AS (tower_id:chararray, name:chararray, province:chararray);

-- Kết nối và gom nhóm theo Trạm và Công nghệ
joined = JOIN events_clean BY tower_id, towers BY tower_id;
grp = GROUP joined BY (events_clean::tower_id, events_clean::technology, towers::province);

kpi_summary = FOREACH grp GENERATE group.tower_id, group.province, group.technology,
    COUNT(joined) AS total_events,
    ROUND_TO(AVG(joined.events_clean::latency), 2) AS avg_lat,
    ROUND_TO((SUM(joined.events_clean::drop) * 100.0 / COUNT(joined)), 3) AS cdr_pct;

-- Lọc ra các trạm suy giảm chất lượng nghiêm trọng
degraded_towers = FILTER kpi_summary BY (cdr_pct > 2.0) OR (avg_lat > 80.0);
STORE degraded_towers INTO '/telecom/output/pig_degraded_towers' USING PigStorage('\\t');''',
        caption="Đoạn mã 3.2: Kịch bản Pig Latin lọc và phân cụm trạm suy giảm chất lượng"
    )

    add_h3(doc, "3.5.3. Thiết kế bảng Apache HBase phục vụ truy cập ngẫu nhiên")
    add_p(doc, "Trong khi HDFS tối ưu hóa cho các thao tác đọc quét tuần tự toàn bộ tệp (Sequential Scan), hệ thống giám sát NOC của nhà mạng lại đòi hỏi khả năng tra cứu ngẫu nhiên tức thời lịch sử chất lượng của một trạm BTS bất kỳ với độ trễ dưới 10 mili-giây. Để giải quyết bài toán này, nhóm đã thiết kế bảng NoSQL phân tán Apache HBase mang tên telecom_kpi_summary:")

    add_tbl(
        doc,
        headers=["Thành phần HBase", "Tên thiết kế / Giá trị", "Mô tả kỹ thuật & Ý nghĩa"],
        data=[
            ["Tên bảng (Table)", "telecom_kpi_summary", "Bảng NoSQL lưu trữ chỉ số KPI tổng hợp của từng trạm BTS."],
            ["RowKey Pattern", "reverse(tower_id) + '_' + technology", "VD: '100_REWOT_4G'. Đảo ngược chuỗi tower_id để phân tán đều các khóa trên các RegionServer, triệt tiêu hiện tượng thắt cổ chai ghi tập trung (Hotspotting)."],
            ["Column Family 1", "kpi_metrics", "Chứa các chỉ số chất lượng dịch vụ: avg_throughput, avg_latency, avg_packet_loss, call_drop_rate, active_users."],
            ["Column Family 2", "status_flags", "Chứa các cờ trạng thái phục vụ cảnh báo: health_category, has_complaint, degradation_flag."],
            ["Cơ chế lưu trữ", "LSM-Tree & MemStore", "Dữ liệu ghi vào MemStore và WAL (Write-Ahead-Log) trước khi đẩy xuống HFile, đạt tốc độ truy xuất cực nhanh < 10 ms."],
        ],
        caption="Bảng 3.1: Thiết kế bảng Apache HBase lưu trữ chỉ số KPI viễn thông độ trễ thấp",
        col_widths=[1.5, 2.0, 2.8]
    )

    add_h3(doc, "3.5.4. Mô phỏng phân tích nghiệp vụ tương tác với BigSheets")
    add_p(doc, "IBM BigSheets là công cụ phân tích dữ liệu lớn trên giao diện bảng tính (Spreadsheet) dành cho các nhà phân tích nghiệp vụ mà không cần viết mã lệnh phức tạp. Nhóm đã xây dựng chương trình mô phỏng tương đương bằng Web Application tương tác (bigsheets/web_app/) kết hợp với Spark DataFrame:")

    add_fig(
        doc,
        img_name="bigsheets_dashboard_preview.jpg",
        caption="Hình 3.3: Giao diện mô phỏng Dashboard phân tích nghiệp vụ BigSheets",
        width_in=6.4
    )

    add_p(doc, "Quy trình nghiệp vụ mô phỏng ánh xạ chính xác 1-1 với các khái niệm của BigSheets:", bold_prefix="Nhận xét giao diện Hình 3.3: ")
    add_bullet(doc, "Collection Definition -> Spark DataFrame: Tạo tập dữ liệu gốc từ nguồn HDFS không cần code.")
    add_bullet(doc, "Calculated Column -> withColumn(): Tạo các cột tính toán nghiệp vụ (session_volume_mb, cdr_pct, qos_score).")
    add_bullet(doc, "Filter Sheet -> filter(): Lọc bỏ dữ liệu lỗi âm và lọc theo ngưỡng cảnh báo.")
    add_bullet(doc, "Group / Pivot Sheet -> groupBy() & agg(): Tổng hợp KPI đa chiều theo tỉnh thành, trạm và công nghệ.")
    add_bullet(doc, "Chart Visualization: Tự động vẽ biểu đồ trực quan hóa xu hướng phục vụ báo cáo quản trị.")

    add_h3(doc, "3.5.5. Mô hình Hồi quy Logistic dự báo khiếu nại bằng R & SQLite")
    add_p(doc, "Ngôn ngữ R kết hợp cơ sở dữ liệu SQLite đảm nhiệm khâu phân tích khoa học dữ liệu chuyên sâu và dự báo nguy cơ phát sinh khiếu nại khách hàng. Kịch bản telecom_analysis.R sử dụng thư viện DBI và RSQLite để kết nối vào tệp CSDL telecom_network.sqlite, thực thi truy vấn SQL có INNER JOIN 3 bảng và GROUP BY theo (tower_id, technology). Dữ liệu sau đó được tiền xử lý bằng dplyr/tidyr và đưa vào mô hình Học máy Hồi quy Logistic (Logistic Regression) với hàm liên kết Logit:")
    add_p(doc, "$$\\ln\\left(\\frac{P}{1 - P}\\right) = \\beta_0 + \\beta_1 \\cdot \\text{Latency} + \\beta_2 \\cdot \\text{PacketLoss} + \\beta_3 \\cdot \\text{Throughput} + \\beta_4 \\cdot \\text{ActiveUsers}$$", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "Trong đó, P là xác suất trạm BTS phát sinh khiếu nại từ khách hàng (has_complaint = 1). Mô hình giúp Trung tâm CSKH chủ động khoanh vùng các trạm có xác suất P > 0.5 để điều phối kỹ sư xử lý trước khi khách hàng gọi điện phản ánh.")

    add_h2(doc, "3.6. Cơ chế lưu trữ và xuất kết quả đa tầng")
    add_p(doc, "Hệ thống kết xuất và lưu trữ dữ liệu đầu ra theo kiến trúc đa tầng (Multi-tier Serving Architecture) phù hợp với từng mục đích khai thác:")
    add_bullet(doc, "Tầng Lưu trữ Lô (HDFS): Lưu trữ kết quả tổng hợp dưới dạng CSV và nén Parquet tại /telecom/output/ phục vụ lưu trữ vĩnh viễn và kiểm toán dữ liệu.")
    add_bullet(doc, "Tầng Tra cứu Thời gian thực (HBase): Cung cấp API truy vấn chỉ số theo trạm cho Dashboard giám sát NOC thời gian thực.")
    add_bullet(doc, "Tầng Quan hệ & Thống kê (SQLite Database): Bảng kpi_analysis_summary trong file telecom_network.sqlite lưu trữ kết quả phân tích thống kê và xác suất khiếu nại dự báo từ R.")
    add_bullet(doc, "Tầng Báo cáo Trực quan: Tự động kết xuất 2 biểu đồ PNG chất lượng cao (chart1_latency_by_tech.png và chart2_packet_loss_vs_drop_rate.png) cùng bảng tổng hợp Power BI (telecom_kpi_summary_powerbi.csv).")

print("Module 2 (Chap 2 & Chap 3) loaded successfully.")
