"""
Catálogo normativo de Seguridad y Salud en el Trabajo (SST).
Basado en estándares internacionales (ISO 7010, OSHA) y normas técnicas nacionales (NTP 399.010-1).
"""
from typing import Dict, Any, List

CATEGORIAS_SST = {
    "Rojas": {
        "nombre": "Contra Incendio y Prohibición",
        "descripcion": "Identifica equipos contra incendios, paradas de emergencia y comportamientos prohibidos que generan peligro inminente.",
        "color_seguridad": "Rojo (Seguridad)",
        "color_contraste": "Blanco",
        "color_hex": "#dc2626",
        "bg_color": "#fee2e2",
        "icono": "fire",
        "norma_base": "NTC 1461 / NTC-ISO 3864-1 / NSR-10 Título J / Res. 2400 de 1979",
        "formas": ["Círculo con barra diagonal descendente a 45° (Prohibición)", "Cuadrado o Rectángulo (Equipos de Extinción)"],
        "cobertura_minima": "Rojo >= 35% de la superficie en prohibición; >= 50% en equipos de extinción"
    },
    "Amarillas": {
        "nombre": "Advertencia y Precaución",
        "descripcion": "Alerta sobre riesgos físicos, químicos, eléctricos, desniveles, radiaciones y peligros potenciales.",
        "color_seguridad": "Amarillo / Amarillo Anaranjado (Seguridad)",
        "color_contraste": "Negro",
        "color_hex": "#d97706",
        "bg_color": "#fef3c7",
        "icono": "alert-triangle",
        "norma_base": "NTC 1461 / NTC-ISO 3864-1 / Res. 2400 de 1979 Art. 202 y 281",
        "formas": ["Triángulo equilátero con borde de contraste negro"],
        "cobertura_minima": "Amarillo >= 50% de la superficie total"
    },
    "Azules": {
        "nombre": "Obligación y Uso de EPP",
        "descripcion": "Indica acción de mando específica, comportamiento obligatorio y porte indispensable de Equipos de Protección Personal.",
        "color_seguridad": "Azul (Seguridad)",
        "color_contraste": "Blanco",
        "color_hex": "#2563eb",
        "bg_color": "#dbeafe",
        "icono": "shield-alert",
        "norma_base": "NTC 1461 / NTC-ISO 7010 / Res. 2400 de 1979 Título IV",
        "formas": ["Círculo pleno"],
        "cobertura_minima": "Azul >= 50% de la superficie total"
    },
    "Verdes": {
        "nombre": "Evacuación, Salvamento y Emergencia",
        "descripcion": "Señala rutas de escape, salidas de emergencia, puntos de reunión, botiquines, camillas y duchas/lavaojos de socorro.",
        "color_seguridad": "Verde (Seguridad)",
        "color_contraste": "Blanco",
        "color_hex": "#059669",
        "bg_color": "#d1fae5",
        "icono": "heart-pulse",
        "norma_base": "NTC 1461 / ISO 16069 / NSR-10 Título K / Decreto 1072 de 2015",
        "formas": ["Cuadrado o Rectángulo"],
        "cobertura_minima": "Verde >= 50% de la superficie total"
    }
}

