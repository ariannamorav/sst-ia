import 'dart:io';
import 'dart:typed_data';
import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;
import '../models/inspeccion.dart';
import '../utils/constants.dart';

/// Genera el PDF localmente. Solo incluye hallazgos validados.
class PdfService {
  Future<Uint8List> generar(Inspeccion i) async {
    final doc = pw.Document();
    final lista = i.validados;
    pw.Widget fila(String k, String v) => pw.Padding(
        padding: const pw.EdgeInsets.only(bottom: 2),
        child: pw.RichText(text: pw.TextSpan(children: [
          pw.TextSpan(text: '$k: ', style: pw.TextStyle(fontWeight: pw.FontWeight.bold)), pw.TextSpan(text: v)])));

    doc.addPage(pw.MultiPage(
      pageFormat: PdfPageFormat.a4,
      margin: const pw.EdgeInsets.all(32),
      build: (_) => [
        pw.Text('SST-IA', style: pw.TextStyle(fontSize: 26, fontWeight: pw.FontWeight.bold, color: PdfColor.fromHex('#0B2A4A'))),
        pw.Text('Informe de inspección ${i.codigo}', style: const pw.TextStyle(fontSize: 14)),
        pw.Divider(),
        fila('Fecha', fFecha(i.fecha)), fila('Sede', i.sede), fila('Edificio', i.edificio),
        fila('Área', i.area), fila('Responsable', i.responsable), fila('Hallazgos validados', '${lista.length}'),
        pw.SizedBox(height: 14),
        for (final h in lista)
          pw.Container(
            margin: const pw.EdgeInsets.only(bottom: 10),
            padding: const pw.EdgeInsets.all(10),
            decoration: pw.BoxDecoration(border: pw.Border.all(color: PdfColors.grey400), borderRadius: pw.BorderRadius.circular(6)),
            child: pw.Row(crossAxisAlignment: pw.CrossAxisAlignment.start, children: [
              if (h.fotoPath != null && File(h.fotoPath!).existsSync())
                pw.Image(pw.MemoryImage(File(h.fotoPath!).readAsBytesSync()), width: 130, height: 100, fit: pw.BoxFit.cover),
              pw.SizedBox(width: 12),
              pw.Expanded(child: pw.Column(crossAxisAlignment: pw.CrossAxisAlignment.start, children: [
                fila('Elemento', h.elemento), fila('Categoría', h.categoria), fila('Ubicación', h.ubicacion),
                fila('Descripción', h.descripcion), fila('Condición', h.condicion), fila('Estado', 'Validado'),
              ])),
            ]),
          ),
        if (lista.isEmpty) pw.Text('Esta inspección no tiene hallazgos validados.'),
      ],
    ));
    return doc.save();
  }
}
