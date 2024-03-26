import sys
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QApplication
from PyQt6.QtCore import Qt

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.layout.setContentsMargins(100, 100, 100, 100)
        self.layout.setSpacing(100)

        self.setWindowTitle("Settings")
        self.setLayout(self.layout)

        settings_label = QLabel("Settings Page")
        self.layout.addWidget(settings_label, 0, 0, 1, 0, Qt.AlignmentFlag.AlignCenter)

        # Adjust size here, assuming screen_size is obtained the same way as in MainWindow
        app = QApplication.instance()
        screen = app.primaryScreen()
        screen_size = screen.size()
        self.resize(int(screen_size.width() / 2), int(screen_size.height() / 2))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    settings_window = SettingsWindow()
    settings_window.show()
    sys.exit(app.exec())
