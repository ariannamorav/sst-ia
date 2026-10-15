> **Estado del proyecto:** MVP funcional. El análisis de hallazgos implementado actualmente es simulado y utiliza reglas y palabras clave. 

## Funcionalidades

- Registro y consulta de inspecciones.
- Captura y registro de evidencias fotográficas.
- Análisis orientativo de hallazgos mediante reglas locales.
- Revisión y validación manual de hallazgos.
- Consulta de hallazgos e historial.
- Generación de informes en PDF.

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


## Nota de compatibilidad web (corrección)

La vista previa de fotografías ahora usa `Image.network` en Flutter Web y `Image.file`
en Android/iOS. Esto evita que `File.existsSync()` provoque `Unsupported operation: _Namespace`
cuando se ejecuta en `localhost:50733`.

## Integración real de IA: estado actual

El servicio conectado en `lib/main.dart` sigue siendo `ServicioAnalisisSimulado`.
Este servicio **no analiza píxeles**: usa observaciones escritas y palabras clave. Para
usar el dataset etiquetado en Roboflow y un modelo YOLO entrenado, hay que sustituirlo
por un `AnalisisService` que envíe la fotografía a una API de inferencia y transforme
las detecciones en un `Hallazgo`. No se debe mostrar la confianza simulada como si fuera
una predicción real.

Flujo objetivo:
1. Flutter captura/selecciona la fotografía.
2. El botón **Analizar evidencia con IA** envía la imagen a una API de inferencia.
3. YOLO devuelve clase, confianza y coordenadas de cada detección.
4. La app propone elemento y categoría; el profesional puede editarlos.
5. **Aprobar hallazgo** lo marca como validado; **Guardar cambios** lo deja pendiente.

Para el MVP, conviene desplegar YOLO detrás de una API HTTPS. No incluyas claves privadas
de Roboflow ni credenciales de servidor dentro de la aplicación Flutter.


## Corrección de generación de informes PDF en Flutter Web

El servicio PDF ya no usa `File.existsSync()` ni `readAsBytesSync()` para las fotografías.
En navegador, lee las imágenes de `image_picker` mediante `XFile.readAsBytes()` (rutas
`blob:`); en Android/iOS usa lectura asíncrona de archivo. Si una foto no se puede leer,
se omite esa foto, pero el informe y el resto de los hallazgos se generan igualmente.
