from Inspection.ports.ouput import TelemetryObserverPort
from Communication.domain.entities.telemetry_entities import TelemetryMessage
from Inspection.adapters.gui.main_window import MainWindow
from PyQt6.QtCore import Qt

class GuiTelemetryObserverAdapter(TelemetryObserverPort):
    """GUI adapter for displaying telemetry data.

    This class handles updating the GUI elements with new telemetry data
    including sensor readings and motor status warnings.

    Args:
        gui (MainWindow): Main window instance for GUI updates

    Attributes:
        gui: Reference to main window for updating UI elements
    """

    def __init__(self, gui:MainWindow):
        """Initialize the GUI telemetry observer.

        Args:
            gui (MainWindow): Main window instance for GUI updates.
        """
        super().__init__()
        self.gui = gui

    def on_telemetry_ready(self, telemetry:TelemetryMessage) -> None:
        """Update GUI with new telemetry data.

        Handles incoming telemetry messages by updating the GUI display with new sensor values
        and motor status information. Updates temperature, humidity, slope angles, and distance
        readings in the telemetry label. Also sets appropriate warning messages based on motor 
        status.

        Args:
            telemetry (TelemetryMessage): Incoming telemetry message containing sensor data
                and motor status information in its variables dictionary. Expected keys:
                'Temperature', 'Humidity', 'X slop', 'Y slop', 'Motor status'.
        """

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