import 'package:flutter/foundation.dart';
import '../models/evidencia.dart';
import '../models/hallazgo.dart';
import '../models/inspeccion.dart';

/// Estado en memoria. TODO: persistir con SharedPreferences/SQLite o Supabase
/// reemplazando solo esta clase (las pantallas no cambian).
class AppState extends ChangeNotifier {
  final String profesional = 'Alejandro Torres';
  final List<Inspeccion> inspecciones = [];
  Inspeccion? actual;

  Inspeccion crear({required DateTime fecha, required String sede, required String edificio, required String area, required String responsable}) {
    final i = Inspeccion(numero: inspecciones.length + 1, fecha: fecha, sede: sede, edificio: edificio, area: area, responsable: responsable);
    inspecciones.insert(0, i);
    actual = i;
    notifyListeners();
    return i;
  }

  void abrir(Inspeccion i) { actual = i; notifyListeners(); }

  void guardarHallazgo(Evidencia e, Hallazgo h) {
    if (!actual!.evidencias.contains(e)) actual!.evidencias.add(e);
    if (!e.hallazgos.contains(h)) e.hallazgos.add(h);
    notifyListeners();
  }

  void finalizar() { actual!.estado = EstadoInspeccion.finalizada; notifyListeners(); }
  void notificar() => notifyListeners();
}
