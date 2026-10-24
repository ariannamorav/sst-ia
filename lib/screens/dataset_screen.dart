import 'dart:async';
import 'package:flutter/material.dart';
import '../services/dataset_service.dart';
import '../utils/constants.dart';
import '../widgets/widgets.dart';

class DatasetScreen extends StatefulWidget {
  const DatasetScreen({super.key});

  @override
  State<DatasetScreen> createState() => _DatasetScreenState();
}

class _DatasetScreenState extends State<DatasetScreen> {
  final _service = DatasetIAService();
  final _curlController = TextEditingController();
  final _yamlPathController = TextEditingController(text: 'data/datasets/sst-completo/data.yaml');

  EstadoServidorIA? _estadoServidor;
  EstadoEntrenamiento? _estadoEntrenamiento;
  Timer? _pollingTimer;

  bool _cargandoSalud = true;
  bool _importandoCurl = false;
  bool _iniciandoEntrenamiento = false;
  int _epochs = 25;

  @override
  void initState() {
    super.initState();
    _actualizarSalud();
    _iniciarPollingEstado();
  }

  @override
  void dispose() {
    _pollingTimer?.cancel();
    _curlController.dispose();
    _yamlPathController.dispose();
    super.dispose();
  }

  Future<void> _actualizarSalud() async {
    setState(() => _cargandoSalud = true);
    final salud = await _service.verificarSalud();
    if (mounted) {
      setState(() {
        _estadoServidor = salud;
        _cargandoSalud = false;
      });
    }
  }

  void _iniciarPollingEstado() {
    _consultarEstado();
    _pollingTimer = Timer.periodic(const Duration(seconds: 3), (_) => _consultarEstado());
  }

  Future<void> _consultarEstado() async {
    final est = await _service.consultarEstadoEntrenamiento();
    if (mounted) {
      setState(() => _estadoEntrenamiento = est);
    }
  }

  Future<void> _importarCurl() async {
    final curl = _curlController.text.trim();
    if (curl.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Por favor ingresa o pega el comando cURL de Roboflow.')),
      );
      return;
    }

