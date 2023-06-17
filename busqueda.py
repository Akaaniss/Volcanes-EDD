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
        self.combobox.currentIndexChanged.connect(self.comboBoxRegion)

    def comboBoxRegion (self, index):
        while self.layout.count() > 1:
            item = self.layout.takeAt(1)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater() 

        if index == 0:
            region_combobox = QComboBox()
            region_combobox.addItem("Arica y Parinacota")
            region_combobox.addItem("Tarapacá")
            region_combobox.addItem("Antofagasta")
            region_combobox.addItem("Atacama")
            region_combobox.addItem("Coquimbo")
            region_combobox.addItem("Valparaíso")
            region_combobox.addItem("Metropolitana")
            region_combobox.addItem("O'Higgins")
            region_combobox.addItem("Maule")
            region_combobox.addItem("Ñuble")
            region_combobox.addItem("Biobío")
            region_combobox.addItem("La Araucanía")
            region_combobox.addItem("Los Ríos")
            region_combobox.addItem("Los Lagos")
            region_combobox.addItem("Aysén")
            region_combobox.addItem("Magallanes")
            self.layout.addWidget(region_combobox)
        
    def busquedaManual(self):
        busquedaTexto=self.busquedaTexto_edit.text()
        with open('erupcionesdesde1903v2.csv', newline='')as csvfile:
            reader=csv.DictReader(csvfile)
            for row in reader:
                if busquedaTexto.lower() in row['NombreVolcan'].lower():
                    print(row)











