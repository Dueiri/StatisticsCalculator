#main.py
#Main application file to run the statistics helper program.
#7/9/2025
import sys
from GUI_Control.statsGui import StatsApp
from PyQt6.QtWidgets import QApplication
if __name__ == "__main__":
    print("Starting Statistics Helper Application...")
    app = QApplication(sys.argv)
    window = StatsApp()
    window.show()
    sys.exit(app.exec())