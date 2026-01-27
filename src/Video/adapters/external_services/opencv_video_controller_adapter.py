from Video.ports.output.video_controller_port import VideoControllerPort
from typing import Callable, Optional
from Video.domain.entities.video_entities import VideoMessage
import cv2
import threading
import time
from logging import Logger

# Refactor de este adaptador para evitar crash de la UI cuando OpenCV sufre segfault en captura RTSP. y al cerrar la app.


class OpencvVideoControllerAdapter(VideoControllerPort):
    """
    Adapter de video para UI (solo visualización).

    Mejoras mínimas:
    - reconexión automática cuando el DVR/cámara pierde RTSP por unos segundos
    - opcional: forzar RTSP sobre TCP (reduce corrupción por UDP)
    - no rompe la interfaz: callback_setup / start_listening / stop_listening igual
    """

    def __init__(self, rtsp_url: str, logger: Logger) -> None:
        super().__init__()
        self.callback: Optional[Callable[[VideoMessage], None]] = None
        self.rtsp_url = rtsp_url
        self.logger = logger

        self.running = False
        self.cap = None

        # Para parar sin carreras
        self._stop_evt = threading.Event()
        self.thread_capture: Optional[threading.Thread] = None

        # --- parámetros conservadores (no agresivos) ---
        self._max_consecutive_failures = 20   # tolera cortes momentáneos
        self._reconnect_sleep_seconds = 0.5   # espera antes de reintentar
        self._read_fail_sleep_seconds = 0.05  # no CPU burn

    def callback_setup(self, callback: Callable[[VideoMessage], None]) -> None:
        self.callback = callback

    def start_listening(self) -> None:
        # Permite reiniciar si se cerró antes
        if self.thread_capture is not None and self.thread_capture.is_alive():
            return

        self._stop_evt.clear()
        self.running = True
        self.thread_capture = threading.Thread(target=self.capture_frames, daemon=True)
        self.thread_capture.start()

    def stop_listening(self) -> None:
        """
        IMPORTANTE:
        - No hacemos cap.release() aquí para evitar segfault por carrera con cap.read()
        - Solo señalizamos y esperamos.
        """
        self.running = False
        self._stop_evt.set()

        if self.thread_capture is not None:
            try:
                self.thread_capture.join(timeout=3.0)
            except Exception:
                pass

        # No uses destroyAllWindows en UI Qt (no estás creando ventanas OpenCV)
        # cv2.destroyAllWindows()

    def _build_rtsp_url(self) -> str:
        # Forzar TCP ayuda a evitar corrupción por UDP (y reduce segfaults)
        url = self.rtsp_url
        if url.startswith("rtsp://") and "rtsp_transport=" not in url:
            sep = "&" if "?" in url else "?"
            url = f"{url}{sep}rtsp_transport=tcp"
        return url

    def _open_capture(self):
        url = self._build_rtsp_url()

        try:
            cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
        except Exception:
            cap = cv2.VideoCapture(url)

        if not cap.isOpened():
            return None

        # Si tu OpenCV lo soporta, esto evita bloqueos largos en read()
        try:
            cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 2000)
        except Exception:
            pass
        try:
            cap.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, 2000)
        except Exception:
            pass
        try:
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        except Exception:
            pass

        return cap

    def capture_frames(self):
        consecutive_failures = 0
        self.cap = None

        try:
            while self.running and not self._stop_evt.is_set():
                # (re)abrir
                if self.cap is None or not self.cap.isOpened():
                    if self.cap is not None:
                        try:
                            self.cap.release()
                        except Exception:
                            pass
                        self.cap = None

                    self.logger.info("[VIDEO] Opening RTSP capture...")
                    self.cap = self._open_capture()
                    if self.cap is None:
                        self.logger.warning("[VIDEO] Cannot open RTSP stream. Retrying...")
                        time.sleep(self._reconnect_sleep_seconds)
                        continue

                    consecutive_failures = 0
                    time.sleep(0.2)

                # leer
                ret, frame = self.cap.read()

                if not self.running or self._stop_evt.is_set():
                    break

                if not ret or frame is None:
                    consecutive_failures += 1
                    if consecutive_failures < self._max_consecutive_failures:
                        time.sleep(self._read_fail_sleep_seconds)
                        continue

                    self.logger.warning("[VIDEO] Stream read failing. Reconnecting capture...")
                    try:
                        self.cap.release()
                    except Exception:
                        pass
                    self.cap = None
                    consecutive_failures = 0
                    time.sleep(self._reconnect_sleep_seconds)
                    continue

                consecutive_failures = 0

                if self.callback is not None:
                    self.callback(VideoMessage(frame=frame))

        except cv2.error as e:
            self.logger.error(f"[VIDEO] OpenCV error: {e}", exc_info=True)

        except Exception as e:
            self.logger.error(f"[VIDEO] Unexpected error: {e}", exc_info=True)

        finally:
            # release solo aquí (en el MISMO hilo que hace read)
            if self.cap is not None:
                try:
                    self.cap.release()
                except Exception:
                    pass
            self.cap = None
            self.logger.info("[VIDEO] capture_frames stopped.")