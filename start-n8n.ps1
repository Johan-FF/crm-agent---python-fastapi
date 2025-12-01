# ============================================
# Script para iniciar N8N con Docker
# ============================================
# Este script inicia N8N con todas las variables necesarias
# Uso: .\start-n8n.ps1

Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   Iniciando N8N con OpenRouter        ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Verificar si Docker está instalado
Write-Host "1. Verificando Docker..." -ForegroundColor Yellow
$docker = docker --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker no está instalado o no está en PATH" -ForegroundColor Red
    Write-Host "   Instala Docker Desktop desde: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}
Write-Host "✓ Docker encontrado: $docker" -ForegroundColor Green
Write-Host ""

# Verificar si N8N está ejecutándose
Write-Host "2. Verificando puerto 5678..." -ForegroundColor Yellow
$testPort = Test-NetConnection -ComputerName localhost -Port 5678 -WarningAction SilentlyContinue
if ($testPort.TcpTestSucceeded) {
    Write-Host "⚠ N8N ya está ejecutándose en puerto 5678" -ForegroundColor Yellow
    Write-Host "  Accede a: http://localhost:5678" -ForegroundColor Cyan
    exit 0
}
Write-Host "✓ Puerto 5678 disponible" -ForegroundColor Green
Write-Host ""

# Verificar API Key de OpenRouter
Write-Host "3. Verificando API Key de OpenRouter..." -ForegroundColor Yellow
$apiKey = $env:OPEN_ROUTER_API_KEY
if ([string]::IsNullOrEmpty($apiKey)) {
    Write-Host "⚠ OPEN_ROUTER_API_KEY no está configurada" -ForegroundColor Yellow
    Write-Host "  Pasos para configurarla:" -ForegroundColor Cyan
    Write-Host "  1. Registrate en https://openrouter.ai" -ForegroundColor Cyan
    Write-Host "  2. Ve a https://openrouter.ai/keys" -ForegroundColor Cyan
    Write-Host "  3. Copia tu API Key" -ForegroundColor Cyan
    Write-Host "  4. Ejecuta: `$env:OPEN_ROUTER_API_KEY='tu_api_key'" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Escribe tu API Key ahora (o presiona Enter para saltarlo):" -ForegroundColor Yellow
    $userInput = Read-Host
    if (-not [string]::IsNullOrEmpty($userInput)) {
        $env:OPEN_ROUTER_API_KEY = $userInput
        Write-Host "✓ API Key configurada" -ForegroundColor Green
    } else {
        Write-Host "⚠ Continuando sin API Key (algunas funciones no funcionarán)" -ForegroundColor Yellow
    }
} else {
    Write-Host "✓ OPEN_ROUTER_API_KEY configurada" -ForegroundColor Green
}
Write-Host ""

# Iniciar N8N
Write-Host "4. Iniciando N8N..." -ForegroundColor Yellow
Write-Host ""

# Crear volumen de datos si no existe
docker volume create n8n_data 2>$null

# Iniciar contenedor con variables
$env:OPEN_ROUTER_MODEL = $env:OPEN_ROUTER_MODEL -or "openai/gpt-3.5-turbo"

docker run -it --rm `
    -p 5678:5678 `
    -e OPEN_ROUTER_API_KEY="$($env:OPEN_ROUTER_API_KEY)" `
    -e OPEN_ROUTER_MODEL="$($env:OPEN_ROUTER_MODEL)" `
    -v n8n_data:/home/node/.n8n `
    n8n

Write-Host ""
Write-Host "═════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "N8N fue detenido" -ForegroundColor Yellow
Write-Host "═════════════════════════════════════════" -ForegroundColor Cyan
