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
    #Light
    _FORCE_EXTREME_STEPS = 30   
    _LED_PLUS_FRAME  = [0xFF, 0x01, 0x02, 0x00, 0x00, 0x3F, 0x42]
    _LED_MINUS_FRAME = [0xFF, 0x01, 0x04, 0x00, 0x00, 0x3F, 0x44]

    #speed
    _SPD = 0x82
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
        self._last_light_level = 0
        self._last_led_level: int | None = None

    def initialize_camera(self) -> bool:
        self.logger.info("Expansion camera initialize_camera(): no-op (pendiente de confirmar INIT real)")
        return True

    def _light_value_to_level(self, v: int) -> int:
        v = max(0, min(100, int(v)))
        if 0 <= v < 11:
            return 0
        elif 11 <= v < 22:
            return 1
        elif 22 <= v < 33:
            return 2
        elif 33 <= v < 44:
            return 3
        elif 44 <= v < 55:
            return 4
        elif 55 <= v < 66:
            return 5
        elif 66 <= v < 77:
            return 6
        elif 77 <= v < 88:
            return 7
        else:  # 88..100
            return 8

    def _apply_led_level(self, new_value: int) -> None:
        v = max(0, min(100, int(new_value)))

        # Evita recalcular/aplicar si el valor no cambió
        if self._last_led_level == v:
            return
        self._last_led_level = v

        # Nivel objetivo (0..8)
        if v <= 10:
            target_level = 0
        elif v >= 90:
            target_level = 8
        else:
            target_level = self._light_value_to_level(v)

        old_level = self._last_light_level

        # Nada que hacer
        if target_level == old_level:
            return

        steps = abs(target_level - old_level)
        frame = self._LED_PLUS_FRAME if target_level > old_level else self._LED_MINUS_FRAME

        # Enviar solo los pasos necesarios (no un "FORCE" fijo)
        for _ in range(steps):
            self._send_rs485_frame_over_can(frame)

        self._last_light_level = target_level




    def update_camera_state(self, module: CameraState) -> None:
        frame = None
        any_motion = (
            module.tilt in (TiltState.UP, TiltState.DOWN)
            or module.pan in (PanState.LEFT, PanState.RIGHT)
            or module.focus in (FocusState.IN, FocusState.OUT)
            or getattr(module, "zoom", ZoomState.STOP) in (ZoomState.IN, ZoomState.OUT)
        )

        if not any_motion:
            self._apply_led_level(module.light.value)

        # 1) STOP tiene prioridad cuando NO hay movimiento activo
        if not any_motion:
            frame = self._STOP_FRAME

        elif getattr(module, "zoom", ZoomState.STOP) in (ZoomState.IN, ZoomState.OUT):
            frame = self._build_zoom_plus() if module.zoom == ZoomState.IN else self._build_zoom_minus()

        elif module.focus in (FocusState.IN, FocusState.OUT):
            frame = self._build_focus_plus() if module.focus == FocusState.IN else self._build_focus_minus()

        elif module.pan in (PanState.LEFT, PanState.RIGHT):
            frame = self._build_pan_cw() if module.pan == PanState.RIGHT else self._build_pan_ccw()

        elif module.tilt in (TiltState.UP, TiltState.DOWN):
            frame = self._build_tilt_up() if module.tilt == TiltState.UP else self._build_tilt_down()

        else:
            frame = self._STOP_FRAME

        print(
            f"[CAM] tilt={module.tilt} pan={module.pan} focus={module.focus} zoom={getattr(module,'zoom',None)} "
            f"light={module.light.value} any_motion={any_motion} frame={'STOP' if frame==self._STOP_FRAME else 'MOVE'}"
        )
        self._send_rs485_frame_over_can(frame)


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

    def _build_tilt_up(self) -> List[int]:
        return self._build_frame(0x00, 0x08, 0x00, self._SPD)

    def _build_tilt_down(self) -> List[int]:
        return self._build_frame(0x00, 0x10, 0x00, self._SPD)

    def _build_pan_cw(self) -> List[int]:
        return self._build_frame(0x00, 0x04, self._SPD, 0x00)

    def _build_pan_ccw(self) -> List[int]:
        return self._build_frame(0x00, 0x02, self._SPD, 0x00)

    def _build_focus_plus(self) -> List[int]:
        return self._build_frame(0x01, 0x00, 0x00, self._SPD)

    def _build_focus_minus(self) -> List[int]:
        return self._build_frame(0x00, 0x80, 0x00, self._SPD)

    def _build_zoom_plus(self) -> List[int]:
        return self._build_frame(0x00, 0x20, 0x00, self._SPD)

    def _build_zoom_minus(self) -> List[int]:
        return self._build_frame(0x00, 0x40, 0x00, self._SPD)



    # -------------------------
    # Transport (TODO)
    # -------------------------

    def _send_rs485_frame_over_can(self, frame: List[int]) -> None:
        if len(frame) != 7:
            raise ValueError(f"MH70 frame must be 7 bytes, got {len(frame)}: {frame}")

        can_id = 0x0005  # Expansion camera CAN ID

        payload = frame + [0x00]  # padding a 8 bytes
        msg = can.Message(
            arbitration_id=can_id,
            data=bytearray(payload),
            is_extended_id=False
        )

        try:
            self.bus.send(msg)
            self.logger.info(f"Sent MH70 over CAN (id=0x{can_id:04X}, dlc=8): {payload}")
        except can.CanError as e:
            self.logger.error(f"CAN Error (expansion camera): {e}")
        except OSError as e:
            self.logger.error(f"OSError (expansion camera): {e}")

