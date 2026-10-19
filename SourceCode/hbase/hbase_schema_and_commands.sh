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
# cf_cell:  Lưu cấu hình vật lý vô tuyến (cell_id, tech, freq, users). VERSIONS => 1 (dữ liệu cấu hình ít đổi)
# cf_alert: Lưu cảnh báo và trạng thái sự cố (status, overload_flag, complaint_id). VERSIONS => 3
# Thuật toán nén: SNAPPY (tốc độ nén và giải nén cực nhanh, giảm 60-70% dung lượng đĩa)

# ------------------------------------------------------------------------------
# 3. LỆNH TẠO BẢNG (CREATE TABLE) KÈM PRE-SPLITTING
# ------------------------------------------------------------------------------
hbase shell << 'EOF'

-- Vô hiệu hóa và xóa bảng cũ nếu tồn tại
disable 'telecom_kpi'
drop 'telecom_kpi'

-- Tạo bảng mới với 3 Column Families, Pre-splitting thành 4 Regions
create 'telecom_kpi', \
  {NAME => 'cf_kpi',   VERSIONS => 3, COMPRESSION => 'SNAPPY', TTL => 7776000, BLOCKCACHE => true}, \
  {NAME => 'cf_cell',  VERSIONS => 1, COMPRESSION => 'SNAPPY', BLOCKCACHE => true}, \
  {NAME => 'cf_alert', VERSIONS => 3, COMPRESSION => 'SNAPPY', BLOCKCACHE => true}, \
  {SPLITS => ['TOWER_005#', 'TOWER_010#', 'TOWER_015#']}

-- -----------------------------------------------------------------------------
-- 4. THAO TÁC DỮ LIỆU: PUT (Ghi bản ghi mới)
-- -----------------------------------------------------------------------------
-- Ghi sự kiện cho trạm TOWER_003
put 'telecom_kpi', 'TOWER_003#9221580638854775807', 'cf_kpi:throughput_mbps', '4.25'
put 'telecom_kpi', 'TOWER_003#9221580638854775807', 'cf_kpi:latency_ms', '145.0'
put 'telecom_kpi', 'TOWER_003#9221580638854775807', 'cf_kpi:packet_loss_pct', '8.50'
put 'telecom_kpi', 'TOWER_003#9221580638854775807', 'cf_kpi:call_dropped', '1'
put 'telecom_kpi', 'TOWER_003#9221580638854775807', 'cf_cell:cell_id', 'CELL_TOWER_003_4G_1800'
put 'telecom_kpi', 'TOWER_003#9221580638854775807', 'cf_cell:technology', '4G'
put 'telecom_kpi', 'TOWER_003#9221580638854775807', 'cf_cell:active_users', '280'
put 'telecom_kpi', 'TOWER_003#9221580638854775807', 'cf_alert:status', 'CRITICAL_OVERLOAD'
put 'telecom_kpi', 'TOWER_003#9221580638854775807', 'cf_alert:overload_flag', 'true'

-- -----------------------------------------------------------------------------
-- 5. THAO TÁC TRUY VẤN: GET (Đọc bản ghi cụ thể theo RowKey)
-- -----------------------------------------------------------------------------
-- Lấy toàn bộ cột của bản ghi
get 'telecom_kpi', 'TOWER_003#9221580638854775807'

-- Chỉ lấy thông số kỹ thuật cf_kpi và cảnh báo cf_alert
get 'telecom_kpi', 'TOWER_003#9221580638854775807', {COLUMN => ['cf_kpi', 'cf_alert']}

-- Lấy tối đa 3 versions của cột latency_ms
get 'telecom_kpi', 'TOWER_003#9221580638854775807', {COLUMN => 'cf_kpi:latency_ms', VERSIONS => 3}

-- -----------------------------------------------------------------------------
-- 6. THAO TÁC QUÉT DỮ LIỆU: SCAN (Quét dữ liệu mới nhất của trạm TOWER_003)
-- -----------------------------------------------------------------------------
-- Quét các sự kiện mới nhất của trạm TOWER_003, giới hạn 10 sự kiện gần nhất
scan 'telecom_kpi', {STARTROW => 'TOWER_003#', STOPROW => 'TOWER_003~', LIMIT => 10}

-- Quét lọc các cell có trạng thái cảnh báo quá tải
scan 'telecom_kpi', {FILTER => "ValueFilter(=, 'binary:CRITICAL_OVERLOAD')"}

-- -----------------------------------------------------------------------------
-- 7. THAO TÁC XÓA: DELETE
-- -----------------------------------------------------------------------------
-- Xóa một cell cụ thể (ví dụ xóa cờ cảnh báo đã được giải quyết)
delete 'telecom_kpi', 'TOWER_003#9221580638854775807', 'cf_alert:overload_flag'

-- Xóa toàn bộ row (toàn bộ các column family tại RowKey này)
deleteall 'telecom_kpi', 'TOWER_003#9221580638854775807'

-- -----------------------------------------------------------------------------
-- 8. SAO LƯU (BACKUP & RESTORE) VÀ PHÂN QUYỀN TRUY CẬP (ACCESS CONTROL - ACL)
-- -----------------------------------------------------------------------------
-- Tạo Snapshot tức thời không làm gián đoạn hệ thống đang chạy (Zero-downtime)
snapshot 'telecom_kpi', 'telecom_kpi_snapshot_20260918'

-- Liệt kê và kiểm tra snapshot
list_snapshots

-- Khôi phục bảng từ snapshot khi gặp sự cố dữ liệu
-- disable 'telecom_kpi'
-- restore_snapshot 'telecom_kpi_snapshot_20260918'
-- enable 'telecom_kpi'

-- Phân quyền truy cập (ACL):
-- Cấp quyền Đọc/Ghi (RW) cho nhóm kỹ sư giám sát mạng (telecom_ops)
grant 'telecom_ops', 'RW', 'telecom_kpi'

-- Cấp quyền Chỉ đọc (R) cho nhóm phân tích dữ liệu & BI (telecom_analysts)
grant 'telecom_analysts', 'R', 'telecom_kpi'

-- Cấp toàn quyền Quản trị (RWCA) cho Quản trị viên viễn thông (admin)
grant 'telecom_admin', 'RWCA', 'telecom_kpi'

exit
EOF
