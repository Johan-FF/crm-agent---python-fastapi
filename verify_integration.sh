#!/bin/bash
# PostgreSQL Integration Verification Script
# Verifica que todos los componentes estén correctamente instalados

echo "=================================================="
echo "PostgreSQL Integration Verification Script"
echo "=================================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print result
check_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $2"
    else
        echo -e "${RED}✗${NC} $2"
    fi
}

echo "1. Checking Required Files..."
echo "================================"

files=(
    "backend/app/db/base.py"
    "backend/app/db/session.py"
    "backend/app/models/contact.py"
    "backend/app/repositories/contact_repository.py"
    "backend/app/services/contact_service.py"
    "backend/app/api/v1/endpoints/contact.py"
    "backend/app/main.py"
    "backend/requirements.txt"
    "docker-compose.yml"
    ".env.example"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        check_result 0 "File: $file"
    else
        check_result 1 "File: $file (MISSING)"
    fi
done

echo ""
echo "2. Checking Python Dependencies..."
echo "================================"

dependencies=(
    "sqlalchemy"
    "psycopg2"
    "alembic"
)

for dep in "${dependencies[@]}"; do
    if grep -q "$dep" backend/requirements.txt; then
        check_result 0 "Dependency: $dep"
    else
        check_result 1 "Dependency: $dep (NOT IN REQUIREMENTS)"
    fi
done

echo ""
echo "3. Checking Docker Compose Configuration..."
echo "================================"

if [ -f "docker-compose.yml" ]; then
    echo "Checking PostgreSQL service..."
    if grep -q "postgres:16-alpine" docker-compose.yml; then
        check_result 0 "PostgreSQL image configured"
    else
        check_result 1 "PostgreSQL image NOT found"
    fi
    
    echo "Checking health checks..."
    if grep -q "pg_isready" docker-compose.yml; then
        check_result 0 "Health checks configured"
    else
        check_result 1 "Health checks NOT found"
    fi
    
    echo "Checking FastAPI dependency..."
    if grep -q "service_healthy" docker-compose.yml; then
        check_result 0 "FastAPI depends on healthy PostgreSQL"
    else
        check_result 1 "FastAPI dependency NOT properly configured"
    fi
fi

echo ""
echo "4. Checking Code Patterns..."
echo "================================"

echo "Checking for SQLAlchemy Base..."
if grep -q "declarative_base()" backend/app/db/base.py; then
    check_result 0 "SQLAlchemy Base configured"
else
    check_result 1 "SQLAlchemy Base NOT found"
fi

echo "Checking for SessionLocal factory..."
if grep -q "SessionLocal" backend/app/db/base.py; then
    check_result 0 "SessionLocal factory defined"
else
    check_result 1 "SessionLocal factory NOT found"
fi

echo "Checking for init_db() function..."
if grep -q "def init_db" backend/app/db/base.py; then
    check_result 0 "init_db() function defined"
else
    check_result 1 "init_db() function NOT found"
fi

echo "Checking for get_db() dependency..."
if grep -q "def get_db" backend/app/db/session.py; then
    check_result 0 "get_db() dependency defined"
else
    check_result 1 "get_db() dependency NOT found"
fi

echo "Checking for ORM model..."
if grep -q "class Contact(Base)" backend/app/models/contact.py; then
    check_result 0 "Contact ORM model defined"
else
    check_result 1 "Contact ORM model NOT found"
fi

echo "Checking for Repository db parameter..."
if grep -q "def __init__(self, db: Session)" backend/app/repositories/contact_repository.py; then
    check_result 0 "Repository accepts db: Session"
else
    check_result 1 "Repository db parameter NOT found"
fi

echo "Checking for Service db parameter..."
if grep -q "def __init__(self, db: Session)" backend/app/services/contact_service.py; then
    check_result 0 "Service accepts db: Session"
else
    check_result 1 "Service db parameter NOT found"
fi

echo "Checking for endpoint db dependency..."
if grep -q "db: Session = Depends(get_db)" backend/app/api/v1/endpoints/contact.py; then
    check_result 0 "Endpoints inject db dependency"
else
    check_result 1 "Endpoint db dependency NOT found"
fi

echo "Checking for lifespan initialization..."
if grep -q "init_db()" backend/app/main.py; then
    check_result 0 "init_db() called in main.py"
else
    check_result 1 "init_db() NOT called in main.py"
fi

echo ""
echo "5. Database Configuration..."
echo "================================"

if [ -f ".env.example" ]; then
    echo "Checking .env.example..."
    if grep -q "DATABASE_URL" .env.example; then
        check_result 0 "DATABASE_URL configured"
    else
        check_result 1 "DATABASE_URL NOT found in .env.example"
    fi
    
    if grep -q "DB_USER" .env.example; then
        check_result 0 "DB_USER configured"
    else
        check_result 1 "DB_USER NOT found in .env.example"
    fi
    
    if grep -q "DB_PASSWORD" .env.example; then
        check_result 0 "DB_PASSWORD configured"
    else
        check_result 1 "DB_PASSWORD NOT found in .env.example"
    fi
else
    check_result 1 ".env.example file NOT found"
fi

echo ""
echo "6. Documentation Files..."
echo "================================"

docs=(
    "docs/POSTGRESQL_INTEGRATION.md"
    "docs/QUICK_START.md"
    "docs/REFACTORING_COMPLETE.md"
    "docs/INTEGRATION_SUMMARY.md"
    "docs/QUICK_REFERENCE.md"
)

for doc in "${docs[@]}"; do
    if [ -f "$doc" ]; then
        check_result 0 "Documentation: $doc"
    else
        check_result 1 "Documentation: $doc (MISSING)"
    fi
done

echo ""
echo "=================================================="
echo "Verification Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env"
echo "2. Run: docker-compose up"
echo "3. Test: curl http://localhost:8000/contact/health"
echo "4. View API docs: http://localhost:8000/docs"
echo ""
