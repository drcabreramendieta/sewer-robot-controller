import json
import threading
import time
from typing import Any, Dict, List, Optional
from logging import Logger

import requests
from websocket import WebSocketApp  # websocket-client

from Inspection.adapters.eventing.diagnosis_event_publisher import DiagnosisEventPublisher
from Inspection.ports.output import DiagnosisControllerPort


class _WsHandle:
    def __init__(self, app: WebSocketApp, thread: threading.Thread, stop_evt: threading.Event):
        self.app = app
        self.thread = thread
        self.stop_evt = stop_evt


class VisionFastApiDiagnosisControllerAdapter(DiagnosisControllerPort):
    def __init__(
        self,
        base_url: str,
        ws_base_url: str,
        timeout_seconds: float,
        event_publisher: DiagnosisEventPublisher,
        logger: Logger,
    ) -> None:
        super().__init__()
        self._base = base_url.rstrip("/")
        self._ws_base = ws_base_url.rstrip("/")
        self._timeout = timeout_seconds
        self._event_publisher = event_publisher
        self._logger = logger
        self._session = requests.Session()
        self._ws_handle: Optional[_WsHandle] = None

    def _url(self, path: str) -> str:
        return f"{self._base}{path}"

    def _ws_url(self, path: str) -> str:
        return f"{self._ws_base}{path}"

    # --------- Diagnosis/config ----------
    def list_models(self) -> List[Dict[str, Any]]:
        r = self._session.get(self._url("/diagnosis/models"), timeout=self._timeout)
        r.raise_for_status()
        return r.json()

    def select_model(self, model_id: str) -> Dict[str, Any]:
        r = self._session.post(self._url(f"/diagnosis/models/{model_id}"), timeout=self._timeout)
        r.raise_for_status()
        return r.json()

    def has_active_model(self) -> bool:
        r = self._session.get(self._url("/diagnosis/models/active"), timeout=self._timeout)
        r.raise_for_status()
        data = r.json()
        return bool(data.get("has_model", False))

    # --------- Video ----------
    def start_video_session(self) -> str:
        r = self._session.post(self._url("/video/start"), timeout=self._timeout)
        r.raise_for_status()
        # FastAPI response_model=UUID -> normalmente string UUID
        return str(r.json())

    def stop_video_session(self, session_id: str) -> str:
        r = self._session.post(self._url(f"/video/stop/{session_id}"), timeout=self._timeout)
        r.raise_for_status()
        return str(r.json())

    def get_video_status(self, session_id: str) -> str:
        r = self._session.get(self._url(f"/video/status/{session_id}"), timeout=self._timeout)
        r.raise_for_status()
        return str(r.json())

    # --------- Report ----------
    def list_report_sessions(self) -> List[str]:
        r = self._session.get(self._url("/report/sessions"), timeout=self._timeout)
        r.raise_for_status()
        return [str(x) for x in r.json()]

    def get_report_summary(
        self,
        session_id: str,
        operator: str,
        location: str,
        job_order: Optional[str] = None,
    ) -> Dict[str, Any]:
        params = {"operator": operator, "location": location}
        if job_order:
            params["job_order"] = job_order

        r = self._session.get(self._url(f"/report/summary/{session_id}"), params=params, timeout=self._timeout)
        r.raise_for_status()
        return r.json()

    # --------- WS ----------
    def connect_report_ws(self, session_id: str) -> None:
        self.disconnect_report_ws()
        ws_url = self._ws_url(f"/report/ws/{session_id}")

        stop_evt = threading.Event()

        def _on_message(ws, message: str):
            try:
                payload = json.loads(message)
                self._event_publisher.publish(payload)
            except Exception as exc:
                self._logger.error("WS message parse failed: %s", exc, exc_info=True)

        def _on_error(ws, error):
            self._logger.error("WS error: %s", error)

        def _on_close(ws, close_status_code, close_msg):
            self._logger.info("WS closed: code=%s msg=%s", close_status_code, close_msg)

        def _on_open(ws):
            # Keepalive: enviar texto periódicamente (el server hace receive_text loop)
            def _keepalive():
                while not stop_evt.is_set():
                    try:
                        ws.send("ping")
                    except Exception:
                        break
                    time.sleep(10)

            t = threading.Thread(target=_keepalive, daemon=True)
            t.start()

        app = WebSocketApp(
            ws_url,
            on_open=_on_open,
            on_message=_on_message,
            on_error=_on_error,
            on_close=_on_close,
        )

        def _run():
            # run_forever bloquea; por eso va en thread
            app.run_forever()

        th = threading.Thread(target=_run, daemon=True)
        th.start()

        self._ws_handle = _WsHandle(app=app, thread=th, stop_evt=stop_evt)

    def disconnect_report_ws(self) -> None:
        if self._ws_handle is None:
            return
        self._ws_handle.stop_evt.set()
        try:
            self._ws_handle.app.close()
        except Exception:
            pass
        finally:
            self._ws_handle = None
