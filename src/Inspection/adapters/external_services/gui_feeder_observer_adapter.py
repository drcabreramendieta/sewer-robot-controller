from Inspection.ports.ouput import FeederObserverPort
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import FeederControlData
from Inspection.adapters.gui.main_window import MainWindow
from PyQt6.QtCore import Qt
"""GUI adapter for feeder observation and telemetry display.

This module provides an adapter that implements the FeederObserverPort interface
for displaying feeder telemetry data in the GUI.
"""

class GuiFeederObserverAdapter(FeederObserverPort):
    """GUI adapter for displaying feeder telemetry data.

    Args:
        gui (MainWindow): Main window instance for GUI updates

    Attributes:
        gui: Reference to main window for updating UI elements
    """
    def __init__(self, gui:MainWindow):
        """Initialize feeder observer GUI adapter."""
        super().__init__()
        self.gui = gui

    def on_feeder_ready(self, feeder_control_data:FeederControlData) -> None:
        """Update GUI with new feeder telemetry data.

        Updates telemetry display label with latest sensor values including
        temperature, humidity, slopes and distance. Also handles encoder
        reset button state based on feeder control data.

        Args:
        feeder_control_data (FeederControlData): Object containing sensor readings
            and control states for the feeder. Includes temperature, humidity,
            slope measurements, distance values and reset status.

        Returns:
            None

        Side Effects:
            - Updates GUI telemetry label with latest sensor values
            - Modifies encoder reset button state
        - Prints feeder data to console
        """
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