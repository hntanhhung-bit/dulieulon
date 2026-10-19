#!/bin/bash
# ==============================================================================
# BÀI TẬP LỚN: XỬ LÝ DỮ LIỆU LỚN (CTKU122) - TRƯỜNG ĐH TN&MT HÀ NỘI
# TỔNG HỢP CÂU LỆNH CHẠY TRÊN MÁY ẢO LINUX (UBUNTU / CENTOS) TỪ CÂU 1 ĐẾN CÂU 10
# Đề tài: Phân tích & Giám sát chất lượng mạng viễn thông (Hadoop, Spark, R)
# ==============================================================================

# Dừng lại nếu có lỗi nghiêm trọng (tùy chọn)
set -e

# Xác định thư mục gốc của dự án
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_title() {
    echo -e "\n${BLUE}================================================================================${NC}"
    echo -e "${YELLOW} $1 ${NC}"
    echo -e "${BLUE}================================================================================${NC}\n"
}

print_title "BẮT ĐẦU: KHỞI ĐỘNG CÁC DỊCH VỤ HADOOP & HBASE TRÊN CỤM LINUX"
echo -e "${GREEN}[*] Khởi động HDFS, YARN và HBase...${NC}"
start-dfs.sh || true
start-yarn.sh || true
start-hbase.sh || true

echo -e "\n${GREEN}[*] Kiểm tra các tiến trình Java bằng lệnh jps:${NC}"
jps

# ==============================================================================
# CÂU 1: ĐẶC TRƯNG 5V VÀ KHÁM PHÁ CÁC TẬP DỮ LIỆU VIỄN THÔNG
# ==============================================================================
print_title "CÂU 1: KHÁM PHÁ ĐẶC TRƯNG 5V VÀ KIỂM TRA DỮ LIỆU THỰC NGHIỆM"
echo -e "${GREEN}[*] Đếm số dòng và kiểm tra 5 dòng đầu của tệp sự kiện đo kiểm (network_kpi_events.csv):${NC}"
wc -l data/network_kpi_events.csv
head -n 5 data/network_kpi_events.csv

echo -e "\n${GREEN}[*] Kiểm tra bảng danh mục trạm BTS và danh mục Cell (Dữ liệu có cấu trúc):${NC}"
head -n 5 data/bts_towers.csv
head -n 5 data/cells_catalog.csv

echo -e "\n${GREEN}[*] Kiểm tra bảng khiếu nại khách hàng:${NC}"
head -n 5 data/customer_complaints.csv

# ==============================================================================
# CÂU 2: THU THẬP VÀ ĐỆM DỮ LIỆU VỚI APACHE FLUME (2 KỊCH BẢN)
# ==============================================================================
print_title "CÂU 2: CẤU HÌNH VÀ THỬ NGHIỆM APACHE FLUME (2 KỊCH BẢN)"
echo -e "${GREEN}[*] Kiểm tra cú pháp kịch bản 1: Nạp CSV theo lô (Spooling Directory + FileChannel):${NC}"
cat flume/flume_csv_to_hdfs.conf | head -n 25

echo -e "\n${GREEN}[*] Kiểm tra cú pháp kịch bản 2: Luồng sự kiện thời gian thực (Netcat Fan-out vào HDFS + HBase):${NC}"
cat flume/flume_events_to_hbase.conf | head -n 25

echo -e "\n${YELLOW}[HƯỚNG DẪN CHẠY FLUME THỰC TẾ]:${NC}"
echo "  Terminal 1 (Chạy Agent nạp lô CSV):"
echo "    flume-ng agent -n csvAgent -c flume/ -f flume/flume_csv_to_hdfs.conf -Dflume.root.logger=INFO,console"
echo "  Terminal 2 (Chạy Agent luồng socket 8888):"
echo "    flume-ng agent -n streamAgent -c flume/ -f flume/flume_events_to_hbase.conf -Dflume.root.logger=INFO,console"

# ==============================================================================
# CÂU 3: THIẾT KẾ 4 VÙNG HDFS, TÍNH TOÁN DUNG LƯỢNG & PHỤC HỒI CHỊU LỖI
# ==============================================================================
print_title "CÂU 3: THIẾT KẾ 4 VÙNG DATA LAKE TRÊN HDFS VÀ PHÂN VÙNG DỮ LIỆU"
echo -e "${GREEN}[*] Khởi tạo 4 vùng dữ liệu: /telecom/raw, /telecom/staging, /telecom/curated, /telecom/output${NC}"
hdfs dfs -mkdir -p /telecom/raw /telecom/staging /telecom/curated /telecom/output /telecom/input

