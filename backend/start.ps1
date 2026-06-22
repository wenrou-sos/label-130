$env:PYTHONPATH = "d:\proje\label-130\backend"
Set-Location "d:\proje\label-130\backend"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
