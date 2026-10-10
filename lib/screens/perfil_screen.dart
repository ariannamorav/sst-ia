import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/app_state.dart';
import '../utils/constants.dart';
import '../widgets/widgets.dart';

class PerfilScreen extends StatelessWidget {
  const PerfilScreen({super.key});
  @override
  Widget build(BuildContext context) {
    final nombre = context.watch<AppState>().profesional;
    Widget fila(IconData i, String t, String s) => AppCard(child: Row(children: [Icon(i, color: C.azul), const SizedBox(width: 14), Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [Text(t, style: const TextStyle(fontWeight: FontWeight.w700, color: C.navy)), Text(s, style: const TextStyle(fontSize: 12, color: C.texto2))]))]));
    return ListView(padding: const EdgeInsets.all(20), children: [
      const Text('Perfil', style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800, color: C.navy)),
      const SizedBox(height: 16),
      AppCard(child: Row(children: [
        const CircleAvatar(radius: 26, backgroundColor: Color(0xFFE8F1FF), child: Icon(Icons.person, color: C.azul)), const SizedBox(width: 14),
        Column(crossAxisAlignment: CrossAxisAlignment.start, children: [Text(nombre, style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 16, color: C.navy)), const Text('Profesional de SST', style: TextStyle(color: C.texto2))]),
      ])),
      fila(Icons.cloud_off_outlined, 'Modo local', 'Todos los datos permanecen en este dispositivo. No requiere Internet.'),
      fila(Icons.auto_awesome, 'Asistente de análisis', 'IA simulada. La IA propone; el profesional revisa y decide.'),
      fila(Icons.info_outline, 'SST-IA v1.0.0', 'Inspecciones más simples, espacios más seguros.'),
    ]);
  }
}
