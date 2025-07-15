from PyQt6.QtWidgets import QSplashScreen
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont

class LoadingScreen(QSplashScreen):
    def __init__(self):
        # Create a simple colored background or use an image
        pixmap = QPixmap(400, 300)
        pixmap.fill(Qt.GlobalColor.darkBlue)
        super().__init__(pixmap, Qt.WindowType.WindowStaysOnTopHint)
        
        # Setup the loading screen layout
        self.setupUI()
        
    def setupUI(self):
        # Create loading text
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        
        self.showMessage("Loading Statistics Helper...", 
                        Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom,
                        Qt.GlobalColor.white)
        
    def update_progress(self, message):
        self.showMessage(message, 
                        Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom,
                        Qt.GlobalColor.white)