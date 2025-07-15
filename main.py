#main.py
#Main application file to run the statistics helper program.
#7/9/2025
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from GUI_Control.loading_screen import LoadingScreen
from GUI_Control.statsGui import StatsApp

def load_application():
    """Simulate loading time and import heavy modules"""
    # Import heavy modules here to simulate loading time
    from GUI_Control.statsGui import StatsApp
    return StatsApp

if __name__ == "__main__":
    print("Starting Statistics Helper Application...")
    app = QApplication(sys.argv)
    
    # Show loading screen
    loading_screen = LoadingScreen()
    loading_screen.show()
    
    # Process events to show the loading screen
    app.processEvents()
    
    # Simulate loading steps
    loading_steps = [
        "Initializing application...",
        "Loading statistics libraries...", 
        "Loading BERT tokenizer...",
        "Setting up user interface...",
        "Ready!"
    ]
    
    def load_step(step_index):
        if step_index < len(loading_steps):
            loading_screen.update_progress(loading_steps[step_index])
            app.processEvents()
            
            # Schedule next step
            QTimer.singleShot(500, lambda: load_step(step_index + 1))
        else:
            # Loading complete - show main window
            window = StatsApp()
            window.show()
            loading_screen.finish(window)
    
    # Start loading process
    load_step(0)
    
    sys.exit(app.exec())