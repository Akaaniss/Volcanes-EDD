import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QComboBox, QLineEdit, QPushButton, QTextEdit


class VentanaDeBusqueda(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Búsqueda de Volcanes")
        self.setGeometry(100, 100, 400, 300)

        self.combobox = QComboBox(self)
        self.combobox.addItems(["Región", "Nombre del volcán", "Año", "VEI"])
        self.combobox.setCurrentIndex(0)
        self.combobox.currentIndexChanged.connect(self.combobox_region)
        self.combobox.move(50, 30)

        self.input_entry = QLineEdit(self)
        self.input_entry.move(50, 70)

        self.search_button = QPushButton("Buscar", self)
        self.search_button.clicked.connect(self.realizar_busqueda)
        self.search_button.move(50, 110)

        self.result_textedit = QTextEdit(self)
        self.result_textedit.setGeometry(50, 150, 300, 120)

    def combobox_region(self, index):
        if index == 0:
            region_combobox = QComboBox(self)
            region_combobox.addItems(
                [
                    "Arica y Parinacota",
                    "Tarapacá",
                    "Antofagasta",
                    "Atacama",
                    "Coquimbo",
                    "Valparaíso",
                    "Metropolitana",
                    "O'Higgins",
                    "Maule",
                    "Ñuble",
                    "Biobío",
                    "La Araucanía",
                    "Los Ríos",
                    "Los Lagos",
                    "Aysén",
                    "Magallanes",
                ]
            )
            region_combobox.setCurrentIndex(0)
            region_combobox.move(50, 70)
            self.input_entry.setText(region_combobox.currentText())
            self.input_entry.setDisabled(True)
        else:
            self.input_entry.setDisabled(False)

    def realizar_busqueda(self):
        criteria = self.combobox.currentText()
        value = self.input_entry.text()

        try:
            with open("erupcionesdesde1903v2.csv", "r", encoding="latin-1") as file:
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

                self.result_textedit.clear()
                self.result_textedit.append(result_text)
            else:
                self.result_textedit.clear()
                self.result_textedit.append("No se encontraron resultados para la búsqueda.")
        except FileNotFoundError:
            self.result_textedit.clear()
            self.result_textedit.append("No se encontró el archivo 'erupcionesdesde1903v2.csv'.")


app = QApplication([])
ventana = VentanaDeBusqueda()
ventana.show()
app.exec()
