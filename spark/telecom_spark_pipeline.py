#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
================================================================================
APACHE SPARK PIPELINE: PHÁT HIỆN CELL QUÁ TẢI VÀ BẤT THƯỜNG THEO THỜI GIAN
================================================================================
Yêu cầu đáp ứng:
- Đọc dữ liệu CSV / JSON
- Làm sạch dữ liệu (Data Cleansing)
- Join bảng sự kiện với bảng danh mục trạm BTS và Cell
- Tối thiểu 5 Transformations (filter, withColumn, join, groupBy, agg, window, orderBy)
- Tối thiểu 3 Actions (count, show, write)
- Sử dụng cache/persist hợp lý với giải thích kỹ thuật
- Xuất dữ liệu tổng hợp ra định dạng Parquet và CSV
================================================================================
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, when, avg, count, sum as spark_sum, min as spark_min, max as spark_max,
    round as spark_round, to_timestamp, hour, dense_rank, desc
)
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType, IntegerType
)
from pyspark.sql.window import Window
from pyspark.storagelevel import StorageLevel
import os
import sys

def main():
    # --------------------------------------------------------------------------
    # 1. KHỞI TẠO SPARK SESSION VỚI CẤU HÌNH TỐI ƯU
    # --------------------------------------------------------------------------
    spark = SparkSession.builder \
        .appName("TelecomNetwork_Overload_Anomaly_Detector") \
        .config("spark.sql.shuffle.partitions", "10") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.parquet.compression.codec", "snappy") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")
    print("\n>>> [1/7] Spark Session khoi tao thanh cong.")

    # Tự động nhận diện môi trường: Nếu chạy trên Linux/YARN thì đọc trực tiếp từ HDFS
    if os.name == 'nt':
        base_dir = os.path.abspath(r"c:\dulieulon\data")
        events_path = os.path.join(base_dir, "network_kpi_events.csv")
        towers_path = os.path.join(base_dir, "bts_towers.csv")
        cells_path = os.path.join(base_dir, "cells_catalog.csv")
        output_dir = os.path.abspath(r"c:\dulieulon\data\spark_output")
        parquet_out = os.path.join(output_dir, "curated_cell_kpi_parquet")
        csv_out = os.path.join(output_dir, "worst_cells_alert_csv")
    else:
        # Môi trường Hadoop / YARN cluster trên Ubuntu: Đọc từ HDFS theo cấu hình defaultFS hoặc local
        if os.path.exists("data/network_kpi_events.csv"):
            events_path = "data/network_kpi_events.csv"
            towers_path = "data/bts_towers.csv"
            cells_path = "data/cells_catalog.csv"
            parquet_out = "output/spark_curated_cell_kpi_parquet"
            csv_out = "output/spark_worst_cells_alert_csv"
        else:
            events_path = "/telecom/input/network_kpi_events.csv"
            towers_path = "/telecom/input/bts_towers.csv"
            cells_path = "/telecom/input/cells_catalog.csv"
            parquet_out = "/telecom/output/spark_curated_cell_kpi_parquet"
            csv_out = "/telecom/output/spark_worst_cells_alert_csv"

    print(f">>> [2/7] Doc du lieu su kien tu: {events_path}")

    # --------------------------------------------------------------------------
    # 2. ĐỊNH NGHĨA SCHEMA VÀ ĐỌC DỮ LIỆU (READ CSV/JSON)
    # --------------------------------------------------------------------------
    events_schema = StructType([
        StructField("event_id", StringType(), False),
        StructField("timestamp", StringType(), False),
        StructField("tower_id", StringType(), False),
        StructField("cell_id", StringType(), False),
        StructField("technology", StringType(), False),
        StructField("throughput_mbps", DoubleType(), True),
        StructField("latency_ms", DoubleType(), True),
        StructField("packet_loss_pct", DoubleType(), True),
        StructField("call_dropped", IntegerType(), True),
        StructField("num_active_users", IntegerType(), True),
        StructField("signal_strength_dbm", DoubleType(), True),
        StructField("error_code", StringType(), True)
    ])

    df_raw_events = spark.read.option("header", "true").schema(events_schema).csv(events_path)
    df_towers = spark.read.option("header", "true").csv(towers_path)
    df_cells = spark.read.option("header", "true").csv(cells_path)

    # --------------------------------------------------------------------------
    # 3. LÀM SẠCH DỮ LIỆU (TRANSFORMATION 1 & 2: filter, withColumn)
    # --------------------------------------------------------------------------
    # Transformation 1: filter - Loại bỏ giá trị null, âm vô lý, hoặc lỗi cảm biến đo
    df_cleaned_events = df_raw_events.filter(
        (col("tower_id").isNotNull()) &
        (col("cell_id").isNotNull()) &
        (col("latency_ms") >= 0.0) &
        (col("throughput_mbps") >= 0.0) &
        (col("packet_loss_pct") >= 0.0) &
        (col("packet_loss_pct") <= 100.0)
    )

    # Transformation 2: withColumn - Chuẩn hóa kiểu timestamp, trích xuất khung giờ và chỉ số quá tải
    df_preprocessed = df_cleaned_events \
        .withColumn("event_time", to_timestamp(col("timestamp"), "yyyy-MM-dd HH:mm:ss")) \
        .withColumn("event_hour", hour(col("event_time"))) \
        .withColumn(
            "is_overloaded_sample",
            when((col("num_active_users") > 150) & (col("throughput_mbps") < 15.0), 1).otherwise(0)
        )

    # --------------------------------------------------------------------------
    # 4. JOIN VỚI BẢNG DANH MỤC (TRANSFORMATION 3: join)
    # --------------------------------------------------------------------------
    # Nối dữ liệu sự kiện với thông tin trạm BTS (tỉnh, huyện) và cấu hình Cell (băng thông tối đa)
    df_enriched = df_preprocessed \
        .join(df_towers.select("tower_id", "tower_name", "province", "district"), on="tower_id", how="inner") \
        .join(df_cells.select("cell_id", "frequency_mhz", "max_bandwidth_mbps"), on="cell_id", how="inner")

    # --------------------------------------------------------------------------
    # 5. CHIẾN LƯỢC TỐI ƯU HÓA BỘ NHỚ: PERSIST / CACHE
    # --------------------------------------------------------------------------
    # Giải thích kỹ thuật: df_enriched là kết quả sau bước Filter và 2 phép Join tốn kém.
    # Dataset này được sử dụng làm nguồn cho 2 nhánh phân tích tiếp theo:
    #   Nhánh 1: Phát hiện cell quá tải cấp trạm/công nghệ
    #   Nhánh 2: Phân tích bất thường theo chuỗi thời gian (khung giờ)
    # Nếu không persist, Spark sẽ phải đọc lại dữ liệu từ đĩa và thực hiện lại toàn bộ phép Join 2 lần!
    df_enriched.persist(StorageLevel.MEMORY_AND_DISK)

    # ACTION 1: count() - Kích hoạt tính toán và nạp dataframe vào bộ nhớ đệm
    total_valid_records = df_enriched.count()
    print(f"\n>>> [ACTION 1] Tong so ban ghi sach sau khi Join: {total_valid_records}")

    # --------------------------------------------------------------------------
    # 6. PHÂN TÍCH VÀ PHÁT HIỆN CELL QUÁ TẢI (TRANSFORMATION 4, 5, 6: groupBy, agg, withColumn)
    # --------------------------------------------------------------------------
    df_cell_kpi = df_enriched.groupBy("tower_id", "cell_id", "technology", "province", "district") \
        .agg(
            count("event_id").alias("total_samples"),
            spark_round(avg("throughput_mbps"), 2).alias("avg_throughput_mbps"),
            spark_round(avg("latency_ms"), 2).alias("avg_latency_ms"),
            spark_round(spark_max("latency_ms"), 2).alias("peak_latency_ms"),
            spark_round(avg("packet_loss_pct"), 2).alias("avg_packet_loss_pct"),
            spark_sum("call_dropped").alias("total_call_drops"),
            spark_round(avg("num_active_users"), 1).alias("avg_concurrent_users"),
            spark_sum("is_overloaded_sample").alias("overload_sample_count")
        ) \
        .withColumn(
            "call_drop_rate_pct",
            spark_round((col("total_call_drops") / col("total_samples")) * 100.0, 3)
        ) \
        .withColumn(
            "overload_ratio_pct",
            spark_round((col("overload_sample_count") / col("total_samples")) * 100.0, 2)
        ) \
        .withColumn(
            "health_status",
            when((col("call_drop_rate_pct") > 2.0) | (col("avg_latency_ms") > 80.0) | (col("overload_ratio_pct") > 40.0), "CRITICAL_OVERLOAD")
            .when((col("avg_latency_ms") > 50.0) | (col("call_drop_rate_pct") > 1.0), "WARNING_DEGRADED")
            .otherwise("HEALTHY")
        )

    # Transformation 7: window function - Xếp hạng các cell theo tỷ lệ rớt cuộc gọi trong từng công nghệ
    tech_window = Window.partitionBy("technology").orderBy(desc("call_drop_rate_pct"), desc("avg_latency_ms"))
    df_ranked_cells = df_cell_kpi.withColumn("rank_in_tech", dense_rank().over(tech_window))

    # Transformation 8: orderBy - Sắp xếp toàn mạng theo mức độ nguy cấp
    df_worst_cells = df_ranked_cells.filter(col("health_status") != "HEALTHY") \
        .orderBy(desc("call_drop_rate_pct"), desc("avg_latency_ms"))

    # ACTION 2: show() - Hiển thị Top các cell quá tải và bất thường nghiêm trọng nhất
    print("\n>>> [ACTION 2] DANH SÁCH TẾ BÀO QUÁ TẢI VÀ SUY GIẢM CHẤT LƯỢNG NGHIÊM TRỌNG (TOP 10):")
    df_worst_cells.select(
        "tower_id", "cell_id", "technology", "province",
        "avg_throughput_mbps", "avg_latency_ms", "call_drop_rate_pct", "health_status", "rank_in_tech"
    ).show(10, truncate=False)

    # --------------------------------------------------------------------------
    # 7. XUẤT DỮ LIỆU TỔNG HỢP RA CSV VÀ PARQUET (ACTION 3: write)
    # --------------------------------------------------------------------------
    # Đường dẫn xuất file đã được xác định động phù hợp với HDFS hoặc local
    print(f"\n>>> [ACTION 3] Xuat ket qua ra: {parquet_out} va {csv_out}")

    print("\n>>> [ACTION 3a] Xuat toan bo KPI tong hop sang dinh dang PARQUET (phan vung theo province)...")
    df_ranked_cells.write \
        .partitionBy("province") \
        .mode("overwrite") \
        .parquet(parquet_out)

    print(">>> [ACTION 3b] Xuat danh sach cell can xu ly gap sang dinh dang CSV...")
    df_worst_cells.coalesce(1).write \
        .mode("overwrite") \
        .option("header", "true") \
        .csv(csv_out)

    # Giải phóng bộ nhớ đệm
    df_enriched.unpersist()
    print("\n>>> [HOÀN TẤT] Pipeline Spark da xu ly va xuat ket qua thanh cong len HDFS!")
    spark.stop()

if __name__ == "__main__":
    main()
