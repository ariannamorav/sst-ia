import 'dart:typed_data';
import 'package:flutter/foundation.dart';
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
  bool _cargando = true;

  @override
  void initState() {
    super.initState();
    _generar();
  }

  Future<void> _generar() async {
    setState(() {
      _error = false;
      _cargando = true;
    });
    try {
      final b = await PdfService().generar(widget.insp);
      if (mounted) {
        setState(() {
          _pdf = b;
          _cargando = false;
        });
      }
    } catch (_) {
      if (mounted) {
        setState(() {
          _error = true;
          _cargando = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final sinHallazgos = widget.insp.validados.isEmpty;

    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: const Text('Informe Pericial de Auditoría SST'),
        backgroundColor: Colors.white,
        foregroundColor: C.navy,
        elevation: 0.5,
      ),
      body: SafeArea(
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 680),
            child: _error
                ? Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const EstadoVacio(
                        Icons.error_outline,
                        'No pudimos generar el informe',
                        'Ocurrió un problema de conexión con el generador de PDF. Inténtalo nuevamente.',
                        color: C.rojo,
                      ),
                      Padding(
                        padding: const EdgeInsets.all(20),
                        child: AppButton('Reintentar Generación', onPressed: _generar),
                      ),
                    ],
                  )
                : _cargando
                    ? const Center(
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            CircularProgressIndicator(),
                            SizedBox(height: 16),
                            Text(
                              'Compilando informe pericial en PDF con ReportLab...',
                              style: TextStyle(color: C.texto2, fontSize: 13),
                            ),
                          ],
                        ),
                      )
                    : SingleChildScrollView(
                        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 32),
                        child: Container(
                          padding: const EdgeInsets.all(28),
                          decoration: BoxDecoration(
                            color: Colors.white,
                            borderRadius: BorderRadius.circular(16),
                            border: Border.all(color: const Color(0xFFE2E8F0)),
                            boxShadow: const [
                              BoxShadow(color: Color(0x08000000), blurRadius: 12, offset: Offset(0, 4))
                            ],
                          ),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.center,
                            children: [
                              Icon(
                                sinHallazgos ? Icons.info_outline : Icons.task_alt,
                                size: 72,
                                color: sinHallazgos ? C.naranja : C.verde,
                              ),
                              const SizedBox(height: 16),
                              Text(
                                sinHallazgos
                                    ? 'Informe Preliminar Sin Hallazgos'
                                    : 'Informe Pericial Generado Exitosamente',
                                textAlign: TextAlign.center,
                                style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w800, color: C.navy),
                              ),
                              const SizedBox(height: 8),
                              const Text(
                                'El documento oficial de auditoría técnica ha sido compilado conforme a NTC 1461, NSR-10, Res. 2400/79 y estándar APA 7ma edición.',
                                textAlign: TextAlign.center,
                                style: TextStyle(color: C.texto2, fontSize: 13, height: 1.35),
                              ),
                              const SizedBox(height: 16),
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                                decoration: BoxDecoration(
                                  color: const Color(0xFFEFF6FF),
                                  borderRadius: BorderRadius.circular(8),
                                  border: Border.all(color: const Color(0xFFBFDBFE)),
                                ),
                                child: Row(
                                  mainAxisSize: MainAxisSize.min,
                                  children: [
                                    const Icon(Icons.picture_as_pdf, color: C.azul, size: 18),
                                    const SizedBox(width: 8),
                                    Text(
                                      'Tamaño: ${((_pdf?.length ?? 0) / 1024).round()} KB · Motor Oficial ReportLab',
                                      style: const TextStyle(
                                          fontSize: 12, fontWeight: FontWeight.w600, color: Color(0xFF1E3A8A)),
                                    ),
                                  ],
                                ),
                              ),
                              const SizedBox(height: 28),
                              AppButton(
                                'Visualizar e Imprimir Informe PDF',
                                icon: Icons.visibility_outlined,
                                onPressed: () => Printing.layoutPdf(
                                  onLayout: (_) async => _pdf!,
                                  name: 'Informe_SST_${widget.insp.codigo}',
                                ),
                              ),
                              const SizedBox(height: 12),
                              AppButton(
                                'Compartir / Exportar Archivo',
                                icon: Icons.share,
                                estilo: EstiloBoton.contorno,
                                onPressed: () => Printing.sharePdf(
                                  bytes: _pdf!,
                                  filename: 'Informe_SST-IA_${widget.insp.codigo.replaceAll('#', '')}.pdf',
                                ),
                              ),
                              const SizedBox(height: 12),
                              AppButton(
                                'Volver al Inicio',
                                icon: Icons.home_outlined,
                                estilo: EstiloBoton.suave,
                                onPressed: () => Navigator.popUntil(context, (r) => r.isFirst),
                              ),
                            ],
                          ),
                        ),
                      ),
          ),
        ),
      ),
    );
  }
}
