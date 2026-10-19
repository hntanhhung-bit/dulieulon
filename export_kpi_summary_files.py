# -*- coding: utf-8 -*-
import os
import sys

bin_dir = r"C:\Users\DELL\AppData\Local\Programs\OSGeo4W\bin"
if os.path.exists(bin_dir):
    try:
        os.add_dll_directory(bin_dir)
    except Exception:
        pass
    os.environ['PATH'] = bin_dir + ';' + os.environ.get('PATH', '')

import sqlite3
import csv

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

db_path = r"c:\dulieulon\data\telecom_network.sqlite"
csv_path = r"c:\dulieulon\data\kpi_analysis_summary.csv"
html_path = r"c:\dulieulon\report\kpi_analysis_summary.html"

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("SELECT * FROM kpi_analysis_summary ORDER BY call_drop_rate_pct DESC;")
rows = cur.fetchall()
col_names = [d[0] for d in cur.description]

# 1. Xuất file CSV để mở trực tiếp bằng Excel
with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(col_names)
    writer.writerows(rows)

print(f"[OK] Đã xuất file CSV chuẩn Excel UTF-8 BOM: {csv_path}")

# 2. Xuất file HTML để mở trực tiếp trên trình duyệt
html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Bảng dữ liệu kpi_analysis_summary</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; background-color: #f8fafc; }}
        h2 {{ color: #1e3a8a; }}
        .badge-bad {{ background-color: #fee2e2; color: #991b1b; padding: 3px 8px; border-radius: 4px; font-weight: bold; }}
        .badge-good {{ background-color: #dcfce7; color: #166534; padding: 3px 8px; border-radius: 4px; font-weight: bold; }}
        table {{ border-collapse: collapse; width: 100%; background: #ffffff; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border-radius: 8px; overflow: hidden; }}
        th {{ background-color: #1e3a8a; color: #ffffff; padding: 10px 12px; text-align: left; font-size: 13px; position: sticky; top: 0; }}
        td {{ padding: 8px 12px; border-bottom: 1px solid #e2e8f0; font-size: 13px; color: #1e293b; }}
        tr:nth-child(even) {{ background-color: #f8fafc; }}
        tr:hover {{ background-color: #f1f5f9; }}
    </style>
</head>
<body>
    <h2>📊 BẢNG DỮ LIỆU TỔNG HỢP: kpi_analysis_summary ({len(rows)} bản ghi)</h2>
    <p>Trích xuất từ CSDL: <code>{db_path}</code></p>
    <table>
        <thead>
            <tr>{''.join(f'<th>{c}</th>' for c in col_names)}</tr>
        </thead>
        <tbody>
"""

for r in rows:
    html_content += "<tr>"
    for idx, val in enumerate(r):
        str_v = str(val)
        if col_names[idx] == 'predicted_complaint_risk':
            badge_class = "badge-bad" if "HIGH" in str_v or "NGUY" in str_v else "badge-good"
            html_content += f"<td><span class='{badge_class}'>{str_v}</span></td>"
        else:
            html_content += f"<td>{str_v}</td>"
    html_content += "</tr>\n"

html_content += """
        </tbody>
    </table>
</body>
</html>
"""

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"[OK] Đã xuất file HTML giao diện đẹp: {html_path}")
conn.close()
