import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';
import '../models/evidencia.dart';
import '../models/hallazgo.dart';
import 'analisis_service.dart';
import 'analisis_simulado_service.dart';

/// Servicio que conecta Flutter con el Backend de Python (YOLO + Datasets de Roboflow).
/// Compatible con Flutter Web, Windows Desktop, Android e iOS.
class ServicioAnalisisIAService implements AnalisisService {
  final ServicioAnalisisSimulado _fallback = ServicioAnalisisSimulado();

  String get _urlServidor {
    // Si corre en emulador Android usa 10.0.2.2, si corre en Windows/Web/iOS usa localhost
    if (!kIsWeb && defaultTargetPlatform == TargetPlatform.android) {
      return 'http://10.0.2.2:5000/analizar';
    }
    return 'http://127.0.0.1:5000/analizar';
  }

  @override
  Future<Hallazgo> analizar(Evidencia e) async {
    try {
      String fotoB64 = '';
      if (e.fotoPath.isNotEmpty) {
        final bytes = await XFile(e.fotoPath).readAsBytes();
        fotoB64 = base64Encode(bytes);
      }

      if (fotoB64.isEmpty) {
        return _fallback.analizar(e);
      }

      final payload = jsonEncode({
        'foto_base64': fotoB64,
        'observacion': e.observacion,
        'ubicacion': e.ubicacion,
        'tipo': e.tipo,
        'adicional': e.adicional,
      });

      final resp = await http.post(
        Uri.parse(_urlServidor),
        headers: {'Content-Type': 'application/json; charset=utf-8'},
        body: payload,
      ).timeout(const Duration(seconds: 15));

      if (resp.statusCode == 200) {
        final data = jsonDecode(utf8.decode(resp.bodyBytes)) as Map<String, dynamic>;

        return Hallazgo(
          elemento: data['elemento'] ?? 'Señal de Seguridad',
          categoria: data['categoria'] ?? 'General',
          ubicacion: data['ubicacion'] ?? e.ubicacion,
          descripcion: data['descripcion'] ?? '',
          condicion: data['condicion'] ?? 'Requiere verificación',
          observacion: e.observacion,
          confianza: (data['confianza'] as num?)?.toDouble() ?? 0.90,
          fotoPath: e.fotoPath,
          estado: EstadoHallazgo.pendiente,
        );
      } else {
        debugPrint('[SST-IA] Servidor retornó código ${resp.statusCode}, usando fallback.');
        return _fallback.analizar(e);
      }
    } catch (err) {
      debugPrint('[SST-IA] Servidor Python desconectado ($err). Usando fallback local.');
      return _fallback.analizar(e);
    }
  }
}