CATALOGO_SENALES = {
    "extintor": {
        "elemento": "Extintor Portátil de Incendio",
        "categoria": "Rojas",
        "condicion_default": "Requiere verificación",
        "norma": "NTC 2885 / NFPA 10 / NSR-10 (Título J, J.4) / NTC 1461",
        "color_seguridad": "Rojo",
        "color_contraste": "Blanco",
        "forma_geometrica": "Cuadrado o Rectángulo con pictograma blanco",
        "cobertura_min_color": ">= 50% de la superficie total",
        "tamano_recomendado": "20x20 cm (d <= 10m) | 30x30 cm (d <= 15m) | 42x42 cm (d <= 20m)",
        "formula_dimension": "S >= d² / 2000 (Área S en m² según distancia máxima de observación d)",
        "altura_montaje": "Manómetro/asa a máx. 1.50m del NPT (peso <= 18kg) o 1.10m (peso > 18kg). Señal de pared a 1.70m - 1.80m.",
        "demarcacion_piso": "Cuadro de 1.00m x 1.00m en piso con franjas diagonales a 45° amarillo/negro o rojo/blanco de 10 cm de ancho (Res. 2400/79).",
        "fotoluminiscencia": "Clase A (210 mcd/m² a 10 min) en áreas públicas; Clase B (40 mcd/m²) en áreas estándar.",
        "checklist_sst": [
            "1. Manómetro en franja verde de operatividad y aguja indicadora visible.",
            "2. Pasador metálico y precinto plástico de seguridad intactos sin manipulación.",
            "3. Tarjeta de inspección técnica mensual vigente y etiqueta de recarga al día.",
            "4. Manguera y boquilla libres de obstrucciones, fisuras o resequedad.",
            "5. Despeje frontal libre de 1.0 metro sin muebles, cajas o equipos que lo bloqueen."
        ],
        "recomendacion": "Instalar señal fotoluminiscente normalizada de 20x20cm a 1.80m sobre el extintor. Demarcar cuadro de despeje de 1.0x1.0m en piso y mantener manómetro en zona verde según NTC 2885 / NSR-10.",
        "palabras_clave": ["extintor", "extintores", "pqs", "co2", "fuego", "incendio", "manguera", "manometro", "carga"]
    },
    "gabinete_incendio": {
        "elemento": "Gabinete Contra Incendio / Manguera y Válvula",
        "categoria": "Rojas",
        "condicion_default": "Requiere verificación",
        "norma": "NTC 1669 / NFPA 14 / NSR-10 (Título J, J.4.2) / NTC 1461",
        "color_seguridad": "Rojo",
        "color_contraste": "Blanco",
        "forma_geometrica": "Cuadrado o Rectángulo con pictograma de manguera",
        "cobertura_min_color": ">= 50% de la superficie total",
        "tamano_recomendado": "30x30 cm (d <= 15m) | 40x40 cm (d <= 20m) en acrílico o poliestireno fotoluminiscente",
        "formula_dimension": "S >= d² / 2000",
        "altura_montaje": "Gabinete con válvula entre 0.90m y 1.50m del NPT. Señalización superior a 1.80m - 2.00m.",
        "demarcacion_piso": "Área de maniobra de 1.00m de radio frontal libre y señalización de piso antideslizante.",
        "fotoluminiscencia": "Clase A (alta luminiscencia) exigida para edificaciones institucionales y comerciales.",
        "checklist_sst": [
            "1. Puerta de fácil apertura a 180° con vidrio o acrílico intacto y sin cerradura con llave.",
            "2. Manguera plegada o en devanadera sin estrangulaciones y con acople rápido certificado.",
            "3. Válvula angular de compuerta operativa, sin fugas ni corrosión en roscas.",
            "4. Hacha de pico, llave de spanner y boquilla de chorro-niebla presentes en su soporte.",
            "5. Radio de 1 metro totalmente libre de objetos y señal visible a más de 15 metros."
        ],
        "recomendacion": "Garantizar radio libre de 1.0 metro alrededor del gabinete. Instalar señal fotoluminiscente de 30x30cm a 1.80m y verificar apertura a 180° y operatividad de la válvula según NTC 1669 / NSR-10.",
        "palabras_clave": ["gabinete", "manguera contra incendio", "boca de incendio", "siamesa", "devanadera", "spanner"]
    },
    "prohibido_fumar": {
        "elemento": "Señal: Prohibido Fumar y Encender Fuego",
        "categoria": "Rojas",
        "condicion_default": "Conforme",
        "norma": "Ley 1335 de 2009 (Arts. 19-20) / NTC 1461 / NTC-ISO 7010 (P002) / Res. 2400/79",
        "color_seguridad": "Rojo (Borde circular y banda diagonal a 45°)",
        "color_contraste": "Blanco (Fondo) y Negro (Pictograma de cigarrillo encendido)",
        "forma_geometrica": "Círculo con borde rojo y banda transversal descendente de izquierda a derecha a 45°",
        "cobertura_min_color": "Rojo >= 35% de la superficie total de la señal",
        "tamano_recomendado": "Diámetro 20 cm o 20x30 cm con texto legal (d <= 10m) | Diámetro 30 cm (d <= 15m)",
        "formula_dimension": "d = D * 40 (d: distancia máx. visual, D: diámetro de la señal)",
        "altura_montaje": "Entre 1.60m y 1.80m del NPT en accesos principales, pasillos y áreas cerradas.",
        "demarcacion_piso": "No aplica demarcación horizontal.",
        "fotoluminiscencia": "Vinilo reflectivo o poliestireno calibre 1mm con tintas UV resistentes.",
        "checklist_sst": [
            "1. Señal visible en todas las puertas de acceso institucional y áreas comunes.",
            "2. Texto complementario legal obligatorio: 'Espacio 100% Libre de Humo de Tabaco - Ley 1335 de 2009'.",
            "3. Ausencia total de ceniceros en áreas de oficinas, laboratorios y aulas.",
            "4. Banda roja diagonal cubriendo con precisión el pictograma a 45° sin desprendimientos."
        ],
        "recomendacion": "Fijar señales circulares reglamentarias de 20cm de diámetro a 1.70m de altura en todos los accesos del bloque, con la leyenda 'Espacio 100% Libre de Humo de Tabaco' conforme a la Ley 1335 de 2009 y NTC 1461.",
        "palabras_clave": ["prohibido fumar", "no fumar", "fumar", "cigarro", "llama abierta", "cerillo", "tabaco", "humo"]
    },
    "prohibido_celular": {
        "elemento": "Señal: Prohibido el Uso de Teléfono Móvil",
        "categoria": "Rojas",
        "condicion_default": "Conforme",
        "norma": "NTC 1461 / NTC-ISO 7010 (P013) / Decreto 1072 de 2015 (Control de Actos Inseguros)",
        "color_seguridad": "Rojo",
        "color_contraste": "Blanco (Fondo) y Negro (Pictograma)",
        "forma_geometrica": "Círculo con banda transversal descendente a 45°",
        "cobertura_min_color": "Rojo >= 35% de la superficie total",
        "tamano_recomendado": "Diámetro 20 cm o formato 20x30 cm con texto preventivo",
        "formula_dimension": "d = D * 40",
        "altura_montaje": "1.60m a 1.75m del NPT en descansos de escaleras, laboratorios y zonas de maniobra.",
        "demarcacion_piso": "Franja amarilla de 10 cm en descansos si es zona de alto tránsito peatonal.",
        "fotoluminiscencia": "Lámina de poliestireno o acrílico 2mm fijada con cinta doble faz 3M o tornillos.",
        "checklist_sst": [
            "1. Señal ubicada en descansos de escaleras para evitar tropiezos y caídas por distracción.",
            "2. Pictograma normalizado NTC-ISO 7010 con banda roja descendente a 45°.",
            "3. Texto complementario: 'Atención: use el pasamanos y evite el celular durante el desplazamiento'.",
            "4. Buen estado de conservación, sin rayones ni decoloración por luz solar."
        ],
        "recomendacion": "Instalar señales de prohibición de celular de 20x20cm en los descansos de escaleras y laboratorios críticos para mitigar caídas al mismo y distinto nivel según Decreto 1072 de 2015 y NTC 1461.",
        "palabras_clave": ["prohibido celular", "no celular", "prohibido movil", "telefono", "celular", "smartphone", "distraccion"]
    },
    "prohibido_paso": {
        "elemento": "Señal: Prohibido el Paso a Personal No Autorizado",
        "categoria": "Rojas",
        "condicion_default": "Conforme",
        "norma": "NTC 1461 / NTC-ISO 7010 (P006) / Res. 2400 de 1979",
        "color_seguridad": "Rojo",
        "color_contraste": "Blanco (Fondo) y Negro (Pictograma de mano alzada o silueta)",
        "forma_geometrica": "Círculo con banda diagonal descendente a 45°",
        "cobertura_min_color": "Rojo >= 35% de la superficie total",
        "tamano_recomendado": "30x20 cm o 30x40 cm con texto restrictivo",
        "formula_dimension": "S >= d² / 2000",
        "altura_montaje": "1.60m - 1.70m en puertas de acceso a subestaciones, cuartos de bombas y tableros.",
        "demarcacion_piso": "Línea de demarcación amarilla continua de 10 cm que defina el límite físico.",
        "fotoluminiscencia": "Poliestireno 1mm o lámina galvanizada con pintura electrostática.",
        "checklist_sst": [
            "1. Puerta de acceso con cerradura con llave y control estricto de ingreso.",
            "2. Señal fijada en la hoja de la puerta o en el marco a la altura visual de lectura.",
            "3. Demarcación de advertencia en el piso previo al umbral de entrada.",
            "4. Registro de bitácora de ingreso de personal autorizado visible."
        ],
        "recomendacion": "Fijar señal restrictiva de 30x20cm en puertas de áreas de riesgo exclusivo (cuartos técnicos, subestaciones) complementada con chapa de seguridad bajo llave según NTC 1461.",
        "palabras_clave": ["prohibido el paso", "no pasar", "restringido", "solo personal autorizado", "acceso denegado", "puerta cerrada"]
    },
    "riesgo_electrico": {
        "elemento": "Señal: Peligro Riesgo Eléctrico / Alta Tensión",
        "categoria": "Amarillas",
        "condicion_default": "Requiere verificación",
        "norma": "RETIE (Reglamento Técnico de Instalaciones Eléctricas) / NTC 1461 / NTC-ISO 7010 (W012)",
        "color_seguridad": "Amarillo / Amarillo Anaranjado",
        "color_contraste": "Negro (Borde triangular y pictograma de rayo)",
        "forma_geometrica": "Triángulo equilátero con vértice superior",
        "cobertura_min_color": "Amarillo >= 50% de la superficie total",
        "tamano_recomendado": "Lado 20 cm (d <= 8m) | Lado 30 cm (d <= 12m) | Formato combinado 30x20 cm",
        "formula_dimension": "d = L * 35 (L: longitud del lado del triángulo equilátero)",
        "altura_montaje": "Fijada directamente sobre la tapa frontal del tablero a 1.50m - 1.70m del NPT.",
        "demarcacion_piso": "Demarcación perimetral de 10 cm con franjas diagonales a 45° amarillo/negro dejando 0.80m de despeje frontal.",
        "fotoluminiscencia": "Vinilo reflectivo Grado Ingeniería o Poliestireno 1mm ignífugo.",
        "checklist_sst": [
            "1. Tablero cerrado con llave y directorio de circuitos legible y actualizado.",
            "2. Mandil protector interno (tapa cubre-barras) instalado sin partes vivas expuestas.",
            "3. Ausencia de humedad, filtraciones o acumulación de polvo dentro del gabinete.",
            "4. Despeje frontal mínimo de 0.80 metros libre de obstáculos para maniobra de emergencia.",
            "5. Certificación de conexión al sistema de puesta a tierra (SPT)."
        ],
        "recomendacion": "Instalar señal triangular de peligro eléctrico de 20cm en el exterior del tablero eléctrico según RETIE y NTC 1461. Demarcar zona de maniobra de 80cm en piso con franjas amarillo/negro a 45°.",
        "palabras_clave": ["riesgo electrico", "tablero", "alta tension", "peligro electrico", "voltaje", "electrocutar", "subestacion", "retie"]
    },
    "peligro_caida": {
        "elemento": "Señal: Peligro Caída de Personas a Distinto Nivel / Desnivel",
        "categoria": "Amarillas",
        "condicion_default": "Requiere verificación",
        "norma": "Res. 4272 de 2021 (Trabajo en Alturas) / Res. 2400 de 1979 / NTC 1461 (W008)",
        "color_seguridad": "Amarillo",
        "color_contraste": "Negro",
        "forma_geometrica": "Triángulo equilátero con pictograma de persona cayendo",
        "cobertura_min_color": "Amarillo >= 50% de la superficie total",
        "tamano_recomendado": "Triángulo de 30 cm de lado o formato 30x20 cm con texto de advertencia",
        "formula_dimension": "d = L * 35",
        "altura_montaje": "1.60m en muros perimetrales o fijada a barandas de protección a 1.05m.",
        "demarcacion_piso": "Franja de huella y contrahuella con cinta antideslizante negra/amarilla de 5 cm.",
        "fotoluminiscencia": "Vinilo reflectivo con borde de alta visibilidad.",
        "checklist_sst": [
            "1. Barandas perimetrales estructurales de altura mínima 1.05m con travesaño intermedio y rodapié.",
            "2. Cinta antideslizante con mineral abrasivo en los bordes de todos los peldaños.",
            "3. Iluminación adecuada en los tramos de escaleras (mínimo 100 Lux).",
            "4. Pasamanos continuo a ambos lados fijado a altura reglamentaria de 0.90m."
        ],
        "recomendacion": "Señalizar con triángulo amarillo de advertencia (lado 30cm) en descansos y borde de desniveles. Instalar cintas antideslizantes fotoluminiscentes de 5cm de ancho en huellas de escaleras (Res. 2400/79).",
        "palabras_clave": ["caida", "desnivel", "altura", "escalera", "hueco", "andamio", "borde", "pasamanos"]
    },
    "piso_resbaloso": {
        "elemento": "Señal: Peligro Piso Resbaloso / Caída al Mismo Nivel",
        "categoria": "Amarillas",
        "condicion_default": "Requiere verificación",
        "norma": "Res. 2400 de 1979 (Art. 17 y 202) / NTC 1461 / NTC-ISO 7010 (W011) / OSHA 1910.22",
        "color_seguridad": "Amarillo",
        "color_contraste": "Negro",
        "forma_geometrica": "Triángulo equilátero en caballete portátil tipo tijera plegable",
        "cobertura_min_color": "Amarillo >= 50% de la superficie",
        "tamano_recomendado": "Caballete de 60 cm de altura x 30 cm de ancho con texto bilingüe y pictograma doble cara",
        "formula_dimension": "Visible a distancia mínima de 8 a 10 metros en pasillos",
        "altura_montaje": "Ubicada directamente sobre el suelo en ambos extremos de la zona húmeda o encerada.",
        "demarcacion_piso": "Delimitación perimetral durante labores de lavado y secado intensivo.",
        "fotoluminiscencia": "Plástico de polipropileno inyectado de alta densidad color amarillo de seguridad.",
        "checklist_sst": [
            "1. Despliegue obligatorio y previo al inicio de labores de trapeado o encerado.",
            "2. Colocación en accesos y bifurcaciones de pasillos para advertir antes de pisar la zona húmeda.",
            "3. Uso de calzado antideslizante por parte de los operarios de servicios generales.",
            "4. Retiro inmediato de los caballetes una vez el piso esté totalmente seco para evitar pérdida de efectividad."
        ],
        "recomendacion": "Dotar al personal de servicios generales con señales móviles tipo tijera ('Precaución Piso Húmedo') de 60cm de altura. Exigir su colocación previa al trapeado en pasillos según Res. 2400/79 y NTC 1461.",
        "palabras_clave": ["piso resbaloso", "mojado", "resbalon", "caida", "limpieza de piso", "wet floor", "humedo", "caballete"]
    },
    "sustancias_peligrosas": {
        "elemento": "Señal: Peligro Sustancias Químicas Inflamables / Reactivas",
        "categoria": "Amarillas",
        "condicion_default": "Requiere verificación",
        "norma": "Decreto 1496 de 2018 (SGA/GHS) / NTC 1461 / NTC 1692 / Res. 2400 de 1979",
        "color_seguridad": "Amarillo (Advertencia) y Rombos SGA con borde rojo",
        "color_contraste": "Negro / Blanco",
        "forma_geometrica": "Triángulo de advertencia y Rombo SGA a 45°",
        "cobertura_min_color": "Amarillo >= 50%",
        "tamano_recomendado": "30x20 cm o matriz combinada de 40x30 cm con pictogramas SGA",
        "formula_dimension": "S >= d² / 2000",
        "altura_montaje": "1.60m en puertas de acceso y a nivel de estantes de almacenamiento.",
        "demarcacion_piso": "Dique de contención con demarcación en franjas amarillo/negro de 10 cm.",
        "fotoluminiscencia": "Lámina galvanizada o poliestireno resistente a vapores corrosivos e inflamables.",
        "checklist_sst": [
            "1. Hojas de Datos de Seguridad (FDS / SDS de 16 secciones) legibles en el área de trabajo.",
            "2. Envases debidamente rotulados con pictogramas del Sistema Globalmente Armonizado (SGA).",
            "3. Bandejas o estibas antiderrame operativas con capacidad del 110% del envase mayor.",
            "4. Kit para control de derrames químicos (absorbentes, diques y EPP específico) disponible."
        ],
        "recomendacion": "Implementar rotulación bajo Sistema Globalmente Armonizado (Decreto 1496 de 2018) y señal de advertencia de 30x20cm. Disponer de FDS visibles y bandejas de contención según Res. 2400/79.",
        "palabras_clave": ["quimicos", "inflamable", "toxico", "acido", "sustancia peligrosa", "reactivo", "sga", "ghs", "derrame"]
    },
    "uso_casco": {
        "elemento": "Señal: Uso Obligatorio de Casco de Seguridad",
        "categoria": "Azules",
        "condicion_default": "Conforme",
        "norma": "ANSI Z89.1 / NTC 1523 / NTC 1461 / NTC-ISO 7010 (M014) / Res. 2400 de 1979",
        "color_seguridad": "Azul",
        "color_contraste": "Blanco (Pictograma de cabeza con casco)",
        "forma_geometrica": "Círculo pleno",
        "cobertura_min_color": "Azul >= 50% de la superficie total",
        "tamano_recomendado": "Diámetro 20 cm (d <= 8m) | Diámetro 30 cm o formato 30x20 cm con texto (d <= 12m)",
        "formula_dimension": "d = D * 40",
        "altura_montaje": "1.60m a 1.70m en el pórtico de acceso al taller, laboratorio u obra.",
        "demarcacion_piso": "Línea de detención amarilla de 10 cm con leyenda 'Área de Uso Obligatorio de EPP'.",
        "fotoluminiscencia": "Poliestireno 1mm con tintas UV o vinilo sobre lámina galvanizada.",
        "checklist_sst": [
            "1. Porte efectivo de casco tipo I o II dieléctrico (Clase E) por parte de operarios y visitantes.",
            "2. Barboquejo de fijación de 3 o 4 puntos en trabajos con riesgo de caída o altura.",
            "3. Inspección del tafilete y carcasa (sin fisuras, abolladuras ni fecha de caducidad superada).",
            "4. Prohibición de uso de gorras o prendas debajo del casco que alteren el ajuste."
        ],
        "recomendacion": "Instalar señal circular azul de uso obligatorio de casco (diámetro 30cm) en el ingreso de laboratorios industriales y zonas de carga conforme a la NTC 1461 y ANSI Z89.1.",
        "palabras_clave": ["casco", "casco de seguridad", "proteccion cabeza", "helmet", "epp casco", "tafilete"]
    },
    "uso_gafas": {
        "elemento": "Señal: Uso Obligatorio de Protección Ocular / Gafas de Seguridad",
        "categoria": "Azules",
        "condicion_default": "Conforme",
        "norma": "ANSI Z87.1 / NTC 1825 / NTC 1461 / NTC-ISO 7010 (M004) / Res. 2400/79",
        "color_seguridad": "Azul",
        "color_contraste": "Blanco",
        "forma_geometrica": "Círculo pleno",
        "cobertura_min_color": "Azul >= 50% de la superficie total",
        "tamano_recomendado": "Diámetro 20 cm o combinado 20x30 cm",
        "formula_dimension": "d = D * 40",
        "altura_montaje": "1.60m en el acceso inmediato y en cada puesto de trabajo con riesgo de proyección.",
        "demarcacion_piso": "Demarcación perimetral de la estación de máquina en color amarillo de 10 cm.",
        "fotoluminiscencia": "Poliestireno 1mm de alta resistencia a solventes.",
        "checklist_sst": [
            "1. Lentes de policarbonato con protección lateral y sello de certificación ANSI Z87.1.",
            "2. Lentes limpios sin rayas profundas que distorsionen el campo visual.",
            "3. Protección contra rayos UV o salpicaduras químicas según la actividad.",
            "4. Disponibilidad de estaciones de limpieza o reemplazo inmediato de EPP ocular."
        ],
        "recomendacion": "Exigir gafas con certificación ANSI Z87.1 y colocar señal azul circular (diámetro 20cm) en cada estación de mecanizado, corte o mezcla química según Res. 2400/79 y NTC 1461.",
        "palabras_clave": ["gafas", "lentes", "proteccion ocular", "careta", "antiparras", "monogafas"]
    },
    "uso_botas": {
        "elemento": "Señal: Uso Obligatorio de Calzado / Botas de Seguridad",
        "categoria": "Azules",
        "condicion_default": "Conforme",
        "norma": "ASTM F2413 / ISO 20345 / NTC 1461 / NTC-ISO 7010 (M008) / Res. 2400/79",
        "color_seguridad": "Azul",
        "color_contraste": "Blanco",
        "forma_geometrica": "Círculo pleno",
        "cobertura_min_color": "Azul >= 50% de la superficie",
        "tamano_recomendado": "Diámetro 20 cm o 30x20 cm",
        "formula_dimension": "d = D * 40",
        "altura_montaje": "1.60m en el acceso de talleres, almacenes y áreas operativas.",
        "demarcacion_piso": "Piso limpio y seco con franja delimitadora de 10 cm.",
        "fotoluminiscencia": "Poliestireno 1mm con tintas UV.",
        "checklist_sst": [
            "1. Puntera de protección de acero o composite certificada contra aplastamiento (mínimo 200J).",
            "2. Suela de poliuretano bidensidad con labrado antideslizante con coeficiente adecuado.",
            "3. Propiedades dieléctricas o antiestáticas según el tipo de riesgo presente en el bloque.",
            "4. Cordones ajustados y sujeción óptima del tobillo."
        ],
        "recomendacion": "Fijar señal azul de calzado de seguridad con puntera certificada (ASTM F2413) de 20x30cm a 1.70m de altura en el acceso de talleres de manufactura y bodegas según Res. 2400/79.",
        "palabras_clave": ["botas", "calzado", "zapatos de seguridad", "punta de acero", "borceguies", "puntera"]
    },
    "uso_guantes": {
        "elemento": "Señal: Uso Obligatorio de Guantes de Protección",
        "categoria": "Azules",
        "condicion_default": "Conforme",
        "norma": "EN 388 (Riesgos Mecánicos) / EN 374 (Químicos) / NTC 1461 / NTC-ISO 7010 (M009)",
        "color_seguridad": "Azul",
        "color_contraste": "Blanco",
        "forma_geometrica": "Círculo pleno",
        "cobertura_min_color": "Azul >= 50% de la superficie",
        "tamano_recomendado": "Diámetro 20 cm o combinado 20x30 cm",
        "formula_dimension": "d = D * 40",
        "altura_montaje": "1.60m en tableros de herramientas y áreas de dosificación.",
        "demarcacion_piso": "No aplica demarcación horizontal.",
        "fotoluminiscencia": "Poliestireno 1mm.",
        "checklist_sst": [
            "1. Guante seleccionado acorde al riesgo específico (nitrilo para químicos, carnaza para calor, vaqueta para corte).",
            "2. Talla correcta del usuario para no limitar la motricidad fina.",
            "3. Ausencia de roturas, perforaciones o contaminación interior con químicos.",
            "4. Descarte y reposición periódica garantizada."
        ],
        "recomendacion": "Instalar señal de protección manual en bancos de trabajo y exigir guantes con certificación EN 388 / EN 374 adecuados al agente manipulado según NTC 1461.",
        "palabras_clave": ["guantes", "proteccion manos", "mitones", "gloves", "nitrilo", "carnaza"]
    },
    "proteccion_auditiva": {
        "elemento": "Señal: Uso Obligatorio de Protección Auditiva",
        "categoria": "Azules",
        "condicion_default": "Conforme",
        "norma": "ANSI S3.19 / NTC 2272 / NTC 1461 / NTC-ISO 7010 (M003) / Res. 2400 de 1979",
        "color_seguridad": "Azul",
        "color_contraste": "Blanco",
        "forma_geometrica": "Círculo pleno",
        "cobertura_min_color": "Azul >= 50% de la superficie",
        "tamano_recomendado": "Diámetro 20 cm (d <= 8m) | 30x20 cm con texto",
        "formula_dimension": "d = D * 40",
        "altura_montaje": "1.60m en el acceso a cuartos de máquinas, plantas eléctricas y carpinterías.",
        "demarcacion_piso": "Franja delimitadora de zona de alto ruido (>= 85 dBA).",
        "fotoluminiscencia": "Poliestireno 1mm o vinilo adhesivo.",
        "checklist_sst": [
            "1. Uso en toda zona donde el nivel sonoro continuo equivalente supere 85 dBA (Res. 2400/79).",
            "2. Tipo de protector acorde a la atenuación requerida NRR (de inserción o de copa).",
            "3. Correcta higiene y almacenamiento en estuche individual.",
            "4. Realización de audiometrías ocupacionales de seguimiento al personal expuesto."
        ],
        "recomendacion": "Fijar señal azul de protección auditiva obligatoria en accesos a áreas con ruido continuo superior a 85 dBA, suministrando protectores con nivel de reducción de ruido (NRR) verificado según NTC 2272.",
        "palabras_clave": ["orejeras", "tapones", "ruido", "proteccion auditiva", "auditivos", "decibeles", "copa"]
    },
    "salida_emergencia": {
        "elemento": "Señal: Salida de Emergencia / Puerta de Evacuación",
        "categoria": "Verdes",
        "condicion_default": "Conforme",
        "norma": "NSR-10 (Título K, K.3.8) / NTC 1461 / ISO 16069 / NTC-ISO 7010 (E001/E002)",
        "color_seguridad": "Verde",
        "color_contraste": "Blanco (Silueta humana corriendo hacia la puerta)",
        "forma_geometrica": "Rectángulo o Cuadrado",
        "cobertura_min_color": "Verde >= 50% de la superficie total",
        "tamano_recomendado": "30x15 cm o 30x20 cm (d <= 10m) | 40x20 cm o 60x20 cm (d <= 20m) | Bandera 30x15 cm",
        "formula_dimension": "S >= d² / 2000 (Dimensiones mayores en corredores largos según norma UNE 23-034 / CTE)",
        "altura_montaje": "Doble nivel obligatorio según ISO 16069: Nivel Alto (sobre dintel de la puerta a 2.00m - 2.20m) y Nivel Bajo / Zócalo (10 cm a 40 cm del piso para visibilidad en presencia de humo).",
        "demarcacion_piso": "Franja de demarcación libre de apertura de puerta pintada en piso (radio de giro sin obstáculos).",
        "fotoluminiscencia": "Obligatoria Clase A (210 mcd/m² a 10 min) con autonomía mínima de 60 minutos según UNE 23-035.",
        "checklist_sst": [
            "1. Puerta con apertura hacia afuera en el sentido de la evacuación mediante barra antipánico certificada.",
            "2. Puerta sin cerraduras con llave, pasadores manuales ni candados durante las horas de ocupación.",
            "3. Lámpara de alumbrado de emergencia operativa sobre el marco con autonomía de batería de 90 min.",
            "4. Despeje absoluto: prohibido colocar sillas, recipientes de basura o mamparas en el vano de escape.",
            "5. Señal fotoluminiscente de alta luminancia visible aún ante corte total de fluido eléctrico."
        ],
        "recomendacion": "Instalar señal verde fotoluminiscente Clase A (mín. 30x15cm) sobre el dintel a 2.10m y a nivel de zócalo (30cm del piso) según ISO 16069. Dotar la puerta con barra antipánico según NSR-10 Título K.",
        "palabras_clave": ["salida", "evacuacion", "salida de emergencia", "escalera de emergencia", "flecha verde", "ruta", "puerta de emergencia"]
    },
    "ruta_evacuacion": {
        "elemento": "Señal: Flecha Direccional de Ruta de Evacuación",
        "categoria": "Verdes",
        "condicion_default": "Conforme",
        "norma": "NSR-10 (Título K, K.3.8) / NTC 1461 / ISO 16069 / NTC-ISO 7010 (E001+flecha)",
        "color_seguridad": "Verde",
        "color_contraste": "Blanco",
        "forma_geometrica": "Rectángulo con silueta humana y flecha direccional según ISO 16069",
        "cobertura_min_color": "Verde >= 50% de la superficie total",
        "tamano_recomendado": "30x15 cm (d <= 10m) | 40x20 cm (d <= 15m) | 60x20 cm (d <= 25m en pasillos amplios)",
        "formula_dimension": "S >= d² / 2000",
        "altura_montaje": "En pared a 1.70m - 1.80m al centro de la señal. En intersecciones de pasillos tipo bandera a >= 2.10m. Complemento a nivel de zócalo a 30cm del suelo.",
        "demarcacion_piso": "Líneas de guiado de piso fotoluminiscentes de 5 cm de ancho en tramos de escaleras y pasillos.",
        "fotoluminiscencia": "Clase A fotoluminiscente (210/29 mcd/m² con 3000 min de tiempo de atenuación).",
        "checklist_sst": [
            "1. Coherencia en la dirección de las flechas hacia la salida real más cercana (sin flechas contradictorias).",
            "2. Interpretación de flechas según ISO 16069 (flecha arriba: seguir recto / subir; flecha diagonal: bajar rampa/escalera).",
            "3. Separación entre señales no mayor a 15 metros en pasillos rectos y obligatoria en todo quiebre o cruce.",
            "4. Sin interrupciones por cortinas, letreros publicitarios ni cuadros decorativos."
        ],
        "recomendacion": "Disponer señales fotoluminiscentes Clase A cada 15 metros a lo largo de los pasillos a 1.70m de altura, orientadas inequívocamente hacia las salidas de emergencia conforme a la ISO 16069 y NSR-10.",
        "palabras_clave": ["ruta evacuacion", "flecha evacuacion", "via de escape", "evacuacion", "corredor", "salida de socorro"]
    },
    "punto_encuentro": {
        "elemento": "Señal: Punto de Encuentro / Zona Segura Exterior",
        "categoria": "Verdes",
        "condicion_default": "Conforme",
        "norma": "NTC 1461 / NTC-ISO 7010 (E007) / Decreto 1072 de 2015 (Planes de Emergencia)",
        "color_seguridad": "Verde",
        "color_contraste": "Blanco (Cuatro flechas señalando al centro con siluetas humanas)",
        "forma_geometrica": "Cuadrado o Rectángulo",
        "cobertura_min_color": "Verde >= 50% de la superficie total",
        "tamano_recomendado": "60x60 cm o 60x80 cm montada en pedestal (d <= 25m) | 80x80 cm para patios abiertos",
        "formula_dimension": "S >= d² / 2000 (Para áreas exteriores amplias de concentración masiva)",
        "altura_montaje": "En poste metálico exterior a altura mínima de 2.20m a 2.50m para visibilidad sobre multitudes.",
        "demarcacion_piso": "Círculo o cuadro de 2.0m x 2.0m pintado en piso con pintura de tráfico verde y bordes blancos reflectivos.",
        "fotoluminiscencia": "Lámina galvanizada calibre 20 con pintura electrostática y vinilo reflectivo Grado Ingeniería Prismático 3M.",
        "checklist_sst": [
            "1. Ubicación en espacio exterior a cielo abierto, lejos de tendidos eléctricos, árboles grandes o vidrios que puedan colapsar.",
            "2. Distancia mínima a fachadas equivalente a 1.5 veces la altura del edificio más alto cercano.",
            "3. Señal visible a 360° o montada sobre pedestal visible desde todas las salidas del campus.",
            "4. Piso demarcado con pintura de tráfico antideslizante con delimitación perimetral clara."
        ],
        "recomendacion": "Instalar poste con señal metálica reflectiva de 60x60cm a 2.30m de altura en el patio exterior. Pintar demarcación perimetral en piso en zona libre de riesgo de desprendimiento según Decreto 1072 de 2015.",
        "palabras_clave": ["punto de encuentro", "zona segura", "zona de concentracion", "reunion", "evacuacion externa"]
    },
    "camilla_primeros_auxilios": {
        "elemento": "Estación de Camilla Rígida y Botiquín de Primeros Auxilios",
        "categoria": "Verdes",
        "condicion_default": "Conforme",
        "norma": "Decreto 1072 de 2015 (Art. 2.2.4.6.25) / Res. 2400 de 1979 (Art. 164) / NTC 1461 / NTC-ISO 7010 (E013)",
        "color_seguridad": "Verde",
        "color_contraste": "Blanco (Cruz de primeros auxilios y silueta de camilla)",
        "forma_geometrica": "Rectángulo o Cuadrado",
        "cobertura_min_color": "Verde >= 50% de la superficie",
        "tamano_recomendado": "30x20 cm o 30x40 cm con texto indicativo",
        "formula_dimension": "S >= d² / 2000",
        "altura_montaje": "Soporte vertical para camilla entre 0.30m y 1.90m. Señal superior a 1.80m - 2.00m.",
        "demarcacion_piso": "Demarcación perimetral en piso de 0.60m x 2.00m con franjas amarillo/negro de 10 cm.",
        "fotoluminiscencia": "Poliestireno fotoluminiscente Clase A con alta visibilidad en penumbra.",
        "checklist_sst": [
            "1. Camilla espinal rígida de polietileno de alta densidad sin fisuras con capacidad de carga >= 150 kg.",
            "2. Juego completo de correas de inmovilización tipo araña y arnés de sujeción operativos.",
            "3. Inmovilizador cervical graduable para adultos y pediátrico en perfecto estado.",
            "4. Botiquín de primeros auxilios dotado según Res. 0705 de 2007 (sin medicamentos vencidos).",
            "5. Manta térmica impermeable y linterna auxiliar con baterías operativas."
        ],
        "recomendacion": "Dotar cada bloque con camilla espinal rígida con correas tipo araña e inmovilizador cervical. Señalizar con letrero verde fotoluminiscente de 30x20cm y botiquín dotado según Res. 2400/79 y Decreto 1072/15.",
        "palabras_clave": ["camilla", "primeros auxilios", "botiquin", "emergencia medica", "cruz roja", "inmovilizador", "espinal"]
    },
    "lavaojos_ducha": {
        "elemento": "Estación de Lavaojos y Ducha de Emergencia",
        "categoria": "Verdes",
        "condicion_default": "Requiere verificación",
        "norma": "ANSI/ISEA Z358.1 / NTC 1461 / NTC-ISO 7010 (E011/E012) / Res. 2400/79",
        "color_seguridad": "Verde",
        "color_contraste": "Blanco",
        "forma_geometrica": "Cuadrado o Rectángulo",
        "cobertura_min_color": "Verde >= 50% de la superficie",
        "tamano_recomendado": "30x30 cm o tipo bandera de 30x20 cm",
        "formula_dimension": "S >= d² / 2000",
        "altura_montaje": "Señal a 2.00m - 2.20m para localización rápida a distancia. Altura de difusor de lavaojos entre 0.83m y 1.14m.",
        "demarcacion_piso": "Área de piso de 0.90m x 0.90m demarcada con franjas diagonales verde/blanco o amarillo/negro de 10 cm con drenaje de piso.",
        "fotoluminiscencia": "Lámina acrílica fotoluminiscente de 2mm resistente a salpicaduras de ácidos y solventes.",
        "checklist_sst": [
            "1. Activación rápida en 1 solo paso (palanca de empuje o tirador) que permanezca abierta sin ayuda de las manos.",
            "2. Suministro de agua potable templada continua (mínimo 15 minutos continuos a flujo constante).",
            "3. Tapas protectoras contra el polvo presentes en los rociadores que salten solas al abrir el flujo.",
            "4. Acceso expedito sin ningún obstáculo a no más de 10 segundos de recorrido (máximo 15 metros).",
            "5. Registro de inspección y purga semanal de la línea hídrica."
        ],
        "recomendacion": "Garantizar prueba de flujo semanal según ANSI Z358.1. Instalar señal fotoluminiscente verde tipo bandera a 2.10m y demarcar recuadro de piso de 90x90cm con rejilla de desagüe según Res. 2400/79.",
        "palabras_clave": ["lavaojos", "ducha de emergencia", "estacion lavaojos", "ducha", "salpicadura", "quimica"]
    },
    "alarma_incendio": {
        "elemento": "Pulsador / Estación Manual de Alarma de Incendio",
        "categoria": "Rojas",
        "condicion_default": "Conforme",
        "norma": "NFPA 72 / NSR-10 (Título J, J.4.3) / NTC 1461 / NTC-ISO 7010 (F005)",
        "color_seguridad": "Rojo",
        "color_contraste": "Blanco",
        "forma_geometrica": "Cuadrado con pictograma de mano accionando pulsador",
        "cobertura_min_color": "Rojo >= 50% de la superficie",
        "tamano_recomendado": "15x15 cm o 20x20 cm en acrílico fotoluminiscente",
        "formula_dimension": "S >= d² / 2000",
        "altura_montaje": "Instalado entre 1.10m y 1.25m del NPT para accesibilidad universal (silla de ruedas). Señal a 1.60m.",
        "demarcacion_piso": "Despeje libre frontal de 0.80 metros sin obstrucción.",
        "fotoluminiscencia": "Clase A fotoluminiscente visible en penumbra total.",
        "checklist_sst": [
            "1. Estación visible sin muebles, plantas o mamparas que la oculten a la vista.",
            "2. Llave o mecanismo de rearme disponible en la central de control o intendencia.",
            "3. Prueba semestral de comunicación con el panel central de incendio y sirena estroboscópica.",
            "4. Instrucción de operación grabada clara ('Empujar y jalar' o 'Romper vidrio en emergencia')."
        ],
        "recomendacion": "Fijar estación manual a 1.20m del piso y señalizar con letrero rojo fotoluminiscente de 15x15cm a 1.60m. Asegurar que las sirenas estroboscópicas cumplan con los decibeles requeridos según NFPA 72 y NSR-10.",
        "palabras_clave": ["alarma", "pulsador", "estacion manual", "alarma incendio", "sirena", "fire alarm", "estroboscopica"]
    },
    "prohibido_comer": {
        "elemento": "Señal: Prohibido Ingerir Alimentos y Bebidas",
        "categoria": "Rojas",
        "condicion_default": "Conforme",
        "norma": "Res. 2400 de 1979 (Art. 182 y 202) / NTC 1461 / NTC-ISO 7010 (P022)",
        "color_seguridad": "Rojo (Círculo y banda diagonal a 45°)",
        "color_contraste": "Blanco (Fondo) y Negro (Pictograma de cubiertos o hamburguesa/vaso)",
        "forma_geometrica": "Círculo con banda diagonal descendente a 45°",
        "cobertura_min_color": "Rojo >= 35% de la superficie",
        "tamano_recomendado": "Diámetro 20 cm o formato 20x30 cm con texto explicativo",
        "formula_dimension": "d = D * 40",
        "altura_montaje": "1.60m a 1.70m en la puerta de acceso y en vitrinas o paneles frontales de laboratorios.",
        "demarcacion_piso": "No aplica demarcación horizontal.",
        "fotoluminiscencia": "Poliestireno 1mm con laminado brillante de fácil limpieza.",
        "checklist_sst": [
            "1. Señal fijada en pórticos de laboratorios de química, sistemas, talleres y áreas limpias.",
            "2. Verificación de ausencia de envases de café, bebidas o restos de comida cerca de equipos electrónicos.",
            "3. Prohibición estricta de consumo dentro de zonas con riesgo biológico o químico.",
            "4. Cumplimiento de políticas de bioseguridad institucional."
        ],
        "recomendacion": "Colocar señales circulares de prohibido comer/beber de 20cm de diámetro en los accesos a salas de cómputo y laboratorios para prevenir fallas en equipos y contaminación cruzada según Res. 2400/79.",
        "palabras_clave": ["prohibido comer", "no comer", "alimentos", "bebidas", "comida", "laboratorio", "refrigerio"]
    }
}

