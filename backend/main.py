# Script de preparación y entrenamiento para el Dataset de SST-IA
import os
try:
    from roboflow import Roboflow
    from ultralytics import YOLO
except ImportError:
    print("Por favor, instala las librerías corriendo en tu terminal:")
    print("pip install roboflow ultralytics")
    exit()

def descargar_datasets():
    print("=== Iniciando descarga de Datasets Base ===")
    # NOTA: Configura tu API Key de Roboflow en el archivo .env o como variable de entorno
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    api_key = os.environ.get("ROBOFLOW_API_KEY", "TU_API_KEY_AQUI")
    
    if not api_key or api_key == "TU_API_KEY_AQUI":
        print("⚠️ ADVERTENCIA: Debes configurar tu ROBOFLOW_API_KEY en .env o como variable de entorno.")
        return None

    rf = Roboflow(api_key=api_key)
    
    # Descargando el primer dataset que encontraste
    print("Descargando dataset 1...")
    project1 = rf.workspace("natwarins-workspace-2g6nk").project("signs-hhsr6")
    dataset1 = project1.version(1).download("yolov8") # Asegúrate de la versión

    print(f"Dataset descargado en: {dataset1.location}")
    return dataset1.location

def entrenar_yolo(data_yaml_path):
    print("=== Iniciando Entrenamiento de YOLOv8 ===")
    # Cargamos el modelo YOLOv8 'nano', que es el más rápido y ligero
    model = YOLO('yolov8n.pt') 
    
    # Iniciamos el entrenamiento (Fine-Tuning)
    # epochs=50 significa que repasará las imágenes 50 veces para aprender
    results = model.train(data=data_yaml_path, epochs=50, imgsz=640)
    print("¡Entrenamiento finalizado! El modelo optimizado está guardado como 'best.pt'")

def main():
    print("¡Bienvenido al sistema de entrenamiento SST-IA!")
    print("Clasificaciones a detectar: Advertencia (Amarillas), Evacuación (Verdes), Incendio (Rojas), Obligación (Azules), Prohibición (Rojas/Cruzadas).")
    print("-" * 50)
    
    # Paso 1: Descargar
    ruta_dataset = descargar_datasets()
    
    # Paso 2: Entrenar (Si el dataset se descargó correctamente)
    if ruta_dataset and os.path.exists(ruta_dataset):
        # El archivo data.yaml contiene las rutas a las imágenes y los nombres de las clases
        yaml_path = os.path.join(ruta_dataset, "data.yaml")
        entrenar_yolo(yaml_path)

if __name__ == "__main__":
    main()
