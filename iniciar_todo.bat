@echo off
title Sistema SST-IA - Lanzador Unificado
color 0b

echo ========================================================
echo         INICIANDO TODO EL ECOSISTEMA SST-IA
echo ========================================================
echo.

echo [1/3] Verificando y liberando puertos 5000 y 8085...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000') do taskkill /f /pid %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8085') do taskkill /f /pid %%a >nul 2>&1

echo.
echo [2/3] Iniciando Servidor Backend Python en http://localhost:5000...
start "SST-IA Backend (Python FastAPI)" cmd /k "cd /d C:\Users\Yairc\Documents\Universidad\IA\Modulo_SST_IA && python server.py"

timeout /t 3 /nobreak >nul

echo.
echo [3/3] Iniciando Aplicacion Web Flutter en http://localhost:8085...
start "SST-IA Frontend (Flutter Web)" cmd /k "cd /d C:\Users\Yairc\Documents\Universidad\IA\sst-ia && flutter run -d chrome --web-port 8085"

echo.
echo ========================================================
echo   Listo! Ambos servicios iniciados:
echo   - Backend: http://localhost:5000
echo   - Web App: http://localhost:8085
echo ========================================================
echo.
pause
