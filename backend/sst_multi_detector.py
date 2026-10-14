import os
import sys
import base64
import requests
import json
from concurrent.futures import ThreadPoolExecutor
# Cargar variables de entorno si existe .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

API_KEY = os.environ.get("ROBOFLOW_API_KEY", "wFNVbgBUcGbkOi1gz6iJ")
WORKSPACE = os.environ.get("ROBOFLOW_WORKSPACE", "yair-cordoba")

# Lista completa de Workflows configurados en Roboflow
# Lista completa de Workflows de Roboflow organizada por categoría de SST
WORKFLOWS = [
    # Evacuación y Emergencia (Verdes)
    {
        "id": "general-segmentation-api-3",
        "classes": "Stretcher",
        "desc": "Camilla de Emergencia",
        "categoria": "evacuacion"
    },
    {
        "id": "general-segmentation-api-6",
        "classes": "0, assembly point sign, down arrow sign, Emergency exit sign, entrance sign",
        "desc": "Punto de Encuentro y Salida",
        "categoria": "evacuacion"
    },
    {
        "id": "general-segmentation-api",
        "classes": "Door, Emergency-Exit",
        "desc": "Puertas y Salidas de Emergencia",
        "categoria": "evacuacion"
    },
    # Equipos Contra Incendio (Rojas)
    {
        "id": "general-segmentation-api-2",
        "classes": "Angle value 2.5, F-Wrench, F-Wrench-DIY, Fire hose 1.5, Fire hose 1.5 Red",
        "desc": "Mangueras y Válvulas de Incendio",
        "categoria": "incendio"
    },
    {
        "id": "senalizacion-de-seguridad-del-ed",
        "classes": "señal de salida de emergencia, señal de extintor, señal de alarma contra incendios, señal de manguera contra incendios",
        "desc": "Señalización Base de Incendio y Evacuación",
        "categoria": "incendio"
    },
    # Advertencia de Peligro (Amarillas)
    {
        "id": "general-segmentation-api-7",
        "classes": "Parking, Grocery, Caution, Diaper Changing Station, Elevator",
        "desc": "Precaución y Avisos Generales",
        "categoria": "advertencia"
    },
    # Prohibición (Rojas con diagonal)
    {
        "id": "general-segmentation-api-8",
        "classes": "female washroom, male washroom, no smoking",
        "desc": "Prohibido Fumar y Avisos",
        "categoria": "prohibicion"
    }
]

# Modelos directos de Roboflow Inference
DIRECT_MODELS = [
    {
        "id": "hazard-detection-cfp1a/1",
        "desc": "Detección de Peligros / Riesgos Químicos y Físicos",
        "categoria": "advertencia"
    },
    {
        "id": "my-first-project-icfhw/2",
        "desc": "Señales y Objetos SST Base",
        "categoria": "general"
    }
]

def _preparar_base64_o_url(imagen_input):
    """Convierte archivo local o bytes en base64, o devuelve URL directa"""
    if isinstance(imagen_input, str):
        if imagen_input.startswith("http://") or imagen_input.startswith("https://"):
            return {"type": "url", "value": imagen_input}
        
        path_candidato = os.path.normpath(imagen_input)
        if not os.path.isabs(path_candidato):
            # Probar relativo al CWD o relativo al archivo
            if not os.path.exists(path_candidato):
                alt_path = os.path.join(os.path.dirname(__file__), "..", path_candidato)
                if os.path.exists(alt_path):
                    path_candidato = alt_path

        if os.path.exists(path_candidato):
            with open(path_candidato, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
                return {"type": "base64", "value": b64}
    elif isinstance(imagen_input, bytes):
        b64 = base64.b64encode(imagen_input).decode("utf-8")
        return {"type": "base64", "value": b64}
    
    return None

WORKFLOW_CONFIDENCE = 0.30  # Sensibilidad natural para detectar alarmas, camillas y extintores
NOISY_MODEL_CONFIDENCE = 0.65  # Umbral alto para modelos con riesgo de falsos positivos (paredes, cables)

def _consultar_workflow(wf, img_payload, timeout=6):
    """Consulta un workflow individual en Roboflow Serverless"""
    url = f"https://serverless.roboflow.com/{WORKSPACE}/workflows/{wf['id']}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    inputs_dict = {
        "image": img_payload,
        "confidence": WORKFLOW_CONFIDENCE,
        "iou_threshold": 0.35,
        "max_detections": 30
    }
    # Si el workflow define clases y no es el base, se agregan
    if wf.get("classes") and wf["id"] != "senalizacion-de-seguridad-del-ed":
        inputs_dict["classes"] = wf["classes"]

    payload = {"inputs": inputs_dict}
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=timeout)
        if res.status_code == 200:
            data = res.json()
            outputs = data.get("outputs", [])
            preds = []
            if outputs:
                p = outputs[0].get("predictions", {})
                if isinstance(p, dict):
                    preds = p.get("predictions", [])
                elif isinstance(p, list):
                    preds = p
            
            # Filtrar y etiquetar
            filtradas = []
            for item in preds:
                if item.get("confidence", 0.0) >= WORKFLOW_CONFIDENCE:
                    item["source"] = f"Workflow: {wf['desc']}"
                    filtradas.append(item)
            return filtradas
    except Exception:
        pass
    return []

