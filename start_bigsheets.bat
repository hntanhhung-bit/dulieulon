@echo off
title Mo Phong BigSheets bang Spark DataFrame, Spark SQL ^& Power BI
cd /d "c:\dulieulon"
echo ===============================================================================
echo   CHUONG TRINH MO PHONG BIGSHEETS BANG SPARK DATAFRAME ^& SPARK SQL
echo   Mapping: Collection -^> DataFrame ^| Filter -^> filter ^| Calc Col -^> withColumn
echo            Join -^> join ^| Group -^> groupBy ^| Sort -^> orderBy
echo ===============================================================================
set PYTHONIOENCODING=utf-8
"C:\Users\DELL\AppData\Local\Programs\OSGeo4W\apps\Python312\python.exe" "c:\dulieulon\spark\bigsheets_spark_simulation.py"
echo.
echo ===============================================================================
echo   Ket qua truc quan hoa da duoc luu tai: c:\dulieulon\report\
echo   - chart_bigsheets_drop_rate_by_province_tech.png
echo   - chart_bigsheets_latency_vs_loss_bubble.png
echo   - chart_bigsheets_top10_worst_towers.png
echo   - telecom_kpi_summary_powerbi.csv (San sang nhap vao Power BI)
echo   - bigsheets_dashboard.html (Dashboard giao dien Web truc quan)
echo ===============================================================================
echo [*] Dang mo Giao dien Web Dashboard tren trinh duyet...
start "" "c:\dulieulon\report\bigsheets_dashboard.html"
echo.
pause
