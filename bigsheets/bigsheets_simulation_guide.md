# HƯỚNG DẪN MÔ PHỎNG QUY TRÌNH PHÂN TÍCH BIGSHEETS BẰNG SPARK DATAFRAME, SPARK SQL VÀ POWER BI
*(Tài liệu chuẩn mực đáp ứng yêu cầu Câu 8 - Đồ án Xử lý Dữ liệu lớn Mạng Viễn thông)*

---

## I. TỔNG QUAN VỀ IBM BIGSHEETS VÀ ĐỊNH HƯỚNG MÔ PHỎNG

**IBM BigSheets** là công cụ trực quan dạng bảng tính (Spreadsheet Interface) được phát triển để trao quyền cho các nhà phân tích nghiệp vụ (Business Analysts), kỹ sư NOC/SOC phân tích dữ liệu lớn mà không cần trực tiếp viết mã Java MapReduce phức tạp. BigSheets tự động dịch các thao tác giao diện người dùng thành các job MapReduce/Pig chạy phân tán trên cụm Hadoop.

Trong chương trình đào tạo kỹ thuật, sinh viên được phép **mô phỏng tương đương toàn bộ quy trình của BigSheets bằng Apache Spark DataFrame, Spark SQL và trực quan hóa phân tích bằng Python / Power BI**. Giải pháp này thể hiện khả năng hiểu sâu về kiến trúc xử lý dữ liệu lớn hiện đại, nơi Spark DataFrame tối ưu hóa tính toán trong bộ nhớ (In-Memory Processing) với Catalyst Optimizer, mang lại tốc độ vượt trội so với MapReduce truyền thống.

---

## II. BẢNG ÁNH XẠ CHUẨN MỰC (MAPPING: BIGSHEETS $\longleftrightarrow$ APACHE SPARK)

| Chức năng BigSheets | Ý nghĩa Nghiệp vụ | Cú pháp tương đương trong Spark DataFrame | Cú pháp tương đương trong Spark SQL |
| :--- | :--- | :--- | :--- |
| **Collection** | Nạp dữ liệu thô từ HDFS vào mô hình dữ liệu bảng có cấu trúc | `spark.read.option("header", "true").schema(schema).csv(path)` | `CREATE TEMPORARY VIEW ... USING csv ...` |
| **Filter / Cleansing** | Lọc dữ liệu lỗi, loại trừ bản ghi âm, mất gói bất thường | `df.filter(...)` hoặc `df.where(...)` | Mệnh đề `WHERE latency_ms >= 0 AND ...` |
| **Calculated Column** | Tạo cột chỉ số KPI nghiệp vụ (QoS, rớt mạng, quá tải) | `df.withColumn("col", when(...).otherwise(...))` | Biểu thức `CASE WHEN ... THEN ... END` |
| **Join** | Nối bảng sự kiện với bảng danh mục địa lý trạm phát sóng BTS | `df.join(towers_df, on="tower_id", how="inner")` | Mệnh đề `INNER JOIN bts_towers ON ...` |
| **Group / Pivot** | Gom nhóm đa chiều theo tỉnh thành, công nghệ và trạm phát sóng | `df.groupBy("province", "technology", "tower_id").agg(...)` | Mệnh đề `GROUP BY province, technology, tower_id` |
| **Sort** | Sắp xếp trạm có tỷ lệ rớt mạng và độ trễ cao nhất lên đầu | `df.orderBy(col("Mean_Call_Drop_Rate").desc())` | Mệnh đề `ORDER BY Mean_Call_Drop_Rate DESC` |
| **Dashboard / Export** | Trực quan hóa đồ thị và xuất số liệu tổng hợp cho báo cáo | Xuất CSV tích hợp Power BI & sinh biểu đồ Python | `spark.sql(...).toPandas()` |

---

## II.1. QUY TRÌNH 6 BƯỚC THAO TÁC GIAO DIỆN DÀNH CHO NGƯỜI DÙNG KHÔNG LẬP TRÌNH (NO-CODE WORKFLOW)

Đối với nhà phân tích nghiệp vụ (Business Analyst) hoặc kỹ sư vận hành NOC/SOC không biết lập trình, quy trình tái tạo 100% kết quả phân tích trên giao diện đồ họa được thực hiện qua 6 bước click chuột trực quan:

