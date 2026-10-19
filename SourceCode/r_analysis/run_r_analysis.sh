#!/bin/bash
# ==============================================================================
# KỊCH BẢN CHẠY PHÂN TÍCH R & SQLITE TRÊN UBUNTU LINUX (CÂU 9)
# ==============================================================================

set -e

# Chuyển về thư mục chứa script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=============================================================================="
echo "  KHỞI CHẠY PHÂN TÍCH CHẤT LƯỢNG MẠNG BẰNG R & SQLITE TRÊN UBUNTU"
echo "  Thư mục làm việc: $SCRIPT_DIR"
echo "=============================================================================="

# 1. Kiểm tra xem Rscript đã được cài đặt chưa
if ! command -v Rscript &> /dev/null; then
    echo "[!] CẢNH BÁO: Hệ thống Ubuntu chưa cài đặt R (Rscript)."
    echo "[*] Vui lòng chạy các lệnh sau để cài đặt R và thư viện SQLite trên Ubuntu:"
    echo "    sudo apt update"
    echo "    sudo apt install -y r-base r-base-dev libsqlite3-dev"
    echo ""
    exit 1
fi

echo "[*] Đã tìm thấy Rscript: $(which Rscript)"
Rscript --version

# 2. Tạo thư mục report nếu chưa có
mkdir -p "$SCRIPT_DIR/../report"

# 3. Thực thi kịch bản R
echo ""
echo "[*] Đang thực thi: Rscript telecom_analysis.R ..."
echo "------------------------------------------------------------------------------"
Rscript telecom_analysis.R
echo "------------------------------------------------------------------------------"

echo ""
echo "=============================================================================="
echo "[+] HOÀN TẤT THỰC THI PHÂN TÍCH R TRÊN UBUNTU!"
echo "[*] Kết quả biểu đồ được lưu tại:"
echo "    - $SCRIPT_DIR/../report/chart1_latency_by_tech.png"
echo "    - $SCRIPT_DIR/../report/chart2_packet_loss_vs_drop_rate.png"
echo "[*] Bảng tổng hợp 'kpi_analysis_summary' đã được ghi vào tệp SQLite."
echo "=============================================================================="
