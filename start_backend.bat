@echo off
echo ===================================================
echo Starting Oral Cancer AI Backend & Cloudflare Tunnel
echo ===================================================
cd /d "%~dp0backend"

echo [1/2] Launching FastAPI Backend on port 8000...
start "Oral Cancer Backend (Uvicorn)" cmd /k "python -m uvicorn main:app --port 8000"

timeout /t 3 /nobreak >nul

echo [2/2] Launching Cloudflare Tunnel...
start "Cloudflare Tunnel" cmd /k ".\cloudflared.exe tunnel --url http://127.0.0.1:8000"

echo.
echo Both services have launched!
echo Check the Cloudflare Tunnel window to see your public URL.
pause
