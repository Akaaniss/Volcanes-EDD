import csv
from PyQt6.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

class ventanadeBusqueda(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Busqueda de Volcanes")
        self.setGeometry(100,100,400,200)

        self.central_widget= QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout=QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        


