def normalizar_clase_ia(clase_ia: str) -> Dict[str, Any]:
    """
    Convierte una etiqueta detectada por modelos YOLO o Roboflow
    (ej: 'extinguisher', 'fire_extinguisher', 'no_cellphone', 'emergency_exit')
    al objeto formal del catálogo SST.
    """
    clase_limpia = clase_ia.lower().strip().replace(" ", "_").replace("-", "_")
    
    # 1. Búsqueda exacta
    if clase_limpia in CATALOGO_SENALES:
        res = dict(CATALOGO_SENALES[clase_limpia])
        res["id_catalogo"] = clase_limpia
        return res
        
    # 2. Mapeos de nombres comunes en modelos entrenados
    mapeos = {
        "extinguisher": "extintor",
        "fire_extinguisher": "extintor",
        "fire_cabinet": "gabinete_incendio",
        "hose": "gabinete_incendio",
        "no_smoking": "prohibido_fumar",
        "smoking": "prohibido_fumar",
        "no_phone": "prohibido_celular",
        "cellphone": "prohibido_celular",
        "no_entry": "prohibido_paso",
        "electrical_hazard": "riesgo_electrico",
        "high_voltage": "riesgo_electrico",
        "fall_hazard": "peligro_caida",
        "helmet": "uso_casco",
        "hard_hat": "uso_casco",
        "glasses": "uso_gafas",
        "goggles": "uso_gafas",
        "boots": "uso_botas",
        "gloves": "uso_guantes",
        "earmuffs": "proteccion_auditiva",
        "exit": "salida_emergencia",
        "emergency_exit": "salida_emergencia",
        "first_aid": "camilla_primeros_auxilios",
        "stretcher": "camilla_primeros_auxilios",
        "camilla": "camilla_primeros_auxilios",
        "eyewash": "lavaojos_ducha",
        "assembly_point": "punto_encuentro",
        "piso_resbaloso": "piso_resbaloso",
        "wet_floor": "piso_resbaloso",
        "alarma_incendio": "alarma_incendio",
        "fire_alarm": "alarma_incendio",
        "prohibido_comer": "prohibido_comer",
        "no_food": "prohibido_comer",
        "ruta_evacuacion": "ruta_evacuacion"
    }
    
    if clase_limpia in mapeos:
        key = mapeos[clase_limpia]
        res = dict(CATALOGO_SENALES[key])
        res["id_catalogo"] = key
        return res
        
    # 3. Búsqueda parcial por subcadenas
    for key, item in CATALOGO_SENALES.items():
        if key in clase_limpia or clase_limpia in key:
            res = dict(item)
            res["id_catalogo"] = key
            return res
            
    # Retorno por defecto si no hay coincidencia exacta
    return {
        "id_catalogo": "desconocido",
        "elemento": f"Elemento SST ({clase_ia})",
        "categoria": "Amarillas",
        "condicion_default": "Requiere verificación",
        "norma": "NTC 1461 / NTC-ISO 3864-1 / Res. 2400 de 1979",
        "color_seguridad": "Amarillo (Advertencia)",
        "color_contraste": "Negro",
        "forma_geometrica": "Triángulo equilátero o Rectángulo complementario",
        "cobertura_min_color": ">= 50%",
        "tamano_recomendado": "20x20 cm (d <= 10m) | 30x30 cm (d <= 15m)",
        "formula_dimension": "S >= d² / 2000",
        "altura_montaje": "1.60m a 1.80m al centro de la señal",
        "demarcacion_piso": "Franja amarilla de 10 cm si delimita área de peligro",
        "fotoluminiscencia": "Poliestireno 1mm o lámina reflectiva",
        "checklist_sst": [
            "1. Verificar visibilidad despejada a la distancia máxima requerida.",
            "2. Contrastes de color legibles sin decoloración por rayos UV.",
            "3. Fijación mecánica segura que impida desprendimientos.",
            "4. Cumplimiento de la norma técnica sectorial específica."
        ],
        "recomendacion": "Verificar estado físico y cumplimiento de la normativa SST específica (NTC 1461 / Res. 2400 de 1979) aplicable al elemento."
    }

