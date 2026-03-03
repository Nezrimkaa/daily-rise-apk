Set objShell = CreateObject("WScript.Shell")
objShell.Run "cmd /c venv\Scripts\activate.bat & start http://localhost:8000 & python -m uvicorn app.main:app --host 127.0.0.1 --port 8000", 0, False
