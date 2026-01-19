from Inspection.ports.input import PanelUpdateServicesPort
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import RobotControlData, CameraControlData, ArmControlData
from Inspection.ports.ouput import MovementControllerPort, CameraControllerPort, ArmControllerPort

class PanelUpdateServices(PanelUpdateServicesPort):
    def __init__(self, movement_controller:MovementControllerPort, camera_controller:CameraControllerPort, arm_controller: ArmControllerPort):
        super().__init__()
        self.movement_controller = movement_controller
        self.camera_controller = camera_controller
        self.arm_controller = arm_controller

    def update_robot_control(self, robot_control_data:RobotControlData) -> None:
        if (robot_control_data.direction == "F"):
            print("Mover hacia adelante")
            self.movement_controller.move_forward()
        elif (robot_control_data.direction == "FR"):
            print("Mover hacia adelante derecha")
            self.movement_controller.rotate_right_forward()
        elif (robot_control_data.direction == "FL"):
            print("Mover hacia adelante izquierda")
            self.movement_controller.rotate_left_forward()
        elif (robot_control_data.direction == "B"):
            print("Mover hacia atrás")
            self.movement_controller.move_backward()
        elif (robot_control_data.direction == "BL"):
            print("Mover hacia atrás izquierda")
            self.movement_controller.rotate_left_backward()
        elif (robot_control_data.direction == "BR"):
            print("Mover hacia atrás derecha")
            self.movement_controller.rotate_right_backward()
        elif (robot_control_data.direction == "STOP"):
            print("Detener")
            self.movement_controller.stop()
            
        print('Robot data UI Controller:', robot_control_data)

    def update_robot_speed(self, speed:int):
        self.movement_controller.change_speed(value=speed)

    def update_camera_control(self, camera_control_data:CameraControlData) -> None:
        if (camera_control_data.movement == "INIT"):
            self.camera_controller.init_camera()
        elif (camera_control_data.movement == "TU"):
            self.camera_controller.tilt_up()
        elif (camera_control_data.movement == "TD"): 
            self.camera_controller.tilt_down()
        elif (camera_control_data.movement == "PL"): 
            self.camera_controller.pan_left()
        elif (camera_control_data.movement == "PR"): 
            self.camera_controller.pan_right()
        elif (camera_control_data.movement == "FI"):
            self.camera_controller.focus_in()
        elif (camera_control_data.movement == "FO"):
            self.camera_controller.focus_out()
        elif (camera_control_data.movement == "ZI"):
            self.camera_controller.zoom_in()
        elif (camera_control_data.movement == "ZO"):
            self.camera_controller.zoom_out()
        elif (camera_control_data.movement == "STOP"): 
            self.camera_controller.tilt_stop()
            self.camera_controller.pan_stop()
            self.camera_controller.focus_stop()
            self.camera_controller.zoom_stop()
        

        if (int(camera_control_data.light) >= 90):
            camera_control_data.light = "100"
        elif (int(camera_control_data.light) <= 10):
            camera_control_data.light = "0"

        # TODO: Update slider with new light value from panel self.gui.slider_light.setValue(int(camera_control_data.light))

        print('Camera data UI Controller:', camera_control_data)

    def update_arm_control(self, arm_control_data: ArmControlData) -> None:
        if arm_control_data.movement == "UP":
            self.arm_controller.arm_up()
        elif arm_control_data.movement == "DOWN":
            self.arm_controller.arm_down()
        elif arm_control_data.movement == "STOP":
            self.arm_controller.arm_stop()

        print("Arm data UI Controller:", arm_control_data)



    def update_camera_light(self, light:int):
        self.camera_controller.change_light(value=light)