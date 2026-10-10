import 'hallazgo.dart';

class Evidencia {
  final String fotoPath;
  final String observacion, ubicacion, tipo, adicional;
  final DateTime fecha = DateTime.now();
  final List<Hallazgo> hallazgos = [];
  Evidencia({required this.fotoPath, required this.observacion, required this.ubicacion, this.tipo = '', this.adicional = ''});
}
