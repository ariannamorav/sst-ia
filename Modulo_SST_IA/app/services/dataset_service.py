"""
Servicio para recepción y procesamiento de cURLs de datasets (Roboflow / YOLO).
Descarga, descomprime, prepara las rutas y entrena modelos YOLOv8 locales.
"""
import os
import re
import shlex
import zipfile
import shutil
import threading
from pathlib import Path
from typing import Dict, Any, Optional
import requests

from app.config import DATASETS_DIR, MODELS_DIR, DEFAULT_YOLO_MODEL

class DatasetService:
    def __init__(self):
        self.estado_entrenamiento = {
            "en_progreso": False,
            "progreso": 0,
            "mensaje": "Listo",
            "ultimo_modelo": None,
            "error": None
        }

    def procesar_curl(self, curl_command: str, nombre_dataset: str = "dataset_sst") -> Dict[str, Any]:
        """
        Extrae la URL y cabeceras de un comando cURL de Roboflow o curl estándar,
        descarga el archivo ZIP del dataset y lo descomprime en data/datasets/<nombre_dataset>.
        """
        curl_command = curl_command.strip()
        
        # 1. Extraer URL con regex
        url_match = re.search(r'https?://[^\s\'"<>]+', curl_command)
        if not url_match:
            raise ValueError("No se pudo encontrar una URL válida en el comando cURL.")
            
        url = url_match.group(0)
        destino_dir = DATASETS_DIR / nombre_dataset
        destino_dir.mkdir(parents=True, exist_ok=True)
        zip_path = destino_dir / "dataset.zip"

        # 2. Descargar con requests
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        # Extraer cabeceras adicionales si vienen en el curl (-H "Header: Value")
        matches_h = re.findall(r'-H\s+[\'"]([^\'"]+)[\'"]', curl_command)
        for h in matches_h:
            if ":" in h:
                k, v = h.split(":", 1)
                headers[k.strip()] = v.strip()

        response = requests.get(url, headers=headers, stream=True, timeout=120)
        response.raise_for_status()

        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=65536):
                if chunk:
                    f.write(chunk)

        # 3. Descomprimir si es archivo ZIP
        es_zip = False
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(destino_dir)
                es_zip = True
        except zipfile.BadZipFile:
            pass

        # 4. Buscar data.yaml generado por Roboflow / YOLO
        archivos_yaml = list(destino_dir.rglob("data.yaml"))
        data_yaml_path = str(archivos_yaml[0]) if archivos_yaml else None

        # Corregir rutas relativas en data.yaml para que apunten a rutas absolutas
        if data_yaml_path:
            self._corregir_rutas_yaml(Path(data_yaml_path), destino_dir)

        return {
            "exito": True,
            "url_descargada": url,
            "directorio": str(destino_dir),
            "es_zip": es_zip,
            "data_yaml": data_yaml_path,
            "archivos_totales": len(list(destino_dir.rglob("*")))
        }

    def _corregir_rutas_yaml(self, yaml_file: Path, base_dataset_dir: Path):
        """Asegura que el campo 'path' en data.yaml apunte a la ruta absoluta correcta."""
        try:
            import yaml
            with open(yaml_file, "r", encoding="utf-8") as f:
                content = yaml.safe_load(f)
            if content and isinstance(content, dict):
                content["path"] = str(base_dataset_dir.resolve()).replace("\\", "/")
                with open(yaml_file, "w", encoding="utf-8") as f:
                    yaml.dump(content, f, sort_keys=False)
        except Exception:
            pass

    def entrenar_modelo_async(self, data_yaml_path: str, epochs: int = 25):
        """Lanza el entrenamiento de YOLOv8 en un hilo separado."""
        if self.estado_entrenamiento["en_progreso"]:
            return {"error": "Ya hay un entrenamiento en curso"}

        def _tarea_entrenamiento():
            self.estado_entrenamiento["en_progreso"] = True
            self.estado_entrenamiento["mensaje"] = "Inicializando YOLOv8..."
            self.estado_entrenamiento["error"] = None
            try:
                from ultralytics import YOLO
                from app.services.detector_ia import detector_ia_service
                
                modelo = YOLO("yolov8n.pt")
                self.estado_entrenamiento["mensaje"] = f"Entrenando por {epochs} épocas..."
                
                resultados = modelo.train(
                    data=data_yaml_path,
                    epochs=epochs,
                    imgsz=640,
                    project=str(DATASETS_DIR / "runs"),
                    name="sst_custom",
                    exist_ok=True,
                    verbose=True
                )
                
                # Copiar best.pt a models/sst_best.pt
                best_weights = DATASETS_DIR / "runs" / "sst_custom" / "weights" / "best.pt"
                if best_weights.exists():
                    shutil.copy(best_weights, DEFAULT_YOLO_MODEL)
                    detector_ia_service.recargar_modelo(str(DEFAULT_YOLO_MODEL))
                    self.estado_entrenamiento["ultimo_modelo"] = str(DEFAULT_YOLO_MODEL)
                    self.estado_entrenamiento["mensaje"] = "¡Entrenamiento completado y modelo activado!"
                else:
                    self.estado_entrenamiento["mensaje"] = "Entrenamiento finalizado."
                    
            except Exception as e:
                self.estado_entrenamiento["error"] = str(e)
                self.estado_entrenamiento["mensaje"] = f"Error en entrenamiento: {e}"
            finally:
                self.estado_entrenamiento["en_progreso"] = False

        hilo = threading.Thread(target=_tarea_entrenamiento, daemon=True)
        hilo.start()
        return {"mensaje": "Entrenamiento iniciado en segundo plano"}

dataset_service = DatasetService()
