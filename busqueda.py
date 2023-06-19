import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QWidget
import pandas as pd

# Cargar los datos desde el archivo CSV
data = pd.read_csv('erupcionesdesde1903v2.csv', delimiter=';', encoding='latin1')

# Convertir las fechas al formato correcto
data['Start Date'] = pd.to_datetime(data['Start Date'], dayfirst=True)

# Reemplazar las comas por puntos en las coordenadas geográficas
data['Latitude'] = data['Latitude'].str.replace(',', '.')
data['Longitude'] = data['Longitude'].str.replace(',', '.')

class VentanaBusqueda(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Búsqueda de Erupciones Volcánicas")
        self.setGeometry(300, 300, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Etiqueta y caja de texto para ingresar la búsqueda
        self.label_busqueda = QLabel("Buscar Volcán:")
        self.layout.addWidget(self.label_busqueda)

        self.entry_busqueda = QLineEdit()
        self.layout.addWidget(self.entry_busqueda)

        # Botón de búsqueda
        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.clicked.connect(self.buscar_erupcion)
        self.layout.addWidget(self.btn_buscar)

        # Cuadro de texto para mostrar los resultados
        self.text_resultados = QTextEdit()
        self.text_resultados.setFixedSize(800, 400)
        self.layout.addWidget(self.text_resultados)

    def buscar_erupcion(self):
        # Obtener el valor ingresado en la caja de texto de búsqueda
        busqueda = self.entry_busqueda.text()

        # Filtrar los datos según el criterio de búsqueda
        resultados = data[data['Volcano Name'].str.contains(busqueda, case=False)]

        # Mostrar los resultados en el cuadro de texto de resultados
        self.text_resultados.clear()
        self.text_resultados.setPlainText(resultados.to_string(index=False))

