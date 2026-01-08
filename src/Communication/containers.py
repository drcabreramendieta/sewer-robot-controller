from dependency_injector import containers, providers

from Communication.adapters.external_services.can_camera_controller_adapter import (
    CanCameraControllerAdapter,
)
from Communication.adapters.external_services.can_arm_controller_adapter import (
    CanArmControllerAdapter,
)
from Communication.adapters.external_services.can_telemetry_controller_adapter import (
    CanTelemetryControllerAdapter,
)
from Communication.adapters.external_services.can_wheels_controller_adapter import (
    CanWheelsControllerAdapter,
)
from Communication.adapters.external_services.mock_can_camera_controller_adapter import (
    MockCanCameraControllerAdapter,
)
from Communication.adapters.external_services.mock_can_telemetry_controller_adapter import (
    MockCanTelemetryControllerAdapter,
)
from Communication.adapters.external_services.mock_can_wheels_controller_adapter import (
    MockCanWheelsControllerAdapter,
)
from Communication.adapters.external_services.pyqt_telemetry_observer_adapter import (
    PyqtTelemetryObserverAdapter,
)
from Communication.application.services.camera_services import CameraServices
from Communication.application.services.movement_service import MovementService
from Communication.application.services.telemetry_services import TelemetryServices
from Communication.application.services.arm_services import ArmServices


def _register_observer(service, observer):
    service.register_observer(observer)
    return True


class CommunicationContainer(containers.DeclarativeContainer):
    logger = providers.Dependency()
    can_bus = providers.Dependency()
    telemetry_update_service = providers.Dependency()

    wheels_controller = providers.Singleton(
        CanWheelsControllerAdapter,
        bus=can_bus,
        logger=logger,
    )
    camera_controller = providers.Singleton(
        CanCameraControllerAdapter,
        bus=can_bus,
        logger=logger,
    )

    arm_controller = providers.Singleton(
        CanArmControllerAdapter,
        bus=can_bus,
        logger=logger,
    )

    telemetry_controller = providers.Singleton(
        CanTelemetryControllerAdapter,
        bus=can_bus,
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

    arm_services = providers.Singleton(
        ArmServices,
        arm_controller=arm_controller,
    )

    telemetry_services = providers.Singleton(
        TelemetryServices,
        telemetry_controller=telemetry_controller,
        logger=logger,
    )

    telemetry_observer = providers.Singleton(
        PyqtTelemetryObserverAdapter,
        telemetry_update_service=telemetry_update_service,
        logger=logger,
    )

    wire_observers = providers.Callable(
        _register_observer,
        service=telemetry_services,
        observer=telemetry_observer,
    )


class CommunicationMockContainer(containers.DeclarativeContainer):
    logger = providers.Dependency()
    telemetry_update_service = providers.Dependency()

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

    telemetry_services = providers.Singleton(
        TelemetryServices,
        telemetry_controller=telemetry_controller,
        logger=logger,
    )

    telemetry_observer = providers.Singleton(
        PyqtTelemetryObserverAdapter,
        telemetry_update_service=telemetry_update_service,
        logger=logger,
    )

    wire_observers = providers.Callable(
        _register_observer,
        service=telemetry_services,
        observer=telemetry_observer,
    )
