enum EstadoHallazgo { validado, pendiente, rechazado }

class Hallazgo {
  String elemento, categoria, ubicacion, descripcion, condicion, observacion;
  double confianza; // 0..1
  EstadoHallazgo estado;
  final DateTime fecha;
  final String? fotoPath;

  Hallazgo({
    required this.elemento, required this.categoria, required this.ubicacion,
    required this.descripcion, required this.condicion, required this.observacion,
    required this.confianza, this.estado = EstadoHallazgo.pendiente, this.fotoPath, DateTime? fecha,
  }) : fecha = fecha ?? DateTime.now();
}
