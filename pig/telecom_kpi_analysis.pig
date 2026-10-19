-- =============================================================================
-- SCRIPT PIG LATIN: PHÂN TÍCH CHẤT LƯỢNG MẠNG VIỄN THÔNG (TELECOM KPI ANALYSIS)
-- Phiên bản tối ưu chuẩn cú pháp Apache Pig 0.17
-- =============================================================================

-- Thiết lập số lượng Reducer mặc định là 1 để tránh lỗi TotalOrderPartitioner/Sampler trên Hadoop 3.3
SET default_parallel 1;

-- 1. LOAD DỮ LIỆU SỰ KIỆN VÀ DANH MỤC VỚI SCHEMA ĐẦY ĐỦ
raw_events = LOAD '/telecom/raw/batch_kpi/network_kpi_events.csv' 
    USING PigStorage(',') 
    AS (
        event_id: chararray,
        timestamp: chararray,
        tower_id: chararray,
        cell_id: chararray,
        technology: chararray,
        throughput_mbps: double,
        latency_ms: double,
        packet_loss_pct: double,
        call_dropped: int,
        num_active_users: int,
        signal_strength_dbm: double,
        error_code: chararray
    );

bts_catalog = LOAD '/telecom/curated/dimension/bts_towers.csv' 
    USING PigStorage(',') 
    AS (
        tower_id: chararray,
        tower_name: chararray,
        province: chararray,
        district: chararray,
        latitude: double,
        longitude: double,
        install_date: chararray
    );

cells_catalog = LOAD '/telecom/curated/dimension/cells_catalog.csv' 
    USING PigStorage(',') 
    AS (
        cell_id: chararray,
        tower_id: chararray,
        technology: chararray,
        frequency_mhz: int,
        max_bandwidth_mbps: double,
        azimuth: int
    );

-- 2. FILTER: LÀM SẠCH VÀ LOẠI BỎ BẢN GHI LỖI / TIÊU ĐỀ
valid_events = FILTER raw_events BY 
    (event_id != 'event_id') AND
    (tower_id IS NOT NULL) AND
    (latency_ms >= 0.0) AND
    (throughput_mbps >= 0.0) AND
    (packet_loss_pct >= 0.0 AND packet_loss_pct <= 100.0);

-- Rút gọn trường dữ liệu trước khi Join để tối ưu bộ nhớ
ev_clean = FOREACH valid_events GENERATE 
    event_id, tower_id, cell_id, technology, 
    throughput_mbps, latency_ms, packet_loss_pct, call_dropped;

bts_clean = FOREACH bts_catalog GENERATE 
    tower_id, tower_name, province, district;

-- 3. JOIN: NỐI SỰ KIỆN VỚI DANH MỤC TRẠM BTS
events_with_bts = JOIN ev_clean BY tower_id, bts_clean BY tower_id;

-- 4. GROUP BY: GOM NHÓM THEO TRẠM, CÔNG NGHỆ VÀ TỈNH THÀNH
grouped_kpi = GROUP events_with_bts BY (
    ev_clean::tower_id, 
    ev_clean::technology, 
    bts_clean::province,
    bts_clean::district
);

-- 5. FOREACH: TÍNH TOÁN CÁC HÀM TỔNG HỢP (COUNT, SUM, AVG, MIN, MAX, CONCAT)
kpi_summary = FOREACH grouped_kpi GENERATE 
    group.$0 AS tower_id: chararray,
    group.$1 AS technology: chararray,
    group.$2 AS province: chararray,
    group.$3 AS district: chararray,
    CONCAT(group.$0, '_', group.$1) AS tower_tech_code: chararray,
    COUNT(events_with_bts) AS sample_count: long,
    AVG(events_with_bts.ev_clean::throughput_mbps) AS mean_throughput_mbps: double,
    AVG(events_with_bts.ev_clean::latency_ms) AS mean_latency_ms: double,
    MAX(events_with_bts.ev_clean::packet_loss_pct) AS max_packet_loss_pct: double,
    SUM(events_with_bts.ev_clean::call_dropped) AS dropped_calls_count: int,
    ((double)SUM(events_with_bts.ev_clean::call_dropped) * 100.0 / (double)COUNT(events_with_bts)) AS call_drop_rate_pct: double;

-- 6. SPLIT: PHÂN LUỒNG TẾ BÀO SUY GIẢM VÀ TẾ BÀO BÌNH THƯỜNG
SPLIT kpi_summary INTO 
    degraded_cells IF (mean_latency_ms > 80.0 OR call_drop_rate_pct > 2.0 OR max_packet_loss_pct > 5.0),
    normal_cells OTHERWISE;

-- 7. TOP 10 TRẠM NGUY CẤP NHẤT: DÙNG NESTED ORDER TRONG FOREACH ĐỂ TRÁNH TOTALORDERPARTITIONER CỦA HADOOP 3
grouped_degraded = GROUP degraded_cells ALL;
top_10_worst_cells = FOREACH grouped_degraded {
    sorted = ORDER degraded_cells BY call_drop_rate_pct DESC;
    top10 = LIMIT sorted 10;
    GENERATE FLATTEN(top10);
};

-- 8. STORE KẾT QUẢ VÀO HDFS
STORE top_10_worst_cells INTO '/telecom/output/alerts/top_10_worst_cells' 
    USING PigStorage(',');

STORE normal_cells INTO '/telecom/output/reports/healthy_cells_kpi' 
    USING PigStorage(',');
