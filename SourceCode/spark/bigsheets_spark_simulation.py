#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
================================================================================
MÔ PHỎNG QUY TRÌNH PHÂN TÍCH BIGSHEETS BẰNG SPARK DATAFRAME & SPARK SQL
Dự án: Phân tích Dữ liệu lớn Mạng Viễn thông (Telecom Big Data Analytics)
================================================================================
MAPPING NGHIỆP VỤ BIGSHEETS SANG APACHE SPARK:
1. BigSheets Collection Definition    --> spark.read.csv (DataFrame)
2. BigSheets Data Cleansing (Filter)  --> df.filter() / df.where()
3. BigSheets Calculated Columns       --> df.withColumn()
4. BigSheets Dimension Table Join     --> df.join()
5. BigSheets Grouping / Pivot         --> df.groupBy().agg()
6. BigSheets Sorting                  --> df.orderBy()
7. BigSheets Dashboard & Export       --> Spark SQL / Power BI CSV / Python Charts
================================================================================
"""

import os
import sys

# Đảm bảo in tiếng Việt trên console Windows bất kể bảng mã CP932/CP1252
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Thiết lập hiển thị bảng tiếng Việt và đồ thị đẹp mắt
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Segoe UI']
plt.rcParams['axes.unicode_minus'] = False

def print_banner(text):
    print("\n" + "=" * 80)
    print(f" {text}")
    print("=" * 80)

def main():
    base_dir = os.path.abspath(r"c:\dulieulon\data")
    report_dir = os.path.abspath(r"c:\dulieulon\report")
    os.makedirs(report_dir, exist_ok=True)

    events_path = os.path.join(base_dir, "network_kpi_events.csv")
    towers_path = os.path.join(base_dir, "bts_towers.csv")
    cells_path = os.path.join(base_dir, "cells_catalog.csv")

    print_banner("KHỞI CHẠY MÔ PHỎNG BIGSHEETS BẰNG SPARK DATAFRAME & SPARK SQL")
    print(f"[*] Thu muc du lieu nguon: {base_dir}")
    print(f"[*] Thu muc bao cao xuat:  {report_dir}")

    # ==========================================================================
    # BƯỚC 1: COLLECTION -> DATAFRAME (Nạp dữ liệu từ kho lưu trữ)
    # Tương đương BigSheets: New Collection từ đường dẫn file trên HDFS
    # Tương đương Spark: spark.read.option("header", "true").csv(...)
    # ==========================================================================
    print_banner("BƯỚC 1: COLLECTION DEFINITION -> SPARK DATAFRAME")
    print(">>> BigSheets: Tao 'Telecom_KPI_Collection' tu HDFS /telecom/raw/network_kpi_events.csv")
    print(">>> Spark:     df_events = spark.read.option('header', 'true').csv(events_path)")
    
    df_raw_events = pd.read_csv(events_path)
    df_towers = pd.read_csv(towers_path)
    df_cells = pd.read_csv(cells_path)

    print(f"    [+] Nap thanh cong Collection KPI Events: {len(df_raw_events):,} ban ghi")
    print(f"    [+] Nap thanh cong Collection BTS Towers: {len(df_towers):,} tram phat song")
    print(f"    [+] Nap thanh cong Collection Cells Catalog: {len(df_cells):,} o phu song")
    
    # Hiển thị cấu trúc Schema tương đương df.printSchema() trong Spark
    print("\n>>> Schema DataFrame su kien KPI (df_events.printSchema()):")
    print("root")
    print(" |-- event_id: string (nullable = false)")
    print(" |-- timestamp: string (nullable = false)")
    print(" |-- tower_id: string (nullable = false)")
    print(" |-- cell_id: string (nullable = false)")
    print(" |-- technology: string (nullable = false)")
    print(" |-- throughput_mbps: double (nullable = true)")
    print(" |-- latency_ms: double (nullable = true)")
    print(" |-- packet_loss_pct: double (nullable = true)")
    print(" |-- call_dropped: integer (nullable = true)")
    print(" |-- num_active_users: integer (nullable = true)")
    print(" |-- signal_strength_dbm: double (nullable = true)")
    print(" |-- error_code: string (nullable = true)")

    # ==========================================================================
    # BƯỚC 2: DATA CLEANSING -> FILTER / WHERE
    # Tương đương BigSheets: Add Sheet -> Filter (loại trừ giá trị âm, rác)
    # Tương đương Spark: df.filter(col("latency_ms") >= 0 & col("throughput_mbps") >= 0 & ...)
    # ==========================================================================
    print_banner("BƯỚC 2: DATA CLEANSING -> SPARK FILTER / WHERE")
    print(">>> BigSheets: Filter quy tac: latency_ms >= 0, throughput_mbps >= 0, packet_loss <= 100")
    print(">>> Spark:     df_cleaned = df_events.filter((col('latency_ms') >= 0.0) & (col('throughput_mbps') >= 0.0) & (col('packet_loss_pct') <= 100.0) & (col('tower_id').isNotNull()))")
    
    total_raw = len(df_raw_events)
    clean_condition = (
        (df_raw_events['latency_ms'] >= 0.0) &
        (df_raw_events['throughput_mbps'] >= 0.0) &
        (df_raw_events['packet_loss_pct'] >= 0.0) &
        (df_raw_events['packet_loss_pct'] <= 100.0) &
        (df_raw_events['tower_id'].notna()) &
        (df_raw_events['cell_id'].notna())
    )
    df_cleaned = df_raw_events[clean_condition].copy()
    dropped_count = total_raw - len(df_cleaned)
    print(f"    [+] Tong so ban ghi ban dau: {total_raw:,}")
    print(f"    [+] So ban ghi loi bi loai bo: {dropped_count:,} ({dropped_count/total_raw*100:.2f}%)")
    print(f"    [+] So ban ghi sach dat chuan: {len(df_cleaned):,}")

    # ==========================================================================
    # BƯỚC 3: CALCULATED COLUMNS -> WITHCOLUMN
    # Tương đương BigSheets: Add Sheet -> Calculate / Formula
    # Tương đương Spark: df.withColumn("tên_cột", biểu_thức)
    # 1. call_drop_rate_pct = IF(call_dropped == 1, 100.0, 0.0)
    # 2. congestion_status  = IF(num_active_users > 150 AND throughput_mbps < 15.0, 'QUÁ_TẢI', 'BÌNH_THƯỜNG')
    # 3. qos_score          = 100.0 - (0.35*latency + 0.35*packet_loss*5 + 0.30*call_dropped*50)
    # ==========================================================================
    print_banner("BƯỚC 3: CALCULATED COLUMNS -> SPARK WITHCOLUMN")
    print(">>> Spark: df_calc = df_cleaned \\")
    print("             .withColumn('call_drop_rate_pct', when(col('call_dropped') == 1, 100.0).otherwise(0.0)) \\")
    print("             .withColumn('congestion_status', when((col('num_active_users') > 150) & (col('throughput_mbps') < 15.0), 'QUA_TAI').otherwise('BINH_THUONG')) \\")
    print("             .withColumn('qos_score', round(100.0 - (0.35*col('latency_ms') + 0.35*col('packet_loss_pct')*5.0 + 0.30*col('call_dropped')*50.0), 2))")

    # 1. Tỷ lệ rớt cuộc gọi (%)
    df_cleaned['call_drop_rate_pct'] = np.where(df_cleaned['call_dropped'] == 1, 100.0, 0.0)
    
    # 2. Trạng thái nghẽn mạng
    congestion_cond = (df_cleaned['num_active_users'] > 150) & (df_cleaned['throughput_mbps'] < 15.0)
    df_cleaned['congestion_status'] = np.where(congestion_cond, 'QUÁ_TẢI', 'BÌNH_THƯỜNG')

    # 3. Điểm đánh giá chất lượng dịch vụ QoS (0 - 100)
    df_cleaned['qos_score'] = 100.0 - (
        0.35 * df_cleaned['latency_ms'] +
        0.35 * df_cleaned['packet_loss_pct'] * 5.0 +
        0.30 * df_cleaned['call_dropped'] * 50.0
    )
    df_cleaned['qos_score'] = df_cleaned['qos_score'].clip(lower=0.0, upper=100.0).round(2)

    overloaded_events = (df_cleaned['congestion_status'] == 'QUÁ_TẢI').sum()
    print(f"    [+] So luong su kien nhan dien QUA_TAI: {overloaded_events:,} / {len(df_cleaned):,} ({overloaded_events/len(df_cleaned)*100:.2f}%)")
    print(f"    [+] Diem QoS trung binh toan mang:      {df_cleaned['qos_score'].mean():.2f} / 100")

    # ==========================================================================
    # BƯỚC 4: DIMENSION JOIN -> SPARK JOIN
    # Tương đương BigSheets: Add Sheet -> Join (với Collection BTS_Towers)
    # Tương đương Spark: df.join(df_towers, on="tower_id", how="inner")
    # ==========================================================================
    print_banner("BƯỚC 4: JOIN BẢNG DANH MỤC TRẠM BTS -> SPARK JOIN")
    print(">>> BigSheets: Join giua KPI Events va BTS_Towers_Catalog tren truong 'tower_id'")
    print(">>> Spark:     df_enriched = df_calc.join(df_towers, on='tower_id', how='inner')")

    df_enriched = pd.merge(df_cleaned, df_towers[['tower_id', 'tower_name', 'province', 'district']], on='tower_id', how='inner')
    print(f"    [+] Du lieu sau khi Join thanh cong: {len(df_enriched):,} dong voi {df_enriched.shape[1]} cot thuoc tinh")

    # ==========================================================================
    # BƯỚC 5: GROUPING / PIVOT -> SPARK GROUPBY & AGG
    # Tương đương BigSheets: Add Sheet -> Pivot / Group By theo province, technology, tower_id
    # Tương đương Spark: df.groupBy("province", "technology", "tower_id").agg(...)
    # ==========================================================================
    print_banner("BƯỚC 5: PIVOT & GOM NHÓM -> SPARK GROUPBY & AGG")
    print(">>> BigSheets: Group By 'province', 'technology', 'tower_id' voi cac ham Avg, Count")
    print(">>> Spark:     df_kpi_summary = df_enriched.groupBy('province', 'technology', 'tower_id', 'tower_name') \\")
    print("                   .agg(count('event_id').alias('Total_Sessions'), \\")
    print("                        round(avg('throughput_mbps'), 2).alias('Avg_Throughput'), \\")
    print("                        round(avg('latency_ms'), 2).alias('Avg_Latency'), \\")
    print("                        round(avg('packet_loss_pct'), 2).alias('Avg_Packet_Loss'), \\")
    print("                        round(avg('call_drop_rate_pct'), 2).alias('Mean_Call_Drop_Rate'), \\")
    print("                        round(avg('qos_score'), 2).alias('Average_QoS_Score'))")

    df_kpi_summary = df_enriched.groupby(['province', 'technology', 'tower_id', 'tower_name']).agg(
        Total_Sessions=('event_id', 'count'),
        Avg_Throughput=('throughput_mbps', lambda x: round(x.mean(), 2)),
        Avg_Latency=('latency_ms', lambda x: round(x.mean(), 2)),
        Avg_Packet_Loss=('packet_loss_pct', lambda x: round(x.mean(), 2)),
        Mean_Call_Drop_Rate=('call_drop_rate_pct', lambda x: round(x.mean(), 2)),
        Average_QoS_Score=('qos_score', lambda x: round(x.mean(), 2))
    ).reset_index()

    # ==========================================================================
    # BƯỚC 6: SORTING -> SPARK ORDERBY & BẢNG CẢNH BÁO
    # Tương đương BigSheets: Sort descending theo Mean_Call_Drop_Rate và Avg_Latency
    # Tương đương Spark: df.orderBy(desc("Mean_Call_Drop_Rate"), desc("Avg_Latency"))
    # ==========================================================================
    print_banner("BƯỚC 6: SẮP XẾP & CẢNH BÁO -> SPARK ORDERBY")
    print(">>> Spark: df_sorted = df_kpi_summary.orderBy(col('Mean_Call_Drop_Rate').desc(), col('Avg_Latency').desc())")
    
    df_sorted = df_kpi_summary.sort_values(by=['Mean_Call_Drop_Rate', 'Avg_Latency'], ascending=[False, False]).reset_index(drop=True)
    
    print("\n>>> KẾT QUẢ TOP 10 TRẠM CÓ TỶ LỆ RỚT MẠNG VÀ ĐỘ TRỄ CAO NHẤT (df_sorted.show(10)):")
    format_cols = ['province', 'technology', 'tower_id', 'tower_name', 'Total_Sessions', 'Avg_Latency', 'Avg_Packet_Loss', 'Mean_Call_Drop_Rate', 'Average_QoS_Score']
    print(df_sorted[format_cols].head(10).to_string(index=False))

    # ==========================================================================
    # BƯỚC 7: TRUY VẤN TƯƠNG ĐƯƠNG BẰNG SPARK SQL
    # ==========================================================================
    print_banner("TRUY VẤN TƯƠNG ĐƯƠNG BẰNG SPARK SQL (spark.sql)")
    spark_sql_statement = """
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
    WHERE e.latency_ms >= 0 
      AND e.throughput_mbps >= 0 
      AND e.packet_loss_pct <= 100
      AND e.tower_id IS NOT NULL
    GROUP BY t.province, e.technology, e.tower_id, t.tower_name
    ORDER BY Mean_Call_Drop_Rate DESC, Avg_Latency DESC;
    """
    print(spark_sql_statement)

    # ==========================================================================
    # BƯỚC 8: XUẤT DỮ LIỆU TỔNG HỢP CHO POWER BI / KIBANA
    # ==========================================================================
    print_banner("XUẤT DỮ LIỆU TỔNG HỢP CHO POWER BI & KIBANA")
    powerbi_csv_path = os.path.join(report_dir, "telecom_kpi_summary_powerbi.csv")
    df_sorted.to_csv(powerbi_csv_path, index=False, encoding='utf-8-sig')
    print(f"[+] Da xuat tap du lieu KPI tong hop cho Power BI tai: {powerbi_csv_path}")

    # ==========================================================================
    # BƯỚC 9: TRỰC QUAN HÓA BẰNG PYTHON (3 BIỂU ĐỒ DASHBOARD CHUYÊN NGHIỆP)
    # 1. Biểu đồ cột: Tỷ lệ rớt mạng theo Tỉnh & Công nghệ + Đường ngưỡng SLA (2%)
    # 2. Biểu đồ bong bóng: Tương quan Độ trễ vs Mất gói, kích thước lưu lượng
    # 3. Biểu đồ thanh ngang: Top 10 trạm phát sóng suy hao nghiêm trọng nhất
    # ==========================================================================
    print_banner("SINH ĐỒ THỊ TRỰC QUAN HÓA PYTHON DASHBOARD")

    # --------------------------------------------------------------------------
    # BIỂU ĐỒ 1: TỶ LỆ RỚT MẠNG THEO TỈNH THÀNH VÀ CÔNG NGHỆ
    # --------------------------------------------------------------------------
    chart1_path = os.path.join(report_dir, "chart_bigsheets_drop_rate_by_province_tech.png")
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    
    pivot_drop = df_enriched.pivot_table(
        index='province', 
        columns='technology', 
        values='call_drop_rate_pct', 
        aggfunc='mean'
    ).fillna(0.0)

    # Đảm bảo thứ tự 3G, 4G, 5G
    tech_order = [t for t in ['3G', '4G', '5G'] if t in pivot_drop.columns]
    pivot_drop = pivot_drop[tech_order]

    colors = {'3G': '#E74C3C', '4G': '#F39C12', '5G': '#2ECC71'}
    bar_colors = [colors.get(c, '#3498DB') for c in pivot_drop.columns]
    
    pivot_drop.plot(kind='bar', ax=ax, width=0.75, color=bar_colors, edgecolor='black', linewidth=0.8)
    
    # Đường ngưỡng viễn thông SLA
    ax.axhline(y=2.0, color='#C0392B', linestyle='--', linewidth=1.8, label='Ngưỡng chuẩn viễn thông SLA (2.0%)')
    
    ax.set_title("BIỂU ĐỒ 1: TỶ LỆ RỚT CUỘC GỌI THEO TỈNH THÀNH VÀ CÔNG NGHỆ (SPARK SIMULATION)", fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Tỉnh / Thành phố", fontsize=11, fontweight='bold')
    ax.set_ylabel("Tỷ lệ rớt mạng trung bình (%)", fontsize=11, fontweight='bold')
    ax.legend(title="Công nghệ mạng", fontsize=10, title_fontsize=10)
    ax.grid(axis='y', linestyle=':', alpha=0.6)
    plt.xticks(rotation=0)
    plt.savefig(chart1_path, bbox_inches='tight')
    plt.close()
    print(f"[+] Da tao Bieu do 1: {chart1_path}")

    # --------------------------------------------------------------------------
    # BIỂU ĐỒ 2: TƯƠNG QUAN ĐỘ TRỄ VS MẤT GÓI (BUBBLE SCATTER PLOT)
    # --------------------------------------------------------------------------
    chart2_path = os.path.join(report_dir, "chart_bigsheets_latency_vs_loss_bubble.png")
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)

    # Gom nhóm theo trạm phát sóng tổng quan
    tower_overall = df_enriched.groupby(['tower_id', 'province', 'tower_name']).agg(
        Avg_Latency=('latency_ms', 'mean'),
        Avg_Packet_Loss=('packet_loss_pct', 'mean'),
        Total_Users=('num_active_users', 'sum'),
        Mean_QoS=('qos_score', 'mean')
    ).reset_index()

    # Chuẩn hóa kích thước bong bóng từ 60 đến 450 điểm
    users_min = tower_overall['Total_Users'].min()
    users_max = tower_overall['Total_Users'].max()
    bubble_sizes = 80 + (tower_overall['Total_Users'] - users_min) / (users_max - users_min + 1e-5) * 380

    scatter = ax.scatter(
        tower_overall['Avg_Latency'],
        tower_overall['Avg_Packet_Loss'],
        s=bubble_sizes,
        c=tower_overall['Mean_QoS'],
        cmap='RdYlGn',
        alpha=0.85,
        edgecolors='black',
        linewidth=1.0
    )

    # Thêm nhãn cho các trạm có QoS thấp hoặc trễ cao
    for _, row in tower_overall.iterrows():
        if row['Mean_QoS'] < 60 or row['Avg_Latency'] > 100:
            ax.annotate(
                f"{row['tower_id']}\n({row['province']})",
                (row['Avg_Latency'], row['Avg_Packet_Loss']),
                xytext=(12, -15),
                textcoords='offset points',
                fontsize=8,
                fontweight='bold',
                color='#78281F',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#FDEDEC', edgecolor='#E74C3C', alpha=0.85)
            )

    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label("Điểm chất lượng dịch vụ QoS (0 - 100)", fontsize=10, fontweight='bold')

    ax.set_xlim(15, 225)
    ax.set_ylim(-0.3, 11.5)

    # Đường phân vùng rủi ro
    ax.axvline(x=50.0, color='gray', linestyle=':', alpha=0.7)
    ax.axhline(y=2.0, color='gray', linestyle=':', alpha=0.7)
    ax.text(60, 9.5, 'VÙNG NGHẼN NGUY HIỂM\n(Trễ > 50ms & Mất gói > 2%)', 
            color='darkred', fontsize=9.5, fontweight='bold', bbox=dict(boxstyle='round,pad=0.5', facecolor='#FADBD8', alpha=0.9))

    ax.set_title("BIỂU ĐỒ 2: TƯƠNG QUAN ĐỘ TRỄ VÀ TỶ LỆ MẤT GÓI THEO TRẠM BTS", fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Độ trễ trung bình Round-Trip Latency (ms)", fontsize=11, fontweight='bold')
    ax.set_ylabel("Tỷ lệ mất gói tin trung bình Packet Loss (%)", fontsize=11, fontweight='bold')
    ax.grid(True, linestyle=':', alpha=0.6)
    plt.savefig(chart2_path, bbox_inches='tight')
    plt.close()
    print(f"[+] Da tao Bieu do 2: {chart2_path}")

    # --------------------------------------------------------------------------
    # BIỂU ĐỒ 3: TOP 10 TRẠM PHÁT SÓNG CÓ ĐIỂM CHẤT LƯỢNG KÉM NHẤT (CẢNH BÁO NOC)
    # --------------------------------------------------------------------------
    chart3_path = os.path.join(report_dir, "chart_bigsheets_top10_worst_towers.png")
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)

    top10_worst = tower_overall.sort_values(by='Mean_QoS', ascending=True).head(10)
    y_pos = np.arange(len(top10_worst))

    # Tô màu theo ngưỡng cảnh báo: < 60 điểm tô màu đỏ, >= 60 điểm tô màu vàng/cam
    bar_colors = ['#E74C3C' if q < 60 else '#F39C12' for q in top10_worst['Mean_QoS']]

    bars = ax.barh(y_pos, top10_worst['Mean_QoS'], color=bar_colors, edgecolor='black', linewidth=0.8, height=0.62)
    ax.set_yticks(y_pos)
    ax.set_yticklabels([f"{row.tower_id} - {row.tower_name}" for _, row in top10_worst.iterrows()], fontsize=9.5)
    ax.invert_yaxis()  # Trạm xấu nhất lên đầu
    
    # Ghi giá trị số điểm trên từng thanh
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 1.2, bar.get_y() + bar.get_height()/2, f"{width:.1f} điểm", 
                va='center', ha='left', fontsize=9.5, fontweight='bold', color='#78281F')

    ax.set_xlim(0, 105)
    ax.axvline(x=60.0, color='#D35400', linestyle='--', linewidth=1.6, label='Ngưỡng cảnh báo can thiệp NOC (QoS < 60)')
    ax.set_title("BIỂU ĐỒ 3: BẢNG CẢNH BÁO TOP 10 TRẠM BTS CHẤT LƯỢNG KÉM NHẤT CẦN BẢO TRÌ", fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Điểm chất lượng dịch vụ tổng hợp QoS (Thang điểm 100)", fontsize=11, fontweight='bold')
    ax.legend(loc='lower right', fontsize=10)
    ax.grid(axis='x', linestyle=':', alpha=0.6)
    plt.savefig(chart3_path, bbox_inches='tight')
    plt.close()
    print(f"[+] Da tao Bieu do 3: {chart3_path}")

    # ==========================================================================
    # BẢNG TỔNG HỢP MAPPING NGHIỆP VỤ BIGSHEETS -> SPARK
    # ==========================================================================
    print_banner("BẢNG ĐỐI CHIẾU MAPPING CHỨC NĂNG BIGSHEETS SANG SPARK")
    mapping_data = [
        ("1. Nạp dữ liệu (Collection)", "Data -> New Collection từ đường dẫn HDFS", "spark.read.option('header', 'true').csv(...)"),
        ("2. Làm sạch (Data Cleansing)", "Add Sheet -> Filter (loại trừ giá trị âm, rác)", "df.filter(...) / df.where(...)"),
        ("3. Cột tính toán (Calculated Col)", "Add Sheet -> Formula / Calculate (IF, math)", "df.withColumn('tên_cột', when(...).otherwise(...))"),
        ("4. Nối bảng danh mục (Join)", "Add Sheet -> Join (khóa ngoại tower_id)", "df.join(towers_df, on='tower_id', how='inner')"),
        ("5. Gom nhóm & Pivot (Group)", "Add Sheet -> Pivot / Group By theo tỉnh, trạm", "df.groupBy('province', 'technology').agg(...)"),
        ("6. Sắp xếp thứ tự (Sort)", "Thanh công cụ -> Sort A-Z / Z-A", "df.orderBy(desc('Mean_Call_Drop_Rate'))"),
        ("7. Trực quan hóa & Xuất báo cáo", "Sheet Charts / Export CSV / REST Data Feed", "Biểu đồ Python Matplotlib / Power BI CSV Export")
    ]
    df_map = pd.DataFrame(mapping_data, columns=["Thao tác Nghiệp vụ", "Chức năng BigSheets", "Cú pháp tương đương trong Spark"])
    print(df_map.to_string(index=False))
    print("\n[OK] TOÀN BỘ TIẾN TRÌNH MÔ PHỎNG ĐÃ HOÀN THÀNH XUẤT SẮC!")

if __name__ == "__main__":
    main()
