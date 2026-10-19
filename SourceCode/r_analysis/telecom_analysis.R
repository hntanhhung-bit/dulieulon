# ==============================================================================
# CHƯƠNG TRÌNH PHÂN TÍCH CHẤT LƯỢNG MẠNG VIỄN THÔNG BẰNG NGÔN NGỮ R
# ==============================================================================
# Yêu cầu đáp ứng:
# 1. Kết nối CSDL SQLite đi kèm bằng DBI / RSQLite
# 2. Truy vấn SQL có JOIN và GROUP BY
# 3. Đọc dữ liệu vào R, tiền xử lý và biến đổi bằng dplyr / tidyr
# 4. Trực quan hóa dữ liệu mạng chuyên sâu bằng ggplot2
# 5. Xây dựng mô hình Học máy: Phân loại nguy cơ khiếu nại (Logistic Regression)
# 6. Ghi bảng kết quả tổng hợp trở lại CSDL SQLite
# 7. Đóng kết nối an toàn bằng khối tryCatch và on.exit
# ==============================================================================

# ------------------------------------------------------------------------------
# 0. THIẾT LẬP THƯ MỤC THƯ VIỆN CÁ NHÂN (TRÁNH LỖI PHÂN QUYỀN PROGRAM FILES)
# ------------------------------------------------------------------------------
user_lib <- Sys.getenv("R_LIBS_USER")
if (user_lib == "" || is.na(user_lib)) {
  user_lib <- file.path(Sys.getenv("LOCALAPPDATA"), "R", "win-library", paste(R.version$major, substr(R.version$minor, 1, 1), sep = "."))
}
dir.create(user_lib, recursive = TRUE, showWarnings = FALSE)
.libPaths(unique(c(user_lib, .libPaths())))

# Khởi tạo kiểm tra và nạp các gói thư viện cần thiết
required_packages <- c("DBI", "RSQLite", "dplyr", "tidyr", "ggplot2")
for (pkg in required_packages) {
  if (!require(pkg, character.only = TRUE, quietly = TRUE, lib.loc = .libPaths())) {
    cat(sprintf(">>> Đang tự động tải và cài đặt gói: %s (vui lòng chờ trong giây lát)...\n", pkg))
    install.packages(pkg, repos = "https://cloud.r-project.org", lib = user_lib, quiet = TRUE)
    library(pkg, character.only = TRUE, lib.loc = .libPaths())
  }
}

