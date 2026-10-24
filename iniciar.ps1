# ========================================================
# Script de Inicio Todo-en-Uno: Sistema SST-IA
# ========================================================

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "         INICIANDO TODO EL ECOSISTEMA SST-IA            " -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

# Detectar rutas relativas al script para que funcione en la maquina de cualquier companero
$baseDir = $PSScriptRoot

$moduloDir = Join-Path $baseDir "Modulo_SST_IA"
if (-not (Test-Path $moduloDir)) {
    $moduloDir = Join-Path (Split-Path $baseDir -Parent) "Modulo_SST_IA"
}

$flutterDir = $baseDir
if (-not (Test-Path (Join-Path $flutterDir "pubspec.yaml"))) {
    $flutterDir = Join-Path $baseDir "sst-ia"
}

# 1. Liberar puertos 5000 o 8085 si quedaron procesos anteriores colgados
Write-Host "[1/3] Verificando puertos..." -ForegroundColor Yellow
$puertos = @(5000, 8085)
foreach ($p in $puertos) {
    $proc = Get-NetTCPConnection -LocalPort $p -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
    if ($proc) {
        Write-Host " -> Liberando puerto $p (PID $proc)..." -ForegroundColor DarkGray
        Stop-Process -Id $proc -Force -ErrorAction SilentlyContinue
    }
}

# 2. Iniciar Backend Python (FastAPI + YOLOv8 + ReportLab)
Write-Host "[2/3] Levantando Servidor Backend Python en http://localhost:5000..." -ForegroundColor Green
$cmdBackend = "cd '$moduloDir'; python server.py"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $cmdBackend

Start-Sleep -Seconds 3

# 3. Iniciar Frontend Flutter Web
Write-Host "[3/3] Levantando Aplicacion Flutter Web en http://localhost:8085..." -ForegroundColor Green
$cmdFrontend = "cd '$flutterDir'; flutter run -d chrome --web-port 8085"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $cmdFrontend

Write-Host ""
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  LISTO! Se abrieron las ventanas para ambos servicios: " -ForegroundColor Green
Write-Host "  - Backend API:  http://localhost:5000" -ForegroundColor White
Write-Host "  - Swagger Docs: http://localhost:5000/docs" -ForegroundColor White
Write-Host "  - Flutter Web:  http://localhost:8085" -ForegroundColor White
Write-Host "========================================================" -ForegroundColor Cyan
