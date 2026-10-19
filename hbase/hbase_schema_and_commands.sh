#!/bin/bash
# ==============================================================================
# THIẾT KẾ BẢNG HBASE VÀ TẬP LỆNH HBASE SHELL CHO BÀI TOÁN VIỄN THÔNG
# Tên bảng: telecom_kpi
# RowKey đề xuất: tower_id#reverse_timestamp
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. PHÂN TÍCH THIẾT KẾ ROWKEY (RowKey Design Analysis)
# ------------------------------------------------------------------------------
# Cấu trúc: [tower_id]#[reverse_timestamp]
# Ví dụ:   TOWER_003#9223370336854775807-1789696000000 = TOWER_003#9221580638854775807
#
# Lý do kỹ thuật:
# (a) Thứ tự thời gian đảo ngược (Reverse Chronological Order):
#     HBase sắp xếp dữ liệu theo thứ tự từ điển (Lexicographical order) của RowKey.
#     Nhờ reverse_timestamp, các sự kiện đo kiểm MỚI NHẤT của mỗi trạm sẽ luôn nằm ở ĐẦU.
#     Khi hệ thống NOC/SOC cần giám sát tức thời chất lượng trạm trong 15 phút gần nhất,
#     lệnh scan chỉ cần quét từ đầu rowkey của trạm đó với LIMIT 50 mà không cần quét ngược toàn bảng.
# (b) Tránh điểm nóng ghi (Hotspotting Prevention) kết hợp Pre-splitting:
#     Nếu dùng timestamp đơn thuần ở đầu RowKey, toàn bộ lưu lượng ghi từ mọi trạm tại cùng một thời điểm
#     sẽ dồn vào đúng 1 RegionServer duy nhất (Write Hotspot).
#     Đặt tower_id ở đầu kết hợp pre-splitting giúp phân tán đều tải ghi sang nhiều RegionServer trên cụm.

# ------------------------------------------------------------------------------
# 2. XÁC ĐỊNH 3 COLUMN FAMILIES VÀ QUẢN LÝ VERSION / TTL / COMPRESSION
# ------------------------------------------------------------------------------
# cf_kpi:   Lưu chỉ số kỹ thuật (tp, lat, loss, drop). VERSIONS => 3, TTL => 7776000 (90 ngày)
# cf_cell:  Lưu cấu hình vật lý vô tuyến (cell_id, tech, freq, users). VERSIONS => 1
# cf_alert: Lưu cảnh báo và trạng thái sự cố (status, overload_flag). VERSIONS => 3

# ------------------------------------------------------------------------------
# 3. LỆNH TẠO BẢNG VÀ THAO TÁC TRÊN HBASE SHELL
# ------------------------------------------------------------------------------
hbase shell << 'EOF'

# Kiểm tra và xóa bảng cũ nếu tồn tại
if exists 'telecom_kpi'
  disable 'telecom_kpi'
  drop 'telecom_kpi'
end

# Tạo bảng mới với 3 Column Families, Pre-splitting thành 4 Regions
create 'telecom_kpi', \
  {NAME => 'cf_kpi',   VERSIONS => 3, TTL => 7776000, BLOCKCACHE => true}, \
  {NAME => 'cf_cell',  VERSIONS => 1, BLOCKCACHE => true}, \
  {NAME => 'cf_alert', VERSIONS => 3, BLOCKCACHE => true}, \
  {SPLITS => ['TOWER_005#', 'TOWER_010#', 'TOWER_015#']}

# ------------------------------------------------------------------------------
# 4. THAO TÁC DỮ LIỆU: PUT (Ghi bản ghi mới)
# ------------------------------------------------------------------------------
put 'telecom_kpi', 'TOWER_003#9221580638854775807', 'cf_kpi:throughput_mbps', '4.25'
put 'telecom_kpi', 'TOWER_003#9221580638854775807', 'cf_kpi:latency_ms', '145.0'
put 'telecom_kpi', 'TOWER_003#9221580638854775807', 'cf_kpi:packet_loss_pct', '8.50'
put 'telecom_kpi', 'TOWER_003#9221580638854775807', 'cf_kpi:call_dropped', '1'
put 'telecom_kpi', 'TOWER_003#9221580638854775807', 'cf_cell:cell_id', 'CELL_TOWER_003_4G_1800'
put 'telecom_kpi', 'TOWER_003#9221580638854775807', 'cf_cell:technology', '4G'
put 'telecom_kpi', 'TOWER_003#9221580638854775807', 'cf_cell:active_users', '280'
put 'telecom_kpi', 'TOWER_003#9221580638854775807', 'cf_alert:status', 'CRITICAL_OVERLOAD'
put 'telecom_kpi', 'TOWER_003#9221580638854775807', 'cf_alert:overload_flag', 'true'

# Ghi sự kiện cho trạm TOWER_008
put 'telecom_kpi', 'TOWER_008#9221580638854775807', 'cf_kpi:throughput_mbps', '3.10'
put 'telecom_kpi', 'TOWER_008#9221580638854775807', 'cf_kpi:latency_ms', '182.5'
put 'telecom_kpi', 'TOWER_008#9221580638854775807', 'cf_kpi:packet_loss_pct', '11.20'
put 'telecom_kpi', 'TOWER_008#9221580638854775807', 'cf_alert:status', 'CRITICAL_OVERLOAD'

# ------------------------------------------------------------------------------
# 5. THAO TÁC TRUY VẤN: GET (Đọc bản ghi cụ thể theo RowKey)
# ------------------------------------------------------------------------------
# Lấy toàn bộ cột của bản ghi trạm TOWER_003
get 'telecom_kpi', 'TOWER_003#9221580638854775807'

# Chỉ lấy thông số kỹ thuật cf_kpi và cảnh báo cf_alert
get 'telecom_kpi', 'TOWER_003#9221580638854775807', {COLUMN => ['cf_kpi', 'cf_alert']}

# Lấy tối đa 3 versions của cột latency_ms
get 'telecom_kpi', 'TOWER_003#9221580638854775807', {COLUMN => 'cf_kpi:latency_ms', VERSIONS => 3}

# ------------------------------------------------------------------------------
# 6. THAO TÁC QUÉT DỮ LIỆU: SCAN (Quét dữ liệu mới nhất của trạm TOWER_003)
# ------------------------------------------------------------------------------
# Quét các sự kiện mới nhất của trạm TOWER_003, giới hạn 10 sự kiện gần nhất
scan 'telecom_kpi', {STARTROW => 'TOWER_003#', STOPROW => 'TOWER_003~', LIMIT => 10}

# Quét tất cả các trạm trong bảng
scan 'telecom_kpi', {LIMIT => 5}

# ------------------------------------------------------------------------------
# 7. SAO LƯU SNAPSHOT & KIỂM TRA
# ------------------------------------------------------------------------------
snapshot 'telecom_kpi', 'telecom_kpi_snapshot_2026'
list_snapshots

exit
EOF
