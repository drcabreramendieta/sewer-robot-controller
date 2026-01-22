import threading
import time
from typing import Any, Dict, List, Optional
from uuid import uuid4
from logging import Logger

from Inspection.adapters.eventing.diagnosis_event_publisher import DiagnosisEventPublisher
from Inspection.ports.output import DiagnosisControllerPort


class _MockWsHandle:
    def __init__(self, stop_evt: threading.Event, thread: threading.Thread):
        self.stop_evt = stop_evt
        self.thread = thread


class MockVisionFastApiDiagnosisControllerAdapter(DiagnosisControllerPort):
    def __init__(self, event_publisher: DiagnosisEventPublisher, logger: Logger) -> None:
        super().__init__()
        self._event_publisher = event_publisher
        self._logger = logger
        self._active_model: Optional[str] = None
        self._sessions: List[str] = []
        self._ws_handle: Optional[_MockWsHandle] = None

    def list_models(self) -> List[Dict[str, Any]]:
        return [
            {"id": "m1", "name": "MockModel-1", "description": "modelo mock"},
            {"id": "m2", "name": "MockModel-2", "description": "modelo mock"},
        ]

    def select_model(self, model_id: str) -> Dict[str, Any]:
        self._active_model = model_id
        return {"status": "model set", "model_id": model_id}

    def has_active_model(self) -> bool:
        return self._active_model is not None

    def start_video_session(self) -> str:
        sid = str(uuid4())
        self._sessions.append(sid)
        return sid

    def stop_video_session(self, session_id: str) -> str:
        return "stopped"

    def get_video_status(self, session_id: str) -> str:
        return "running"

    def list_report_sessions(self) -> List[str]:
        return list(self._sessions)

    def get_report_summary(
        self,
        session_id: str,
        operator: str,
        location: str,
        job_order: Optional[str] = None,
    ) -> Dict[str, Any]:
        return {
            "session_id": session_id,
            "operator": operator,
            "location": location,
            "job_order": job_order,
            "counts_by_label": {"NORMAL": 120, "ANOMALY": 5},
            "total_events": 10,
        }

    def connect_report_ws(self, session_id: str) -> None:
        self.disconnect_report_ws()
        stop_evt = threading.Event()

        def _run():
            labels = ["NORMAL", "NORMAL", "ANOMALY", "NORMAL"]
            idx = 0
            while not stop_evt.is_set():
                payload = {
                    "type": "state_change",
                    "session_id": session_id,
                    "event_index": idx + 1,
                    "frame_path": f"/tmp/frame_{idx}.png",
                    "label": labels[idx % len(labels)],
                    "timestamp": "2026-01-01T00:00:00",
                }
                self._event_publisher.publish(payload)
                idx += 1
                time.sleep(0.7)

        th = threading.Thread(target=_run, daemon=True)
        th.start()
        self._ws_handle = _MockWsHandle(stop_evt=stop_evt, thread=th)

    def disconnect_report_ws(self) -> None:
        if self._ws_handle is not None:
            self._ws_handle.stop_evt.set()
            self._ws_handle = None
