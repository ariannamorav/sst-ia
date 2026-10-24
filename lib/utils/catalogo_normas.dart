/// Catálogo oficial de Normas de Seguridad y Salud en el Trabajo (SST)
/// Basado en NTC 1461, NTC-ISO 3864, NTC-ISO 7010, NSR-10 (Títulos J y K),
/// Resolución 2400 de 1979, Decreto 1072 de 2015, RETIE y Ley 1335 de 2009.
library;

class CategoriaSSTInfo {
  final String id;
  final String nombre;
  final String descripcion;
  final String colorSeguridad;
  final String colorContraste;
  final String colorHex;
  final String normaBase;
  final String formaGeometrica;
  final String coberturaMinima;

  const CategoriaSSTInfo({
    required this.id,
    required this.nombre,
    required this.descripcion,
    required this.colorSeguridad,
    required this.colorContraste,
    required this.colorHex,
    required this.normaBase,
    required this.formaGeometrica,
    required this.coberturaMinima,
  });
}

class SenalNormativaInfo {
  final String id;
  final String elemento;
  final String categoria;
  final String condicionDefault;
  final String norma;
  final String colorSeguridad;
  final String colorContraste;
  final String formaGeometrica;
  final String coberturaMinColor;
  final String tamanoRecomendado;
  final String formulaDimension;
  final String alturaMontaje;
  final String demarcacionPiso;
  final String fotoluminiscencia;
  final String recomendacion;
  final List<String> checklistSst;
  final List<String> palabrasClave;

  const SenalNormativaInfo({
    required this.id,
    required this.elemento,
    required this.categoria,
    required this.condicionDefault,
    required this.norma,
    required this.colorSeguridad,
    required this.colorContraste,
    required this.formaGeometrica,
    required this.coberturaMinColor,
    required this.tamanoRecomendado,
    required this.formulaDimension,
    required this.alturaMontaje,
    required this.demarcacionPiso,
    required this.fotoluminiscencia,
    required this.recomendacion,
    required this.checklistSst,
    required this.palabrasClave,
  });
}

class CatalogoNormasSST {
  static const Map<String, CategoriaSSTInfo> categorias = {
    'Rojas': CategoriaSSTInfo(
      id: 'Rojas',
      nombre: 'Contra Incendio y Prohibición',
      descripcion:
          'Identifica equipos contra incendios, pulsadores de alarma y comportamientos prohibidos que generan peligro inminente.',
      colorSeguridad: 'Rojo (Seguridad)',
      colorContraste: 'Blanco',
      colorHex: '#DC2626',
      normaBase: 'NTC 1461 / NTC-ISO 3864-1 / NSR-10 Título J / Res. 2400 de 1979',
      formaGeometrica:
          'Círculo con barra diagonal descendente a 45° (Prohibición) / Cuadrado o Rectángulo (Equipos de Extinción)',
      coberturaMinima: 'Rojo >= 35% en prohibición; >= 50% en equipos contra incendio',
    ),
    'Amarillas': CategoriaSSTInfo(
      id: 'Amarillas',
      nombre: 'Advertencia y Precaución',
      descripcion:
          'Alerta sobre riesgos físicos, eléctricos, desniveles, radiaciones y sustancias peligrosas.',
      colorSeguridad: 'Amarillo / Amarillo Anaranjado (Seguridad)',
      colorContraste: 'Negro',
      colorHex: '#D97706',
      normaBase: 'NTC 1461 / NTC-ISO 3864-1 / Res. 2400 de 1979 Art. 202 y 281',
      formaGeometrica: 'Triángulo equilátero con borde de contraste negro',
      coberturaMinima: 'Amarillo >= 50% de la superficie total',
    ),
    'Azules': CategoriaSSTInfo(
      id: 'Azules',
      nombre: 'Obligación y Uso de EPP',
      descripcion:
          'Indica acción de mando específica, comportamiento obligatorio y porte indispensable de Equipos de Protección Personal.',
      colorSeguridad: 'Azul (Seguridad)',
      colorContraste: 'Blanco',
      colorHex: '#2563EB',
      normaBase: 'NTC 1461 / NTC-ISO 7010 / Res. 2400 de 1979 Título IV',
      formaGeometrica: 'Círculo pleno',
      coberturaMinima: 'Azul >= 50% de la superficie total',
    ),
    'Verdes': CategoriaSSTInfo(
      id: 'Verdes',
      nombre: 'Evacuación, Salvamento y Emergencia',
      descripcion:
          'Señala rutas de escape, salidas de socorro, puntos de reunión, botiquines, camillas y duchas/lavaojos de socorro.',
      colorSeguridad: 'Verde (Seguridad)',
      colorContraste: 'Blanco',
      colorHex: '#059669',
      normaBase: 'NTC 1461 / ISO 16069 / NSR-10 Título K / Decreto 1072 de 2015',
      formaGeometrica: 'Cuadrado o Rectángulo',
      coberturaMinima: 'Verde >= 50% de la superficie total',
    ),
  };

