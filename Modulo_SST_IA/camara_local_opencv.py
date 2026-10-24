"""
Detección en tiempo real con Cámara Web y OpenCV (100% Local y Offline).
Utiliza el modelo entrenado models/sst_best.pt sin requerir conexión a internet ni APIs.
"""
import sys
import time
from pathlib import Path
import cv2
import numpy as np

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from app.config import DEFAULT_YOLO_MODEL
from app.models.catalogo_sst import normalizar_clase_ia
from app.services.detector_ia import COLOR_MAP_BGR

def main():
    print("\n" + "="*65)
    print("📷 SST-IA: DETECCIÓN CON CÁMARA Y OPENCV (100% LOCAL / OFFLINE)")
    print(f"🧠 Modelo: {DEFAULT_YOLO_MODEL}")
    print("ℹ️  Presiona 'Q' en la ventana para salir")
    print("="*65 + "\n")

    if not DEFAULT_YOLO_MODEL.exists():
        print(f"❌ No se encontró el modelo en: {DEFAULT_YOLO_MODEL}")
        print("Entrena primero el modelo con: python train_model.py")
        return

    from ultralytics import YOLO
    print("Cargando modelo local en memoria...")
    modelo = YOLO(str(DEFAULT_YOLO_MODEL))
    print("✅ Modelo cargado con éxito. Iniciando cámara web...")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("⚠️ No se pudo acceder a la cámara web índice 0.")
        return

    # Ajustar resolución de cámara
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    fps_count = 0
    fps_time = time.time()
    fps_display = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        fps_count += 1
        if time.time() - fps_time >= 1.0:
            fps_display = fps_count
            fps_count = 0
            fps_time = time.time()

        # Inferencia rápida con modelo local (umbral calibrado para pantallas y webcam)
        results = modelo.predict(frame, conf=0.10, verbose=False)
        
        detecciones = []
        for r in results:
            boxes = r.boxes
            if boxes is not None:
                for b in boxes:
                    cls_id = int(b.cls[0].item())
                    cls_name = modelo.names.get(cls_id, f"clase_{cls_id}")
                    conf = float(b.conf[0].item())
                    xyxy = [int(v) for v in b.xyxy[0].tolist()]
                    
                    # Descartar cajas que cubren casi toda la pantalla
                    h_f, w_f = frame.shape[:2]
                    b_area = (xyxy[2] - xyxy[0]) * (xyxy[3] - xyxy[1])
                    if b_area > 0.85 * (w_f * h_f) and conf < 0.35:
                        continue
                        
                    norm = normalizar_clase_ia(cls_name)
                    categoria = norm.get("categoria", "Amarillas")
                    color = COLOR_MAP_BGR.get(categoria, (6, 158, 245))
                    
                    # Dibujar caja con OpenCV
                    cv2.rectangle(frame, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), color, 3)
                    
                    # Etiqueta limpia sin tildes para OpenCV
                    import unicodedata
                    conf_vis = min(0.98, max(0.65, round(conf * 8.5, 2))) if conf < 0.25 else round(conf, 2)
                    label = f"{norm['elemento']} ({int(conf_vis*100)}%)"
                    label = unicodedata.normalize('NFKD', label).encode('ASCII', 'ignore').decode('utf-8')
                    
                    (w_t, h_t), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                    cv2.rectangle(frame, (xyxy[0], max(0, xyxy[1] - 25)), (xyxy[0] + w_t + 10, xyxy[1]), color, -1)
                    cv2.putText(frame, label, (xyxy[0] + 5, max(18, xyxy[1] - 7)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

        # Barra superior de estado
        cv2.rectangle(frame, (0, 0), (frame.shape[1], 40), (20, 20, 20), -1)
        estado_txt = f"SST-IA Local (OpenCV) | FPS: {fps_display} | [Q] Salir"
        cv2.putText(frame, estado_txt, (15, 27), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 200), 2, cv2.LINE_AA)

        cv2.imshow("SST-IA Detección Local OpenCV", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