echo -e "${GREEN}[*] Đẩy dữ liệu đo kiểm lên vùng /telecom/raw và /telecom/input:${NC}"
hdfs dfs -put -f data/*.csv /telecom/input/
hdfs dfs -put -f data/network_kpi_events.csv /telecom/raw/

echo -e "\n${GREEN}[*] Kiểm tra danh mục trên HDFS:${NC}"
hdfs dfs -ls /telecom

echo -e "\n${GREEN}[*] Kiểm tra hệ số nhân bản RF=3 và tình trạng Block dữ liệu (fsck):${NC}"
hdfs fsck /telecom/raw/network_kpi_events.csv -files -blocks -locations

# ==============================================================================
# CÂU 4: XỬ LÝ VÀ TỔNG HỢP DỮ LIỆU BẰNG APACHE PIG LATIN
# ==============================================================================
print_title "CÂU 4: THỰC THI KỊCH BẢN XỬ LÝ DỮ LIỆU APACHE PIG LATIN"
echo -e "${GREEN}[*] Xóa thư mục kết quả Pig cũ trên HDFS (nếu có):${NC}"
hdfs dfs -rm -r -f /telecom/output/pig_degraded_towers || true

echo -e "${GREEN}[*] Đang chạy kịch bản Pig Latin (chế độ MapReduce / YARN):${NC}"
# Chạy với Pig (fallback sang local nếu YARN bận)
if command -v pig &> /dev/null; then
    pig -x mapreduce pig/telecom_kpi_analysis.pig || pig -x local pig/telecom_kpi_analysis.pig
    echo -e "\n${GREEN}[*] Kết quả trạm suy giảm chất lượng từ Pig Latin:${NC}"
    hdfs dfs -cat /telecom/output/pig_degraded_towers/* | head -n 10 || true
else
    echo -e "${YELLOW}[!] Lệnh 'pig' chưa có trong PATH máy ảo. Kiểm tra mã nguồn Pig Latin tại: pig/telecom_kpi_analysis.pig${NC}"
fi

# ==============================================================================
# CÂU 5: THUẬT TOÁN HADOOP MAPREDUCE JAVA (COMPOSITE KEY & CUSTOM PARTITIONER)
# ==============================================================================
print_title "CÂU 5: BIÊN DỊCH VÀ CHẠY THUẬT TOÁN HADOOP MAPREDUCE JAVA"
mkdir -p /tmp/mr_classes
rm -rf /tmp/mr_classes/*

echo -e "${GREEN}[*] 1. Biên dịch mã nguồn Java (TelecomKpiAnalysis.java):${NC}"
javac -cp $(hadoop classpath) -d /tmp/mr_classes mapreduce/TelecomKpiAnalysis.java

echo -e "${GREEN}[*] 2. Đóng gói tệp JAR MapReduce:${NC}"
jar -cvf mapreduce/TelecomKpiAnalysis.jar -C /tmp/mr_classes/ .

echo -e "${GREEN}[*] 3. Xóa thư mục output cũ trên HDFS:${NC}"
hdfs dfs -rm -r -f /telecom/output/mapreduce_kpi || true

echo -e "${GREEN}[*] 4. Thực thi Job MapReduce trên cụm YARN:${NC}"
hadoop jar mapreduce/TelecomKpiAnalysis.jar \
    vn.edu.hunre.bigdata.telecom.TelecomKpiAnalysis \
    /telecom/input/network_kpi_events.csv \
    /telecom/output/mapreduce_kpi

echo -e "\n${GREEN}[*] 5. Kết quả tính toán KPI (Độ trễ, Mất gói, Rớt cuộc gọi) từ MapReduce:${NC}"
hdfs dfs -cat /telecom/output/mapreduce_kpi/part-r-00000 | head -n 15

# ==============================================================================
# CÂU 6: PIPELINE APACHE SPARK PHÁT HIỆN CELL QUÁ TẢI & XUẤT PARQUET
# ==============================================================================
print_title "CÂU 6: THỰC THI APACHE SPARK PIPELINE & SO SÁNH VỚI MAPREDUCE"
echo -e "${GREEN}[*] Đang submit ứng dụng PySpark lên Spark Engine:${NC}"
if command -v spark-submit &> /dev/null; then
    spark-submit --master local[*] spark/telecom_spark_pipeline.py
else
    python3 spark/telecom_spark_pipeline.py || python spark/telecom_spark_pipeline.py
fi

echo -e "\n${GREEN}[*] Kiểm tra các tệp Snappy Parquet đã được xuất bởi Spark:${NC}"
hdfs dfs -ls /telecom/curated/ || ls -la output/curated/ || true

# ==============================================================================
# CÂU 7: THIẾT KẾ CSDL NOSQL APACHE HBASE (ROWKEY & COMMANDS)
# ==============================================================================
print_title "CÂU 7: KHỞI TẠO BẢNG HBASE, THAO TÁC PUT/GET/SCAN VÀ ROWKEY"
echo -e "${GREEN}[*] Thực thi kịch bản cấu hình và thao tác trên HBase Shell:${NC}"
if command -v hbase &> /dev/null; then
    hbase shell hbase/hbase_schema_and_commands.sh
else
    echo -e "${YELLOW}[!] HBase daemon chưa bật hoặc lệnh 'hbase' chưa có trong PATH.${NC}"
    echo "Xem kịch bản lệnh đầy đủ tại: hbase/hbase_schema_and_commands.sh"
fi

# ==============================================================================
# CÂU 8: MÔ PHỎNG QUY TRÌNH PHÂN TÍCH BIGSHEETS BẰNG SPARK DATAFRAME
# ==============================================================================
print_title "CÂU 8: MÔ PHỎNG QUY TRÌNH BIGSHEETS 6 BƯỚC & XUẤT DASHBOARD"
echo -e "${GREEN}[*] Thực thi script mô phỏng 6 bước của BigSheets:${NC}"
python3 spark/bigsheets_spark_simulation.py || python spark/bigsheets_spark_simulation.py

echo -e "\n${GREEN}[*] Kiểm tra các sản phẩm đầu ra của BigSheets:${NC}"
ls -lh report/chart_bigsheets_*.png
ls -lh report/telecom_kpi_summary_powerbi.csv
ls -lh report/bigsheets_dashboard.html

# ==============================================================================
# CÂU 9: PHÂN TÍCH R & CSDL SQLITE (HỌC MÁY HỒI QUY LOGISTIC)
# ==============================================================================
print_title "CÂU 9: PHÂN TÍCH CHUYÊN SÂU BẰNG NGÔN NGỮ R & SQLITE"
if command -v Rscript &> /dev/null; then
    echo -e "${GREEN}[*] Đang chạy phân tích R (telecom_analysis.R):${NC}"
    Rscript r_analysis/telecom_analysis.R
    echo -e "\n${GREEN}[*] Kiểm tra bảng kpi_analysis_summary đã được ghi vào SQLite:${NC}"
    python3 view_kpi_summary.py || python view_kpi_summary.py
else
    echo -e "${YELLOW}[!] Chưa có Rscript. Kiểm tra kết quả đã sinh sẵn tại: report/chart1_latency_by_tech.png${NC}"
    python3 view_kpi_summary.py || python view_kpi_summary.py
fi

# ==============================================================================
# CÂU 10: TỔNG HỢP BÁO CÁO KỸ THUẬT VÀ MA TRẬN 5 KHUYẾN NGHỊ NOC
# ==============================================================================
print_title "CÂU 10: KIỂM TRA BÁO CÁO KỸ THUẬT HOÀN CHỈNH VÀ SLIDE"
echo -e "${GREEN}[*] Danh mục tài liệu báo cáo và slide đã hoàn thiện:${NC}"
ls -lh BaoCao*.pdf Slide*.pdf BaoCao*.docx Slide*.pptx || true

echo -e "\n${GREEN}================================================================================${NC}"
echo -e "${GREEN}  CHÚC MỪNG: BẠN ĐÃ THỰC THI THÀNH CÔNG TOÀN BỘ 10 CÂU BÀI TẬP LỚN BIG DATA!    ${NC}"
echo -e "${GREEN}================================================================================${NC}\n"
