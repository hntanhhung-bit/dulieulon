import sqlite3
import csv
import random
import datetime
import os

data_dir = r"c:\dulieulon\data"
os.makedirs(data_dir, exist_ok=True)

sqlite_path = os.path.join(data_dir, "telecom_network.sqlite")
if os.path.exists(sqlite_path):
    os.remove(sqlite_path)

conn = sqlite3.connect(sqlite_path)
cursor = conn.cursor()

# 1. Bảng bts_towers
cursor.execute('''
CREATE TABLE bts_towers (
    tower_id TEXT PRIMARY KEY,
    tower_name TEXT NOT NULL,
    province TEXT NOT NULL,
    district TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    install_date TEXT NOT NULL
)
''')

# 2. Bảng cells_catalog
cursor.execute('''
CREATE TABLE cells_catalog (
    cell_id TEXT PRIMARY KEY,
    tower_id TEXT NOT NULL,
    technology TEXT NOT NULL,
    frequency_mhz INTEGER NOT NULL,
    max_bandwidth_mbps REAL NOT NULL,
    azimuth INTEGER NOT NULL,
    FOREIGN KEY(tower_id) REFERENCES bts_towers(tower_id)
)
''')

# 3. Bảng network_kpi_events
cursor.execute('''
CREATE TABLE network_kpi_events (
    event_id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    tower_id TEXT NOT NULL,
    cell_id TEXT NOT NULL,
    technology TEXT NOT NULL,
    throughput_mbps REAL,
    latency_ms REAL,
    packet_loss_pct REAL,
    call_dropped INTEGER,
    num_active_users INTEGER,
    signal_strength_dbm REAL,
    error_code TEXT,
    FOREIGN KEY(tower_id) REFERENCES bts_towers(tower_id),
    FOREIGN KEY(cell_id) REFERENCES cells_catalog(cell_id)
)
''')

# 4. Bảng customer_complaints
cursor.execute('''
CREATE TABLE customer_complaints (
    complaint_id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    tower_id TEXT NOT NULL,
    cell_id TEXT NOT NULL,
    user_msisdn TEXT NOT NULL,
    complaint_type TEXT NOT NULL,
    status TEXT NOT NULL,
    resolution_time_hrs REAL,
    FOREIGN KEY(tower_id) REFERENCES bts_towers(tower_id),
    FOREIGN KEY(cell_id) REFERENCES cells_catalog(cell_id)
)
''')

# Dữ liệu trạm mẫu
locations = [
    ("Hà Nội", "Cầu Giấy", 21.0333, 105.7833),
    ("Hà Nội", "Hoàn Kiếm", 21.0285, 105.8542),
    ("Hà Nội", "Đống Đa", 21.0180, 105.8285),
    ("Hà Nội", "Hai Bà Trưng", 21.0089, 105.8567),
    ("Đà Nẵng", "Hải Châu", 16.0678, 108.2208),
    ("Đà Nẵng", "Sơn Trà", 16.0820, 108.2435),
    ("Hồ Chí Minh", "Quận 1", 10.7769, 106.7009),
    ("Hồ Chí Minh", "Quận 3", 10.7844, 106.6844),
    ("Hồ Chí Minh", "Bình Thạnh", 10.8106, 106.7091),
    ("Hồ Chí Minh", "Tân Bình", 10.7989, 106.6572)
]

towers_data = []
cells_data = []
tower_count = 20

for i in range(1, tower_count + 1):
    t_id = f"TOWER_{i:03d}"
    loc = locations[(i - 1) % len(locations)]
    name = f"BTS {loc[1]} - Station {i:02d}"
    lat = loc[2] + random.uniform(-0.02, 0.02)
    lon = loc[3] + random.uniform(-0.02, 0.02)
    inst_date = (datetime.date(2021, 1, 1) + datetime.timedelta(days=i*45)).isoformat()
    towers_data.append((t_id, name, loc[0], loc[1], round(lat, 5), round(lon, 5), inst_date))
    
    # Mỗi trạm có 3-4 cell (3G, 4G, 5G)
    for tech, freq, bw in [("3G", 2100, 42.0), ("4G", 1800, 150.0), ("4G", 2600, 300.0), ("5G", 3500, 1000.0)]:
        c_id = f"CELL_{t_id}_{tech}_{freq}"
        azimuth = random.choice([0, 120, 240])
        cells_data.append((c_id, t_id, tech, freq, bw, azimuth))

cursor.executemany("INSERT INTO bts_towers VALUES (?,?,?,?,?,?,?)", towers_data)
cursor.executemany("INSERT INTO cells_catalog VALUES (?,?,?,?,?,?)", cells_data)

# Sinh sự kiện KPI (network_kpi_events)
random.seed(42)
events_data = []
complaints_data = []

start_time = datetime.datetime(2026, 9, 1, 0, 0, 0)
event_idx = 1
complaint_idx = 1

