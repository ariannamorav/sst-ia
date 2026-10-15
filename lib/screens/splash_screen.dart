import 'dart:async';
import 'package:flutter/material.dart';
import '../widgets/widgets.dart';
import '../utils/constants.dart';
import 'home_screen.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});
  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  Timer? _t;
  @override
  void initState() {
    super.initState();
    _t = Timer(const Duration(seconds: 3), _entrar);
  }

  void _entrar() {
    if (mounted) Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => const HomeScreen()));
  }

  @override
  void dispose() { _t?.cancel(); super.dispose(); }

  @override
  Widget build(BuildContext context) => Scaffold(
        body: Container(
          width: double.infinity,
          decoration: const BoxDecoration(gradient: LinearGradient(begin: Alignment.topCenter, end: Alignment.bottomCenter, colors: [Color(0xFF0B2A4A), Color(0xFF123F6E)])),
          child: SafeArea(
            child: Padding(
              padding: const EdgeInsets.all(28),
              child: Column(children: [
                const Spacer(),
                const Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                  Icon(Icons.verified_user, color: Colors.white, size: 54), SizedBox(width: 10),
                  Text('SST-IA', style: TextStyle(color: Colors.white, fontSize: 42, fontWeight: FontWeight.w800)),
                ]),
                const SizedBox(height: 16),
                const Text('Inspecciones más simples,\nespacios más seguros.', textAlign: TextAlign.center, style: TextStyle(color: Colors.white70, fontSize: 18)),
                const Spacer(),
                SizedBox(width: double.infinity, child: ElevatedButton(
                  style: ElevatedButton.styleFrom(backgroundColor: Colors.white, foregroundColor: C.navy, minimumSize: const Size(0, 52), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))),
                  onPressed: _entrar, child: const Text('Ingresar', style: TextStyle(fontWeight: FontWeight.w700)))),
                const SizedBox(height: 12),
              ]),
            ),
          ),
        ),
      );
}
