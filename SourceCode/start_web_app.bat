@echo off
title He Thong IBM BigSheets Vien Thong - Web App
cd /d "c:\dulieulon\bigsheets\web_app"
echo ===============================================================================
echo   KHOI DONG HE THONG IBM BIGSHEETS VIEN THONG (WEB APP)
echo   Cong ket noi: http://localhost:8080/bigsheets
echo ===============================================================================
echo [*] Dang mo giao dien Web App tren trinh duyet...
start "" "http://localhost:8080/bigsheets"
echo [*] Dang khoi dong Node.js Server...
node server.js
pause
