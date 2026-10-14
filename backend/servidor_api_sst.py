import os
import sys
import json
import base64
from http.server import HTTPServer, BaseHTTPRequestHandler

# Importar el motor multi-detector y clasificador
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from sst_multi_detector import detectar_todo
from inspeccion_sst_app import clasificar_con_catalogo, normalizar_texto

PUERTO = 5000

class HandlerAPI_SST(BaseHTTPRequestHandler):
    def _enviar_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self._enviar_cors()
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._enviar_cors()
        self.end_headers()
        respuesta = {
            "status": "online",
            "servicio": "SST-IA Backend (YOLO + Roboflow Datasets)",
            "mensaje": "Servidor listo para recibir fotos de la app Flutter."
        }
        self.wfile.write(json.dumps(respuesta, ensure_ascii=False).encode("utf-8"))

    def do_POST(self):
        if self.path == "/analizar":
            try:
                longitud = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(longitud).decode("utf-8")
                datos = json.loads(body)

                foto_b64 = datos.get("foto_base64", "")
                observacion = datos.get("observacion", "")
                ubicacion = datos.get("ubicacion", "")
                tipo = datos.get("tipo", "")

                if not foto_b64:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'{"error": "Falta foto_base64"}')
                    return

                # Decodificar imagen
                jpg_bytes = base64.b64decode(foto_b64)
                
                print(f"\n[PETICIÓN FLUTTER] Analizando evidencia...")
                print(f" -> Ubicación: {ubicacion} | Observación: {observacion} | Tipo: {tipo}")

                # Ejecutar motor de IA con los datasets
                detecciones = detectar_todo(jpg_bytes)

                clase_detectada = ""
                conf = 0.85
                if detecciones:
                    mejor = max(detecciones, key=lambda d: d.get("confidence", 0.0))
                    clase_detectada = mejor.get("class", mejor.get("label", ""))
                    conf = float(mejor.get("confidence", 0.85))
                    print(f" -> [IA DETECTADO]: '{clase_detectada}' ({int(conf * 100)}%)")
                else:
                    print(" -> [IA]: Sin detección visual directa, aplicando clasificación contextual.")

                # Mapear al catálogo normativo de 20 señales de SST
                texto_combinado = f"{tipo} {observacion} {ubicacion}"
                info_sst = clasificar_con_catalogo(clase_detectada, texto_combinado)

                # Formato exacto que espera la clase Hallazgo en Flutter
                resultado_flutter = {
                    "elemento": info_sst["elemento"],
                    "categoria": info_sst["categoria"],
                    "ubicacion": ubicacion if ubicacion else "Área inspeccionada",
                    "descripcion": info_sst["descripcion"],
                    "condicion": info_sst["condicion_default"],
                    "observacion": observacion,
                    "confianza": round(conf, 2),
                    "estado": "pendiente"
                }

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self._enviar_cors()
                self.end_headers()
                self.wfile.write(json.dumps(resultado_flutter, ensure_ascii=False).encode("utf-8"))
                print(f" -> [RESPUESTA ENVIADA]: {resultado_flutter['elemento']} ({resultado_flutter['categoria']})\n")

            except Exception as e:
                print(f"[ERROR]: {e}")
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self._enviar_cors()
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def iniciar_servidor():
    servidor = HTTPServer(("0.0.0.0", PUERTO), HandlerAPI_SST)
    print("=" * 65)
    print("🛡️  SERVIDOR API SST-IA ACTIVO PARA FLUTTER")
    print("=" * 65)
    print(f"• Escuchando en: http://localhost:{PUERTO}/analizar")
    print(f"• Para Emulador Android usa: http://10.0.2.2:{PUERTO}/analizar")
    print(f"• Conectado a todos los Workflows y Datasets de Roboflow")
    print("=" * 65)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
        servidor.server_close()

if __name__ == "__main__":
    iniciar_servidor()
