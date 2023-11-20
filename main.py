from PyQt6.QtWidgets import QApplication
from modules.MainWindow import MainWindow
import sys

if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())