1. **Bước 1: Định nghĩa Collection (Nạp dữ liệu không cần code):**
   - Đăng nhập Web Console BigSheets $\rightarrow$ Chọn tab **Data** $\rightarrow$ Nhấp nút **New Collection**.
   - Đặt tên: `Telecom_Network_KPI_Collection`. Chọn định dạng: **CSV / Delimited Text**.
   - Chỉ định đường dẫn HDFS: `/telecom/curated/network_kpi_events.csv`, chọn Delimiter là dấu phẩy (`,`) và tích chọn **First row contains headers**.
   - Nhấp **Save & Build Workbook**: Hệ thống tự động trích xuất mẫu dữ liệu 1,000 dòng đầu tiên để khám phá tức thì.

2. **Bước 2: Khám phá và Làm sạch dữ liệu (Data Profiling & Cleansing):**
   - Nhấp vào tiêu đề cột `latency_ms` $\rightarrow$ Chọn tính năng **Profile Column** để xem biểu đồ phân bố giá trị Min, Max, Mean, Null Count.
   - Nhấp nút **Add Sheet $\rightarrow$ Filter** để tạo quy tắc lọc trực quan bằng chuột:
     * Quy tắc 1: `latency_ms >= 0.0` (Loại bỏ giá trị độ trễ âm do lỗi cảm biến đo).
     * Quy tắc 2: `throughput_mbps >= 0.0`.
     * Quy tắc 3: `packet_loss_pct <= 100.0`.
     * Quy tắc 4: `tower_id IS NOT EMPTY`.
   - Nhấp **Apply**: BigSheets tự động tạo một Sheet mới đã loại bỏ hoàn toàn 48 bản ghi rác, giữ lại 11,952 bản ghi sạch.

3. **Bước 3: Tạo các Cột tính toán nghiệp vụ (Calculated Columns):**
   - Nhấp **Add Sheet $\rightarrow$ Formula / Calculate** để thêm các chỉ số chất lượng dịch vụ:
     * *Cột Tỷ lệ rớt cuộc gọi (`call_drop_rate_pct`):* Nhập công thức `IF([#call_dropped] == 1, 100.0, 0.0)`
     * *Cột Nhận diện Nghẽn mạng (`congestion_status`):* Nhập công thức `IF([#num_active_users] > 150 AND [#throughput_mbps] < 15.0, "QUÁ_TẢI", "BÌNH_THƯỜNG")`
     * *Cột Điểm chất lượng dịch vụ tổng hợp (`qos_score` - Thang 100):* Nhập công thức `100.0 - (0.35 * [#latency_ms] + 0.35 * [#packet_loss_pct] * 5.0 + 0.30 * [#call_dropped] * 50.0)`

4. **Bước 4: Nối bảng danh mục và Gom nhóm (Join & Pivot/Group By):**
   - **Nối bảng (Join):** Nhấp **Add Sheet $\rightarrow$ Join** $\rightarrow$ Chọn nối với Collection danh mục trạm `BTS_Towers_Catalog` $\rightarrow$ Chọn khóa ghép `tower_id` $\rightarrow$ Giữ lại các cột địa lý: `province` (Tỉnh/Thành), `district` (Quận/Huyện), `tower_name`.
   - **Gom nhóm (Group By / Pivot):** Nhấp **Add Sheet $\rightarrow$ Pivot / Group By** $\rightarrow$ Kéo 3 trường vào vùng Group By: `province`, `technology`, `tower_id` $\rightarrow$ Tại vùng Tổng hợp (Values) chọn:
     * `Count([event_id])` $\rightarrow$ Đặt tên: `Total_Sessions`
     * `Average([throughput_mbps])` $\rightarrow$ Đặt tên: `Avg_Throughput`
     * `Average([latency_ms])` $\rightarrow$ Đặt tên: `Avg_Latency`
     * `Average([packet_loss_pct])` $\rightarrow$ Đặt tên: `Avg_Packet_Loss`
     * `Average([call_drop_rate_pct])` $\rightarrow$ Đặt tên: `Mean_Call_Drop_Rate`
     * `Average([qos_score])` $\rightarrow$ Đặt tên: `Average_QoS_Score`
   - **Sắp xếp (Sort):** Nhấp vào tiêu đề cột `Mean_Call_Drop_Rate` $\rightarrow$ Chọn **Sort Descending (Z-A)**.

