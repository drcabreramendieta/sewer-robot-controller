from dependency_injector import containers, providers

from Panel_and_Feeder.adapters.external_services.mock_serial_panel_and_feeder_controller_adapter import (
    MockSerialPanelAndFeederControllerAdapter,
)
from Panel_and_Feeder.adapters.external_services.pyqt_feeder_observer_adapter import (
    PyqtFeederObserverAdapter,
)
from Panel_and_Feeder.adapters.external_services.pyqt_panel_observer_adapter import (
    PyqtPanelObserverAdapter,
)
from Panel_and_Feeder.adapters.external_services.serial_panel_and_feeder_controller_adapter import (
    SerialPanelAndFeederControllerAdapter,
)
from Panel_and_Feeder.application.services.feeder_services import FeederServices
from Panel_and_Feeder.application.services.panel_services import PanelServices
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import SerialConfig


def _register_observers(panel_services, panel_observer, feeder_services, feeder_observer):
    panel_services.register_observer(panel_observer)
    feeder_services.register_observer(feeder_observer)
    return True


class PanelAndFeederContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    logger = providers.Dependency()
    panel_update_services = providers.Dependency()
    feeder_update_service = providers.Dependency()

    serial_config = providers.Singleton(
        SerialConfig,
        port=config.port,
        baudrate=config.baudrate,
        timeout=config.timeout,
    )
    panel_and_feeder_controller = providers.Singleton(
        SerialPanelAndFeederControllerAdapter,
        serial_conf=serial_config,
        logger=logger,
    )

    panel_services = providers.Singleton(
        PanelServices,
        paf_controller=panel_and_feeder_controller,
        logger=logger,
    )

    feeder_services = providers.Singleton(
        FeederServices,
        paf_controller=panel_and_feeder_controller,
        logger=logger,
    )

    panel_observer = providers.Singleton(
        PyqtPanelObserverAdapter,
        panel_update_services=panel_update_services,
        logger=logger,
    )
    feeder_observer = providers.Singleton(
        PyqtFeederObserverAdapter,
        feeder_update_service=feeder_update_service,
        logger=logger,
    )

    wire_observers = providers.Callable(
        _register_observers,
        panel_services=panel_services,
        panel_observer=panel_observer,
        feeder_services=feeder_services,
        feeder_observer=feeder_observer,
    )


class PanelAndFeederMockContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    logger = providers.Dependency()
    panel_update_services = providers.Dependency()
    feeder_update_service = providers.Dependency()

    serial_config = providers.Singleton(
        SerialConfig,
        port=config.port,
        baudrate=config.baudrate,
        timeout=config.timeout,
    )
    panel_and_feeder_controller = providers.Singleton(
        MockSerialPanelAndFeederControllerAdapter,
        serial_conf=serial_config,
        logger=logger,
    )

    panel_services = providers.Singleton(
        PanelServices,
        paf_controller=panel_and_feeder_controller,
        logger=logger,
    )

    feeder_services = providers.Singleton(
        FeederServices,
        paf_controller=panel_and_feeder_controller,
        logger=logger,
    )

    panel_observer = providers.Singleton(
        PyqtPanelObserverAdapter,
        panel_update_services=panel_update_services,
        logger=logger,
    )
    feeder_observer = providers.Singleton(
        PyqtFeederObserverAdapter,
        feeder_update_service=feeder_update_service,
        logger=logger,
    )

    wire_observers = providers.Callable(
        _register_observers,
        panel_services=panel_services,
        panel_observer=panel_observer,
        feeder_services=feeder_services,
        feeder_observer=feeder_observer,
    )
