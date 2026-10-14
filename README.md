> **Estado del proyecto:** MVP funcional. El análisis de hallazgos implementado actualmente es simulado y utiliza reglas y palabras clave. 

## Funcionalidades

- Registro y consulta de inspecciones.
- Captura y registro de evidencias fotográficas.
- Análisis orientativo de hallazgos mediante reglas locales.
- Revisión y validación manual de hallazgos.
- Consulta de hallazgos e historial.
- Generación de informes en PDF

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
