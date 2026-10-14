import 'dart:io';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart';
import '../models/hallazgo.dart';
import '../utils/constants.dart';

Future<T?> ir<T>(BuildContext c, Widget w, {String? nombre}) =>
    Navigator.push<T>(c, MaterialPageRoute(builder: (_) => w, settings: RouteSettings(name: nombre)));

enum EstiloBoton { primario, contorno, peligro, suave }

class AppButton extends StatelessWidget {
  final String label;
  final VoidCallback? onPressed;
  final IconData? icon;
  final EstiloBoton estilo;
  const AppButton(this.label, {super.key, this.onPressed, this.icon, this.estilo = EstiloBoton.primario});

  @override
  Widget build(BuildContext context) {
    final (bg, fg, borde) = switch (estilo) {
      EstiloBoton.primario => (C.azul, Colors.white, C.azul),
      EstiloBoton.contorno => (Colors.white, C.azul, C.azul),
      EstiloBoton.peligro => (const Color(0xFFFFF5F5), C.rojo, const Color(0xFFF3B8B4)),
      EstiloBoton.suave => (C.gris, C.navy, C.borde),
    };
    final st = ElevatedButton.styleFrom(
        backgroundColor: bg, foregroundColor: fg, elevation: 0, minimumSize: const Size(0, 52),
        side: BorderSide(color: borde), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        textStyle: const TextStyle(fontWeight: FontWeight.w600, fontSize: 15));
    return SizedBox(
      width: double.infinity,
      child: icon == null
          ? ElevatedButton(style: st, onPressed: onPressed, child: Text(label))
          : ElevatedButton.icon(style: st, onPressed: onPressed, icon: Icon(icon, size: 20), label: Text(label)),
    );
  }
}

class AppCard extends StatelessWidget {
  final Widget child;
  final VoidCallback? onTap;
  final EdgeInsets padding;
  const AppCard({super.key, required this.child, this.onTap, this.padding = const EdgeInsets.all(14)});
  @override
  Widget build(BuildContext context) => Container(
        margin: const EdgeInsets.only(bottom: 12),
        decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(14), border: Border.all(color: C.borde),
            boxShadow: [BoxShadow(color: Colors.black.withOpacity(.04), blurRadius: 10, offset: const Offset(0, 3))]),
        child: Material(color: Colors.transparent, child: InkWell(borderRadius: BorderRadius.circular(14), onTap: onTap, child: Padding(padding: padding, child: child))),
      );
}

class StatusBadge extends StatelessWidget {
  final String texto;
  final Color color;
  const StatusBadge(this.texto, this.color, {super.key});
  @override
  Widget build(BuildContext context) => Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(color: color.withOpacity(.12), borderRadius: BorderRadius.circular(20)),
      child: Text(texto, style: TextStyle(color: color, fontSize: 12, fontWeight: FontWeight.w600)));
}

StatusBadge badgeEstado(EstadoHallazgo e) => switch (e) {
      EstadoHallazgo.validado => const StatusBadge('Validado', C.verde),
      EstadoHallazgo.pendiente => const StatusBadge('Pendiente', C.naranja),
      EstadoHallazgo.rechazado => const StatusBadge('Rechazado', C.rojo),
    };

class ConfidenceBar extends StatelessWidget {
  final double valor;
  const ConfidenceBar(this.valor, {super.key});
  @override
  Widget build(BuildContext context) => Column(children: [
        Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
          const Text('Confianza del modelo', style: TextStyle(fontWeight: FontWeight.w700, fontSize: 13)),
          Text('${(valor * 100).round()}%', style: const TextStyle(color: C.verde, fontWeight: FontWeight.w700)),
        ]),
        const SizedBox(height: 6),
        ClipRRect(borderRadius: BorderRadius.circular(6), child: LinearProgressIndicator(value: valor, minHeight: 7, color: C.verde, backgroundColor: C.borde)),
      ]);
}

