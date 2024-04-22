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

from Video.adapters.hikvision_dvr_link import HikvisionDvrLink
from Video.adapters.tiny_db_link import TinyDbLink
from Video.domain.use_cases.control_session import ControlSession
from Inspection.adapters.gidtec_session_controller import GidtecSessionController
from Inspection.ui.sessions_list_dialog import SessionsListDialog

from Panel_and_Feeder.adapters.serial_peripheral_link import SerialPeripheralLink
from Panel_and_Feeder.adapters.qt_feeder_observer import QtFeederObserver
from Panel_and_Feeder.adapters.qt_panel_observer import QtPanelObserver
from Panel_and_Feeder.domain.entities import SerialConfig
from Panel_and_Feeder.domain.feeder_notifier import FeederNotifier
from Panel_and_Feeder.domain.panel_notifier import PanelNotifier

class CommunicationModuleContainer(containers.DeclarativeContainer):
    configuration = providers.Configuration()
    bus = providers.Singleton(can.interface.Bus, channel='can0', interface='socketcan', bitrate=250000)
    #bus = providers.Singleton(can.interface.Bus, channel='test', interface='virtual', bitrate=1000000)
    robot_link = providers.Singleton(CANRobotLink, bus=bus)
    move_robot_use_case = providers.Factory(MoveRobot, link=robot_link)
    robot_controller = providers.Singleton(GidtecRobotController, communication_controller=move_robot_use_case)
    control_camera_use_case = providers.Factory(ControlCamera, robot_link=robot_link)
    camera_controller = providers.Singleton(GidtecCameraController, control_camera=control_camera_use_case)

    telemetry_observer = providers.Factory(TestTelemetryObserver)
    notify_telemetry_use_case = providers.Singleton(NotifyTelemetry, link=robot_link)

    video_observer = providers.Factory(QtVideoObserver)
    video_link = providers.Singleton(OpenCVVideoLink, rtsp_url='rtsp://admin:inspection24@192.168.18.155:554/Streaming/Channels/101')
    #video_link = providers.Singleton(OpenCVVideoLink, rtsp_url='/home/dcabrera/UPS/Terminal/src/example.mp4')
    notify_video_use_case = providers.Singleton(VideoNotifier, link=video_link)
    
    db_link = providers.Factory(TinyDbLink, db_name='SessionsDB.json')
    dvr_link = providers.Factory(HikvisionDvrLink, url='http://192.168.18.155:80', user="admin", password="inspection24", dir="/home/iiot/Pictures")
    control_session_use_case = providers.Factory(ControlSession, dvr_link=dvr_link, db_link=db_link)
    session_controller = providers.Factory(GidtecSessionController, control_session=control_session_use_case)

    serial_conf = providers.Factory(SerialConfig, port='/dev/ttyACM0', baudrate=115200, timeout=0.1)
    peripheral_link = providers.Singleton(SerialPeripheralLink, serial_conf=serial_conf)
    panel_observer = providers.Factory(QtPanelObserver)
    panel_notifier = providers.Factory(PanelNotifier, link=peripheral_link)
    feeder_observer = providers.Factory(QtFeederObserver)
    feeder_notifier = providers.Factory(FeederNotifier, link=peripheral_link)

    main_window = providers.Singleton(MainWindow, robot_controller=robot_controller,camera_controller=camera_controller, video_observer=video_observer, video_notifier=notify_video_use_case, telemetry_observer=telemetry_observer, telemetry_notifier=notify_telemetry_use_case, session_controller=session_controller,  panel_observer=panel_observer, panel_notifier=panel_notifier, feeder_observer=feeder_observer, feeder_notifier=feeder_notifier)
    