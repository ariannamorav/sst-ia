"""
Módulo de compatibilidad y alias para el servicio de reporte fotográfico.
Redirige directamente al servicio oficial centralizado: app/services/pdf_service.py
"""
from app.services.pdf_service import (
    pdf_service as reporte_fotografico_service,
    PDFService as ReporteFotograficoService,
    pdf_service
)

__all__ = ["reporte_fotografico_service", "ReporteFotograficoService", "pdf_service"]
