# src/Communication/adapters/external_services/can_expansion_camera_controller_adapter.py

from __future__ import annotations

from logging import Logger
from typing import List

import can

from Communication.ports.output.camera_controller_port import CameraControllerPort
from Communication.domain.entities.camera_entities import (
    CameraState,
    FocusState,
    PanState,
    TiltState,
    ZoomState,
)

class CanExpansionCameraControllerAdapter(CameraControllerPort):
    """
    Adapter para la camara nueva (Expansion Mode) basada en protocolo RS485 (MH70).

    NOTA:
    - El protocolo MH70 (PDF) define tramas de 7 bytes: FF 01 ... checksum.
    - Falta definir como se encapsula esta trama RS485 dentro del bus CAN de su sistema.
    """

    # RS485 (MH70) constants (segun PDF: address = 0x01)
    _HDR = 0xFF
    _ADDR = 0x01

    # Pelco-D style commands (segun PDF)
    _STOP_FRAME = [0xFF, 0x01, 0x00, 0x00, 0x00, 0x00, 0x01]

    # Tilt
    _CMD_TILT_UP   = (0x00, 0x08)  # cmd2=0x08, speed in data2
    _CMD_TILT_DOWN = (0x00, 0x10)

    # Pan
    _CMD_PAN_CW  = (0x00, 0x04)    # horizontal clockwise
    _CMD_PAN_CCW = (0x00, 0x02)    # horizontal counterclockwise

    # Focus
    _CMD_FOCUS_PLUS  = (0x01, 0x00)
    _CMD_FOCUS_MINUS = (0x00, 0x80)

    # Zoom
    _CMD_ZOOM_PLUS  = (0x00, 0x20)
    _CMD_ZOOM_MINUS = (0x00, 0x40)

    def __init__(self, bus: can.BusABC, logger: Logger) -> None:
        self.bus = bus
        self.logger = logger

    def initialize_camera(self) -> bool:
        """
        Si su camara nueva requiere un INIT especifico, se define aqui.
        Por ahora, no se inventa un INIT: puede ser no requerido a nivel RS485.
        """
        self.logger.info("Expansion camera initialize_camera(): no-op (pendiente de confirmar INIT real)")
        return True

    def update_camera_state(self, module: CameraState) -> None:
        """
        Construye y envia un comando segun prioridad:
        - STOP (si todo esta en STOP)
        - Zoom / Focus / Pan / Tilt (segun estados)
        Nota: segun el PDF, cualquier operacion debe ser seguida por STOP.
        """
        # 1) Determinar comando principal
        frame = None

        # Zoom tiene prioridad (por ser nuevo en expansion camera)
        if hasattr(module, "zoom") and module.zoom in (ZoomState.IN, ZoomState.OUT):
            if module.zoom == ZoomState.IN:
                frame = self._build_zoom_plus(module)
            else:
                frame = self._build_zoom_minus(module)

        # Focus
        elif module.focus in (FocusState.IN, FocusState.OUT):
            if module.focus == FocusState.IN:
                frame = self._build_focus_plus(module)
            else:
                frame = self._build_focus_minus(module)

        # Pan
        elif module.pan in (PanState.LEFT, PanState.RIGHT):
            if module.pan == PanState.RIGHT:
                frame = self._build_pan_cw(module)
            else:
                frame = self._build_pan_ccw(module)

        # Tilt
        elif module.tilt in (TiltState.UP, TiltState.DOWN):
            if module.tilt == TiltState.UP:
                frame = self._build_tilt_up(module)
            else:
                frame = self._build_tilt_down(module)

        # Si no hay movimiento -> STOP
        else:
            frame = self._STOP_FRAME

        # 2) Enviar comando
        self._send_rs485_frame_over_can(frame)

        # 3) Segun el PDF: toda operacion debe ser seguida por STOP
        # Para STOP ya no se repite.
        if frame != self._STOP_FRAME:
            self._send_rs485_frame_over_can(self._STOP_FRAME)

    # -------------------------
    # Frame builders
    # -------------------------

    def _brightness_to_0x3f(self, light_value_0_100: int) -> int:
        # Mapea 0..100 a 0..63
        v = max(0, min(100, int(light_value_0_100)))
        return int(round(v * 63 / 100))

    def _checksum_pelco_d(self, bytes_6: List[int]) -> int:
        # Checksum = suma de bytes (ADDR..DATA2) modulo 256
        return sum(bytes_6[1:6]) & 0xFF

    def _build_frame(self, cmd1: int, cmd2: int, data1: int, data2: int) -> List[int]:
        base = [self._HDR, self._ADDR, cmd1 & 0xFF, cmd2 & 0xFF, data1 & 0xFF, data2 & 0xFF]
        chk = self._checksum_pelco_d(base)
        return base + [chk]

    def _build_tilt_up(self, module: CameraState) -> List[int]:
        speed = self._brightness_to_0x3f(module.light.value)  # reutilizamos slider como “speed” si no hay otro
        cmd1, cmd2 = self._CMD_TILT_UP
        return self._build_frame(cmd1, cmd2, 0x00, speed)

    def _build_tilt_down(self, module: CameraState) -> List[int]:
        speed = self._brightness_to_0x3f(module.light.value)
        cmd1, cmd2 = self._CMD_TILT_DOWN
        return self._build_frame(cmd1, cmd2, 0x00, speed)

    def _build_pan_cw(self, module: CameraState) -> List[int]:
        speed = self._brightness_to_0x3f(module.light.value)
        cmd1, cmd2 = self._CMD_PAN_CW
        return self._build_frame(cmd1, cmd2, speed, 0x00)

    def _build_pan_ccw(self, module: CameraState) -> List[int]:
        speed = self._brightness_to_0x3f(module.light.value)
        cmd1, cmd2 = self._CMD_PAN_CCW
        return self._build_frame(cmd1, cmd2, speed, 0x00)

    def _build_focus_plus(self, module: CameraState) -> List[int]:
        speed = self._brightness_to_0x3f(module.light.value)
        cmd1, cmd2 = self._CMD_FOCUS_PLUS
        return self._build_frame(cmd1, cmd2, 0x00, speed)

    def _build_focus_minus(self, module: CameraState) -> List[int]:
        speed = self._brightness_to_0x3f(module.light.value)
        cmd1, cmd2 = self._CMD_FOCUS_MINUS
        return self._build_frame(cmd1, cmd2, 0x00, speed)

    def _build_zoom_plus(self, module: CameraState) -> List[int]:
        speed = self._brightness_to_0x3f(module.light.value)
        cmd1, cmd2 = self._CMD_ZOOM_PLUS
        return self._build_frame(cmd1, cmd2, 0x00, speed)

    def _build_zoom_minus(self, module: CameraState) -> List[int]:
        speed = self._brightness_to_0x3f(module.light.value)
        cmd1, cmd2 = self._CMD_ZOOM_MINUS
        return self._build_frame(cmd1, cmd2, 0x00, speed)

    # -------------------------
    # Transport (TODO)
    # -------------------------

    def _send_rs485_frame_over_can(self, frame: List[int]) -> None:
        """
        TODO (no se inventa):
        Definir como se envia una trama RS485 (7 bytes) usando el bus CAN de su sistema.

        Necesito que usted confirme una de estas dos cosas:
        - Existe un "bridge" CAN->RS485 y cual es el arbitration_id + formato de payload.
        - O bien, que la camara nueva NO se controla via RS485 directo, sino via comandos compactos (tipo 4 bytes)
          como la camara antigua.
        """
        self.logger.info(f"Expansion camera RS485 frame ready (len={len(frame)}): {frame}")

        # Placeholder seguro: no enviar nada hasta confirmar encapsulado.
        # raise NotImplementedError("Defina encapsulado CAN->RS485 para enviar la trama RS485.")
        try:
            # Ejemplo SOLO de estructura (NO funcional sin especificacion):
            # message = can.Message(arbitration_id=0x????, data=frame[:8], is_extended_id=False)
            # self.bus.send(message)
            pass
        except can.CanError as e:
            self.logger.error(f"CAN Error (expansion camera): {e}")
        except OSError as e:
            self.logger.error(f"OSError (expansion camera): {e}")
