import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:printing/printing.dart';
import '../models/inspeccion.dart';
import '../services/pdf_service.dart';
import '../utils/constants.dart';
import '../widgets/widgets.dart';

class InformeScreen extends StatefulWidget {
  final Inspeccion insp;
  const InformeScreen(this.insp, {super.key});
  @override
  State<InformeScreen> createState() => _InformeScreenState();
}

class _InformeScreenState extends State<InformeScreen> {
  Uint8List? _pdf;
  bool _error = false;

  @override
  void initState() { super.initState(); _generar(); }

  Future<void> _generar() async {
    setState(() => _error = false);
    try {
      final b = await PdfService().generar(widget.insp);
      if (mounted) setState(() => _pdf = b);
    } catch (_) {
      if (mounted) setState(() => _error = true);
    }
  }

  @override
  Widget build(BuildContext context) {
    final sinHallazgos = widget.insp.validados.isEmpty;
    return Scaffold(
      appBar: AppBar(title: const Text('Informe de inspección')),
      body: SafeArea(
        child: _error
            ? Column(children: [
                const Expanded(child: EstadoVacio(Icons.error_outline, 'No pudimos generar el informe', 'Ocurrió un problema al crear el documento. Inténtalo nuevamente.', color: C.rojo)),
                Padding(padding: const EdgeInsets.all(20), child: AppButton('Reintentar', onPressed: _generar)),
              ])
            : _pdf == null
                ? const Center(child: CircularProgressIndicator())
                : Padding(padding: const EdgeInsets.all(24), child: Column(children: [
                    const Spacer(),
                    Icon(sinHallazgos ? Icons.info_outline : Icons.task_alt, size: 84, color: sinHallazgos ? C.naranja : C.verde),
                    const SizedBox(height: 18),
                    Text(sinHallazgos ? 'Informe sin hallazgos validados' : 'Informe generado correctamente', textAlign: TextAlign.center, style: const TextStyle(fontSize: 24, fontWeight: FontWeight.w800, color: C.navy)),
                    const SizedBox(height: 8),
                    Text(sinHallazgos ? 'Aún no hay hallazgos validados; el informe se generó sin hallazgos.' : 'El informe en formato PDF ha sido creado con los hallazgos validados de la inspección.', textAlign: TextAlign.center, style: const TextStyle(color: C.texto2)),
                    const Spacer(),
                    AppButton('Ver informe PDF', icon: Icons.visibility_outlined, onPressed: () => Printing.layoutPdf(onLayout: (_) async => _pdf!, name: 'Informe_SST-IA_${widget.insp.codigo}')),
                    const SizedBox(height: 10),
                    AppButton('Compartir', icon: Icons.share, estilo: EstiloBoton.contorno, onPressed: () => Printing.sharePdf(bytes: _pdf!, filename: 'Informe_SST-IA_${widget.insp.numero}.pdf')),
                    const SizedBox(height: 10),
                    AppButton('Volver al inicio', icon: Icons.home_outlined, estilo: EstiloBoton.suave, onPressed: () => Navigator.popUntil(context, (r) => r.isFirst)),
                  ])),
      ),
    );
  }
}