    setState(() => _importandoCurl = true);
    try {
      final res = await _service.importarDatasetCurl(curlCommand: curl);
      if (!mounted) return;

      if (res['data_yaml'] != null) {
        _yamlPathController.text = res['data_yaml'].toString();
      }

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          backgroundColor: C.verde,
          content: Text('Dataset importado exitosamente (${res['archivos_totales']} archivos).'),
        ),
      );
      _curlController.clear();
      _actualizarSalud();
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(backgroundColor: C.rojo, content: Text('Error: $e')),
      );
    } finally {
      if (mounted) setState(() => _importandoCurl = false);
    }
  }

  Future<void> _entrenar() async {
    final yaml = _yamlPathController.text.trim();
    if (yaml.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Por favor indica la ruta del archivo data.yaml.')),
      );
      return;
    }

    setState(() => _iniciandoEntrenamiento = true);
    try {
      await _service.iniciarEntrenamiento(dataYamlPath: yaml, epochs: _epochs);
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          backgroundColor: C.azul,
          content: Text('Entrenamiento de YOLOv8 iniciado en segundo plano.'),
        ),
      );
      _consultarEstado();
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(backgroundColor: C.rojo, content: Text('Error: $e')),
      );
    } finally {
      if (mounted) setState(() => _iniciandoEntrenamiento = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final esDesktop = MediaQuery.of(context).size.width >= 850;
    final servidorOk = _estadoServidor?.operativo == true;
    final entrenando = _estadoEntrenamiento?.enProgreso == true;

    // Tarjeta de estado del backend
    Widget tarjetaEstado = Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: servidorOk ? const Color(0xFFF0FDF4) : const Color(0xFFFFFBEB),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: servidorOk ? const Color(0xFFBBF7D0) : const Color(0xFFFDE68A)),
      ),
      child: Row(
        children: [
          Icon(
            servidorOk ? Icons.check_circle : Icons.warning_amber_rounded,
            color: servidorOk ? C.verde : C.naranja,
            size: 30,
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  servidorOk ? 'Backend Modulo_SST_IA Conectado y Operativo' : 'Backend Desconectado (Modo Local)',
                  style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 13.5, color: C.navy),
                ),
                const SizedBox(height: 3),
                Text(
                  _cargandoSalud
                      ? 'Consultando servidor...'
                      : 'Modelo activo: ${_estadoServidor?.modeloCargado ?? "Simulador"} · URL: ${_estadoServidor?.url ?? ""}',
                  style: const TextStyle(fontSize: 11.5, color: C.texto2),
                ),
              ],
            ),
          ),
          IconButton(
            icon: const Icon(Icons.refresh, color: C.azul, size: 20),
            onPressed: () {
              _actualizarSalud();
              _consultarEstado();
            },
            tooltip: 'Verificar conexión',
          ),
        ],
      ),
    );

    // Monitor de progreso de entrenamiento
    Widget monitorProgreso = Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: entrenando ? const Color(0xFFEFF6FF) : const Color(0xFFF8FAFC),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: entrenando ? const Color(0xFFBFDBFE) : const Color(0xFFE2E8F0)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(entrenando ? Icons.sync : Icons.task_alt, color: C.azul, size: 20),
              const SizedBox(width: 8),
              Text(
                entrenando ? 'Entrenando YOLOv8 en progreso...' : 'Estado del Entrenamiento',
                style: const TextStyle(fontWeight: FontWeight.w700, color: C.navy, fontSize: 13),
              ),
              const Spacer(),
              Text(
                '${_estadoEntrenamiento?.progreso ?? 0}%',
                style: const TextStyle(fontWeight: FontWeight.w800, color: C.azul, fontSize: 14),
              ),
            ],
          ),
          const SizedBox(height: 10),
          LinearProgressIndicator(
            value: (_estadoEntrenamiento?.progreso ?? 0) / 100.0,
            backgroundColor: const Color(0xFFE2E8F0),
            color: C.azul,
            minHeight: 8,
            borderRadius: BorderRadius.circular(4),
          ),
          const SizedBox(height: 8),
          Text(
            _estadoEntrenamiento?.mensaje ?? 'Listo para entrenar',
            style: const TextStyle(fontSize: 12, color: C.texto2),
          ),
        ],
      ),
    );

    // Sección 1: Importar Dataset vía cURL
    Widget seccionCurl = Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: const Color(0xFFE2E8F0)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('1. Importar Dataset desde Roboflow (cURL)',
              style: TextStyle(fontWeight: FontWeight.w700, fontSize: 14.5, color: C.navy)),
          const SizedBox(height: 4),
          const Text(
            'Pega el comando cURL generado por Roboflow (formato YOLOv8) para descargarlo automáticamente en el servidor.',
            style: TextStyle(fontSize: 12, color: C.texto2),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _curlController,
            maxLines: 4,
            style: const TextStyle(fontFamily: 'monospace', fontSize: 12),
            decoration: InputDecoration(
              hintText: 'curl -L "https://universe.roboflow.com/ds/..." > roboflow.zip; unzip...',
              hintStyle: const TextStyle(fontSize: 11, color: C.texto2),
              filled: true,
              fillColor: const Color(0xFFF8FAFC),
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(10),
                borderSide: const BorderSide(color: Color(0xFFCBD5E1)),
              ),
            ),
          ),
          const SizedBox(height: 12),
          AppButton(
            _importandoCurl ? 'Descargando e Importando Dataset...' : 'Descargar e Importar Dataset',
            icon: Icons.cloud_download_outlined,
            onPressed: _importandoCurl ? () {} : _importarCurl,
          ),
        ],
      ),
    );

    // Sección 2: Reentrenar Modelo
    Widget seccionEntrenamiento = Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: const Color(0xFFE2E8F0)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('2. Reentrenar Modelo YOLOv8',
              style: TextStyle(fontWeight: FontWeight.w700, fontSize: 14.5, color: C.navy)),
          const SizedBox(height: 4),
          const Text(
            'Indica la ruta del archivo data.yaml y el número de épocas para actualizar sst_best.pt.',
            style: TextStyle(fontSize: 12, color: C.texto2),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _yamlPathController,
            decoration: InputDecoration(
              labelText: 'Ruta de data.yaml',
              labelStyle: const TextStyle(fontSize: 12),
              filled: true,
              fillColor: const Color(0xFFF8FAFC),
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(10),
                borderSide: const BorderSide(color: Color(0xFFCBD5E1)),
              ),
            ),
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              const Text('Épocas:', style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: C.navy)),
              const SizedBox(width: 12),
              Expanded(
                child: DropdownButtonFormField<int>(
                  initialValue: _epochs,
                  decoration: InputDecoration(
                    filled: true,
                    fillColor: const Color(0xFFF8FAFC),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(10),
                      borderSide: const BorderSide(color: Color(0xFFCBD5E1)),
                    ),
                  ),
                  items: const [
                    DropdownMenuItem(value: 10, child: Text('10 épocas (Rápido)')),
                    DropdownMenuItem(value: 25, child: Text('25 épocas (Recomendado)')),
                    DropdownMenuItem(value: 35, child: Text('35 épocas (Alta precisión)')),
                    DropdownMenuItem(value: 50, child: Text('50 épocas (Exhaustivo)')),
                  ],
                  onChanged: (v) {
                    if (v != null) setState(() => _epochs = v);
                  },
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          AppButton(
            _iniciandoEntrenamiento || entrenando ? 'Entrenamiento en Ejecución...' : 'Iniciar Reentrenamiento YOLOv8',
            icon: Icons.model_training,
            estilo: EstiloBoton.primario,
            onPressed: (_iniciandoEntrenamiento || entrenando) ? () {} : _entrenar,
          ),
        ],
      ),
    );

    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: const Text('Dataset y Gestión del Modelo IA'),
        backgroundColor: Colors.white,
        foregroundColor: C.navy,
        elevation: 0.5,
      ),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 1100),
          child: ListView(
            padding: const EdgeInsets.fromLTRB(20, 20, 20, 36),
            children: [
              tarjetaEstado,
              const SizedBox(height: 16),
              if (esDesktop) ...[
                // Layout de 2 columnas en Desktop
                Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Expanded(child: seccionCurl),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        children: [
                          monitorProgreso,
                          const SizedBox(height: 16),
                          seccionEntrenamiento,
                        ],
                      ),
                    ),
                  ],
                ),
              ] else ...[
                // Layout vertical en Móvil
                monitorProgreso,
                const SizedBox(height: 16),
                seccionCurl,
                const SizedBox(height: 16),
                seccionEntrenamiento,
              ],
              const SizedBox(height: 20),
              // Nota institucional
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: const Color(0xFFF1F5F9),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: const Row(
                  children: [
                    Icon(Icons.info_outline, color: C.texto2, size: 20),
                    SizedBox(width: 10),
                    Expanded(
                      child: Text(
                        'Los pesos reentrenados se almacenan en C:\\Users\\Yairc\\Documents\\Universidad\\IA\\Modulo_SST_IA\\models\\sst_best.pt y son consumidos automáticamente por la app Flutter.',
                        style: TextStyle(fontSize: 11.5, color: C.texto2),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
