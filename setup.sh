#!/bin/bash
# Setup Script para CRM Agent
# Uso: ./setup.sh

set -e

echo "================================"
echo " CRM Agent - Setup"
echo "================================"
echo ""

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Función para imprimir con color
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Verificar Python
echo "Checking Python..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 no está instalado"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
print_success "Python $PYTHON_VERSION encontrado"

# Verificar pip
echo ""
echo "Checking pip..."
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 no está instalado"
    exit 1
fi
print_success "pip3 encontrado"

# Crear .env si no existe
echo ""
echo "Setting up environment variables..."
if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    print_warning "Archivo .env creado. Por favor edita con tu PIPEDRIVE_API_KEY"
    print_warning "Ejecuta: nano backend/.env"
else
    print_success "Archivo .env ya existe"
fi

# Instalar dependencias
echo ""
echo "Installing Python dependencies..."
cd backend
pip3 install -q -r requirements.txt
cd ..
print_success "Dependencias instaladas"

# Validar setup
echo ""
echo "Validating setup..."
python3 validate_setup.py

echo ""
echo "================================"
echo "✓ Setup completado"
echo "================================"
echo ""
echo "Próximos pasos:"
echo "1. Editar backend/.env con tu PIPEDRIVE_API_KEY"
echo "2. Ejecutar: python backend/main.py"
echo "3. En otra terminal: n8n start"
echo "4. Importar flujo en http://localhost:5678"
echo ""
