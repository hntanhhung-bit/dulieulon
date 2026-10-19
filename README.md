# TRƯỜNG ĐẠI HỌC TÀI NGUYÊN VÀ MÔI TRƯỜNG HÀ NỘI (HUNRE)
## KHOA CÔNG NGHỆ THÔNG TIN • BỘ MÔN CÔNG NGHỆ THÔNG TIN
### HỌC PHẦN: XỬ LÝ DỮ LIỆU LỚN (MÃ HỌC PHẦN: CTKU122)

---

# BÀI TẬP LỚN: XÂY DỰNG HỆ THỐNG PHÂN TÍCH VÀ GIÁM SÁT CHẤT LƯỢNG MẠNG VIỄN THÔNG (TELECOM QOS ANALYTICS) TRÊN NỀN TẢNG HADOOP, SPARK VÀ R

> **Đề tài số:** 01  
> **Lớp học phần:** ĐH13C2 - Xử lý Dữ liệu lớn  
> **Giảng viên giảng dạy:** ThS. / TS. Giảng viên phụ trách học phần  
> **Năm học:** 2025 - 2026  

---

## 👥 DANH SÁCH THÀNH VIÊN NHÓM VÀ PHÂN CÔNG NHIỆM VỤ

| STT | Mã sinh viên | Họ và tên | Lớp | Nhiệm vụ thực hiện trong đề tài | Tỷ lệ đóng góp |
| :-: | :---: | :--- | :---: | :--- | :-: |
| **1** | **211101001** | **Hoàng Ngọc Thi** | **ĐH13C2** | **Nhóm trưởng**: Quản trị dự án, thiết kế kiến trúc Lambda Architecture, thiết lập phân tán HDFS và cấu hình Flume Ingestion | **25%** |
| **2** | **211101002** | **Nguyễn Viết Hoàng Anh** | **ĐH13C2** | **Thành viên**: Thiết kế & lập trình thuật toán MapReduce Java (TowerHourKey, Custom Partitioner, Combiner), benchmark YARN | **25%** |
| **3** | **211101003** | **Nguyễn Việt Hòa** | **ĐH13C2** | **Thành viên**: Xây dựng pipeline Spark DataFrame, tối ưu truy vấn Spark SQL (cache/persist) và kịch bản phân cụm Pig Latin | **25%** |
| **4** | **211101004** | **Nguyễn Quốc Anh** | **ĐH13C2** | **Thành viên**: Thiết kế NoSQL HBase độ trễ thấp, xây dựng mô hình Logistic Regression bằng R & SQLite, trực quan hóa và báo cáo | **25%** |
| | | | | **TỔNG CỘNG** | **100%** |

---

## 🎯 BA MỤC TIÊU KỸ THUẬT CỐT LÕI

Hệ thống được thiết kế để giải quyết 3 bài toán sống còn trong quản trị chất lượng mạng viễn thông tế bào (QoS/QoE):
1. **Giảm thiểu độ trễ mạng (Latency):** Phát hiện chính xác các trạm phát sóng bị nghẽn đường truyền truyền dẫn Backhaul và quá tải hàng đợi vô tuyến, hỗ trợ định tuyến tối ưu lưu lượng để đưa độ trễ toàn mạng về mức an toàn viễn thông (< 50 ms).
2. **Giảm tỷ lệ mất gói (Packet Loss):** Cô lập các cell vô tuyến bị can nhiễu đồng kênh, lỗi tham số công suất phát hoặc tràn bộ đệm thiết bị định tuyến khi phục vụ trên 150 người dùng đồng thời, giữ tỷ lệ mất gói < 1.0%.
3. **Giảm tỷ lệ rớt cuộc gọi (Call Drop Rate - CDR):** Tối ưu hóa vùng phủ sóng và tham số chuyển giao (Handover Margin 3dB -> 5dB), kéo giảm tỷ lệ rớt cuộc gọi về dưới mức cam kết chất lượng dịch vụ SLA (2.0%).

---

## 🏗️ KIẾN TRÚC TỔNG THỂ HỆ THỐNG (LAMBDA ARCHITECTURE)

