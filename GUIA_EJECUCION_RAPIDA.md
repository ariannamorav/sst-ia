# 🚀 Guía de Ejecución Rápida: Sistema SST-IA

Esta guía detalla cómo iniciar y operar el ecosistema completo **SST-IA** en tu computadora en menos de 1 minuto:
1. **Backend de Inteligencia Artificial (FastAPI + YOLOv8 + ReportLab PDF):** Ubicado en `Modulo_SST_IA` (Puerto 5000).
2. **Frontend Multiplataforma (Flutter Web / Desktop):** Ubicado en `sst-ia` (Puerto 8085).

---

## ⚡ Opción 1: Iniciar Todo con un Solo Comando (Recomendada)

Desde tu terminal de PowerShell en la carpeta principal `C:\Users\Yairc\Documents\Universidad\IA`:

```powershell
.\iniciar.ps1
```
*(O en CMD: `iniciar_todo.bat` o haz doble clic a [iniciar_todo.bat](file:///c:/Users/Yairc/Documents/Universidad/IA/iniciar_todo.bat)).*

> 🪄 **¿Qué hace este único comando automáticamente?**
> 1. Si los puertos 5000 u 8085 quedaron tomados por un proceso anterior, los libera automáticamente.
> 2. Abre una ventana con el **Backend Python FastAPI** (`http://localhost:5000`).
> 3. Abre otra ventana con la **App Flutter Web** (`http://localhost:8085`) y abre Chrome automáticamente.

---

## 🛠️ Opción 2: Inicio Manual en Dos Pasos

Si prefieres abrir cada terminal por separado:

### Terminal 1: Backend de IA (Python)
```powershell
cd C:\Users\Yairc\Documents\Universidad\IA\Modulo_SST_IA
python server.py
```

### Terminal 2: Aplicación Web (Flutter)
```powershell
cd C:\Users\Yairc\Documents\Universidad\IA\sst-ia
flutter run -d chrome --web-port 8085
```

---

## 🌐 URLs y Puertos del Ecosistema

| Servicio | URL / Puerto | Descripción |
| :--- | :--- | :--- |
| **App Flutter Web** | `http://localhost:8085` | Interfaz de usuario con diseño adaptable para PC y móvil. |
| **Backend de IA** | `http://localhost:5000` | API FastAPI con YOLOv8 (`sst_best.pt`) y generador de PDF. |
| **API Swagger Docs** | `http://localhost:5000/docs` | Documentación interactiva de todos los endpoints REST. |
| **Informe Oficial PDF** | `http://localhost:5000/api/inspecciones/activa/informe.pdf` | Generador pericial oficial en PDF con ReportLab y APA 7ma. |

---

## 🔍 Funcionalidades Clave y Cómo Usarlas

### 1. Detección Asistida por IA y Bounding Boxes
* Entra en **"Iniciar Nueva Inspección Técnica"** y toma o carga una foto de una señal o equipo locativo.
* El sistema enviará la imagen en Base64 a `http://localhost:5000/analizar`.
* En la pantalla de resultados podrás alternar entre la **fotografía original** y la **detección con caja delimitadora (Bounding Box)** dibujada por el modelo en los colores oficiales.
* Se desplegarán automáticamente la **Norma Legal Aplicable**, los colores reglamentarios, alturas de montaje y la **Recomendación Técnica Oficial**.

### 2. Checklist Normativo y Validación Humana
* En la pantalla de revisión, dispones de casillas de verificación interactivas para certificar en terreno cada uno de los puntos normativos (manómetro en verde, despeje de 1 metro, pasador intacto, etc.).
* El auditor puede editar la recomendación técnica y condición antes de aprobar el hallazgo.

### 3. Generación y Descarga de Informes en PDF
* En la sección **"Informes PDF"**, haz clic en **"Visualizar e Imprimir Informe PDF"**.
* El sistema obtiene directamente el informe pericial oficial de 400+ KB generado por el motor ReportLab de Python, incluyendo:
  * Encabezados institucionales y marco legal colombiano (NTC 1461, NSR-10 Títulos J y K, Res. 2400/79, Dec. 1072/15).
  * Matriz técnica de riesgos y guía cromática de señalización.
  * Registro fotográfico estructurado bajo normas APA 7ma edición.
  * Bloque de firmas oficiales del auditor y de la coordinación SST.

### 4. Gestión del Dataset y Reentrenamiento YOLOv8
* En el menú lateral o inicio, entra en **"Dataset y Modelo YOLOv8"**:
  * **Importar vía cURL:** Pega tu comando cURL de Roboflow para descargar y descomprimir el dataset en la carpeta `data/datasets/`.
  * **Reentrenar Modelo:** Selecciona el número de épocas (10, 25, 35, 50) y presiona **"Iniciar Reentrenamiento YOLOv8"**.
  * **Monitoreo en Vivo:** Sigue el porcentaje de avance y los mensajes de estado en tiempo real. Los pesos se guardan en `models/sst_best.pt`.

### 5. Catálogo Oficial de Normas SST
* Pestaña **"Normas SST"** en la barra lateral:
  * Filtra por categorías cromáticas (Rojas, Amarillas, Azules, Verdes).
  * Busca por palabras clave (ej: *extintor, gabinete, salida, retie, casco*).
  * Consulta alturas de fijación, colores de contraste, fórmulas dimensionales ($S \ge d^2 / 2000$) y checklists.

---

## 🛠️ Solución de Problemas Frecuentes

### 1. El backend dice que el puerto 5000 ya está en uso
Verifica si ya tenías una terminal corriendo `python server.py` o `python run.py`. Puedes detenerla con `Ctrl + C` o revisar procesos con:
```powershell
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
```

### 2. El puerto 8085 está ocupado al correr Flutter
Puedes cambiar el puerto web en el comando:
```powershell
flutter run -d chrome --web-port 8090
```

### 3. La app Flutter muestra "Modo Local Offline"
Asegúrate de que la terminal del backend Python esté abierta y respondiendo en `http://localhost:5000`. Puedes verificarlo visitando `http://localhost:5000/api/health` en tu navegador.
