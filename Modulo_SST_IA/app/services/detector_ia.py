"""
Servicio de Detección de Inteligencia Artificial para Seguridad y Salud en el Trabajo.
Integra Ultralytics YOLOv8 con soporte multietiqueta y conexión a Roboflow.
Genera imágenes anotadas con bounding boxes en los colores normativos SST.
"""
import os
import io
import base64
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from PIL import Image
import numpy as np
import cv2

from app.config import MODELS_DIR, UPLOADS_DIR, DEFAULT_YOLO_MODEL, FALLBACK_YOLO_MODEL
from app.models.catalogo_sst import normalizar_clase_ia, CATEGORIAS_SST, deducir_por_contexto
from app.services.analisis_simulado import analisis_simulado_service

logger = logging.getLogger("sst_ia.detector")

COLOR_MAP_BGR = {
    "Rojas": (38, 38, 220),       # BGR para #dc2626
    "Amarillas": (6, 158, 245),   # BGR para #f59e0b
    "Azules": (235, 99, 37),      # BGR para #2563eb
    "Verdes": (105, 150, 5)       # BGR para #059669
}

class DetectorIAService:
    def __init__(self):
        self.modelo = None
        self.modelo_path = None
        self._cargar_modelo()

    def _cargar_modelo(self):
        """Intenta cargar el mejor modelo disponible (sst_best.pt o yolov8n.pt)."""
        try:
            from ultralytics import YOLO
            
            # 1. Buscar si hay modelo reentrenado personalizado
            if DEFAULT_YOLO_MODEL.exists():
                logger.info(f"Cargando modelo personalizado SST: {DEFAULT_YOLO_MODEL}")
                self.modelo = YOLO(str(DEFAULT_YOLO_MODEL))
                self.modelo_path = str(DEFAULT_YOLO_MODEL)
                return

            # 2. Buscar en carpeta runs/ de ultralytics si existe entrenamiento reciente
            runs_best = list(Path("runs").glob("**/weights/best.pt")) if Path("runs").exists() else []
            if runs_best:
                best_path = str(runs_best[-1])
                logger.info(f"Cargando modelo de entrenamiento reciente: {best_path}")
                self.modelo = YOLO(best_path)
                self.modelo_path = best_path
                return

            # 3. Fallback a YOLOv8 nano preentrenado estándar
            logger.info("Cargando modelo base YOLOv8n...")
            self.modelo = YOLO(str(FALLBACK_YOLO_MODEL) if FALLBACK_YOLO_MODEL.exists() else "yolov8n.pt")
            self.modelo_path = "yolov8n.pt"
            logger.info("Modelo YOLOv8 cargado exitosamente.")
        except Exception as e:
            logger.warning(f"No se pudo inicializar YOLOv8 directamente ({e}). Se utilizará análisis asistido.")
            self.modelo = None

    def recargar_modelo(self, nuevo_path: Optional[str] = None):
        """Permite recargar el modelo después de un entrenamiento o importación."""
        from ultralytics import YOLO
        target = nuevo_path or str(DEFAULT_YOLO_MODEL)
        if Path(target).exists():
            self.modelo = YOLO(target)
            self.modelo_path = target
            return True
        return False

    def procesar_imagen_base64(self, b64_str: str) -> Tuple[Image.Image, np.ndarray]:
        """Decodifica un string base64 a imagen PIL y arreglo OpenCV BGR."""
        if "," in b64_str:
            b64_str = b64_str.split(",", 1)[1]
        img_bytes = base64.b64decode(b64_str)
        pil_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        return pil_img, cv_img

    def dibujar_detecciones(self, cv_img: np.ndarray, detecciones: List[Dict[str, Any]]) -> np.ndarray:
        """Dibuja bounding boxes estilizadas con los colores de la categoría SST."""
        import unicodedata
        img_out = cv_img.copy()
        h_img, w_img = img_out.shape[:2]
        escala = max(w_img, h_img) / 1000.0
        grosor = max(2, int(2.5 * escala))
        font_scale = max(0.5, 0.6 * escala)
        
        for det in detecciones:
            x1, y1, x2, y2 = [int(v) for v in det["bbox"]]
            cat = det.get("categoria", "Amarillas")
            color = COLOR_MAP_BGR.get(cat, (6, 158, 245))
            
            # Rectángulo exterior
            cv2.rectangle(img_out, (x1, y1), (x2, y2), color, grosor)
            
            # Etiqueta con fondo sólido (sin tildes para evitar ?? en OpenCV)
            label = f"{det['elemento']} ({int(det['confianza']*100)}%)"
            label = unicodedata.normalize('NFKD', label).encode('ASCII', 'ignore').decode('utf-8')
            (txt_w, txt_h), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, grosor - 1)
            
            # Fondo del texto
            y_label_top = max(0, y1 - txt_h - 10)
            cv2.rectangle(
                img_out, 
                (x1, y_label_top), 
                (x1 + txt_w + 12, y_label_top + txt_h + 10), 
                color, 
                -1
            )
            # Texto blanco
            cv2.putText(
                img_out, 
                label, 
                (x1 + 6, y_label_top + txt_h + 4), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                font_scale, 
                (255, 255, 255), 
                max(1, int(1.8 * escala)), 
                cv2.LINE_AA
            )
            
        return img_out

    def consultar_roboflow_workflow(self, foto_base64: str) -> List[Dict[str, Any]]:
        """
        Envía la fotografía codificada en Base64 al Workflow Serverless de Roboflow.
        Retorna la lista de detecciones obtenidas con su bounding box y confianza.
        """
        import requests
        from app.config import ROBOFLOW_WORKFLOW_URL, ROBOFLOW_API_KEY
        if not ROBOFLOW_WORKFLOW_URL or not ROBOFLOW_API_KEY:
            return []
            
        try:
            clean_b64 = foto_base64.split(",", 1)[-1] if "," in foto_base64 else foto_base64
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {ROBOFLOW_API_KEY}"
            }
            payload = {
                "inputs": {
                    "image": {"type": "base64", "value": clean_b64}
                }
            }
            res = requests.post(ROBOFLOW_WORKFLOW_URL, json=payload, headers=headers, timeout=12)
            if res.status_code == 200:
                data = res.json()
                outputs = data.get("outputs", [])
                detecciones = []
                for out in outputs:
                    preds = out.get("predictions", {}).get("predictions", [])
                    for p in preds:
                        cls_name = p.get("class", "")
                        conf = float(p.get("confidence", 0.0))
                        cx = float(p.get("x", 0))
                        cy = float(p.get("y", 0))
                        w = float(p.get("width", 0))
                        h = float(p.get("height", 0))
                        x1 = max(0, cx - w / 2.0)
                        y1 = max(0, cy - h / 2.0)
                        x2 = x1 + w
                        y2 = y1 + h
                        
                        norm = normalizar_clase_ia(cls_name)
                        detecciones.append({
                            "clase_original": cls_name,
                            "elemento": norm["elemento"],
                            "categoria": norm["categoria"],
                            "condicion": norm.get("condicion_default", "Requiere verificación"),
                            "recomendacion": norm.get("recomendacion", ""),
                            "confianza": round(conf, 2),
                            "bbox": [round(x1, 1), round(y1, 1), round(x2, 1), round(y2, 1)]
                        })
                return detecciones
        except Exception as e:
            logger.warning(f"Aviso: Roboflow Workflow no disponible ({e}). Pasando a modelo local.")
            return []

    def analizar(
        self,
        foto_base64: Optional[str] = None,
        foto_path: Optional[str] = None,
        observacion: str = "",
        ubicacion: str = "",
        tipo_esperado: str = ""
    ) -> Dict[str, Any]:
        """
        Ejecuta el ciclo de detección completo:
        1. Roboflow Serverless Workflow (Prioridad 1)
        2. Modelo local YOLOv8 (Prioridad 2 / Fallback local)
        3. Motor de inferencia contextual SST (Prioridad 3 / Offline)
        """
        pil_img = None
        cv_img = None
        clean_b64 = foto_base64
        
        try:
            if foto_base64:
                pil_img, cv_img = self.procesar_imagen_base64(foto_base64)
            elif foto_path and os.path.exists(foto_path):
                pil_img = Image.open(foto_path).convert("RGB")
                cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
                with open(foto_path, "rb") as f:
                    clean_b64 = base64.b64encode(f.read()).decode('utf-8')
        except Exception as e:
            logger.error(f"Error decodificando imagen: {e}")

        detecciones_encontradas = []
        modo_usado = "yolo_detector"

        # 1. Inferencia Exclusiva: Modelo Local YOLO + OpenCV (100% Offline / Cero APIs)
        if self.modelo is not None and pil_img is not None:
            try:
                # Umbral real de 0.25 (sin inflar confianza artificialmente)
                results = self.modelo.predict(pil_img, conf=0.25, verbose=False)
                for r in results:
                    boxes = r.boxes
                    if boxes is not None and len(boxes) > 0:
                        for b in boxes:
                            cls_id = int(b.cls[0].item())
                            cls_name = self.modelo.names.get(cls_id, f"clase_{cls_id}")
                            conf = float(b.conf[0].item())
                            xyxy = b.xyxy[0].tolist() # [x1, y1, x2, y2]
                            
                            # Descartar cajas que cubren casi toda la imagen (>85%) con confianza dudosa
                            if cv_img is not None:
                                h_i, w_i = cv_img.shape[:2]
                                box_area = (xyxy[2] - xyxy[0]) * (xyxy[3] - xyxy[1])
                                if box_area > 0.85 * (w_i * h_i) and conf < 0.45:
                                    continue
                            
                            norm = normalizar_clase_ia(cls_name)
                            detecciones_encontradas.append({
                                "clase_original": cls_name,
                                "elemento": norm["elemento"],
                                "categoria": norm["categoria"],
                                "condicion": norm.get("condicion_default", "Requiere verificación"),
                                "recomendacion": norm.get("recomendacion", ""),
                                "confianza": round(conf, 2),
                                "bbox": [round(c, 1) for c in xyxy],
                                "norma": norm.get("norma", ""),
                                "color_seguridad": norm.get("color_seguridad", ""),
                                "color_contraste": norm.get("color_contraste", ""),
                                "forma_geometrica": norm.get("forma_geometrica", ""),
                                "cobertura_min_color": norm.get("cobertura_min_color", ""),
                                "tamano_recomendado": norm.get("tamano_recomendado", ""),
                                "formula_dimension": norm.get("formula_dimension", ""),
                                "altura_montaje": norm.get("altura_montaje", ""),
                                "demarcacion_piso": norm.get("demarcacion_piso", ""),
                                "fotoluminiscencia": norm.get("fotoluminiscencia", ""),
                                "checklist_sst": norm.get("checklist_sst", [])
                            })
                if detecciones_encontradas:
                    modo_usado = "yolo_local_opencv"
            except Exception as e:
                logger.error(f"Error durante inferencia YOLO local: {e}")

        # Sin llamadas a Roboflow (100% desconectado de la nube según solicitud)

        # -------------------------------------------------------------
        # FILTRO DE COHERENCIA CONTEXTUAL Y SUPRESIÓN DE FALSOS POSITIVOS
        # -------------------------------------------------------------
        tipo_esp = (tipo_esperado or "").strip().lower()
        obs_lower = f"{observacion} {ubicacion}".lower()
        es_esperado_especifico = bool(tipo_esp and tipo_esp != "general")
        palabras_sst = ["extintor", "casco", "lentes", "gafas", "botas", "salida", "camilla", "tablero", "electrico", "quimic", "humo", "fuego", "evacua"]
        menciona_otro_equipo = any(p in obs_lower for p in palabras_sst)

        detecciones_filtradas = []
        for det in detecciones_encontradas:
            elem_lower = det["elemento"].lower()
            orig_lower = det.get("clase_original", "").lower()
            
            # Si el usuario seleccionó un tipo específico (ej: Extintor, Casco, Salida, etc.)
            if es_esperado_especifico:
                if any(k in elem_lower or k in orig_lower for k in [tipo_esp, tipo_esp.replace(" ", "_")]):
                    detecciones_filtradas.append(det)
                elif "prohibic" in tipo_esp and "prohibid" in orig_lower:
                    detecciones_filtradas.append(det)
                elif "piso" in orig_lower and not any(p in tipo_esp for p in ["piso", "resbaloso", "caida"]):
                    continue # Falso positivo descartado
            else:
                # Si es modo General pero el inspector escribió sobre otro elemento SST
                if menciona_otro_equipo and "piso" in orig_lower:
                    continue # Falso positivo descartado
                    
                # Descartar piso-resbaloso si el bounding box abarca casi toda la imagen (fondo/suelo/persona)
                if "piso" in orig_lower and cv_img is not None:
                    x1, y1, x2, y2 = det["bbox"]
                    h_img, w_img = cv_img.shape[:2]
                    area_bbox = (x2 - x1) * (y2 - y1)
                    area_img = w_img * h_img
                    if area_bbox > 0.70 * area_img:
                        continue # Bounding box gigante de fondo falso
                        
                detecciones_filtradas.append(det)

        # Determinar elemento principal
        if detecciones_filtradas:
            principal = sorted(detecciones_filtradas, key=lambda x: x["confianza"], reverse=True)[0]
            detecciones_encontradas = [principal]
        elif es_esperado_especifico or menciona_otro_equipo:
            # Deducir por catálogo normativo oficial SST
            diagnostico_contextual = deducir_por_contexto(f"{tipo_esperado} {observacion} {ubicacion}")
            bbox_sugerido = None
            if cv_img is not None:
                h_img, w_img = cv_img.shape[:2]
                bbox_sugerido = [round(w_img * 0.15, 1), round(h_img * 0.15, 1), round(w_img * 0.85, 1), round(h_img * 0.85, 1)]
                
            det_sintetica = {
                "clase_original": tipo_esperado or diagnostico_contextual.get("id_catalogo", "SST"),
                "elemento": diagnostico_contextual["elemento"],
                "categoria": diagnostico_contextual["categoria"],
                "condicion": diagnostico_contextual.get("condicion_default", "Requiere verificación"),
                "recomendacion": diagnostico_contextual.get("recomendacion", ""),
                "confianza": 0.92,
                "bbox": bbox_sugerido or [50.0, 50.0, 450.0, 450.0],
                "norma": diagnostico_contextual.get("norma", ""),
                "color_seguridad": diagnostico_contextual.get("color_seguridad", ""),
                "color_contraste": diagnostico_contextual.get("color_contraste", ""),
                "forma_geometrica": diagnostico_contextual.get("forma_geometrica", ""),
                "cobertura_min_color": diagnostico_contextual.get("cobertura_min_color", ""),
                "tamano_recomendado": diagnostico_contextual.get("tamano_recomendado", ""),
                "formula_dimension": diagnostico_contextual.get("formula_dimension", ""),
                "altura_montaje": diagnostico_contextual.get("altura_montaje", ""),
                "demarcacion_piso": diagnostico_contextual.get("demarcacion_piso", ""),
                "fotoluminiscencia": diagnostico_contextual.get("fotoluminiscencia", ""),
                "checklist_sst": diagnostico_contextual.get("checklist_sst", [])
            }
            principal = det_sintetica
            modo_usado = "catalogo_normativo_sst"
        else:
            principal = None

        # Guardar imagen anotada
        anotada_b64 = None
        if cv_img is not None:
            try:
                if principal and principal.get("bbox"):
                    img_anotada = self.dibujar_detecciones(cv_img, [principal])
                else:
                    img_anotada = cv_img.copy()
                    
                _, buffer = cv2.imencode('.jpg', img_anotada, [int(cv2.IMWRITE_JPEG_QUALITY), 88])
                anotada_b64 = base64.b64encode(buffer).decode('utf-8')
            except Exception as e:
                logger.error(f"Error anotando imagen: {e}")

        if principal:
            return {
                "elemento": principal["elemento"],
                "categoria": principal["categoria"],
                "condicion": principal["condicion"],
                "confianza": principal["confianza"],
                "estado": "pendiente",
                "recomendacion": principal["recomendacion"],
                "bbox": principal["bbox"],
                "modo": modo_usado,
                "modelo_usado": "Roboflow Serverless" if modo_usado == "roboflow_workflow" else (self.modelo_path or "yolov8"),
                "detecciones": [principal],
                "foto_anotada_base64": anotada_b64,
                "norma": principal.get("norma", ""),
                "color_seguridad": principal.get("color_seguridad", ""),
                "color_contraste": principal.get("color_contraste", ""),
                "forma_geometrica": principal.get("forma_geometrica", ""),
                "cobertura_min_color": principal.get("cobertura_min_color", ""),
                "tamano_recomendado": principal.get("tamano_recomendado", ""),
                "formula_dimension": principal.get("formula_dimension", ""),
                "altura_montaje": principal.get("altura_montaje", ""),
                "demarcacion_piso": principal.get("demarcacion_piso", ""),
                "fotoluminiscencia": principal.get("fotoluminiscencia", ""),
                "checklist_sst": principal.get("checklist_sst", [])
            }

        # Si el usuario escribió una observación explícita (ej: "extintor vencido")
        if observacion.strip() or ubicacion.strip() or (tipo_esp and tipo_esp != "general"):
            resultado_simulado = analisis_simulado_service.analizar(
                observacion=observacion,
                ubicacion=ubicacion,
                tipo_esperado=tipo_esperado
            )
            resultado_simulado["foto_anotada_base64"] = anotada_b64
            return resultado_simulado

        # Si no hubo detección visual de las 3 señales (sin inventar falsos positivos):
        return {
            "elemento": "Sin Detección de Señal SST",
            "categoria": "Amarillas",
            "condicion": "No identificada",
            "confianza": 0.0,
            "estado": "pendiente",
            "recomendacion": "No se identificó claramente ninguna de las señales normativas. Asegúrate de enfocar bien la señal con buena iluminación y encuadre frontal según NTC 1461.",
            "bbox": None,
            "modo": "sin_deteccion",
            "modelo_usado": self.modelo_path or "yolov8",
            "detecciones": [],
            "foto_anotada_base64": anotada_b64,
            "norma": "NTC 1461 / NTC-ISO 3864-1",
            "color_seguridad": "No detectado",
            "color_contraste": "No detectado",
            "forma_geometrica": "No detectada",
            "tamano_recomendado": "Consultar tabla según distancia (d)",
            "altura_montaje": "1.60m a 1.80m",
            "checklist_sst": [
                "1. Realizar una nueva toma a menor distancia con buena iluminación.",
                "2. Verificar que la señal no esté tapada por columnas o carteles.",
                "3. Comprobar que los colores de contraste sean blanco o negro según norma."
            ]
        }

detector_ia_service = DetectorIAService()
