from Inspection.ports.input import PanelUpdateServicesPort
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import RobotControlData, CameraControlData
from Inspection.ports.ouput import MovementControllerPort, CameraControllerPort

class PanelUpdateServices(PanelUpdateServicesPort):
    """Service for coordinating robot and camera control operations.
    
    PanelUpdateServices This module provides services for coordinating robot movement and
    camera control operations through a unified interface.

    Args:
        PanelUpdateServicesPort (PanelUpdateServicesPort): Base interface defining panel control operations
    """    
    def __init__(self, movement_controller:MovementControllerPort, camera_controller:CameraControllerPort):
        """Initialize panel update service.

        Args:
            movement_controller (MovementControllerPort): Interface for robot movement control
            camera_controller (CameraControllerPort): Interface for camera operations control
        """        
        super().__init__()
        self.movement_controller = movement_controller
        self.camera_controller = camera_controller

    def update_robot_control(self, robot_control_data:RobotControlData) -> None:
        """Update robot movement based on control input.
        update_robot_control Processes direction commands and triggers corresponding
        movement controller operations.

        Args:
            robot_control_data (RobotControlData): Contains movement direction command
        """        
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
        """Update robot movement speed.
        
        Sets the movement speed for robot operations. Speed values
        are constrained between 3-1000, where 3 is minimum speed
        and 1 is maximum speed.

        Args:
            speed (int): New speed value to set
        """        
        self.movement_controller.change_speed(value=speed)

    def update_camera_control(self, camera_control_data:CameraControlData) -> None:
        """Update camera position and focus based on control input.
        
        update_camera_control Processes camera movement commands for pan, tilt and focus operations.
        

        Args:
            camera_control_data (CameraControlData):  Contains camera movement and light settings
        """        
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
        elif (camera_control_data.movement == "STOP"): 
            self.camera_controller.tilt_stop()
            self.camera_controller.pan_stop()
            self.camera_controller.focus_stop()
        
        
        if (int(camera_control_data.light) >= 90):
            camera_control_data.light = "100"
        elif (int(camera_control_data.light) <= 10):
            camera_control_data.light = "0"

        # TODO: Update slider with new light value from panel self.gui.slider_light.setValue(int(camera_control_data.light))

        print('Camera data UI Controller:', camera_control_data)

    def update_camera_light(self, light:int):
        """Update camera light intensity.
        
        update_camera_light Controls the camera's illumination system by setting the light
        intensity level. Values are expected to be between 0-100,
        where 0 is off and 100 is maximum brightness.

        Args:
            light (int): New light intensity value
        """        
        self.camera_controller.change_light(value=light)