from dependency_injector import containers, providers
from Communication.domain.use_cases.move_robot import MoveRobot
from Communication.application.services.telemetry_services import TelemetryServices
from Communication.adapters.external_services.can_telemetry_controller_adapter import CanTelemetryControllerAdapter
from Communication.adapters.external_services.pyqt_telemetry_observer_adapter import PyqtTelemetryObserverAdapter
import can

from Inspection.ui.main_window import MainWindow
from Inspection.adapters.external_services.comm_movement_controller_adapter import CommMovementControllerAdapter
from Inspection.adapters.external_services.comm_camera_controller_adapter import CommCameraControllerAdapter 
from Communication.domain.use_cases.control_camera import ControlCamera

from Video.adapters.external_services.test_video_observer import TestVideoObserver
from Video.adapters.external_services.pyqt_video_observer_adapter import PyqtVideoObserverAdapter
from Video.adapters.external_services.opencv_video_controller_adapter import OpencvVideoControllerAdapter
from Video.application.services.video_services import VideoServices
from Video.domain.entities.video_entities import VideoMessage
from PyQt6.QtCore import pyqtSignal

from Video.adapters.external_services.hikvision_dvr_controller_adapter import HikvisionDvrControllerAdapter
from Video.adapters.repositories.tinydb_repository_adapter import TinydbRepositoryAdapter
from Video.application.services.session_services import SessionServices
from Inspection.adapters.gidtec_session_controller import GidtecSessionController
from Inspection.ui.sessions_list_dialog import SessionsListDialog

from Panel_and_Feeder.adapters.serial_panel_and_feeder_controller_adapter import SerialPanelAndFeederControllerAdapter
from Panel_and_Feeder.adapters.pyqt_feeder_observer_adapter import PyqtFeederObserverAdapter
from Panel_and_Feeder.adapters.pyqt_panel_observer_adapter import PyqtPanelObserverAdapter
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import SerialConfig
from Panel_and_Feeder.application.services.feeder_services import FeederServices
from Panel_and_Feeder.application.services.panel_services import PanelServices

import logging

def get_logger(name='app_logger'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

def create_can_bus(channel: str, interface: str, bitrate: int, logger: logging.Logger):
    try:
        return can.interface.Bus(channel=channel, interface=interface, bitrate=bitrate)
    except OSError as e:
        logger.error(f"Failed to establish communication with the CAN bus: {e}", exc_info=True)
        return None

class CommunicationModuleContainer(containers.DeclarativeContainer):
    configuration = providers.Configuration()
    logger = providers.ThreadSafeSingleton(get_logger)
    
    bus = providers.Singleton(
        create_can_bus, 
        channel='can0', 
        interface='socketcan', 
        bitrate=250000,
        logger=logger
    )
    
    robot_link = providers.Singleton(CanTelemetryControllerAdapter, bus=bus, logger=logger)
    move_robot_use_case = providers.Factory(MoveRobot, link=robot_link, logger=logger)
    robot_controller = providers.Singleton(CommMovementControllerAdapter, communication_controller=move_robot_use_case, logger=logger)
    control_camera_use_case = providers.Factory(ControlCamera, robot_link=robot_link, logger=logger)
    camera_controller = providers.Singleton(CommCameraControllerAdapter, control_camera=control_camera_use_case, logger=logger)

    telemetry_observer = providers.Factory(PyqtTelemetryObserverAdapter, logger=logger)
    notify_telemetry_use_case = providers.Singleton(TelemetryServices, link=robot_link, logger=logger)

    video_observer = providers.Factory(PyqtVideoObserverAdapter, logger=logger)
    video_link = providers.Singleton(OpencvVideoControllerAdapter, rtsp_url='rtsp://admin:inspection24@192.168.18.155:554/Streaming/Channels/101', logger=logger)
    notify_video_use_case = providers.Singleton(VideoServices, link=video_link, logger=logger)
    
    db_link = providers.Factory(TinydbRepositoryAdapter, db_name='SessionsDB.json', logger=logger)
    dvr_link = providers.Factory(HikvisionDvrControllerAdapter, url='http://192.168.18.155:80', user="admin", password="inspection24", dir="/home/iiot/Pictures", logger=logger)
    control_session_use_case = providers.Factory(SessionServices, dvr_link=dvr_link, db_link=db_link, logger=logger)
    session_controller = providers.Factory(GidtecSessionController, control_session=control_session_use_case, logger=logger)

    serial_conf = providers.Factory(SerialConfig, port='/dev/ttyACM0', baudrate=115200, timeout=0.1)
    peripheral_link = providers.Singleton(SerialPanelAndFeederControllerAdapter, serial_conf=serial_conf, logger=logger)
    panel_observer = providers.Factory(PyqtPanelObserverAdapter, logger=logger)
    panel_notifier = providers.Factory(PanelServices, link=peripheral_link, logger=logger)
    feeder_observer = providers.Factory(PyqtFeederObserverAdapter, logger=logger)
    feeder_notifier = providers.Factory(FeederServices, link=peripheral_link, logger=logger)

    main_window = providers.Singleton(MainWindow, 
                                      robot_controller=robot_controller,
                                      camera_controller=camera_controller,
                                      video_observer=video_observer,
                                      video_notifier=notify_video_use_case,
                                      telemetry_observer=telemetry_observer,
                                      telemetry_notifier=notify_telemetry_use_case,
                                      session_controller=session_controller,
                                      panel_observer=panel_observer,
                                      panel_notifier=panel_notifier,
                                      feeder_observer=feeder_observer,
                                      feeder_notifier=feeder_notifier)
