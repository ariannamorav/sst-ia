import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import cv2
import requests
import json
import base64
import threading
import time

# Cargar variables de entorno si existe .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

_API_KEY_RAW = os.environ.get("ROBOFLOW_API_KEY", "wFNVbgBUcGbkOi1gz6iJ")
API_KEY = f"Bearer {_API_KEY_RAW}" if not _API_KEY_RAW.startswith("Bearer ") else _API_KEY_RAW
_WORKSPACE = os.environ.get("ROBOFLOW_WORKSPACE", "yair-cordoba")
WORKFLOW_URL = f"https://serverless.roboflow.com/{_WORKSPACE}/workflows/senalizacion-de-seguridad-del-ed"

class CamaraEnTiempoReal:
    def __init__(self, root):
        self.root = root
        self.root.title("SST-IA - Detección Automática en Tiempo Real")
        self.root.geometry("850x700")
        self.root.configure(bg="#181825")

        self.current_frame = None
        self.ultimas_detecciones = []
        self.procesando = False
        self.auto_detect = True  # Activado por defecto para detectar de una

        # Título
        self.lbl_titulo = tk.Label(
            root, 
            text="SST-IA: Detección Automática de Señales", 
            font=("Arial", 16, "bold"), 
            fg="#cdd6f4", 
            bg="#181825"
        )
        self.lbl_titulo.pack(pady=8)

        # Contenedor del Video
        self.lbl_video = tk.Label(root, bg="#11111b")
        self.lbl_video.pack(padx=10, pady=5)

        # Panel de Estado y Resultados
        self.frame_info = tk.Frame(root, bg="#181825")
        self.frame_info.pack(fill="x", padx=20, pady=5)

        self.lbl_estado = tk.Label(
            self.frame_info, 
            text="🟢 Modo continuo activo: Muestra una señal a la cámara...", 
            font=("Arial", 12, "bold"), 
            fg="#a6e3a1", 
            bg="#181825"
        )
        self.lbl_estado.pack(side="left", pady=5)

        # Controles
        self.btn_toggle = tk.Button(
            self.frame_info,
            text="Pausar Detección",
            font=("Arial", 10, "bold"),
            bg="#f38ba8",
            fg="#11111b",
            command=self.toggle_auto,
            cursor="hand2"
        )
        self.btn_toggle.pack(side="right", padx=5)

        # Iniciar Cámara
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "No se pudo acceder a la cámara web de tu PC.")
            return

        # Bucle de actualización de video
        self.actualizar_video()

        # Bucle de análisis continuo (cada 1.2 segundos para no sobrecargar)
        self.bucle_auto_analisis()

    def toggle_auto(self):
        self.auto_detect = not self.auto_detect
        if self.auto_detect:
            self.btn_toggle.config(text="Pausar Detección", bg="#f38ba8")
            self.lbl_estado.config(text="🟢 Escaneando en tiempo real...", fg="#a6e3a1")
        else:
            self.btn_toggle.config(text="Reanudar Detección", bg="#a6e3a1")
            self.lbl_estado.config(text="⏸️ Detección en pausa", fg="#f9e2af")

    def actualizar_video(self):
        ret, frame = self.cap.read()
        if ret:
            self.current_frame = frame.copy()

            # Convertir a RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img = img.resize((700, 480))

            # Dibujar los recuadros de las detecciones si hay alguna
            if self.ultimas_detecciones:
                draw = ImageDraw.Draw(img)
                orig_h, orig_w = frame.shape[:2]
                scale_x = 700 / orig_w
                scale_y = 480 / orig_h

                for det in self.ultimas_detecciones:
                    conf = det.get("confidence", 0.0)
                    if conf < 0.55:  # Descartar detecciones dudosas o falsos positivos
                        continue

                    # Las predicciones de Roboflow traen coordenadas normalizadas o en píxeles (x, y, width, height)
                    x = det.get("x", 0) * scale_x
                    y = det.get("y", 0) * scale_y
                    w = det.get("width", 0) * scale_x
                    h = det.get("height", 0) * scale_y
                    clase = det.get("class", det.get("label", "Señal"))

                    x0 = x - (w / 2)
                    y0 = y - (h / 2)
                    x1 = x + (w / 2)
                    y1 = y + (h / 2)

                    # Dibujar caja y texto
                    draw.rectangle([x0, y0, x1, y1], outline="#a6e3a1", width=3)
                    draw.text((x0, max(0, y0 - 15)), f"{clase} ({int(conf * 100)}%)", fill="#a6e3a1")

            imgtk = ImageTk.PhotoImage(image=img)
            self.lbl_video.imgtk = imgtk
            self.lbl_video.configure(image=imgtk)

        self.root.after(25, self.actualizar_video)

    def bucle_auto_analisis(self):
        if self.auto_detect and not self.procesando and self.current_frame is not None:
            self.procesando = True
            threading.Thread(target=self._analizar_en_segundo_plano, args=(self.current_frame.copy(),), daemon=True).start()

        # Volver a llamar al análisis cada 1.5 segundos
        self.root.after(1500, self.bucle_auto_analisis)

    def _analizar_en_segundo_plano(self, frame):
        try:
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_bytes = buffer.tobytes()

            from sst_multi_detector import detectar_todo
            preds = detectar_todo(jpg_bytes)

            self.ultimas_detecciones = preds

            if preds:
                # Tomar los nombres de clases detectadas únicas
                nombres = ", ".join(list(dict.fromkeys([p.get('class', p.get('label', 'Objeto SST')) for p in preds])))
                self.root.after(0, lambda: self.lbl_estado.config(text=f"🎯 ¡DETECTADO!: {nombres}", fg="#a6e3a1"))
            else:
                self.root.after(0, lambda: self.lbl_estado.config(text="🔍 Escaneando... muestra una señal, camilla o extintor", fg="#89b4fa"))
        except Exception as e:
            pass
        finally:
            self.procesando = False

    def cerrar(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CamaraEnTiempoReal(root)
    root.protocol("WM_DELETE_WINDOW", app.cerrar)
    root.mainloop()
