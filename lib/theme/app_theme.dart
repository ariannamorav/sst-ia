import 'package:flutter/material.dart';
import '../utils/constants.dart';

ThemeData appTheme() {
  OutlineInputBorder b(Color c) => OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: BorderSide(color: c));
  return ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(seedColor: C.azul, primary: C.azul),
    scaffoldBackgroundColor: Colors.white,
    appBarTheme: const AppBarTheme(
        backgroundColor: Colors.white, foregroundColor: C.navy, elevation: 0, centerTitle: true,
        titleTextStyle: TextStyle(color: C.navy, fontSize: 17, fontWeight: FontWeight.w700)),
    inputDecorationTheme: InputDecorationTheme(
      filled: true, fillColor: Colors.white,
      contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 14),
      border: b(C.borde), enabledBorder: b(C.borde), focusedBorder: b(C.azul), errorBorder: b(C.rojo),
    ),
  );
}
