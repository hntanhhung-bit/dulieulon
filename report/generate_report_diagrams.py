import os
from PIL import Image, ImageDraw, ImageFont

output_dir = r"c:\dulieulon\report"
os.makedirs(output_dir, exist_ok=True)

def get_font(size, bold=False):
    # Try Windows fonts
    font_paths = [
        "C:\\Windows\\Fonts\\tahomabd.ttf" if bold else "C:\\Windows\\Fonts\\tahoma.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
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

# ------------------------------------------------------------------------------
# 1. HÌNH 1.1: SƠ ĐỒ KIẾN TRÚC TỔNG THỂ HỆ THỐNG (LAMBDA / BIG DATA ARCHITECTURE)
# ------------------------------------------------------------------------------
def create_architecture_diagram():
    w, h = 1200, 680
    img = Image.new("RGB", (w, h), "#F8FAFC")
    draw = ImageDraw.Draw(img)

    f_title = get_font(24, bold=True)
    f_sub = get_font(15, bold=False)
    f_sec = get_font(18, bold=True)
    f_box_t = get_font(15, bold=True)
    f_box_d = get_font(13, bold=False)

    # Header Banner
    draw.rectangle([0, 0, w, 70], fill="#1E293B")
    draw.text((w//2, 25), "KIẾN TRÚC HỆ THỐNG PHÂN TÍCH CHẤT LƯỢNG MẠNG VIỄN THÔNG (LAMBDA ARCHITECTURE)", fill="#F8FAFC", font=f_title, anchor="mm")
    draw.text((w//2, 52), "Tích hợp Thu thập, Lưu trữ phân tán, Xử lý lô & Thời gian thực, Cơ sở dữ liệu NoSQL/RDBMS và Trực quan hóa BI", fill="#94A3B8", font=f_sub, anchor="mm")

    # Layer Columns
    cols = [
        ("1. NGUỒN DỮ LIỆU\n(Data Sources)", 40, 240, "#EFF6FF", "#3B82F6", [
            ("50,000+ Trạm BTS", "Tín hiệu vô tuyến 3G/4G/5G\nChu kỳ đo 1s - 10s"),
            ("CDR / xDR Logs", "Bản ghi cước & phiên dữ liệu\n10 - 25 GB log thô/ngày"),
            ("Hệ thống CSKH", "Customer Complaints\nKhiếu nại rớt mạng, chậm"),
        ]),
        ("2. THU THẬP & LƯU TRỮ\n(Ingestion & Storage)", 270, 480, "#F0FDF4", "#22C55E", [
            ("Apache Flume Agent", "SpoolDir Source -> File Channel\nĐẩy luồng log tự động vào HDFS"),
            ("Hadoop HDFS Cluster", "Lưu trữ phân tán 128MB Block\nReplication Factor = 3 (Chống lỗi)"),
            ("Metadata Catalog", "BTS Towers & Cells Catalog\nThông tin địa lý & cấu hình cell"),
        ]),
        ("3. TẦNG XỬ LÝ (COMPUTE)\n(Batch & Speed Layer)", 510, 770, "#FEFCE8", "#EAB308", [
            ("MapReduce (Java)", "Composite Key & Partitioner\nTổng hợp KPI dung lượng cực lớn"),
            ("Apache Spark & Spark SQL", "Xử lý In-Memory tốc độ cao\nLàm sạch, Join 4 bảng, Lọc KPI"),
            ("Apache Pig Latin", "ETL chuyển đổi định dạng\nLọc và phân cụm trạm lỗi"),
        ]),
        ("4. TẦNG PHỤC VỤ (SERVING)\n(NoSQL & RDBMS)", 800, 980, "#FAF5FF", "#A855F7", [
            ("Apache HBase NoSQL", "Column-family kpi_metrics\nTruy cập ngẫu nhiên < 10ms"),
            ("SQLite Database", "telecom_network.sqlite\nLưu trữ kết quả phân tích R"),
        ]),
        ("5. BÁO CÁO & PHÂN TÍCH\n(Analytics & BI)", 1000, 1170, "#FFF1F2", "#F43F5E", [
            ("BigSheets Simulator", "Dashboard tương tác KPI\nLọc theo Tỉnh, Trạm, Công nghệ"),
            ("R & RStudio (ML)", "Hồi quy Logistic dự báo khiếu nại\nTrực quan hóa đồ thị ggplot2"),
        ]),
    ]

    for title, x1, x2, bg, border, boxes in cols:
        draw_rounded_rect(draw, (x1, 90, x2, 650), 12, fill=bg, outline=border, width=2)
        # Section title
        draw.text(((x1 + x2)//2, 125), title, fill="#0F172A", font=f_sec, anchor="mm", align="center")

        # Inner boxes
        y_box = 175
        for b_title, b_desc in boxes:
            box_h = 135
            draw_rounded_rect(draw, (x1 + 10, y_box, x2 - 10, y_box + box_h), 8, fill="#FFFFFF", outline="#CBD5E1", width=1)
            draw.text(((x1 + x2)//2, y_box + 28), b_title, fill=border, font=f_box_t, anchor="mm")
            draw.text(((x1 + x2)//2, y_box + 75), b_desc, fill="#475569", font=f_box_d, anchor="mm", align="center")
            y_box += box_h + 15

    # Connective arrows across columns
    arrow_y = [240, 390, 540]
    for y in arrow_y:
        draw.polygon([(245, y-5), (265, y), (245, y+5)], fill="#64748B")
        draw.line([(240, y), (265, y)], fill="#64748B", width=3)
        draw.polygon([(485, y-5), (505, y), (485, y+5)], fill="#64748B")
        draw.line([(480, y), (505, y)], fill="#64748B", width=3)
        draw.polygon([(775, y-5), (795, y), (775, y+5)], fill="#64748B")
        draw.line([(770, y), (795, y)], fill="#64748B", width=3)
        draw.polygon([(985, y-5), (995, y), (985, y+5)], fill="#64748B")
        draw.line([(980, y), (995, y)], fill="#64748B", width=3)

    img.save(os.path.join(output_dir, "hinh_1_1_kien_truc_tong_the.png"), quality=95)
    print("Saved hinh_1_1_kien_truc_tong_the.png")

# ------------------------------------------------------------------------------
# 2. HÌNH 3.1: PIPELINE XỬ LÝ DỮ LIỆU ĐẦU CUỐI (DATA PIPELINE)
# ------------------------------------------------------------------------------
def create_pipeline_diagram():
    w, h = 1350, 530
    img = Image.new("RGB", (w, h), "#F8FAFC")
    draw = ImageDraw.Draw(img)

    f_title = get_font(21, bold=True)
    f_sub = get_font(12, bold=False)
    f_step = get_font(14, bold=True)
    f_name = get_font(15, bold=True)
    f_tech = get_font(12, bold=True)
    f_desc = get_font(11, bold=False)

    # Top Banner
    draw.rectangle([0, 0, w, 70], fill="#0F172A")
    draw.rectangle([0, 67, w, 70], fill="#38BDF8")  # Accent cyan line
    draw.text((w//2, 26), "PIPELINE THU THẬP, TIỀN XỬ LÝ VÀ PHÂN TÍCH DỮ LIỆU LỚN VIỄN THÔNG", fill="#FFFFFF", font=f_title, anchor="mm")
    draw.text((w//2, 50), "Quy trình dữ liệu đầu cuối: Ingestion (Flume) → Storage (HDFS) → ETL (Spark/Pig) → Batch Analytics (MapReduce) → Serving (R / BigSheets)", fill="#94A3B8", font=f_sub, anchor="mm")

    steps = [
        ("BƯỚC 1", "THU THẬP LOG", "Apache Flume", [
            "• Thu thập 12.000 log đo kiểm",
            "• 12.001 dòng dữ liệu gốc",
            "• Đóng gói batch 1.000 events",
            "• Chuyển qua Flume HDFS Sink",
            "• Ghi bền vững FileChannel"
        ], "#F0F9FF", "#0284C7"),

        ("BƯỚC 2", "LƯU TRỮ HDFS", "Hadoop HDFS", [
            "• Lưu tại /telecom/curated/",
            "• Phân vùng block 128 MB",
            "• Nhân bản 3 bản sao tin cậy",
            "• Đảm bảo toàn vẹn dữ liệu",
            "• Sẵn sàng cho Batch & Speed"
        ], "#F0FDF4", "#16A34A"),

        ("BƯỚC 3", "LÀM SẠCH & ETL", "Spark & Pig", [
            "• Lọc dữ liệu lỗi, âm vô lý",
            "  (throughput < 0, latency < 0)",
            "• Join kết hợp 4 tệp dữ liệu",
            "• Tính toán chỉ số CDR %",
            "• Gán nhãn Health Status"
        ], "#FEFCE8", "#D97706"),

        ("BƯỚC 4", "TÍNH TOÁN KPI", "MapReduce / SQL", [
            "• Gộp nhóm (tower_id, tech)",
            "• Tính TB độ trễ & mất gói",
            "• Custom Partitioner tối ưu",
            "• Phát hiện trạm nghẽn mạng",
            "  (TOWER_003, 008, 015)"
        ], "#FAF5FF", "#9333EA"),

        ("BƯỚC 5", "DỰ BÁO & BÁO CÁO", "R & BigSheets", [
            "• Mô hình Logistic Regression",
            "• Dự báo nguy cơ khiếu nại",
            "• Dashboard BigSheets NOC",
            "• Cảnh báo SLA thời gian thực",
            "• Đồng bộ kết quả vào SQLite"
        ], "#FFF1F2", "#E11D48"),
    ]

    box_w = 225
    box_h = 380
    gap = 34
    x_start = (w - (5 * box_w + 4 * gap)) // 2  # Căn giữa hoàn hảo
    y1 = 100
    y2 = y1 + box_h

    for i, (b_step, b_name, b_tech, b_items, bg_col, border_col) in enumerate(steps):
        x1 = x_start + i * (box_w + gap)
        x2 = x1 + box_w

        # Hộp chính với viền bo tròn
        draw_rounded_rect(draw, (x1, y1, x2, y2), 12, fill=bg_col, outline=border_col, width=2)
        
        # Step header pill
        pill_w = 110
        pill_x1 = (x1 + x2 - pill_w) // 2
        pill_x2 = pill_x1 + pill_w
        draw_rounded_rect(draw, (pill_x1, y1 + 14, pill_x2, y1 + 42), 6, fill=border_col, outline=border_col, width=1)
        draw.text(((x1 + x2)//2, y1 + 28), b_step, fill="#FFFFFF", font=f_step, anchor="mm")

        # Name & Tech
        draw.text(((x1 + x2)//2, y1 + 68), b_name, fill="#0F172A", font=f_name, anchor="mm")
        draw.text(((x1 + x2)//2, y1 + 94), f"[{b_tech}]", fill=border_col, font=f_tech, anchor="mm")
        draw.line([(x1 + 18, y1 + 114), (x2 - 18, y1 + 114)], fill="#CBD5E1", width=1)

        # Content Bullet Items
        cur_y = y1 + 134
        for item in b_items:
            # Nếu là dòng thụt lề phụ
            if item.startswith("  "):
                draw.text((x1 + 22, cur_y), item.strip(), fill="#64748B", font=f_desc, anchor="lt")
                cur_y += 24
            else:
                draw.text((x1 + 14, cur_y), item, fill="#1E293B", font=f_desc, anchor="lt")
                cur_y += 28

        # Mũi tên kết nối giữa các bước (nằm hoàn toàn trong khoảng gap, không chạm chữ)
        if i < len(steps) - 1:
            ax1 = x2 + 4
            ax2 = x2 + gap - 4
            ay = y1 + box_h // 2
            # Đầu mũi tên
            draw.polygon([(ax2, ay), (ax2 - 10, ay - 6), (ax2 - 10, ay + 6)], fill="#64748B")
            # Thân mũi tên
            draw.line([(ax1, ay), (ax2 - 8, ay)], fill="#64748B", width=3)

    # Lưu cả vào report và Output
    out_file1 = os.path.join(output_dir, "hinh_3_1_pipeline_xu_ly.png")
    img.save(out_file1, quality=95)
    
    output_folder = r"c:\dulieulon\Output"
    if os.path.exists(output_folder):
        img.save(os.path.join(output_folder, "hinh_3_1_pipeline_xu_ly.png"), quality=95)
        
    print("Saved hinh_3_1_pipeline_xu_ly.png to report and Output")

# ------------------------------------------------------------------------------
# 3. HÌNH 3.2: SƠ ĐỒ LUỒNG MAPREDUCE TỐI ƯU
# ------------------------------------------------------------------------------
def create_mapreduce_diagram():
    w, h = 1100, 520
    img = Image.new("RGB", (w, h), "#F8FAFC")
    draw = ImageDraw.Draw(img)

    f_title = get_font(22, bold=True)
    f_head = get_font(16, bold=True)
    f_text = get_font(13, bold=False)

    draw.rectangle([0, 0, w, 60], fill="#1E293B")
    draw.text((w//2, 30), "SƠ ĐỒ THUẬT TOÁN MAPREDUCE TỐI ƯU: COMPOSITE KEY & CUSTOM PARTITIONER", fill="#FFFFFF", font=f_title, anchor="mm")

    # 4 stages
    stages = [
        ("1. PHA MAP (Mapper)", 40, 270, "#EFF6FF", "#2563EB", [
            "Input: network_kpi_events.csv",
            "Loại bỏ dữ liệu lỗi (âm, ngoại lai)",
            "Tách trường: tower_id, tech",
            "Phát ra Khóa phức hợp:",
            "Key: (TOWER_001, 4G)",
            "Value: (tp, lat, loss, drop, calls, 1)"
        ]),
        ("2. COMBINER (Tại chỗ)", 300, 530, "#FEF3C7", "#D97706", [
            "Chạy cục bộ trên từng Node DataNode",
            "Cộng dồn thông lượng, độ trễ",
            "Cộng dồn số cuộc gọi & rớt",
            "Giảm 80% lưu lượng mạng",
            "trước khi truyền Shuffle",
            "Output: Tổng trung gian tích lũy"
        ]),
        ("3. PARTITIONER & SHUFFLE", 560, 790, "#F3E8FF", "#7C3AED", [
            "Custom TowerPartitioner",
            "Hash theo tower_id duy nhất",
            "partition = (tower_id.hash & MAX) % N",
            "Đảm bảo cùng 1 trạm BTS",
            "(3G, 4G, 5G) về CÙNG 1 REDUCER",
            "Tránh Data Skew (lệch dữ liệu)"
        ]),
        ("4. PHA REDUCE (Reducer)", 820, 1060, "#DCFCE7", "#15803D", [
            "Nhận toàn bộ dữ liệu của từng trạm",
            "Tính Avg Throughput, Avg Latency",
            "Tính Avg Packet Loss, CDR %",
            "Phân loại trạng thái trạm:",
            "NORMAL hoặc DEGRADED_QUALITY",
            "Ghi kết quả định dạng báo cáo"
        ]),
    ]

    for title, x1, x2, bg, border, items in stages:
        draw_rounded_rect(draw, (x1, 90, x2, 480), 10, fill=bg, outline=border, width=2)
        draw.text(((x1 + x2)//2, 125), title, fill=border, font=f_head, anchor="mm")
        draw.line([(x1 + 15, 145), (x2 - 15, 145)], fill="#CBD5E1", width=1)

        y_item = 175
        for it in items:
            draw.text(((x1 + x2)//2, y_item), it, fill="#1E293B", font=f_text, anchor="mm")
            y_item += 45

    # Connective arrows
    for x in [275, 535, 795]:
        draw.polygon([(x + 20, 270), (x + 5, 263), (x + 5, 277)], fill="#475569")
        draw.line([(x, 270), (x + 20, 270)], fill="#475569", width=3)

    img.save(os.path.join(output_dir, "hinh_3_2_luong_mapreduce.png"), quality=95)
    print("Saved hinh_3_2_luong_mapreduce.png")

if __name__ == "__main__":
    create_architecture_diagram()
    create_pipeline_diagram()
    create_mapreduce_diagram()
    print("All diagrams generated successfully!")
