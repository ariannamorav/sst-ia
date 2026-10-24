import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/inspeccion.dart';
import '../services/app_state.dart';
import '../utils/constants.dart';
import '../widgets/widgets.dart';
import 'hallazgos_screen.dart';
import 'informe_screen.dart';
import 'inspeccion_screen.dart';

/// Historial ("Mis inspecciones"). Con soloInformes se usa como pestaña Informes.
class HistorialScreen extends StatelessWidget {
  final bool soloInformes;
  const HistorialScreen({super.key, this.soloInformes = false});

  void _abrir(BuildContext c, Inspeccion i) {
    c.read<AppState>().abrir(i);
    if (soloInformes) {
      ir(c, InformeScreen(i));
    } else if (i.estado == EstadoInspeccion.enCurso) {
      ir(c, InspeccionScreen(i), nombre: 'inspeccion');
    } else {
      ir(c, HallazgosScreen(i));
    }
  }

  @override
  Widget build(BuildContext context) {
    final lista = context.watch<AppState>().inspecciones;
    final titulo = soloInformes ? 'Informes Periciales de Auditoría' : 'Historial de Inspecciones SST';

    return Center(
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 1000),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(24, 20, 24, 12),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    titulo,
                    style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w800, color: C.navy),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    soloInformes
                        ? 'Consulta y exporta los informes técnicos validados de cada recorrido.'
                        : 'Gestiona los recorridos técnicos en curso y finalizados en las distintas sedes.',
                    style: const TextStyle(color: C.texto2, fontSize: 13),
                  ),
                ],
              ),
            ),
            Expanded(
              child: lista.isEmpty
                  ? Center(
                      child: EstadoVacio(
                        Icons.fact_check_outlined,
                        'Aún no hay inspecciones registradas',
                        soloInformes
                            ? 'Cuando completes una inspección y valides sus hallazgos, podrás generar su informe PDF oficial aquí.'
                            : 'Inicia un nuevo recorrido desde la pantalla de Inicio para registrar evidencias.',
                      ),
                    )
                  : ListView(
                      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 8),
                      children: [
                        for (final i in lista)
                          AppCard(
                            onTap: () => _abrir(context, i),
                            child: Row(
                              children: [
                                Container(
                                  padding: const EdgeInsets.all(12),
                                  decoration: BoxDecoration(
                                    color: (i.estado == EstadoInspeccion.enCurso ? C.azul : C.verde).withValues(alpha: 0.1),
                                    borderRadius: BorderRadius.circular(10),
                                  ),
                                  child: Icon(
                                    soloInformes ? Icons.picture_as_pdf : Icons.assignment_outlined,
                                    color: i.estado == EstadoInspeccion.enCurso ? C.azul : C.verde,
                                    size: 24,
                                  ),
                                ),
                                const SizedBox(width: 16),
                                Expanded(
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        'Inspección ${i.codigo} · ${i.sede}',
                                        style: const TextStyle(fontWeight: FontWeight.w700, color: C.navy, fontSize: 14),
                                      ),
                                      const SizedBox(height: 2),
                                      Text('${i.edificio} — ${i.area}',
                                          style: const TextStyle(color: C.texto2, fontSize: 12)),
                                      const SizedBox(height: 2),
                                      Text(
                                        '${fFecha(i.fecha)} · ${i.hallazgos.length} hallazgos (${i.validados.length} validados)',
                                        style: const TextStyle(color: C.texto2, fontSize: 11.5),
                                      ),
                                    ],
                                  ),
                                ),
                                i.estado == EstadoInspeccion.enCurso
                                    ? const StatusBadge('En curso', C.azul)
                                    : const StatusBadge('Finalizada', C.verde),
                                const SizedBox(width: 8),
                                const Icon(Icons.chevron_right, color: C.texto2),
                              ],
                            ),
                          ),
                      ],
                    ),
            ),
          ],
        ),
      ),
    );
  }
}
