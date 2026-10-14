import os
import sys
import json
from sst_multi_detector import detectar_todo, WORKFLOWS, DIRECT_MODELS

def probar_detector(imagen_ruta_o_url):
    print("=" * 65)
    print("SST-IA: Probador Multi-Dataset Roboflow")
    print("=" * 65)
    print(f"Probando {len(WORKFLOWS)} Workflows y {len(DIRECT_MODELS)} Modelos Integrados:")
    for w in WORKFLOWS:
        print(f" • [Workflow] {w['id']} ({w['desc']}) -> Clases: {w['classes']}")
    for m in DIRECT_MODELS:
        print(f" • [Modelo]   {m['id']} ({m['desc']})")
    print("-" * 65)
    print(f"Analizando imagen: {imagen_ruta_o_url} ...")
    
    resultados = detectar_todo(imagen_ruta_o_url)
    
    print("\n" + "=" * 65)
    print(f"¡Detección completada! Total de objetos encontrados: {len(resultados)}")
    print("=" * 65)
    
    if resultados:
        for idx, det in enumerate(resultados, 1):
            clase = det.get("class", det.get("label", "Objeto"))
            conf = det.get("confidence", 0.0)
            fuente = det.get("source", "Roboflow")
            print(f"{idx}. {clase.upper()} | Confianza: {int(conf * 100)}% | Origen: {fuente}")
    else:
        print("No se encontraron detecciones para esta imagen (prueba con otra o revisa los umbrales).")

if __name__ == "__main__":
    # URL de prueba por defecto
    url_ejemplo = "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=640&q=80"
    
    if len(sys.argv) > 1:
        probar_detector(sys.argv[1])
    else:
        probar_detector(url_ejemplo)