def _consultar_modelo_directo(m, img_payload, timeout=6):
    """Consulta un modelo directo de Roboflow Inference API con umbral seguro"""
    conf = NOISY_MODEL_CONFIDENCE if "my-first-project" in m["id"] else WORKFLOW_CONFIDENCE
    url = f"https://serverless.roboflow.com/{m['id']}?api_key={API_KEY}&confidence={conf}&overlap=35"
    try:
        if img_payload["type"] == "base64":
            res = requests.post(
                url, 
                data=img_payload["value"], 
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=timeout
            )
        else:
            url_with_img = f"{url}&image={img_payload['value']}"
            res = requests.post(url_with_img, timeout=timeout)

        if res.status_code == 200:
            data = res.json()
            preds = data.get("predictions", [])
            filtradas = []
            for item in preds:
                if item.get("confidence", 0.0) >= conf:
                    item["source"] = f"Modelo: {m['desc']}"
                    filtradas.append(item)
            return filtradas
    except Exception:
        pass
    return []

def detectar_todo(imagen_input, categoria_filtro=None, max_workers=6):
    """
    Ejecuta los workflows y modelos pertinentes de forma concurrente en paralelo.
    Si se especifica categoria_filtro ('evacuacion', 'incendio', 'advertencia', 'prohibicion', 'obligacion'),
    solo consulta los modelos asociados a esa categoría, eliminando confusiones cruzadas.
    """
    img_payload = _preparar_base64_o_url(imagen_input)
    if not img_payload:
        print("[ERROR] Formato de imagen no válido o archivo no encontrado.")
        return []

    # Si el usuario eligió una categoría específica, solo corremos los modelos correspondientes
    wfs_a_consultar = WORKFLOWS
    modelos_a_consultar = DIRECT_MODELS

    if categoria_filtro and categoria_filtro != "todas":
        wfs_filtrados = [w for w in WORKFLOWS if w.get("categoria") == categoria_filtro]
        md_filtrados = [m for m in DIRECT_MODELS if m.get("categoria") == categoria_filtro]
        if wfs_filtrados or md_filtrados:
            wfs_a_consultar = wfs_filtrados
            modelos_a_consultar = md_filtrados

    todas_las_detecciones = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futuros_wf = [executor.submit(_consultar_workflow, wf, img_payload) for wf in wfs_a_consultar]
        futuros_md = [executor.submit(_consultar_modelo_directo, m, img_payload) for m in modelos_a_consultar]
        
        for f in futuros_wf:
            todas_las_detecciones.extend(f.result())
        for f in futuros_md:
            todas_las_detecciones.extend(f.result())

    return todas_las_detecciones

def probar_detector(imagen_ruta_o_url):
    print("=" * 65)
    print("Iniciando Detección Multi-Modelo SST-IA (Todos los Datasets)")
    print("=" * 65)
    print(f"Consultando {len(WORKFLOWS)} Workflows y {len(DIRECT_MODELS)} Modelos en simultáneo...")
    
    resultados = detectar_todo(imagen_ruta_o_url)
    print(f"\n[RESULTADOS] Total de objetos detectados: {len(resultados)}")
    print("-" * 65)
    
    for idx, d in enumerate(resultados, 1):
        clase = d.get("class", d.get("label", "Desconocido"))
        conf = d.get("confidence", 0.0)
        fuente = d.get("source", "Roboflow")
        print(f"{idx}. [{clase.upper()}] - Confianza: {int(conf * 100)}% | Origen: {fuente}")
        
    return resultados

if __name__ == "__main__":
    url_test = "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=640&q=80"
    if len(sys.argv) > 1:
        probar_detector(sys.argv[1])
    else:
        probar_detector(url_test)
