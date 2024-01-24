from Communication.ports.link import RobotLink
from Communication.domain.entities import WheelsModule, Telemetry, WheelInformation
from typing import Callable
import can

class CANRobotLink(RobotLink):
    def __init__(self, bus:can.Bus) -> None:
        self.callback = None
        self.notifier = None
        self.bus = bus

    def send(self, wheelsModuleLeft:WheelsModule, wheelsModuleRight:WheelsModule) -> None:
        # Get the speed message to the wheels modules considering the side. There are two ranges of values 
        # depending on the direction of rotation. The first goes ascending from 0x0000 to 0x7FFE, being 0% 
        # and 100% respectively. The second goes descending from 0xFFFF to 0x8000, being 0% and 100%, 
        # respectively.        
            
            if wheelsModuleLeft.direction == "F":
                speed_left = f'{int((wheelsModuleLeft.speed / 100) * 0x7FFE):016b}'
            elif wheelsModuleLeft.direction == "R":
                speed_left = f'{int((wheelsModuleLeft.speed / 100) * 0x7FFE):016b}'
            elif wheelsModuleLeft.direction == "L":
                speed_left = f'{int((100 - wheelsModuleLeft.speed) / 100 * (0xFFFF - 0x8000)) + 0x8000:016b}'
            elif wheelsModuleLeft.direction == "B":
                speed_left = f'{int((100 - wheelsModuleLeft.speed) / 100 * (0xFFFF - 0x8000)) + 0x8000:016b}'
            elif wheelsModuleLeft.direction == "S":
                speed_left = f'{0:016b}'
            
            if wheelsModuleRight.direction == "F":
                speed_right = f'{int((100 - wheelsModuleLeft.speed) / 100 * (0xFFFF - 0x8000)) + 0x8000:016b}'
            elif wheelsModuleRight.direction == "R":
                speed_right = f'{int((wheelsModuleRight.speed / 100) * 0x7FFE):016b}'
            elif wheelsModuleRight.direction == "L":
                speed_right = f'{int((100 - wheelsModuleLeft.speed) / 100 * (0xFFFF - 0x8000)) + 0x8000:016b}'
            elif wheelsModuleRight.direction == "B":
                speed_right = f'{int((wheelsModuleRight.speed / 100) * 0x7FFE):016b}'
            elif wheelsModuleRight.direction == "S":
                speed_right = f'{0:016b}' 

            speed_left_data0 = int(speed_left[:8],2)
            speed_left_data1 = int(speed_left[8:],2)
            
            speed_right_data0 = int(speed_right[:8],2)
            speed_right_data1 = int(speed_right[8:],2)
            

            m1 = [speed_left_data0, speed_left_data1, speed_left_data0, speed_left_data1, \
                  speed_left_data0, speed_left_data1, speed_right_data0, speed_right_data1]
            m2 = [speed_right_data0, speed_right_data1, speed_right_data0, speed_right_data1,\
                  0, 0, 0, 0]
            

        #Configure CAN protocol communication 
            try:
                bus = can.interface.Bus(device_id=0, interface='socketcan')
                message1 = can.Message(arbitration_id=0x0202, data=m1)
                message2 = can.Message(arbitration_id=0x0203, data=m2)
                
                bus.send(message1)
                bus.send(message2)

                print('Mensaje enviado')
                print(message1.data)
                print(message2.data)

            except can.CanError as e:
                print(f"Error CAN: {e}")
        
            finally:
                if 'bus' in locals():
                    bus.shutdown()
            

            
            
                
            

            
            

    def callback_setup(self, callback:Callable[[Telemetry], None]) -> None:
        self.callback = callback

    def start_listening(self) -> None:
        self.notifier = can.Notifier(bus=self.bus,listeners=[self._can_message_handler],timeout=2)

    def stop_listening(self) -> None:
        self.notifier.bus.shutdown()

    def _can_message_handler(self,message:can.Message):
        print(message)
        w1 = WheelInformation(10,30)
        w2 = WheelInformation(30,40)
        w_list = list()
        w_list.append(w1)
        w_list.append(w2)
        self.callback(Telemetry(20,20,w_list))
