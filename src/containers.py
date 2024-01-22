from dependency_injector import containers, providers
from Communication.domain.use_cases.move_robot import MoveRobot
from Communication.adapters.can_bus import CANRobotLink

class CommunicationModuleContainer(containers.DeclarativeContainer):
    configuration = providers.Configuration()
    robot_link = providers.Factory(CANRobotLink)
    move_robot_use_case = providers.Factory(MoveRobot, link=robot_link)


