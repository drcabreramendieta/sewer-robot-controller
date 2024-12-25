from PyQt6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QApplication, QPushButton, QHBoxLayout, QFileDialog, QMessageBox
from Inspection.ports.input import SessionServicesPort
import os 

class SessionsListDialog(QDialog):
    def __init__(self, control_session:SessionServicesPort ):
        super().__init__()
        self.control_session = control_session
        self.setWindowTitle(self.tr("Session Names"))
        self.resize(400, 300)
        layout = QVBoxLayout()
        
        self.listWidget = QListWidget()
        session_names = self.control_session.get_sessions()
        self.listWidget.addItems(session_names)
        layout.addWidget(self.listWidget)
        
        self.downloadButton = QPushButton(self.tr("Download"))
        self.cancelButton = QPushButton(self.tr("Cancel"))
        
        self.downloadButton.clicked.connect(self.download)
        self.cancelButton.clicked.connect(self.reject)
        
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.downloadButton)
        buttonLayout.addWidget(self.cancelButton)
        
        layout.addLayout(buttonLayout)
        
        self.setLayout(layout)
        self.move_to_center()

    
     

    def move_to_center(self):
        screen = QApplication.primaryScreen()
        screenGeometry = screen.geometry()
        
        centerX = screenGeometry.center().x()
        centerY = screenGeometry.center().y()
        
        self.move(centerX - self.width() // 2, centerY - self.height() // 2)

    def download(self):
        selected_session = self.listWidget.currentItem().text() if self.listWidget.currentItem() else None
        if selected_session:
            baseFolder = QFileDialog.getExistingDirectory(self, self.tr("Choose folder to save session"))

            if baseFolder:
                sessionFolder = os.path.join(baseFolder, selected_session)
                print(sessionFolder)
                try:
                    os.makedirs(sessionFolder, exist_ok=True)
                    print(f"Se creó la carpeta para la sesión: '{sessionFolder}'.")
                    download_session_result = self.control_session.download_session(selected_session, sessionFolder)
                    
                    if download_session_result is True:
                        QMessageBox.information(self, self.tr("Saved Session"), self.tr("Successful session save."))
                        self.accept()
                    elif download_session_result is False:
                        QMessageBox.critical(self, self.tr("Error"), self.tr("Session was not saved correctly."))
                    else:
                        # Manejar el caso cuando no se encuentra contenido para descargar
                        QMessageBox.warning(self, self.tr("Content not found"), self.tr("The session does not have videos or images to download."))
                except Exception as e:
                    print(self.tr(f"Error creating folder for session: {e}"))
                    QMessageBox.critical(self, self.tr("Error"), f"{self.tr('Error creating folder for session:')} {e}")
        else:
            QMessageBox.warning(self, self.tr("Session selection"),self.tr( "No session selected."))

    