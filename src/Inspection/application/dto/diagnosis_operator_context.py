from dataclasses import dataclass
# Esto sirve para definir el contexto del operador de visión y poder generar el summary del reporte
@dataclass
class DiagnosisOperatorContext:
    operator: str
    location: str
    job_order: str
