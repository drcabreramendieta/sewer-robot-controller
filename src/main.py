from containers import CommunicationModuleContainer
def run():
    communication_module_container = CommunicationModuleContainer()
    move_robot_use_case = communication_module_container.move_robot_use_case()
    move_robot_use_case.run('F', 100)

if __name__ == "__main__":
    run()