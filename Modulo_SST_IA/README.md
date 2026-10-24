# Módulo de Inteligencia Artificial para Seguridad y Salud en el Trabajo (SST-IA)

Este módulo es una solución **completamente autónoma, portable e independiente** de visión por computadora para detección de elementos normativos SST en tiempo real, auditoría visual e inspección con generación de informes técnicos.

---

## 🚀 Requisitos e Instalación

Para utilizar este módulo en cualquier entorno, proyecto o herramienta:

```powershell
pip install -r requirements.txt
```

---

## 🎯 Comandos Principales

### 1. Iniciar la Plataforma Web y Servidor API REST
Inicia el servidor backend en el puerto 5000 y abre automáticamente el navegador:
```powershell
python run.py
```
* **Interfaz Web:** `http://localhost:5000`
* **API REST para apps móviles/Flutter/React:** `POST http://localhost:5000/analizar`
* **Documentación interactiva Swagger:** `http://localhost:5000/docs`

---

### 2. Entrenar el Modelo con Dataset Básico (2 Clases)
Entrena YOLOv8 con el dataset de `prohibido-celular` y `piso-resbaloso`:
```powershell
python train_model.py --epochs 25 --yaml "data/datasets/prohibido-celular/data.yaml"
```

---

### 3. Entrenar el Modelo con Dataset Completo (8 Clases Normativas)
Entrena YOLOv8 con todas las señales unificadas (Extintor, Gabinete, Ruta Evacuación, Punto Encuentro, etc.):
```powershell
python train_model.py --epochs 35 --yaml "data/datasets/sst-completo/data.yaml"
```
*Los mejores pesos se guardan automáticamente en `models/sst_best.pt` al finalizar.*

---

### 4. Detección en Tiempo Real con Cámara Web (100% Offline OpenCV)
```powershell
python camara_local_opencv.py
```

### 5. Prueba por Lote sobre Carpetas de Imágenes con OpenCV
```powershell
python probar_fotos_opencv.py
```

---

## 🔌 Integración en Otra Herramienta

### Modo A: Consumo vía API REST (Recomendado para Flutter, React, Vue, Node.js)
El servidor expone el endpoint estándar `/analizar`:
* **Método:** `POST`
* **URL:** `http://localhost:5000/analizar`
* **Body (JSON):**
  ```json
  {
    "foto_base64": "data:image/jpeg;base64,...",
    "observacion": "Inspección de pasillo",
    "ubicacion": "Piso 2",
    "tipo_esperado": "General"
  }
  ```
* **Respuesta:**
  ```json
  {
    "elemento": "Extintor de Incendio",
    "categoria": "Rojas",
    "condicion": "Requiere verificación",
    "confianza": 0.94,
    "recomendacion": "Verificar manómetro en zona verde...",
    "bbox": [120.0, 85.0, 450.0, 680.0],
    "foto_anotada_base64": "..."
  }
  ```

### Modo B: Uso Directo como Librería Python
Puedes importar el servicio detector en cualquier script de Python:
```python
from app.services.detector_ia import detector_ia_service

# Analizar imagen desde archivo o Base64
resultado = detector_ia_service.analizar(foto_path="ruta/a/mi_foto.jpg")

print("Elemento detectado:", resultado["elemento"])
print("Categoría SST:", resultado["categoria"])
print("Confianza:", resultado["confianza"])
```
