"""
Servicio de Análisis Simulado (Fallback Offline).
Permite que el inspector continúe su labor de campo aún sin conexión a internet
o si el modelo de red neuronal no se encuentra cargado, utilizando reglas de inferencia SST.
"""
from typing import Dict, Any, Optional
from app.models.catalogo_sst import deducir_por_contexto

class AnalisisSimuladoService:
    def analizar(self, observacion: str = "", ubicacion: str = "", tipo_esperado: str = "") -> Dict[str, Any]:
        """
        Deduce la señal y condición a partir de la observación de campo y ubicación.
        """
        texto_completo = f"{observacion} {ubicacion} {tipo_esperado}".strip()
        diagnostico = deducir_por_contexto(texto_completo)
        
        # Ajustar condición según adjetivos encontrados en la observación
        condicion = diagnostico.get("condicion_default", "Requiere verificación")
        texto_lower = texto_completo.lower()
        if any(w in texto_lower for w in ["bueno", "ok", "conforme", "operativo", "limpio"]):
            condicion = "Conforme"
        elif any(w in texto_lower for w in ["bloqueado", "obstruido", "tapado", "cajas enfrente"]):
            condicion = "Obstruido"
        elif any(w in texto_lower for w in ["vencido", "descargado", "baja presion", "sin tarjeta"]):
            condicion = "Vencido / Requiere Mantenimiento"
        elif any(w in texto_lower for w in ["roto", "danado", "despegado", "descolorido"]):
            condicion = "Dañado / Deteriorado"
            
        return {
            "elemento": diagnostico["elemento"],
            "categoria": diagnostico["categoria"],
            "condicion": condicion,
            "confianza": 0.88,
            "estado": "pendiente",
            "recomendacion": diagnostico["recomendacion"],
            "norma": diagnostico.get("norma", ""),
            "color_seguridad": diagnostico.get("color_seguridad", ""),
            "color_contraste": diagnostico.get("color_contraste", ""),
            "forma_geometrica": diagnostico.get("forma_geometrica", ""),
            "cobertura_min_color": diagnostico.get("cobertura_min_color", ""),
            "tamano_recomendado": diagnostico.get("tamano_recomendado", ""),
            "formula_dimension": diagnostico.get("formula_dimension", ""),
            "altura_montaje": diagnostico.get("altura_montaje", ""),
            "demarcacion_piso": diagnostico.get("demarcacion_piso", ""),
            "fotoluminiscencia": diagnostico.get("fotoluminiscencia", ""),
            "checklist_sst": diagnostico.get("checklist_sst", []),
            "modo": "simulado_offline",
            "detecciones": []
        }

analisis_simulado_service = AnalisisSimuladoService()
