import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/inspeccion.dart';
import '../services/app_state.dart';
import '../utils/constants.dart';
import '../widgets/widgets.dart';
import 'captura_evidencia_screen.dart';
import 'hallazgos_screen.dart';
import 'informe_screen.dart';

class InspeccionScreen extends StatelessWidget {
  final Inspeccion insp;
  const InspeccionScreen(this.insp, {super.key});

  Widget _fila(IconData i, String k, String v) => Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(children: [Icon(i, size: 16, color: C.texto2), const SizedBox(width: 8), SizedBox(width: 90, child: Text('$k:', style: const TextStyle(color: C.texto2, fontSize: 12))), Expanded(child: Text(v, style: const TextStyle(fontSize: 13, color: C.navy)))]));

  Future<void> _finalizar(BuildContext context) async {
    final ok = await showDialog<bool>(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text('¿Deseas finalizar esta inspección?'),
        content: Text(insp.hallazgos.isEmpty
            ? 'Esta inspección aún no tiene hallazgos registrados. Una vez finalizada podrás generar el informe.'
            : 'Una vez finalizada podrás generar el informe.'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context, false), child: const Text('Cancelar')),
          TextButton(onPressed: () => Navigator.pop(context, true), child: const Text('Finalizar inspección')),
        ],
      ),
    );
    if (ok == true && context.mounted) {
      context.read<AppState>().finalizar();
      Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => InformeScreen(insp)));
    }
  }

  @override
  Widget build(BuildContext context) {
    context.watch<AppState>();
    return Scaffold(
      appBar: AppBar(title: const Text('Inspección en curso')),
      body: contenido([
        AppCard(child: Column(children: [
          Row(children: [Text('Inspección ${insp.codigo}', style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 16, color: C.navy)), const Spacer(), const StatusBadge('En curso', C.verde)]),
          const SizedBox(height: 8),
          _fila(Icons.location_on_outlined, 'Sede', insp.sede), _fila(Icons.apartment, 'Edificio', insp.edificio), _fila(Icons.layers_outlined, 'Área', insp.area),
          _fila(Icons.event, 'Fecha', '${fFecha(insp.fecha)} - ${fHora(insp.fecha)}'), _fila(Icons.person_outline, 'Responsable', insp.responsable),
        ])),
        AppCard(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          const Text('Hallazgos registrados', style: TextStyle(fontWeight: FontWeight.w700)),
          Row(children: [
            Text('${insp.hallazgos.length}', style: const TextStyle(fontSize: 32, fontWeight: FontWeight.w800, color: C.navy)), const Spacer(),
            TextButton(onPressed: () => ir(context, HallazgosScreen(insp)), child: const Text('Ver detalles >')),
          ]),
        ])),
        const SizedBox(height: 8),
        AppButton('Capturar nuevo hallazgo', icon: Icons.photo_camera_outlined, onPressed: () => ir(context, const CapturaEvidenciaScreen())),
        const SizedBox(height: 10),
        AppButton('Ver hallazgos registrados', icon: Icons.checklist, estilo: EstiloBoton.contorno, onPressed: () => ir(context, HallazgosScreen(insp))),
        const SizedBox(height: 28),
        AppButton('Finalizar inspección', estilo: EstiloBoton.peligro, onPressed: () => _finalizar(context)),
      ]),
    );
  }
}
