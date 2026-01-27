from dependency_injector import containers, providers
import logging
import can
from pathlib import Path

from Communication.containers import CommunicationContainer
from Inspection.containers import InspectionContainer
from Panel_and_Feeder.containers import PanelAndFeederContainer
from Video.containers import VideoContainer


def get_logger(name: str = "app_logger") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


def create_can_bus(channel: str, interface: str, bitrate: int, logger: logging.Logger):
    try:
        return can.interface.Bus(channel=channel, interface=interface, bitrate=bitrate)
    except OSError as exc:
        logger.error("Failed to establish communication with the CAN bus: %s", exc, exc_info=True)
        return None


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "configs" / "config.yaml"


def _wire_all(communication, panel_and_feeder, video, inspection):
    communication.wire_observers()
    panel_and_feeder.wire_observers()
    video.wire_observers()
    inspection.wire_observers()
    return True


class HexContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    logger = providers.Singleton(get_logger, name=config.logging.name)

    can_bus = providers.Singleton(
        create_can_bus,
        channel=config.can.channel,
        interface=config.can.interface,
        bitrate=config.can.bitrate,
        logger=logger,
    )

    telemetry_update_service = providers.Dependency()
    panel_update_services = providers.Dependency()
    feeder_update_service = providers.Dependency()
    video_update_service = providers.Dependency()

    communication = providers.Container(
        CommunicationContainer,
        logger=logger,
        can_bus=can_bus,
        telemetry_update_service=telemetry_update_service,
    )

    panel_and_feeder = providers.Container(
        PanelAndFeederContainer,
        config=config.serial,
        logger=logger,
        panel_update_services=panel_update_services,
        feeder_update_service=feeder_update_service,
    )

    video = providers.Container(
        VideoContainer,
        config=config.video,
        logger=logger,
        video_update_service=video_update_service,
    )

    inspection = providers.Container(
        InspectionContainer,
        logger=logger,
        movement_service=communication.movement_service,
        camera_services=communication.camera_services,
        arm_services=communication.arm_services,
        selector_signal=communication.selector_signal,
        feeder_services=panel_and_feeder.feeder_services,
        video_session_services=video.session_services,
        vision=config.vision,   # NEW Diagnosis
        
    )

    wire_observers = providers.Callable(
        _wire_all,
        communication=communication,
        panel_and_feeder=panel_and_feeder,
        video=video,
        inspection=inspection,
    )


def build_container(config_path: str = str(DEFAULT_CONFIG_PATH)) -> HexContainer:
    container = HexContainer()
    container.config.from_yaml(config_path)

    container.telemetry_update_service.override(container.inspection.telemetry_update_service)
    container.panel_update_services.override(container.inspection.panel_update_services)
    container.feeder_update_service.override(container.inspection.feeder_update_service)
    container.video_update_service.override(container.inspection.video_update_service)

    container.wire_observers()

    return container
