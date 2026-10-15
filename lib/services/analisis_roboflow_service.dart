
import '../models/evidencia.dart';
import '../models/hallazgo.dart';
import 'analisis_service.dart';
import 'roboflow_service.dart';

class ServicioAnalisisRoboflow implements AnalisisService {
  final RoboflowService _roboflow = RoboflowService();

  // Umbral inicial: descartar detecciones con menos del 30 %.
  static const double _confianzaMinima = 0.30;

  @override
  Future<Hallazgo> analizar(Evidencia evidencia) async {
    final bytes = evidencia.fotoBytes;

    if (bytes == null || bytes.isEmpty) {
      throw Exception(
        'No hay datos de la fotografía. Vuelve a capturar la evidencia.',
      );
    }

    final respuesta = await _roboflow.analizarImagen(bytes);

    // Roboflow Workflow: outputs[0].predictions.predictions
    final dynamic outputs = respuesta['outputs'];

    if (outputs is! List || outputs.isEmpty) {
      throw const FormatException(
        'Roboflow no devolvió resultados en outputs.',
      );
    }

    final dynamic salida = outputs.first;
    if (salida is! Map) {
      throw const FormatException(
        'El primer resultado de Roboflow no es válido.',
      );
    }

    final dynamic bloque = salida['predictions'];
    if (bloque is! Map) {
      throw const FormatException(
        'No se encontró el bloque de predicciones del workflow.',
      );
    }

    final dynamic lista = bloque['predictions'];
    if (lista is! List || lista.isEmpty) {
      throw Exception(
        'Roboflow no detectó objetos en esta fotografía.',
      );
    }

    final detecciones = lista
        .whereType<Map>()
        .where((d) => d['class'] is String)
        .where((d) {
          final confianza = (d['confidence'] as num?)?.toDouble() ?? 0;
          return confianza >= _confianzaMinima;
        })
        .toList();

    if (detecciones.isEmpty) {
      throw Exception(
        'No se encontraron detecciones con confianza suficiente. '
        'Intenta tomar una fotografía más clara y cercana.',
      );
    }

    detecciones.sort((a, b) {
      final confianzaA = (a['confidence'] as num?)?.toDouble() ?? 0;
      final confianzaB = (b['confidence'] as num?)?.toDouble() ?? 0;
      return confianzaB.compareTo(confianzaA);
    });

    final mejor = detecciones.first;
    final clase = mejor['class'] as String;
    final confianza = ((mejor['confidence'] as num?)?.toDouble() ?? 0)
        .clamp(0.0, 1.0)
        .toDouble();

    final datos = _describirClase(clase);

    return Hallazgo(
      elemento: datos.elemento,
      categoria: datos.categoria,
      ubicacion: evidencia.ubicacion,
      descripcion: datos.descripcion,
      condicion: 'Requiere verificación profesional',
      observacion: evidencia.observacion,
      confianza: confianza,
      fotoPath: evidencia.fotoPath,
    );
  }

  _Descripcion _describirClase(String clase) {
    switch (clase.toLowerCase()) {
      case 'extintor':
        return const _Descripcion(
          'Extintor',
          'Equipos contra incendios',
          'El modelo detectó un posible extintor en la fotografía.',
        );
      case 'salida_emergencia':
        return const _Descripcion(
          'Señal de salida de emergencia',
          'Evacuación',
          'El modelo detectó una posible señal de salida de emergencia.',
        );
      case 'senal_extintor':
        return const _Descripcion(
          'Señal de extintor',
          'Equipos contra incendios',
          'El modelo detectó una posible señalización de extintor.',
        );
      case 'prohibido_parquear':
        return const _Descripcion(
          'Señal de prohibido parquear',
          'Señalización de seguridad',
          'El modelo detectó una posible señal de prohibido parquear.',
        );
      default:
        return _Descripcion(
          clase,
          'Seguridad y salud en el trabajo',
          'El modelo detectó el elemento "$clase". Requiere revisión profesional.',
        );
    }
  }
}

class _Descripcion {
  final String elemento;
  final String categoria;
  final String descripcion;

  const _Descripcion(
    this.elemento,
    this.categoria,
    this.descripcion,
  );
}
