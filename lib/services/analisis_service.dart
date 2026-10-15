import '../models/evidencia.dart';
import '../models/hallazgo.dart';

/// Contrato de análisis. Las pantallas solo conocen esta interfaz.
abstract class AnalisisService {
  Future<Hallazgo> analizar(Evidencia evidencia);
}
