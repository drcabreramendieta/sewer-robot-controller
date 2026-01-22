from typing import Any, Dict
from Inspection.ports.output import DiagnosisObserverPort
from Inspection.adapters.gui.main_window import MainWindow

class GuiDiagnosisObserverAdapter(DiagnosisObserverPort):
    def __init__(self, gui: MainWindow):
        super().__init__()
        self.gui = gui

    def on_diagnosis_event(self, event: Dict[str, Any]) -> None:
        et = event.get("type", "unknown")

        if et == "vision_init":
            if event.get("ok"):
                self.gui.append_diagnosis_status(
                    f"[OK] Vision listo | modelos={event.get('models_count')} sesiones={event.get('sessions_count')} "
                    f"| modelo_activo={event.get('has_active_model')}"
                )
            else:
                self.gui.append_diagnosis_status(f"[ERROR] Vision init: {event.get('error')}")

        elif et == "model_selected":
            self.gui.append_diagnosis_status(f"Modelo seleccionado: {event.get('model_id')}")

        elif et == "diagnosis_started":
            sid = event.get("session_id")
            self.gui.append_diagnosis_status(f"Diagnóstico iniciado. session_id={sid}")
            self.gui.set_diagnosis_overlay(f"RUNNING\nsid={sid}")
            self.gui.set_diag_controls_state(running=True) # Manejar estado botones


        elif et == "diagnosis_stopped":
            self.gui.append_diagnosis_status(f"Diagnóstico detenido. status={event.get('status')}")
            self.gui.set_diagnosis_overlay("STOPPED")
            self.gui.set_diag_controls_state(running=False) # Manejar estado botones


        elif et == "state_change":
            label = event.get("label", "N/A")
            idx = event.get("event_index", "?")
            self.gui.set_diagnosis_overlay(f"{label}\nevent={idx}")

        elif et == "summary" and "summary" in event:
            s = event["summary"]
            counts = s.get("counts_by_label", {})
            self.gui.append_diagnosis_status(f"Resumen: counts_by_label={counts}")

        elif et == "summary":
            # cuando viene directo desde WS (sin wrapper)
            counts = event.get("counts_by_label", {})
            self.gui.append_diagnosis_status(f"Resumen (WS): counts_by_label={counts}")

        # Mostrar mensajes del tipo ui_message
        elif et == "ui_message":
            self.gui.append_diagnosis_status(event.get("text", ""))

        else:
            # fallback
            self.gui.append_diagnosis_status(f"[{et}] {event}")
