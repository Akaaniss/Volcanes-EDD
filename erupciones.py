import os
import sys
import csv
import matplotlib.pyplot as plt
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QComboBox, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem

current_dir = os.path.dirname(os.path.abspath(__file__))
relative_path = os.path.join(current_dir, "erupcionesdesde1903.csv")

data = []
with open(relative_path, 'r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        data.append(row)


class VentanaBusqueda(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Búsqueda de Volcanes")
        self.setGeometry(150, 150, 580, 560)

        self.archivo_csv_actual = "erupcionesdesde1903.csv"#archivo actual

        self.combobox = QComboBox(self)
        self.combobox.addItems(["Nombre del volcán", "Región", "Año", "VEI"])
        self.combobox.setCurrentIndex(0)
        self.combobox.currentIndexChanged.connect(self.comboboxRegion)
        self.combobox.move(50, 30)
        self.combobox.setFixedWidth(250)

        self.entradatexto = QLineEdit(self)
        self.entradatexto.move(50, 70)
        self.entradatexto.setFixedWidth(250)

        self.regionCombobox = QComboBox(self)
        self.regionCombobox.addItems(
            [
                "Region de Arica y Parinacota",
                "Region de Tarapaca",
                "Region de Antofagasta",
                "Región de Atacama",
                "Region de Coquimbo",
                "Region de Valparaiso",
                "Region Metropolitana",
                "Region de O'Higgins",
                "Region del Maule",
                "Region de Nuble",
                "Region del Biobio",
                "Region de La Araucania",
                "Region de Los Rios",
                "Region de Los Lagos",
                "Region de Aysen",
                "Region de Magallanes y la Antartica Chilena",
            ]
        )
        self.regionCombobox.setCurrentIndex(0)
        self.regionCombobox.move(50, 70)
        self.regionCombobox.setFixedWidth(250)
        self.regionCombobox.hide()

        self.botonBusqueda = QPushButton("Buscar", self)
        self.botonBusqueda.clicked.connect(self.realizarBusqueda)
        self.botonBusqueda.move(50, 110)

        self.botonGrafico = QPushButton("Gráfico Erupciones por Año", self)
        self.botonGrafico.clicked.connect(self.generarGrafico)
        self.botonGrafico.move(200, 110)
        self.botonGrafico.setFixedWidth(160)

        self.botonGraficoVEI = QPushButton("Gráfico VEI", self)
        self.botonGraficoVEI.clicked.connect(self.generarGraficoVEI)
        self.botonGraficoVEI.move(410, 110)
        self.botonGraficoVEI.setFixedWidth(100) 


        self.resultadoTabla = QTableWidget(self)
        self.resultadoTabla.setGeometry(50, 150, 520, 400)
        self.resultadoTabla.setColumnCount(5)
        self.resultadoTabla.setHorizontalHeaderLabels(["Región", "Nombre del volcán", "Año", "VEI", "Coordenadas"])

        self.mensajeLabel = QLabel(self)
        self.mensajeLabel.setGeometry(50, 150, 500, 30)
        self.mensajeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mensajeLabel.setStyleSheet("color: black; font-weight: bold;")

        self.comboboxArchivo = QComboBox(self)
        self.comboboxArchivo.addItems(["Erupciones desde 1903", "Volcanes del Mundo"])  # Agrega los nombres de tus archivos CSV aquí
        self.comboboxArchivo.currentIndexChanged.connect(self.cambiarArchivo)
        self.comboboxArchivo.move(320, 30)
        self.comboboxArchivo.setFixedWidth(250)
        opciones_erupciones = ["Nombre del volcán", "Región", "Año", "VEI"]
        opciones_volcano_data = ["Nombre del volcán", "País", "Año"]

        self.opciones_csv = {
                "erupcionesdesde1903.csv": opciones_erupciones,
                "volcano_data_2010.csv": opciones_volcano_data
                }

    def actualizarComboBox(self):
        opciones = self.opciones_csv.get(self.archivo_csv_actual, [])
        self.combobox.clear()
        self.combobox.addItems(opciones)
        if "Región" in opciones:
            self.entradatexto.hide()
            self.regionCombobox.show()
        else:
            self.regionCombobox.hide()
            self.entradatexto.show()

    def cambiarArchivo(self, index):
        archivos_csv = ["erupcionesdesde1903.csv", "volcano_data_2010.csv"]  # Agrega los nombres de tus archivos CSV aquí
        self.archivo_csv_actual = archivos_csv[index]
        self.actualizarDatos()
        self.actualizarComboBox()
        self.realizarBusqueda()

    def actualizarDatos(self):
        data = []
        with open(self.archivo_csv_actual, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                data.append(row)
        self.datos = data




    def comboboxRegion(self, index):
        if index == 1:
            self.entradatexto.hide()
            self.regionCombobox.show()
        else:
            self.regionCombobox.hide()
            self.entradatexto.show()

    def realizarBusqueda(self):
        criterio = self.combobox.currentText()

        if criterio == "Nombre del volcán" or criterio == "Región":
            if criterio == "Región":
                valor = self.regionCombobox.currentText()
            else:
                valor = self.entradatexto.text()
            self.BusquedaBinaria(criterio, valor)
        elif criterio == "Año" or criterio == "VEI":
            valor = self.entradatexto.text()
            self.BusquedaLineal(criterio, valor)

    def BusquedaBinaria(self, criterio, valor):
        encontrarVolcan = []

        if criterio == "Nombre del volcán" or criterio == "Región":
            sorted_data = sorted(data, key=lambda x: x[criterio])

            if criterio == "Región":
                left = 0
                right = len(sorted_data) - 1
                while left <= right:
                    mid = (left + right) // 2
                    if sorted_data[mid][criterio] == valor:
                        encontrarVolcan.append(sorted_data[mid])
                        i = mid - 1
                        while i >= 0 and sorted_data[i][criterio] == valor:
                            encontrarVolcan.append(sorted_data[i])
                            i -= 1
                        i = mid + 1
                        while i < len(sorted_data) and sorted_data[i][criterio] == valor:
                            encontrarVolcan.append(sorted_data[i])
                            i += 1
                        break
                    elif sorted_data[mid][criterio] < valor:
                        left = mid + 1
                    else:
                        right = mid - 1

            else:
                left = 0
                right = len(sorted_data) - 1
                while left <= right:
                    mid = (left + right) // 2
                    if sorted_data[mid][criterio].lower() == valor.lower():
                        encontrarVolcan.append(sorted_data[mid])
                        i = mid - 1
                        while i >= 0 and sorted_data[i][criterio].lower() == valor.lower():
                            encontrarVolcan.append(sorted_data[i])
                            i -= 1
                        i = mid + 1
                        while i < len(sorted_data) and sorted_data[i][criterio].lower() == valor.lower():
                            encontrarVolcan.append(sorted_data[i])
                            i += 1
                        break
                    elif sorted_data[mid][criterio].lower() < valor.lower():
                        left = mid + 1
                    else:
                        right = mid - 1

        self.mostrarResultados(encontrarVolcan)

    def BusquedaLineal(self, criterio, valor):
        encontrarVolcan = []

        for item in data:
            if criterio == "Año" and item["Start Date"].split("-")[0] == valor:
                encontrarVolcan.append(item)
            elif criterio == "VEI" and item["Max. VEI"] == valor:
                encontrarVolcan.append(item)

        self.mostrarResultados(encontrarVolcan)

    def mostrarResultados(self, resultados):
        if resultados:
            self.resultadoTabla.setVisible(True)
            self.resultadoTabla.setRowCount(len(resultados))
            for row, item in enumerate(resultados):
                self.resultadoTabla.setItem(row, 0, QTableWidgetItem(item["Región"]))
                self.resultadoTabla.setItem(row, 1, QTableWidgetItem(item["Nombre del volcán"]))
                self.resultadoTabla.setItem(row, 2, QTableWidgetItem(item["Start Date"]))
                self.resultadoTabla.setItem(row, 3, QTableWidgetItem(item["Max. VEI"]))
                self.resultadoTabla.setItem(row, 4, QTableWidgetItem(f"{item['Latitude']}, {item['Longitude']}"))
            self.mensajeLabel.setText("")
        else:
            self.resultadoTabla.clearContents()
            self.resultadoTabla.setRowCount(0)
            self.resultadoTabla.setVisible(False)
            self.mensajeLabel.setText("No se encontraron resultados.")

        self.resultadoTabla.resizeColumnsToContents()

    def generarGraficoVEI(self):
        magnitudes = []
        for item in data:
            magnitudes.append(float(item["Max. VEI"]))

        plt.figure(figsize=(8, 6))
        plt.hist(magnitudes, bins=10)
        plt.xlabel("Magnitud de la Explosión (VEI)")
        plt.ylabel("Cantidad")
        plt.title("Distribución de Magnitudes de Explosiones de Volcanes")
        plt.show()

    def generarGrafico(self):
        anos = []
        explosions_per_year = {}
        for item in data:
            year = item["Start Date"].split("-")[2]
            if year in explosions_per_year:
                explosions_per_year[year] += 1
            else:
                explosions_per_year[year] = 1

        plt.figure(figsize=(15, 6))  # se ajusta el tamaño de la ventana para que los años se visualzen mejor
        plt.bar(explosions_per_year.keys(), explosions_per_year.values())
        plt.xlabel("Año")
        plt.ylabel("Explosiones")
        plt.title("Explosiones de Volcanes por Año")
        plt.xticks(rotation=60)  # rota los años en 60 gradoss para que se vean mejor
        plt.tight_layout()  
        plt.show()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaBusqueda()
    ventana.show()
    sys.exit(app.exec())
