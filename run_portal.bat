@echo off
title SK Sutras - Review Portal (Hiranyam AI Labs)
cd /d "%~dp0"
echo =====================================================================
echo  SK Sutras - by Shri Shripad Kulkarni: Review Portal
echo  Powered by Hiranyam AI Labs (https://hiranyamai.com/)
echo =====================================================================
echo Starting Streamlit Review Portal in your default web browser...
echo.
call .venv\Scripts\python.exe -m streamlit run src\ui\app.py --server.port 8501
pause
