from dependency_injector import containers, providers
from Communication.domain.use_cases.move_robot import MoveRobot
from Communication.domain.use_cases.notify_telemetry import NotifyTelemetry
from Communication.adapters.can_bus import CANRobotLink
from Communication.adapters.test_observer import TestTelemetryObserver
import can

from Inspection.ui.main_window import MainWindow
from Inspection.adapters.gidtec_robot_controller import GidtecRobotController
from Inspection.adapters.gidtec_camera_controller import GidtecCameraController 
from Communication.domain.use_cases.control_camera import ControlCamera

from Video.adapters.test_video_observer import TestVideoObserver
from Inspection.adapters.qt_video_observer import QtVideoObserver
from Video.adapters.opencv_video_link import OpenCVVideoLink
from Video.domain.use_cases.video_notifier import VideoNotifier
from Video.domain.entities import VideoMessage
from PyQt6.QtCore import pyqtSignal


class CommunicationModuleContainer(containers.DeclarativeContainer):
    configuration = providers.Configuration()
    #bus = providers.Singleton(can.interface.Bus, device_id=0, interface='pcan', bitrate=1000000)
    bus = providers.Singleton(can.interface.Bus, channel='test', interface='virtual', bitrate=1000000)
    robot_link = providers.Singleton(CANRobotLink, bus=bus)
    move_robot_use_case = providers.Factory(MoveRobot, link=robot_link)
    robot_controller = providers.Singleton(GidtecRobotController, communication_controller=move_robot_use_case)
    control_camera_use_case = providers.Factory(ControlCamera, robot_link=robot_link)
    camera_controller = providers.Singleton(GidtecCameraController, control_camera=control_camera_use_case)

    telemetry_observer = providers.Factory(TestTelemetryObserver)
    list_observers = providers.List(telemetry_observer, telemetry_observer, telemetry_observer)
    notify_telemetry_use_case = providers.Factory(NotifyTelemetry,telemetry_observers=list_observers, link=robot_link)

    video_observer = providers.Factory(QtVideoObserver)
    video_link = providers.Singleton(OpenCVVideoLink, rtsp_url='/home/diego/robot/Terminal/src/example.mp4')
    notify_video_use_case = providers.Singleton(VideoNotifier, link=video_link)
    main_window = providers.Singleton(MainWindow, robot_controller=robot_controller,camera_controller=camera_controller, video_observer=video_observer, video_notifier=notify_video_use_case)
