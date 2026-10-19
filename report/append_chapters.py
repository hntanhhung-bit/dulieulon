def build_chapter_3(doc):
    # --------------------------------------------------------------------------
    # CHƯƠNG 3. XÂY DỰNG HỆ THỐNG XỬ LÝ DỮ LIỆU LỚN
    # --------------------------------------------------------------------------
    add_h1("CHƯƠNG 3. XÂY DỰNG HỆ THỐNG XỬ LÝ DỮ LIỆU LỚN")
    
    add_h2("3.1. Thiết lập môi trường triển khai thực nghiệm")
    add_p("Hệ thống được thiết kế và triển khai theo mô hình kiến trúc phân tán lai ghép (Hybrid Architecture) kết hợp giữa Cụm máy ảo Linux và Máy trạm Windows:")
    add_bullet("Hạ tầng Cụm Big Data (Ubuntu Server 22.04 LTS): Đóng vai trò là cụm xử lý phân tán chính (`masternode` tại địa chỉ IP `192.168.231.132`), cấp phát 4 vCPU, 8 GB RAM và 100 GB dung lượng lưu trữ trên nền tảng VMware Workstation Pro. Cụm vận hành đầy đủ hệ sinh thái: Apache Hadoop 3.3.6 (NameNode, DataNode, YARN ResourceManager, NodeManager), Apache Spark 3.5.0, Apache Flume 1.11.0, Apache Pig 0.17.0 và Apache HBase 2.5.5 trên nền Java OpenJDK 11 và Python 3.12.")
    add_bullet("Hạ tầng Máy trạm Phân tích (Windows 11 Host): Đóng vai trò là môi trường Khoa học dữ liệu (Data Science Workstation), vận hành R 4.6.1, RStudio Desktop 2026.09.0, Node.js 18+ và Power BI để kết nối dữ liệu từ xa, huấn luyện mô hình học máy và xây dựng Dashboard điều hành.")

    add_h2("3.2. Tổ chức lưu trữ phân tán và cơ chế dung lỗi trên HDFS")
    add_p("Hệ thống tệp phân tán HDFS đóng vai trò là kho lưu trữ dữ liệu trung tâm (Data Lake). Cây thư mục trên HDFS được tổ chức khoa học theo chuẩn kiến trúc dữ liệu doanh nghiệp:")
    add_bullet("`/telecom/raw/`: Chứa các tệp log thô được đẩy liên tục từ các trạm BTS thông qua Apache Flume.")
    add_bullet("`/telecom/input/`: Chứa các tệp dữ liệu đã được làm sạch sơ bộ: `network_kpi_events.csv`, `bts_towers.csv`, `cells_catalog.csv` và `customer_complaints.csv`.")
    add_bullet("`/telecom/output/`: Thư mục lưu trữ kết quả tính toán phân tán của các job MapReduce, Pig và Spark.")
    add_bullet("`/telecom/archive/`: Lưu trữ dữ liệu lịch sử nén dưới định dạng cột tối ưu Snappy Parquet phục vụ phân tích xu hướng dài hạn.")

    add_callout(
        "Cơ chế dung lỗi và độ tin cậy HDFS",
        "Kích thước khối (Block Size) được thiết lập ở mức 128 MB nhằm giảm thiểu số lượng block và tải quản lý metadata trên bộ nhớ RAM của NameNode. Hệ số nhân bản (Replication Factor) được đặt bằng 3 theo Chính sách nhận biết mạng (Rack Awareness): Bản sao 1 nằm trên Node cục bộ ghi dữ liệu, Bản sao 2 nằm trên một Node khác cùng Rack, và Bản sao 3 nằm trên một Node ở Rack khác. NameNode duy trì liên lạc với DataNode thông qua tín hiệu nhịp tim (Heartbeat 3s) và báo cáo khối (Block Report). Nếu một DataNode ngừng hoạt động sau 10 phút 30 giây, NameNode sẽ tự động khởi tạo tiến trình nhân bản các khối dữ liệu bị thiếu sang các DataNode còn lại, bảo đảm an toàn dữ liệu tuyệt đối."
    )

    add_h2("3.3. Thiết kế pipeline luồng dữ liệu đầu cuối (End-to-End)")
    add_p("Pipeline xử lý dữ liệu được thiết kế thành một chu trình khép kín gồm 5 giai đoạn liên hoàn từ khâu thu thập log thô đến khi xuất ra các bảng điều khiển nghiệp vụ:")

    add_fig(
        img_name="hinh_3_1_pipeline_xu_ly.png",
        caption="Hình 3.1: Pipeline luồng dữ liệu đầu cuối từ Ingestion đến Analytics",
        width_in=6.5
    )

    add_bullet("Giai đoạn 1 (Thu thập - Ingestion): Flume Agent cấu hình Spooling Directory Source quét liên tục thư mục `/var/log/telecom/`, nạp sự kiện vào Memory Channel và đẩy theo từng khối batch 1000 sự kiện qua HDFS Sink.")
    add_bullet("Giai đoạn 2 (Lưu trữ - Storage): Dữ liệu cập cảng HDFS tại `/telecom/input/`, tự động băm thành các khối 128 MB và nhân bản 3 lần.")
    add_bullet("Giai đoạn 3 (Làm sạch & ETL): Spark DataFrame và Pig Latin đọc song song dữ liệu, thực hiện kiểm tra tính hợp lệ và loại bỏ các bản ghi có thông lượng âm, độ trễ âm hoặc mất gói > 100%.")
    add_bullet("Giai đoạn 4 (Tính toán KPI): Thuật toán MapReduce và Spark SQL thực thi các phép gom nhóm (Group By) theo trạm phát sóng và công nghệ mạng, tính toán chỉ số CDR %, phân loại trạm lỗi.")
    add_bullet("Giai đoạn 5 (Phục vụ & Phân tích): Kết quả được nạp vào Apache HBase NoSQL (cho truy cập ngẫu nhiên độ trễ < 10 ms), SQLite Database (cho mô hình học máy R) và hiển thị trên BigSheets Dashboard.")

    add_h2("3.4. Cài đặt pipeline phân tích bằng Apache Spark & Spark SQL")
    add_p("Apache Spark là thành phần tính toán cốt lõi đảm nhiệm xử lý biến đổi dữ liệu quy mô lớn trong bộ nhớ. Chương trình `telecom_spark_pipeline.py` tận dụng tối đa hai cơ chế tối ưu hóa ngầm định mạnh mẽ của Spark là Catalyst Optimizer (tối ưu hóa cây kế hoạch logic và vật lý) và Tungsten Engine (quản lý bộ nhớ off-heap và sinh mã bytecode thực thi tức thời Whole-stage Code Generation).")

    add_p("Đoạn mã xử lý cốt lõi bằng PySpark thực hiện làm sạch, tính toán cột phái sinh và kết nối 4 bảng dữ liệu:", bold_prefix="Mã nguồn thực thi Spark: ")
    add_code(
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

    add_h2("3.5. Các thành phần và thuật toán chuyên biệt trong đề tài")

    add_h3("3.5.1. Thuật toán MapReduce tối ưu tính KPI viễn thông")
    add_p("Mặc dù Apache Spark có tốc độ vượt trội, thuật toán Hadoop MapReduce (Java) vẫn là nền tảng chuẩn mực cho các tác vụ xử lý lô khổng lồ không bị áp lực thời gian. Để tính toán KPI viễn thông chính xác và tối ưu đường truyền mạng, nhóm đã thiết kế một giải pháp kỹ thuật tối ưu hóa MapReduce gồm 3 cải tiến quan trọng:")

    add_fig(
        img_name="hinh_3_2_luong_mapreduce.png",
        caption="Hình 3.2: Sơ đồ luồng thuật toán MapReduce với Composite Key và Custom Partitioner",
        width_in=6.2
    )

    add_bullet("1. Khóa phức hợp (Composite Key - TowerTechKey): Thay vì chỉ sử dụng một khóa đơn giản, lớp `TowerTechKey` gói gọn hai trường `(tower_id, technology)` và hiện thực giao diện `WritableComparable`. Điều này cho phép sắp xếp tự nhiên theo thứ tự trạm BTS trước, sau đó sắp xếp theo thế hệ công nghệ (3G -> 4G -> 5G).")
    add_bullet("2. Bộ phân vùng tùy biến (Custom TowerPartitioner): Trong mạng viễn thông, một trạm BTS luôn phát sóng đồng thời cả 3G, 4G và 5G. Nếu dùng bộ băm mặc định, các công nghệ của cùng một trạm có thể bị phân tán sang các Reducer khác nhau. Bộ phân vùng tùy biến `TowerPartitioner` chỉ băm theo `tower_id` duy nhất: `(key.getTowerId().hashCode() & Integer.MAX_VALUE) % numPartitions`. Cơ chế này bảo đảm toàn bộ dữ liệu của một trạm tập trung về cùng một Reducer, triệt tiêu hoàn toàn hiện tượng lệch dữ liệu (Data Skew).")
    add_bullet("3. Bộ gộp cục bộ (Combiner): Chạy trực tiếp trên từng DataNode ngay sau pha Map, thực hiện cộng dồn sơ bộ thông lượng, độ trễ và số cuộc gọi rớt trước khi phát ra mạng. Cải tiến này giúp cắt giảm hơn 80% lưu lượng mạng I/O trong pha Shuffle.")

    add_h3("3.5.2. Kịch bản ETL và phân cụm trạm lỗi với Apache Pig Latin")
    add_p("Apache Pig cung cấp ngôn ngữ kịch bản luồng dữ liệu Pig Latin, giúp viết các tác vụ trích xuất và biến đổi (ETL) một cách ngắn gọn mà không cần viết hàng trăm dòng code Java MapReduce. Kịch bản `telecom_kpi_analysis.pig` nạp dữ liệu từ HDFS, lọc bỏ các giá trị dị thường, liên kết với danh mục trạm BTS và lọc ra danh sách các trạm có tỷ lệ rớt cuộc gọi vượt ngưỡng 2.0%:")
    add_code(
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

    add_h3("3.5.3. Thiết kế bảng Apache HBase phục vụ truy cập ngẫu nhiên")
    add_p("Trong khi HDFS tối ưu hóa cho các thao tác đọc quét tuần tự toàn bộ tệp (Sequential Scan), hệ thống giám sát NOC của nhà mạng lại đòi hỏi khả năng tra cứu ngẫu nhiên tức thời lịch sử chất lượng của một trạm BTS bất kỳ với độ trễ dưới 10 mili-giây. Để giải quyết bài toán này, nhóm đã thiết kế bảng NoSQL phân tán Apache HBase mang tên `telecom_kpi_summary`:")

    add_tbl(
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

    add_h3("3.5.4. Mô phỏng phân tích nghiệp vụ tương tác với BigSheets")
    add_p("IBM BigSheets là công cụ phân tích dữ liệu lớn trên giao diện bảng tính (Spreadsheet) dành cho các nhà phân tích nghiệp vụ mà không cần viết mã lệnh phức tạp. Nhóm đã xây dựng chương trình mô phỏng tương đương bằng Web Application tương tác (`bigsheets/web_app/`) kết hợp với Spark DataFrame:")

    add_fig(
        img_name="bigsheets_dashboard_preview.jpg",
        caption="Hình 3.3: Giao diện mô phỏng Dashboard phân tích nghiệp vụ BigSheets",
        width_in=6.4
    )

    add_p("Quy trình nghiệp vụ mô phỏng ánh xạ chính xác 1-1 với các khái niệm của BigSheets:")
    add_bullet("Collection Definition -> Spark DataFrame: Tạo tập dữ liệu gốc từ nguồn HDFS.")
    add_bullet("Calculated Column -> withColumn(): Tạo các cột tính toán nghiệp vụ (`session_volume_mb`, `cdr_pct`).")
    add_bullet("Filter Sheet -> filter(): Lọc bỏ dữ liệu lỗi âm và lọc theo ngưỡng cảnh báo.")
    add_bullet("Group / Pivot Sheet -> groupBy() & agg(): Tổng hợp KPI đa chiều theo tỉnh thành, trạm và công nghệ.")
    add_bullet("Chart Visualization: Tự động vẽ biểu đồ trực quan hóa xu hướng phục vụ báo cáo quản trị.")

    add_h3("3.5.5. Mô hình Hồi quy Logistic dự báo khiếu nại bằng R & SQLite")
    add_p("Ngôn ngữ R kết hợp cơ sở dữ liệu SQLite đảm nhiệm khâu phân tích khoa học dữ liệu chuyên sâu và dự báo nguy cơ phát sinh khiếu nại khách hàng. Kịch bản `telecom_analysis.R` sử dụng thư viện `DBI` và `RSQLite` để kết nối vào tệp CSDL `telecom_network.sqlite`, thực thi truy vấn SQL có `INNER JOIN` 3 bảng và `GROUP BY` theo `(tower_id, technology)`. Dữ liệu sau đó được tiền xử lý bằng `dplyr`/`tidyr` và đưa vào mô hình Học máy Hồi quy Logistic (Logistic Regression) với hàm liên kết Logit:")
    add_p("$$\\ln\\left(\\frac{P}{1 - P}\\right) = \\beta_0 + \\beta_1 \\cdot \\text{Latency} + \\beta_2 \\cdot \\text{PacketLoss} + \\beta_3 \\cdot \\text{Throughput} + \\beta_4 \\cdot \\text{ActiveUsers}$$", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p("Trong đó, $P$ là xác suất trạm BTS phát sinh khiếu nại từ khách hàng ($has\\_complaint = 1$). Mô hình giúp Trung tâm CSKH chủ động khoanh vùng các trạm có xác suất $P > 0.5$ để điều phối kỹ sư xử lý trước khi khách hàng gọi điện phản ánh.")

    add_h2("3.6. Cơ chế lưu trữ và xuất kết quả đa tầng")
    add_p("Hệ thống kết xuất và lưu trữ dữ liệu đầu ra theo kiến trúc đa tầng (Multi-tier Serving Architecture) phù hợp với từng mục đích khai thác:")
    add_bullet("Tầng Lưu trữ Lô (HDFS): Lưu trữ kết quả tổng hợp dưới dạng CSV và nén Parquet tại `/telecom/output/` phục vụ lưu trữ vĩnh viễn và kiểm toán dữ liệu.")
    add_bullet("Tầng Tra cứu Thời gian thực (HBase): Cung cấp API truy vấn chỉ số theo trạm cho Dashboard giám sát NOC thời gian thực.")
    add_bullet("Tầng Quan hệ & Thống kê (SQLite Database): Bảng `kpi_analysis_summary` trong file `telecom_network.sqlite` lưu trữ kết quả phân tích thống kê và xác suất khiếu nại dự báo từ R.")
    add_bullet("Tầng Báo cáo Trực quan: Tự động kết xuất 2 biểu đồ PNG chất lượng cao (`chart1_latency_by_tech.png` và `chart2_packet_loss_vs_drop_rate.png`) cùng bảng tổng hợp Power BI (`telecom_kpi_summary_powerbi.csv`).")

    doc.add_page_break()

print("Chapter 3 builder defined.")
