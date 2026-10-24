import 'package:flutter/material.dart';
import '../models/evidencia.dart';
import '../utils/constants.dart';
import '../utils/validators.dart';
import '../widgets/widgets.dart';
import 'analizando_screen.dart';

class EvidenciaScreen extends StatefulWidget {
  final String fotoPath;
  const EvidenciaScreen(this.fotoPath, {super.key});
  @override
  State<EvidenciaScreen> createState() => _EvidenciaScreenState();
}

class _EvidenciaScreenState extends State<EvidenciaScreen> {
  final _form = GlobalKey<FormState>();
  final _obs = TextEditingController(), _ubi = TextEditingController(), _extra = TextEditingController();
  String? _tipo;

  void _analizar() {
    if (!_form.currentState!.validate()) return;
    final e = Evidencia(fotoPath: widget.fotoPath, observacion: _obs.text.trim(), ubicacion: _ubi.text.trim(), tipo: _tipo ?? '', adicional: _extra.text.trim());
    ir(context, AnalizandoScreen(e));
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(title: const Text('Información de la evidencia')),
        body: Form(key: _form, child: contenido([
          Foto(widget.fotoPath, height: 170),
          const Etiqueta('Observación del profesional'),
          TextFormField(controller: _obs, validator: requerido, maxLines: 3, maxLength: 500,
              decoration: const InputDecoration(hintText: 'Ej.: Se observa una señal de extintor ubicada en el pasillo del segundo piso.')),
          const Etiqueta('Ubicación específica'),
          TextFormField(controller: _ubi, validator: requerido, decoration: const InputDecoration(prefixIcon: Icon(Icons.location_on_outlined, size: 20), hintText: 'Pasillo segundo piso')),
          const Etiqueta('Tipo de señalización (opcional)'),
          DropdownButtonFormField<String>(initialValue: _tipo, isExpanded: true, hint: const Text('Selecciona un tipo'),
              items: tiposSenal.map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(), onChanged: (v) => _tipo = v),
          const Etiqueta('Información adicional (opcional)'),
          TextFormField(controller: _extra, maxLines: 2, decoration: const InputDecoration(hintText: 'Añade más detalles relevantes...')),
          const SizedBox(height: 22),
          AppButton('Analizar evidencia con IA', icon: Icons.auto_awesome, onPressed: _analizar),
        ])),
      );
}
