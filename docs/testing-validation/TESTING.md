# 🧪 Guía de Testing - Verticcal CRM Agent

Este documento proporciona instrucciones detalladas para probar el sistema completo.

## ✅ Pre-requisitos para Testing

1. **FastAPI corriendo:**
   ```bash
   cd backend
   python main.py
   # o
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **n8n corriendo:**
   ```bash
   n8n start
   # o si usas Docker:
   docker run -it --name n8n -p 5678:5678 n8nio/n8n:latest
   ```

3. **Flujo importado y activado en n8n**

4. **Pipedrive API Key configurado en `backend/.env`**

5. **OpenAI API Key configurado en n8n Credentials**

---

## 🧪 Caso 1: Crear Contacto

### Propósito
Verificar que el agente puede interpretar una orden de crear contacto, extraer los datos, invocar FastAPI y crear el contacto en Pipedrive.

### Criterios de Aceptación
- ✅ Contacto creado en Pipedrive
- ✅ Mensaje de confirmación en n8n con ID del contacto
- ✅ Email validado (no permite duplicados)
- ✅ Logs con Correlation ID

### Prompts de Prueba

#### Test 1.1: Crear con todos los datos
```
Crea a Ana Gómez con email ana.gomez@ejemplo.com y teléfono +57 315 222 3344.
```

**Resultado esperado:**
- El agente extrae: name="Ana Gómez", email="ana.gomez@ejemplo.com", phone="+57 315 222 3344"
- Invoca `POST /crm/contact` en FastAPI
- FastAPI retorna: `{"success": true, "contact_id": 123, "url": "...", "correlation_id": "uuid"}`
- n8n muestra: "✅ Contacto 'Ana Gómez' creado exitosamente. ID: 123"
- En Pipedrive: Nuevo contacto visible con email y teléfono

#### Test 1.2: Crear solo con nombre y email
```
Registra un nuevo contacto: Carlos Martín, carlos.martin@empresa.com
```

**Resultado esperado:**
- name="Carlos Martín", email="carlos.martin@empresa.com", phone=null
- Contacto creado correctamente en Pipedrive

#### Test 1.3: Crear solo con nombre
```
Agrega a María López a los contactos.
```

**Resultado esperado:**
- name="María López", email=null, phone=null
- Contacto creado correctamente

#### Test 1.4: Validación de Duplicados
1. Crear Ana Gómez con email ana.gomez@ejemplo.com
2. Intentar crear otro Ana Gómez con el mismo email

**Resultado esperado:**
- Primera creación: ✅ Éxito
- Segunda creación: ❌ Error con mensaje "Ya existe un contacto con email ana.gomez@ejemplo.com"

#### Test 1.5: Variaciones de Lenguaje Natural
Probar cada variación para verificar que el agente entienda diferentes formas de pedir:

```
"Necesito registrar a Juan Pérez, teléfono +57 310 555 6666"
"Crea el contacto de Pedro García - pedro@mail.com"
"Agrega este contacto: Sofía Rodríguez, +57 301 222 3333"
```

**Resultado esperado:**
- Todas deberían crear contactos correctamente (el agente entiende la intención)

---

## 🧪 Caso 2: Agregar Nota a Contacto

### Propósito
Verificar que se puede agregar una nota a un contacto existente. El agente debe encontrar el contacto por nombre y luego crear la nota.

### Criterios de Aceptación
- ✅ Nota creada en Pipedrive bajo el contacto
- ✅ Mensaje de confirmación en n8n
- ✅ El agente busca el contacto por nombre si es necesario
- ✅ Manejo elegante si el contacto no existe

### Prompts de Prueba

#### Test 2.1: Agregar nota a contacto recientemente creado
```
Agrega una nota a Ana Gómez: 'Cliente interesado en plan Premium'.
```

**Resultado esperado:**
- El agente reconoce "Ana Gómez" del contexto conversacional
- Invoca `POST /crm/contact/note` con contact_id y content
- n8n muestra: "✅ Nota agregada al contacto Ana Gómez"
- En Pipedrive: Nota visible en el timeline del contacto

#### Test 2.2: Agregar nota con ID explícito (si es necesario)
```
Agrega una nota al contacto ID 123: 'Seguimiento: llamar el próximo martes'
```

**Resultado esperado:**
- El agente extrae contact_id=123 y content
- Nota creada correctamente

#### Test 2.3: Múltiples notas al mismo contacto
```
Agrega a Ana Gómez: 'Solicita demo del plan Pro'
```
```
Anota que Ana está esperando presupuesto
```

**Resultado esperado:**
- Se crean 2 notas diferentes
- Ambas visibles en Pipedrive

#### Test 2.4: Contacto no encontrado
```
Agrega una nota a Contacto Fantasma: 'Esto no debería funcionar'
```

**Resultado esperado:**
- El agente pide el ID del contacto
- O retorna error claro: "No encontré el contacto, proporciona el ID"

#### Test 2.5: Nota vacía (validación)
```
Agrega una nota vacía a Ana Gómez: ''
```

**Resultado esperado:**
- FastAPI rechaza con error: "El contenido de la nota no puede estar vacío"
- n8n muestra error de manera clara

---

## 🧪 Caso 3: Actualizar Campo de Contacto

### Propósito
Verificar que se puede actualizar uno o varios campos de un contacto (teléfono, estado, etc.).

### Criterios de Aceptación
- ✅ Campo actualizado en Pipedrive
- ✅ Mensaje de confirmación en n8n
- ✅ Puede actualizar múltiples campos a la vez
- ✅ Validación de tipos de datos

### Prompts de Prueba

#### Test 3.1: Actualizar teléfono
```
Actualiza el teléfono de Ana Gómez a +57 311 999 0000.
```

**Resultado esperado:**
- El agente extrae: contact_id (del contexto o búsqueda), fields={"phone": "+57 311 999 0000"}
- Invoca `PATCH /crm/contact`
- n8n muestra: "✅ Teléfono de Ana Gómez actualizado a +57 311 999 0000"
- En Pipedrive: Teléfono actualizado

#### Test 3.2: Actualizar estado
```
Cámbia el estado de Ana a 'Qualified'.
```

**Resultado esperado:**
- fields={"status": "Qualified"}
- Contacto marcado como Qualified en Pipedrive

#### Test 3.3: Actualizar múltiples campos
```
Actualiza a Carlos: teléfono +57 320 000 1122 y estado a 'Qualified'.
```

**Resultado esperado:**
- fields={"phone": "+57 320 000 1122", "status": "Qualified"}
- Ambos campos actualizados simultáneamente

#### Test 3.4: Actualizar email
```
Cambia el email de María López a maria.nueva@empresa.com.
```

**Resultado esperado:**
- Email actualizado en Pipedrive

#### Test 3.5: Validación de ID
```
Actualiza el contacto ID 999999 a estado 'Lead'.
```

**Resultado esperado:**
- Si el ID no existe en Pipedrive, debería retornar error claro
- n8n muestra: "❌ Contacto ID 999999 no encontrado"

---

## 🔄 Caso Completo: Flujo Conversacional Completo

### Escenario
Simular un caso real donde el usuario hace múltiples acciones en una conversación.

```
Usuario: "Crea a Pedro García con email pedro@empresa.com y teléfono +57 310 555 6666"
Sistema: "✅ Contacto Pedro García creado (ID: 456)"

