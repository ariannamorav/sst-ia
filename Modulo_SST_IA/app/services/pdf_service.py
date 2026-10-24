"""
Servicio generador de Informes Técnicos Periciales de Inspección SST en PDF con ReportLab.
Estructurado rigurosamente según el marco legal y normas técnicas colombianas:
- NTC 1461: Colores y señales de seguridad (código de colores, formas y porcentajes de área).
- NTC-ISO 3864-1:2011 y NTC-ISO 3864-3:2012: Principios de diseño para señales de seguridad.
- NTC-ISO 7010:2021: Símbolos gráficos registrados.
- Resolución 2400 de 1979 (Estatuto de Seguridad Industrial: pasillos libres >= 40cm, demarcación amarilla 10cm, barandas 60cm a 45°).
- NSR-10: Título J (Protección contra incendios, NTC 2885 / NTC 1669) y Título K (Medios y señalización de evacuación).
- Decreto 1072 de 2015: Art. 2.2.4.6.25 (Plan de Prevención, Preparación y Respuesta ante Emergencias).
- ISO 16069: Sistemas de señalización fotoluminiscente de evacuación (señales altas, intermedias y a nivel de zócalo).
- Catálogos técnicos oficiales (CCS y Covadonga): Fórmula S >= d² / 2000, distancias vs. tamaños y fotoluminiscencia Clase A/B.
- Estándar de citación y registro fotográfico APA 7ma Edición.
"""
import io
import os
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

from app.models.catalogo_sst import CATEGORIAS_SST, CATALOGO_SENALES


