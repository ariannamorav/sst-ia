import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/app_state.dart';
import '../utils/constants.dart';
import '../widgets/widgets.dart';
import 'hallazgos_screen.dart';

class HallazgoGuardadoScreen extends StatelessWidget {
  const HallazgoGuardadoScreen({super.key});
  void _aInspeccion(BuildContext c) => Navigator.popUntil(c, (r) => r.settings.name == 'inspeccion');

  @override
  Widget build(BuildContext context) => Scaffold(
        body: SafeArea(child: Padding(padding: const EdgeInsets.all(24), child: Column(children: [
          const Spacer(),
          const CircleAvatar(radius: 48, backgroundColor: C.verde, child: Icon(Icons.check, color: Colors.white, size: 56)),
          const SizedBox(height: 22),
          const Text('¡Hallazgo registrado!', style: TextStyle(fontSize: 24, fontWeight: FontWeight.w800, color: C.navy)),
          const SizedBox(height: 8),
          const Text('La información ha sido guardada correctamente en esta inspección.', textAlign: TextAlign.center, style: TextStyle(color: C.texto2)),
          const Spacer(),
          AppButton('Registrar otro hallazgo', icon: Icons.photo_camera_outlined, onPressed: () => _aInspeccion(context)),
          const SizedBox(height: 10),
          AppButton('Ver hallazgos de la inspección', icon: Icons.checklist, estilo: EstiloBoton.contorno, onPressed: () {
            _aInspeccion(context);
            ir(context, HallazgosScreen(context.read<AppState>().actual!));
          }),
          const SizedBox(height: 10),
          AppButton('Volver al inicio', icon: Icons.home_outlined, estilo: EstiloBoton.suave, onPressed: () => Navigator.popUntil(context, (r) => r.isFirst)),
        ]))),
      );
}
