from dependency_injector import containers, providers
from Communication.domain.use_cases.move_robot import MoveRobot
from Communication.domain.use_cases.notify_telemetry import NotifyTelemetry
from Communication.adapters.can_bus import CANRobotLink
from Communication.adapters.test_observer import TestTelemetryObserver
import can

from Inspection.ui.main_window import MainWindow
from Inspection.adapters.gidtec_robot_controller import GidtecRobotController

class CommunicationModuleContainer(containers.DeclarativeContainer):
    configuration = providers.Configuration()
    bus = providers.Singleton(can.interface.Bus, device_id=0, interface='pcan', bitrate=1000000)
    robot_link = providers.Singleton(CANRobotLink, bus=bus)
    move_robot_use_case = providers.Factory(MoveRobot, link=robot_link)
    robot_controller = providers.Singleton(GidtecRobotController, communication_controller=move_robot_use_case)
    main_window = providers.Singleton(MainWindow, robot_controller=robot_controller)

    telemetry_observer = providers.Factory(TestTelemetryObserver)
    list_observers = providers.List(telemetry_observer, telemetry_observer, telemetry_observer)
    
    notify_telemetry_use_case = providers.Factory(NotifyTelemetry,telemetry_observers=list_observers, link=robot_link)

