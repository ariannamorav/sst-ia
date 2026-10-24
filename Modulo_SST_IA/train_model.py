"""
Script para entrenar o afinar YOLOv8 con los datasets de señales SST.
Guarda los mejores pesos en models/sst_best.pt y actualiza el detector en caliente.

Uso:
  python train_model.py
  python train_model.py --epochs 30 --imgsz 640
"""
import sys
import shutil
import argparse
from pathlib import Path

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from app.config import DATASETS_DIR, MODELS_DIR, DEFAULT_YOLO_MODEL

def main():
    parser = argparse.ArgumentParser(description="Entrena un modelo YOLOv8 para SST-IA")
    parser.add_argument("--yaml", type=str, help="Ruta al archivo data.yaml del dataset")
    parser.add_argument("--epochs", type=int, default=25, help="Número de épocas de entrenamiento (default: 25)")
    parser.add_argument("--imgsz", type=int, default=640, help="Tamaño de imagen (default: 640)")
    parser.add_argument("--model", type=str, default="yolov8n.pt", help="Modelo base (yolov8n.pt, yolov8s.pt)")
    args = parser.parse_args()

    # Buscar data.yaml si no se especifica
    yaml_path = args.yaml
    if not yaml_path:
        candidatos = list(DATASETS_DIR.rglob("data.yaml"))
        if not candidatos:
            print("❌ No se encontró ningún archivo 'data.yaml' en data/datasets/")
            print("Descarga primero un dataset con: python dataset_manager.py")
            return
        yaml_path = str(candidatos[0])
        print(f"🔍 Usando dataset detectado automáticamente: {yaml_path}")

    print("\n" + "="*60)
    print("🔥 INICIANDO ENTRENAMIENTO DE MODELO SST-IA (YOLOv8)")
    print(f"📊 Dataset: {yaml_path}")
    print(f"⚡ Épocas: {args.epochs} | Tamaño de Imagen: {args.imgsz}")
    print(f"🎯 Modelo Base: {args.model}")
    print("="*60 + "\n")

    # Asegurar que el path en data.yaml sea dinámico y funcione en cualquier ubicación
    try:
        import yaml
        yaml_file = Path(yaml_path).resolve()
        if yaml_file.exists():
            with open(yaml_file, "r", encoding="utf-8") as f:
                ydata = yaml.safe_load(f)
            parent_posix = yaml_file.parent.as_posix()
            if ydata and ydata.get("path") != parent_posix:
                ydata["path"] = parent_posix
                with open(yaml_file, "w", encoding="utf-8") as f:
                    yaml.dump(ydata, f, sort_keys=False, default_flow_style=False)
                print(f"🔄 Ruta del dataset verificada y adaptada: {parent_posix}")
    except Exception as e:
        print(f"Nota: Validación dinámica de data.yaml: {e}")

    try:
        from ultralytics import YOLO
        model = YOLO(args.model)
        
        results = model.train(
            data=yaml_path,
            epochs=args.epochs,
            imgsz=args.imgsz,
            cls=2.0,          # Penalización 4x más fuerte para evitar confundir pictograma de celular con comida
            close_mosaic=10,  # Desactivar cortes de mosaico en las últimas 10 épocas para ver el pictograma completo
            degrees=10.0,     # Leve rotación para tolerar ángulos de cámara
            scale=0.25,       # Variaciones de escala
            project=str(DATASETS_DIR / "runs"),
            name="sst_custom",
            exist_ok=True,
            verbose=True
        )

        best_weights = DATASETS_DIR / "runs" / "sst_custom" / "weights" / "best.pt"
        if best_weights.exists():
            shutil.copy(best_weights, DEFAULT_YOLO_MODEL)
            print("\n" + "="*60)
            print("🎉 ¡ENTRENAMIENTO COMPLETADO CON ÉXITO!")
            print(f"💾 Nuevo modelo guardado en: {DEFAULT_YOLO_MODEL}")
            print("El detector en el servidor y la app ahora usarán este nuevo modelo entrenado.")
            print("="*60)
        else:
            print("⚠️ Entrenamiento terminado pero no se generó el archivo weights/best.pt.")

    except Exception as e:
        print(f"\n❌ Error durante el entrenamiento: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