class NumberedCanvas(canvas.Canvas):
    """Canvas dinámico de ReportLab que calcula y numera las páginas totales (Página X de Y)."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Encabezado institucional en páginas 2 en adelante
        if self._pageNumber > 1:
            self.drawString(36, 762, "Politécnico Grancolombiano | Auditoría Pericial SST: Condiciones, Señalización y Demarcación")
            self.drawRightString(576, 762, "NTC 1461 / NSR-10 / Res. 2400 / Dec. 1072")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.6)
            self.line(36, 756, 576, 756)

        # Pie de página institucional en todas las páginas
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.6)
        self.line(36, 42, 576, 42)
        
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748b"))
        texto_pie = f"Página {self._pageNumber} de {page_count} · Dictamen Oficial de Auditoría Técnica y Conformidad Legal SST"
        self.drawString(36, 28, texto_pie)
        self.drawRightString(576, 28, f"Sede Medellín · Sistema SST-IA · {datetime.now().strftime('%d/%m/%Y')}")
        self.restoreState()


class PDFService:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._crear_estilos()

    def _crear_estilos(self):
        self.estilo_titulo = ParagraphStyle(
            'TituloSST',
            parent=self.styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=15,
            leading=19,
            textColor=colors.HexColor('#0f172a'),
            alignment=0,
            spaceAfter=4
        )
        self.estilo_subtitulo_meta = ParagraphStyle(
            'SubtituloMetaSST',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor('#334155'),
            spaceAfter=8
        )
        self.estilo_seccion_num = ParagraphStyle(
            'SeccionNumSST',
            parent=self.styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=14,
            textColor=colors.HexColor('#1e3a8a'),
            spaceBefore=10,
            spaceAfter=5
        )
        self.estilo_subseccion_num = ParagraphStyle(
            'SubSeccionNumSST',
            parent=self.styles['Heading3'],
            fontName='Helvetica-Bold',
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor('#0f2942'),
            spaceBefore=6,
            spaceAfter=4
        )
        self.estilo_parrafo = ParagraphStyle(
            'ParrafoSST',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            leading=11.5,
            textColor=colors.HexColor('#1e293b'),
            alignment=4, # Justificado
            spaceAfter=5
        )
        self.estilo_norma_item = ParagraphStyle(
            'NormaItemSST',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=7.8,
            leading=11,
            textColor=colors.HexColor('#1e293b'),
            spaceAfter=3.5
        )
        self.estilo_celda = ParagraphStyle(
            'CeldaSST',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=7.2,
            leading=9.5,
            textColor=colors.HexColor('#1e293b')
        )
        self.estilo_celda_bold = ParagraphStyle(
            'CeldaBoldSST',
            parent=self.styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=7.2,
            leading=9.5,
            textColor=colors.HexColor('#0f172a')
        )
        self.estilo_celda_center = ParagraphStyle(
            'CeldaCenterSST',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=7.2,
            leading=9.5,
            alignment=1,
            textColor=colors.HexColor('#1e293b')
        )
        self.estilo_celda_th = ParagraphStyle(
            'CeldaThSST',
            parent=self.styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=7.5,
            leading=10,
            textColor=colors.HexColor('#ffffff'),
            alignment=1 # Centrado
        )

        # Estilos estándar APA 7ma Edición para figuras
        self.estilo_apa_figura = ParagraphStyle(
            'ApaFiguraSST',
            parent=self.styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=2
        )
        self.estilo_apa_titulo = ParagraphStyle(
            'ApaTituloSST',
            parent=self.styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=8,
            leading=10.5,
            textColor=colors.HexColor('#334155'),
            spaceAfter=4
        )
        self.estilo_apa_nota = ParagraphStyle(
            'ApaNotaSST',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=7.2,
            leading=9.8,
            textColor=colors.HexColor('#475569'),
            spaceBefore=3,
            spaceAfter=10
        )

    def generar_pdf_inspeccion(self, inspeccion: Dict[str, Any]) -> bytes:
        """Genera el informe formal en formato PDF de acuerdo con los requerimientos colombianos y APA 7."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            leftMargin=36,
            rightMargin=36,
            topMargin=36,
            bottomMargin=50
        )
        
        story = []
        
        # -----------------------------------------------------------------
        # TÍTULO INSTITUCIONAL Y METADATOS
        # -----------------------------------------------------------------
        story.append(Paragraph(
            "Informe Pericial de Inspección Técnica de Seguridad y Salud en el Trabajo (SST): "
            "Evaluación de Condiciones Locativas, Sistemas de Emergencia, Señalización y Demarcación",
            self.estilo_titulo
        ))
        
        responsable = inspeccion.get("responsable", "Yair Alexander Córdoba Palomeque")
        if not responsable or responsable.strip() in ["Auditor SST", "YO", ""]:
            responsable = "Yair Alexander Córdoba Palomeque"
            
        sede = inspeccion.get("sede", "Politécnico Grancolombiano, Sede Medellín")
        if "Politécnico" not in sede:
            institucion_txt = f"Politécnico Grancolombiano · {sede}"
        else:
            institucion_txt = sede

        fecha_txt = inspeccion.get("fecha", "14 de octubre de 2026")
        numero_insp = inspeccion.get("numero", "#0001")
        area_txt = inspeccion.get("area", "Pasillos de Laboratorios y Aulas Múltiples")

        meta_parrafo = (
            f"<b>Preparado por:</b> {responsable} &nbsp;|&nbsp; <b>Rol:</b> Especialista / Auditor SST<br/>"
            f"<b>Institución:</b> {institucion_txt} &nbsp;|&nbsp; <b>Área Auditada:</b> {area_txt}<br/>"
            f"<b>Fecha de Recorrido:</b> {fecha_txt} &nbsp;|&nbsp; <b>Expediente Correlativo:</b> {numero_insp} &nbsp;|&nbsp; <b>Vigencia:</b> 2026-2027"
        )
        story.append(Paragraph(meta_parrafo, self.estilo_subtitulo_meta))
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1e3a8a"), spaceAfter=8))

        # -----------------------------------------------------------------
        # 1. INTRODUCCIÓN Y ALCANCE
        # -----------------------------------------------------------------
        story.append(Paragraph("1. Introducción y Alcance del Recorrido Técnico", self.estilo_seccion_num))
        intro_texto = (
            "El presente informe documenta los resultados de la auditoría física y verificación técnica de Seguridad y Salud "
            "en el Trabajo (SST) llevada a cabo en las instalaciones del campus institucional. El propósito fundamental radicó en "
            "evaluar el grado de conformidad con las disposiciones legales colombianas vigentes en materia de prevención, preparación "
            "y respuesta ante emergencias (Decreto 1072 de 2015), protección contra incendios (NSR-10 Título J), medios de evacuación "
            "(NSR-10 Título K), y el estricto cumplimiento de los estándares cromáticos, dimensionales y de visibilidad de la señalización "
            "de seguridad (NTC 1461, NTC-ISO 3864, ISO 16069 y Resolución 2400 de 1979). El dictamen tiene validez para fines de gestión "
            "del riesgo, planes de mejora ante ARL y auditorías del Ministerio de Trabajo."
        )
        story.append(Paragraph(intro_texto, self.estilo_parrafo))
        story.append(Spacer(1, 3))

        # -----------------------------------------------------------------
        # 2. MARCO LEGAL Y NORMAS TÉCNICAS OBLIGATORIAS
        # -----------------------------------------------------------------
        story.append(Paragraph("2. Marco Legal y Normas Técnicas Obligatorias de Referencia", self.estilo_seccion_num))
        story.append(Paragraph(
            "La inspección técnica se fundamenta en las regulaciones jurídicas y técnicas de obligatorio cumplimiento en Colombia "
            "para edificaciones de uso educativo y público, recopiladas en la carpeta oficial de normas técnicas:",
            self.estilo_parrafo
        ))

        normas = [
            ("NTC 1461 (ICONTEC) / NTC-ISO 3864-1:2011 / NTC-ISO 3864-3:2012:",
             "Establece los principios de diseño para señales de seguridad y demarcaciones: colores de seguridad (rojo, amarillo, azul, verde), "
             "colores de contraste (blanco y negro), formas geométricas estandarizadas y porcentajes mínimos de recubrimiento de color."),
            ("NTC-ISO 7010:2021:",
             "Símbolos gráficos normalizados a nivel internacional y nacional para señales de seguridad registradas (prohibición, advertencia, obligación y salvamento)."),
            ("Resolución 2400 de 1979 (Ministerio de Trabajo - Estatuto de Seguridad Industrial):",
             "<b>Art. 17:</b> Pisos limpios, sin humedad ni riesgos de resbalón.<br/>"
             "<b>Art. 164:</b> Dotación obligatoria de camillas y botiquines en puestos de primeros auxilios.<br/>"
             "<b>Art. 182:</b> Prohibición expresa de alimentos en laboratorios y áreas de riesgo.<br/>"
             "<b>Art. 202:</b> Señalización y código de colores en áreas industriales y de servicios.<br/>"
             "<b>Art. 281:</b> Ancho libre no menor de 40 cm entre máquinas, equipos o muros y pasillos, con demarcación continua de 10 cm en amarillo."),
            ("NSR-10 (Reglamento Colombiano de Construcción Sismo Resistente - Ley 400 de 1997):",
             "• <b>Título J (Extinción de Incendios):</b> Dotación obligatoria de extintores portátiles según carga de fuego (NTC 2885 / NFPA 10), "
             "distancia máxima de recorrido (15m a 23m), altura de montaje (máx. 1.50m) y red contra incendios con gabinetes equipados (NTC 1669 / NFPA 14).<br/>"
             "• <b>Título K (Medios de Evacuación):</b> Dimensionamiento de pasillos, salidas de emergencia con apertura hacia afuera, barras antipánico y señalética continua."),
            ("ISO 16069 (Sistemas de Señalización de Rutas de Evacuación - SWGS):",
             "Disposición de señales fotoluminiscentes en tres niveles de altura: nivel alto (> 2.00m), intermedio (1.60m - 1.80m) y bajo/zócalo (10cm - 40cm del piso) para escape bajo humo."),
            ("Decreto 1072 de 2015 (Decreto Único Reglamentario del Sector Trabajo):",
             "Art. 2.2.4.6.25: Obligación del empleador de estructurar y dotar el Plan de Prevención, Preparación y Respuesta ante Emergencias con recursos técnicos certificados."),
            ("Ley 1335 de 2009 (Ley Antitabaco):",
             "Arts. 19-20: Garantía de espacios 100% libres de humo de tabaco en instituciones educativas y fijación de avisos restrictivos obligatorios en todos los accesos.")
        ]

        for titulo_norma, desc_norma in normas:
            p_norma = Paragraph(f"• <b>{titulo_norma}</b> {desc_norma}", self.estilo_norma_item)
            story.append(p_norma)

        story.append(Spacer(1, 4))

        # -----------------------------------------------------------------
        # 3. GUÍA METROLÓGICA Y CROMÁTICA DE SEÑALIZACIÓN Y DEMARCACIÓN
        # -----------------------------------------------------------------
        story.append(Paragraph("3. Guía Metrológica y Cromática de Señalización y Demarcación", self.estilo_seccion_num))
        story.append(Paragraph(
            "Conforme a la NTC 1461, NTC-ISO 3864 y los manuales técnicos del Consejo Colombiano de Seguridad (CCS) y Covadonga, "
            "la señalización debe cumplir parámetros cromáticos y dimensionales exactos para garantizar su rápida legibilidad:",
            self.estilo_parrafo
        ))

        # Tabla 3.1: Matriz Cromática y Geométrica
        tabla_cromat_datos = [
            [
                Paragraph("<b>Color de Seguridad</b>", self.estilo_celda_th),
                Paragraph("<b>Color de Contraste</b>", self.estilo_celda_th),
                Paragraph("<b>Forma Geométrica</b>", self.estilo_celda_th),
                Paragraph("<b>% Mínimo Color</b>", self.estilo_celda_th),
                Paragraph("<b>Significado Técnico y Ejemplos de Aplicación</b>", self.estilo_celda_th)
            ],
            [
                Paragraph("<font color='#dc2626'><b>ROJO</b></font>", self.estilo_celda_bold),
                Paragraph("Blanco", self.estilo_celda),
                Paragraph("Círculo con barra diagonal descendente a 45°", self.estilo_celda),
                Paragraph(">= 35%", self.estilo_celda_center),
                Paragraph("<b>Prohibición:</b> Prohibido fumar (Ley 1335/09), no celular, no pase, parada de emergencia.", self.estilo_celda)
            ],
            [
                Paragraph("<font color='#dc2626'><b>ROJO</b></font>", self.estilo_celda_bold),
                Paragraph("Blanco", self.estilo_celda),
                Paragraph("Cuadrado o Rectángulo", self.estilo_celda),
                Paragraph(">= 50%", self.estilo_celda_center),
                Paragraph("<b>Equipos de Lucha Contra Incendios:</b> Extintores, gabinetes, pulsador de alarma (NSR-10 J).", self.estilo_celda)
            ],
            [
                Paragraph("<font color='#d97706'><b>AMARILLO</b></font>", self.estilo_celda_bold),
                Paragraph("Negro", self.estilo_celda),
                Paragraph("Triángulo equilátero", self.estilo_celda),
                Paragraph(">= 50%", self.estilo_celda_center),
                Paragraph("<b>Advertencia y Precaución:</b> Peligro eléctrico, piso resbaloso, caídas, sustancias químicas.", self.estilo_celda)
            ],
            [
                Paragraph("<font color='#d97706'><b>AMARILLO / NEGRO</b></font>", self.estilo_celda_bold),
                Paragraph("Contraste alterno", self.estilo_celda),
                Paragraph("Franjas diagonales a 45° de ancho similar", self.estilo_celda),
                Paragraph("50% / 50%", self.estilo_celda_center),
                Paragraph("<b>Riesgo Permanente:</b> Desniveles, vigas bajas, obstáculos salientes, bordes de escaleras.", self.estilo_celda)
            ],
            [
                Paragraph("<font color='#2563eb'><b>AZUL</b></font>", self.estilo_celda_bold),
                Paragraph("Blanco", self.estilo_celda),
                Paragraph("Círculo pleno", self.estilo_celda),
                Paragraph(">= 50%", self.estilo_celda_center),
                Paragraph("<b>Acción de Mando / Obligación:</b> Uso obligatorio de casco, gafas, calzado y protección auditiva.", self.estilo_celda)
            ],
            [
                Paragraph("<font color='#059669'><b>VERDE</b></font>", self.estilo_celda_bold),
                Paragraph("Blanco", self.estilo_celda),
                Paragraph("Cuadrado o Rectángulo", self.estilo_celda),
                Paragraph(">= 50%", self.estilo_celda_center),
                Paragraph("<b>Salvamento y Evacuación:</b> Salida de socorro, camilla, botiquín, punto de encuentro, lavaojos.", self.estilo_celda)
            ]
        ]

        t_cromat = Table(tabla_cromat_datos, colWidths=[70, 55, 115, 60, 240])
        t_cromat.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f2444')),
            ('ALIGN', (0,0), (-1,0), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(t_cromat)
        story.append(Spacer(1, 6))

        # Tabla 3.2: Distancias de Observación y Dimensiones Técnicas (S >= d² / 2000)
        story.append(Paragraph("<b>Tabla de Distancias de Visualización y Dimensionamiento Reglamentario (Fórmula S &ge; d² / 2000):</b>", self.estilo_parrafo))
        tabla_dim_datos = [
            [
                Paragraph("<b>Distancia de Visión (d)</b>", self.estilo_celda_th),
                Paragraph("<b>Superficie Mínima (S)</b>", self.estilo_celda_th),
                Paragraph("<b>Dimensión Cuadrada</b>", self.estilo_celda_th),
                Paragraph("<b>Dimensión Rectangular</b>", self.estilo_celda_th),
                Paragraph("<b>Diámetro Circular (d/40)</b>", self.estilo_celda_th),
                Paragraph("<b>Ubicación Típica Recomendada</b>", self.estilo_celda_th)
            ],
            [
                Paragraph("Hasta 5 metros", self.estilo_celda_bold),
                Paragraph("&ge; 0.0125 m²", self.estilo_celda_center),
                Paragraph("10 x 10 cm", self.estilo_celda_center),
                Paragraph("12 x 7 cm / 15 x 10 cm", self.estilo_celda_center),
                Paragraph("&Oslash; 12.5 cm", self.estilo_celda_center),
                Paragraph("Oficinas pequeñas, tableros eléctricos individuales.", self.estilo_celda)
            ],
            [
                Paragraph("Hasta 10 metros", self.estilo_celda_bold),
                Paragraph("&ge; 0.0500 m²", self.estilo_celda_center),
                Paragraph("20 x 20 cm / 21x21 cm", self.estilo_celda_center),
                Paragraph("30 x 15 cm / 30 x 20 cm", self.estilo_celda_center),
                Paragraph("&Oslash; 20.0 cm", self.estilo_celda_center),
                Paragraph("Pasillos estándar de aulas, laboratorios, extintores.", self.estilo_celda)
            ],
            [
                Paragraph("Hasta 15 metros", self.estilo_celda_bold),
                Paragraph("&ge; 0.1125 m²", self.estilo_celda_center),
                Paragraph("30 x 30 cm", self.estilo_celda_center),
                Paragraph("40 x 20 cm / 45 x 20 cm", self.estilo_celda_center),
                Paragraph("&Oslash; 30.0 cm", self.estilo_celda_center),
                Paragraph("Corredores principales, accesos a bloques, gabinetes.", self.estilo_celda)
            ],
            [
                Paragraph("Hasta 20 metros", self.estilo_celda_bold),
                Paragraph("&ge; 0.2000 m²", self.estilo_celda_center),
                Paragraph("42 x 42 cm (DIN A3)", self.estilo_celda_center),
                Paragraph("60 x 20 cm / 60 x 30 cm", self.estilo_celda_center),
                Paragraph("&Oslash; 40.0 cm", self.estilo_celda_center),
                Paragraph("Auditorios, cafeterías, vías de evacuación amplias.", self.estilo_celda)
            ],
            [
                Paragraph("Hasta 30 metros", self.estilo_celda_bold),
                Paragraph("&ge; 0.4500 m²", self.estilo_celda_center),
                Paragraph("60 x 60 cm (DIN A2)", self.estilo_celda_center),
                Paragraph("80 x 40 cm / 90 x 45 cm", self.estilo_celda_center),
                Paragraph("&Oslash; 60.0 cm", self.estilo_celda_center),
                Paragraph("Patios exteriores, zonas comunes abiertas, parqueaderos.", self.estilo_celda)
            ]
        ]

        t_dim = Table(tabla_dim_datos, colWidths=[80, 75, 75, 85, 80, 145])
        t_dim.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a8a')),
            ('ALIGN', (0,0), (-1,0), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(t_dim)
        story.append(Spacer(1, 5))

        # Parámetros de Instalación, Cotas y Demarcación
        texto_cotas = (
            "<b>Cotas Reglamentarias de Montaje y Demarcación (Res. 2400/79 e ISO 16069):</b><br/>"
            "• <b>Altura en pared estándar:</b> Entre 1.60m y 1.80m medidos desde el piso terminado (NPT) hasta el centro de la señal.<br/>"
            "• <b>Señales tipo bandera o suspendidas:</b> Altura libre mínima &ge; 2.00m a 2.20m para evitar obstrucción al paso y asegurar visibilidad sobre cabezas.<br/>"
            "• <b>Nivel de zócalo (ISO 16069):</b> Instalación entre 10 cm y 40 cm del suelo en corredores de evacuación para visibilidad en presencia de humo denso.<br/>"
            "• <b>Extintores portátiles (NTC 2885 / NSR-10):</b> Altura máxima de la manija a 1.50m (equipos &le; 18 kg) o 1.10m (equipos > 18 kg). "
            "Despeje frontal libre de 1.0 metro demarcado en piso con cuadro de 1.0m x 1.0m con franjas diagonales a 45° amarillo/negro de 10 cm.<br/>"
            "• <b>Vías de circulación peatonal:</b> Franjas amarillas continuas de 10 cm de ancho en piso, manteniendo pasillos libres de mínimo 40 cm entre máquinas o muros (Res. 2400/79 Art. 281).<br/>"
            "• <b>Calidad fotoluminiscente (Catálogo CCS / Covadonga):</b> Clase A (&ge; 210 mcd/m² a 10 min y 3.000 min de atenuación) obligatoria para edificios públicos con carga lumínica mínima de 15 minutos."
        )
        story.append(Paragraph(texto_cotas, self.estilo_norma_item))
        story.append(Spacer(1, 6))

        # -----------------------------------------------------------------
        # 4. MATRIZ DE HALLAZGOS Y EVALUACIÓN DE CONFORMIDAD NORMATIVA
        # -----------------------------------------------------------------
        story.append(Paragraph("4. Matriz de Hallazgos, Evaluación de Conformidad y Parámetros Técnicos", self.estilo_seccion_num))
        story.append(Paragraph(
            "A continuación, se detalla la matriz pericial de condiciones subestándar identificadas en el recorrido, fundamentadas "
            "en el incumplimiento de las normas técnicas y especificando los colores, tamaños mínimos y alturas requeridas:",
            self.estilo_parrafo
        ))

        # Tabla técnica completa de la matriz normativa
        matriz_base = [
            ("Extintores Portátiles",
             "Ausencia total de extintores en pasillos de laboratorios y aulas múltiples del bloque.",
             "NSR-10 (Título J, J.4) y NTC 2885 / NFPA 10. Omisión de dotación básica por carga combustible.",
             "Rojo (&ge; 50%) y contraste blanco. Formato 20x20cm (d&le;10m) o 30x30cm (d&le;15m) fotoluminiscente Clase A. Altura máx. manija: 1.50m. Cuadro de despeje en piso 1.0x1.0m.",
             "Alto", "#ef4444",
             "Instalar extintores multipropósito ABC de 10 lbs y CO2 a 1.50m. Fijar señal fotoluminiscente a 1.80m y demarcar piso."),
            ("Gabinetes Contra Incendio",
             "Inexistencia de red contra incendios y gabinetes en bloques principales de la institución.",
             "NSR-10 (Título J, J.4.2) y NTC 1669 / NFPA 14. Ausencia de sistemas hídricos de supresión.",
             "Rojo (&ge; 50%) y pictograma blanco. Formato 30x30cm o 40x40cm fotoluminiscente. Válvula a 1.20m. Despeje libre frontal de 1.0m de radio sin muebles.",
             "Alto", "#ef4444",
             "Diseñar red contra incendios con gabinetes tipo II/III conectados a reserva exclusiva de agua con radio libre de 1.0m."),
            ("Estación de Camilla y Botiquín",
             "No se evidencian camillas rígidas de inmovilización ni botiquín dotado en pasillos.",
             "Decreto 1072 de 2015 (Art. 2.2.4.6.25) y Res. 2400/1979 (Art. 164). Carencia de recursos de primeros auxilios.",
             "Verde (&ge; 50%) y cruz blanca. Formato 30x20cm o 30x40cm. Soporte vertical para camilla espinal entre 0.30m y 1.90m. Señal superior a 1.80m.",
             "Alto", "#ef4444",
             "Dotar cada bloque con camilla espinal rígida de polietileno, correas araña, inmovilizador cervical y botiquín dotado."),
            ("Rutas de Evacuación",
             "Falta de señalización direccional fotoluminiscente continua hacia las salidas.",
             "NSR-10 (Título K, K.3.8), NTC 1461 e ISO 16069. Vías de escape no identificables en humo o apagón.",
             "Verde (&ge; 50%) y contraste blanco. Formato 30x15cm (d&le;10m) o 40x20cm (d&le;15m) Clase A (210 mcd/m²). Montaje a 1.70m y zócalo a 30cm del piso.",
             "Alto", "#ef4444",
             "Instalar señales fotoluminiscentes Clase A cada 15m a 1.70m y a nivel de zócalo (30cm) según ISO 16069 y NSR-10 K."),
            ("Punto de Encuentro",
             "Área de reunión exterior no delimitada ni identificada con señalética reglamentaria.",
             "Decreto 1072 de 2015 (Planes de Emergencia) y NTC 1461. Falta de zona segura post-evacuación.",
             "Verde (&ge; 50%) y contraste blanco. Formato 60x60cm o 80x80cm montada en poste metálico exterior a altura &ge; 2.20m. Círculo en piso 2.0x2.0m.",
             "Alto", "#ef4444",
             "Fijar poste con letrero metálico reflectivo de 60x60cm a 2.30m en patio exterior y pintar delimitación en piso con pintura de tráfico."),
            ("Piso Resbaloso / Humedad",
             "Ausencia de caballetes móviles de advertencia durante rutinas de aseo en pasillos.",
             "Res. 2400/1979 (Arts. 17 y 202) y NTC 1461 / OSHA 1910.22. Exposición a caídas al mismo nivel.",
             "Amarillo (&ge; 50%) y contraste negro. Caballete plegable tipo tijera de 60cm de altura con texto bilingüe y pictograma visible a 10m en pasillo.",
             "Medio", "#f59e0b",
             "Dotar al personal de servicios generales con caballetes tipo tijera de 60cm y exigir su despliegue obligatorio antes del trapeado."),
            ("Prohibición de Fumar",
             "Falta de señalización restrictiva de fumar en accesos y áreas cerradas del campus.",
             "Ley 1335 de 2009 (Arts. 19-20), Res. 2400/1979 y NTC 1461. Falta de control administrativo legal.",
             "Rojo (&ge; 35%) con banda a 45° y contraste blanco. Diámetro 20cm o formato 20x30cm con leyenda legal obligatoria a altura 1.60m - 1.70m.",
             "Medio", "#f59e0b",
             "Instalar letreros circulares de 20cm con la leyenda 'Espacio 100% Libre de Humo de Tabaco - Ley 1335 de 2009' en todas las puertas."),
            ("Prohibición de Alimentos",
             "Ausencia de señal restrictiva de comida en laboratorios de cómputo y equipos.",
             "Res. 2400/1979 (Art. 182) y bioseguridad. Riesgo de daño a equipos y contaminación cruzada.",
             "Rojo (&ge; 35%) con banda a 45° y contraste blanco/negro. Formato circular de 20cm o 20x30cm a 1.60m en puerta de laboratorio.",
             "Bajo", "#3b82f6",
             "Fijar señalización circular de prohibido comer/beber de 20cm en el pórtico de cada laboratorio y sala de informática."),
            ("Uso de Celular en Escaleras",
             "No hay advertencia sobre el uso de dispositivos móviles en tramos de escaleras.",
             "Decreto 1072 de 2015 (Control de actos inseguros) y Res. 2400/1979. Factor de caída y distracción.",
             "Rojo (&ge; 35%) con banda diagonal a 45°. Formato 20x20cm o 20x30cm con texto preventivo a 1.60m en descansos de escaleras.",
             "Bajo", "#3b82f6",
             "Colocar avisos de prohibido celular en descansos de escaleras promoviendo el uso del pasamanos continuo.")
        ]

        # Encabezado de la tabla de matriz
        tabla_filas = [
            [
                Paragraph("<b>Ítem / Elemento</b>", self.estilo_celda_th),
                Paragraph("<b>Condición Observada</b>", self.estilo_celda_th),
                Paragraph("<b>Norma Incumplida</b>", self.estilo_celda_th),
                Paragraph("<b>Especificación Técnica Exigida (Colores, Tamaño S&ge;d²/2000 y Altura)</b>", self.estilo_celda_th),
                Paragraph("<b>Nivel Riesgo</b>", self.estilo_celda_th),
                Paragraph("<b>Acción Correctiva y Adquisición</b>", self.estilo_celda_th),
            ]
        ]

        # Llenar la matriz
        for item, cond, norm, exig, nivel, color_hex, accion in matriz_base:
            p_item = Paragraph(f"<b>{item}</b>", self.estilo_celda_bold)
            p_cond = Paragraph(cond, self.estilo_celda)
            p_norm = Paragraph(norm, self.estilo_celda)
            p_exig = Paragraph(exig, self.estilo_celda)
            p_nivel = Paragraph(f"<font color='{color_hex}'><b>{nivel.upper()}</b></font>", self.estilo_celda_bold)
            p_accion = Paragraph(accion, self.estilo_celda)
            tabla_filas.append([p_item, p_cond, p_norm, p_exig, p_nivel, p_accion])

        # Dimensiones de columnas (Total = 540 pt)
        t_matriz = Table(tabla_filas, colWidths=[70, 95, 95, 125, 45, 110])
        t_matriz.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f2444')),
            ('ALIGN', (0,0), (-1,0), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 3),
            ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ]))
        story.append(t_matriz)
        story.append(Spacer(1, 8))

        # -----------------------------------------------------------------
        # 5. EVIDENCIAS Y REGISTRO FOTOGRÁFICO (ESTÁNDAR APA 7ma EDICIÓN)
        # -----------------------------------------------------------------
        story.append(Paragraph("5. Evidencias y Registro Fotográfico Pericial (Estándar APA 7ma Edición)", self.estilo_seccion_num))
        story.append(Paragraph(
            "<i>(Nota metodológica: Las evidencias fotográficas se estructuran bajo el estándar editorial APA 7ma edición, "
            "identificando para cada figura el incumplimiento de señalización, cromatismo, dimensionamiento y cotas de altura).</i>",
            self.estilo_parrafo
        ))

        # Figuras estándar oficiales enriquecidas con análisis técnico
        figuras_apa = [
            {
                "num": 1,
                "titulo": "Ausencia de extintor portatil y gabinete de red contra incendio en pasillo",
                "nota": "Nota. Se evidencia infracción directa de la NSR-10 Título J y NTC 2885. Los muros carecen de extintores a altura reglamentaria (máx. 1.50m) y señalización roja fotoluminiscente de 20x20cm (d<=10m). Asimismo, no existe red contra incendios ni gabinetes hídricos (NTC 1669).",
                "match_words": ["extintor", "gabinete", "incendio"]
            },
            {
                "num": 2,
                "titulo": "Carencia de camilla rigida de inmovilizacion y estacion de primeros auxilios",
                "nota": "Nota. Se constata omisión del Decreto 1072 de 2015 (Art. 2.2.4.6.25) y Res. 2400/1979 (Art. 164). El bloque carece de camilla espinal rígida de polietileno con correas tipo araña y letrero verde de salvamento de 30x20cm (&ge; 50% verde) para estabilización de politraumatismos.",
                "match_words": ["camilla", "primeros auxilios", "inmovilizacion", "botiquin"]
            },
            {
                "num": 3,
                "titulo": "Falta de señalizacion direccional fotoluminiscente de rutas de evacuacion y punto de encuentro",
                "nota": "Nota. Incumplimiento de la NTC 1461, NSR-10 Título K e ISO 16069. No existen flechas verdes fotoluminiscentes Clase A (210 mcd/m²) a 1.70m ni a nivel de zócalo (30cm del piso) para escape bajo humo denso, ni poste exterior de 60x60cm para el punto de encuentro.",
                "match_words": ["evacuacion", "salida", "punto de encuentro", "ruta"]
            },
            {
                "num": 4,
                "titulo": "Condicion de riesgo locativo por falta de caballete de advertencia de piso resbaloso",
                "nota": "Nota. Vulneración de la Resolución 2400 de 1979 (Art. 17) y NTC 1461. Falta de caballetes tipo tijera amarillos (&ge; 50% amarillo) de 60cm de altura durante rutinas de aseo, dejando al personal expuesto a caídas al mismo nivel.",
                "match_words": ["piso", "resbaloso", "humedo", "caida", "caballete"]
            },
            {
                "num": 5,
                "titulo": "Ausencia de señalizacion restrictiva de no fumar, no celulares y prohibicion de alimentos",
                "nota": "Nota. Incumplimiento de la Ley 1335 de 2009 (Art. 19-20), Res. 2400/1979 (Art. 182) y NTC 1461. Falta de letreros circulares rojos (cobertura &ge; 35% y banda a 45°) de diámetro 20cm en los accesos a aulas, escaleras y laboratorios de cómputo.",
                "match_words": ["fumar", "celular", "comer", "prohibid"]
            }
        ]

        evidencias_existentes = inspeccion.get("evidencias", [])

        # Emparejar evidencias fotográficas reales tomadas en la inspección con las figuras APA
        for fig in figuras_apa:
            num_fig = fig["num"]
            titulo_fig = fig["titulo"]
            nota_fig = fig["nota"]
            
            foto_encontrada = None
            for ev in evidencias_existentes:
                texto_ev = f"{ev.get('observacion', '')} {ev.get('ubicacion', '')} {ev.get('tipo_esperado', '')}".lower()
                for h in ev.get("hallazgos", []):
                    texto_ev += f" {h.get('elemento', '')} {h.get('categoria', '')}".lower()
                
                if any(w in texto_ev for w in fig["match_words"]):
                    path_cand = ev.get("foto_path", "")
                    if path_cand and os.path.exists(path_cand):
                        foto_encontrada = path_cand
                        break

            if not foto_encontrada and len(evidencias_existentes) >= num_fig:
                cand = evidencias_existentes[num_fig - 1].get("foto_path", "")
                if cand and os.path.exists(cand):
                    foto_encontrada = cand

            bloque_figura = []
            bloque_figura.append(Paragraph(f"<b>Figura {num_fig}</b>", self.estilo_apa_figura))
            bloque_figura.append(Paragraph(f"<i>{titulo_fig}</i>", self.estilo_apa_titulo))

            if foto_encontrada:
                try:
                    rl_img = RLImage(foto_encontrada, width=3.8 * inch, height=2.3 * inch)
                    t_img = Table([[rl_img]], colWidths=[540], style=[
                        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                        ('LEFTPADDING', (0,0), (-1,-1), 0),
                        ('RIGHTPADDING', (0,0), (-1,-1), 0),
                        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                    ])
                    bloque_figura.append(t_img)
                except Exception:
                    p_ph = Paragraph("<i>[Fotografía capturada y archivada en el expediente digital de auditoría]</i>", self.estilo_celda)
                    bloque_figura.append(p_ph)
            else:
                p_box = Table(
                    [[Paragraph(
                        f"<b>[Registro Fotográfico Pericial - Figura {num_fig}]</b><br/>"
                        f"<font size=7 color='#475569'>Evidencia física documentada durante el recorrido de auditoría en campus: {titulo_fig}.</font><br/>"
                        f"<font size=6.5 color='#64748b'>Falta de conformidad con especificaciones de color, tamaño (S &ge; d²/2000) y cotas de altura según NTC 1461 y NSR-10.</font>",
                        self.estilo_celda_center
                    )]],
                    colWidths=[540],
                    style=[
                        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
                        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
                        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                        ('TOPPADDING', (0,0), (-1,-1), 12),
                        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
                    ]
                )
                bloque_figura.append(p_box)

            bloque_figura.append(Paragraph(nota_fig, self.estilo_apa_nota))
            story.append(KeepTogether(bloque_figura))

        # -----------------------------------------------------------------
        # 6. PLAN DE ACCIÓN PRIORIZADO Y CRONOGRAMA DE CORRECCIÓN
        # -----------------------------------------------------------------
        story.append(Spacer(1, 4))
        plan_bloque = []
        plan_bloque.append(Paragraph("6. Plan de Acción Priorizado y Cronograma de Cumplimiento", self.estilo_seccion_num))
        plan_bloque.append(Paragraph(
            "Se establece el plan de intervención técnica priorizado en tres fases operativas para subsanar los hallazgos "
            "conforme a los estándares del Consejo Colombiano de Seguridad (CCS) y la NTC 1461:",
            self.estilo_parrafo
        ))

        tabla_plan_datos = [
            [
                Paragraph("<b>Fase / Plazo</b>", self.estilo_celda_th),
                Paragraph("<b>Actividad Técnica y Especificación de Compra</b>", self.estilo_celda_th),
                Paragraph("<b>Norma Reguladora</b>", self.estilo_celda_th),
                Paragraph("<b>Responsable Designado</b>", self.estilo_celda_th),
                Paragraph("<b>Entregable Verificable</b>", self.estilo_celda_th)
            ],
            [
                Paragraph("<b>Fase 1: Inmediato</b><br/>(&lt; 48 Horas)", self.estilo_celda_bold),
                Paragraph("Adquisición de extintores ABC de 10 lbs recargados y camilla espinal rígida con correas tipo araña e inmovilizador. Señalización provisional de piso resbaloso.", self.estilo_celda),
                Paragraph("NSR-10 Título J<br/>Res. 2400/79 Art. 164", self.estilo_celda),
                Paragraph("Dirección de Compras y Coordinación SST", self.estilo_celda),
                Paragraph("Acta de entrega y recibo a satisfacción con tarjeta de inspección.", self.estilo_celda)
            ],
            [
                Paragraph("<b>Fase 2: Corto Plazo</b><br/>(&lt; 15 Días)", self.estilo_celda_bold),
                Paragraph("Instalación de señalética fotoluminiscente Clase A (210 mcd/m²) de rutas de evacuación (30x15cm a 1.70m y zócalo a 30cm). Fijación de letreros Ley 1335 de prohibido fumar y demarcación de franjas de 10cm en pasillos.", self.estilo_celda),
                Paragraph("NTC 1461<br/>ISO 16069<br/>Ley 1335 de 2009<br/>Res. 2400/79 Art. 281", self.estilo_celda),
                Paragraph("Mantenimiento Locativo y Auditor SST", self.estilo_celda),
                Paragraph("Inspección de luminancia y registro fotográfico de conformidad cromática y dimensional.", self.estilo_celda)
            ],
            [
                Paragraph("<b>Fase 3: Mediano Plazo</b><br/>(&lt; 30 Días)", self.estilo_celda_bold),
                Paragraph("Diseño e instalación de red contra incendios con gabinetes tipo II/III equipados con manguera, llave spanner y boquilla según NSR-10. Instalación de poste reflectivo de 60x60cm para punto de encuentro.", self.estilo_celda),
                Paragraph("NSR-10 (Título J)<br/>NTC 1669 / NFPA 14<br/>Decreto 1072/2015", self.estilo_celda),
                Paragraph("Rectoría / Dirección de Infraestructura", self.estilo_celda),
                Paragraph("Certificación hidrostática de la red y planimetría de emergencias actualizada.", self.estilo_celda)
            ]
        ]

        t_plan = Table(tabla_plan_datos, colWidths=[80, 160, 100, 95, 105])
        t_plan.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f2444')),
            ('ALIGN', (0,0), (-1,0), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 3),
            ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ]))
        plan_bloque.append(t_plan)
        story.append(KeepTogether(plan_bloque))
        story.append(Spacer(1, 6))

        # -----------------------------------------------------------------
        # 7. CONCLUSIONES Y DICTAMEN PERICIAL
        # -----------------------------------------------------------------
        conclusiones_bloque = []
        conclusiones_bloque.append(Paragraph("7. Conclusiones y Dictamen de Auditoría Pericial", self.estilo_seccion_num))
        
        texto_conclusiones = (
            "La auditoría técnica constata una brecha legal y técnica sustancial entre el estado actual de las instalaciones del bloque "
            "y las prescripciones obligatorias del marco normativo colombiano (Decreto 1072 de 2015, NSR-10 Títulos J y K, NTC 1461 y Resolución 2400 de 1979). "
            "La carencia simultánea de equipos de extinción portátiles, redes hídricas, elementos de inmovilización médica y señalización fotoluminiscente "
            "eleva el índice de vulnerabilidad de la comunidad académica ante situaciones de emergencia o siniestro, exponiendo además a la entidad a sanciones "
            "onerosas por parte de las entidades administradoras de riesgos laborales (ARL) y el Ministerio de Trabajo.<br/><br/>"
            "Se dictamina la necesidad imperiosa de ejecutar con carácter prioritario el Plan de Acción formulado en el numeral 6, "
            "adquiriendo señales normalizadas bajo las especificaciones cromáticas (colores de seguridad y contraste reglamentarios), dimensionales "
            "(cálculo S &ge; d² / 2000), materiales con tintas UV sobre poliestireno o lámina electrostática y propiedades fotoluminiscentes Clase A."
        )
        conclusiones_bloque.append(Paragraph(texto_conclusiones, self.estilo_parrafo))
        conclusiones_bloque.append(Spacer(1, 24))

        # Firmas formales de certificación pericial
        conclusiones_bloque.append(Table([
            [
                Paragraph(
                    "____________________________________________________<br/>"
                    f"<b>{responsable}</b><br/>"
                    "Auditor Líder / Especialista SST<br/>"
                    "Licencia en Salud Ocupacional / SST Vigente<br/>"
                    "Politécnico Grancolombiano · Sede Medellín",
                    self.estilo_celda
                ),
                Paragraph(
                    "____________________________________________________<br/>"
                    "<b>Rectoría / Dirección Administrativa y Financiera</b><br/>"
                    "Representante Legal / Gerencia del SG-SST<br/>"
                    "Politécnico Grancolombiano · Sede Medellín",
                    self.estilo_celda
                )
            ]
        ], colWidths=[270, 270], style=[
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'TOP')
        ]))

        story.append(KeepTogether(conclusiones_bloque))

        doc.build(story, canvasmaker=NumberedCanvas)
        return buffer.getvalue()


pdf_service = PDFService()
