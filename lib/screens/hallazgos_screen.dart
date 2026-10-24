import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/hallazgo.dart';
import '../models/inspeccion.dart';
import '../services/app_state.dart';
import '../utils/constants.dart';
import '../widgets/widgets.dart';
import 'informe_screen.dart';
import 'revisar_hallazgo_screen.dart';

class HallazgosScreen extends StatelessWidget {
  final Inspeccion insp;
  const HallazgosScreen(this.insp, {super.key});

  Widget _stat(String n, String l, Color c) => Expanded(
      child: Container(margin: const EdgeInsets.symmetric(horizontal: 4), padding: const EdgeInsets.symmetric(vertical: 12),
          decoration: BoxDecoration(color: c.withValues(alpha: .08), borderRadius: BorderRadius.circular(12)),
          child: Column(children: [Text(n, style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800, color: c)), Text(l, style: const TextStyle(fontSize: 12, color: C.texto2))])));

  @override
  Widget build(BuildContext context) {
    context.watch<AppState>();
    final lista = insp.hallazgos;
    int n(EstadoHallazgo e) => lista.where((h) => h.estado == e).length;
    return Scaffold(
      appBar: AppBar(title: const Text('Hallazgos de la inspección')),
      body: lista.isEmpty
          ? const EstadoVacio(Icons.inbox_outlined, 'Inspección sin hallazgos', 'Aún no se han registrado hallazgos. Captura una evidencia para comenzar.')
          : SafeArea(child: ListView(padding: const EdgeInsets.all(20), children: [
              Row(children: [_stat('${lista.length}', 'Total', C.navy), _stat('${n(EstadoHallazgo.validado)}', 'Validados', C.verde), _stat('${n(EstadoHallazgo.pendiente)}', 'Pendientes', C.naranja)]),
              const SizedBox(height: 14),
              for (final e in insp.evidencias)
                for (final h in e.hallazgos) FindingCard(h, onTap: () => ir(context, RevisarHallazgoScreen(e, h))),
            ])),
      bottomNavigationBar: SafeArea(child: Padding(padding: const EdgeInsets.all(16), child: AppButton('Generar informe', icon: Icons.description_outlined, onPressed: () => ir(context, InformeScreen(insp))))),
    );
  }
}
