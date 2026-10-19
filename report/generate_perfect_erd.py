# -*- coding: utf-8 -*-
"""
TẠO SƠ ĐỒ THỰC THỂ QUAN HỆ DỮ LIỆU VIỄN THÔNG (ERD SCHEMA)
Độ phân giải cao (1450 x 920), layout 2x2 chống chồng chéo, font chữ lớn, sắc nét.
"""

import os
from PIL import Image, ImageDraw, ImageFont

output_dir = r"c:\dulieulon\report"
output_dir2 = r"c:\dulieulon\Output"
os.makedirs(output_dir, exist_ok=True)
os.makedirs(output_dir2, exist_ok=True)

def get_font(size, bold=False):
    font_paths = [
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\tahomabd.ttf" if bold else "C:\\Windows\\Fonts\\tahoma.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def draw_rounded_rect(draw, xy, rad, fill, outline, width=2):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle([x1, y1, x2, y2], radius=rad, fill=fill, outline=outline, width=width)

def draw_table_card(draw, x1, y1, x2, y2, title_vn, title_en, header_bg, rows, f_h_title, f_h_sub, f_row_pk, f_row_fk, f_row_col, f_row_type):
    # Khung bo góc
    draw_rounded_rect(draw, (x1, y1, x2, y2), 12, fill="#FFFFFF", outline=header_bg, width=3)
    
    # Header card
    h_height = 58
    # Vẽ phần header với bo góc trên
    draw.rounded_rectangle([x1, y1, x2, y1 + h_height + 10], radius=12, fill=header_bg)
    draw.rectangle([x1, y1 + h_height - 6, x2, y1 + h_height], fill=header_bg)
    
    # Tiêu đề bảng
    draw.text(((x1 + x2)//2, y1 + 18), title_vn, fill="#FFFFFF", font=f_h_title, anchor="mm")
    draw.text(((x1 + x2)//2, y1 + 42), title_en, fill="#E2E8F0", font=f_h_sub, anchor="mm")
    
    # Các dòng thuộc tính
    row_y = y1 + h_height + 12
    row_gap = 27
    
    for item in rows:
        tag, col_name, data_type = item
        # Phân loại màu sắc
        if tag == "PK":
            tag_color = "#DC2626" # Đỏ tươi
            col_font = f_row_pk
            tag_bg = "#FEE2E2"
        elif tag == "FK":
            tag_color = "#2563EB" # Xanh dương
            col_font = f_row_fk
            tag_bg = "#DBEAFE"
        else:
            tag_color = "#64748B"
            col_font = f_row_col
            tag_bg = "#F1F5F9"
            
        # Tag pill
        if tag:
            draw.rounded_rectangle([x1 + 16, row_y - 10, x1 + 46, row_y + 10], radius=4, fill=tag_bg, outline=tag_color, width=1)
            draw.text((x1 + 31, row_y), tag, fill=tag_color, font=f_row_pk, anchor="mm")
        
        # Tên cột
        draw.text((x1 + 56, row_y), col_name, fill="#0F172A", font=col_font, anchor="lm")
        
        # Kiểu dữ liệu
        draw.text((x2 - 16, row_y), data_type, fill="#475569", font=f_row_type, anchor="rm")
        
        # Đường kẻ phân cách mờ
        draw.line([(x1 + 16, row_y + 14), (x2 - 16, row_y + 14)], fill="#F1F5F9", width=1)
        
        row_y += row_gap

def generate_erd():
    w, h = 1480, 940
    img = Image.new("RGB", (w, h), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    
    f_banner_title = get_font(25, bold=True)
    f_banner_sub = get_font(15, bold=False)
    
    f_h_title = get_font(18, bold=True)
    f_h_sub = get_font(13, bold=False)
    
    f_row_pk = get_font(13, bold=True)
    f_row_fk = get_font(13, bold=True)
    f_row_col = get_font(13, bold=False)
    f_row_type = get_font(12, bold=False)
    
    f_rel = get_font(13, bold=True)
    
    # 1. Top Banner
    draw.rectangle([0, 0, w, 74], fill="#0F172A")
    draw.text((w//2, 26), "SƠ ĐỒ THỰC THỂ QUAN HỆ DỮ LIỆU VIỄN THÔNG (TELECOM ENTITY RELATIONSHIP DIAGRAM - ERD)", fill="#FFFFFF", font=f_banner_title, anchor="mm")
    draw.text((w//2, 54), "Mô hình quan hệ 4 tập dữ liệu: bts_towers, cells_catalog, network_kpi_events, customer_complaints", fill="#94A3B8", font=f_banner_sub, anchor="mm")

    # 2. Định nghĩa cấu trúc 4 bảng
    towers_rows = [
        ("PK", "tower_id", "VARCHAR(20)"),
        ("", "tower_name", "VARCHAR(100)"),
        ("", "province", "VARCHAR(50)"),
        ("", "district", "VARCHAR(50)"),
        ("", "latitude", "DOUBLE"),
        ("", "longitude", "DOUBLE"),
        ("", "install_date", "DATE"),
        ("", "status", "VARCHAR(20)")
    ]
    
    cells_rows = [
        ("PK", "cell_id", "VARCHAR(20)"),
        ("FK", "tower_id", "VARCHAR(20)"),
        ("", "technology", "VARCHAR(10) [3G/4G/5G]"),
        ("", "frequency_mhz", "INT [1800-3500]"),
        ("", "max_bandwidth_mbps", "DOUBLE [42-1000]"),
        ("", "azimuth_degrees", "INT [0°, 120°, 240°]"),
        ("", "antenna_tilt", "DOUBLE [Tilt góc]"),
        ("", "hardware_vendor", "VARCHAR(50)")
    ]
    
    events_rows = [
        ("PK", "event_id", "VARCHAR(30)"),
        ("", "timestamp", "TIMESTAMP (yyyy-MM-dd)"),
        ("FK", "tower_id", "VARCHAR(20)"),
        ("FK", "cell_id", "VARCHAR(20)"),
        ("", "technology", "VARCHAR(10)"),
        ("", "throughput_mbps", "DOUBLE (Tốc độ tải)"),
        ("", "latency_ms", "DOUBLE (Độ trễ ping)"),
        ("", "packet_loss_pct", "DOUBLE (Tỷ lệ mất gói %)"),
        ("", "call_dropped", "INT (0: Thành công / 1: Rớt)"),
        ("", "num_active_users", "INT (Số thuê bao tải)"),
        ("", "signal_strength_dbm", "DOUBLE (Mức thu RSRP)"),
        ("", "error_code", "VARCHAR(30) (Mã lỗi NOC)")
    ]
    
    complaints_rows = [
        ("PK", "complaint_id", "VARCHAR(30)"),
        ("", "timestamp", "TIMESTAMP (Thời điểm)"),
        ("FK", "tower_id", "VARCHAR(20)"),
        ("FK", "cell_id", "VARCHAR(20)"),
        ("", "user_msisdn", "VARCHAR(20) (Số ĐT)"),
        ("", "complaint_type", "VARCHAR(50) (Loại sự cố)"),
        ("", "status", "VARCHAR(20) (Tiến độ)"),
        ("", "resolution_time_hrs", "DOUBLE (Giờ xử lý)"),
        ("", "notes", "TEXT (Ghi chú kỹ thuật)")
    ]
    
    # 3. Tọa độ các khối (Layout 2x2 thoáng đãng)
    # Hàng trên:
    # Bảng 1: bts_towers (Trái trên)
    b1_x1, b1_y1, b1_x2, b1_y2 = 45, 105, 520, 420
    draw_table_card(draw, b1_x1, b1_y1, b1_x2, b1_y2, 
                    "bts_towers", "Danh mục Trạm phát sóng BTS", 
                    "#1E40AF", towers_rows, f_h_title, f_h_sub, f_row_pk, f_row_fk, f_row_col, f_row_type)
    
    # Bảng 2: cells_catalog (Phải trên)
    b2_x1, b2_y1, b2_x2, b2_y2 = 960, 105, 1435, 420
    draw_table_card(draw, b2_x1, b2_y1, b2_x2, b2_y2, 
                    "cells_catalog", "Danh mục Sector Cell Vô tuyến", 
                    "#065F46", cells_rows, f_h_title, f_h_sub, f_row_pk, f_row_fk, f_row_col, f_row_type)
    
    # Hàng dưới:
    # Bảng 3: network_kpi_events (Trái dưới - Bảng sự kiện Fact trung tâm)
    b3_x1, b3_y1, b3_x2, b3_y2 = 45, 510, 560, 915
    draw_table_card(draw, b3_x1, b3_y1, b3_x2, b3_y2, 
                    "network_kpi_events", "Dữ liệu Đo kiểm Phiên (12,000 sự kiện)", 
                    "#9A3412", events_rows, f_h_title, f_h_sub, f_row_pk, f_row_fk, f_row_col, f_row_type)
    
    # Bảng 4: customer_complaints (Phải dưới)
    b4_x1, b4_y1, b4_x2, b4_y2 = 920, 510, 1435, 875
    draw_table_card(draw, b4_x1, b4_y1, b4_x2, b4_y2, 
                    "customer_complaints", "Phản ánh Khiếu nại Khách hàng", 
                    "#831843", complaints_rows, f_h_title, f_h_sub, f_row_pk, f_row_fk, f_row_col, f_row_type)
    
    # 4. Vẽ các đường quan hệ (Relationship Lines) - Tuyệt đối không cắt ngang chữ!
    # Quan hệ 1: bts_towers (1) -> cells_catalog (N) qua tower_id
    # Đi ngang qua khoảng trống ở giữa hai bảng hàng trên
    y_rel1 = 200
    draw.line([(b1_x2, y_rel1), (b2_x1, y_rel1)], fill="#1E40AF", width=3)
    # Mũi tên chỉ vào cells_catalog
    draw.polygon([(b2_x1, y_rel1), (b2_x1 - 12, y_rel1 - 7), (b2_x1 - 12, y_rel1 + 7)], fill="#1E40AF")
    # Điểm gốc tròn tại bts_towers
    draw.ellipse([b1_x2 - 5, y_rel1 - 5, b1_x2 + 5, y_rel1 + 5], fill="#1E40AF")
    # Nhãn quan hệ
    lbl1_box = (640, y_rel1 - 24, 840, y_rel1 + 24)
    draw_rounded_rect(draw, lbl1_box, 6, fill="#EFF6FF", outline="#1E40AF", width=2)
    draw.text(((lbl1_box[0] + lbl1_box[2])//2, y_rel1), "1 : N (tower_id)", fill="#1E40AF", font=f_rel, anchor="mm")

    # Quan hệ 2: bts_towers (1) -> network_kpi_events (N) qua tower_id
    # Đi thẳng đứng từ đáy bảng 1 xuống đỉnh bảng 3
    x_rel2 = 250
    draw.line([(x_rel2, b1_y2), (x_rel2, b3_y1)], fill="#1E40AF", width=3)
    draw.polygon([(x_rel2, b3_y1), (x_rel2 - 7, b3_y1 - 12), (x_rel2 + 7, b3_y1 - 12)], fill="#1E40AF")
    draw.ellipse([x_rel2 - 5, b1_y2 - 5, x_rel2 + 5, b1_y2 + 5], fill="#1E40AF")
    # Nhãn quan hệ
    lbl2_box = (x_rel2 - 80, 445, x_rel2 + 80, 485)
    draw_rounded_rect(draw, lbl2_box, 6, fill="#EFF6FF", outline="#1E40AF", width=2)
    draw.text((x_rel2, 465), "1 : N (tower_id)", fill="#1E40AF", font=f_rel, anchor="mm")

    # Quan hệ 3: cells_catalog (1) -> network_kpi_events (N) qua cell_id
    # Đường đi thông minh: Từ đáy cells_catalog (x=1100, y=420) đi xuống y=475, rẽ trái sang x=420, rồi cắm xuống đỉnh bảng 3 (y=510)!
    draw.line([(1100, b2_y2), (1100, 475)], fill="#065F46", width=3)
    draw.line([(1100, 475), (420, 475)], fill="#065F46", width=3)
    draw.line([(420, 475), (420, b3_y1)], fill="#065F46", width=3)
    draw.polygon([(420, b3_y1), (420 - 7, b3_y1 - 12), (420 + 7, b3_y1 - 12)], fill="#065F46")
    draw.ellipse([1100 - 5, b2_y2 - 5, 1100 + 5, b2_y2 + 5], fill="#065F46")
    # Nhãn quan hệ
    lbl3_box = (670, 455, 870, 495)
    draw_rounded_rect(draw, lbl3_box, 6, fill="#ECFDF5", outline="#065F46", width=2)
    draw.text(((lbl3_box[0] + lbl3_box[2])//2, 475), "1 : N (cell_id)", fill="#065F46", font=f_rel, anchor="mm")

    # Quan hệ 4: network_kpi_events (1) -> customer_complaints (N) qua (tower_id, cell_id)
    # Đi ngang qua khoảng trống ở giữa hai bảng hàng dưới
    y_rel4 = 680
    draw.line([(b3_x2, y_rel4), (b4_x1, y_rel4)], fill="#831843", width=3)
    draw.polygon([(b4_x1, y_rel4), (b4_x1 - 12, y_rel4 - 7), (b4_x1 - 12, y_rel4 + 7)], fill="#831843")
    draw.ellipse([b3_x2 - 5, y_rel4 - 5, b3_x2 + 5, y_rel4 + 5], fill="#831843")
    # Nhãn quan hệ
    lbl4_box = (630, y_rel4 - 24, 850, y_rel4 + 24)
    draw_rounded_rect(draw, lbl4_box, 6, fill="#FDF2F8", outline="#831843", width=2)
    draw.text(((lbl4_box[0] + lbl4_box[2])//2, y_rel4), "1 : N (tower, cell)", fill="#831843", font=f_rel, anchor="mm")

    # Lưu ảnh ra cả 2 thư mục
    path1 = os.path.join(output_dir, "hinh_2_1_mo_hinh_du_lieu.png")
    path2 = os.path.join(output_dir2, "hinh_2_1_mo_hinh_du_lieu.png")
    img.save(path1, quality=95)
    img.save(path2, quality=95)
    print(f"Generated clean ERD at:\n  {path1}\n  {path2}")

if __name__ == "__main__":
    generate_erd()