Usuario: "Agrega una nota: 'Interesado en integración API'"
Sistema: "✅ Nota agregada a Pedro"

Usuario: "Actualiza su estado a Qualified"
Sistema: "✅ Estado actualizado a Qualified"

Usuario: "¿Cuál es el teléfono de Pedro?"
Sistema: "+57 310 555 6666 (del contexto conversacional)"
```

**Resultado esperado:**
- Toda la conversación funciona fluidamente
- El Chat Memory mantiene el contexto
- Cada acción se verifica en Pipedrive
- Logs muestran todos los Correlation IDs

---

## 🔧 Testing Manual de Endpoints

Si quieres probar los endpoints directamente sin n8n:

### Test Crear Contacto
```bash
curl -X POST http://localhost:8000/crm/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@ejemplo.com",
    "phone": "+57 300 000 0000"
  }'
```

**Respuesta esperada:**
```json
{
  "success": true,
  "message": "Contacto creado",
  "contact_id": 123,
  "url": "https://app.pipedrive.com/person/123",
  "correlation_id": "uuid-here"
}
```

### Test Agregar Nota
```bash
curl -X POST http://localhost:8000/crm/contact/note \
  -H "Content-Type: application/json" \
  -d '{
    "contact_id": 123,
    "content": "Test note"
  }'
