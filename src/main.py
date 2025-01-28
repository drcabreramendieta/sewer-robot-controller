from containers import CommunicationModuleContainer
import sys
from PyQt6.QtWidgets import QApplication
from Inspection.adapters.gui.main_window import MainWindow

def run():
    """Initialize and run the application.

    Sets up dependency injection container, initializes hardware
    interfaces and launches the main application window.

    Raises:
        SystemExit: If CAN bus initialization fails
        RuntimeError: If component initialization fails

    Returns:
        None
    """
    app = QApplication(sys.argv)
    container = CommunicationModuleContainer()

    if container.bus() is None:
        MainWindow.show_error_dialog_connections()
        sys.exit(1)

    robot_link = None
    notify_video_use_case = None
    main_window = None

    robot_link = container.robot_link()
    
    notify_video_use_case = container.notify_video_use_case()
    #notify_video_use_case.start_listening()

    main_window = container.main_window()
    main_window.show()
    code = app.exec()
    #time.sleep(5)
    robot_link.stop_listening()
    notify_video_use_case.stop_listening()
    
    sys.exit(code)
    #move_robot_use_case = communication_module_container.move_robot_use_case()
    #move_robot_use_case.run('F', 100)

    #notify_telemetry_use_case = communication_module_container.notify_telemetry_use_case()
    #notify_telemetry_use_case.start_listening()

    #bus1 = can.interface.Bus('test', interface='virtual')

    #msg1 = can.Message(arbitration_id=0xabcde, data=[1,2,3])
    #bus1.send(msg1)
    #time.sleep(5)
    #bus1.shutdown()
    #notify_telemetry_use_case.stop_listening()

if __name__ == "__main__":
    run()