import csv
from PyQt6.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QComboBox, QTextEdit

class ventanadeBusqueda(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Búsqueda de Volcanes")
        self.setGeometry(300, 300, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.combobox = QComboBox()

        self.combobox.addItem("Región")
        self.combobox.addItem("Nombre del volcán")
        self.combobox.addItem("Año")
        self.combobox.addItem("VEI")

        self.layout.addWidget(self.combobox)
        self.combobox.currentIndexChanged.connect(self.comboBoxRegion)

        self.result_textedit = QTextEdit()  # Agregar QTextEdit
        self.layout.addWidget(self.result_textedit)

    def comboBoxRegion(self, index):
        while self.layout.count() > 2:  # Ajustar el recuento para incluir QTextEdit
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

        elif index == 1:
            label = QLabel("Nombre del volcán:")
            self.layout.addWidget(label)

            line_edit = QLineEdit()
            self.layout.addWidget(line_edit)

            search_button = QPushButton("Buscar")
            search_button.clicked.connect(lambda: self.realizarBusqueda("Nombre del volcán", line_edit.text()))
            self.layout.addWidget(search_button)

        elif index == 2:
            label = QLabel("Año:")
            self.layout.addWidget(label)

            line_edit = QLineEdit()
            self.layout.addWidget(line_edit)

            search_button = QPushButton("Buscar")
            search_button.clicked.connect(lambda: self.realizarBusqueda("Año", line_edit.text()))
            self.layout.addWidget(search_button)

        elif index == 3:
            label = QLabel("VEI:")
            self.layout.addWidget(label)

            line_edit = QLineEdit()
            self.layout.addWidget(line_edit)

            search_button = QPushButton("Buscar")
            search_button.clicked.connect(lambda: self.realizarBusqueda("VEI", line_edit.text()))
            self.layout.addWidget(search_button)

    def realizarBusqueda(self, criteria, value):
        try:
            with open("erupcionesdesde1903v2.csv","r", encoding='utf-8-sig') as file:
                reader = csv.DictReader(file, delimiter=";")
                encontrarVolcan = []
                for row in reader:
                    if criteria in row and row[criteria].lower() == value.lower():
                        encontrarVolcan.append(row)
                        print(row)

            if encontrarVolcan:
                result_text = "Resultados de la búsqueda:\n\n"
                for volcan in encontrarVolcan:
                    result_text += "-" * 30 + "\n"
                    result_text += "Región: {}\n".format(volcan['Región'])
                    result_text += "Nombre del volcán: {}\n".format(volcan['Nombre del volcán'])
                    result_text += "Año: {}\n".format(volcan['Año'])
                    result_text += "VEI: {}\n".format(volcan['VEI'])

                self.result_textedit.setPlainText(result_text)
            else:
                self.result_textedit.setPlainText("No se encontraron resultados para la búsqueda.")
        except FileNotFoundError:
            self.result_textedit.setPlainText("No se encontró el archivo 'erupcionesdesde1903v2.csv'.")

