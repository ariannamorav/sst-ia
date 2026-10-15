import 'dart:convert';
import 'dart:typed_data';

import 'package:http/http.dart' as http;

class RoboflowService {
  static const String _workspace = 'sstiasenalizacion';

  static const String _workflowId =
      'sst-ia-senalizacion-sst-ia-senalizacion-3-rfdetr-small-t1-workflow';

  static const String _apiKey = String.fromEnvironment(
    'ROBOFLOW_API_KEY',
  );

  static const String _baseUrl = 'https://serverless.roboflow.com';

  Future<Map<String, dynamic>> analizarImagen(
    Uint8List bytes,
  ) async {
    if (bytes.isEmpty) {
      throw Exception('La fotografía está vacía.');
    }

    if (_apiKey.isEmpty) {
      throw Exception(
        'Falta configurar ROBOFLOW_API_KEY al ejecutar Flutter.',
      );
    }

    final uri = Uri.parse(
      '$_baseUrl/$_workspace/workflows/$_workflowId',
    );

    final response = await http
        .post(
          uri,
          headers: {
            'Content-Type': 'application/json',
          },
          body: jsonEncode({
            'api_key': _apiKey,
            'inputs': {
              'image': {
                'type': 'base64',
                'value': base64Encode(bytes),
              },
            },
          }),
        )
        .timeout(const Duration(seconds: 100));

    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw Exception(
        'Error de Roboflow HTTP ${response.statusCode}: '
        '${response.body}',
      );
    }

    final dynamic decoded = jsonDecode(response.body);

    if (decoded is Map<String, dynamic>) {
      return decoded;
    }

    throw const FormatException(
      'Roboflow devolvió una respuesta JSON inesperada.',
    );
  }
}
