# SST-IA - Aplicación Móvil y Web de Inspección SST

> **Sistema Completo:** Aplicación Flutter integrada con el motor de Inteligencia Artificial (Backend en Python con YOLOv8 y Roboflow). Permite la inspección en campo, captura fotográfica de señales y elementos de seguridad, detección automática por visión artificial, validación normativa (NTC / ISO) y generación de informes en PDF.

## Funcionalidades Principales

- **Detección Automática por IA:** Conexión en tiempo real con el servidor de visión artificial (`http://localhost:5000/analizar`) para clasificar señales de evacuación, incendio, advertencia, obligación y prohibición.
- **Modo Offline / Respaldo:** En caso de no tener el backend encendido, cuenta con un motor de reglas y palabras clave local para no detener la operación.
- **Registro de Inspecciones:** Creación y seguimiento de inspecciones por sede, área y responsable.
- **Captura de Evidencias:** Compatible con cámara en vivo y carga de imágenes en Web, Desktop (Windows) y Móvil (Android/iOS).
- **Validación Normativa:** Revisión de hallazgos contra el catálogo de 20 normas de seguridad y salud en el trabajo.
- **Reportes en PDF:** Exportación inmediata de informes técnicos de inspección para brigadas y comités de SST.

## Tecnologías utilizadas

- **Flutter:** desarrollo de la aplicación móvil.
- **Dart:** lenguaje de programación.
- **Provider:** gestión del estado de la aplicación.
- **image_picker:** selección y captura de imágenes.
- **pdf:** generación de documentos PDF.
- **printing:** impresión o visualización de documentos PDF, según la plataforma.

## Requisitos

Para ejecutar el proyecto completo necesitas:
- Flutter SDK (3.10+ o superior) y Dart.
- Python 3.10 o superior (para el servidor y modelos de IA).
- Google Chrome (para Web) o dispositivo Android / Windows.

### 1. Instalar dependencias

**Frontend (Flutter):**
```bash
flutter pub get
```

**Backend de IA (Python):**
```bash
pip install -r backend/requirements.txt
```

---

## 🎮 Ejecución del Proyecto

### Opción A: Sistema Completo (Servidor IA + Flutter)

1. **Terminal 1 - Iniciar Servidor de Visión Artificial:**
   ```bash
   python backend/servidor_api_sst.py
   ```
   *El servidor quedará escuchando en `http://localhost:5000` listo para procesar evidencias.*

2. **Terminal 2 - Iniciar la App de Flutter:**
   ```bash
   flutter run -d chrome
   ```
   *(o en Windows nativo con `flutter run -d windows`)*

---

### Opción B: Aplicación de Escritorio con Cámara Web en Vivo Directa

Si deseas abrir la cámara de tu PC con OpenCV para encuadrar en tiempo real y validar hallazgos:
```bash
python backend/inspeccion_sst_app.py
```

---

## Estructura del proyecto

```text
sst-ia/
├── backend/                       # Motor de Inteligencia Artificial (Python)
│   ├── servidor_api_sst.py        # API HTTP para Flutter (puerto 5000)
│   ├── sst_multi_detector.py      # Motor multi-workflow y Roboflow Datasets
│   ├── inspeccion_sst_app.py      # App de escritorio con cámara web en vivo
│   ├── camara_workflow.py         # Monitor de detección continua
│   ├── test_workflow.py           # Pruebas con imágenes
│   ├── main.py                    # Script de entrenamiento YOLOv8
│   ├── requirements.txt           # Dependencias Python
│   └── .env.example               # Configuración de variables de entorno
│
├── lib/                           # Código fuente de la app Flutter
│   ├── models/                    # Modelos (Inspección, Evidencia, Hallazgo)
│   ├── screens/                   # 14 Pantallas de la aplicación
│   ├── services/                  # Conexión HTTP (analisis_ia_service.dart) y AppState
│   ├── theme/                     # Tema visual
│   ├── utils/                     # Constantes y utilidades
│   ├── widgets/                   # Componentes reutilizables
│   └── main.dart                  # Punto de entrada
│
├── pubspec.yaml                   # Dependencias de Flutter (http, provider, pdf, printing)
├── README.md                      # Documentación del proyecto
└── .gitignore                     # Exclusiones de Git
```

## Verificación del código

```bash
flutter test
flutter analyze
```

