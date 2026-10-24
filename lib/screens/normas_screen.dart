import 'package:flutter/material.dart';
import '../utils/catalogo_normas.dart';
import '../utils/constants.dart';
import '../widgets/widgets.dart';

class NormasScreen extends StatefulWidget {
  const NormasScreen({super.key});

  @override
  State<NormasScreen> createState() => _NormasScreenState();
}

class _NormasScreenState extends State<NormasScreen> {
  String _filtroCategoria = 'Todas';
  String _busqueda = '';

  Color _colorCategoria(String cat) {
    switch (cat) {
      case 'Rojas':
        return const Color(0xFFDC2626);
      case 'Amarillas':
        return const Color(0xFFD97706);
      case 'Azules':
        return const Color(0xFF2563EB);
      case 'Verdes':
        return const Color(0xFF059669);
      default:
        return C.navy;
    }
  }

  @override
  Widget build(BuildContext context) {
    final ancho = MediaQuery.of(context).size.width;
    final esDesktop = ancho >= 850;

    final senalesFiltradas = CatalogoNormasSST.senales.where((s) {
      final coincideCat = _filtroCategoria == 'Todas' || s.categoria == _filtroCategoria;
      if (!coincideCat) return false;
      if (_busqueda.isEmpty) return true;
      final q = _busqueda.toLowerCase();
      return s.elemento.toLowerCase().contains(q) ||
          s.norma.toLowerCase().contains(q) ||
          s.palabrasClave.any((p) => p.toLowerCase().contains(q));
    }).toList();

    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: const Text('Catálogo de Normas de Señalización SST'),
        backgroundColor: Colors.white,
        foregroundColor: C.navy,
        elevation: 0.5,
      ),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 1100),
          child: Column(
            children: [
              // Barra de búsqueda y filtros
              Container(
                padding: const EdgeInsets.fromLTRB(20, 14, 20, 10),
                decoration: const BoxDecoration(
                  color: Colors.white,
                  border: Border(bottom: BorderSide(color: Color(0xFFE2E8F0))),
                ),
                child: Column(
                  children: [
                    TextField(
                      decoration: InputDecoration(
                        hintText: 'Buscar por señal, equipo o norma (NTC 1461, NSR-10, extintor, salida)...',
                        hintStyle: const TextStyle(fontSize: 13, color: C.texto2),
                        prefixIcon: const Icon(Icons.search, color: C.azul),
                        filled: true,
                        fillColor: const Color(0xFFF1F5F9),
                        contentPadding: const EdgeInsets.symmetric(vertical: 0, horizontal: 16),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(10),
                          borderSide: BorderSide.none,
                        ),
                      ),
                      onChanged: (v) => setState(() => _busqueda = v.trim()),
                    ),
                    const SizedBox(height: 10),
                    SingleChildScrollView(
                      scrollDirection: Axis.horizontal,
                      child: Row(
                        children: [
                          _chipCategoria('Todas', null),
                          _chipCategoria('Rojas (Incendio / Prohibición)', 'Rojas'),
                          _chipCategoria('Amarillas (Advertencia)', 'Amarillas'),
                          _chipCategoria('Azules (Obligación EPP)', 'Azules'),
                          _chipCategoria('Verdes (Evacuación / Socorro)', 'Verdes'),
                        ],
                      ),
                    ),
                  ],
                ),
              ),

              // Lista de Señales
              Expanded(
                child: senalesFiltradas.isEmpty
                    ? const Center(
                        child: EstadoVacio(
                          Icons.menu_book_outlined,
                          'No se encontraron señales normativas',
                          'Prueba ajustando el término de búsqueda o el filtro de categoría.',
                        ),
                      )
                    : ListView(
                        padding: const EdgeInsets.fromLTRB(20, 16, 20, 32),
                        children: [
                          _resumenNormativoCard(),
                          if (esDesktop)
                            // En Desktop: 2 columnas ordenadas
                            Wrap(
                              spacing: 16,
                              runSpacing: 16,
                              children: [
                                for (final s in senalesFiltradas)
                                  SizedBox(
                                    width: (1100 - 40 - 16) / 2,
                                    child: _cardSenal(s),
                                  ),
                              ],
                            )
                          else
                            // En Móvil: 1 columna
                            for (final s in senalesFiltradas) _cardSenal(s),
                        ],
                      ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _chipCategoria(String label, String? catId) {
    final seleccionada = (catId == null && _filtroCategoria == 'Todas') || _filtroCategoria == catId;
    final color = catId != null ? _colorCategoria(catId) : C.azul;

    return Padding(
      padding: const EdgeInsets.only(right: 8),
      child: FilterChip(
        label: Text(
          label,
          style: TextStyle(
            fontSize: 12,
            fontWeight: seleccionada ? FontWeight.w700 : FontWeight.w500,
            color: seleccionada ? Colors.white : C.navy,
          ),
        ),
        selected: seleccionada,
        selectedColor: color,
        backgroundColor: const Color(0xFFF1F5F9),
        showCheckmark: false,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        onSelected: (_) => setState(() => _filtroCategoria = catId ?? 'Todas'),
      ),
    );
  }

  Widget _resumenNormativoCard() {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFFEFF6FF),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: const Color(0xFFBFDBFE)),
      ),
      child: const Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(Icons.gavel, color: C.azul, size: 26),
          SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Marco Normativo Colombiano de Auditoría SST',
                  style: TextStyle(fontWeight: FontWeight.w700, color: C.navy, fontSize: 13.5),
                ),
                SizedBox(height: 4),
                Text(
                  'Catálogo oficial parametrizado según NTC 1461, Res. 2400 de 1979, NSR-10 (Títulos J y K), Decreto 1072 de 2015 e ISO 16069. Incluye checklists de campo, cálculo dimensional (S >= d²/2000), alturas de fijación y colores normativos.',
                  style: TextStyle(fontSize: 12, color: Color(0xFF1E3A8A), height: 1.35),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _cardSenal(SenalNormativaInfo s) {
    final color = _colorCategoria(s.categoria);

    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: const Color(0xFFE2E8F0)),
        boxShadow: const [BoxShadow(color: Color(0x06000000), blurRadius: 6, offset: Offset(0, 2))],
      ),
      child: Theme(
        data: Theme.of(context).copyWith(dividerColor: Colors.transparent),
        child: ExpansionTile(
          tilePadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 4),
          leading: Container(
            width: 8,
            height: 40,
            decoration: BoxDecoration(
              color: color,
              borderRadius: BorderRadius.circular(4),
            ),
          ),
          title: Text(
            s.elemento,
            style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 13.5, color: C.navy),
          ),
          subtitle: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 3),
              Text(
                'Norma: ${s.norma}',
                style: const TextStyle(fontSize: 11, color: C.texto2),
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
              const SizedBox(height: 4),
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                    decoration: BoxDecoration(
                      color: color.withValues(alpha: 0.12),
                      borderRadius: BorderRadius.circular(4),
                    ),
                    child: Text(
                      s.categoria,
                      style: TextStyle(fontSize: 10.5, fontWeight: FontWeight.w700, color: color),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Text(
                    'Altura: ${s.alturaMontaje.split('.').first}',
                    style: const TextStyle(fontSize: 10.5, color: C.texto2),
                  ),
                ],
              ),
            ],
          ),
          children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(14, 0, 14, 14),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Divider(),
                  // Ficha técnica
                  _filaTecnica('Norma aplicable:', s.norma),
                  _filaTecnica('Color de seguridad:', s.colorSeguridad),
                  _filaTecnica('Color de contraste:', s.colorContraste),
                  _filaTecnica('Forma geométrica:', s.formaGeometrica),
                  _filaTecnica('Tamaño recomendado:', s.tamanoRecomendado),
                  _filaTecnica('Cálculo dimensional:', s.formulaDimension),
                  _filaTecnica('Altura de montaje:', s.alturaMontaje),
                  if (s.demarcacionPiso.isNotEmpty)
                    _filaTecnica('Demarcación en piso:', s.demarcacionPiso),
                  if (s.fotoluminiscencia.isNotEmpty)
                    _filaTecnica('Fotoluminiscencia:', s.fotoluminiscencia),

                  const SizedBox(height: 10),
                  // Recomendación técnica
                  Container(
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: const Color(0xFFF8FAFC),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: const Color(0xFFE2E8F0)),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'Recomendación Técnica Oficial:',
                          style: TextStyle(fontWeight: FontWeight.w700, fontSize: 11.5, color: C.navy),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          s.recomendacion,
                          style: const TextStyle(fontSize: 11.5, color: Color(0xFF334155), height: 1.3),
                        ),
                      ],
                    ),
                  ),

                  const SizedBox(height: 10),
                  // Checklist de inspección
                  const Text(
                    'Puntos de Chequeo Obligatorios (Checklist SST):',
                    style: TextStyle(fontWeight: FontWeight.w700, fontSize: 12, color: C.navy),
                  ),
                  const SizedBox(height: 6),
                  for (final item in s.checklistSst)
                    Padding(
                      padding: const EdgeInsets.symmetric(vertical: 2.5),
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Icon(Icons.check_circle_outline, size: 14, color: C.verde),
                          const SizedBox(width: 8),
                          Expanded(
                            child: Text(
                              item,
                              style: const TextStyle(fontSize: 11.5, color: Color(0xFF334155)),
                            ),
                          ),
                        ],
                      ),
                    ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _filaTecnica(String k, String v) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2),
      child: RichText(
        text: TextSpan(
          style: const TextStyle(fontSize: 11.5, color: Color(0xFF334155)),
          children: [
            TextSpan(text: '$k ', style: const TextStyle(fontWeight: FontWeight.w700, color: C.navy)),
            TextSpan(text: v),
          ],
        ),
      ),
    );
  }
}
