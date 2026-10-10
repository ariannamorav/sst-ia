import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../utils/constants.dart';
import '../widgets/widgets.dart';
import 'evidencia_screen.dart';

/// Usa la cámara real del teléfono (image_picker).
class CapturaEvidenciaScreen extends StatefulWidget {
  const CapturaEvidenciaScreen({super.key});
  @override
  State<CapturaEvidenciaScreen> createState() => _CapturaEvidenciaScreenState();
}

class _CapturaEvidenciaScreenState extends State<CapturaEvidenciaScreen> {
  String? _foto;
  String? _error; // 'cancelada' | 'permiso'

  Future<void> _tomar() async {
    try {
      final x = await ImagePicker().pickImage(source: ImageSource.camera, imageQuality: 85, maxWidth: 1600);
      setState(() { _foto = x?.path; _error = x == null ? 'cancelada' : null; });
    } catch (_) {
      setState(() => _error = 'permiso');
    }
  }

  Widget _visor() {
    if (_foto != null) return Foto(_foto);
    final (icono, t, m) = switch (_error) {
      'permiso' => (Icons.no_photography_outlined, 'No tenemos acceso a la cámara.', 'Puedes habilitar el permiso desde la configuración del dispositivo.'),
      'cancelada' => (Icons.photo_camera_outlined, 'Fotografía cancelada', 'No se tomó ninguna fotografía. Puedes intentarlo nuevamente.'),
      _ => (Icons.photo_camera_outlined, 'Captura la evidencia', 'Encuadra la señalización y toma la fotografía.'),
    };
    return Container(
        decoration: BoxDecoration(color: C.navy, borderRadius: BorderRadius.circular(14)),
        child: Center(child: Padding(padding: const EdgeInsets.all(24), child: Column(mainAxisSize: MainAxisSize.min, children: [
          Icon(icono, color: Colors.white70, size: 56), const SizedBox(height: 14),
          Text(t, textAlign: TextAlign.center, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w700, fontSize: 16)),
          const SizedBox(height: 6), Text(m, textAlign: TextAlign.center, style: const TextStyle(color: Colors.white70)),
        ]))));
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(title: const Text('Capturar evidencia')),
        body: SafeArea(child: Padding(padding: const EdgeInsets.all(20), child: Column(children: [
          Expanded(child: SizedBox(width: double.infinity, child: _visor())),
          const SizedBox(height: 16),
          if (_foto == null) ...[
            AppButton('Tomar fotografía', icon: Icons.photo_camera, onPressed: _tomar),
            const SizedBox(height: 10),
            AppButton('Volver', estilo: EstiloBoton.suave, onPressed: () => Navigator.pop(context)),
          ] else ...[
            AppButton('Usar esta fotografía', icon: Icons.check, onPressed: () => Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => EvidenciaScreen(_foto!)))),
            const SizedBox(height: 10),
            AppButton('Repetir fotografía', icon: Icons.refresh, estilo: EstiloBoton.contorno, onPressed: _tomar),
          ],
        ]))),
      );
}
