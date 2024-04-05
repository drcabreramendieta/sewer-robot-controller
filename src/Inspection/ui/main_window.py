import cv2
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot, QSize, QTranslator, QFile
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QGridLayout, QPushButton, QWidget, QSlider, QLabel, QHBoxLayout, QCheckBox, QComboBox, QApplication, QTextEdit, QDialog, QLineEdit, QMessageBox
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

class SessionNameDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle(self.tr("Enter the session name"))
        layout = QVBoxLayout()
        self.resize(400, 100)  
        self.move_to_center()
        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText(self.tr("Session name")) 
        layout.addWidget(self.lineEdit)
        
        
        buttonLayout = QHBoxLayout()
        
        self.acceptButton = QPushButton(self.tr("Save"))
        self.acceptButton.setEnabled(False)  
        self.acceptButton.clicked.connect(self.accept)
        buttonLayout.addWidget(self.acceptButton)
        
        self.cancelButton = QPushButton(self.tr("Cancel")) 
        self.cancelButton.clicked.connect(self.reject)  
        buttonLayout.addWidget(self.cancelButton)
        
        layout.addLayout(buttonLayout)  
        
        self.setLayout(layout)

        self.lineEdit.textChanged.connect(self.checkInput)
    
    def getSessionName(self):
        return self.lineEdit.text().strip()

    def move_to_center(self):
        screen = QApplication.screens()[0]
        screenGeometry = screen.geometry()
            
        centerX = screenGeometry.center().x()
        centerY = screenGeometry.center().y()
        
        self.move(centerX - self.width() // 2, centerY - self.height() // 2)

    def checkInput(self):
        self.acceptButton.setEnabled(bool(self.lineEdit.text().strip()))

class MainWindow(QMainWindow):
    video_changed_signal = pyqtSignal(VideoMessage)
    telemetry_updated_signal = pyqtSignal(TelemetryMessage)
    
    def __init__(self, robot_controller: RobotController, camera_controller: CameraController, video_observer: QtVideoObserver, video_notifier: VideoNotifier, telemetry_observer: TestTelemetryObserver, telemetry_notifier: NotifyTelemetry, session_controller: SessionController) -> None:
        super().__init__()
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

        self.translator = QTranslator(self)
        self.SessionState = False  
              
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
        self.button1 = QPushButton(self.tr("Start Record")) 
        self.button1.setIcon(QIcon("/home/iiot/Documents/Terminal/src/Icons/record.png"))
        self.button1.setIconSize(QSize(45,20))
        self.button1.setEnabled(False)
        self.button2 = QPushButton(self.tr("Capture Image")) 
        self.button2.setIcon(QIcon("/home/iiot/Documents/Terminal/src/Icons/capture.png"))
        self.button2.setIconSize(QSize(45,20))
        self.button2.setEnabled(False)
        record_layout.addWidget(self.button1)
        record_layout.addWidget(self.button2)

        
        settings_layout = QHBoxLayout()  
        self.telemetryCheckbox = QCheckBox(self.tr("Show Telemetry"))
        self.telemetryCheckbox.setChecked(True)
        self.telemetryCheckbox.stateChanged.connect(self.toggleTelemetryVisibility)
        settings_layout.addWidget(self.telemetryCheckbox, alignment=Qt.AlignmentFlag.AlignHCenter)

        
        warning_layout = QHBoxLayout()
        self.warning_label = QLabel(self.tr("Warning"))
        self.warning_text = QTextEdit(self.tr(f"No hay advertencias.")) 
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
        self.closeButton = QPushButton(self.tr('Close'))
        self.closeButton.setIcon(QIcon("/home/iiot/Documents/Terminal/src/Icons/close.png"))
        self.closeButton.setIconSize(QSize(45,20))
        self.closeButton.clicked.connect(self.close)
        session_layout.addWidget(self.startButton)
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

        self.button1.clicked.connect(self.toggle_record)
        self.startButton.clicked.connect(self.openSessionNameDialog)
        

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
        self.button1.pressed.connect(self.session_controller.start_recording)
        self.button1.released.connect(self.session_controller.stop_recording)
        self.button2.clicked.connect(self.session_controller.take_capture)

    def toggleTelemetryVisibility(self, state):
        self.telemetry_label.setVisible(self.telemetryCheckbox.isChecked())

    def toggle_record(self):
        if self.button1.text() == self.tr("Start Record"):
            self.button1.setText(self.tr("Stop Record"))
        else:
            self.button1.setText(self.tr("Start Record"))

    
    def openSessionNameDialog(self):
        if not self.SessionState:
            dialog = SessionNameDialog()
            if dialog.exec():
                session_name = dialog.getSessionName().strip()
                if session_name:
                    print(f"Nombre de la sesión: {session_name}")
                    self.startButton.setText(self.tr("Log Out")) 
                    self.SessionState = True
                    self.updateSessionButtonState()
                    
                    self.button1.setEnabled(True)
                    self.button2.setEnabled(True)
                    self.session_controller.begin_session()
            
        else:
            if self.button1.text() == self.tr("Stop Record"):
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Icon.Warning)
                msgBox.setWindowTitle(self.tr(self.tr("Advertencia")))
                msgBox.setText(self.tr("La grabación está activa."))
                msgBox.setInformativeText(self.tr("Por favor, detén la grabación antes de cerrar sesión."))
                msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
                msgBox.exec()
            else:
                self.startButton.setText(self.tr("Log In"))
                self.SessionState = False
                self.updateSessionButtonState()
                
                self.button1.setEnabled(False)
                self.button2.setEnabled(False)
                self.session_controller.finish_session()


    def changeLanguage(self, index):
        language_code = self.languageComboBox.itemData(index)
        self.translator.load(f"/home/iiot/Documents/Terminal/src/Translations/{language_code}.qm")
        _app = QApplication.instance()
        _app.installTranslator(self.translator)
        
        self.retranslateUi()
        self.updateSessionButtonState()

    def updateSessionButtonState(self):
        if self.SessionState:
            self.startButton.setText(self.tr("Log Out"))
        else:
            self.startButton.setText(self.tr("Log In"))

        
    def retranslateUi(self):
        # Actualizar el título de la ventana y otros textos estáticos
        if self.button1.text() == "Start Record" or self.button1.text() == "Iniciar Grabación": 
            self.button1.setText(self.tr("Start Record"))
        else: 
            self.button1.setText(self.tr("Stop Record"))

        if self.SessionState:
            self.startButton.setText(self.tr("Log Out"))
        else:
            self.startButton.setText(self.tr("Log In"))

        self.button2.setText(self.tr("Capture Image"))
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
            msgBox.setWindowTitle(self.tr("Advertencia"))
            msgBox.setText(self.tr("La sesión está activa."))
            msgBox.setInformativeText(self.tr("Por favor, cierra la sesión antes de cerrar el programa."))
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
    
    @pyqtSlot(TelemetryMessage)
    def update_telemetry(self, telemetry: TelemetryMessage):
        temperature = telemetry.variables.get("Temperature", "N/A")
        humidity = telemetry.variables.get("Humidity", "N/A")
        x_slop = telemetry.variables.get("X slop", "N/A")
        y_slop = telemetry.variables.get("Y slop", "N/A")
        motor_status = telemetry.variables.get("Motor status", "N/A")
       
        telemetry_text = (f"{self.tr('Telemetry')}\n"
                  f"{self.tr('Temperature:')} {temperature} °C \n"
                  f"{self.tr('Humidity:')} {humidity} HR \n"
                  f"{self.tr('X slop:')} {x_slop} °\n"
                  f"{self.tr('Y slop:')} {y_slop} °")
        
        self.telemetry_label.setText(self.tr(telemetry_text))
        self.telemetry_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        if (motor_status == 0xC0):
            self.warning_text.setText(self.tr("No warnings."))
        elif (motor_status == 0xE0): 
            self.warning_text.setText(self.tr("Caution locked wheels."))
    
    
    
    
