import sys
from PyQt6.QtWidgets import QApplication
from views.MainWindow import MainWindow

# Create an instance of the application
root = QApplication(sys.argv)

app = MainWindow()
app.show()

sys.exit(root.exec())