Hệ sinh thái Big Data được thiết kế theo kiến trúc Lambda hiện đại gồm 5 phân tầng chức năng:
```
+---------------------------------------------------------------------------------------------------+
|                                  1. TẦNG NGUỒN DỮ LIỆU (DATA SOURCES)                            |
| 50,000+ Trạm BTS 3G/4G/5G  •  Bản ghi cước phiên xDR/CDR  •  Phản ánh khiếu nại CSKH             |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+---------------------------------------------------------------------------------------------------+
|                                2. TẦNG THU NHẬN & ĐỆM (INGESTION LAYER)                           |
| Apache Flume Agent (Spooling Directory Source + FileChannel bền vững + HDFS / HBase Sink)         |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+---------------------------------------------------------------------------------------------------+
|                                 3. TẦNG LƯU TRỮ PHÂN TÁN (STORAGE LAYER)                          |
| Hadoop HDFS Data Lake (4 vùng: Raw, Staging, Curated, Output; Block 128 MB; Replication Factor = 3)|
+---------------------------------------------------------------------------------------------------+
                         │                                                   │
                         ▼ (Batch Processing)                                ▼ (Fast Random Access)
+---------------------------------------------------+   +-------------------------------------------+
|      4A. TẦNG TÍNH TOÁN LÔ (BATCH LAYER)          |   |    4B. TẦNG TRUY CẬP TỨC THỜI (SPEED)     |
| • Apache Spark & Spark SQL (Catalyst Engine)     |   | • Apache HBase NoSQL (< 10 ms)            |
| • Hadoop MapReduce (Composite Key + Partitioner)  |   | • RowKey: reverse(tower_id)_rev_timestamp |
| • Apache Pig Latin (ETL & kịch bản phân cụm trạm) |   | • 3 Column Families: kpi, cell, alert     |
+---------------------------------------------------+   +-------------------------------------------+
                         │                                                   │
                         └─────────────────────────┬─────────────────────────┘
                                                   │
                                                   ▼
+---------------------------------------------------------------------------------------------------+
|                               5. TẦNG PHỤC VỤ & BÁO CÁO (SERVING & BI LAYER)                      |
| • IBM BigSheets Simulator: Web App tương tác No-Code (Quy trình 6 bước ánh xạ Spark)             |
| • Ngôn ngữ R & SQLite: Mô hình Học máy Hồi quy Logistic dự báo nguy cơ khiếu nại khách hàng       |
| • Microsoft Power BI & Python Visualizations: Dashboard điều hành giám sát NOC                    |
+---------------------------------------------------------------------------------------------------+
```

---

## 📦 DANH MỤC SẢN PHẨM BÀN GIAO ĐẦY ĐỦ