5. **Bước 5: Xây dựng Dashboard KPI mạng theo trạm, tỉnh và công nghệ:**
   - Nhấp vào biểu tượng **Charts** trên thanh công cụ của Sheet để dựng 3 biểu đồ giám sát:
     * *Biểu đồ Cột (Bar Chart):* Phân tích theo Tỉnh và Công nghệ (Trục X: `province`, Trục Y: `Mean_Call_Drop_Rate`, Phân màu theo `technology`, đặt đường tham chiếu SLA $2.0\%$).
     * *Biểu đồ Bong bóng (Bubble Chart):* Phân tích tương quan theo Trạm BTS (Trục X: `Avg_Latency`, Trục Y: `Avg_Packet_Loss`, Kích thước: `Total_Sessions`, Phân màu theo `Average_QoS_Score` để cô lập Vùng nghẽn Backhaul).
     * *Bảng Xếp hạng Cảnh báo (Alert Grid):* Lọc các trạm có `Average_QoS_Score < 60` để cảnh báo can thiệp hạ tầng khẩn cấp.

6. **Bước 6: Thực thi toàn diện và Xuất báo cáo (Run Workbook & Export):**
   - Nhấp nút **Run Full Workbook**: Hệ thống Hadoop bên dưới tự động kích hoạt job MapReduce phân tán xử lý toàn bộ 100% dữ liệu gốc trong HDFS.
   - Nhấp menu **Export**:
     * Chọn **Export to CSV / Excel**: Tải tệp số liệu [`telecom_kpi_summary_powerbi.csv`](file:///c:/dulieulon/report/telecom_kpi_summary_powerbi.csv) gửi email cho Ban Giám đốc và nạp vào Power BI.
     * Chọn **Publish as Data Feed (REST / Atom API)**: Cấp API trực tiếp cho hệ thống giám sát NOC tập trung.
     * Mở Dashboard Web tương tác trực quan tại [`bigsheets_dashboard.html`](file:///c:/dulieulon/report/bigsheets_dashboard.html) và bấm nút **In Báo Cáo** để xuất bản in PDF.

---

## III. QUY TRÌNH 7 BƯỚC THỰC THI CHI TIẾT TRÊN APACHE SPARK

### Bước 1: Định nghĩa Collection $\longrightarrow$ Spark DataFrame
Nạp tệp sự kiện đo kiểm viễn thông [`network_kpi_events.csv`](file:///c:/dulieulon/data/network_kpi_events.csv) và danh mục trạm [`bts_towers.csv`](file:///c:/dulieulon/data/bts_towers.csv):
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, avg, count, round, desc

spark = SparkSession.builder.appName("BigSheets_Spark_Simulation").getOrCreate()

# Nạp Collection sự kiện đo kiểm
df_events = spark.read.option("header", "true").schema(events_schema).csv("c:/dulieulon/data/network_kpi_events.csv")

# Nạp Collection danh mục trạm BTS
df_towers = spark.read.option("header", "true").csv("c:/dulieulon/data/bts_towers.csv")
```

---

### Bước 2: Làm sạch dữ liệu $\longrightarrow$ `filter()` / `where()`
Loại bỏ 48 bản ghi rác đo kiểm lỗi (độ trễ âm, thông lượng âm, tỷ lệ mất gói $> 100\%$ hoặc mã trạm null):
```python
df_cleaned = df_events.filter(
    (col("latency_ms") >= 0.0) &
    (col("throughput_mbps") >= 0.0) &
    (col("packet_loss_pct") >= 0.0) &
    (col("packet_loss_pct") <= 100.0) &
    (col("tower_id").isNotNull()) &
    (col("cell_id").isNotNull())
)
```

---

### Bước 3: Tạo cột tính toán nghiệp vụ $\longrightarrow$ `withColumn()`
Thiết lập 3 cột KPI viễn thông cốt lõi:
1. **Tỷ lệ rớt cuộc gọi (`call_drop_rate_pct`):** Chuyển đổi cờ nhị phân `call_dropped` thành giá trị phần trăm ($0.0\%$ hoặc $100.0\%$).
2. **Trạng thái quá tải (`congestion_status`):** Đánh dấu `QUÁ_TẢI` khi số người dùng hoạt động vượt 150 mà thông lượng rớt dưới 15 Mbps.
3. **Điểm chất lượng dịch vụ tổng hợp (`qos_score` - Thang điểm 100):**
   $$\text{QoS Score} = 100.0 - \left(0.35 \times \text{Latency} + 0.35 \times \text{Packet Loss} \times 5.0 + 0.30 \times \text{Call Dropped} \times 50.0\right)$$

```python
df_calc = df_cleaned \
    .withColumn("call_drop_rate_pct", when(col("call_dropped") == 1, 100.0).otherwise(0.0)) \
    .withColumn("congestion_status", when((col("num_active_users") > 150) & (col("throughput_mbps") < 15.0), "QUÁ_TẢI").otherwise("BÌNH_THƯỜNG")) \
    .withColumn("qos_score", round(100.0 - (0.35 * col("latency_ms") + 0.35 * col("packet_loss_pct") * 5.0 + 0.30 * col("call_dropped") * 50.0), 2))
```

---

### Bước 4: Nối bảng danh mục trạm BTS $\longrightarrow$ `join()`
Làm giàu dữ liệu sự kiện với thông tin Tỉnh/Thành phố (`province`) và Tên trạm (`tower_name`):
```python
df_enriched = df_calc.join(df_towers, on="tower_id", how="inner")
```

---

### Bước 5: Gom nhóm đa chiều $\longrightarrow$ `groupBy()` & `agg()`
Tổng hợp các chỉ số trung bình theo Tỉnh thành, Công nghệ và Trạm phát sóng:
```python
df_kpi_summary = df_enriched.groupBy("province", "technology", "tower_id", "tower_name").agg(
    count("event_id").alias("Total_Sessions"),
    round(avg("throughput_mbps"), 2).alias("Avg_Throughput"),
    round(avg("latency_ms"), 2).alias("Avg_Latency"),
    round(avg("packet_loss_pct"), 2).alias("Avg_Packet_Loss"),
    round(avg("call_drop_rate_pct"), 2).alias("Mean_Call_Drop_Rate"),
    round(avg("qos_score"), 2).alias("Average_QoS_Score")
)
```

---

### Bước 6: Sắp xếp cảnh báo $\longrightarrow$ `orderBy()`
Đưa các trạm có tỷ lệ rớt mạng cao nhất và độ trễ lớn nhất lên đầu bảng điều khiển:
```python
df_sorted = df_kpi_summary.orderBy(
    col("Mean_Call_Drop_Rate").desc(), 
    col("Avg_Latency").desc()
)
df_sorted.show(10, truncate=False)
```

---

### Bước 7: Truy vấn tương đương bằng Spark SQL
```sql
SELECT 
    t.province,
    e.technology,
    e.tower_id,
    t.tower_name,
    COUNT(e.event_id) AS Total_Sessions,
    ROUND(AVG(e.throughput_mbps), 2) AS Avg_Throughput,
    ROUND(AVG(e.latency_ms), 2) AS Avg_Latency,
    ROUND(AVG(e.packet_loss_pct), 2) AS Avg_Packet_Loss,
    ROUND(AVG(CASE WHEN e.call_dropped = 1 THEN 100.0 ELSE 0.0 END), 2) AS Mean_Call_Drop_Rate,
    ROUND(AVG(100.0 - (0.35 * e.latency_ms + 0.35 * e.packet_loss_pct * 5.0 + 0.30 * e.call_dropped * 50.0)), 2) AS Average_QoS_Score
FROM network_events e
INNER JOIN bts_towers t ON e.tower_id = t.tower_id
WHERE e.latency_ms >= 0.0 
  AND e.throughput_mbps >= 0.0 
  AND e.packet_loss_pct <= 100.0
  AND e.tower_id IS NOT NULL
GROUP BY t.province, e.technology, e.tower_id, t.tower_name
ORDER BY Mean_Call_Drop_Rate DESC, Avg_Latency DESC;
```

---

## IV. BỘ BIỂU ĐỒ TRỰC QUAN HÓA PYTHON DASHBOARD ĐÃ TẠO

Kịch bản tự động lưu 3 biểu đồ giám sát tại thư mục [`c:\dulieulon\report\`](file:///c:/dulieulon/report/):

1. **Biểu đồ Cột (Bar Chart):** [`chart_bigsheets_drop_rate_by_province_tech.png`](file:///c:/dulieulon/report/chart_bigsheets_drop_rate_by_province_tech.png)  
   - So sánh tỷ lệ rớt mạng theo Tỉnh thành & Công nghệ (3G/4G/5G).
   - Thể hiện đường ngưỡng chuẩn cam kết dịch vụ SLA ($2.0\%$).
2. **Biểu đồ Bong bóng (Bubble Chart):** [`chart_bigsheets_latency_vs_loss_bubble.png`](file:///c:/dulieulon/report/chart_bigsheets_latency_vs_loss_bubble.png)  
   - Phân tích tương quan giữa Độ trễ (ms) và Tỷ lệ mất gói (%).
   - Kích thước bong bóng biểu thị khối lượng người dùng; màu sắc thể hiện điểm QoS; làm nổi bật *Vùng nghẽn nguy hiểm*.
3. **Bảng Cảnh báo Trạm Suy hao (Horizontal Bar Chart):** [`chart_bigsheets_top10_worst_towers.png`](file:///c:/dulieulon/report/chart_bigsheets_top10_worst_towers.png)  
   - Bảng xếp hạng Top 10 trạm BTS chất lượng kém nhất cần bảo trì gấp.
   - Thể hiện rõ đường ngưỡng can thiệp NOC ($< 60$ điểm màu đỏ).

---

## V. HƯỚNG DẪN KẾT NỐI VÀ TẠO DASHBOARD TRÊN MICROSOFT POWER BI

1. **Chuẩn bị dữ liệu:** Tệp CSV tổng hợp đã được kịch bản xuất tại:  
   [`c:\dulieulon\report\telecom_kpi_summary_powerbi.csv`](file:///c:/dulieulon/report/telecom_kpi_summary_powerbi.csv).
2. **Nạp dữ liệu vào Power BI Desktop:**
   - Mở Power BI Desktop $\rightarrow$ Chọn nút **Get Data** $\rightarrow$ Chọn **Text/CSV**.
   - Trỏ tới đường dẫn `c:\dulieulon\report\telecom_kpi_summary_powerbi.csv` $\rightarrow$ Nhấp **Load**.
3. **Thiết lập trực quan hóa (Visuals):**
   - **Thẻ tổng quan (Cards):** Thể hiện Tổng số phiên đo (`SUM(Total_Sessions)`), Độ trễ trung bình toàn mạng (`AVERAGE(Avg_Latency)`).
   - **Clustered Column Chart:** Trục X là `province`, Trục Y là `Mean_Call_Drop_Rate`, Phân loại `technology`.
   - **Scatter Chart:** Phân tích `Avg_Latency` vs `Avg_Packet_Loss`, kích thước theo `Total_Sessions`.
   - **Table:** Danh sách các trạm với định dạng có điều kiện (Conditional Formatting) tô đỏ các dòng có `Average_QoS_Score` $< 60$.

---

## VI. HƯỚNG DẪN VẬN HÀNH KỊCH BẢN (EXECUTION INSTRUCTIONS)

Người dùng có thể thực thi kịch bản bằng 2 cách tiện lợi:

- **Cách 1: Chạy file Batch tự động**  
  Nhấp đúp vào [`c:\dulieulon\start_bigsheets.bat`](file:///c:/dulieulon/start_bigsheets.bat).

- **Cách 2: Chạy trực tiếp từ dòng lệnh PowerShell**
  ```powershell
  $env:PYTHONIOENCODING="utf-8"
  & "C:\Users\DELL\AppData\Local\Programs\OSGeo4W\apps\Python312\python.exe" "c:\dulieulon\spark\bigsheets_spark_simulation.py"
  ```
Kịch bản sẽ tự động in bảng log từng bước, tính toán định lượng trên 12,000 bản ghi, xuất file CSV cho Power BI và làm mới toàn bộ 3 đồ thị trực quan hóa trong thư mục báo cáo.
