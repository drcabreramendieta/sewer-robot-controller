from dependency_injector import containers, providers
from Communication.domain.use_cases.move_robot import MoveRobot
from Communication.domain.use_cases.notify_telemetry import NotifyTelemetry
from Communication.adapters.can_bus import CANRobotLink
from Communication.adapters.test_observer import TestTelemetryObserver
import can

class CommunicationModuleContainer(containers.DeclarativeContainer):
    configuration = providers.Configuration()
    bus = providers.Singleton(can.interface.Bus, channel='test', interface='virtual')
    robot_link = providers.Singleton(CANRobotLink, bus=bus)
    move_robot_use_case = providers.Factory(MoveRobot, link=robot_link)
    
    telemetry_observer = providers.Factory(TestTelemetryObserver)
    list_observers = providers.List(telemetry_observer, telemetry_observer, telemetry_observer)
    
    notify_telemetry_use_case = providers.Factory(NotifyTelemetry,telemetry_observers=list_observers, link=robot_link)
