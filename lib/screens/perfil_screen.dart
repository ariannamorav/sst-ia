import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/app_state.dart';
import '../utils/constants.dart';
import '../widgets/widgets.dart';
import 'dataset_screen.dart';

class PerfilScreen extends StatelessWidget {
  const PerfilScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final nombre = context.watch<AppState>().profesional;

    Widget fila(IconData i, String t, String s, {VoidCallback? onTap}) => AppCard(
          onTap: onTap,
          child: Row(
            children: [
              Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: C.azul.withValues(alpha: 0.1),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Icon(i, color: C.azul),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(t, style: const TextStyle(fontWeight: FontWeight.w700, color: C.navy, fontSize: 13.5)),
                    const SizedBox(height: 2),
                    Text(s, style: const TextStyle(fontSize: 12, color: C.texto2)),
                  ],
                ),
              ),
              if (onTap != null) const Icon(Icons.chevron_right, color: C.texto2),
            ],
          ),
        );

    return Center(
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 800),
        child: ListView(
          padding: const EdgeInsets.all(24),
          children: [
            const Text('Perfil Profesional y Configuración',
                style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800, color: C.navy)),
            const SizedBox(height: 16),
            AppCard(
              child: Row(
                children: [
                  const CircleAvatar(
                    radius: 28,
                    backgroundColor: Color(0xFFE8F1FF),
                    child: Icon(Icons.person, color: C.azul, size: 30),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(nombre,
                            style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 17, color: C.navy)),
                        const SizedBox(height: 2),
                        const Text('Auditor Especialista SST · Politécnico Grancolombiano',
                            style: TextStyle(color: C.texto2, fontSize: 12.5)),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 10),
            fila(
              Icons.model_training,
              'Gestión de Datasets y Modelo YOLOv8',
              'Entrenamiento de modelos con cURL de Roboflow y pesos sst_best.pt.',
              onTap: () => ir(context, const DatasetScreen()),
            ),
            fila(
              Icons.verified_outlined,
              'Gobernanza Ética y Validación Humana',
              'El modelo propone la señal y la norma; el profesional SST valida o edita el dictamen final.',
            ),
            fila(
              Icons.gavel_outlined,
              'Marco Normativo Colombiano',
              'Conforme a NTC 1461, Res. 2400/1979, NSR-10 (Títulos J y K) y Dec. 1072/2015.',
            ),
            fila(
              Icons.info_outline,
              'SST-IA v2.0.0 (FastAPI + YOLOv8 + Flutter Web)',
              'Inspecciones técnicas inteligentes, espacios más seguros.',
            ),
          ],
        ),
      ),
    );
  }
}
