@echo off
title MediVision AI

cd /d "C:\MediVision_Backup\MediVision_AI"

echo Starting MediVision AI...
echo Please wait...

if not exist ".venv\Scripts\python.exe" (
    echo Python environment not found!
    pause
    exit /b
)

start "" cmd /c "timeout /t 5 /nobreak >nul && start http://localhost:8501"

".venv\Scripts\python.exe" -m streamlit run app.py --server.port 8501 --server.headless true

pause