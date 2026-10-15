import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/evidencia.dart';
import '../models/hallazgo.dart';
import '../services/app_state.dart';
import '../utils/constants.dart';
import '../widgets/widgets.dart';
import 'revisar_hallazgo_screen.dart';

class ResultadoIAScreen extends StatelessWidget {
  final Evidencia evidencia;
  final Hallazgo hallazgo;
  const ResultadoIAScreen(this.evidencia, this.hallazgo, {super.key});

  void _rechazar(BuildContext context) {
    hallazgo.estado = EstadoHallazgo.rechazado;
    context.read<AppState>().guardarHallazgo(evidencia, hallazgo);
    ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Hallazgo rechazado. No se incluirá en el informe.')));
    Navigator.popUntil(context, (r) => r.settings.name == 'inspeccion');
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(title: const Text('Resultado de IA'), actions: const [Padding(padding: EdgeInsets.only(right: 14), child: StatusBadge('Preliminar', C.azul))]),
        body: contenido([
          Foto(hallazgo.fotoPath, height: 150),
          const Etiqueta('Identificación preliminar'),
          Dato('Elemento', hallazgo.elemento), Dato('Categoría', hallazgo.categoria), Dato('Ubicación', hallazgo.ubicacion),
          Dato('Descripción', hallazgo.descripcion), Dato('Condición', hallazgo.condicion),
          ConfidenceBar(hallazgo.confianza),
          const SizedBox(height: 14), const AvisoPreliminar(), const SizedBox(height: 16),
          Row(children: [
            Expanded(child: AppButton('Rechazar', estilo: EstiloBoton.peligro, onPressed: () => _rechazar(context))), const SizedBox(width: 12),
            Expanded(child: AppButton('Continuar', onPressed: () => ir(context, RevisarHallazgoScreen(evidencia, hallazgo)))),
          ]),
        ]),
      );
}
