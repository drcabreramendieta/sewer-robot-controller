from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QApplication
from PyQt6.QtCore import pyqtSignal

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
   