/// Foto desde archivo con respaldo cuando no existe.
class Foto extends StatelessWidget {
  final String? path;
  final double? height, width;
  const Foto(this.path, {super.key, this.height, this.width});
  @override
  Widget build(BuildContext context) => ClipRRect(
        borderRadius: BorderRadius.circular(10),
        child: SizedBox(
          height: height, width: width,
          // En Flutter Web, File.existsSync() lanza Unsupported operation:
          // _Namespace. image_picker devuelve una URL temporal (blob:) que
          // debe mostrarse con Image.network. En Android/iOS se usa Image.file.
          child: path == null
              ? Container(color: C.gris, child: const Icon(Icons.image_outlined, color: C.texto2))
              : kIsWeb
                  ? Image.network(
                      path!,
                      fit: BoxFit.cover,
                      errorBuilder: (_, __, ___) => Container(
                        color: C.gris,
                        child: const Icon(Icons.image_outlined, color: C.texto2),
                      ),
                    )
                  : _fotoLocal(path!),
        ),
      );
}


Widget _fotoLocal(String path) {
  final file = File(path);
  return file.existsSync()
      ? Image.file(file, fit: BoxFit.cover)
      : Container(color: C.gris, child: const Icon(Icons.image_outlined, color: C.texto2));
}

class FindingCard extends StatelessWidget {
  final Hallazgo h;
  final VoidCallback? onTap;
  const FindingCard(this.h, {super.key, this.onTap});
  @override
  Widget build(BuildContext context) => AppCard(
        onTap: onTap,
        padding: const EdgeInsets.all(10),
        child: Row(children: [
          Foto(h.fotoPath, width: 64, height: 64),
          const SizedBox(width: 12),
          Expanded(
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Row(children: [
                Expanded(child: Text(h.elemento, style: const TextStyle(fontWeight: FontWeight.w700, color: C.navy))),
                badgeEstado(h.estado),
              ]),
              const SizedBox(height: 3),
              Text(h.categoria, style: const TextStyle(color: C.texto2, fontSize: 12)),
              Text('${h.ubicacion} · ${fFecha(h.fecha)} ${fHora(h.fecha)}', style: const TextStyle(color: C.texto2, fontSize: 11)),
            ]),
          ),
          const Icon(Icons.chevron_right, color: C.texto2),
        ]),
      );
}

class Etiqueta extends StatelessWidget {
  final String texto;
  const Etiqueta(this.texto, {super.key});
  @override
  Widget build(BuildContext context) =>
      Padding(padding: const EdgeInsets.only(top: 14, bottom: 6), child: Text(texto, style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13, color: C.navy)));
}

class Dato extends StatelessWidget {
  final String label, valor;
  const Dato(this.label, this.valor, {super.key});
  @override
  Widget build(BuildContext context) => Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(label, style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 12, color: C.texto2)),
        Text(valor, style: const TextStyle(fontSize: 14, color: C.navy)),
      ]));
}

class AvisoPreliminar extends StatelessWidget {
  const AvisoPreliminar({super.key});
  @override
  Widget build(BuildContext context) => Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(color: const Color(0xFFE8F1FF), borderRadius: BorderRadius.circular(10), border: Border.all(color: const Color(0xFFB9D3F8))),
      child: const Row(children: [
        Icon(Icons.info, color: C.azul, size: 20), SizedBox(width: 10),
        Expanded(child: Text('Este es un resultado preliminar.\nDebe ser revisado por el profesional.', style: TextStyle(fontSize: 12.5, color: C.navy))),
      ]));
}

/// Pantalla de estado vacío / error amigable.
class EstadoVacio extends StatelessWidget {
  final IconData icono;
  final String titulo, mensaje;
  final Color color;
  const EstadoVacio(this.icono, this.titulo, this.mensaje, {super.key, this.color = C.texto2});
  @override
  Widget build(BuildContext context) => Center(
      child: Padding(padding: const EdgeInsets.all(28), child: Column(mainAxisSize: MainAxisSize.min, children: [
        Icon(icono, size: 54, color: color), const SizedBox(height: 14),
        Text(titulo, textAlign: TextAlign.center, style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w700, color: C.navy)),
        const SizedBox(height: 6),
        Text(mensaje, textAlign: TextAlign.center, style: const TextStyle(color: C.texto2)),
      ])));
}

Widget contenido(List<Widget> hijos) => SafeArea(child: ListView(padding: const EdgeInsets.fromLTRB(20, 8, 20, 24), children: hijos));
