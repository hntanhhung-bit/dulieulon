@echo off
title Xem Bang Du Lieu kpi_analysis_summary
cd /d "c:\dulieulon"
echo ===============================================================================
echo   XEM BANG DU LIEU KPI TONG HOP: kpi_analysis_summary (CAU 9)
echo   Nguon CSDL: c:\dulieulon\data\telecom_network.sqlite
echo ===============================================================================
echo.
echo [*] Dang xuat va mo file truc quan kpi_analysis_summary.html tren trinh duyet...
start "" "c:\dulieulon\report\kpi_analysis_summary.html"

echo [*] Dang hien thi du lieu truc tiep tren Command Prompt:
echo.
"c:\dulieulon\.venv\Scripts\python.exe" "c:\dulieulon\view_kpi_summary.py"
echo.
echo ===============================================================================
echo   Ban cung co the mo file CSV nay bang Microsoft Excel:
echo   c:\dulieulon\data\kpi_analysis_summary.csv
echo ===============================================================================
pause
