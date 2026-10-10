import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/app_state.dart';
import '../utils/constants.dart';
import '../widgets/widgets.dart';
import 'historial_screen.dart';
import 'nueva_inspeccion_screen.dart';
import 'perfil_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});
  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _tab = 0;
  @override
  Widget build(BuildContext context) {
    final tabs = [_Inicio(irA: (i) => setState(() => _tab = i)), const HistorialScreen(), const HistorialScreen(soloInformes: true), const PerfilScreen()];
    return Scaffold(
      body: SafeArea(child: IndexedStack(index: _tab, children: tabs)),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _tab, onDestinationSelected: (i) => setState(() => _tab = i),
        backgroundColor: Colors.white, indicatorColor: const Color(0xFFE3EEFF),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home, color: C.azul), label: 'Inicio'),
          NavigationDestination(icon: Icon(Icons.fact_check_outlined), selectedIcon: Icon(Icons.fact_check, color: C.azul), label: 'Inspecciones'),
          NavigationDestination(icon: Icon(Icons.bar_chart_outlined), selectedIcon: Icon(Icons.bar_chart, color: C.azul), label: 'Informes'),
          NavigationDestination(icon: Icon(Icons.person_outline), selectedIcon: Icon(Icons.person, color: C.azul), label: 'Perfil'),
        ],
      ),
    );
  }
}

class _Inicio extends StatelessWidget {
  final void Function(int) irA;
  const _Inicio({required this.irA});

  Widget _item(IconData i, String t, String s, VoidCallback f) => AppCard(
        onTap: f,
        child: Row(children: [
          Container(padding: const EdgeInsets.all(10), decoration: BoxDecoration(color: const Color(0xFFE8F1FF), borderRadius: BorderRadius.circular(10)), child: Icon(i, color: C.azul)),
          const SizedBox(width: 14),
          Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(t, style: const TextStyle(fontWeight: FontWeight.w700, color: C.navy)),
            Text(s, style: const TextStyle(fontSize: 12, color: C.texto2)),
          ])),
          const Icon(Icons.chevron_right, color: C.texto2),
        ]),
      );

  @override
  Widget build(BuildContext context) {
    final nombre = context.watch<AppState>().profesional.split(' ').first;
    return ListView(padding: const EdgeInsets.all(20), children: [
      const Row(children: [
        Icon(Icons.verified_user, color: C.azul, size: 30), SizedBox(width: 8),
        Text('SST-IA', style: TextStyle(fontSize: 24, fontWeight: FontWeight.w800, color: C.navy)),
        Spacer(), StatusBadge('Sin conexión · modo local', C.texto2),
      ]),
      const SizedBox(height: 22),
      Text('Hola, $nombre', style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w800, color: C.navy)),
      const Text('Profesional de SST', style: TextStyle(color: C.texto2)),
      const SizedBox(height: 18),
      InkWell(
        onTap: () => ir(context, const NuevaInspeccionScreen()),
        borderRadius: BorderRadius.circular(14),
        child: Container(
          padding: const EdgeInsets.all(18),
          decoration: BoxDecoration(color: C.azul, borderRadius: BorderRadius.circular(14)),
          child: const Row(children: [
            CircleAvatar(backgroundColor: Colors.white24, child: Icon(Icons.add, color: Colors.white)), SizedBox(width: 14),
            Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text('Nueva inspección', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w700, fontSize: 16)),
              Text('Comenzar un nuevo recorrido', style: TextStyle(color: Colors.white70, fontSize: 12)),
            ]),
          ]),
        ),
      ),
      const SizedBox(height: 14),
      _item(Icons.description_outlined, 'Mis inspecciones', 'Ver inspecciones en curso y finalizadas', () => irA(1)),
      _item(Icons.bar_chart, 'Informes', 'Generar y consultar reportes', () => irA(2)),
      _item(Icons.settings_outlined, 'Configuración', 'Perfil y preferencias', () => irA(3)),
    ]);
  }
}