  static const List<SenalNormativaInfo> senales = [
    SenalNormativaInfo(
      id: 'extintor',
      elemento: 'Extintor Portátil de Incendio',
      categoria: 'Rojas',
      condicionDefault: 'Requiere verificación',
      norma: 'NTC 2885 / NFPA 10 / NSR-10 (Título J, J.4) / NTC 1461',
      colorSeguridad: 'Rojo',
      colorContraste: 'Blanco',
      formaGeometrica: 'Cuadrado o Rectángulo con pictograma blanco',
      coberturaMinColor: '>= 50% de la superficie total',
      tamanoRecomendado: '20x20 cm (d <= 10m) | 30x30 cm (d <= 15m) | 42x42 cm (d <= 20m)',
      formulaDimension: 'S >= d² / 2000 (Área S en m² según distancia máxima de observación d)',
      alturaMontaje:
          'Manómetro/asa a máx. 1.50m del NPT (peso <= 18kg) o 1.10m (peso > 18kg). Señal de pared a 1.70m - 1.80m.',
      demarcacionPiso:
          'Cuadro de 1.00m x 1.00m en piso con franjas diagonales a 45° amarillo/negro o rojo/blanco de 10 cm de ancho (Res. 2400/79).',
      fotoluminiscencia:
          'Clase A (210 mcd/m² a 10 min) en áreas públicas; Clase B (40 mcd/m²) en áreas estándar.',
      checklistSst: [
        '1. Manómetro en franja verde de operatividad y aguja indicadora visible.',
        '2. Pasador metálico y precinto plástico de seguridad intactos sin manipulación.',
        '3. Tarjeta de inspección técnica mensual vigente y etiqueta de recarga al día.',
        '4. Manguera y boquilla libres de obstrucciones, fisuras o resequedad.',
        '5. Despeje frontal libre de 1.0 metro sin muebles, cajas o equipos que lo bloqueen.',
      ],
      recomendacion:
          'Instalar señal fotoluminiscente normalizada de 20x20cm a 1.80m sobre el extintor. Demarcar cuadro de despeje de 1.0x1.0m en piso y mantener manómetro en zona verde según NTC 2885 / NSR-10.',
      palabrasClave: ['extintor', 'extintores', 'pqs', 'co2', 'fuego', 'incendio', 'manguera', 'manometro', 'carga'],
    ),
    SenalNormativaInfo(
      id: 'gabinete_incendio',
      elemento: 'Gabinete Contra Incendio / Manguera y Válvula',
      categoria: 'Rojas',
      condicionDefault: 'Requiere verificación',
      norma: 'NTC 1669 / NFPA 14 / NSR-10 (Título J, J.4.2) / NTC 1461',
      colorSeguridad: 'Rojo',
      colorContraste: 'Blanco',
      formaGeometrica: 'Cuadrado o Rectángulo con pictograma de manguera',
      coberturaMinColor: '>= 50% de la superficie total',
      tamanoRecomendado: '30x30 cm (d <= 15m) | 40x40 cm (d <= 20m) en acrílico o poliestireno fotoluminiscente',
      formulaDimension: 'S >= d² / 2000',
      alturaMontaje: 'Gabinete con válvula entre 0.90m y 1.50m del NPT. Señalización superior a 1.80m - 2.00m.',
      demarcacionPiso: 'Área de maniobra de 1.00m de radio frontal libre y señalización de piso antideslizante.',
      fotoluminiscencia: 'Clase A (alta luminiscencia) exigida para edificaciones institucionales y comerciales.',
      checklistSst: [
        '1. Puerta de fácil apertura a 180° con vidrio o acrílico intacto y sin cerradura con llave.',
        '2. Manguera plegada o en devanadera sin estrangulaciones y con acople rápido certificado.',
        '3. Válvula angular de compuerta operativa, sin fugas ni corrosión en roscas.',
        '4. Hacha de pico, llave de spanner y boquilla de chorro-niebla presentes en su soporte.',
        '5. Radio de 1 metro totalmente libre de objetos y señal visible a más de 15 metros.',
      ],
      recomendacion:
          'Garantizar radio libre de 1.0 metro alrededor del gabinete. Instalar señal fotoluminiscente de 30x30cm a 1.80m y verificar apertura a 180° y operatividad de la válvula según NTC 1669 / NSR-10.',
      palabrasClave: ['gabinete', 'manguera contra incendio', 'boca de incendio', 'siamesa', 'devanadera', 'spanner'],
    ),
    SenalNormativaInfo(
      id: 'prohibido_fumar',
      elemento: 'Señal: Prohibido Fumar y Encender Fuego',
      categoria: 'Rojas',
      condicionDefault: 'Conforme',
      norma: 'Ley 1335 de 2009 (Arts. 19-20) / NTC 1461 / NTC-ISO 7010 (P002) / Res. 2400/79',
      colorSeguridad: 'Rojo (Borde circular y banda diagonal a 45°)',
      colorContraste: 'Blanco (Fondo) y Negro (Pictograma de cigarrillo encendido)',
      formaGeometrica: 'Círculo con borde rojo y banda transversal descendente a 45°',
      coberturaMinColor: 'Rojo >= 35% de la superficie total de la señal',
      tamanoRecomendado: 'Diámetro 20 cm o 20x30 cm con texto legal (d <= 10m) | Diámetro 30 cm (d <= 15m)',
      formulaDimension: 'd = D * 40 (d: distancia máx. visual, D: diámetro de la señal)',
      alturaMontaje: 'Entre 1.60m y 1.80m del NPT en accesos principales, pasillos y áreas cerradas.',
      demarcacionPiso: 'No aplica demarcación horizontal.',
      fotoluminiscencia: 'Vinilo reflectivo o poliestireno calibre 1mm con tintas UV resistentes.',
      checklistSst: [
        '1. Señal visible en todas las puertas de acceso institucional y áreas comunes.',
        '2. Texto complementario legal obligatorio: "Espacio 100% Libre de Humo de Tabaco - Ley 1335 de 2009".',
        '3. Ausencia total de ceniceros en áreas de oficinas, laboratorios y aulas.',
        '4. Banda roja diagonal cubriendo con precisión el pictograma a 45° sin desprendimientos.',
      ],
      recomendacion:
          'Fijar señales circulares reglamentarias de 20cm de diámetro a 1.70m de altura en todos los accesos del bloque, con la leyenda "Espacio 100% Libre de Humo de Tabaco" conforme a la Ley 1335 de 2009 y NTC 1461.',
      palabrasClave: ['prohibido fumar', 'no fumar', 'fumar', 'cigarro', 'llama abierta', 'cerillo', 'tabaco', 'humo'],
    ),
    SenalNormativaInfo(
      id: 'prohibido_celular',
      elemento: 'Señal: Prohibido el Uso de Teléfono Móvil',
      categoria: 'Rojas',
      condicionDefault: 'Conforme',
      norma: 'NTC 1461 / NTC-ISO 7010 (P013) / Decreto 1072 de 2015 (Control de Actos Inseguros)',
      colorSeguridad: 'Rojo',
      colorContraste: 'Blanco (Fondo) y Negro (Pictograma)',
      formaGeometrica: 'Círculo con banda transversal descendente a 45°',
      coberturaMinColor: 'Rojo >= 35% de la superficie total',
      tamanoRecomendado: 'Diámetro 20 cm o formato 20x30 cm con texto preventivo',
      formulaDimension: 'd = D * 40',
      alturaMontaje: '1.60m a 1.75m del NPT en descansos de escaleras, laboratorios y zonas de maniobra.',
      demarcacionPiso: 'Franja amarilla de 10 cm en descansos si es zona de alto tránsito peatonal.',
      fotoluminiscencia: 'Lámina de poliestireno o acrílico 2mm fijada con cinta doble faz 3M o tornillos.',
      checklistSst: [
        '1. Señal ubicada en descansos de escaleras para evitar tropiezos y caídas por distracción.',
        '2. Pictograma normalizado NTC-ISO 7010 con banda roja descendente a 45°.',
        '3. Texto complementario: "Atención: use el pasamanos y evite el celular durante el desplazamiento".',
        '4. Buen estado de conservación, sin rayones ni decoloración por luz solar.',
      ],
      recomendacion:
          'Instalar señales de prohibición de celular de 20x20cm en los descansos de escaleras y laboratorios críticos para mitigar caídas al mismo y distinto nivel según Decreto 1072 de 2015 y NTC 1461.',
      palabrasClave: ['prohibido celular', 'no celular', 'prohibido movil', 'telefono', 'celular', 'smartphone', 'distraccion'],
    ),
    SenalNormativaInfo(
      id: 'riesgo_electrico',
      elemento: 'Señal: Peligro Riesgo Eléctrico / Alta Tensión',
      categoria: 'Amarillas',
      condicionDefault: 'Requiere verificación',
      norma: 'RETIE (Reglamento Técnico de Instalaciones Eléctricas) / NTC 1461 / NTC-ISO 7010 (W012)',
      colorSeguridad: 'Amarillo / Amarillo Anaranjado',
      colorContraste: 'Negro (Borde triangular y pictograma de rayo)',
      formaGeometrica: 'Triángulo equilátero con vértice superior',
      coberturaMinColor: 'Amarillo >= 50% de la superficie total',
      tamanoRecomendado: 'Lado 20 cm (d <= 8m) | Lado 30 cm (d <= 12m) | Formato combinado 30x20 cm',
      formulaDimension: 'd = L * 35 (L: longitud del lado del triángulo equilátero)',
      alturaMontaje: 'Fijada directamente sobre la tapa frontal del tablero a 1.50m - 1.70m del NPT.',
      demarcacionPiso:
          'Demarcación perimetral de 10 cm con franjas diagonales a 45° amarillo/negro dejando 0.80m de despeje frontal.',
      fotoluminiscencia: 'Vinilo reflectivo Grado Ingeniería o Poliestireno 1mm ignífugo.',
      checklistSst: [
        '1. Tablero cerrado con llave y directorio de circuitos legible y actualizado.',
        '2. Mandil protector interno (tapa cubre-barras) instalado sin partes vivas expuestas.',
        '3. Ausencia de humedad, filtraciones o acumulación de polvo dentro del gabinete.',
        '4. Despeje frontal mínimo de 0.80 metros libre de obstáculos para maniobra de emergencia.',
        '5. Certificación de conexión al sistema de puesta a tierra (SPT).',
      ],
      recomendacion:
          'Instalar señal triangular de peligro eléctrico de 20cm en el exterior del tablero eléctrico según RETIE y NTC 1461. Demarcar zona de maniobra de 80cm en piso con franjas amarillo/negro a 45°.',
      palabrasClave: ['riesgo electrico', 'tablero', 'alta tension', 'peligro electrico', 'voltaje', 'electrocutar', 'subestacion', 'retie'],
    ),
    SenalNormativaInfo(
      id: 'piso_resbaloso',
      elemento: 'Señal: Peligro Superficie Resbaladiza / Piso Húmedo',
      categoria: 'Amarillas',
      condicionDefault: 'Requiere verificación',
      norma: 'Resolución 2400 de 1979 (Art. 17) / NTC 1461 / OSHA 1910.22',
      colorSeguridad: 'Amarillo',
      colorContraste: 'Negro',
      formaGeometrica: 'Triángulo equilátero o Caballete tijera plegable bilingüe',
      coberturaMinColor: 'Amarillo >= 50% de la superficie total',
      tamanoRecomendado: 'Caballete móvil de 60x30 cm con pictograma de persona resbalando a doble cara',
      formulaDimension: 'd = L * 35',
      alturaMontaje: 'Colocado a nivel de piso en el perímetro inmediato de la zona mojada o en trapeado.',
      demarcacionPiso: 'Cintas antideslizantes fotoluminiscentes de 5 cm de ancho en bordes de huellas de escaleras.',
      fotoluminiscencia: 'Polipropileno de alto impacto de color amarillo tráfico de alta visibilidad.',
      checklistSst: [
        '1. Caballete desplegado de forma visible antes de iniciar el lavado o trapeado del piso.',
        '2. Pisos secos y libres de grasas o productos de limpieza resbalosos no retirados.',
        '3. Presencia de felpudos antideslizantes absorbentes en las puertas de ingreso los días de lluvia.',
        '4. Cintas antideslizantes colocadas en la totalidad de peldaños de escaleras.',
      ],
      recomendacion:
          'Desplegar de forma obligatoria caballetes de aviso de piso mojado durante rutinas de aseo conforme al Art. 17 de la Res. 2400 de 1979. Instalar cintas antideslizantes en escaleras.',
      palabrasClave: ['piso resbaloso', 'piso mojado', 'resbalon', 'caida', 'trapeado', 'humedo', 'antideslizante'],
    ),
    SenalNormativaInfo(
      id: 'uso_casco',
      elemento: 'Señal: Uso Obligatorio de Casco de Seguridad',
      categoria: 'Azules',
      condicionDefault: 'Conforme',
      norma: 'NTC 1461 / NTC-ISO 7010 (M014) / NTC 1523 / Res. 2400/79 (Art. 177)',
      colorSeguridad: 'Azul (Seguridad)',
      colorContraste: 'Blanco',
      formaGeometrica: 'Círculo pleno',
      coberturaMinColor: 'Azul >= 50% de la superficie total',
      tamanoRecomendado: 'Diámetro 20 cm (d <= 8m) | Diámetro 30 cm (d <= 12m) | 20x30 cm con texto',
      formulaDimension: 'd = D * 40',
      alturaMontaje: '1.60m - 1.80m en pórticos de acceso a obras, bodegas, talleres y zonas de izaje.',
      demarcacionPiso: 'Línea de demarcación amarilla continua de 10 cm que defina el inicio de la zona EPP.',
      fotoluminiscencia: 'Poliestireno 1mm o vinilo adhesivo de alta adherencia para muros o lámina.',
      checklistSst: [
        '1. Todo el personal en el área porta casco Tipo I o II con barbuquejo de 3 o 4 puntos colocado.',
        '2. Cascos libres de fisuras, perforaciones caseras o deterioro por radiación solar.',
        '3. Suspensión interna (tafilete) regulada adecuadamente a la cabeza del trabajador.',
        '4. Señalización visible antes de cruzar la línea perimetral de riesgo de caída de objetos.',
      ],
      recomendacion:
          'Fijar señal circular reglamentaria de 20cm de diámetro a 1.70m de altura en el acceso a la zona operativa. Exigir casco con barbuquejo según NTC 1523 y Resolución 2400 de 1979.',
      palabrasClave: ['uso de casco', 'casco', 'proteccion cabeza', 'casco de seguridad', 'barbuquejo', 'obra'],
    ),
    SenalNormativaInfo(
      id: 'uso_gafas',
      elemento: 'Señal: Uso Obligatorio de Gafas / Protección Ocular',
      categoria: 'Azules',
      condicionDefault: 'Conforme',
      norma: 'NTC 1461 / NTC-ISO 7010 (M004) / ANSI Z87.1 / Res. 2400/79 (Art. 178)',
      colorSeguridad: 'Azul (Seguridad)',
      colorContraste: 'Blanco',
      formaGeometrica: 'Círculo pleno',
      coberturaMinColor: 'Azul >= 50% de la superficie total',
      tamanoRecomendado: 'Diámetro 20 cm o formato 20x30 cm con texto legal de obligatoriedad',
      formulaDimension: 'd = D * 40',
      alturaMontaje: '1.60m - 1.75m en la entrada a laboratorios de química, talleres de mecanizado y pulido.',
      demarcacionPiso: 'Franja amarilla de delimitación frente a bancos de máquinas herramientas.',
      fotoluminiscencia: 'Poliestireno 1mm.',
      checklistSst: [
        '1. Monogafas o lentes de seguridad con sello ANSI Z87.1 y protección lateral.',
        '2. Lentes limpios, sin rayones profundos que reduzcan la visibilidad del operador.',
        '3. Prohibición expresa de uso de gafas comunes de aumento como sustituto de gafas de seguridad.',
        '4. Señal fijada en el umbral visual de cada máquina generadora de esquirlas o salpicaduras.',
      ],
      recomendacion:
          'Ubicar señal de protección ocular de 20cm en el pórtico de laboratorios y puestos de esmerilado/química. Exigir gafas certificadas ANSI Z87.1 conforme a la Res. 2400 de 1979 Art. 178.',
      palabrasClave: ['uso de gafas', 'gafas de seguridad', 'proteccion ocular', 'lentes', 'monogafas', 'esquirlas'],
    ),
    SenalNormativaInfo(
      id: 'salida_emergencia',
      elemento: 'Señal: Salida de Emergencia / Socorro',
      categoria: 'Verdes',
      condicionDefault: 'Conforme',
      norma: 'NSR-10 (Título K, K.3.8) / NTC 1461 / ISO 16069 / NTC-ISO 7010 (E001/E002)',
      colorSeguridad: 'Verde (Seguridad)',
      colorContraste: 'Blanco',
      formaGeometrica: 'Rectángulo horizontal con silueta de persona corriendo hacia la puerta',
      coberturaMinColor: 'Verde >= 50% de la superficie total',
      tamanoRecomendado: '30x15 cm (d <= 10m) | 40x20 cm (d <= 15m) | 60x30 cm (d <= 20m)',
      formulaDimension: 'S >= d² / 2000',
      alturaMontaje:
          'Señal alta montada directamente sobre el dintel de la puerta de salida a 2.10m - 2.30m del NPT. Señal baja complementaria a 0.30m del piso.',
      demarcacionPiso:
          'Demarcación perimetral de apertura de puerta con cuadrante rayado amarillo/negro de 10 cm para evitar que sea obstaculizada.',
      fotoluminiscencia:
          'Clase A (alta luminiscencia - 210 mcd/m² a 10 min y 29 mcd/m² a 60 min) certificada DIN 67510.',
      checklistSst: [
        '1. Puerta de evacuación con apertura hacia afuera en sentido de la salida y barra antipánico.',
        '2. Puerta libre de cerrojos, candados, cadenas o llaves durante la presencia de personas.',
        '3. Ancho útil de puerta mínimo de 90 cm a 1.20 metros según cálculo de carga de ocupación NSR-10.',
        '4. Señal fotoluminiscente Clase A visible aún con corte total de fluido eléctrico.',
        '5. Pasillo de salida totalmente despejado sin cajas, muebles ni papeleras que estrechen la vía.',
      ],
      recomendacion:
          'Instalar señal fotoluminiscente Clase A sobre el dintel de la salida a 2.20m según NSR-10 K y NTC 1461. Dotar con barra antipánico y mantener el pasillo con ancho libre mínimo de 1.20m.',
      palabrasClave: ['salida de emergencia', 'salida de socorro', 'puerta de escape', 'evacuacion', 'escape', 'barra antipanico'],
    ),
    SenalNormativaInfo(
      id: 'ruta_evacuacion',
      elemento: 'Señal: Ruta de Evacuación / Flecha Direccional',
      categoria: 'Verdes',
      condicionDefault: 'Conforme',
      norma: 'ISO 16069 / NTC 1461 / NSR-10 (Título K) / Decreto 1072 de 2015',
      colorSeguridad: 'Verde (Seguridad)',
      colorContraste: 'Blanco',
      formaGeometrica: 'Rectángulo con flecha direccional y pictograma de escape',
      coberturaMinColor: 'Verde >= 50% de la superficie total',
      tamanoRecomendado: '30x15 cm (d <= 10m) | 40x20 cm (d <= 15m)',
      formulaDimension: 'S >= d² / 2000',
      alturaMontaje:
          'Intermedia: 1.60m - 1.80m en paredes de pasillos. Nivel de zócalo: 15cm - 30cm del piso para guiar el escape gateando bajo humo.',
      demarcacionPiso:
          'Flechas fotoluminiscentes o franjas verdes continuas de 10 cm en el piso cada 5 metros.',
      fotoluminiscencia: 'Clase A (210 mcd/m² a 10 min).',
      checklistSst: [
        '1. Señales direccionales colocadas en todos los cambios de dirección, cruces de pasillos y bifurcaciones.',
        '2. Distancia máxima entre señales consecutivas de 15 a 20 metros en pasillos rectos.',
        '3. Señalización continua que conduce sin interrupción hasta el punto de encuentro exterior.',
        '4. Flechas apuntando inequívocamente hacia la salida más próxima y segura.',
      ],
      recomendacion:
          'Colocar señales fotoluminiscentes de ruta de evacuación cada 15 metros a 1.70m de altura y a nivel de zócalo (30cm) conforme a la norma ISO 16069 y NSR-10 Título K.',
      palabrasClave: ['ruta de evacuacion', 'flecha de evacuacion', 'direccion de escape', 'via de escape', 'flecha verde'],
    ),
    SenalNormativaInfo(
      id: 'camilla_emergencia',
      elemento: 'Camilla Rígida de Inmovilización Espinal',
      categoria: 'Verdes',
      condicionDefault: 'Requiere verificación',
      norma: 'Decreto 1072 de 2015 (Art. 2.2.4.6.25) / Resolución 2400 de 1979 (Art. 164) / NTC 1461',
      colorSeguridad: 'Verde (Seguridad)',
      colorContraste: 'Blanco (Pictograma de cruz o camilla)',
      formaGeometrica: 'Cuadrado o Rectángulo',
      coberturaMinColor: 'Verde >= 50% de la superficie total',
      tamanoRecomendado: '30x20 cm o 30x30 cm fijada sobre el soporte de la camilla',
      formulaDimension: 'S >= d² / 2000',
      alturaMontaje:
          'Camilla suspendida verticalmente en soporte metálico o gabinete con base a 0.30m y señal a 1.80m - 2.00m.',
      demarcacionPiso: 'Cuadro de despeje de 1.00m x 0.50m en piso para acceso rápido.',
      fotoluminiscencia: 'Clase B estándar o vinilo reflectivo.',
      checklistSst: [
        '1. Camilla rígida de polietileno de alta densidad (espinal larga) sin fisuras ni astillamientos.',
        '2. Juego completo de correas tipo araña (arnés de sujeción corporal de 10 puntos) con velcro o broches operativos.',
        '3. Inmovilizador de cabeza (dameros laterales) y collarín cervical graduable presentes.',
        '4. Camilla protegida con funda impermeable protectora contra el polvo y la intemperie.',
        '5. Despeje absoluto para retiro inmediato sin herramientas ni llaves.',
      ],
      recomendacion:
          'Instalar camilla rígida espinal con juego de correas tipo araña e inmovilizador cefálico en soporte de pared a 1.80m señalizada con letrero verde según Resolución 2400 de 1979 Art. 164 y Dec. 1072/15.',
      palabrasClave: ['camilla', 'camilla rigida', 'inmovilizacion', 'primeros auxilios', 'correas tipo arana', 'espinal'],
    ),
    SenalNormativaInfo(
      id: 'botiquin',
      elemento: 'Botiquín de Primeros Auxilios (Tipo A / B)',
      categoria: 'Verdes',
      condicionDefault: 'Requiere verificación',
      norma: 'Resolución 0705 de 2007 (Secretaría de Salud) / Decreto 1072 de 2015 / NTC 1461',
      colorSeguridad: 'Verde (Seguridad)',
      colorContraste: 'Blanco (Cruz de primeros auxilios)',
      formaGeometrica: 'Cuadrado o Rectángulo',
      coberturaMinColor: 'Verde >= 50% de la superficie total',
      tamanoRecomendado: '20x20 cm o 30x30 cm',
      formulaDimension: 'S >= d² / 2000',
      alturaMontaje: 'Gabinete o maletín ubicado a 1.50m del NPT. Señal de cruz verde a 1.70m - 1.80m.',
      demarcacionPiso: 'No requiere demarcación de piso, pero sí despeje visual.',
      fotoluminiscencia: 'Poliestireno fotoluminiscente o acrílico.',
      checklistSst: [
        '1. Gabinete metálico o maletín plástico de fácil transporte con chapa sin llave (acceso libre).',
        '2. Dotación completa según Resolución 0705 de 2007 (gasas estériles, vendas elásticas, micropore, suero fisiológico).',
        '3. Cero medicamentos ingeribles (acetaminofén, aspirinas, antibióticos) prohibidos por norma.',
        '4. Lista de chequeo de inventario con fechas de vencimiento al día y formato de reposición.',
      ],
      recomendacion:
          'Dotar botiquín Tipo A/B con elementos de curación limpios según Resolución 0705 de 2007 (sin medicamentos orales). Fijar señal de cruz de socorro a 1.70m según NTC 1461.',
      palabrasClave: ['botiquin', 'primeros auxilios', 'curacion', 'gasas', 'vendas', 'urgencias', 'cruz verde'],
    ),
    SenalNormativaInfo(
      id: 'punto_encuentro',
      elemento: 'Señal: Punto de Encuentro / Zona Segura',
      categoria: 'Verdes',
      condicionDefault: 'Conforme',
      norma: 'Decreto 1072 de 2015 (Plan de Emergencias) / NTC 1461 / ISO 7010 (E007)',
      colorSeguridad: 'Verde (Seguridad)',
      colorContraste: 'Blanco (Cuatro flechas convergiendo hacia el centro)',
      formaGeometrica: 'Cuadrado',
      coberturaMinColor: 'Verde >= 50% de la superficie total',
      tamanoRecomendado: '60x60 cm o 80x80 cm en poste exterior (d <= 25m - 35m)',
      formulaDimension: 'S >= d² / 2000',
      alturaMontaje: 'Montado en poste metálico exterior a altura >= 2.20m para visibilidad sobre multitudes.',
      demarcacionPiso: 'Círculo exterior pintado en piso de 2.00m x 2.00m en pintura epóxica o de tráfico amarilla/blanca.',
      fotoluminiscencia: 'Lámina metálica galvanizada con vinilo reflectivo Grado Alta Intensidad.',
      checklistSst: [
        '1. Ubicado en patio o zona exterior abierta libre de líneas eléctricas aéreas o caída de vidrios.',
        '2. Letrero metálico visible desde todos los accesos peatonales del bloque.',
        '3. Círculo o área delimitada en piso con número o letra de punto de encuentro.',
        '4. Espacio suficiente para albergar la carga de ocupación total de la sede.',
      ],
      recomendacion:
          'Fijar letrero metálico reflectivo de 60x60cm a 2.30m de altura en poste exterior y pintar delimitación circular en piso de 2.0m de diámetro según Decreto 1072 de 2015 y NTC 1461.',
      palabrasClave: ['punto de encuentro', 'zona segura', 'reunion', 'evacuacion exterior', 'patio seguro'],
    ),
  ];

  /// Busca una señal normativa por id o texto clave
  static SenalNormativaInfo? buscarPorTexto(String texto) {
    final t = _normalizar(texto);
    for (final s in senales) {
      if (t.contains(s.id)) return s;
      for (final p in s.palabrasClave) {
        if (t.contains(_normalizar(p))) return s;
      }
    }
    return null;
  }

  static String _normalizar(String s) {
    const de = 'áéíóúüñ', a = 'aeiouun';
    var res = s.toLowerCase();
    for (var i = 0; i < de.length; i++) {
      res = res.replaceAll(de[i], a[i]);
    }
    return res;
  }
}
