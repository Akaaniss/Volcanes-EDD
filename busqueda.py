import os
import sys
import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QComboBox, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem

csv_file_path = os.path.abspath(r'C:\Users\fidja\Downloads\Volcanes-EDD-main\Volcanes-EDD-main\erupcionesdesde1903.csv')

data = []
with open(csv_file_path, 'r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        data.append(row)

class VentanaBusqueda(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Búsqueda de Volcanes")
        self.setGeometry(100, 100, 600, 400)

        self.combobox = QComboBox(self)
        self.combobox.addItems(["Nombre del volcán", "Región", "Año", "VEI"])
        self.combobox.setCurrentIndex(0)
        self.combobox.currentIndexChanged.connect(self.combobox_region)
        self.combobox.move(50, 30)

        self.input_entry = QLineEdit(self)
        self.input_entry.move(50, 70)

        self.region_combobox = QComboBox(self)
        self.region_combobox.addItems(
            [
                "Region de Arica y Parinacota",
                "Region de Tarapaca",
                "Region de Antofagasta",
                "Region de Atacama",
                "Region de Coquimbo",
                "Region de Valparaiso",
                "Region Metropolitana",
                "Region de O'Higgins",
                "Region del Maule",
                "Region de Nuble",
                "Region del Bio Bio",
                "Region de La Araucania",
                "Region de Los Rios",
                "Region de Los Lagos",
                "Region de Aysen",
                "Region de Magallanes y la Antartida Chilena",
            ]
        )
        self.region_combobox.setCurrentIndex(0)
        self.region_combobox.move(50, 70)
        self.region_combobox.hide()

        self.search_button = QPushButton("Buscar", self)
        self.search_button.clicked.connect(self.realizar_busqueda)
        self.search_button.move(50, 110)

        self.result_table = QTableWidget(self)
        self.result_table.setGeometry(50, 150, 500, 240)
        self.result_table.setColumnCount(5)
        self.result_table.setHorizontalHeaderLabels(["Región", "Nombre del volcán", "Año", "VEI", "Coordenadas"])

    def combobox_region(self, index):
        if index == 1:
            self.input_entry.hide()
            self.region_combobox.show()
        else:
            self.region_combobox.hide()
            self.input_entry.show()

    def realizar_busqueda(self):
        criteria = self.combobox.currentText()
        if criteria == "Región":
            value = self.region_combobox.currentText()
        else:
            value = self.input_entry.text()

        encontrar_volcan = []
        for volcan in data:
            if criteria == "Nombre del volcán" and volcan["Volcano Name"].lower() == value.lower():
                encontrar_volcan.append(volcan)
            elif criteria == "Región" and volcan["Region"].lower() == value.lower():
                encontrar_volcan.append(volcan)
            elif criteria == "Año" and value == volcan["Start Date"].split("-")[2]:
                encontrar_volcan.append(volcan)
            elif criteria == "VEI" and value == volcan["Max. VEI"]:
                encontrar_volcan.append(volcan)

        self.mostrar_resultados(encontrar_volcan)

    def mostrar_resultados(self, volcanes):
        self.result_table.setRowCount(len(volcanes))

        for index, volcan in enumerate(volcanes):
            region_item = QTableWidgetItem(volcan["Region"])
            nombre_item = QTableWidgetItem(volcan["Volcano Name"])
            año_item = QTableWidgetItem(volcan["Start Date"].split("-")[2])
            vei_item = QTableWidgetItem(volcan["Max. VEI"])

            coordenadas = volcan.get("Latitude (dd)", "") + ", " + volcan.get("Longitude (dd)", "")
            coordenadas_item = QTableWidgetItem(coordenadas)

            self.result_table.setItem(index, 0, region_item)
            self.result_table.setItem(index, 1, nombre_item)
            self.result_table.setItem(index, 2, año_item)
            self.result_table.setItem(index, 3, vei_item)
            self.result_table.setItem(index, 4, coordenadas_item)

        self.result_table.resizeColumnsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaBusqueda()
    ventana.show()
    sys.exit(app.exec())
