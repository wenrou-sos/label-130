@echo off
set PYTHONPATH=d:\proje\label-130\backend
cd /d d:\proje\label-130\backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause
