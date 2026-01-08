from dependency_injector import containers, providers

from Inspection.adapters.external_services.comm_camera_controller_adapter import (
    CommCameraControllerAdapter,
)
from Inspection.adapters.external_services.comm_arm_controller_adapter import (
    CommArmControllerAdapter,
)
from Inspection.adapters.external_services.comm_movement_controller_adapter import (
    CommMovementControllerAdapter,
)
from Inspection.adapters.external_services.gui_feeder_observer_adapter import (
    GuiFeederObserverAdapter,
)
from Inspection.adapters.external_services.gui_telemetry_observer_adapter import (
    GuiTelemetryObserverAdapter,
)
from Inspection.adapters.external_services.gui_video_observer_adapter import (
    GuiVideoObserverAdapter,
)
from Inspection.adapters.external_services.paf_feeder_controller_adapter import (
    PafFeederControllerAdapter,
)
from Inspection.adapters.external_services.video_session_controller_adapter import (
    VideoSessionControllerAdapter,
)
from Inspection.adapters.gui.main_window import MainWindow
from Inspection.application.services.feeder_update_service import FeederUpdateService
from Inspection.application.services.panel_update_services import PanelUpdateServices
from Inspection.application.services.session_services import SessionServices
from Inspection.application.services.telemetry_update_service import TelemetryUpdateService
from Inspection.application.services.video_update_service import VideoUpdateService


def _register_observers(
    feeder_update_service,
    gui_feeder_observer,
    telemetry_update_service,
    gui_telemetry_observer,
    video_update_service,
    gui_video_observer,
):
    feeder_update_service.register_observer(gui_feeder_observer)
    telemetry_update_service.register_observer(gui_telemetry_observer)
    video_update_service.register_observer(gui_video_observer)
    return True


class InspectionContainer(containers.DeclarativeContainer):
    logger = providers.Dependency()
    movement_service = providers.Dependency()
    camera_services = providers.Dependency()
    arm_services = providers.Dependency()
    feeder_services = providers.Dependency()
    video_session_services = providers.Dependency()

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
    comm_arm_controller = providers.Singleton(
        CommArmControllerAdapter,
        arm=arm_services,
        logger=logger,
    )
    panel_update_services = providers.Singleton(
        PanelUpdateServices,
        movement_controller=comm_movement_controller,
        camera_controller=comm_camera_controller,
        arm_controller=comm_arm_controller,
    )

    feeder_controller = providers.Singleton(
        PafFeederControllerAdapter,
        feeder_services=feeder_services,
    )

    feeder_update_service = providers.Singleton(
        FeederUpdateService,
        feeder_controller=feeder_controller,
    )
    telemetry_update_service = providers.Singleton(
        TelemetryUpdateService,
    )
    video_update_service = providers.Singleton(
        VideoUpdateService,
    )

    video_session_controller = providers.Singleton(
        VideoSessionControllerAdapter,
        control_session=video_session_services,
        logger=logger,
    )
    session_services = providers.Singleton(
        SessionServices,
        session_controller=video_session_controller,
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

    wire_observers = providers.Callable(
        _register_observers,
        feeder_update_service=feeder_update_service,
        gui_feeder_observer=gui_feeder_observer,
        telemetry_update_service=telemetry_update_service,
        gui_telemetry_observer=gui_telemetry_observer,
        video_update_service=video_update_service,
        gui_video_observer=gui_video_observer,
    )
