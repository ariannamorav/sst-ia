import 'dart:io';
import 'dart:typed_data';

import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:image_picker/image_picker.dart';
import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;

import '../models/inspeccion.dart';
import '../models/hallazgo.dart';
import '../utils/constants.dart';

/// Genera el PDF localmente. Solo incluye hallazgos validados.
///
/// En Flutter Web, las fotos de image_picker tienen una ruta blob: y no se
/// pueden leer con dart:io. XFile.readAsBytes() permite leerlas de forma
/// compatible con web y móvil.
class PdfService {
  Future<Uint8List> generar(Inspeccion i) async {
    final doc = pw.Document();
    final lista = i.validados;

    // Leer las fotos antes de construir el PDF y evitar File.existsSync(),
    // que no está soportado en Flutter Web.
    final fotos = <HallazgoFoto>[];
    for (final h in lista) {
      Uint8List? bytes;
      final path = h.fotoPath;
      if (path != null && path.isNotEmpty) {
        try {
          bytes = kIsWeb
              ? await XFile(path).readAsBytes()
              : await File(path).readAsBytes();
        } catch (_) {
          // La foto es opcional para el informe: si no se puede leer,
          // el resto del informe debe generarse normalmente.
        }
      }
      fotos.add(HallazgoFoto(h, bytes));
    }

    pw.Widget fila(String k, String v) => pw.Padding(
      padding: const pw.EdgeInsets.only(bottom: 2),
      child: pw.RichText(
        text: pw.TextSpan(children: [
          pw.TextSpan(
            text: '$k: ',
            style: pw.TextStyle(fontWeight: pw.FontWeight.bold),
          ),
          pw.TextSpan(text: v),
        ]),
      ),
    );

    doc.addPage(
      pw.MultiPage(
        pageFormat: PdfPageFormat.a4,
        margin: const pw.EdgeInsets.all(32),
        build: (_) => [
          pw.Text(
            'SST-IA',
            style: pw.TextStyle(
              fontSize: 26,
              fontWeight: pw.FontWeight.bold,
              color: PdfColor.fromHex('#0B2A4A'),
            ),
          ),
          pw.Text(
            'Informe de inspección ${i.codigo}',
            style: const pw.TextStyle(fontSize: 14),
          ),
          pw.Divider(),
          fila('Fecha', fFecha(i.fecha)),
          fila('Sede', i.sede),
          fila('Edificio', i.edificio),
          fila('Área', i.area),
          fila('Responsable', i.responsable),
          fila('Hallazgos validados', '${lista.length}'),
          pw.SizedBox(height: 14),
          for (final item in fotos)
            pw.Container(
              margin: const pw.EdgeInsets.only(bottom: 10),
              padding: const pw.EdgeInsets.all(10),
              decoration: pw.BoxDecoration(
                border: pw.Border.all(color: PdfColors.grey400),
                borderRadius: pw.BorderRadius.circular(6),
              ),
              child: pw.Row(
                crossAxisAlignment: pw.CrossAxisAlignment.start,
                children: [
                  if (item.bytes != null)
                    pw.Container(
                      width: 130,
                      height: 100,
                      child: pw.Image(
                        pw.MemoryImage(item.bytes!),
                        fit: pw.BoxFit.cover,
                      ),
                    ),
                  if (item.bytes != null) pw.SizedBox(width: 12),
                  pw.Expanded(
                    child: pw.Column(
                      crossAxisAlignment: pw.CrossAxisAlignment.start,
                      children: [
                        fila('Elemento', item.hallazgo.elemento),
                        fila('Categoría', item.hallazgo.categoria),
                        fila('Ubicación', item.hallazgo.ubicacion),
                        fila('Descripción', item.hallazgo.descripcion),
                        fila('Condición', item.hallazgo.condicion),
                        fila('Estado', 'Validado'),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          if (lista.isEmpty)
            pw.Text('Esta inspección no tiene hallazgos validados.'),
        ],
      ),
    );

    return doc.save();
  }
}

class HallazgoFoto {
  final Hallazgo hallazgo;
  final Uint8List? bytes;
  HallazgoFoto(this.hallazgo, this.bytes);
}
