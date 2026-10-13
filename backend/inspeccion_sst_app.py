import os
import sys
import time
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import cv2

# Asegurar ruta para imports relativos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from sst_multi_detector import detectar_todo

# Catálogo Oficial de Señales de SST
CATALOGO_SST = {
    # Evacuación y Emergencia (Verdes)
    "ruta_evacuacion": {
        "elemento": "Ruta de Evacuación",
        "categoria": "Evacuación y Emergencia (Verdes)",
        "color": "#27ae60",
        "descripcion": "Flecha que indica la dirección de salida segura hacia la zona de evacuación.",
        "condicion_default": "Conforme",
        "alias": ["ruta de evacuacion", "evacuacion", "down arrow sign", "arrow", "salida", "rota de fuga", "left exit", "right exit", "straight exit"]
    },
    "salida_emergencia": {
        "elemento": "Salida de Emergencia (Exit)",
        "categoria": "Evacuación y Emergencia (Verdes)",
        "color": "#27ae60",
        "descripcion": "Ubicada directamente sobre las puertas de escape para desalojo inmediato.",
        "condicion_default": "Conforme",
        "alias": ["salida de emergencia", "emergency-exit", "emergency exit sign", "exit", "door", "puerta de emergencia"]
    },
    "punto_encuentro": {
        "elemento": "Punto de Encuentro",
        "categoria": "Evacuación y Emergencia (Verdes)",
        "color": "#27ae60",
        "descripcion": "Zona exterior segura para agrupar y contabilizar a las personas evacuadas.",
        "condicion_default": "Conforme",
        "alias": ["punto de encuentro", "assembly point", "assembly point sign", "punto_de_reunion"]
    },
    "botiquin": {
        "elemento": "Botiquín",
        "categoria": "Evacuación y Emergencia (Verdes)",
        "color": "#27ae60",
        "descripcion": "Ubicación de los elementos de primeros auxilios y atención médica primaria.",
        "condicion_default": "Requiere verificación de inventario",
        "alias": ["botiquin", "first_aid_signage", "primeros auxilios", "first aid"]
    },
    "camilla": {
        "elemento": "Camilla de Emergencia",
        "categoria": "Evacuación y Emergencia (Verdes)",
        "color": "#27ae60",
        "descripcion": "Ubicación de la camilla rígida de rescate e inmovilización para brigadistas.",
        "condicion_default": "Conforme (Disponible y despejada)",
        "alias": ["camilla", "stretcher", "camilla de emergencia", "camilla de primeros auxilios"]
    },

    # Equipos Contra Incendio (Rojas)
    "extintor": {
        "elemento": "Extintor",
        "categoria": "Equipos Contra Incendio (Rojas)",
        "color": "#e74c3c",
        "descripcion": "Ubicación del cilindro presurizado contra fuego (PQS / ABC, CO₂ o Agua).",
        "condicion_default": "Requiere verificación de manómetro y vigencia",
        "alias": ["extintor", "extintor de po quimico", "pqs", "fire extinguisher", "cilindro"]
    },
    "gabinete_incendio": {
        "elemento": "Gabinete de Incendio",
        "categoria": "Equipos Contra Incendio (Rojas)",
        "color": "#e74c3c",
        "descripcion": "Lugar de la manguera contra incendio, llave de ajuste y herramientas de bomberos.",
        "condicion_default": "Requiere verificación de accesibilidad y manguera",
        "alias": ["gabinete de incendio", "gabinete_incendio", "fire_hose_box", "fire-cabinet", "fire hose", "caja de manguera", "abrigo para mangueira", "angle value", "f-wrench"]
    },
    "pulsador_alarma": {
        "elemento": "Pulsador de Alarma",
        "categoria": "Equipos Contra Incendio (Rojas)",
        "color": "#e74c3c",
        "descripcion": "Estación manual o botón de activación de alerta sonora para evacuación y emergencia.",
        "condicion_default": "Conforme",
        "alias": [
            "pulsador de alarma", "alarma de emergencia", "alarma contra incendios", 
            "senal de alarma contra incendios", "alarma", "alarm", "fire alarm", 
            "acionador de incendio", "pulsador", "estacion manual"
        ]
    },

    # Advertencia de Peligro (Amarillas)
    "riesgo_electrico": {
        "elemento": "Riesgo Eléctrico",
        "categoria": "Advertencia de Peligro (Amarillas)",
        "color": "#f39c12",
        "descripcion": "En tableros eléctricos, cuartos técnicos y servidores (alta tensión).",
        "condicion_default": "Precaución / Requiere acceso restringido",
        "alias": ["riesgo electrico", "alta tension", "alta_tension", "high voltage", "riesgo eléctrico"]
    },
    "piso_resbaladizo": {
        "elemento": "Piso Resbaladizo",
        "categoria": "Advertencia de Peligro (Amarillas)",
        "color": "#f39c12",
        "descripcion": "Alerta temporal por limpieza, piso húmedo o derrames para evitar caídas.",
        "condicion_default": "Riesgo temporal activo",
        "alias": ["piso resbaladizo", "piso mojado", "piso_mojado", "wet_floor_sign", "caution", "wet floor"]
    },
    "escalon_desnivel": {
        "elemento": "Cuidado con el Escalón / Desnivel",
        "categoria": "Advertencia de Peligro (Amarillas)",
        "color": "#f39c12",
        "descripcion": "Alerta de tropiezos o caídas a nivel en pasillos, gradas o rampas.",
        "condicion_default": "Precaución",
        "alias": ["escalon", "desnivel", "escalera", "stair", "step", "warning"]
    },
    "riesgo_quimico_biologico": {
        "elemento": "Riesgo Químico / Biológico",
        "categoria": "Advertencia de Peligro (Amarillas)",
        "color": "#f39c12",
        "descripcion": "En laboratorios, áreas de almacenamiento de sustancias y depósito de residuos.",
        "condicion_default": "Peligro / Uso obligatorio de EPP",
        "alias": ["riesgo quimico", "riesgo biologico", "biohazard", "material_toxico", "inflamable", "peligro_general"]
    },

    # Obligación y Comportamiento (Azules)
    "gafas_seguridad": {
        "elemento": "Uso Obligatorio de Gafas",
        "categoria": "Obligación y Comportamiento (Azules)",
        "color": "#2980b9",
        "descripcion": "Protección ocular requerida en laboratorios, talleres o áreas de partículas.",
        "condicion_default": "Cumplimiento obligatorio",
        "alias": ["gafas", "proteccion ocular", "eye protection", "glasses"]
    },
    "bata": {
        "elemento": "Uso Obligatorio de Bata",
        "categoria": "Obligación y Comportamiento (Azules)",
        "color": "#2980b9",
        "descripcion": "Vestimenta requerida en áreas de prácticas, laboratorios y toma de muestras.",
        "condicion_default": "Cumplimiento obligatorio",
        "alias": ["bata", "lab coat"]
    },
    "puerta_cerrada": {
        "elemento": "Mantener Puerta Cerrada",
        "categoria": "Obligación y Comportamiento (Azules)",
        "color": "#2980b9",
        "descripcion": "En puertas cortafuego de escaleras de emergencia y cuartos técnicos.",
        "condicion_default": "Cumplimiento obligatorio",
        "alias": ["puerta cerrada", "mantener cerrada", "keep closed"]
    },
    "tapabocas": {
        "elemento": "Uso Obligatorio de Tapabocas",
        "categoria": "Obligación y Comportamiento (Azules)",
        "color": "#2980b9",
        "descripcion": "En áreas de salud, manipulación biológica o prevención de contagios.",
        "condicion_default": "Cumplimiento obligatorio",
        "alias": ["tapabocas", "mascarilla", "mask"]
    },

    # Prohibición (Rojas con diagonal)
    "prohibido_fumar": {
        "elemento": "Prohibido Fumar / Vapear",
        "categoria": "Prohibición (Rojas con diagonal)",
        "color": "#c0392b",
        "descripcion": "En todos los espacios cerrados del edificio, pasillos y áreas comunes.",
        "condicion_default": "Prohibición estricta",
        "alias": ["prohibido fumar", "prohibido_fumar", "no smoking", "no-smoking-sign", "no_smoking_signage"]
    },
    "prohibido_paso": {
        "elemento": "Prohibido el Paso / Solo Personal Autorizado",
        "categoria": "Prohibición (Rojas con diagonal)",
        "color": "#c0392b",
        "descripcion": "En azoteas, cuartos de máquinas, subestaciones y servidores.",
        "condicion_default": "Acceso restringido",
        "alias": ["prohibido el paso", "prohibido_paso", "no entry", "personal autorizado"]
    },
    "no_ascensor_emergencia": {
        "elemento": "No Usar Ascensor en Caso de Emergencia",
        "categoria": "Prohibición (Rojas con diagonal)",
        "color": "#c0392b",
        "descripcion": "Al lado de los ascensores para evitar atrapamiento durante sismos o incendios.",
        "condicion_default": "Advertencia crítica de seguridad",
        "alias": ["no usar ascensor", "ascensor emergencia", "elevator emergency", "do not use elevator"]
    },
    "prohibido_alimentos": {
        "elemento": "Prohibido Ingresar con Alimentos",
        "categoria": "Prohibición (Rojas con diagonal)",
        "color": "#c0392b",
        "descripcion": "En salas de cómputo, laboratorios y bibliotecas para proteger equipos.",
        "condicion_default": "Prohibición",
        "alias": ["prohibido alimentos", "no food", "sin comida"]
    }
}

