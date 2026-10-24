import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/app_state.dart';
import '../utils/constants.dart';
import '../utils/validators.dart';
import '../widgets/widgets.dart';
import 'inspeccion_screen.dart';

class NuevaInspeccionScreen extends StatefulWidget {
  const NuevaInspeccionScreen({super.key});
  @override
  State<NuevaInspeccionScreen> createState() => _NuevaInspeccionScreenState();
}

class _NuevaInspeccionScreenState extends State<NuevaInspeccionScreen> {
  final _form = GlobalKey<FormState>();
  late DateTime _fecha = DateTime.now();
  String? _sede, _edificio, _area;
  late final _responsable = TextEditingController(text: context.read<AppState>().profesional);

  Future<void> _elegirFecha() async {
    final f = await showDatePicker(context: context, initialDate: _fecha, firstDate: DateTime(2020), lastDate: DateTime(2100));
    if (f != null) setState(() => _fecha = DateTime(f.year, f.month, f.day, _fecha.hour, _fecha.minute));
  }

  Future<void> _elegirHora() async {
    final h = await showTimePicker(context: context, initialTime: TimeOfDay.fromDateTime(_fecha));
    if (h != null) setState(() => _fecha = DateTime(_fecha.year, _fecha.month, _fecha.day, h.hour, h.minute));
  }

  Widget _combo(String l, List<String> items, String? v, void Function(String?) f) => Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Etiqueta(l),
        DropdownButtonFormField<String>(
            initialValue: v, isExpanded: true, validator: requerido, hint: Text('Selecciona $l'.toLowerCase()),
            items: items.map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(), onChanged: f),
      ]);

  void _comenzar() {
    if (!_form.currentState!.validate()) return;
    final i = context.read<AppState>().crear(fecha: _fecha, sede: _sede!, edificio: _edificio!, area: _area!, responsable: _responsable.text.trim());
    Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => InspeccionScreen(i), settings: const RouteSettings(name: 'inspeccion')));
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(title: const Text('Nueva inspección')),
        body: Form(
          key: _form,
          child: contenido([
            const Text('Completa la información general para iniciar el recorrido.', style: TextStyle(color: C.texto2)),
            const Etiqueta('Fecha'),
            TextFormField(key: ValueKey(fFecha(_fecha)), initialValue: fFecha(_fecha), readOnly: true, onTap: _elegirFecha, decoration: const InputDecoration(prefixIcon: Icon(Icons.calendar_today_outlined, size: 20))),
            const Etiqueta('Hora'),
            TextFormField(key: ValueKey(fHora(_fecha)), initialValue: fHora(_fecha), readOnly: true, onTap: _elegirHora, decoration: const InputDecoration(prefixIcon: Icon(Icons.access_time, size: 20))),
            _combo('Sede', sedes, _sede, (v) => setState(() => _sede = v)),
            _combo('Edificio', edificios, _edificio, (v) => setState(() => _edificio = v)),
            _combo('Área', areas, _area, (v) => setState(() => _area = v)),
            const Etiqueta('Responsable'),
            TextFormField(controller: _responsable, validator: requerido, decoration: const InputDecoration(prefixIcon: Icon(Icons.person_outline, size: 20))),
            const SizedBox(height: 24),
            AppButton('Comenzar inspección', onPressed: _comenzar),
          ]),
        ),
      );
}
