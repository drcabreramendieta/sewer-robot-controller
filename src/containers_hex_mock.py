from dependency_injector import containers, providers
import logging
from pathlib import Path
from typing import Optional

from Communication.application.services.camera_services import CameraServices
from Communication.application.services.movement_service import MovementService
from Communication.application.services.telemetry_services import TelemetryServices
from Communication.adapters.external_services.mock_can_camera_controller_adapter import (
    MockCanCameraControllerAdapter,
)
from Communication.adapters.external_services.mock_can_telemetry_controller_adapter import (
    MockCanTelemetryControllerAdapter,
)
from Communication.adapters.external_services.mock_can_wheels_controller_adapter import (
    MockCanWheelsControllerAdapter,
)
from Communication.adapters.external_services.pyqt_telemetry_observer_adapter import PyqtTelemetryObserverAdapter

from Inspection.application.services.feeder_update_service import FeederUpdateService
from Inspection.application.services.panel_update_services import PanelUpdateServices
from Inspection.application.services.session_services import SessionServices as InspectionSessionServices
from Inspection.application.services.telemetry_update_service import TelemetryUpdateService
from Inspection.application.services.video_update_service import VideoUpdateService
from Inspection.adapters.external_services.comm_camera_controller_adapter import CommCameraControllerAdapter
from Inspection.adapters.external_services.comm_movement_controller_adapter import CommMovementControllerAdapter
from Inspection.adapters.external_services.gui_feeder_observer_adapter import GuiFeederObserverAdapter
from Inspection.adapters.external_services.gui_telemetry_observer_adapter import GuiTelemetryObserverAdapter
from Inspection.adapters.external_services.gui_video_observer_adapter import GuiVideoObserverAdapter
from Inspection.adapters.external_services.paf_feeder_controller_adapter import PafFeederControllerAdapter
from Inspection.adapters.external_services.video_session_controller_adapter import VideoSessionControllerAdapter
from Inspection.adapters.gui.main_window import MainWindow

from Panel_and_Feeder.application.services.feeder_services import FeederServices
from Panel_and_Feeder.application.services.panel_services import PanelServices
from Panel_and_Feeder.adapters.external_services.mock_serial_panel_and_feeder_controller_adapter import (
    MockSerialPanelAndFeederControllerAdapter,
)
from Panel_and_Feeder.adapters.external_services.pyqt_feeder_observer_adapter import PyqtFeederObserverAdapter
from Panel_and_Feeder.adapters.external_services.pyqt_panel_observer_adapter import PyqtPanelObserverAdapter
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import SerialConfig

from Video.adapters.external_services.mock_hikvision_dvr_controller_adapter import (
    MockHikvisionDvrControllerAdapter,
)
from Video.adapters.external_services.opencv_video_controller_adapter import OpencvVideoControllerAdapter
from Video.adapters.external_services.pyqt_video_observer_adapter import PyqtVideoObserverAdapter
from Video.adapters.repositories.tinydb_repository_adapter import TinydbRepositoryAdapter
from Video.application.services.session_services import SessionServices as VideoSessionServices
from Video.application.services.video_services import VideoServices


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


def _register_observer(service, observer):
    if observer is not None:
        service.register_observer(observer)
    return service


def _wire_gui_observers(
    feeder_update_service,
    gui_feeder_observer,
    telemetry_update_service,
    gui_telemetry_observer,
    video_update_service,
    gui_video_observer,
):
    _register_observer(feeder_update_service, gui_feeder_observer)
    _register_observer(telemetry_update_service, gui_telemetry_observer)
    _register_observer(video_update_service, gui_video_observer)
    return True


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "configs" / "config_mock.yaml"


class HexMockContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    logger = providers.Singleton(get_logger, name=config.logging.name)

    can_bus = providers.Object(object())

    serial_config = providers.Singleton(
        SerialConfig,
        port=config.serial.port,
        baudrate=config.serial.baudrate,
        timeout=config.serial.timeout,
    )

    wheels_controller = providers.Singleton(
        MockCanWheelsControllerAdapter,
        logger=logger,
    )
    camera_controller = providers.Singleton(
        MockCanCameraControllerAdapter,
        logger=logger,
    )
    telemetry_controller = providers.Singleton(
        MockCanTelemetryControllerAdapter,
        logger=logger,
    )

    movement_service = providers.Singleton(
        MovementService,
        wheels_controller=wheels_controller,
    )
    camera_services = providers.Singleton(
        CameraServices,
        camera_controller=camera_controller,
    )

    comm_movement_controller = providers.Singleton(
        CommMovementControllerAdapter,
        robot=movement_service,
        logger=logger,
    )
    comm_camera_controller = providers.Singleton(
        CommCameraControllerAdapter,
        camera=camera_services,
        logger=logger,
    )

    panel_update_services = providers.Singleton(
        PanelUpdateServices,
        movement_controller=comm_movement_controller,
        camera_controller=comm_camera_controller,
    )

    panel_and_feeder_controller = providers.Singleton(
        MockSerialPanelAndFeederControllerAdapter,
        serial_conf=serial_config,
        logger=logger,
    )

    feeder_services = providers.Singleton(
        FeederServices,
        paf_controller=panel_and_feeder_controller,
        logger=logger,
        observer=providers.Object(None),
    )
    feeder_controller = providers.Singleton(
        PafFeederControllerAdapter,
        feeder_services=feeder_services,
    )
    feeder_update_service = providers.Singleton(
        FeederUpdateService,
        feeder_controller=feeder_controller,
        observer=providers.Object(None),
    )
    pyqt_feeder_observer = providers.Singleton(
        PyqtFeederObserverAdapter,
        feeder_update_service=feeder_update_service,
        logger=logger,
    )

    panel_observer = providers.Singleton(
        PyqtPanelObserverAdapter,
        panel_update_services=panel_update_services,
        logger=logger,
    )
    panel_services = providers.Singleton(
        PanelServices,
        paf_controller=panel_and_feeder_controller,
        logger=logger,
        observer=panel_observer,
    )

    video_controller = providers.Singleton(
        OpencvVideoControllerAdapter,
        rtsp_url=config.video.rtsp_url,
        logger=logger,
    )
    video_update_service = providers.Singleton(
        VideoUpdateService,
        observer=providers.Object(None),
    )
    pyqt_video_observer = providers.Singleton(
        PyqtVideoObserverAdapter,
        video_update_service=video_update_service,
        logger=logger,
    )
    video_services = providers.Singleton(
        VideoServices,
        video_controller=video_controller,
        logger=logger,
        observer=pyqt_video_observer,
    )

    video_repository = providers.Singleton(
        TinydbRepositoryAdapter,
        db_name=config.video.sessions_db,
        logger=logger,
    )
    dvr_controller = providers.Singleton(
        MockHikvisionDvrControllerAdapter,
        url=config.video.dvr.url,
        user=config.video.dvr.user,
        password=config.video.dvr.password,
        dir=config.video.dvr.dir,
        logger=logger,
    )
    video_session_services = providers.Singleton(
        VideoSessionServices,
        dvr_controller=dvr_controller,
        repository=video_repository,
        logger=logger,
    )
    video_session_controller = providers.Singleton(
        VideoSessionControllerAdapter,
        control_session=video_session_services,
        logger=logger,
    )
    session_services = providers.Singleton(
        InspectionSessionServices,
        session_controller=video_session_controller,
    )

    telemetry_update_service = providers.Singleton(
        TelemetryUpdateService,
        observer=providers.Object(None),
    )
    pyqt_telemetry_observer = providers.Singleton(
        PyqtTelemetryObserverAdapter,
        telemetry_update_service=telemetry_update_service,
        logger=logger,
    )
    telemetry_services = providers.Singleton(
        TelemetryServices,
        telemetry_controller=telemetry_controller,
        logger=logger,
        telemetry_observer=pyqt_telemetry_observer,
    )

    main_window = providers.Singleton(
        MainWindow,
        panel_services=panel_update_services,
        feeder_services=feeder_update_service,
        session_services=session_services,
    )

    gui_video_observer = providers.Singleton(
        GuiVideoObserverAdapter,
        gui=main_window,
    )
    gui_telemetry_observer = providers.Singleton(
        GuiTelemetryObserverAdapter,
        gui=main_window,
    )
    gui_feeder_observer = providers.Singleton(
        GuiFeederObserverAdapter,
        gui=main_window,
    )

    wire_feeder_observer = providers.Callable(
        _register_observer,
        service=feeder_services,
        observer=pyqt_feeder_observer,
    )
    wire_gui_observers = providers.Callable(
        _wire_gui_observers,
        feeder_update_service=feeder_update_service,
        gui_feeder_observer=gui_feeder_observer,
        telemetry_update_service=telemetry_update_service,
        gui_telemetry_observer=gui_telemetry_observer,
        video_update_service=video_update_service,
        gui_video_observer=gui_video_observer,
    )


def build_container(config_path: Optional[str] = None) -> HexMockContainer:
    container = HexMockContainer()
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    container.config.from_yaml(str(path))
    return container
