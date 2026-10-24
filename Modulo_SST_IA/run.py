"""
Lanzador Principal SST-IA.
Inicia el servidor backend en puerto 5000 y abre automáticamente el navegador
para que el profesional pueda realizar inspecciones de inmediato.

Uso:
  python run.py
"""
import sys
import time
import webbrowser
import threading
import uvicorn
from app.config import HOST, PORT

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def abrir_navegador():
    time.sleep(1.5)
    url = f"http://localhost:{PORT}"
    print(f"\n[OK] Abriendo SST-IA en el navegador: {url}")
    try:
        webbrowser.open(url)
    except Exception:
        print(f"Abre manualmente tu navegador en: {url}")

if __name__ == "__main__":
    print("\n" + "="*65)
    print("SISTEMA SST-IA: INSPECCION ASISTIDA POR INTELIGENCIA ARTIFICIAL")
    print("="*65)
    print(f"Servidor Local: http://localhost:{PORT}")
    print(f"API para Flutter: http://localhost:{PORT}/analizar")
    print(f"Swagger Docs: http://localhost:{PORT}/docs")
    print("="*65 + "\n")

    threading.Thread(target=abrir_navegador, daemon=True).start()
    uvicorn.run("server:app", host=HOST, port=PORT, log_level="info", reload=True)
