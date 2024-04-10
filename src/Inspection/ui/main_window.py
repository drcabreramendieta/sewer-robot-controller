import cv2
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot, QSize, QTranslator, QFile
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QGridLayout, QPushButton, QWidget, QSlider, QLabel, QHBoxLayout, QCheckBox, QComboBox, QApplication, QTextEdit, QMessageBox
from PyQt6.QtGui import QImage, QPixmap, QIcon
from Inspection.ports.robot_controller import RobotController
from Inspection.ports.camera_controller import CameraController
from Video.domain.use_cases.video_notifier import VideoNotifier
from Video.domain.entities import VideoMessage
from Inspection.adapters.qt_video_observer import QtVideoObserver
from Communication.adapters.test_observer import TestTelemetryObserver
from Communication.domain.entities import TelemetryMessage
from Communication.domain.use_cases.notify_telemetry import NotifyTelemetry
from Inspection.ports.session_controller import SessionController
from Inspection.ui.session_name_dialog import SessionNameDialog
from Inspection.ui.sessions_list_dialog import SessionsListDialog
from Video.domain.use_cases.control_session import ControlSession

class MainWindow(QMainWindow):
    video_changed_signal = pyqtSignal(VideoMessage)
    telemetry_updated_signal = pyqtSignal(TelemetryMessage)
    
    
    def __init__(self, robot_controller: RobotController, camera_controller: CameraController, video_observer: QtVideoObserver, video_notifier: VideoNotifier, telemetry_observer: TestTelemetryObserver, telemetry_notifier: NotifyTelemetry, session_controller: SessionController, control_session_use_case: ControlSession,  ) -> None:
        super().__init__()
        self.latest_temperature = "N/A"
        self.latest_humidity = "N/A"
        self.latest_x_slop = "N/A"
        self.latest_y_slop = "N/A"
        self.robot_controller = robot_controller
        self.camera_controller = camera_controller
        self.video_notifier = video_notifier
        self.video_observer = video_observer
        self.video_observer.register_signal(self.video_changed_signal)
        self.video_notifier.register_observer(self.video_observer)
        self.telemetry_notifier = telemetry_notifier
        self.telemetry_observer = telemetry_observer
        self.telemetry_observer.register_signal(self.telemetry_updated_signal)
        self.telemetry_notifier.register_observer(self.telemetry_observer)

        self.session_controller = session_controller
        self.control_session_user_case = control_session_use_case 

        self.translator = QTranslator(self)
        self.SessionState = False  
        self.isRecording = False
              
        self.disply_width = 960
        self.display_height = 470
        self.disply_width_telemetry = 720
        self.display_height_telemetry = 460
        
        self.init_ui()
        self.setup_connections()
        self.load_translation("es")
        
    
    def init_ui(self):
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        main_layout = QHBoxLayout()
        
        video_telemetry_layout = QVBoxLayout()
        self.image_label = QLabel()
        self.image_label.setFixedSize(720, 450)
        video_telemetry_layout.addWidget(self.image_label)
        

        record_layout = QHBoxLayout()  
        self.record_button = QPushButton(self.tr("Start Record")) 
        self.record_button.setIcon(QIcon("/home/iiot/Documents/Terminal/src/Icons/record.png"))
        self.record_button.setIconSize(QSize(45,20))
        self.record_button.setEnabled(False)
        self.capture_button = QPushButton(self.tr("Capture Image")) 
        self.capture_button.setIcon(QIcon("/home/iiot/Documents/Terminal/src/Icons/capture.png"))
        self.capture_button.setIconSize(QSize(45,20))
        self.capture_button.setEnabled(False)
        record_layout.addWidget(self.record_button)
        record_layout.addWidget(self.capture_button)

        
        settings_layout = QHBoxLayout()  
        self.telemetryCheckbox = QCheckBox(self.tr("Show Telemetry"))
        self.telemetryCheckbox.setChecked(True)
        self.telemetryCheckbox.stateChanged.connect(self.toggleTelemetryVisibility)
        settings_layout.addWidget(self.telemetryCheckbox, alignment=Qt.AlignmentFlag.AlignHCenter)

        
        warning_layout = QHBoxLayout()
        self.warning_label = QLabel(self.tr("Warning"))
        self.warning_text = QTextEdit(self.tr(f"There are no warnings.")) 
        self.warning_text.setReadOnly(True)  
        self.warning_text.setFixedHeight(25)  
        
        warning_layout.addWidget(self.warning_label)
        warning_layout.addWidget(self.warning_text)
        
        video_telemetry_layout.addLayout(settings_layout) 
        video_telemetry_layout.addLayout(warning_layout)
        video_telemetry_layout.addLayout(record_layout)

        self.telemetry_label = QLabel(self.image_label)
        self.telemetry_label.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 128);")
        self.telemetry_label.move(self.disply_width_telemetry - 210, self.display_height_telemetry - 100)
        self.telemetry_label.setFixedSize(500, 125)
        self.telemetry_label.setWordWrap(True)

        
        session_layout = QHBoxLayout()  
        self.startButton = QPushButton(self.tr('Log In'))
        self.startButton.setIcon(QIcon("/home/iiot/Documents/Terminal/src/Icons/session.png"))
        self.startButton.setIconSize(QSize(45,20))
        self.closeButton = QPushButton(self.tr("Close"))
        self.closeButton.setIcon(QIcon("/home/iiot/Documents/Terminal/src/Icons/close.png"))
        self.closeButton.setIconSize(QSize(45,20))
        self.downloadButton = QPushButton(self.tr("Download Sessions"))
        self.downloadButton.setIcon(QIcon("/home/iiot/Documents/Terminal/src/Icons/download.png"))
        self.downloadButton.setIconSize(QSize(45,20))
        session_layout.addWidget(self.startButton)
        session_layout.addWidget(self.downloadButton)
        session_layout.addWidget(self.closeButton)        
        video_telemetry_layout.addLayout(session_layout)
                      
        controls_layout = QVBoxLayout()
        
        self.label_robot_controls = QLabel(self.tr("Robot Controls"))
        self.label_robot_controls.setAlignment(Qt.AlignmentFlag.AlignCenter)
        controls_layout.addWidget(self.label_robot_controls)

        movement_layout = QGridLayout()
        self.btn_forward = QPushButton(self.tr("Forward"))
        self.btn_forward.setIcon(QIcon("/home/iiot/Documents/Terminal/src/Icons/Forward.png"))
        self.btn_forward.setIconSize(QSize(45,25))
        self.btn_backward = QPushButton(self.tr("Backward"))
        self.btn_backward.setIcon(QIcon("/home/iiot/Documents/Terminal/src/Icons/Backward.png"))
        self.btn_backward.setIconSize(QSize(45,25))
        self.btn_left_forward = QPushButton(self.tr("Left Forward"))
        self.btn_left_forward.setIcon(QIcon("/home/iiot/Documents/Terminal/src/Icons/Left Forward.png"))
        self.btn_left_forward.setIconSize(QSize(45,25))
        self.btn_right_forward = QPushButton(self.tr("Right Forward"))
        self.btn_right_forward.setIcon(QIcon("/home/iiot/Documents/Terminal/src/Icons/Right Forward.png"))
        self.btn_right_forward.setIconSize(QSize(45,25))
        self.btn_left_backward = QPushButton(self.tr("Left Backward"))
        self.btn_left_backward.setIcon(QIcon("/home/iiot/Documents/Terminal/src/Icons/Left Backward.png"))
        self.btn_left_backward.setIconSize(QSize(45,25))
        self.btn_right_backward = QPushButton(self.tr("Right Backward"))
        self.btn_right_backward.setIcon(QIcon("/home/iiot/Documents/Terminal/src/Icons/Right Backward.png"))
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
        self.slider_speed.setMinimum(10)
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
        self.btn_init_camera.setIcon(QIcon("/home/iiot/Documents/Terminal/src/Icons/init.png"))
        self.btn_init_camera.setIconSize(QSize(45,25))


        self.btn_tilt_down = QPushButton(self.tr("Tilt Down"))
        self.btn_tilt_up = QPushButton(self.tr("Tilt Up"))
        camera_layout.addWidget(self.btn_tilt_down, 1, 0)
        camera_layout.addWidget(self.btn_tilt_up, 1, 1)
        self.btn_tilt_down.setIcon(QIcon("/home/iiot/Documents/Terminal/src/Icons/Tilt down.png"))
        self.btn_tilt_down.setIconSize(QSize(45,25))
        self.btn_tilt_up.setIcon(QIcon("/home/iiot/Documents/Terminal/src/Icons/Tilt up.png"))
        self.btn_tilt_up.setIconSize(QSize(45,25))

        self.btn_pan_left = QPushButton(self.tr("Pan Left"))
        self.btn_pan_right = QPushButton(self.tr("Pan Right"))
        camera_layout.addWidget(self.btn_pan_left, 2, 0)
        camera_layout.addWidget(self.btn_pan_right, 2, 1)
        self.btn_pan_left.setIcon(QIcon("/home/iiot/Documents/Terminal/src/Icons/Pan Left.png"))
        self.btn_pan_left.setIconSize(QSize(45,25))
        self.btn_pan_right.setIcon(QIcon("/home/iiot/Documents/Terminal/src/Icons/Pan Right.png"))
        self.btn_pan_right.setIconSize(QSize(45,25))

        self.btn_focus_out = QPushButton(self.tr("Focus Out"))
        self.btn_focus_in = QPushButton(self.tr("Focus In"))
        camera_layout.addWidget(self.btn_focus_out, 3, 0)
        camera_layout.addWidget(self.btn_focus_in, 3, 1)
        controls_layout.addLayout(camera_layout)
        self.btn_focus_out.setIcon(QIcon("/home/iiot/Documents/Terminal/src/Icons/Focus Out.png"))
        self.btn_focus_out.setIconSize(QSize(45,25))
        self.btn_focus_in.setIcon(QIcon("/home/iiot/Documents/Terminal/src/Icons/Focus In.png"))
        self.btn_focus_in.setIconSize(QSize(45,25))

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

       

        # Añadir el QComboBox del idioma al layout de controles principal
        encoder_controls_layout = QHBoxLayout()
        self.label_encoder_controls = QLabel(self.tr("Reel"))
        self.btn_init_encoder = QPushButton(self.tr("Initialize Reel"))
        self.btn_init_encoder.setIcon(QIcon("/home/iiot/Documents/Terminal/src/Icons/Reel.png"))
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
        # Connect movement buttons
        self.btn_forward.pressed.connect(self.robot_controller.move_forward)
        self.btn_backward.pressed.connect(self.robot_controller.move_backward)
        self.btn_left_forward.pressed.connect(self.robot_controller.rotate_left_forward)
        self.btn_right_forward.pressed.connect(self.robot_controller.rotate_right_forward)
        self.btn_left_backward.pressed.connect(self.robot_controller.rotate_left_backward)
        self.btn_right_backward.pressed.connect(self.robot_controller.rotate_right_backward)

        self.btn_forward.released.connect(self.robot_controller.stop)
        self.btn_backward.released.connect(self.robot_controller.stop)
        self.btn_left_forward.released.connect(self.robot_controller.stop)
        self.btn_right_forward.released.connect(self.robot_controller.stop)
        self.btn_left_backward.released.connect(self.robot_controller.stop)
        self.btn_right_backward.released.connect(self.robot_controller.stop)

        self.slider_speed.valueChanged.connect(self.robot_controller.change_speed)

        self.record_button.clicked.connect(self.updateRecordButtonState)
        self.startButton.clicked.connect(self.openSessionNameDialog)
        self.downloadButton.clicked.connect(self.openSessionsListDialog)
        self.closeButton.clicked.connect(self.close)
        

        # Connect camera buttons
        self.btn_tilt_down.pressed.connect(self.camera_controller.tilt_down)
        self.btn_tilt_up.pressed.connect(self.camera_controller.tilt_up)
        self.btn_pan_left.pressed.connect(self.camera_controller.pan_left)
        self.btn_pan_right.pressed.connect(self.camera_controller.pan_right)
        self.btn_focus_in.pressed.connect(self.camera_controller.focus_in)
        self.btn_focus_out.pressed.connect(self.camera_controller.focus_out)

        self.btn_tilt_up.released.connect(self.camera_controller.tilt_stop)
        self.btn_tilt_down.released.connect(self.camera_controller.tilt_stop)
        self.btn_pan_left.released.connect(self.camera_controller.pan_stop)
        self.btn_pan_right.released.connect(self.camera_controller.pan_stop)
        self.btn_focus_in.released.connect(self.camera_controller.focus_stop)
        self.btn_focus_out.released.connect(self.camera_controller.focus_stop)

        self.slider_light.valueChanged.connect(self.camera_controller.change_light)
        self.btn_init_camera.clicked.connect(self.camera_controller.init_camera)

        # Connect video update signal
        self.video_changed_signal.connect(self.update_image)
        self.video_notifier.start_listening()

        # Connect translation
        self.languageComboBox.currentIndexChanged.connect(self.changeLanguage)

        #Connect telemetry
        self.telemetry_updated_signal.connect(self.update_telemetry)
        self.telemetry_notifier.start_listening()

        #Connect session
        self.record_button.clicked.connect(self.toggleRecording)
        self.capture_button.clicked.connect(self.session_controller.take_capture)

    def toggleTelemetryVisibility(self, state):
        self.telemetry_label.setVisible(self.telemetryCheckbox.isChecked())
    
    def toggleRecording(self):
        if self.isRecording:
            self.session_controller.start_recording()
        else:
            self.session_controller.stop_recording()
        self.isRecording = not self.isRecording
        self.updateRecordButtonState()

      
    def openSessionNameDialog(self):
        if not self.SessionState:
            dialog = SessionNameDialog()
            if dialog.exec():
                session_name = dialog.getSessionName().strip()
                if session_name and self.session_controller.begin_session(session_name):
                    print(f"Nombre de la sesión: {session_name}")
                    self.startButton.setText(self.tr("Log Out")) 
                    self.SessionState = True
                    self.updateSessionButtonState()
                    
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
                self.session_controller.finish_session()

    def openSessionsListDialog(self): 
        dialog = SessionsListDialog(self.control_session_user_case, json_file_path= "/home/iiot/Documents/Terminal/SessionsDB.json")
        if dialog.exec():
            pass


    def changeLanguage(self, index):
        language_code = self.languageComboBox.itemData(index)
        self.translator.load(f"/home/iiot/Documents/Terminal/src/Translations/{language_code}.qm")
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
        self.isRecording = not self.isRecording
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
        translation_file = f"/home/iiot/Documents/Terminal/src/Translations/{language_code}.qm"
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

        
    @pyqtSlot(VideoMessage)
    def update_image(self, video: VideoMessage):
        qt_img = self.convert_cv_qt(video.frame)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
    def update_telemetry(self, telemetry: TelemetryMessage):
        # Actualizar los atributos con los nuevos valores si están disponibles
        self.latest_temperature = telemetry.variables.get("Temperature", self.latest_temperature)
        self.latest_humidity = telemetry.variables.get("Humidity", self.latest_humidity)
        self.latest_x_slop = telemetry.variables.get("X slop", self.latest_x_slop)
        self.latest_y_slop = telemetry.variables.get("Y slop", self.latest_y_slop)
        motor_status = telemetry.variables.get("Motor status", "N/A")

        # Construir el texto de telemetría con los últimos valores conocidos
        telemetry_text = (f"{self.tr('Telemetry')}\n"
                          f"{self.tr('Temperature:')} {self.latest_temperature} °C \n"
                          f"{self.tr('Humidity:')} {self.latest_humidity} HR \n"
                          f"{self.tr('X slop:')} {self.latest_x_slop} °\n"
                          f"{self.tr('Y slop:')} {self.latest_y_slop} °")

        # Actualizar la etiqueta con el texto de telemetría
        self.telemetry_label.setText(telemetry_text)
        self.telemetry_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        print(telemetry.variables) 
        # Actualizar el texto de advertencia basado en el estado del motor
        if motor_status == 0xC0:
            self.warning_text.setText(self.tr("No warnings."))
        elif motor_status == 0xE0:
            self.warning_text.setText(self.tr("Caution locked wheels."))

    
    
    
    