# Đánh dấu 3 trạm bị quá tải/suy giảm nghiêm trọng
degraded_towers = {"TOWER_003", "TOWER_008", "TOWER_015"}

for step in range(150): # 150 mốc thời gian -> 150 * 80 cells = đúng 12,000 bản ghi dữ liệu đo kiểm (12,001 dòng cả header)
    curr_time = start_time + datetime.timedelta(minutes=step * 15)
    t_str = curr_time.strftime("%Y-%m-%d %H:%M:%S")
    
    for c in cells_data:
        c_id, t_id, tech, freq, max_bw, azimuth = c
        is_degraded = t_id in degraded_towers
        
        # Mô phỏng phân phối
        if is_degraded:
            # Quá tải: throughput thấp, latency cao, packet loss cao, rớt cuộc gọi nhiều
            users = random.randint(180, 350)
            tp = round(random.uniform(1.5, 12.0) if tech != "5G" else random.uniform(15.0, 45.0), 2)
            lat = round(random.uniform(95.0, 280.0), 1)
            loss = round(random.uniform(3.5, 14.5), 2)
            dropped = 1 if random.random() < 0.08 else 0
            sig = round(random.uniform(-115.0, -98.0), 1)
            err = random.choice(["ERR_TIMEOUT", "ERR_CONGESTION", "ERR_RAB_SETUP", None])
        else:
            # Bình thường:
            users = random.randint(15, 85)
            if tech == "3G":
                tp = round(random.uniform(8.0, 28.0), 2)
                lat = round(random.uniform(45.0, 75.0), 1)
            elif tech == "4G":
                tp = round(random.uniform(35.0, 110.0), 2)
                lat = round(random.uniform(18.0, 42.0), 1)
            else: # 5G
                tp = round(random.uniform(250.0, 750.0), 2)
                lat = round(random.uniform(8.0, 16.0), 1)
            loss = round(random.uniform(0.05, 0.9), 2)
            dropped = 1 if random.random() < 0.005 else 0
            sig = round(random.uniform(-88.0, -65.0), 1)
            err = None
            
        e_id = f"EVT_{event_idx:07d}"
        event_idx += 1
        
        # Thỉnh thoảng chèn 1 bản ghi bất thường (noise/corrupted) để test Data Cleaning
        if event_idx % 250 == 0:
            events_data.append((e_id, t_str, t_id, c_id, tech, -99.0, -1.0, 99.9, dropped, users, sig, "CORRUPTED"))
        else:
            events_data.append((e_id, t_str, t_id, c_id, tech, tp, lat, loss, dropped, users, sig, err))
            
        # Sinh khiếu nại nếu cell bị suy giảm hoặc rớt cuộc gọi
        if (is_degraded and random.random() < 0.05) or (dropped == 1 and random.random() < 0.3):
            comp_id = f"CMP_{complaint_idx:06d}"
            complaint_idx += 1
            msisdn = f"8498{random.randint(1000000, 9999999)}"
            c_type = random.choice(["Chậm dữ liệu", "Rớt cuộc gọi liên tục", "Mất sóng hoàn toàn", "Độ trễ cao khi chơi game/video call"])
            status = random.choice(["Đã xử lý", "Đang kiểm tra", "Chờ tối ưu trạm"])
            res_time = round(random.uniform(2.0, 48.0), 1)
            complaints_data.append((comp_id, t_str, t_id, c_id, msisdn, c_type, status, res_time))

cursor.executemany("INSERT INTO network_kpi_events VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", events_data)
cursor.executemany("INSERT INTO customer_complaints VALUES (?,?,?,?,?,?,?,?)", complaints_data)

# Tạo chỉ mục tối ưu truy vấn
cursor.execute("CREATE INDEX idx_kpi_tower_tech ON network_kpi_events(tower_id, technology)")
cursor.execute("CREATE INDEX idx_kpi_timestamp ON network_kpi_events(timestamp)")
cursor.execute("CREATE INDEX idx_complaints_tower ON customer_complaints(tower_id)")

conn.commit()
conn.close()

# Xuất ra các file CSV tương ứng
def write_csv(filename, header, data):
    filepath = os.path.join(data_dir, filename)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
    print(f"Exported {filepath} with {len(data)} rows.")

write_csv("bts_towers.csv", ["tower_id", "tower_name", "province", "district", "latitude", "longitude", "install_date"], towers_data)
write_csv("cells_catalog.csv", ["cell_id", "tower_id", "technology", "frequency_mhz", "max_bandwidth_mbps", "azimuth"], cells_data)
write_csv("network_kpi_events.csv", ["event_id", "timestamp", "tower_id", "cell_id", "technology", "throughput_mbps", "latency_ms", "packet_loss_pct", "call_dropped", "num_active_users", "signal_strength_dbm", "error_code"], events_data)
write_csv("customer_complaints.csv", ["complaint_id", "timestamp", "tower_id", "cell_id", "user_msisdn", "complaint_type", "status", "resolution_time_hrs"], complaints_data)

print("Dataset generation completed successfully!")