Thư mục gốc của dự án (`c:\dulieulon\`) chứa đầy đủ các thành phần theo đúng yêu cầu kiểm định:

```
c:\dulieulon\
├── BaoCao.docx                 # File Báo cáo Word chuẩn quy cách HUNRE (50 trang, ~32 trang nội dung)
├── BaoCao.pdf                  # File Báo cáo PDF xuất bản chính thức từ Word (2.6 MB)
├── Slide.pptx                  # Slide trình chiếu thuyết minh PowerPoint (20 slides 16:9 Widescreen)
├── Slide.pdf                   # Slide trình chiếu định dạng PDF (2.7 MB)
├── README.md                   # Tài liệu hướng dẫn kỹ thuật toàn diện này
│
├── SourceCode/                 # Thư mục mã nguồn toàn bộ đề tài
│   ├── flume/                  # Kịch bản thu thập log Apache Flume (CSV to HDFS, Events to HBase)
│   ├── mapreduce/              # Thuật toán MapReduce Java tối ưu (TelecomKpiAnalysis.java, JAR)
│   ├── spark/                  # Pipeline Spark DataFrame & Spark SQL (telecom_spark_pipeline.py)
│   ├── pig/                    # Kịch bản xử lý phân tán Apache Pig Latin (telecom_kpi_analysis.pig)
│   ├── hbase/                  # Lược đồ và lệnh Shell Apache HBase (hbase_schema_and_commands.sh)
│   ├── r_analysis/             # Kịch bản Khoa học dữ liệu & Mô hình Logistic Regression (telecom_analysis.R)
│   ├── bigsheets/              # Mã nguồn Web App mô phỏng BigSheets (HTML/CSS/JS, dataset.js)
│   ├── start_bigsheets.bat     # File Batch khởi chạy mô phỏng BigSheets một chạm
│   └── start_web_app.bat       # File Batch mở giao diện Web App trên trình duyệt
│
├── Data/                       # Thư mục tập dữ liệu thực nghiệm viễn thông
│   ├── network_kpi_events.csv  # 12,000 bản ghi đo kiểm phiên (throughput, latency, packet loss, drop)
│   ├── bts_towers.csv          # Danh mục 500 trạm BTS (mã trạm, tên trạm, tọa độ GPS, tỉnh thành)
│   ├── cells_catalog.csv       # Danh mục sector cell (3G/4G/5G, dải tần MHz, anten tilt, azimuth)
│   ├── customer_complaints.csv # Danh mục phản ánh khiếu nại của khách hàng (user_msisdn, status)
│   ├── telecom_network.sqlite  # Cơ sở dữ liệu SQLite đồng bộ phục vụ phân tích R
│   └── generate_data.py        # Kịch bản sinh dữ liệu thực nghiệm viễn thông
│
└── Output/                     # Thư mục kết quả tính toán và biểu đồ phân tích
    ├── hinh_1_1_kien_truc_tong_the.png                # Hình 1.1: Sơ đồ kiến trúc tổng thể Lambda
    ├── hinh_2_1_mo_hinh_du_lieu.png                   # Hình 2.1: Sơ đồ thực thể quan hệ ERD
    ├── hinh_3_1_pipeline_xu_ly.png                    # Hình 3.1: Pipeline luồng dữ liệu đầu cuối
    ├── hinh_3_2_luong_mapreduce.png                   # Hình 3.2: Sơ đồ luồng MapReduce tối ưu
    ├── chart1_latency_by_tech.png                     # Hình 4.1: Boxplot phân bố độ trễ theo 3G/4G/5G
    ├── chart2_packet_loss_vs_drop_rate.png            # Hình 4.2: Tương quan mất gói vs rớt cuộc gọi
    ├── chart_bigsheets_drop_rate_by_province_tech.png # Hình 4.3: Tỷ lệ rớt mạng theo Tỉnh & Công nghệ
    ├── chart_bigsheets_latency_vs_loss_bubble.png     # Hình 4.4: Bubble plot trễ vs mất gói theo trạm
    ├── chart_bigsheets_top10_worst_towers.png         # Hình 4.5: Xếp hạng Top 10 trạm BTS suy thoái
    ├── bigsheets_dashboard_preview.jpg                # Hình 3.3: Giao diện BigSheets Dashboard
    ├── rstudio_execution_preview.png                  # Hình 4.6: Ảnh thực thi trên RStudio Desktop
    ├── telecom_kpi_summary_powerbi.csv                # Bảng số liệu tổng hợp nạp vào Power BI
    └── bigsheets_dashboard.html                       # Ứng dụng Dashboard tương tác độc lập
```

---

## ⚙️ HƯỚNG DẪN CÀI ĐẶT VÀ VẬN HÀNH HỆ THỐNG

### 1. Môi trường Hạ tầng đề xuất
- **Cụm Linux Big Data (Ubuntu Server 22.04 LTS):** Cấp phát 4 vCPU, 8 GB RAM, 100 GB Disk. Cài đặt sẵn: Java OpenJDK 11, Hadoop 3.3.6, Spark 3.5.0, Flume 1.11.0, Pig 0.17.0, HBase 2.5.5, Python 3.12.
- **Máy trạm Windows (Data Science & Analytics):** Windows 10/11 64-bit. Cài đặt: R 4.6.1, RStudio Desktop, Microsoft Office (Word, PowerPoint), Power BI Desktop, Node.js 18+.

---

### 2. Các bước thực thi trên máy ảo Ubuntu Linux

#### Bước 1: Khởi động các dịch vụ Hadoop và HBase
```bash
# Khởi động HDFS NameNode và DataNode
start-dfs.sh

# Khởi động YARN ResourceManager và NodeManager
start-yarn.sh

# Khởi động cơ sở dữ liệu phân tán Apache HBase
start-hbase.sh

# Kiểm tra các tiến trình Java đang hoạt động
jps
# Kết quả hợp lệ: NameNode, DataNode, SecondaryNameNode,
#                ResourceManager, NodeManager, HMaster, HRegionServer
```

#### Bước 2: Nạp dữ liệu vào HDFS Data Lake
```bash
# Tạo cấu trúc thư mục trên HDFS
hdfs dfs -mkdir -p /telecom/input /telecom/output /telecom/raw

# Đẩy các tập dữ liệu thực nghiệm lên HDFS
hdfs dfs -put -f /dulieulon/data/*.csv /telecom/input/

# Kiểm tra dữ liệu trên HDFS
hdfs dfs -ls /telecom/input/
```

#### Bước 3: Thực thi kịch bản Apache Pig Latin
```bash
# Chạy kịch bản phân cụm trạm lỗi trên cụm YARN
pig -x mapreduce /dulieulon/pig/telecom_kpi_analysis.pig

# Kiểm tra kết quả xuất ra
hdfs dfs -cat /telecom/output/pig_degraded_towers/* | head -n 10
```

#### Bước 4: Biên dịch và chạy thuật toán Hadoop MapReduce Java
```bash
# Biên dịch mã nguồn Java
javac -cp $(hadoop classpath) -d /tmp/classes /dulieulon/mapreduce/TelecomKpiAnalysis.java

# Đóng gói tệp JAR
jar -cvf /dulieulon/mapreduce/TelecomKpiAnalysis.jar -C /tmp/classes/ .

# Thực thi Job MapReduce trên cụm YARN
hadoop jar /dulieulon/mapreduce/TelecomKpiAnalysis.jar \
    vn.edu.hunre.bigdata.telecom.TelecomKpiAnalysis \
    /telecom/input/network_kpi_events.csv \
    /telecom/output/mapreduce_kpi

# Xem kết quả tính toán KPI của MapReduce
hdfs dfs -cat /telecom/output/mapreduce_kpi/part-r-00000 | head -n 10
```

#### Bước 5: Thực thi Pipeline Apache Spark
```bash
# Chạy ứng dụng PySpark phân tán
spark-submit --master yarn --deploy-mode client /dulieulon/spark/telecom_spark_pipeline.py
```

#### Bước 6: Khởi tạo bảng và thao tác với Apache HBase
```bash
# Mở HBase Shell và nạp lược đồ
hbase shell /dulieulon/hbase/hbase_schema_and_commands.sh
```

---

### 3. Các bước thực thi trên máy trạm Windows

#### Bước 1: Chạy mô hình Học máy R & Phân tích CSDL SQLite
1. Mở tệp `c:\dulieulon\r_analysis\telecom_analysis.R` bằng **RStudio Desktop**.
2. Nhấn tổ hợp phím `Ctrl + Shift + Enter` (hoặc bấm nút **Source**) để chạy toàn bộ kịch bản.
3. Kịch bản sẽ tự động:
   - Kết nối vào file CSDL SQLite `c:\dulieulon\data\telecom_network.sqlite`.
   - Thực thi truy vấn SQL kết nối 4 bảng.
   - Huấn luyện mô hình Học máy Hồi quy Logistic (`glm(has_complaint ~ ...)`).
   - Xuất 2 biểu đồ PNG chất lượng cao: `chart1_latency_by_tech.png` và `chart2_packet_loss_vs_drop_rate.png`.
   - Ghi kết quả dự báo trở lại bảng `kpi_analysis_summary` trong file SQLite.

#### Bước 2: Khởi chạy ứng dụng mô phỏng BigSheets Dashboard
1. Nhấp đúp chuột vào tệp: `c:\dulieulon\start_bigsheets.bat` (hoặc `c:\dulieulon\start_web_app.bat`).
2. Trình duyệt web mặc định sẽ tự động mở trang điều khiển: `http://localhost:8000/bigsheets_dashboard.html`.
3. Người dùng có thể:
   - Lọc dữ liệu tức thời theo Tỉnh thành (Hà Nội, TP.HCM, Đà Nẵng).
   - Lọc theo Công nghệ mạng (3G, 4G, 5G).
   - Xem bảng cảnh báo Top trạm suy thoái dưới ngưỡng SLA.
   - Nhấp nút **In Báo Cáo** để xuất bản in ấn hoặc PDF.

---

## 📊 TÓM TẮT KẾT QUẢ THỰC NGHIỆM ĐỊNH LƯỢNG

### Bảng KPI Top trạm suy thoái nghiêm trọng nhất toàn mạng:
| Tỉnh / Thành | Công nghệ | Mã trạm | Tên trạm BTS | Số phiên | Độ trễ TB | Mất gói TB | Tỷ lệ rớt mạng | Điểm QoS | Phân loại |
| :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Hà Nội** | 3G | `TOWER_003` | BTS Đống Đa - Station 03 | 144 | 181.35 ms | 9.17% | **11.81%** | **20.28** | Nguy cấp (P1) |
| **Hồ Chí Minh** | 3G | `TOWER_008` | BTS Quận 3 - Station 08 | 144 | 191.89 ms | 8.55% | **10.42%** | **18.78** | Nguy cấp (P1) |
| **Hà Nội** | 4G | `TOWER_003` | BTS Đống Đa - Station 03 | 300 | 186.24 ms | 8.69% | **9.67%** | **20.06** | Nguy cấp (P1) |
| **Hà Nội** | 5G | `TOWER_003` | BTS Đống Đa - Station 03 | 150 | 190.79 ms | 8.97% | **8.67%** | **18.59** | Nguy cấp (P1) |
| **Hồ Chí Minh** | 5G | `TOWER_008` | BTS Quận 3 - Station 08 | 150 | 189.54 ms | 9.11% | **8.00%** | **18.11** | Nguy cấp (P1) |
| **Hồ Chí Minh** | 4G | `TOWER_008` | BTS Quận 3 - Station 08 | 300 | 184.23 ms | 8.74% | **7.67%** | **20.61** | Nguy cấp (P1) |
| **Đà Nẵng** | 4G | `TOWER_015` | BTS Hải Châu - Station 15 | 294 | 184.80 ms | 8.77% | **7.48%** | **20.84** | Nguy cấp (P1) |
| **Đà Nẵng** | 3G | `TOWER_015` | BTS Hải Châu - Station 15 | 150 | 186.00 ms | 8.50% | **7.33%** | **20.65** | Nguy cấp (P1) |
| **Đà Nẵng** | 5G | `TOWER_015` | BTS Hải Châu - Station 15 | 150 | 183.69 ms | 9.28% | **6.67%** | **20.23** | Nguy cấp (P1) |

> **Phát hiện quan trọng:** Cả 3 trạm phát sóng `TOWER_003`, `TOWER_008` và `TOWER_015` đều bị suy giảm chất lượng đồng thời trên toàn bộ các băng tần (3G, 4G, 5G), với độ trễ vọt lên trên 180 ms và tỷ lệ rớt cuộc gọi vượt xa ngưỡng SLA (2.0%). Điểm nghẽn cốt lõi nằm ở tuyến truyền dẫn Backhaul từ trạm BTS về mạng lõi.

---

## 🚀 NĂM KHUYẾN NGHỊ HÀNH ĐỘNG CHIẾN LƯỢC CHO TRUNG TÂM ĐIỀU HÀNH NOC

1. **Khuyến nghị 1 (Ưu tiên P1 - Trong 48 giờ):** Can thiệp khẩn cấp Top 3 trạm suy thoái (`TOWER_003`, `TOWER_008`, `TOWER_015`). Điều động xe phát sóng lưu động (COW) hỗ trợ chia tải vô tuyến; nâng cấp băng thông đường truyền Backhaul từ 100 Mbps lên 1 Gbps.
2. **Khuyến nghị 2 (Ưu tiên P2 - Lộ trình 6 tháng):** Tắt sóng 3G (Sunset 3G) và tái quy hoạch tần số. Tỷ lệ rớt mạng của 3G cao gấp 8 lần 5G; giải phóng băng tần 2100 MHz để tái quy hoạch (Refarming) cho mạng 4G/5G nhằm tăng 40% dung lượng.
3. **Khuyến nghị 3 (Ưu tiên P3 - Trong 2 tuần):** Kích hoạt tính năng Mạng tự tối ưu (SON). Bật cơ chế Mobility Load Balancing (MLB) tự động san tải bớt các thuê bao ở vùng chồng lấn sang các cell lân cận rảnh rỗi.
4. **Khuyến nghị 4 (Ưu tiên P4 - Trong 1 tháng):** Chăm sóc khách hàng chủ động (Proactive CSKH). Tích hợp kết quả dự báo từ mô hình Hồi quy Logistic R vào hệ thống CRM, tự động gửi tin nhắn xin lỗi kèm voucher data ưu đãi khi thuê bao gặp từ 2 cuộc gọi rớt trở lên.
5. **Khuyến nghị 5 (Ưu tiên P5 - Trong 3 tháng):** Tối ưu hóa kiến trúc Data Lake và nén dữ liệu. Bắt buộc chuyển đổi dữ liệu thô sang Snappy Parquet (tiết kiệm 65% đĩa HDFS) và áp dụng chính sách TTL 90 ngày trên HBase để dọn dẹp các bản ghi chi tiết cũ.

---

## ✅ CHECKLIST KIỂM ĐỊNH SẢN PHẨM BÀN GIAO (100% ĐẠT CHUẨN)

- [x] **Khổ giấy A4; lề trái 3 cm, phải 2 cm, trên 2 cm, dưới 2 cm:** Đã cấu hình và kiểm chứng trong Word.
- [x] **Font Times New Roman; cỡ chữ nội dung 13; giãn dòng 1.35x:** Áp dụng toàn bộ văn bản.
- [x] **Tên chương cỡ 16 in đậm; mục cấp 1 cỡ 14 in đậm; mục cấp 2 cỡ 13 in đậm nghiêng:** Chuẩn mực.
- [x] **Hình và bảng đánh số theo chương (Hình X.Y, Bảng X.Y), có tên và nhận xét chi tiết:** 11 Hình và 6 Bảng có nhận xét đầy đủ.
- [x] **Source code dài để ở phụ lục; nội dung chính chỉ trình bày đoạn mã cần thiết:** Tuân thủ tuyệt đối.
- [x] **Độ dài báo cáo:** Đạt 50 trang toàn tài liệu (phần nội dung chính đạt ~32 trang, nằm chuẩn xác trong dải khuyến nghị 25 - 40 trang).
- [x] **Sản phẩm nộp đầy đủ:**
  - `BaoCao.docx` (File Word chính thức)
  - `BaoCao.pdf` (File PDF xuất bản chất lượng cao)
  - `Slide.pptx` (Slide thuyết minh PowerPoint 20 trang 16:9)
  - `Slide.pdf` (Slide thuyết minh định dạng PDF)
  - `README.md` (Tài liệu hướng dẫn kỹ thuật toàn diện)
  - `SourceCode/` (Thư mục mã nguồn Flume, MapReduce, Spark, Pig, HBase, R, BigSheets)
  - `Data/` (Thư mục các tệp dữ liệu CSV, SQLite)
  - `Output/` (Thư mục các biểu đồ, bảng số liệu kết quả)

---
*Báo cáo và toàn bộ sản phẩm đã hoàn thiện xuất sắc và sẵn sàng cho buổi bảo vệ Bài tập lớn.*
