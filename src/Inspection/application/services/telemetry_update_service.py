from Inspection.ports.input import TelemetryUpdateServicePort
from Communication.domain.entities.telemetry_entities import TelemetryMessage
from Inspection.ui.main_window import MainWindow
from PyQt6.QtCore import Qt

class TelemetryUpdateService(TelemetryUpdateServicePort):
    def __init__(self, gui:MainWindow):
        super().__init__()
        self.gui = gui

    def update_telemetry(self, telemetry: TelemetryMessage) -> None:
        # Actualizar los atributos con los nuevos valores si están disponibles
        self.gui.latest_temperature = telemetry.variables.get("Temperature", self.gui.latest_temperature)
        self.gui.latest_humidity = telemetry.variables.get("Humidity", self.gui.latest_humidity)
        self.gui.latest_x_slop = telemetry.variables.get("X slop", self.gui.latest_x_slop)
        self.gui.latest_y_slop = telemetry.variables.get("Y slop", self.gui.latest_y_slop)
        
        motor_status = telemetry.variables.get("Motor status", "N/A")
        

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
        #print(telemetry.variables) 
        # Actualizar el texto de advertencia basado en el estado del motor
        if motor_status == 0xC0:
            self.gui.warning_text.setText(self.tr("No warnings."))
        elif motor_status == 0xE0:
            self.gui.warning_text.setText(self.tr("Caution locked wheels."))