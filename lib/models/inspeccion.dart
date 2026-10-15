import 'evidencia.dart';
import 'hallazgo.dart';

enum EstadoInspeccion { enCurso, finalizada }

class Inspeccion {
  final int numero;
  final DateTime fecha;
  final String sede, edificio, area, responsable;
  EstadoInspeccion estado = EstadoInspeccion.enCurso;
  final List<Evidencia> evidencias = [];

  Inspeccion({required this.numero, required this.fecha, required this.sede, required this.edificio, required this.area, required this.responsable});

  String get codigo => '#${numero.toString().padLeft(4, '0')}';
  List<Hallazgo> get hallazgos => evidencias.expand((e) => e.hallazgos).toList();
  List<Hallazgo> get validados => hallazgos.where((h) => h.estado == EstadoHallazgo.validado).toList();
}
