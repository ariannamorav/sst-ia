import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/evidencia.dart';
import '../models/hallazgo.dart';
import '../services/app_state.dart';
import '../utils/constants.dart';
import '../utils/validators.dart';
import '../widgets/widgets.dart';
import 'hallazgo_guardado_screen.dart';

/// El profesional corrige y decide. También sirve para editar desde la lista.
class RevisarHallazgoScreen extends StatefulWidget {
  final Evidencia evidencia;
  final Hallazgo hallazgo;
  const RevisarHallazgoScreen(this.evidencia, this.hallazgo, {super.key});
  @override
  State<RevisarHallazgoScreen> createState() => _RevisarHallazgoScreenState();
}

class _RevisarHallazgoScreenState extends State<RevisarHallazgoScreen> {
  final _form = GlobalKey<FormState>();
  late final Hallazgo h = widget.hallazgo;
  late final _elemento = TextEditingController(text: h.elemento), _ubi = TextEditingController(text: h.ubicacion),
      _desc = TextEditingController(text: h.descripcion), _obs = TextEditingController(text: h.observacion);
  late String _categoria = h.categoria, _condicion = h.condicion;

  Widget _combo(String v, List<String> base, void Function(String?) f) {
    final items = base.contains(v) ? base : [...base, v];
    return DropdownButtonFormField<String>(value: v, isExpanded: true, items: items.map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(), onChanged: f);
  }

  /// Devuelve true si fue la primera vez que se guarda (flujo nuevo).
  bool _guardar(EstadoHallazgo estado) {
    h..elemento = _elemento.text.trim()..categoria = _categoria..ubicacion = _ubi.text.trim()
      ..descripcion = _desc.text.trim()..condicion = _condicion..observacion = _obs.text.trim()..estado = estado;
    final nuevo = !widget.evidencia.hallazgos.contains(h);
    context.read<AppState>().guardarHallazgo(widget.evidencia, h);
    return nuevo;
  }

  void _accion(EstadoHallazgo estado) {
    if (!_form.currentState!.validate()) return;
    final nuevo = _guardar(estado);
    if (nuevo) {
      Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => const HallazgoGuardadoScreen()));
    } else {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Cambios guardados correctamente.')));
      Navigator.pop(context);
    }
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(title: const Text('Revisar hallazgo')),
        body: Form(key: _form, child: contenido([
          const Text('Edita los campos si es necesario.', style: TextStyle(color: C.texto2)),
          const SizedBox(height: 10), Foto(h.fotoPath, height: 130),
          const Etiqueta('Elemento'), TextFormField(controller: _elemento, validator: requerido),
          const Etiqueta('Categoría'), _combo(_categoria, categorias, (v) => _categoria = v!),
          const Etiqueta('Ubicación'), TextFormField(controller: _ubi, validator: requerido),
          const Etiqueta('Descripción'), TextFormField(controller: _desc, maxLines: 3),
          const Etiqueta('Condición'), _combo(_condicion, condiciones, (v) => _condicion = v!),
          const Etiqueta('Observación'), TextFormField(controller: _obs, maxLines: 2),
          const SizedBox(height: 22),
          Row(children: [
            Expanded(child: AppButton('Guardar cambios', estilo: EstiloBoton.contorno, onPressed: () => _accion(EstadoHallazgo.pendiente))), const SizedBox(width: 12),
            Expanded(child: AppButton('Aprobar hallazgo', onPressed: () => _accion(EstadoHallazgo.validado))),
          ]),
        ])),
      );
}