```

### Test Actualizar Contacto
```bash
curl -X PATCH http://localhost:8000/crm/contact \
  -H "Content-Type: application/json" \
  -d '{
    "contact_id": 123,
    "fields": {"phone": "+57 311 999 0000"}
  }'
```

### Test Health Check
```bash
curl http://localhost:8000/health
```

---

## 📊 Tabla de Casos de Prueba

| ID | Descripción | Prompt | Resultado Esperado | Status |
|----|-------------|--------|-------------------|--------|
| 1.1 | Crear contacto completo | "Crea a Ana..." | Contacto creado | ☐ |
| 1.2 | Crear sin teléfono | "Carlos Martín..." | Contacto sin phone | ☐ |
| 1.3 | Crear solo nombre | "Agrega a María..." | Contacto minimal | ☐ |
| 1.4 | Validar duplicados | Crear 2 con mismo email | Error en segunda | ☐ |
| 1.5 | Variación lenguaje | Múltiples formas | Todas funcionan | ☐ |
| 2.1 | Nota a contacto | "Agrega nota a Ana..." | Nota creada | ☐ |
| 2.2 | Nota con ID | "Nota a ID 123..." | Nota creada | ☐ |
| 2.3 | Múltiples notas | 2+ notas mismo contacto | Ambas visibles | ☐ |
| 2.4 | Contacto no existe | "Nota a Fantasma..." | Error claro | ☐ |
| 3.1 | Actualizar teléfono | "Actualiza teléfono..." | Teléfono updated | ☐ |
| 3.2 | Actualizar estado | "Estado a Qualified..." | Status updated | ☐ |
| 3.3 | Múltiples campos | "Actualiza 2 campos..." | Ambos updated | ☐ |
| 3.4 | Validación ID | "Update ID fake..." | Error apropiado | ☐ |

---

## 🎯 Checklist Final

Antes de considerar el testing completo:

- [ ] FastAPI responde en `/health`
- [ ] Todos los casos 1.1-1.5 funcionan
- [ ] Todos los casos 2.1-2.4 funcionan
- [ ] Todos los casos 3.1-3.4 funcionan
- [ ] Los contactos aparecen en Pipedrive
- [ ] Las notas aparecen en Pipedrive
- [ ] Los campos se actualizan en Pipedrive
- [ ] Los logs muestran Correlation IDs
- [ ] Los errores se manejan elegantemente
- [ ] El flujo conversacional funciona sin interrupciones

---

## 📝 Notas

- Todos los prompts pueden variarse (lenguaje natural)
- El sistema debe entender intenciones, no solo palabras exactas
- Los IDs de Pipedrive deben tomarse de la API
- Verificar siempre en Pipedrive que los cambios se hayan guardado
- Revisar logs de FastAPI para Correlation IDs

Para más información, ver `docs/reference/FAQ.md` o consultar la documentación en `docs/setup-guides/`
