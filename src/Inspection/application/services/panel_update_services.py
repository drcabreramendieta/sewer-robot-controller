from Inspection.ports.input import PanelUpdateServicesPort
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import RobotControlData, CameraControlData
from Inspection.ui.main_window import MainWindow
from Inspection.ports.ouput import MovementControllerPort, CameraControllerPort

class PanelUpdateServices(PanelUpdateServicesPort):
    def __init__(self, gui:MainWindow, movement_controller:MovementControllerPort, camera_controller:CameraControllerPort):
        super().__init__()
        self.gui = gui
        self.movement_controller = movement_controller
        self.camera_controller = camera_controller

    def update_robot_control(self, robot_control_data:RobotControlData) -> None:
        if (robot_control_data.direction == "F"):
            print("Mover hacia adelante")
            self.movement_controller.move_forward()
            self.gui.btn_forward.setDown(True)
            self.gui.btn_right_forward.setDown(False)
            self.gui.btn_left_forward.setDown(False)
            self.gui.btn_backward.setDown(False)
            self.gui.btn_left_backward.setDown(False)
            self.gui.btn_right_backward.setDown(False)
        elif (robot_control_data.direction == "FR"):
            print("Mover hacia adelante derecha")
            self.movement_controller.rotate_right_forward()
            self.gui.btn_forward.setDown(False)
            self.gui.btn_right_forward.setDown(True)
            self.gui.btn_left_forward.setDown(False)
            self.gui.btn_backward.setDown(False)
            self.gui.btn_left_backward.setDown(False)
            self.gui.btn_right_backward.setDown(False)
        elif (robot_control_data.direction == "FL"):
            print("Mover hacia adelante izquierda")
            self.movement_controller.rotate_left_forward()
            self.gui.btn_forward.setDown(False)
            self.gui.btn_right_forward.setDown(False)
            self.gui.btn_left_forward.setDown(True)
            self.gui.btn_backward.setDown(False)
            self.gui.btn_left_backward.setDown(False)
            self.gui.btn_right_backward.setDown(False)
        elif (robot_control_data.direction == "B"):
            print("Mover hacia atrás")
            self.movement_controller.move_backward()
            self.gui.btn_forward.setDown(False)
            self.gui.btn_right_forward.setDown(False)
            self.gui.btn_left_forward.setDown(False)
            self.gui.btn_backward.setDown(True)
            self.gui.btn_left_backward.setDown(False)
            self.gui.btn_right_backward.setDown(False)
        elif (robot_control_data.direction == "BL"):
            print("Mover hacia atrás izquierda")
            self.movement_controller.rotate_left_backward()
            self.gui.btn_forward.setDown(False)
            self.gui.btn_right_forward.setDown(False)
            self.gui.btn_left_forward.setDown(False)
            self.gui.btn_backward.setDown(False)
            self.gui.btn_left_backward.setDown(True)
            self.gui.btn_right_backward.setDown(False)
        elif (robot_control_data.direction == "BR"):
            print("Mover hacia atrás derecha")
            self.movement_controller.rotate_right_backward()
            self.gui.btn_forward.setDown(False)
            self.gui.btn_right_forward.setDown(False)
            self.gui.btn_left_forward.setDown(False)
            self.gui.btn_backward.setDown(False)
            self.gui.btn_left_backward.setDown(False)
            self.gui.btn_right_backward.setDown(True)
        elif (robot_control_data.direction == "STOP"):
            print("Detener")
            self.movement_controller.stop()
            self.gui.btn_forward.setDown(False)
            self.gui.btn_right_forward.setDown(False)
            self.gui.btn_left_forward.setDown(False)
            self.gui.btn_backward.setDown(False)
            self.gui.btn_left_backward.setDown(False)
            self.gui.btn_right_backward.setDown(False)
            
        print('Robot data UI Controller:', robot_control_data)

    def update_robot_speed(self, speed:int):
        self.movement_controller.change_speed(value=speed)

    def update_camera_control(self, camera_control_data:CameraControlData) -> None:
        if (camera_control_data.movement == "INIT"):
            self.camera_controller.init_camera()
        elif (camera_control_data.movement == "TU"):
            self.camera_controller.tilt_up()
            self.gui.btn_tilt_up.setDown(True)
            self.gui.btn_tilt_down.setDown(False)
            self.gui.btn_pan_left.setDown(False)
            self.gui.btn_pan_right.setDown(False)
        elif (camera_control_data.movement == "TD"): 
            self.camera_controller.tilt_down()
            self.gui.btn_tilt_up.setDown(False)
            self.gui.btn_tilt_down.setDown(True)
            self.gui.btn_pan_left.setDown(False)
            self.gui.btn_pan_right.setDown(False)
        elif (camera_control_data.movement == "PL"): 
            self.camera_controller.pan_left()
            self.gui.btn_tilt_up.setDown(False)
            self.gui.btn_tilt_down.setDown(False)
            self.gui.btn_pan_left.setDown(True)
            self.gui.btn_pan_right.setDown(False)
        elif (camera_control_data.movement == "PR"): 
            self.camera_controller.pan_right()
            self.gui.btn_tilt_up.setDown(False)
            self.gui.btn_tilt_down.setDown(False)
            self.gui.btn_pan_left.setDown(False)
            self.gui.btn_pan_right.setDown(True)
        elif (camera_control_data.movement == "FI"):
            self.camera_controller.focus_in()
        elif (camera_control_data.movement == "FO"):
            self.camera_controller.focus_out()
        elif (camera_control_data.movement == "STOP"): 
            self.camera_controller.tilt_stop()
            self.camera_controller.pan_stop()
            self.camera_controller.focus_stop()
            self.gui.btn_tilt_up.setDown(False)
            self.gui.btn_tilt_down.setDown(False)
            self.gui.btn_pan_left.setDown(False)
            self.gui.btn_pan_right.setDown(False)
        
        
        if (int(camera_control_data.light) >= 90):
            camera_control_data.light = "100"
        elif (int(camera_control_data.light) <= 10):
            camera_control_data.light = "0"

        self.gui.slider_light.setValue(int(camera_control_data.light))

        print('Camera data UI Controller:', camera_control_data)

    def update_camera_light(self, light:int):
        self.camera_controller.change_light(value=light)