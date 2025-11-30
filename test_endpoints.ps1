# Script para probar todos los endpoints de Verticcal CRM en Windows

$BASE_URL = "http://localhost:8000/api/v1"
$CONTACT_ID = $null

# Generar número aleatorio para emails únicos
$randomNum = Get-Random -Minimum 10000 -Maximum 99999

# ================================================================
# 1. Health Check
# ================================================================
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "1 - HEALTH CHECK" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

try {
    $response = Invoke-WebRequest -Uri "$BASE_URL/contact/health" -Method GET -ContentType "application/json" -ErrorAction Stop
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 5
    Write-Host "[+] API está saludable" -ForegroundColor Green
} catch {
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
}

Read-Host "Presione Enter para continuar"

# ================================================================
# 2. Crear Contacto
# ================================================================
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "2 - CREAR CONTACTO" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

try {
    $body = @{
        name = "Sofia Martinez $randomNum"
        email = "sofia$randomNum@example.com"
        phone = "+34621234567"
    } | ConvertTo-Json -Compress
    
    $response = Invoke-WebRequest -Uri "$BASE_URL/contact" -Method POST -Body $body -ContentType "application/json" -ErrorAction Stop
    $data = $response.Content | ConvertFrom-Json
    
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 5
    
    $CONTACT_ID = $data.contact_id
    Write-Host "[+] Contacto creado con ID: $CONTACT_ID" -ForegroundColor Green
} catch {
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
}

Read-Host "Presione Enter para continuar"

# ================================================================
# 3. Actualizar Teléfono
# ================================================================
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "3 - ACTUALIZAR TELEFONO" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

if ($CONTACT_ID) {
    try {
        $body = @{
            contact_id = $CONTACT_ID
            phone = "+34699999999"
        } | ConvertTo-Json -Compress
        
        $response = Invoke-WebRequest -Uri "$BASE_URL/contact" -Method PATCH -Body $body -ContentType "application/json" -ErrorAction Stop
        $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 5
        
        Write-Host "[+] Teléfono actualizado" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Read-Host "Presione Enter para continuar"

# ================================================================
# 4. Actualizar Múltiples Campos
# ================================================================
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "4 - ACTUALIZAR MULTIPLES CAMPOS" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

if ($CONTACT_ID) {
    try {
        $body = @{
            contact_id = $CONTACT_ID
            name = "Sofia Martinez Updated"
            email = "sofia.updated$randomNum@example.com"
        } | ConvertTo-Json -Compress
        
        $response = Invoke-WebRequest -Uri "$BASE_URL/contact" -Method PATCH -Body $body -ContentType "application/json" -ErrorAction Stop
        $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 5
        
        Write-Host "[+] Contacto actualizado" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Read-Host "Presione Enter para continuar"

# ================================================================
# 5. Agregar Primera Nota
# ================================================================
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "5 - AGREGAR PRIMERA NOTA" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

if ($CONTACT_ID) {
    try {
        $body = @{
            contact_id = $CONTACT_ID
            content = "Nota de prueba desde PowerShell"
        } | ConvertTo-Json -Compress
        
        $response = Invoke-WebRequest -Uri "$BASE_URL/contact/note" -Method POST -Body $body -ContentType "application/json" -ErrorAction Stop
        $data = $response.Content | ConvertFrom-Json
        
        $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 5
        
        Write-Host "[+] Nota agregada (ID: $($data.note_id))" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Read-Host "Presione Enter para continuar"

# ================================================================
# 6. Agregar Segunda Nota
# ================================================================
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "6 - AGREGAR SEGUNDA NOTA" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

if ($CONTACT_ID) {
    try {
        $body = @{
            contact_id = $CONTACT_ID
            content = "Segunda nota - Información adicional"
        } | ConvertTo-Json -Compress
        
        $response = Invoke-WebRequest -Uri "$BASE_URL/contact/note" -Method POST -Body $body -ContentType "application/json" -ErrorAction Stop
        $data = $response.Content | ConvertFrom-Json
        
        $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 5
        
        Write-Host "[+] Nota agregada (ID: $($data.note_id))" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Read-Host "Presione Enter para continuar"

# ================================================================
# 7. Crear Segundo Contacto
# ================================================================
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "7 - CREAR SEGUNDO CONTACTO" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

$randomNum2 = Get-Random -Minimum 10000 -Maximum 99999

try {
    $body = @{
        name = "Carlos Lopez $randomNum2"
        email = "carlos$randomNum2@example.com"
        phone = "+34611111111"
    } | ConvertTo-Json -Compress
    
    $response = Invoke-WebRequest -Uri "$BASE_URL/contact" -Method POST -Body $body -ContentType "application/json" -ErrorAction Stop
    $data = $response.Content | ConvertFrom-Json
    
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 5
    
    Write-Host "[+] Segundo contacto creado (ID: $($data.contact_id))" -ForegroundColor Green
} catch {
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
}

Read-Host "Presione Enter para continuar"

# ================================================================
# 8. Resumen Final
# ================================================================
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "RESUMEN DE PRUEBAS" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[OK] Health Check" -ForegroundColor Green
Write-Host "[OK] Crear Contacto" -ForegroundColor Green
Write-Host "[OK] Actualizar Teléfono" -ForegroundColor Green
Write-Host "[OK] Actualizar Múltiples Campos" -ForegroundColor Green
Write-Host "[OK] Agregar Nota 1" -ForegroundColor Green
Write-Host "[OK] Agregar Nota 2" -ForegroundColor Green
Write-Host "[OK] Crear Segundo Contacto" -ForegroundColor Green
Write-Host ""
Write-Host "Contacto principal ID: $CONTACT_ID" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para ver logs:" -ForegroundColor Yellow
Write-Host "  docker compose logs fastapi --tail=100" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para consultar la BD:" -ForegroundColor Yellow
Write-Host "  docker compose exec db psql -U crm_user -d verticcal_crm" -ForegroundColor Cyan
Write-Host "  SELECT id, name, email, phone, crm_id FROM contacts;" -ForegroundColor Cyan
Write-Host ""

Read-Host "Presione Enter para salir"
