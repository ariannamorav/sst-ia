import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

import '../utils/constants.dart';
import '../widgets/widgets.dart';
import 'evidencia_screen.dart';

class CapturaEvidenciaScreen extends StatefulWidget {
  const CapturaEvidenciaScreen({super.key});

  @override
  State<CapturaEvidenciaScreen> createState() => _CapturaEvidenciaScreenState();
}

class _CapturaEvidenciaScreenState extends State<CapturaEvidenciaScreen> {
  XFile? _foto;
  String? _error;
  bool _cargando = false;

  Future<void> _tomar() async {
    try {
      final foto = await ImagePicker().pickImage(
        source: ImageSource.camera,
        imageQuality: 85,
        maxWidth: 1600,
      );

      if (!mounted) return;

      setState(() {
        _foto = foto;
        _error = foto == null ? 'cancelada' : null;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() => _error = 'permiso');
      debugPrint('Error al capturar fotografía: $e');
    }
  }

  Future<void> _usarFoto() async {
    if (_foto == null || _cargando) return;

    setState(() => _cargando = true);

    try {
      // XFile permite leer los bytes tanto en Web como en Android.
      final bytes = await _foto!.readAsBytes();

      if (!mounted) return;

      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (_) => EvidenciaScreen(
            _foto!.path,
            fotoBytes: bytes,
          ),
        ),
      );
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _cargando = false;
        _error = 'permiso';
      });
      debugPrint('Error al leer fotografía: $e');
    }
  }

  Widget _visor() {
    if (_foto != null) return Foto(_foto!.path);

    final (icono, titulo, mensaje) = switch (_error) {
      'permiso' => (
          Icons.no_photography_outlined,
          'No se pudo acceder a la fotografía.',
          'Revisa los permisos de la cámara e inténtalo nuevamente.',
        ),
      'cancelada' => (
          Icons.photo_camera_outlined,
          'Fotografía cancelada',
          'Puedes intentarlo nuevamente.',
        ),
      _ => (
          Icons.photo_camera_outlined,
          'Captura la evidencia',
          'Encuadra la señalización y toma la fotografía.',
        ),
    };

    return Container(
      decoration: BoxDecoration(
        color: C.navy,
        borderRadius: BorderRadius.circular(14),
      ),
      child: Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(icono, color: Colors.white70, size: 56),
              const SizedBox(height: 14),
              Text(
                titulo,
                textAlign: TextAlign.center,
                style: const TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.w700,
                  fontSize: 16,
                ),
              ),
              const SizedBox(height: 6),
              Text(
                mensaje,
                textAlign: TextAlign.center,
                style: const TextStyle(color: Colors.white70),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Capturar evidencia')),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            children: [
              Expanded(
                child: SizedBox(
                  width: double.infinity,
                  child: _visor(),
                ),
              ),
              const SizedBox(height: 16),
              if (_foto == null) ...[
                AppButton(
                  'Tomar fotografía',
                  icon: Icons.photo_camera,
                  onPressed: _tomar,
                ),
                const SizedBox(height: 10),
                AppButton(
                  'Volver',
                  estilo: EstiloBoton.suave,
                  onPressed: () => Navigator.pop(context),
                ),
              ] else ...[
                AppButton(
                  _cargando
                      ? 'Preparando fotografía...'
                      : 'Usar esta fotografía',
                  icon: Icons.check,
                  onPressed: _cargando ? null : _usarFoto,
                ),
                const SizedBox(height: 10),
                AppButton(
                  'Repetir fotografía',
                  icon: Icons.refresh,
                  estilo: EstiloBoton.contorno,
                  onPressed: _cargando ? null : _tomar,
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}
