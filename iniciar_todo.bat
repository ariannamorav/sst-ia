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
if exist "%~dp0Modulo_SST_IA" (
    start "SST-IA Backend (Python FastAPI)" cmd /k "cd /d "%~dp0Modulo_SST_IA" && python server.py"
) else (
    start "SST-IA Backend (Python FastAPI)" cmd /k "cd /d "%~dp0..\Modulo_SST_IA" && python server.py"
)

timeout /t 3 /nobreak >nul

if exist "C:\src\flutter\bin" set "PATH=C:\src\flutter\bin;%PATH%"

echo.
echo [3/3] Iniciando Aplicacion Web Flutter en http://localhost:8085...
if exist "%~dp0pubspec.yaml" (
    start "SST-IA Frontend (Flutter Web)" cmd /k "if exist C:\src\flutter\bin set PATH=C:\src\flutter\bin;%%PATH%% && cd /d "%~dp0" && flutter run -d chrome --web-port 8085"
) else (
    start "SST-IA Frontend (Flutter Web)" cmd /k "if exist C:\src\flutter\bin set PATH=C:\src\flutter\bin;%%PATH%% && cd /d "%~dp0sst-ia" && flutter run -d chrome --web-port 8085"
)

echo.
echo ========================================================
echo   Listo! Ambos servicios iniciados:
echo   - Backend: http://localhost:5000
echo   - Web App: http://localhost:8085
echo ========================================================
echo.
pause
