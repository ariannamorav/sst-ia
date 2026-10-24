# Guía de Integración Técnica - Módulo SST-IA

Esta guía detalla cómo conectar o integrar este módulo de Inteligencia Artificial con cualquier otra herramienta, sistema o aplicación externa (Flutter, React, Node.js, Django, C#, etc.).

---

## Métodos de Integración

### 1. Integración como Microservicio REST API (Recomendado)
Puedes ejecutar el servidor en segundo plano y consumirlo desde cualquier lenguaje o framework cliente.

* **Comando para iniciar el servicio:**
  ```powershell
  python server.py
  ```
  *(O `python run.py` para abrir además la interfaz web).*

* **Endpoint de Detección:**
  * **Ruta:** `POST http://localhost:5000/analizar`
  * **Headers:** `Content-Type: application/json`
  * **Payload enviado:**
    ```json
    {
      "foto_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
      "observacion": "Letrero ubicado en puerta principal",
      "ubicacion": "Pasillo 1",
      "tipo_esperado": "General"
    }
    ```
  * **Respuesta recibida:**
    ```json
    {
      "elemento": "Señal: Ruta de Evacuación",
      "categoria": "Verdes",
      "condicion": "Conforme",
      "confianza": 0.94,
      "recomendacion": "Verificar dirección de flecha de escape...",
      "bbox": [150.0, 120.0, 520.0, 380.0],
      "foto_anotada_base64": "data:image/jpeg;base64,..."
    }
    ```

---

### 2. Integración Directa en Código Python (Como Módulo / Paquete)
Si la otra herramienta está escrita en Python, puedes importar el detector directamente sin necesidad de levantar puertos HTTP:

```python
import sys
from pathlib import Path

# Agregar la ruta del módulo al PATH
sys.path.append(r"C:\Users\Yairc\Downloads\Modulo_SST_IA")

from app.services.detector_ia import detector_ia_service

# Analizar una foto por ruta de archivo
resultado = detector_ia_service.analizar(foto_path="mi_foto.jpg")

print("Señal detectada:", resultado["elemento"])
print("Categoría SST:", resultado["categoria"])
print("Certeza:", resultado["confianza"])
print("Caja delimitadora:", resultado["bbox"])
```

---

### 3. Reentrenamiento Automático desde Otra Herramienta
Si tu otra herramienta necesita actualizar el modelo con nuevos datos de forma programática:

* **Con Dataset de Prohibición (2 clases):**
  ```powershell
  python train_model.py --epochs 25 --yaml "data/datasets/prohibido-celular/data.yaml"
  ```

* **Con Dataset Completo Normativo (8 clases):**
  ```powershell
  python train_model.py --epochs 35 --yaml "data/datasets/sst-completo/data.yaml"
  ```

Los pesos finales se guardan automáticamente en `models/sst_best.pt`, listos para ser consumidos de inmediato sin reiniciar la máquina.
