import sys
import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

class ventanadeBusqueda(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Busqueda de Volcanes")
        
        self.central_widget= QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout=QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        




















if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ventanadeBusqueda()
    window.show()
    sys.exit(app.exec())