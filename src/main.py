from containers import CommunicationModuleContainer
import time
import can
def run():
    communication_module_container = CommunicationModuleContainer()
    move_robot_use_case = communication_module_container.move_robot_use_case()
    #move_robot_use_case.run('F', 100)

    notify_telemetry_use_case = communication_module_container.notify_telemetry_use_case()
    notify_telemetry_use_case.start_listening()

    #bus1 = can.interface.Bus('test', interface='virtual')

    #msg1 = can.Message(arbitration_id=0xabcde, data=[1,2,3])
    #bus1.send(msg1)
    time.sleep(0.75)
    #bus1.shutdown()
    notify_telemetry_use_case.stop_listening()

if __name__ == "__main__":
    run()