@echo off
title MEDI AI Smart Hospital
py -m pip install -r requirements.txt
if errorlevel 1 (
  echo Installation failed. Check that Python is installed.
  pause
  exit /b 1
)
py -m streamlit run app.py
pause
