import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QComboBox
import sys

data = []
with open('erupciones.csv', 'r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        data.append(row)

class VentanaDeBusqueda(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Búsqueda de Erupciones Volcánicas")
        self.setGeometry(300, 300, 400, 300)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.text_resultados = QTextEdit()
        self.layout.addWidget(self.text_resultados)

        self.setCentralWidget(self.central_widget)

        self.combobox = QComboBox()
        self.combobox.addItem("Región")
        self.combobox.addItem("Nombre del volcán")
        self.combobox.addItem("Año")
        self.combobox.addItem("VEI")
        self.combobox.setCurrentIndex(-1)
        self.layout.addWidget(self.combobox)

        self.combobox.currentIndexChanged.connect(self.comboBoxSegunda)

    def comboBoxSegunda(self, index):
        while self.layout.count() > 1:
            item = self.layout.takeAt(1)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        if index == 0:
            region_combobox = QComboBox()
            region_combobox.setCurrentIndex(-1)
            region_combobox.addItem("Region de Arica y Parinacota")
            region_combobox.addItem("Region de Tarapacá")
            region_combobox.addItem("Region de Antofagasta")
            region_combobox.addItem("Region de Atacama")
            region_combobox.addItem("Region de Coquimbo")
            region_combobox.addItem("Region de Valparaíso")
            region_combobox.addItem("Region de Metropolitana")
            region_combobox.addItem("Region de O'Higgins")
            region_combobox.addItem("Region del Maule")
            region_combobox.addItem("Region de Ñuble")
            region_combobox.addItem("Region de Biobío")
            region_combobox.addItem("Region de La Araucanía")
            region_combobox.addItem("Region de Los Ríos")
            region_combobox.addItem("Region de Los Lagos")
            region_combobox.addItem("Region de Aysén")
            region_combobox.addItem("Region de Magallanes")
            boton_buscar = QPushButton("Buscar")
            self.layout.addWidget(region_combobox)
            self.layout.addWidget(boton_buscar)
            boton_buscar.clicked.connect(lambda: self.realizarBusqueda("Region", region_combobox.currentText()))

        elif index == 1:
            self.label_busqueda = QLabel("Buscar Volcán:")
            self.layout.addWidget(self.label_busqueda)

            self.entry_busqueda = QLineEdit()
            self.layout.addWidget(self.entry_busqueda)

            self.btn_buscar = QPushButton("Buscar")
            self.btn_buscar.clicked.connect(self.buscar_erupcion)
            self.layout.addWidget(self.btn_buscar)

        elif index == 2:
            label = QLabel("Año:")
            self.layout.addWidget(label)

            line_edit = QLineEdit()
            self.layout.addWidget(line_edit)

            search_button = QPushButton("Buscar")
            search_button.clicked.connect(lambda: self.realizarBusqueda("Start Date", line_edit.text()))
            self.layout.addWidget(search_button)

        elif index == 3:
            vei_combobox = QComboBox()
            vei_combobox.addItem("0")
            vei_combobox.addItem("1")
            vei_combobox.addItem("2")
            vei_combobox.addItem("3")
            vei_combobox.addItem("4")
            vei_combobox.addItem("5")
            vei_combobox.addItem("6")
            vei_combobox.addItem("7")
            vei_combobox.addItem("8")
            search_button = QPushButton("Buscar")
            self.layout.addWidget(vei_combobox)
            self.layout.addWidget(search_button)
            search_button.clicked.connect(lambda: self.realizarBusqueda("Max. VEI", vei_combobox.currentText()))

    def buscar_erupcion(self):
        busqueda = self.entry_busqueda.text()
        resultados = []
        for row in data:
            if busqueda.lower() in row['Volcano Name'].lower():
                resultados.append(row)
        self.mostrar_resultados(resultados)

    def realizar_busqueda(self):
            criteria = self.combobox.currentText()
            value = self.input_entry.text()

            try:
                with open("erupciones.csv", "r", encoding="latin-1") as file:
                    reader = csv.DictReader(file, delimiter=";")
                    encontrar_volcan = []
                    for row in reader:
                        if criteria == "Región" and row["Region"].lower() == value.lower():
                            encontrar_volcan.append(row)
                        elif criteria == "Nombre del volcán" and row["Volcano Name"].lower() == value.lower():
                            encontrar_volcan.append(row)
                        elif criteria == "Año" and row["Start Date"] == value:
                            encontrar_volcan.append(row)
                        elif criteria == "VEI" and row["Max. VEI"] == value:
                            encontrar_volcan.append(row)

                if encontrar_volcan:
                    result_text = "Resultados de la búsqueda:\n\n"
                    for volcan in encontrar_volcan:
                        result_text += "-" * 30 + "\n"
                        result_text += "Región: {}\n".format(volcan["Region"])
                        result_text += "Nombre del volcán: {}\n".format(volcan["Volcano Name"])
                        result_text += "Año: {}\n".format(volcan["Start Date"])
                        result_text += "VEI: {}\n".format(volcan["Max. VEI"])
                        result_text += "Coordenadas: {}\n".format(volcan["Latitude"] + ", " + volcan["Longitude"])
                        result_text += "\n"

                    self.result_textedit.setText(result_text)
                else:
                    self.result_textedit.setText("No se encontraron volcanes que coincidan con los criterios de búsqueda.")

            except FileNotFoundError:
                self.result_textedit.setText("No se encontró el archivo 'erupcionesdesde1903v2.csv'.")

    def mostrar_resultados(self, resultados):
        self.text_resultados.clear()

        if len(resultados) == 0:
            self.text_resultados.setPlainText("No se encontraron resultados.")
        else:
            for row in resultados:
                texto = "Volcano Name: {}\nVolcano Name Ref: {}\nRegion: {}\nStart Date: {}\nMax. VEI: {}\nLatitude: {}\nLongitude: {}\n\n".format(
                    row.get('Volcano Name', ''),
                    row.get('Volcano Name Ref', ''),
                    row.get('Region', ''),
                    row.get('Start Date', ''),
                    row.get('Max. VEI', ''),
                    row.get('Latitude', ''),
                    row.get('Longitude', '')
                )
                self.text_resultados.insertPlainText(texto)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaDeBusqueda()
    ventana.show()
    sys.exit(app.exec())

