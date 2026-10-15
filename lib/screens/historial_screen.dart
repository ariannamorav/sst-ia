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
    if (soloInformes) { ir(c, InformeScreen(i)); }
    else if (i.estado == EstadoInspeccion.enCurso) { ir(c, InspeccionScreen(i), nombre: 'inspeccion'); }
    else { ir(c, HallazgosScreen(i)); }
  }

  @override
  Widget build(BuildContext context) {
    final lista = context.watch<AppState>().inspecciones;
    final titulo = soloInformes ? 'Informes' : 'Mis inspecciones';
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Padding(padding: const EdgeInsets.fromLTRB(20, 16, 20, 8), child: Text(titulo, style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w800, color: C.navy))),
      Expanded(
        child: lista.isEmpty
            ? EstadoVacio(Icons.fact_check_outlined, 'Aún no hay inspecciones', soloInformes ? 'Cuando finalices una inspección podrás generar su informe aquí.' : 'Crea tu primera inspección desde el inicio.')
            : ListView(padding: const EdgeInsets.symmetric(horizontal: 20), children: [
                for (final i in lista)
                  AppCard(
                    onTap: () => _abrir(context, i),
                    child: Row(children: [
                      Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                        Text('Inspección ${i.codigo}', style: const TextStyle(fontWeight: FontWeight.w700, color: C.navy)),
                        Text('${i.sede} · ${i.edificio}', style: const TextStyle(color: C.texto2, fontSize: 12)),
                        Text('${fFecha(i.fecha)} · ${i.hallazgos.length} hallazgos', style: const TextStyle(color: C.texto2, fontSize: 12)),
                      ])),
                      i.estado == EstadoInspeccion.enCurso ? const StatusBadge('En curso', C.azul) : const StatusBadge('Finalizada', C.verde),
                      const Icon(Icons.chevron_right, color: C.texto2),
                    ]),
                  ),
              ]),
      ),
    ]);
  }
}
