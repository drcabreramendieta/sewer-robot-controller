from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QApplication
from PyQt6.QtCore import pyqtSignal
"""Dialog module for entering and validating inspection session names.

This module provides a modal dialog for users to input names for new 
inspection sessions, with input validation and centered positioning.
"""
class SessionNameDialog(QDialog):
    """
    SessionNameDialog Dialog for entering new inspection session names.
    
    A modal dialog that allows users to enter and validate session names.
    Provides a text input field and save/cancel buttons. The dialog is
    centered on screen and validates input before allowing save.

    Args:
        QDialog (_type_): _description_
    """
    def __init__(self):
        """Initialize session name dialog.
        
        Creates and configures the dialog window with:
        - Text input field for session name
        - Save button (disabled until valid input)
        - Cancel button
        - Centered position on screen
        """      
       
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
        """
        getSessionName Get the entered session name.

        Returns:
            str: The entered session name with leading/trailing whitespace removed
        """       
        return self.lineEdit.text().strip()

    def move_to_center(self):
        """Validate session name input.
        
        move_to_center Enables/disables save button based on whether the input field
        contains non-whitespace characters.
        """      
        screen = QApplication.screens()[0]
        screenGeometry = screen.geometry()
            
        centerX = screenGeometry.center().x()
        centerY = screenGeometry.center().y()
        
        self.move(centerX - self.width() // 2, centerY - self.height() // 2)

    def checkInput(self):
        """Validate session name input.
        
        checkInput Enables/disables save button based on whether the input field
        contains non-whitespace characters.
        """        
        self.acceptButton.setEnabled(bool(self.lineEdit.text().strip()))
   
