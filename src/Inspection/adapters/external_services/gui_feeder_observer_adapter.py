from Inspection.ports.output import FeederObserverPort
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import FeederControlData
from Inspection.adapters.gui.main_window import MainWindow
from PyQt6.QtCore import Qt

class GuiFeederObserverAdapter(FeederObserverPort):
    def __init__(self, gui:MainWindow):
        super().__init__()
        self.gui = gui

    def on_feeder_ready(self, feeder_control_data:FeederControlData) -> None:
        self.gui.latest_distance = feeder_control_data.distance
        # Construir el texto de telemetría con los últimos valores conocidos
        telemetry_text = (f"{self.gui.tr('Telemetry')}\n"
                          f"{self.gui.tr('Temperature:')} {self.gui.latest_temperature} °C \n"
                          f"{self.gui.tr('Humidity:')} {self.gui.latest_humidity} HR \n"
                          f"{self.gui.tr('X slop:')} {self.gui.latest_x_slop} °\n"
                          f"{self.gui.tr('Y slop:')} {self.gui.latest_y_slop} °\n"
                          f"{self.gui.tr('Distance:')} {self.gui.latest_distance}")

        # Actualizar la etiqueta con el texto de telemetría
        self.gui.telemetry_label.setText(telemetry_text)
        self.gui.telemetry_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        
        if (feeder_control_data.reset == "RESET"): 
            self.gui.btn_init_encoder.setDown(True)
        elif (feeder_control_data.reset == "NO"):
            self.gui.btn_init_encoder.setDown(False)

        print('Feeder data UI Controller:', feeder_control_data)