def limpiar_texto_acentos(texto: str) -> str:
    reemplazos = (
        ("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"),
        ("Á", "a"), ("É", "e"), ("Í", "i"), ("Ó", "o"), ("Ú", "u")
    )
    res = texto
    for a, b in reemplazos:
        res = res.replace(a, b)
    return res.lower()

def deducir_por_contexto(texto_contexto: str) -> Dict[str, Any]:
    """
    Analiza observaciones y ubicación escritas por el inspector
    para sugerir el hallazgo adecuado mediante reglas NLP offline.
    """
    texto = limpiar_texto_acentos(texto_contexto)
    
    for key, data in CATALOGO_SENALES.items():
        for palabra in data["palabras_clave"]:
            if limpiar_texto_acentos(palabra) in texto:
                res = dict(data)
                res["id_catalogo"] = key
                return res
                
    # Si no coincide nada específico pero contiene palabras de alerta
    if any(p in texto for p in ["fuego", "humo", "quema", "alarma"]):
        res = dict(CATALOGO_SENALES["extintor"])
        res["id_catalogo"] = "extintor"
        return res
    if any(p in texto for p in ["puerta", "pasillo", "bloquead", "salida", "escape", "evacua"]):
        res = dict(CATALOGO_SENALES["salida_emergencia"])
        res["id_catalogo"] = "salida_emergencia"
        return res
        
    return {
        "id_catalogo": "inspeccion_general",
        "elemento": "Inspección General de Área",
        "categoria": "Amarillas",
        "condicion_default": "Requiere verificación",
        "norma": "NTC 1461 / Res. 2400 de 1979 / Decreto 1072 de 2015",
        "color_seguridad": "Amarillo (Precaución)",
        "color_contraste": "Negro",
        "forma_geometrica": "Triángulo o Rectángulo",
        "cobertura_min_color": ">= 50%",
        "tamano_recomendado": "30x20 cm según distancia de pasillo",
        "formula_dimension": "S >= d² / 2000",
        "altura_montaje": "1.60m a 1.80m del NPT",
        "demarcacion_piso": "Demarcación de 10 cm amarillo continuo",
        "fotoluminiscencia": "Según requerimiento de evacuación",
        "checklist_sst": [
            "1. Pasillos libres con ancho no menor a 40 cm entre máquinas o muros (Res. 2400/79 Art. 281).",
            "2. Demarcación perimetral de áreas de almacenamiento y tránsito peatonal.",
            "3. Orden y aseo locativo sin materiales que obstruyan rutas de evacuación.",
            "4. Correcta iluminación y ventilación en el puesto de trabajo."
        ],
        "recomendacion": "Realizar evaluación minuciosa de condiciones subestándar y actos inseguros en el puesto de trabajo conforme a la Res. 2400 de 1979 y Decreto 1072 de 2015."
    }
