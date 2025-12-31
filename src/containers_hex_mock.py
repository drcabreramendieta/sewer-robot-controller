from dependency_injector import containers, providers
import logging
from pathlib import Path

from Communication.containers import CommunicationMockContainer
from Inspection.containers import InspectionContainer
from Panel_and_Feeder.containers import PanelAndFeederMockContainer
from Video.containers import VideoMockContainer


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


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "configs" / "config_mock.yaml"


def _wire_all(communication, panel_and_feeder, video, inspection):
    communication.wire_observers()
    panel_and_feeder.wire_observers()
    video.wire_observers()
    inspection.wire_observers()
    return True


class HexMockContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    logger = providers.Singleton(get_logger, name=config.logging.name)

    telemetry_update_service = providers.Dependency()
    panel_update_services = providers.Dependency()
    feeder_update_service = providers.Dependency()
    video_update_service = providers.Dependency()

    movement_service = providers.Dependency()
    camera_services = providers.Dependency()
    feeder_services = providers.Dependency()
    video_session_services = providers.Dependency()

    communication = providers.Container(
        CommunicationMockContainer,
        logger=logger,
        telemetry_update_service=telemetry_update_service,
    )

    panel_and_feeder = providers.Container(
        PanelAndFeederMockContainer,
        config=config.serial,
        logger=logger,
        panel_update_services=panel_update_services,
        feeder_update_service=feeder_update_service,
    )

    video = providers.Container(
        VideoMockContainer,
        config=config.video,
        logger=logger,
        video_update_service=video_update_service,
    )

    inspection = providers.Container(
        InspectionContainer,
        logger=logger,
        movement_service=movement_service,
        camera_services=camera_services,
        feeder_services=feeder_services,
        video_session_services=video_session_services,
    )

    wire_observers = providers.Callable(
        _wire_all,
        communication=communication,
        panel_and_feeder=panel_and_feeder,
        video=video,
        inspection=inspection,
    )


def build_container(config_path: str = str(DEFAULT_CONFIG_PATH)) -> HexMockContainer:
    container = HexMockContainer()
    container.config.from_yaml(config_path)

    container.telemetry_update_service.override(container.inspection.telemetry_update_service)
    container.panel_update_services.override(container.inspection.panel_update_services)
    container.feeder_update_service.override(container.inspection.feeder_update_service)
    container.video_update_service.override(container.inspection.video_update_service)

    container.movement_service.override(container.communication.movement_service)
    container.camera_services.override(container.communication.camera_services)
    container.feeder_services.override(container.panel_and_feeder.feeder_services)
    container.video_session_services.override(container.video.session_services)

    container.wire_observers()

    return container
