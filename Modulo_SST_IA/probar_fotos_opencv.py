"""
Script para probar imágenes con OpenCV y el modelo local (100% Offline).
Toma imágenes de las carpetas locales, detecta las señales y guarda las fotos anotadas.
"""
import sys
from pathlib import Path
import cv2

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from app.config import DEFAULT_YOLO_MODEL, BASE_DIR
from app.models.catalogo_sst import normalizar_clase_ia
from app.services.detector_ia import COLOR_MAP_BGR

def probar_carpetas(carpetas: list, conf: float = 0.15):
    from ultralytics import YOLO

    if not DEFAULT_YOLO_MODEL.exists():
        print(f"❌ No se encontró el modelo en: {DEFAULT_YOLO_MODEL}")
        return

    print(f"🧠 Cargando modelo local: {DEFAULT_YOLO_MODEL}")
    modelo = YOLO(str(DEFAULT_YOLO_MODEL))

    output_dir = BASE_DIR / "data" / "resultados_opencv"
    output_dir.mkdir(parents=True, exist_ok=True)

    total_detectadas = 0
    total_imagenes = 0

    for carpeta in carpetas:
        p_carpeta = Path(carpeta)
        if not p_carpeta.exists():
            print(f"⚠️ Carpeta no encontrada: {carpeta}")
            continue

        archivos = list(p_carpeta.glob("*.jpg")) + list(p_carpeta.glob("*.png"))
        print(f"\n📂 Analizando {len(archivos)} imágenes en: {p_carpeta.name}")

        for img_path in archivos:
            total_imagenes += 1
            frame = cv2.imread(str(img_path))
            if frame is None:
                continue

            results = modelo.predict(frame, conf=conf, verbose=False)
            hubo_deteccion = False

            for r in results:
                boxes = r.boxes
                if boxes is not None and len(boxes) > 0:
                    hubo_deteccion = True
                    total_detectadas += 1
                    for b in boxes:
                        cls_id = int(b.cls[0].item())
                        cls_name = modelo.names.get(cls_id, f"clase_{cls_id}")
                        conf_val = float(b.conf[0].item())
                        xyxy = [int(v) for v in b.xyxy[0].tolist()]

                        norm = normalizar_clase_ia(cls_name)
                        color = COLOR_MAP_BGR.get(norm.get("categoria", "Amarillas"), (6, 158, 245))

                        # Dibujar caja y etiqueta con OpenCV
                        cv2.rectangle(frame, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), color, 3)
                        import unicodedata
                        txt = f"{norm['elemento']} ({int(conf_val*100)}%)"
                        txt = unicodedata.normalize('NFKD', txt).encode('ASCII', 'ignore').decode('utf-8')
                        (tw, th), _ = cv2.getTextSize(txt, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                        cv2.rectangle(frame, (xyxy[0], max(0, xyxy[1] - 25)), (xyxy[0] + tw + 10, xyxy[1]), color, -1)
                        cv2.putText(frame, txt, (xyxy[0] + 5, max(18, xyxy[1] - 7)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

            if hubo_deteccion:
                out_path = output_dir / f"det_{p_carpeta.name}_{img_path.name}"
                cv2.imwrite(str(out_path), frame)

    print("\n" + "="*60)
    print(f"✅ ANÁLISIS COMPLETADO (100% LOCAL / OPENCV)")
    print(f"Total imágenes analizadas: {total_imagenes}")
    print(f"Total detecciones guardadas: {total_detectadas}")
    print(f"Imágenes con recuadros guardadas en: {output_dir}")
    print("="*60)

if __name__ == "__main__":
    carpetas_usuario = [
        r"C:\Users\Yairc\Downloads\piso-resbaloso",
        r"C:\Users\Yairc\Downloads\prohibido-celular",
        r"C:\Users\Yairc\Downloads\prohibido-comer",
        r"C:\Users\Yairc\Downloads\extintor",
        r"C:\Users\Yairc\Downloads\gabinete-incendio",
        r"C:\Users\Yairc\Downloads\ruta-evacuacion",
        r"C:\Users\Yairc\Downloads\punto-encuentro",
        r"C:\Users\Yairc\Downloads\prohibido-fumar"
    ]
    confianza = float(sys.argv[1]) if len(sys.argv) > 1 else 0.10
    probar_carpetas(carpetas_usuario, conf=confianza)
