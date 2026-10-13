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

Para ejecutar el proyecto necesitas:

- Flutter instalado y configurado.
- Dart, incluido con Flutter.
- Git.
- Android Studio y las herramientas del SDK de Android, si deseas ejecutar la aplicación en Android.
- Un dispositivo físico o emulador compatible.

Puedes comprobar la configuración de tu entorno con:

```bash
flutter doctor
```

### 1. Instalar las dependencias

```bash
flutter pub get
```

### 2. Ejecutar la aplicación

Comprueba los dispositivos disponibles:

```bash
flutter devices
```

Inicia la aplicación con:

```bash
flutter run
```


## Estructura del proyecto

```text
sst_ia/
├── lib/
│   ├── models/
│   ├── screens/
│   ├── services/
│   ├── theme/
│   ├── utils/
│   ├── widgets/
│   └── main.dart
├── android/
├── pubspec.yaml
├── pubspec.lock
├── analysis_options.yaml
├── README.md
└── .gitignore
```

## Verificación del código

Para revisar posibles problemas estáticos:

```bash
flutter analyze
```

Para ejecutar las pruebas automatizadas, si están configuradas:

```bash
flutter test
```
