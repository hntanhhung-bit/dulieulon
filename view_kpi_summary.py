# -*- coding: utf-8 -*-
import os
import sys

# Thêm thư mục chứa sqlite3.dll vào DLL path
bin_dir = r"C:\Users\DELL\AppData\Local\Programs\OSGeo4W\bin"
if os.path.exists(bin_dir):
    try:
        os.add_dll_directory(bin_dir)
    except Exception:
        pass
    os.environ['PATH'] = bin_dir + ';' + os.environ.get('PATH', '')

import sqlite3

# Đảm bảo hiển thị tiếng Việt trên Windows terminal
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

db_path = r"c:\dulieulon\data\telecom_network.sqlite"

if not os.path.exists(db_path):
    print(f"Không tìm thấy file CSDL tại: {db_path}")
    sys.exit(1)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# 1. Liệt kê các bảng trong database
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [t[0] for t in cur.fetchall()]
print("=" * 95)
print(f"CÁC BẢNG HIỆN CÓ TRONG CSDL ({db_path}):")
print(", ".join(tables))
print("=" * 95)

target_table = "kpi_analysis_summary"

if target_table not in tables:
    print(f"Bảng '{target_table}' chưa có trong CSDL. Kiểm tra các bảng khác...")
else:
    # 2. Xem cấu trúc các cột
    cur.execute(f"PRAGMA table_info({target_table});")
    columns_info = cur.fetchall()
    print(f"\nCẤU TRÚC BẢNG '{target_table}':")
    for col in columns_info:
        print(f"  - Cột {col[0]}: {col[1]:<22} (Kiểu: {col[2]})")

    # 3. Đếm tổng số dòng
    cur.execute(f"SELECT COUNT(*) FROM {target_table};")
    total_rows = cur.fetchone()[0]
    print(f"\nTổng số dòng dữ liệu: {total_rows} bản ghi.")

    # 4. In mẫu 15 dòng đầu tiên định dạng bảng đẹp mắt
    print("\n" + "=" * 95)
    print(f"DỮ LIỆU BẢNG '{target_table}' (15 DÒNG TIÊU BIỂU):")
    print("=" * 95)
    
    cur.execute(f"SELECT * FROM {target_table} LIMIT 15;")
    rows = cur.fetchall()
    col_names = [d[0] for d in cur.description]
    
    # In header
    header_str = " | ".join(f"{name:<12}" for name in col_names[:8])
    print(header_str)
    print("-" * 95)
    for r in rows:
        row_str = " | ".join(f"{str(val)[:12]:<12}" for val in r[:8])
        print(row_str)
    print("=" * 95)

conn.close()
