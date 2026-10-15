import '../models/evidencia.dart';
import '../models/hallazgo.dart';
import 'analisis_service.dart';

/// IA simulada 100% local: reglas por palabras clave, sin Internet.
/// TODO: reemplazar por ServicioAnalisisGemini en main.dart (sin tocar pantallas).
class ServicioAnalisisSimulado implements AnalisisService {
  static const _reglas = [
    _Regla(['extintor', 'incendio', 'contra incendios'], 'Señal de extintor', 'Equipos contra incendios', 'Requiere verificación',
        'Se identifica una señal asociada a la ubicación de un equipo contra incendios.', .92),
    _Regla(['salida', 'evacuacion', 'emergencia'], 'Señal de evacuación', 'Evacuación', 'Conforme',
        'Se identifica señalización asociada a una ruta o salida de evacuación.', .95),
    _Regla(['prohibido', 'prohibicion', 'no fumar'], 'Señal de prohibición', 'Prohibición', 'Requiere revisión',
        'Se identifica una señal de prohibición en el área inspeccionada.', .94),
    _Regla(['riesgo', 'peligro', 'electrico', 'advertencia'], 'Señal de advertencia', 'Advertencia', 'Requiere atención',
        'Se identifica una señal de advertencia relacionada con un posible riesgo.', .89),
    _Regla(['obligatorio', 'obligacion', 'proteccion'], 'Señal de obligación', 'Obligación', 'Conforme',
        'Se identifica una señal que comunica una acción o condición de cumplimiento obligatorio.', .91),
  ];

  @override
  Future<Hallazgo> analizar(Evidencia e) async {
    await Future.delayed(const Duration(milliseconds: 1500)); // procesamiento simulado
    final texto = _normalizar('${e.observacion} ${e.tipo} ${e.adicional}');
    final r = _reglas.firstWhere((r) => r.claves.any(texto.contains),
        orElse: () => const _Regla([], 'Señal de seguridad', 'General', 'Requiere revisión',
            'Se identifica un elemento de señalización de seguridad que requiere revisión por parte del profesional.', .80));
    return Hallazgo(
      elemento: r.elemento, categoria: r.categoria, ubicacion: e.ubicacion, descripcion: r.descripcion,
      condicion: r.condicion, observacion: e.observacion, confianza: r.confianza, fotoPath: e.fotoPath,
    );
  }

  String _normalizar(String s) {
    const de = 'áéíóúü', a = 'aeiouu';
    var t = s.toLowerCase();
    for (var i = 0; i < de.length; i++) { t = t.replaceAll(de[i], a[i]); }
    return t;
  }
}

class _Regla {
  final List<String> claves;
  final String elemento, categoria, condicion, descripcion;
  final double confianza;
  const _Regla(this.claves, this.elemento, this.categoria, this.condicion, this.descripcion, this.confianza);
}
