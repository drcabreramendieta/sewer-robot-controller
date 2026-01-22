from PyQt6.QtCore import Qt, QSize, QTranslator, QFile
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QGridLayout, QPushButton, QWidget, QSlider, QLabel, QHBoxLayout, QCheckBox, QComboBox, QApplication, QTextEdit, QMessageBox, QLineEdit
from PyQt6.QtGui import QIcon
from Inspection.adapters.gui.session_name_dialog import SessionNameDialog
from Inspection.adapters.gui.sessions_list_dialog import SessionsListDialog
from Panel_and_Feeder.domain.entities.panel_and_feeder_entities import RobotControlData, CameraControlData, ArmControlData

from Inspection.ports.input import PanelUpdateServicesPort, SessionServicesPort, FeederUpdateServicePort, DiagnosisServicesPort

class MainWindow(QMainWindow):
    _error_dialog_instance = None
    
    def __init__(self, panel_services: PanelUpdateServicesPort, feeder_services:FeederUpdateServicePort, session_services:SessionServicesPort, diagnosis_services: DiagnosisServicesPort) -> None:
        super().__init__()
        self.latest_temperature = "N/A"
        self.latest_humidity = "N/A"
        self.latest_x_slop = "N/A"
        self.latest_y_slop = "N/A"
        self.latest_distance = "N/A"
        self.panel_services = panel_services
        self.session_services = session_services
        self.feeder_services = feeder_services
        self.diagnosis_services = diagnosis_services
        self.operator_name = None
        self.location_name = "N/A"  # puedes cambiarlo luego (config/UI)


        self.translator = QTranslator(self)
        self.SessionState = False  
        self.isRecording = False
              
        self.disply_width = 720
        self.display_height = 480
        self.disply_width_telemetry = 720
        self.display_height_telemetry = 402
        
        self.init_ui()
        self.setup_connections()
        self.load_translation("es")

        self.set_diag_controls_state(running=False) # Para manejar el bloque / estado de los botones de diagnóstico
        
    
    def init_ui(self):
        self._expansion_widgets = []
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        main_layout = QHBoxLayout()
        
        video_telemetry_layout = QVBoxLayout()
        self.image_label = QLabel()
        self.image_label.setFixedSize(720, 450)
        video_telemetry_layout.addWidget(self.image_label)
        
        
        record_layout = QHBoxLayout()  
        self.record_button = QPushButton(self.tr("Start Record")) 
        self.record_button.setIcon(QIcon("src/Inspection/Icons/record.png"))
        self.record_button.setIconSize(QSize(45,20))
        self.record_button.setEnabled(False)
        self.capture_button = QPushButton(self.tr("Capture Image")) 
        self.capture_button.setIcon(QIcon("src/Inspection/Icons/capture.png"))
        self.capture_button.setIconSize(QSize(45,20))
        self.capture_button.setEnabled(False)
        record_layout.addWidget(self.record_button)
        record_layout.addWidget(self.capture_button)

        
        settings_layout = QHBoxLayout()  
        self.telemetryCheckbox = QCheckBox(self.tr("Show Telemetry"))
        self.telemetryCheckbox.setChecked(True)
        self.telemetryCheckbox.stateChanged.connect(self.toggleTelemetryVisibility)
        settings_layout.addWidget(self.telemetryCheckbox, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.expansionModeCheckbox = QCheckBox(self.tr("Expansion Mode"))
        self.expansionModeCheckbox.setChecked(False)
        settings_layout.addWidget(self.expansionModeCheckbox, alignment=Qt.AlignmentFlag.AlignHCenter)

        video_telemetry_layout.addLayout(settings_layout)

        # --- Expansion Mode: Diagnostic/Session controls (visible only when Expansion Mode is enabled)
        self.expansion_diagnostic_widget = QWidget(self)
        expansion_diag_layout = QGridLayout()
        self.expansion_diagnostic_widget.setLayout(expansion_diag_layout)

        # Buttons
        self.btn_exp_initialize = QPushButton(self.tr("Initialize"))
        self.btn_exp_start_diagnostic = QPushButton(self.tr("Start Diagnostic Session"))
        self.btn_exp_stop_diagnostic = QPushButton(self.tr("Stop Diagnostic"))
        self.btn_exp_report = QPushButton(self.tr("Report"))

        # Initial enable-state logic (requested)
        self.btn_exp_initialize.setEnabled(True)
        self.btn_exp_start_diagnostic.setEnabled(False)
        self.btn_exp_stop_diagnostic.setEnabled(False)
        self.btn_exp_report.setEnabled(False)

        # Dropdowns
        self.label_models = QLabel(self.tr("Models:"))
        self.combo_models = QComboBox()
        self.label_sessions = QLabel(self.tr("Sessions:"))
        self.combo_sessions = QComboBox()

        # Session ID input
        self.label_session_id = QLabel(self.tr("Session ID:"))
        self.txt_session_id = QLineEdit()

        # Internal layout for "Models" and "Sessions" aligned in a single column (as in the mockup)
        models_sessions_layout = QGridLayout()
        models_sessions_layout.addWidget(self.label_models, 0, 0)
        models_sessions_layout.addWidget(self.combo_models, 0, 1)
        models_sessions_layout.addWidget(self.label_sessions, 1, 0)
        models_sessions_layout.addWidget(self.combo_sessions, 1, 1)

        # Internal layout for "Session ID"
        session_id_layout = QHBoxLayout()
        session_id_layout.addWidget(self.label_session_id)
        session_id_layout.addWidget(self.txt_session_id)

        # Place elements to resemble the provided image
        expansion_diag_layout.addWidget(self.btn_exp_initialize, 0, 0)
        expansion_diag_layout.addLayout(models_sessions_layout, 0, 1, 2, 1)  # span two rows
        expansion_diag_layout.addWidget(self.btn_exp_start_diagnostic, 0, 2)
        expansion_diag_layout.addLayout(session_id_layout, 1, 0)
        expansion_diag_layout.addWidget(self.btn_exp_stop_diagnostic, 2, 1)
        expansion_diag_layout.addWidget(self.btn_exp_report, 2, 2)

        # Register as Expansion widgets (hidden by default; toggled by checkbox)
        self._expansion_widgets.append(self.expansion_diagnostic_widget)
        self.expansion_diagnostic_widget.setVisible(False)

        warning_layout = QHBoxLayout()
        self.warning_label = QLabel(self.tr("Warning"))
        self.warning_text = QTextEdit(self.tr(f"There are no warnings.")) 
        self.warning_text.setReadOnly(True)  
        self.warning_text.setFixedHeight(25) 
        
        video_telemetry_layout.addWidget(self.expansion_diagnostic_widget)
        video_telemetry_layout.addLayout(warning_layout)
        video_telemetry_layout.addLayout(record_layout)
         
        
        warning_layout.addWidget(self.warning_label)
        warning_layout.addWidget(self.warning_text)
        self.telemetry_label = QLabel(self.image_label)
        # Funciones de Diagnóstico
        # Overlay para mostrar el último label del diagnóstico (NEW)
        self.diagnosis_overlay = QLabel(self.image_label)
        self.diagnosis_overlay.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 128);")
        self.diagnosis_overlay.move(10, 10)
        self.diagnosis_overlay.setFixedSize(220, 55)
        self.diagnosis_overlay.setWordWrap(True)
        self.diagnosis_overlay.setText(self.tr("Diagnosis:\nN/A"))
        # Final funciones de Diagnóstico

        self.telemetry_label.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 128);")
        self.telemetry_label.move(self.disply_width_telemetry - 210, self.display_height_telemetry - 100)
        self.telemetry_label.setFixedSize(500, 125)
        self.telemetry_label.setWordWrap(True)

        
        session_layout = QHBoxLayout()  
        self.startButton = QPushButton(self.tr('Log In'))
        self.startButton.setIcon(QIcon("src/Inspection/Icons/session.png"))
        self.startButton.setIconSize(QSize(45,20))
        self.closeButton = QPushButton(self.tr("Close"))
        self.closeButton.setIcon(QIcon("src/Inspection/Icons/close.png"))
        self.closeButton.setIconSize(QSize(45,20))
        self.downloadButton = QPushButton(self.tr("Download Sessions"))
        self.downloadButton.setIcon(QIcon("src/Inspection/Icons/download.png"))
        self.downloadButton.setIconSize(QSize(45,20))
        session_layout.addWidget(self.startButton)
        session_layout.addWidget(self.downloadButton)
        session_layout.addWidget(self.closeButton)        
        video_telemetry_layout.addLayout(session_layout)
                      
        controls_layout = QVBoxLayout()

        # =========================
        # Vision / Diagnosis Controls (NEW)
        # =========================
        diag_layout = QGridLayout()

        self.btn_diag_init = QPushButton(self.tr("Initialize"))
        self.btn_diag_init.setMinimumHeight(40)

        self.cb_models = QComboBox()
        self.cb_models.setMinimumWidth(220)
        self.cb_sessions = QComboBox()
        self.cb_sessions.setMinimumWidth(220)

        self.btn_diag_start = QPushButton(self.tr("Start Diagnosis Session"))
        self.btn_diag_stop = QPushButton(self.tr("Stop Diagnosis"))
        self.btn_diag_report = QPushButton(self.tr("Report"))

        # Caja de texto (reemplaza el botón tachado de tu mockup)
        self.diag_status = QTextEdit()
        self.diag_status.setReadOnly(True)
        self.diag_status.setFixedHeight(60)

        # Grid parecido a tu layout:
        # Row 0: Initialize | combos | Start
        diag_layout.addWidget(self.btn_diag_init,   0, 0)
        diag_layout.addWidget(self.cb_models,       0, 1)
        diag_layout.addWidget(self.cb_sessions,     0, 2)
        diag_layout.addWidget(self.btn_diag_start,  0, 3)

        # Row 1: status box | Stop | Report
        diag_layout.addWidget(self.diag_status,     1, 0, 1, 2)
        diag_layout.addWidget(self.btn_diag_stop,   1, 2)
        diag_layout.addWidget(self.btn_diag_report, 1, 3)

        controls_layout.addLayout(diag_layout)

        ## Fin Vision / Diagnosis Controls ##
        
        self.label_robot_controls = QLabel(self.tr("Robot Controls"))
        self.label_robot_controls.setAlignment(Qt.AlignmentFlag.AlignCenter)
        controls_layout.addWidget(self.label_robot_controls)

        movement_layout = QGridLayout()
        self.btn_forward = QPushButton(self.tr("Forward"))
        self.btn_forward.setIcon(QIcon("src/Inspection/Icons/Forward.png"))
        self.btn_forward.setIconSize(QSize(45,25))
        self.btn_backward = QPushButton(self.tr("Backward"))
        self.btn_backward.setIcon(QIcon("src/Inspection/Icons/Backward.png"))
        self.btn_backward.setIconSize(QSize(45,25))
        self.btn_left_forward = QPushButton(self.tr("Left Forward"))
        self.btn_left_forward.setIcon(QIcon("src/Inspection/Icons/Left Forward.png"))
        self.btn_left_forward.setIconSize(QSize(45,25))
        self.btn_right_forward = QPushButton(self.tr("Right Forward"))
        self.btn_right_forward.setIcon(QIcon("src/Inspection/Icons/Right Forward.png"))
        self.btn_right_forward.setIconSize(QSize(45,25))
        self.btn_left_backward = QPushButton(self.tr("Left Backward"))
        self.btn_left_backward.setIcon(QIcon("src/Inspection/Icons/Left Backward.png"))
        self.btn_left_backward.setIconSize(QSize(45,25))
        self.btn_right_backward = QPushButton(self.tr("Right Backward"))
        self.btn_right_backward.setIcon(QIcon("src/Inspection/Icons/Right Backward.png"))
        self.btn_right_backward.setIconSize(QSize(45,25))

        movement_layout.addWidget(self.btn_left_forward, 0, 0)
        movement_layout.addWidget(self.btn_right_forward, 0, 1)
        movement_layout.addWidget(self.btn_forward, 1, 0, 1, 2)
        movement_layout.addWidget(self.btn_backward, 2, 0, 1, 2)
        movement_layout.addWidget(self.btn_left_backward, 3, 0)
        movement_layout.addWidget(self.btn_right_backward, 3, 1)
        controls_layout.addLayout(movement_layout)

        
        
        self.label_speed = QLabel(self.tr("Speed Control"))
        self.label_speed.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.slider_speed = QSlider(Qt.Orientation.Horizontal)
        self.slider_speed.setMinimum(3)
        self.slider_speed.setMaximum(1000)
        
        
        speed_layout = QHBoxLayout()
        speed_layout.addWidget(self.label_speed)
        speed_layout.addWidget(self.slider_speed)

        # Agregar el layout horizontal al layout vertical principal
        controls_layout.addLayout(speed_layout)

        # Etiqueta y controles de la cámara
        self.label_camera_controls = QLabel(self.tr("Camera Controls"))
        self.label_camera_controls.setAlignment(Qt.AlignmentFlag.AlignCenter)
        controls_layout.addWidget(self.label_camera_controls)

        camera_layout = QGridLayout()
        self.btn_init_camera = QPushButton(self.tr("Initialize Camera"))
        camera_layout.addWidget(self.btn_init_camera, 0, 0, 1, 2)  # Span 2 columns
        self.btn_init_camera.setIcon(QIcon("src/Inspection/Icons/init.png"))
        self.btn_init_camera.setIconSize(QSize(45,25))


        self.btn_tilt_down = QPushButton(self.tr("Tilt Down"))
        self.btn_tilt_up = QPushButton(self.tr("Tilt Up"))
        camera_layout.addWidget(self.btn_tilt_down, 1, 0)
        camera_layout.addWidget(self.btn_tilt_up, 1, 1)
        self.btn_tilt_down.setIcon(QIcon("src/Inspection/Icons/Tilt down.png"))
        self.btn_tilt_down.setIconSize(QSize(45,25))
        self.btn_tilt_up.setIcon(QIcon("src/Inspection/Icons/Tilt up.png"))
        self.btn_tilt_up.setIconSize(QSize(45,25))

        self.btn_pan_left = QPushButton(self.tr("Pan Left"))
        self.btn_pan_right = QPushButton(self.tr("Pan Right"))
        camera_layout.addWidget(self.btn_pan_left, 2, 0)
        camera_layout.addWidget(self.btn_pan_right, 2, 1)
        self.btn_pan_left.setIcon(QIcon("src/Inspection/Icons/Pan Left.png"))
        self.btn_pan_left.setIconSize(QSize(45,25))
        self.btn_pan_right.setIcon(QIcon("src/Inspection/Icons/Pan Right.png"))
        self.btn_pan_right.setIconSize(QSize(45,25))

        self.btn_focus_out = QPushButton(self.tr("Focus Out"))
        self.btn_focus_in = QPushButton(self.tr("Focus In"))
        camera_layout.addWidget(self.btn_focus_out, 3, 0)
        camera_layout.addWidget(self.btn_focus_in, 3, 1)
        
        self.btn_focus_out.setIcon(QIcon("src/Inspection/Icons/Focus Out.png"))
        self.btn_focus_out.setIconSize(QSize(45,25))
        self.btn_focus_in.setIcon(QIcon("src/Inspection/Icons/Focus In.png"))
        self.btn_focus_in.setIconSize(QSize(45,25))

        # --- NUEVO: Zoom buttons (solo disponibles en Expansion Mode)
        self.btn_zoom_out = QPushButton(self.tr("Zoom Out"))
        self.btn_zoom_in = QPushButton(self.tr("Zoom In"))
        camera_layout.addWidget(self.btn_zoom_out, 4, 0)
        camera_layout.addWidget(self.btn_zoom_in, 4, 1)
        controls_layout.addLayout(camera_layout)
        #self.btn_zoom_out.setIcon(QIcon("src/Inspection/Icons/Zoom Out.png"))
        #self.btn_zoom_out.setIconSize(QSize(45,25))
        #self.btn_zoom_in.setIcon(QIcon("src/Inspection/Icons/Zoom In.png"))
        #self.btn_zoom_in.setIconSize(QSize(45,25))

        # Registrar como widgets "expansión" y ocultarlos por defecto
        self._expansion_widgets.append(self.btn_zoom_out)
        self._expansion_widgets.append(self.btn_zoom_in)
        self.btn_zoom_out.setVisible(False)
        self.btn_zoom_in.setVisible(False)

        # Layout para controles de iluminación
        light_controls_layout = QHBoxLayout()
        self.label_light_controls = QLabel(self.tr("Illumination Control"))
        self.label_light_controls.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.slider_light = QSlider(Qt.Orientation.Horizontal)
        self.slider_light.setMinimum(0)
        self.slider_light.setMaximum(100)
        light_controls_layout.addWidget(self.label_light_controls)
        light_controls_layout.addWidget(self.slider_light)
        controls_layout.addLayout(light_controls_layout)

        # --- NUEVO: Layout para controles de brazo (solo Expansion Mode)
        self.label_arm_controls = QLabel(self.tr("Arm Controls"))
        self.label_arm_controls.setAlignment(Qt.AlignmentFlag.AlignCenter)
        controls_layout.addWidget(self.label_arm_controls)

        arm_layout = QGridLayout()
        self.btn_arm_down = QPushButton(self.tr("Down"))
        self.btn_arm_up = QPushButton(self.tr("Up"))
        arm_layout.addWidget(self.btn_arm_down, 0, 0)
        arm_layout.addWidget(self.btn_arm_up, 0, 1)
        controls_layout.addLayout(arm_layout)
        # Registrar el bloque completo como "expansión" (se oculta/activa con el checkbox)
        self._expansion_widgets.extend([
            self.label_arm_controls,
            self.btn_arm_down,
            self.btn_arm_up
        ])
        self.label_arm_controls.setVisible(False)
        self.btn_arm_down.setVisible(False)
        self.btn_arm_up.setVisible(False)

        # Insertarlo debajo del bloque de cámara
        #controls_layout.addWidget(self.arm_group)


        # Añadir el QComboBox del idioma al layout de controles principal
        encoder_controls_layout = QHBoxLayout()
        self.label_encoder_controls = QLabel(self.tr("Reel"))
        self.btn_init_encoder = QPushButton(self.tr("Initialize Reel"))
        self.btn_init_encoder.setIcon(QIcon("src/Inspection/Icons/Reel.png"))
        self.btn_init_encoder.setIconSize(QSize(45,25))
        encoder_controls_layout.addWidget(self.label_encoder_controls, alignment=Qt.AlignmentFlag.AlignVCenter)
        encoder_controls_layout.addWidget(self.btn_init_encoder)
        controls_layout.addLayout(encoder_controls_layout)

         # Añadir el QComboBox del idioma al layout de controles principal
        language_controls_layout = QHBoxLayout()
        self.label_language_controls = QLabel(self.tr("Language"))
        self.languageComboBox = QComboBox()
        self.languageComboBox.addItem("English", "en")
        self.languageComboBox.addItem("Español", "es")
        # Establecer el idioma predeterminado en español
        default_language = "Español"
        self.languageComboBox.setCurrentText(default_language)

        language_controls_layout.addWidget(self.label_language_controls, alignment=Qt.AlignmentFlag.AlignVCenter)
        language_controls_layout.addWidget(self.languageComboBox)
        controls_layout.addLayout(language_controls_layout)

        # Añadir los layouts de video/telemetría y controles al layout principal
        main_layout.addLayout(video_telemetry_layout)
        main_layout.addLayout(controls_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def setup_connections(self):
        # Connect ExpasionMode checkbox
        self.expansionModeCheckbox.stateChanged.connect(self.on_expansion_mode_changed)

        # Expansion Mode: enable/disable chain for diagnostic controls (UI-only logic for now)
        self.btn_exp_initialize.clicked.connect(self._on_exp_initialize_clicked)
        self.btn_exp_start_diagnostic.clicked.connect(self._on_exp_start_diagnostic_clicked)
        self.btn_exp_stop_diagnostic.clicked.connect(self._on_exp_stop_diagnostic_clicked)

        # Connect movement buttons
        self.btn_forward.pressed.connect(lambda: self.panel_services.update_robot_control(RobotControlData(direction='F')))
        self.btn_backward.pressed.connect(lambda: self.panel_services.update_robot_control(RobotControlData(direction='B')))
        self.btn_left_forward.pressed.connect(lambda: self.panel_services.update_robot_control(RobotControlData(direction='FL')))
        self.btn_right_forward.pressed.connect(lambda: self.panel_services.update_robot_control(RobotControlData(direction='FR')))
        self.btn_left_backward.pressed.connect(lambda: self.panel_services.update_robot_control(RobotControlData(direction='BL')))
        self.btn_right_backward.pressed.connect(lambda: self.panel_services.update_robot_control(RobotControlData(direction='BR')))

        self.btn_forward.released.connect(lambda: self.panel_services.update_robot_control(RobotControlData(direction='STOP')))
        self.btn_backward.released.connect(lambda: self.panel_services.update_robot_control(RobotControlData(direction='STOP')))
        self.btn_left_forward.released.connect(lambda: self.panel_services.update_robot_control(RobotControlData(direction='STOP')))
        self.btn_right_forward.released.connect(lambda: self.panel_services.update_robot_control(RobotControlData(direction='STOP')))
        self.btn_left_backward.released.connect(lambda: self.panel_services.update_robot_control(RobotControlData(direction='STOP')))
        self.btn_right_backward.released.connect(lambda: self.panel_services.update_robot_control(RobotControlData(direction='STOP')))

        self.slider_speed.valueChanged.connect(self.panel_services.update_robot_speed)

        self.record_button.clicked.connect(self.updateRecordButtonState)
        self.startButton.clicked.connect(self.openSessionNameDialog)
        self.downloadButton.clicked.connect(self.openSessionsListDialog)
        self.closeButton.clicked.connect(self.close)
        

        # Connect camera buttons
        self.btn_tilt_down.pressed.connect(lambda: self.panel_services.update_camera_control(CameraControlData(movement='TD',light=str(self.slider_light.value()))))
        self.btn_tilt_up.pressed.connect(lambda: self.panel_services.update_camera_control(CameraControlData(movement='TU',light=str(self.slider_light.value()))))
        self.btn_pan_left.pressed.connect(lambda: self.panel_services.update_camera_control(CameraControlData(movement='PL',light=str(self.slider_light.value()))))
        self.btn_pan_right.pressed.connect(lambda: self.panel_services.update_camera_control(CameraControlData(movement='PR',light=str(self.slider_light.value()))))
        self.btn_focus_in.pressed.connect(lambda: self.panel_services.update_camera_control(CameraControlData(movement='FI',light=str(self.slider_light.value()))))
        self.btn_focus_out.pressed.connect(lambda: self.panel_services.update_camera_control(CameraControlData(movement='FO',light=str(self.slider_light.value()))))

        self.btn_tilt_up.released.connect(lambda: self.panel_services.update_camera_control(CameraControlData(movement='STOP',light=str(self.slider_light.value()))))
        self.btn_tilt_down.released.connect(lambda: self.panel_services.update_camera_control(CameraControlData(movement='STOP',light=str(self.slider_light.value()))))
        self.btn_pan_left.released.connect(lambda: self.panel_services.update_camera_control(CameraControlData(movement='STOP',light=str(self.slider_light.value()))))
        self.btn_pan_right.released.connect(lambda: self.panel_services.update_camera_control(CameraControlData(movement='STOP',light=str(self.slider_light.value()))))
        self.btn_focus_in.released.connect(lambda: self.panel_services.update_camera_control(CameraControlData(movement='STOP',light=str(self.slider_light.value()))))
        self.btn_focus_out.released.connect(lambda: self.panel_services.update_camera_control(CameraControlData(movement='STOP',light=str(self.slider_light.value()))))

        self.slider_light.valueChanged.connect(self.panel_services.update_camera_light)
        self.btn_init_camera.clicked.connect(lambda: self.panel_services.update_camera_control(CameraControlData(movement='INIT',light=str(self.slider_light.value()))))

        # Connect zoom buttons (Expansion Mode)
        self.btn_zoom_in.pressed.connect(lambda: self.panel_services.update_camera_control(CameraControlData(movement='ZI', light=str(self.slider_light.value()))))
        self.btn_zoom_out.pressed.connect(lambda: self.panel_services.update_camera_control(CameraControlData(movement='ZO', light=str(self.slider_light.value()))))
        self.btn_zoom_in.released.connect(lambda: self.panel_services.update_camera_control(CameraControlData(movement='STOP', light=str(self.slider_light.value()))))
        self.btn_zoom_out.released.connect(lambda: self.panel_services.update_camera_control(CameraControlData(movement='STOP', light=str(self.slider_light.value()))))

        # Connect arm buttons (Expansion Mode)
        self.btn_arm_up.pressed.connect(lambda: self.panel_services.update_arm_control(ArmControlData(movement="UP")))
        self.btn_arm_down.pressed.connect(lambda: self.panel_services.update_arm_control(ArmControlData(movement="DOWN")))
        self.btn_arm_up.released.connect(lambda: self.panel_services.update_arm_control(ArmControlData(movement="STOP")))
        self.btn_arm_down.released.connect(lambda: self.panel_services.update_arm_control(ArmControlData(movement="STOP")))

        # Connect translation
        self.languageComboBox.currentIndexChanged.connect(self.changeLanguage)

        #Connect session
        self.record_button.clicked.connect(self.toggleRecording)
        self.capture_button.clicked.connect(self.session_services.take_capture)

        #Connect init encoder button 
        self.btn_init_encoder.clicked.connect(self.initializate_encoder)

        # Diagnosis (NEW)
        self.btn_diag_init.clicked.connect(self.on_diag_init_clicked)
        self.cb_models.currentIndexChanged.connect(self.on_model_changed)
        self.btn_diag_start.clicked.connect(self.on_diag_start_clicked)
        self.btn_diag_stop.clicked.connect(self.on_diag_stop_clicked)
        self.btn_diag_report.clicked.connect(self.on_diag_report_clicked)
    

    # ---------------------------------------------------------------------
    # Expansion Mode: Diagnostic/Session controls (UI-only state machine)
    # ---------------------------------------------------------------------
    def _reset_expansion_diagnostic_controls(self) -> None:
        """Reset enable/disable state for Expansion Mode diagnostic controls."""
        self.btn_exp_initialize.setEnabled(True)
        self.btn_exp_start_diagnostic.setEnabled(False)
        self.btn_exp_stop_diagnostic.setEnabled(False)
        self.btn_exp_report.setEnabled(False)

    def _on_exp_initialize_clicked(self) -> None:
        # After Initialize -> enable Start Diagnostic Session; keep Stop/Report disabled
        self.btn_exp_start_diagnostic.setEnabled(True)
        self.btn_exp_stop_diagnostic.setEnabled(False)
        self.btn_exp_report.setEnabled(False)

    def _on_exp_start_diagnostic_clicked(self) -> None:
        # After Start Diagnostic Session -> enable Stop Diagnostic; keep Report disabled
        self.btn_exp_stop_diagnostic.setEnabled(True)
        self.btn_exp_report.setEnabled(False)

    def _on_exp_stop_diagnostic_clicked(self) -> None:
        # After Stop Diagnostic -> enable Report
        self.btn_exp_report.setEnabled(True)

    def initializate_encoder(self):
        print("Enviar por serial")
        self.feeder_services.send_message("feeder RESET")
        
    def on_expansion_mode_changed(self, state: int):
        is_enabled = self.expansionModeCheckbox.isChecked()
        #send to backend
        self.panel_services.set_expansion_mode(is_enabled)
        for w in self._expansion_widgets:
            w.setVisible(is_enabled)
        #STOP camera
        self.panel_services.update_camera_control(
            CameraControlData(movement='STOP', light=str(self.slider_light.value()))
        )

    def toggleTelemetryVisibility(self, state):
        self.telemetry_label.setVisible(self.telemetryCheckbox.isChecked())
    
    def toggleRecording(self):
        if self.isRecording:
            self.session_services.stop_recording()
        else:
            self.session_services.start_recording()
        self.isRecording = not self.isRecording
        self.updateRecordButtonState()

      
    def openSessionNameDialog(self):
        if not self.SessionState:
            dialog = SessionNameDialog()
            if dialog.exec():
                session_name = dialog.getSessionName().strip()
                if session_name and self.session_services.begin_session(session_name):
                    print(f"Nombre de la sesión: {session_name}")
                    self.startButton.setText(self.tr("Log Out")) 
                    self.SessionState = True
                    self.updateSessionButtonState()
                    self.operator_name = session_name

                    
                    self.record_button.setEnabled(True)
                    self.capture_button.setEnabled(True)                
                else:
                    print('The session name is not valid')
                    msgBox = QMessageBox()
                    msgBox.setIcon(QMessageBox.Icon.Warning)  
                    msgBox.setWindowTitle(self.tr("Session error"))  
                    msgBox.setText(self.tr(f"The name {session_name} is not valid.")) 
                    msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)  
                    msgBox.exec()  
            
        else:
            if self.record_button.text() == self.tr("Stop Record"):
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Icon.Warning)
                msgBox.setWindowTitle(self.tr(self.tr("Warning")))
                msgBox.setText(self.tr("Recording in progress."))
                msgBox.setInformativeText(self.tr("Please stop recording before loging out."))
                msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
                msgBox.exec()
            else:
                self.startButton.setText(self.tr("Log In"))
                self.SessionState = False
                self.updateSessionButtonState()
                
                self.record_button.setEnabled(False)
                self.capture_button.setEnabled(False)
                self.session_services.finish_session()

    def openSessionsListDialog(self): 
        dialog = SessionsListDialog(self.session_services)
        if dialog.exec():
            pass


    def changeLanguage(self, index):
        language_code = self.languageComboBox.itemData(index)
        self.translator.load(f"src/Inspection/Translations/{language_code}.qm")
        _app = QApplication.instance()
        _app.installTranslator(self.translator)
        
        self.retranslateUi()
        self.updateSessionButtonState()
        self.updateRecordButtonState()

    def updateSessionButtonState(self):
        if self.SessionState:
            self.startButton.setText(self.tr("Log Out"))
        else:
            self.startButton.setText(self.tr("Log In"))

    def updateRecordButtonState(self):
        if self.isRecording:
            self.record_button.setText(self.tr("Stop Record"))
        else:
            self.record_button.setText(self.tr("Start Record"))
        
    def retranslateUi(self):
        # Actualizar el título de la ventana y otros textos estáticos
        if self.isRecording:  
            self.record_button.setText(self.tr("Stop Record"))
        else: 
            self.record_button.setText(self.tr("Start Record"))
        
        if self.SessionState:
            self.startButton.setText(self.tr("Log Out"))
        else:
            self.startButton.setText(self.tr("Log In"))

        self.capture_button.setText(self.tr("Capture Image"))
        self.telemetryCheckbox.setText(self.tr("Show Telemetry"))
        self.closeButton.setText(self.tr("Close"))
        self.label_robot_controls.setText(self.tr("Robot Controls"))
        self.label_speed.setText(self.tr("Speed Control"))
        self.label_light_controls.setText(self.tr("Illumination Control"))
        self.label_camera_controls.setText(self.tr("Camera Controls"))
        self.warning_label.setText(self.tr("Warning"))
        self.label_encoder_controls.setText(self.tr("Reel"))
        self.label_language_controls.setText(self.tr("Language"))
        self.startButton.setText(self.tr("Log In"))
        self.expansionModeCheckbox.setText(self.tr("Expansion Mode"))
        self.btn_zoom_in.setText(self.tr("Zoom In"))
        self.btn_zoom_out.setText(self.tr("Zoom Out"))
        self.label_arm_controls.setText(self.tr("Arm Controls"))
        self.btn_arm_up.setText(self.tr("Up"))
        self.btn_arm_down.setText(self.tr("Down"))


        # Actualizar etiquetas y controles específicos
        self.btn_forward.setText(self.tr("Forward"))
        self.btn_backward.setText(self.tr("Backward"))
        self.btn_left_forward.setText(self.tr("Left Forward"))
        self.btn_right_forward.setText(self.tr("Right Forward"))
        self.btn_left_backward.setText(self.tr("Left Backward"))
        self.btn_right_backward.setText(self.tr("Right Backward"))
        self.btn_init_camera.setText(self.tr("Initialize Camera"))
        self.btn_tilt_down.setText(self.tr("Tilt Down"))
        self.btn_tilt_up.setText(self.tr("Tilt Up"))
        self.btn_pan_left.setText(self.tr("Pan Left"))
        self.btn_pan_right.setText(self.tr("Pan Right"))
        self.btn_focus_in.setText(self.tr("Focus In"))
        self.btn_focus_out.setText(self.tr("Focus Out"))
        self.btn_init_encoder.setText(self.tr("Initialize Reel"))
        self.warning_text.setText(self.tr("No warnings."))
        self.downloadButton.setText(self.tr("Download Sessions"))
        

    def load_translation(self, language_code):
        translation_file = f"src/Inspection/Translations/{language_code}.qm"
        if QFile.exists(translation_file):
            self.translator.load(translation_file)
            _app = QApplication.instance()
            _app.installTranslator(self.translator)

        self.retranslateUi()

    def closeEvent(self, event):
         if self.SessionState:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.setWindowTitle(self.tr("Warning"))
            msgBox.setText(self.tr("Session in progress."))
            msgBox.setInformativeText(self.tr("Please log out before closing the program."))
            msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
            msgBox.exec()

            event.ignore()  
         else:
            event.accept()  
    
    # =========================
    # Diagnosis UI helpers (NEW)
    # =========================
    def append_diagnosis_status(self, text: str) -> None:
        try:
            self.diag_status.append(text)
        except Exception:
            pass

    def set_diagnosis_overlay(self, text: str) -> None:
        try:
            self.diagnosis_overlay.setText(self.tr("Diagnosis:") + "\n" + str(text))
        except Exception:
            pass

    def _reload_models(self) -> None:
        self.cb_models.blockSignals(True)
        self.cb_models.clear()
        try:
            models = self.diagnosis_services.list_models()
            for m in models:
                mid = m.get("id")
                name = m.get("name", mid)
                desc = m.get("description", "")
                self.cb_models.addItem(f"{name}", mid)
                # opcional: tooltip
                if desc:
                    self.cb_models.setItemData(self.cb_models.count() - 1, desc, Qt.ItemDataRole.ToolTipRole)
        finally:
            self.cb_models.blockSignals(False)

    def _reload_sessions(self) -> None:
        self.cb_sessions.clear()
        sessions = self.diagnosis_services.list_sessions()
        for sid in sessions:
            self.cb_sessions.addItem(sid, sid)

    def on_diag_init_clicked(self) -> None:
        self.append_diagnosis_status("Inicializando visión...")
        resp = self.diagnosis_services.initialize_system()
        if resp.get("ok"):
            self._reload_models()
            self._reload_sessions()
        else:
            self.append_diagnosis_status("ERROR: no se pudo inicializar visión.")

    def on_model_changed(self, index: int) -> None:
        if index < 0:
            return
        model_id = self.cb_models.itemData(index)
        if not model_id:
            return
        try:
            self.diagnosis_services.select_model(str(model_id))
        except Exception as exc:
            self.append_diagnosis_status(f"ERROR seleccionando modelo: {exc}")

    def on_diag_start_clicked(self) -> None:
        operator = self.operator_name or "operator"
        location = self.location_name or "N/A"
        try:
            sid = self.diagnosis_services.start_diagnosis_session(operator=operator, location=location)
            self.append_diagnosis_status(f"Session creada: {sid}")
            self.set_diagnosis_overlay(f"RUNNING\nsid={sid}")
            self.set_diag_controls_state(running=True)
            # refrescar sesiones para que aparezca la nueva
            self._reload_sessions()
        except Exception as exc:
            self.append_diagnosis_status(f"ERROR iniciando diagnóstico: {exc}")

    def on_diag_stop_clicked(self) -> None:
        try:
            status = self.diagnosis_services.stop_diagnosis_session()
            self.append_diagnosis_status(f"Stop: {status}")
            self.set_diagnosis_overlay("STOPPED")
            self.set_diag_controls_state(running=False)
        except Exception as exc:
            self.append_diagnosis_status(f"ERROR deteniendo: {exc}")

    def on_diag_report_clicked(self) -> None:
        operator = self.operator_name or "operator"
        location = self.location_name or "N/A"

        # preferir sesión seleccionada; si no, la activa
        sid = None
        idx = self.cb_sessions.currentIndex()
        if idx >= 0:
            sid = self.cb_sessions.itemData(idx)
        sid = sid or self.diagnosis_services.get_current_session_id()
        if not sid:
            self.append_diagnosis_status("No hay session_id para reporte.")
            return

        try:
            summary = self.diagnosis_services.get_summary(session_id=str(sid), operator=operator, location=location)
            self.append_diagnosis_status(f"Summary OK. counts_by_label={summary.get('counts_by_label')}")
        except Exception as exc:
            self.append_diagnosis_status(f"ERROR summary: {exc}")

    # Fin Diagnosis UI helpers

    #Helpers para botones de diagnóstico (bloqueo)
    def set_diag_controls_state(self, running: bool) -> None:
        self.btn_diag_init.setEnabled(not running)
        self.btn_diag_start.setEnabled(not running)
        self.btn_diag_stop.setEnabled(running)
        # Report se habilita solo cuando no está running; pero además depende del STOPPED (lo valida el service)
        self.btn_diag_report.setEnabled(not running)


    @classmethod
    def show_error_dialog_connections(cls):
        if cls._error_dialog_instance is not None:
            return

        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setText(cls.tr("             Connection Error.             "))
        error_dialog.setInformativeText(cls.tr("             Please check connections between robot and reel.             "))
        error_dialog.setWindowTitle(cls.tr("             Connection Error.             "))
        error_dialog.finished.connect(cls._clear_error_dialog_instance)
        cls._error_dialog_instance = error_dialog

        error_dialog.exec()

    @classmethod
    def show_error_dialog_restart(cls):
        if cls._error_dialog_instance is not None:
            return  

        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setText(cls.tr("             Connection Error.                "))
        error_dialog.setInformativeText(cls.tr("             Please restart the system.             "))
        error_dialog.setWindowTitle(cls.tr("             Communication Error.             "))
        error_dialog.finished.connect(cls._clear_error_dialog_instance)
        cls._error_dialog_instance = error_dialog

        error_dialog.exec()

    @staticmethod
    def _clear_error_dialog_instance():
        MainWindow._error_dialog_instance = None