def normalizar_texto(texto):
    reemplazos = (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"))
    t = texto.lower()
    for o, d in reemplazos:
        t = t.replace(o, d)
    return t

def clasificar_con_catalogo(clase_detectada, texto_usuario=""):
    """Mapea lo que detectó YOLO / Roboflow con el catálogo normativo de SST"""
    busqueda = normalizar_texto(f"{clase_detectada} {texto_usuario}")
    
    for clave, item in CATALOGO_SST.items():
        for alias in item["alias"]:
            if alias in busqueda:
                return item
                
    # Caso por defecto si es una señal no clasificada
    return {
        "elemento": clase_detectada.capitalize() if clase_detectada else "Señal de Seguridad",
        "categoria": "General SST",
        "color": "#7f8c8d",
        "descripcion": "Elemento de seguridad identificado en inspección física.",
        "condicion_default": "Requiere verificación por inspector",
    }

class AppInspeccionSST:
    def __init__(self, root):
        self.root = root
        self.root.title("SST-IA: Asistente Inteligente de Inspecciones (Estilo Flutter)")
        self.root.geometry("1100x720")
        self.root.configure(bg="#1e1e2e")

        self.cap = cv2.VideoCapture(0)
        self.foto_actual = None
        self.foto_cv2 = None
        self.hallazgos_registrados = []

        self._crear_interfaz()
        self._actualizar_camara()

    def _crear_interfaz(self):
        # Header Superior
        header = tk.Frame(self.root, bg="#11111b", height=50)
        header.pack(fill="x")
        lbl_titulo = tk.Label(
            header, 
            text="🛡️ SST-IA: Registro y Análisis Inteligente de Inspección", 
            font=("Segoe UI", 14, "bold"), 
            fg="#cdd6f4", 
            bg="#11111b"
        )
        lbl_titulo.pack(pady=10)

        # Contenedor Principal (2 Columnas)
        main_frame = tk.Frame(self.root, bg="#1e1e2e")
        main_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # --- Columna Izquierda: Captura de Foto / Evidencia ---
        col_izq = tk.LabelFrame(main_frame, text=" 📸 Evidencia Visual (Cámara / Imagen) ", font=("Segoe UI", 11, "bold"), fg="#89b4fa", bg="#181825")
        col_izq.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.lbl_video = tk.Label(col_izq, bg="#11111b")
        self.lbl_video.pack(fill="both", expand=True, padx=10, pady=10)

        botones_foto = tk.Frame(col_izq, bg="#181825")
        botones_foto.pack(fill="x", padx=10, pady=(0, 10))

        self.btn_tomar_foto = tk.Button(
            botones_foto, 
            text="📸 Tomar Foto de Evidencia", 
            font=("Segoe UI", 10, "bold"), 
            bg="#a6e3a1", 
            fg="#11111b", 
            command=self.capturar_foto, 
            cursor="hand2"
        )
        self.btn_tomar_foto.pack(side="left", expand=True, fill="x", padx=5)

        self.btn_subir_foto = tk.Button(
            botones_foto, 
            text="📁 Cargar Archivo...", 
            font=("Segoe UI", 10, "bold"), 
            bg="#89b4fa", 
            fg="#11111b", 
            command=self.cargar_archivo, 
            cursor="hand2"
        )
        self.btn_subir_foto.pack(side="right", expand=True, fill="x", padx=5)

        # --- Columna Derecha: Parámetros del Usuario y Análisis IA ---
        col_der = tk.LabelFrame(main_frame, text=" 📋 Datos de la Inspección & Análisis IA ", font=("Segoe UI", 11, "bold"), fg="#a6e3a1", bg="#181825")
        col_der.pack(side="right", fill="both", expand=True)

        # Parámetros que ingresa el usuario (como en la app de Flutter)
        form_frame = tk.Frame(col_der, bg="#181825")
        form_frame.pack(fill="x", padx=15, pady=10)

        tk.Label(form_frame, text="Ubicación Física:", font=("Segoe UI", 10, "bold"), fg="#cdd6f4", bg="#181825").grid(row=0, column=0, sticky="w", pady=3)
        self.txt_ubicacion = tk.Entry(form_frame, font=("Segoe UI", 10), bg="#313244", fg="#cdd6f4", insertbackground="white")
        self.txt_ubicacion.insert(0, "Piso 2 - Pasillo Principal / Escaleras")
        self.txt_ubicacion.grid(row=0, column=1, sticky="ew", padx=5, pady=3)

        tk.Label(form_frame, text="Señal a Inspeccionar:", font=("Segoe UI", 10, "bold"), fg="#a6e3a1", bg="#181825").grid(row=1, column=0, sticky="w", pady=3)
        self.combo_senal_esperada = ttk.Combobox(form_frame, values=[
            "🔍 [Automático] Detectar Cualquier Señal",
            "🟢 Camilla de Emergencia",
            "🟢 Salida de Emergencia (Exit)",
            "🟢 Ruta de Evacuación",
            "🟢 Punto de Encuentro",
            "🟢 Botiquín",
            "🔴 Extintor",
            "🔴 Gabinete de Incendio",
            "🔴 Pulsador de Alarma",
            "🟡 Riesgo Eléctrico",
            "🟡 Piso Resbaladizo",
            "🟡 Cuidado con el Escalón / Desnivel",
            "🟡 Riesgo Químico / Biológico",
            "🔵 Uso Obligatorio de Gafas",
            "🔵 Uso Obligatorio de Bata",
            "🔵 Mantener Puerta Cerrada",
            "🔵 Uso Obligatorio de Tapabocas",
            "🚫 Prohibido Fumar / Vapear",
            "🚫 Prohibido el Paso / Personal Autorizado",
            "🚫 No Usar Ascensor en Caso de Emergencia",
            "🚫 Prohibido Ingresar con Alimentos"
        ], font=("Segoe UI", 9))
        self.combo_senal_esperada.set("🟢 Camilla de Emergencia")
        self.combo_senal_esperada.grid(row=1, column=1, sticky="ew", padx=5, pady=3)

        tk.Label(form_frame, text="Observación del Inspector:", font=("Segoe UI", 10, "bold"), fg="#cdd6f4", bg="#181825").grid(row=2, column=0, sticky="w", pady=3)
        self.txt_observacion = tk.Entry(form_frame, font=("Segoe UI", 10), bg="#313244", fg="#cdd6f4", insertbackground="white")
        self.txt_observacion.insert(0, "Inspección de equipo y señalización obligatoria")
        self.txt_observacion.grid(row=2, column=1, sticky="ew", padx=5, pady=3)

        tk.Label(form_frame, text="Área / Sección:", font=("Segoe UI", 10, "bold"), fg="#cdd6f4", bg="#181825").grid(row=3, column=0, sticky="w", pady=3)
        self.combo_area = ttk.Combobox(form_frame, values=["Áreas Comunes", "Laboratorio", "Salas de Cómputo", "Cuarto de Máquinas", "Talleres", "Salidas"], font=("Segoe UI", 9))
        self.combo_area.set("Áreas Comunes")
        self.combo_area.grid(row=3, column=1, sticky="ew", padx=5, pady=3)

        form_frame.columnconfigure(1, weight=1)

        # Botón Analizar con IA
        self.btn_analizar = tk.Button(
            col_der, 
            text="⚡ Analizar con IA & Evaluar Similitud", 
            font=("Segoe UI", 11, "bold"), 
            bg="#f9e2af", 
            fg="#11111b", 
            command=self.ejecutar_analisis, 
            cursor="hand2"
        )
        self.btn_analizar.pack(fill="x", padx=15, pady=5)

        # Tarjeta de Resultados (Hallazgo Generado)
        self.card_resultado = tk.LabelFrame(col_der, text=" 🎯 Evaluación de Similitud y Hallazgo ", font=("Segoe UI", 10, "bold"), fg="#f9e2af", bg="#313244")
        self.card_resultado.pack(fill="both", expand=True, padx=15, pady=10)

        self.lbl_similitud = tk.Label(self.card_resultado, text="Estado: (Esperando análisis...)", font=("Segoe UI", 11, "bold"), fg="#89b4fa", bg="#313244", anchor="w")
        self.lbl_similitud.pack(fill="x", padx=10, pady=2)

        self.lbl_elem = tk.Label(self.card_resultado, text="Elemento: -", font=("Segoe UI", 10, "bold"), fg="#cdd6f4", bg="#313244", anchor="w")
        self.lbl_elem.pack(fill="x", padx=10, pady=2)

        self.lbl_cat = tk.Label(self.card_resultado, text="Categoría: -", font=("Segoe UI", 10, "bold"), fg="#a6e3a1", bg="#313244", anchor="w")
        self.lbl_cat.pack(fill="x", padx=10, pady=2)

        self.lbl_cond = tk.Label(self.card_resultado, text="Condición: -", font=("Segoe UI", 10), fg="#f9e2af", bg="#313244", anchor="w")
        self.lbl_cond.pack(fill="x", padx=10, pady=2)

        self.lbl_desc = tk.Label(self.card_resultado, text="Descripción Normativa:\n-", font=("Segoe UI", 9), fg="#bac2de", bg="#313244", justify="left", wraplength=450, anchor="w")
        self.lbl_desc.pack(fill="x", padx=10, pady=3)

        self.lbl_conf = tk.Label(self.card_resultado, text="Certeza IA: -", font=("Segoe UI", 9, "bold"), fg="#89b4fa", bg="#313244", anchor="w")
        self.lbl_conf.pack(fill="x", padx=10, pady=2)

        # Botones de Acción (Validar o Rechazar Hallazgo como en Flutter)
        acciones = tk.Frame(col_der, bg="#181825")
        acciones.pack(fill="x", padx=15, pady=(0, 10))

        self.btn_validar = tk.Button(acciones, text="✅ Validar Hallazgo", font=("Segoe UI", 10, "bold"), bg="#a6e3a1", fg="#11111b", command=self.validar_hallazgo, state="disabled")
        self.btn_validar.pack(side="left", expand=True, fill="x", padx=5)

        self.btn_rechazar = tk.Button(acciones, text="❌ Rechazar", font=("Segoe UI", 10, "bold"), bg="#f38ba8", fg="#11111b", command=self.rechazar_hallazgo, state="disabled")
        self.btn_rechazar.pack(side="right", expand=True, fill="x", padx=5)

    def _actualizar_camara(self):
        if self.cap.isOpened() and self.foto_cv2 is None:
            ret, frame = self.cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb).resize((480, 340))
                imgtk = ImageTk.PhotoImage(image=img)
                self.lbl_video.imgtk = imgtk
                self.lbl_video.configure(image=imgtk)
        self.root.after(30, self._actualizar_camara)

    def capturar_foto(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.foto_cv2 = frame.copy()
                # Guardar evidencia local
                os.makedirs("evidencias_capturadas", exist_ok=True)
                nombre_archivo = f"evidencias_capturadas/evidencia_{int(time.time())}.jpg"
                cv2.imwrite(nombre_archivo, self.foto_cv2)
                self.foto_actual = nombre_archivo

                # Mostrar foto congelada
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb).resize((480, 340))
                imgtk = ImageTk.PhotoImage(image=img)
                self.lbl_video.imgtk = imgtk
                self.lbl_video.configure(image=imgtk)
                self.btn_tomar_foto.config(text="🔄 Reanudar Cámara", command=self.reanudar_camara)

    def reanudar_camara(self):
        self.foto_cv2 = None
        self.foto_actual = None
        self.btn_tomar_foto.config(text="📸 Tomar Foto de Evidencia", command=self.capturar_foto)

    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.jpeg *.png")])
        if ruta:
            self.foto_actual = ruta
            img_bgr = cv2.imread(ruta)
            if img_bgr is not None:
                self.foto_cv2 = img_bgr
                frame_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb).resize((480, 340))
                imgtk = ImageTk.PhotoImage(image=img)
                self.lbl_video.imgtk = imgtk
                self.lbl_video.configure(image=imgtk)
                self.btn_tomar_foto.config(text="🔄 Reanudar Cámara", command=self.reanudar_camara)

    def ejecutar_analisis(self):
        if self.foto_actual is None:
            messagebox.showwarning("Atención", "Primero toma una foto con la cámara o carga una imagen.")
            return

        self.btn_analizar.config(text="⏳ Analizando con IA...", state="disabled")
        self.root.update()

        # Determinar categoría filtro a partir de la selección del SST
        seleccion = self.combo_senal_esperada.get()
        cat_filtro = None
        if "Evacuación" in seleccion or "Camilla" in seleccion or "Salida" in seleccion or "Ruta" in seleccion or "Punto" in seleccion or "Botiquín" in seleccion:
            cat_filtro = "evacuacion"
        elif "Incendio" in seleccion or "Extintor" in seleccion or "Gabinete" in seleccion or "Pulsador" in seleccion:
            cat_filtro = "incendio"
        elif "Advertencia" in seleccion or "Riesgo" in seleccion or "Piso" in seleccion or "Escalón" in seleccion:
            cat_filtro = "advertencia"
        elif "Prohibición" in seleccion or "Fumar" in seleccion or "Paso" in seleccion or "Ascensor" in seleccion or "Alimentos" in seleccion:
            cat_filtro = "prohibicion"
        elif "Obligación" in seleccion or "Gafas" in seleccion or "Bata" in seleccion or "Puerta" in seleccion or "Tapabocas" in seleccion:
            cat_filtro = "obligacion"

        esperado_nombre = seleccion.replace("🔍 [Automático] Detectar Cualquier Señal", "Automático")
        for prefijo in ["🟢 ", "🔴 ", "🟡 ", "🔵 ", "🚫 ", "[Evacuación] ", "[Incendio] ", "[Advertencia] ", "[Obligación] ", "[Prohibición] "]:
            esperado_nombre = esperado_nombre.replace(prefijo, "")
        esperado_nombre = esperado_nombre.strip()

        # Inferencia con el multi-detector de Roboflow (escaneo completo de señales)
        try:
            detecciones = detectar_todo(self.foto_actual)
            
            # Dibujar recuadros en la imagen si hay detecciones
            if detecciones and self.foto_cv2 is not None:
                img_dibujada = self.foto_cv2.copy()
                h_orig, w_orig = img_dibujada.shape[:2]
                
                mejor_det = max(detecciones, key=lambda d: d.get("confidence", 0.0))
                clase_detectada = mejor_det.get("class", mejor_det.get("label", ""))
                conf = mejor_det.get("confidence", 0.0)

                # Clasificar con el catálogo oficial
                texto_usr = f"{self.txt_observacion.get()} {self.txt_ubicacion.get()}"
                info_sst = clasificar_con_catalogo(clase_detectada, texto_usr)

                for d in detecciones:
                    cx = int(d.get("x", 0))
                    cy = int(d.get("y", 0))
                    w = int(d.get("width", 0))
                    h = int(d.get("height", 0))
                    x0 = max(0, cx - w // 2)
                    y0 = max(0, cy - h // 2)
                    x1 = min(w_orig, cx + w // 2)
                    y1 = min(h_orig, cy + h // 2)
                    cv2.rectangle(img_dibujada, (x0, y0), (x1, y1), (0, 255, 0), 3)

                # Actualizar vista previa
                rgb = cv2.cvtColor(img_dibujada, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb).resize((480, 340))
                imgtk = ImageTk.PhotoImage(image=img)
                self.lbl_video.imgtk = imgtk
                self.lbl_video.configure(image=imgtk)

                # AUTO-SELECCIÓN: Si detecta una señal que no estaba seleccionada, la selecciona automáticamente
                elemento_detectado = info_sst["elemento"]
                actual_seleccion = self.combo_senal_esperada.get()
                auto_cambiado = False

                for valor_combo in self.combo_senal_esperada["values"]:
                    # Si coincide el nombre del elemento con el combo
                    if normalizar_texto(elemento_detectado) in normalizar_texto(valor_combo):
                        if actual_seleccion != valor_combo:
                            self.combo_senal_esperada.set(valor_combo)
                            auto_cambiado = True
                        break

                if auto_cambiado:
                    self.lbl_similitud.config(
                        text=f"🔄 ¡Detectado y Auto-Seleccionado!: '{elemento_detectado}'",
                        fg="#a6e3a1"
                    )
                else:
                    self.lbl_similitud.config(
                        text=f"🎯 ¡Coincidencia Confirmada: {elemento_detectado} (100%)!",
                        fg="#a6e3a1"
                    )

                # Actualizar tarjeta
                self.lbl_elem.config(text=f"Elemento: {info_sst['elemento']}")
                self.lbl_cat.config(text=f"Categoría: {info_sst['categoria']}", fg=info_sst['color'])
                self.lbl_cond.config(text=f"Condición Evaluada: {info_sst['condicion_default']}")
                self.lbl_desc.config(text=f"Descripción Normativa:\n{info_sst['descripcion']}")
                self.lbl_conf.config(text=f"Certeza IA: {int(conf * 100)}% (Detectado: {clase_detectada})")

                self.btn_validar.config(state="normal")
                self.btn_rechazar.config(state="normal")
                self.ultimo_hallazgo = info_sst
            else:
                # Si la IA no detectó en la imagen, sugerir basado en la selección del SST y texto
                texto_usr = f"{esperado_nombre} {self.txt_observacion.get()} {self.txt_ubicacion.get()}"
                info_sst = clasificar_con_catalogo("", texto_usr)
                
                self.lbl_similitud.config(
                    text="🔍 Señal no visualizada con suficiente certeza en la imagen.",
                    fg="#fab387"
                )
                self.lbl_elem.config(text=f"Elemento Esperado: {info_sst['elemento']}")
                self.lbl_cat.config(text=f"Categoría: {info_sst['categoria']}", fg=info_sst['color'])
                self.lbl_cond.config(text=f"Condición: {info_sst['condicion_default']}")
                self.lbl_desc.config(text=f"Descripción Normativa:\n{info_sst['descripcion']}")
                self.lbl_conf.config(text="Certeza IA: Sin detección visual clara (Validación asistida por inspector)")
                self.btn_validar.config(state="normal")
                self.btn_rechazar.config(state="normal")
                self.ultimo_hallazgo = info_sst
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la inferencia: {e}")
        finally:
            self.btn_analizar.config(text="⚡ Analizar con IA & Evaluar Similitud", state="normal")

    def validar_hallazgo(self):
        elem = self.ultimo_hallazgo.get("elemento", "Hallazgo")
        messagebox.showinfo("Validado", f"¡Hallazgo '{elem}' validado correctamente para el reporte de inspección!")
        self.btn_validar.config(state="disabled")
        self.btn_rechazar.config(state="disabled")

    def rechazar_hallazgo(self):
        messagebox.showwarning("Rechazado", "El hallazgo ha sido descartado de la inspección.")
        self.btn_validar.config(state="disabled")
        self.btn_rechazar.config(state="disabled")

    def cerrar(self):
        if self.cap.isOpened():
            self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AppInspeccionSST(root)
    root.protocol("WM_DELETE_WINDOW", app.cerrar)
    root.mainloop()
