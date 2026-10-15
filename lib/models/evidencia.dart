import 'dart:typed_data';

import 'hallazgo.dart';

class Evidencia {
  final String fotoPath;
  final Uint8List? fotoBytes;
  final String observacion;
  final String ubicacion;
  final String tipo;
  final String adicional;

  final DateTime fecha = DateTime.now();
  final List<Hallazgo> hallazgos = [];

  Evidencia({
    required this.fotoPath,
    this.fotoBytes,
    required this.observacion,
    required this.ubicacion,
    this.tipo = '',
    this.adicional = '',
  });
}
