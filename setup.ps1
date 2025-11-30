# Setup Script para CRM Agent (PowerShell)
# Uso: .\setup.ps1

Write-Host "================================" -ForegroundColor Cyan
Write-Host " CRM Agent - Setup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Función para imprimir con color
function Write-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

# Verificar Python
Write-Host "Checking Python..."
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error "Python no está instalado"
    exit 1
}
Write-Success "Python encontrado: $pythonVersion"

# Verificar pip
Write-Host ""
Write-Host "Checking pip..."
$pipVersion = pip --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error "pip no está instalado"
    exit 1
}
Write-Success "pip encontrado"

# Crear .env si no existe
Write-Host ""
Write-Host "Setting up environment variables..."
if (-not (Test-Path "backend\.env")) {
    Copy-Item "backend\.env.example" "backend\.env"
    Write-Warning "Archivo .env creado. Por favor edita con tu PIPEDRIVE_API_KEY"
    Write-Warning "Ejecuta: notepad backend\.env"
} else {
    Write-Success "Archivo .env ya existe"
}

# Instalar dependencias
Write-Host ""
Write-Host "Installing Python dependencies..."
Set-Location backend
python -m pip install -q -r requirements.txt
Set-Location ..
Write-Success "Dependencias instaladas"

# Validar setup
Write-Host ""
Write-Host "Validating setup..."
python validate_setup.py

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "✓ Setup completado" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Próximos pasos:" -ForegroundColor Yellow
Write-Host "1. Editar backend\.env con tu PIPEDRIVE_API_KEY"
Write-Host "2. Ejecutar: python backend\main.py"
Write-Host "3. En otra terminal: n8n start"
Write-Host "4. Importar flujo en http://localhost:5678"
Write-Host ""