# ------------------------------------------------------------------------------
# 1. ĐỊNH NGHĨA HÀM THỰC THI CHÍNH KÈM CƠ CHẾ ĐÓNG KẾT NỐI AN TOÀN
# ------------------------------------------------------------------------------
run_telecom_analysis <- function(db_path = NULL, output_chart_dir = NULL) {
  
  # Tự động dò tìm đường dẫn CSDL phù hợp trên cả Windows và Ubuntu Linux
  if (is.null(db_path)) {
    candidates_db <- c(
      "c:/dulieulon/data/telecom_network.sqlite",
      "../data/telecom_network.sqlite",
      "./data/telecom_network.sqlite",
      "data/telecom_network.sqlite",
      "telecom_network.sqlite",
      file.path(Sys.getenv("HOME"), "dulieulon/data/telecom_network.sqlite"),
      "/home/hadoop/dulieulon/data/telecom_network.sqlite"
    )
    for (cand in candidates_db) {
      if (file.exists(cand)) {
        db_path <- cand
        break
      }
    }
    if (is.null(db_path)) {
      db_path <- "c:/dulieulon/data/telecom_network.sqlite"
    }
  }

  # Tự động dò tìm thư mục xuất báo cáo đồ thị
  if (is.null(output_chart_dir)) {
    candidates_report <- c(
      "c:/dulieulon/report",
      "../report",
      "./report",
      "report",
      file.path(Sys.getenv("HOME"), "dulieulon/report"),
      "/home/hadoop/dulieulon/report"
    )
    for (cand in candidates_report) {
      if (dir.exists(cand)) {
        output_chart_dir <- cand
        break
      }
    }
    if (is.null(output_chart_dir)) {
      output_chart_dir <- if (dir.exists("c:/dulieulon/report")) "c:/dulieulon/report" else "./report"
    }
  }
  
  cat("====================================================================\n")
  cat(">>> [BƯỚC 1] KẾT NỐI VÀO CƠ SỞ DỮ LIỆU SQLITE: ", db_path, "\n")
  cat(">>> [THƯ MỤC XUẤT ĐỒ THỊ]: ", output_chart_dir, "\n")
  cat("====================================================================\n")
  
  if (!file.exists(db_path)) {
    stop(paste("Khong tim thay file CSDL tai:", db_path, 
               "\nVui long dat file telecom_network.sqlite vao thu muc 'data' hoac truyen tham so db_path."))
  }
  
  # Kết nối SQLite
  con <- dbConnect(RSQLite::SQLite(), dbname = db_path)
  
  # Đảm bảo ngắt kết nối an toàn dù hàm kết thúc bình thường hay gặp lỗi bất ngờ
  on.exit({
    if (dbIsValid(con)) {
      dbDisconnect(con)
      cat(">>> [AN TOÀN] Đã ngắt kết nối CSDL SQLite thành công.\n")
    }
  }, add = TRUE)

  # ----------------------------------------------------------------------------
  # 2. VIẾT TRUY VẤN SQL CÓ JOIN VÀ GROUP BY
  # ----------------------------------------------------------------------------
  cat("\n>>> [BƯỚC 2] THỰC THI TRUY VẤN SQL CÓ JOIN VÀ GROUP BY...\n")
  
  sql_query <- "
    SELECT 
      e.tower_id,
      t.tower_name,
      t.province,
      t.district,
      e.technology,
      COUNT(e.event_id) AS total_sessions,
      ROUND(AVG(e.throughput_mbps), 2) AS avg_throughput_mbps,
      ROUND(AVG(e.latency_ms), 2) AS avg_latency_ms,
      ROUND(MAX(e.latency_ms), 2) AS max_latency_ms,
      ROUND(AVG(e.packet_loss_pct), 2) AS avg_packet_loss_pct,
      SUM(e.call_dropped) AS total_dropped_calls,
      ROUND(AVG(e.num_active_users), 1) AS avg_active_users,
      COUNT(DISTINCT c.complaint_id) AS total_complaints
    FROM network_kpi_events e
    INNER JOIN bts_towers t ON e.tower_id = t.tower_id
    INNER JOIN cells_catalog cl ON e.cell_id = cl.cell_id
    LEFT JOIN customer_complaints c ON e.tower_id = c.tower_id AND e.cell_id = c.cell_id
    WHERE e.latency_ms >= 0.0 AND e.throughput_mbps >= 0.0
    GROUP BY e.tower_id, t.tower_name, t.province, t.district, e.technology
    ORDER BY avg_latency_ms DESC
  "
  
  # Đọc dữ liệu vào R Data Frame
  df_kpi_raw <- dbGetQuery(con, sql_query)
  cat(sprintf(">>> Đã đọc thành công %d bản ghi tổng hợp từ CSDL.\n", nrow(df_kpi_raw)))
  print(head(df_kpi_raw, 5))

  # ----------------------------------------------------------------------------
  # 3. TIỀN XỬ LÝ VÀ BIẾN ĐỔI DỮ LIỆU BẰNG DPLYR / TIDYR
  # ----------------------------------------------------------------------------
  cat("\n>>> [BƯỚC 3] BIẾN ĐỔI VÀ TÍNH TOÁN CHỈ SỐ BẰNG DPLYR & TIDYR...\n")
  
  df_processed <- df_kpi_raw %>%
    # Tính tỷ lệ rớt cuộc gọi (%)
    mutate(
      call_drop_rate_pct = round((total_dropped_calls / total_sessions) * 100, 3),
      # Tạo biến phân loại: Có khiếu nại hay không (1: Có, 0: Không)
      has_complaint = if_else(total_complaints > 0, 1, 0),
      # Phân loại trạng thái sức khỏe trạm BTS
      health_category = case_when(
        call_drop_rate_pct > 2.0 | avg_latency_ms > 80.0 ~ "Nguy cấp (Critical)",
        avg_latency_ms > 45.0 | call_drop_rate_pct > 1.0 ~ "Cảnh báo (Warning)",
        TRUE ~ "Bình thường (Healthy)"
      )
    ) %>%
    # Sắp xếp theo tỷ lệ rớt cuộc gọi giảm dần
    arrange(desc(call_drop_rate_pct), desc(avg_latency_ms))

  print(head(df_processed %>% select(tower_id, technology, province, avg_latency_ms, call_drop_rate_pct, health_category), 5))

  # ----------------------------------------------------------------------------
  # 4. TRỰC QUAN HÓA CHẤT LƯỢNG MẠNG CHUYÊN SÂU BẰNG GGPLOT2
  # ----------------------------------------------------------------------------
  cat("\n>>> [BƯỚC 4] XÂY DỰNG BIỂU ĐỒ TRỰC QUAN BẰNG GGPLOT2...\n")
  dir.create(output_chart_dir, showWarnings = FALSE, recursive = TRUE)

  # Biểu đồ 1: Phân bố Độ trễ (Latency) theo Công nghệ (3G, 4G, 5G)
  p1 <- ggplot(df_processed, aes(x = technology, y = avg_latency_ms, fill = technology)) +
    geom_boxplot(alpha = 0.7, outlier.color = "red") +
    geom_jitter(width = 0.15, alpha = 0.5, color = "#2c3e50") +
    labs(
      title = "Phân Bố Độ Trễ Trung Bình (ms) Theo Công Nghệ",
      subtitle = "Đánh giá chất lượng mạng giữa 3G, 4G và 5G trên toàn quốc",
      x = "Công Nghệ Mạng",
      y = "Độ Trễ Trung Bình (ms)",
      caption = "Nguồn: Hệ thống đo kiểm viễn thông Big Data"
    ) +
    theme_minimal() +
    theme(plot.title = element_text(face = "bold", size = 14))

  ggsave(file.path(output_chart_dir, "chart1_latency_by_tech.png"), plot = p1, width = 8, height = 5)
  cat(">>> [Đồ thị 1] Đã lưu chart1_latency_by_tech.png\n")

  # Biểu đồ 2: Tương quan giữa Tỷ lệ mất gói và Tỷ lệ rớt cuộc gọi
  p2 <- ggplot(df_processed, aes(x = avg_packet_loss_pct, y = call_drop_rate_pct, color = health_category)) +
    geom_point(aes(size = avg_active_users), alpha = 0.8) +
    geom_smooth(method = "lm", se = FALSE, color = "black", linetype = "dashed") +
    scale_color_manual(values = c("Bình thường (Healthy)" = "#27ae60", 
                                  "Cảnh báo (Warning)" = "#f39c12", 
                                  "Nguy cấp (Critical)" = "#c0392b")) +
    labs(
      title = "Tương Quan Giữa Tỷ Lệ Mất Gói và Tỷ Lệ Rớt Cuộc Gọi",
      subtitle = "Kích thước điểm biểu diễn số lượng người dùng đồng thời (Active Users)",
      x = "Tỷ Lệ Mất Gói Trung Bình (%)",
      y = "Tỷ Lệ Rớt Cuộc Gọi (%)",
      color = "Trạng Thái Trạm",
      size = "Số Người Dùng"
    ) +
    theme_minimal() +
    theme(plot.title = element_text(face = "bold", size = 14))

  ggsave(file.path(output_chart_dir, "chart2_packet_loss_vs_drop_rate.png"), plot = p2, width = 9, height = 5)
  cat(">>> [Đồ thị 2] Đã lưu chart2_packet_loss_vs_drop_rate.png\n")

  # ----------------------------------------------------------------------------
  # 5. MÔ HÌNH HỌC MÁY: PHÂN LOẠI NGUY CƠ KHIẾU NẠI (LOGISTIC REGRESSION)
  # ----------------------------------------------------------------------------
  cat("\n>>> [BƯỚC 5] XÂY DỰNG MÔ HÌNH DỰ ĐOÁN NGUY CƠ KHIẾU NẠI (LOGISTIC REGRESSION)...\n")
  
  # Huấn luyện mô hình hồi quy Logistic:
  # has_complaint ~ avg_latency_ms + avg_packet_loss_pct + avg_throughput_mbps + avg_active_users
  model_complaint <- glm(
    has_complaint ~ avg_latency_ms + avg_packet_loss_pct + avg_throughput_mbps + avg_active_users,
    data = df_processed,
    family = binomial(link = "logit")
  )
  
  print(summary(model_complaint))

  # Dự báo xác suất khiếu nại cho từng trạm BTS
  df_processed$predicted_complaint_prob <- round(predict(model_complaint, type = "response"), 4)
  df_processed$predicted_complaint_risk <- if_else(df_processed$predicted_complaint_prob > 0.5, "CAO (HIGH)", "THẤP (LOW)")

  cat("\n>>> BẢNG XẾP HẠNG TOP 5 TRẠM CÓ NGUY CƠ PHÁT SINH KHIẾU NẠI CAO NHẤT:\n")
  top_risk_towers <- df_processed %>%
    arrange(desc(predicted_complaint_prob)) %>%
    select(tower_id, province, technology, avg_latency_ms, call_drop_rate_pct, predicted_complaint_prob, predicted_complaint_risk)
  print(head(top_risk_towers, 5))

  # ----------------------------------------------------------------------------
  # 6. GHI BẢNG KẾT QUẢ TRỞ LẠI CƠ SỞ DỮ LIỆU SQLITE
  # ----------------------------------------------------------------------------
  cat("\n>>> [BƯỚC 6] GHI BẢNG KẾT QUẢ PHÂN TÍCH VÀO CSDL SQLITE...\n")
  result_table_name <- "kpi_analysis_summary"
  
  # Ghi đè bảng kết quả vào SQLite
  dbWriteTable(con, name = result_table_name, value = df_processed, overwrite = TRUE, row.names = FALSE)
  cat(sprintf(">>> Ghi thành công %d bản ghi vào bảng '%s' trong CSDL!\n", nrow(df_processed), result_table_name))

  # Kiểm tra lại số lượng bản ghi trong bảng vừa tạo
  verify_count <- dbGetQuery(con, paste0("SELECT COUNT(*) AS count FROM ", result_table_name))
  cat(sprintf(">>> Xác minh thành công: Bảng '%s' hiện có %d bản ghi.\n", result_table_name, verify_count$count[1]))

  cat("\n====================================================================\n")
  cat(">>> TOÀN BỘ TIẾN TRÌNH PHÂN TÍCH R VỚI SQLITE ĐÃ HOÀN TẤT THÀNH CÔNG!\n")
  cat("====================================================================\n")
}

# Chạy kịch bản
tryCatch({
  run_telecom_analysis()
}, error = function(e) {
  cat(">>> [LỖI TRONG TIẾN TRÌNH R]: ", e$message, "\n")
})
