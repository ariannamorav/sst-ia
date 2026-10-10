import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'screens/splash_screen.dart';
import 'services/analisis_service.dart';
import 'services/analisis_simulado_service.dart';
import 'services/app_state.dart';
import 'theme/app_theme.dart';

void main() => runApp(MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AppState()),
        // TODO: cambiar a ServicioAnalisisGemini() cuando exista (las pantallas no cambian).
        Provider<AnalisisService>(create: (_) => ServicioAnalisisSimulado()),
      ],
      child: const SstIaApp(),
    ));

class SstIaApp extends StatelessWidget {
  const SstIaApp({super.key});
  @override
  Widget build(BuildContext context) =>
      MaterialApp(title: 'SST-IA', debugShowCheckedModeBanner: false, theme: appTheme(), home: const SplashScreen());
}
