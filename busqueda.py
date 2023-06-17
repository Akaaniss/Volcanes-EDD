import csv
from PyQt6.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QComboBox

class ventanadeBusqueda(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Busqueda de Volcanes")
        self.setGeometry(300,300,400,300)

        self.central_widget= QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.combobox = QComboBox()

        self.combobox.addItem("Región")
        self.combobox.addItem("Nombre del volcan")
        self.combobox.addItem("Año")
        self.combobox.addItem("VEI")

        self.layout.addWidget(self.combobox)
        
    def busquedaManual(self):
        busquedaTexto=self.busquedaTexto_edit.text()
        with open('erupcionesdesde1903v2.csv', newline='')as csvfile:
            reader=csv.DictReader(csvfile)
            for row in reader:
                if busquedaTexto.lower() in row['NombreVolcan'].lower():
                    print(row)











