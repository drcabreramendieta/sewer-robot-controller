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

# Para funciones de diagnosis
from Inspection.adapters.external_services.vision_fastapi_diagnosis_controller_adapter import (
    VisionFastApiDiagnosisControllerAdapter,
)
from Inspection.adapters.external_services.mock_vision_fastapi_diagnosis_controller_adapter import (
    MockVisionFastApiDiagnosisControllerAdapter,
)
from Inspection.adapters.eventing.qt_diagnosis_event_publisher_adapter import (
    QtDiagnosisEventPublisherAdapter,
)
from Inspection.adapters.gui.gui_diagnosis_observer_adapter import (
    GuiDiagnosisObserverAdapter,
)

from Inspection.application.services.diagnosis_services import DiagnosisServices
from Inspection.adapters.eventing.diagnosis_event_notifier import DiagnosisEventNotifier
from Inspection.application.services.diagnosis_sessions_registry import DiagnosisSessionsRegistry, DiagnosisSessionEntry


def _register_observers(
    feeder_update_service,
    gui_feeder_observer,
    telemetry_update_service,
    gui_telemetry_observer,
    video_update_service,
    gui_video_observer,
    diagnosis_event_notifier,   # Diagnosis
    gui_diagnosis_observer,     # Diagnosis
):
    feeder_update_service.register_observer(gui_feeder_observer)
    telemetry_update_service.register_observer(gui_telemetry_observer)
    video_update_service.register_observer(gui_video_observer)

    diagnosis_event_notifier.register_observer(gui_diagnosis_observer)  # Diagnosis
    return True


class InspectionContainer(containers.DeclarativeContainer):
    vision = providers.Configuration()   # Diagnosis
    logger = providers.Dependency()
    movement_service = providers.Dependency()
    camera_services = providers.Dependency()
    arm_services = providers.Dependency()
    feeder_services = providers.Dependency()
    video_session_services = providers.Dependency()
    selector_signal = providers.Dependency()
    config = providers.Dependency()  # <-- NUEVO para configuración general


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
        arm_service=arm_services,
        logger=logger,
    )
    panel_update_services = providers.Singleton(
        PanelUpdateServices,
        movement_controller=comm_movement_controller,
        camera_controller=comm_camera_controller,
        arm_controller=comm_arm_controller,
        selector_signal=selector_signal,
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

    # Providers para Diagnosis services

    diagnosis_event_notifier = providers.Singleton(
        DiagnosisEventNotifier,
    )

    diagnosis_event_publisher = providers.Singleton(
        QtDiagnosisEventPublisherAdapter,
        diagnosis_event_notifier=diagnosis_event_notifier,
    )

    diagnosis_controller_real = providers.Singleton(
        VisionFastApiDiagnosisControllerAdapter,
        base_url=vision.base_url,
        ws_base_url=vision.ws_base_url,
        timeout_seconds=vision.timeout_seconds,
        event_publisher=diagnosis_event_publisher,
        logger=logger,
    )

    diagnosis_controller_mock = providers.Singleton(
        MockVisionFastApiDiagnosisControllerAdapter,
        event_publisher=diagnosis_event_publisher,
        logger=logger,
    )

    diagnosis_controller = providers.Selector(
        vision.mode,  # "real" o "mock"
        real=diagnosis_controller_real,
        mock=diagnosis_controller_mock,
    )

    # Nuevo provider para DiagnosisSessionsRegistry (Manejo información de sesiones de diagnóstico)
    diagnosis_sessions_registry = providers.Singleton(
        DiagnosisSessionsRegistry,
        path=vision.sessions_registry_path,
    )


    diagnosis_services = providers.Singleton(
        DiagnosisServices,
        controller=diagnosis_controller,
        logger=logger,
        diagnosis_sessions_registry=diagnosis_sessions_registry,    # Agregamos el diagnosis_sessions_registry
        model_id_from_config=vision.model_id,   # Agregamos el model_id desde configuración
        report_artifacts_dir=vision.report_artifacts_dir,  # Usar de manera opcional
    )
    # Fin Providers para Diagnosis services

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
        diagnosis_services=diagnosis_services,
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
    
    # Providers para Diagnosis GUI observer. Agregamos el observer de diagnosis para el GUI
    gui_diagnosis_observer = providers.Singleton(
        GuiDiagnosisObserverAdapter,
        gui=main_window,
    )
    # Fin Providers para Diagnosis GUI observer


    wire_observers = providers.Callable(
        _register_observers,
        feeder_update_service=feeder_update_service,
        gui_feeder_observer=gui_feeder_observer,
        telemetry_update_service=telemetry_update_service,
        gui_telemetry_observer=gui_telemetry_observer,
        video_update_service=video_update_service,
        gui_video_observer=gui_video_observer,
        diagnosis_event_notifier=diagnosis_event_notifier,  # Diagnosis
        gui_diagnosis_observer=gui_diagnosis_observer,      # Diagnosis
    )
