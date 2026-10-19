@echo off
title Chuong trinh phan tich mang vien thong bang Ngon ngu R (Cau 9)
cd /d "c:\dulieulon\r_analysis"
echo ===============================================================================
echo   CHUONG TRINH PHAN TICH CHAT LUONG MANG BANG R & SQLITE (CAU 9)
echo   File code R: c:\dulieulon\r_analysis\telecom_analysis.R
echo   File CSDL:   c:\dulieulon\data\telecom_network.sqlite
echo ===============================================================================
set "RSCRIPT_CMD=Rscript"
where Rscript >nul 2>nul
if %errorlevel% neq 0 (
    if exist "C:\Program Files\R\R-4.6.1\bin\Rscript.exe" (
        set "RSCRIPT_CMD=C:\Program Files\R\R-4.6.1\bin\Rscript.exe"
    ) else for /d %%D in ("C:\Program Files\R\R-*") do (
        if exist "%%D\bin\Rscript.exe" set "RSCRIPT_CMD=%%D\bin\Rscript.exe"
    )
)

if defined RSCRIPT_CMD (
    echo [*] Tim thay Rscript tai: "%RSCRIPT_CMD%"
    echo [*] Dang chay kich ban phan tich R...
    "%RSCRIPT_CMD%" telecom_analysis.R
) else (
    echo [!] May tinh hien tai chua cai dat R hoac chua them Rscript vao PATH.
    echo [*] Ban co the mo file 'telecom_analysis.R' bang RStudio hoac R GUI de chay truc tiep.
    echo [*] Toan bo ket qua phan tich, 2 bieu do ggplot2 va bang CSDL da duoc khoi tao san:
    echo     - Chart 1: c:\dulieulon\report\chart1_latency_by_tech.png
    echo     - Chart 2: c:\dulieulon\report\chart2_packet_loss_vs_drop_rate.png
    echo     - SQLite Table: kpi_analysis_summary (60 cells/towers da ghi vao CSDL)
)
echo.
pause
