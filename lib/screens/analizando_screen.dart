import 'dart:async';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/evidencia.dart';
import '../services/analisis_service.dart';
import '../utils/constants.dart';
import '../widgets/widgets.dart';
import 'resultado_ia_screen.dart';

class AnalizandoScreen extends StatefulWidget {
  final Evidencia evidencia;
  const AnalizandoScreen(this.evidencia, {super.key});
  @override
  State<AnalizandoScreen> createState() => _AnalizandoScreenState();
}

class _AnalizandoScreenState extends State<AnalizandoScreen> {
  static const _pasos = ['Procesando fotografía', 'Identificando señalización', 'Analizando información', 'Generando propuesta'];
  int _paso = 0;
  Timer? _timer;
  bool _error = false;

  @override
  void initState() {
    super.initState();
    _timer = Timer.periodic(const Duration(milliseconds: 600), (_) { if (_paso < _pasos.length - 1 && mounted) setState(() => _paso++); });
    _correr();
  }

  Future<void> _correr() async {
    setState(() => _error = false);
    try {
      // La pantalla solo conoce AnalisisService; no sabe qué IA hay detrás.
      final r = await Future.wait([context.read<AnalisisService>().analizar(widget.evidencia), Future.delayed(const Duration(milliseconds: 2400))]);
      if (!mounted) return;
      Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => ResultadoIAScreen(widget.evidencia, r[0] as dynamic)));
    } catch (_) {
      if (mounted) setState(() => _error = true);
    }
  }

  @override
  void dispose() { _timer?.cancel(); super.dispose(); }

  @override
  Widget build(BuildContext context) => Scaffold(
        backgroundColor: C.navy,
        body: SafeArea(
          child: _error
              ? Padding(padding: const EdgeInsets.all(24), child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
                  const Icon(Icons.error_outline, color: Colors.white, size: 54), const SizedBox(height: 14),
                  const Text('No pudimos analizar la evidencia', style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.w700)),
                  const SizedBox(height: 20), AppButton('Reintentar', onPressed: _correr),
                  const SizedBox(height: 10), AppButton('Volver', estilo: EstiloBoton.suave, onPressed: () => Navigator.pop(context)),
                ]))
              : Padding(padding: const EdgeInsets.all(28), child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
                  const Icon(Icons.cloud_sync_outlined, color: Colors.white, size: 80), const SizedBox(height: 18),
                  const Text('Analizando evidencia...', style: TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.w800)),
                  const SizedBox(height: 28),
                  for (var i = 0; i < _pasos.length; i++)
                    Padding(padding: const EdgeInsets.symmetric(vertical: 7), child: Row(children: [
                      Icon(i < _paso ? Icons.check_circle : Icons.radio_button_unchecked, color: i < _paso ? C.verde : Colors.white54),
                      const SizedBox(width: 12), Text(_pasos[i], style: TextStyle(color: i <= _paso ? Colors.white : Colors.white54, fontSize: 15)),
                    ])),
                  const SizedBox(height: 20),
                  ClipRRect(borderRadius: BorderRadius.circular(6), child: LinearProgressIndicator(value: (_paso + 1) / _pasos.length, minHeight: 6, color: const Color(0xFF3DA5FF), backgroundColor: Colors.white24)),
                  const SizedBox(height: 28),
                  const Text('Este proceso puede tardar unos segundos.', style: TextStyle(color: Colors.white60)),
                ])),
        ),
      );
}
