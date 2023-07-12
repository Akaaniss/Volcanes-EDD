import os
import sys
import csv
import matplotlib.pyplot as plt
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QComboBox, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem

class VentanaBusqueda(QMainWindow):
    current_figure = None
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Búsqueda de Volcanes")
        self.setGeometry(150, 150, 580, 560)

        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.relative_path = os.path.join(self.current_dir, "erupcionesdesde1903.csv")

        self.data = []
        self.archivo_csv_actual = "erupcionesdesde1903.csv"  # archivo actual
        self.busqueda_realizada = False  # Bandera para indicar si se ha realizado una búsqueda

        self.load_data()
        self.create_widgets()

    def load_data(self):
        with open(self.archivo_csv_actual, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                self.data.append(row)

    def create_widgets(self):
        self.combobox = QComboBox(self)
        self.combobox.addItems(["Nombre del volcán", "Región", "Año", "VEI"])
        self.combobox.setCurrentIndex(1)
        self.combobox.currentIndexChanged.connect(self.comboboxRegion)
        self.combobox.move(50, 30)
        self.combobox.setFixedWidth(250)

        self.entradatexto = QLineEdit(self)
        self.entradatexto.move(50, 70)
        self.entradatexto.setFixedWidth(250)

        self.regionCombobox = QComboBox(self)
        self.regionCombobox.addItems(["Region de Arica y Parinacota", "Region de Tarapaca", "Region de Antofagasta", "Región de Atacama", "Region de Coquimbo", "Region de Valparaiso", "Region Metropolitana", "Region de O'Higgins", "Region del Maule", "Region de Nuble", "Region del Biobio", "Region de La Araucania", "Region de Los Rios", "Region de Los Lagos", "Region de Aysen", "Region de Magallanes y la Antartica Chilena"])
        self.regionCombobox.setCurrentIndex(0)
        self.regionCombobox.move(50, 70)
        self.regionCombobox.setFixedWidth(250)
        self.regionCombobox.setVisible(False)  # Ocultar la comboBox de regiones al inicio

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

        self.mensajeLabel = QLabel(self)
        self.mensajeLabel.setGeometry(50, 150, 500, 30)
        self.mensajeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mensajeLabel.setStyleSheet("color: black; font-weight: bold;")

        self.comboboxArchivo = QComboBox(self)
        self.comboboxArchivo.addItems(["Erupciones desde 1903 en Chile", "Volcanes del Mundo"])  # Agrega los nombres de tus archivos CSV aquí
        self.comboboxArchivo.currentIndexChanged.connect(self.cambiarArchivo)
        self.comboboxArchivo.move(320, 30)
        self.comboboxArchivo.setFixedWidth(250)

        self.botonGraficoPais = QPushButton("Gráfico Erupciones por País", self)
        self.botonGraficoPais.clicked.connect(self.generarGraficoPais)
        self.botonGraficoPais.move(370, 110)
        self.botonGraficoPais.setFixedWidth(160)
        self.botonGraficoPais.hide()  # Ocultar el botón inicialmente


        opciones_erupciones = ["Región", "Nombre del Volcán", "Año", "VEI"]
        opciones_volcano_data = ["Nombre del volcán", "País", "Año",]

        self.opciones_csv = {
            "erupcionesdesde1903.csv": opciones_erupciones,
            "volcano_data_2010.csv": opciones_volcano_data
        }
        self.columnas_csv = {
            "erupcionesdesde1903.csv": ["Región", "Nombre del volcán", "Año", "VEI", "Coordenadas"],
            "volcano_data_2010.csv": ["Nombre del volcán", "País", "Año","Locacion", "Latitude", "Longitude"]
        }

        self.actualizarComboBox()
        self.actualizarDatos()
        self.realizarBusqueda()


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
        columnas_tabla = self.columnas_csv.get(self.archivo_csv_actual, [])
        self.resultadoTabla.setColumnCount(len(columnas_tabla))
        self.resultadoTabla.setHorizontalHeaderLabels(columnas_tabla)
        if self.archivo_csv_actual == "volcano_data_2010.csv":
            self.botonGrafico.hide()
            self.botonGraficoVEI.hide()
            self.botonGraficoPais.show()
        else:
            self.botonGrafico.show()
            self.botonGraficoVEI.show()
            self.botonGraficoPais.hide()


    def cambiarArchivo(self, index):
        archivos_csv = ["erupcionesdesde1903.csv", "volcano_data_2010.csv"]  # Agrega los nombres de tus archivos CSV aquí
        self.archivo_csv_actual = archivos_csv[index]
        self.actualizarDatos()
        self.busqueda_realizada = False
        self.actualizarComboBox()
        self.realizarBusqueda()
        if self.archivo_csv_actual == "volcano_data_2010.csv":
            self.botonGrafico.hide()
            self.botonGraficoVEI.hide()
        else:
            self.botonGrafico.show()
            self.botonGraficoVEI.show()

    def actualizarDatos(self):
        self.data = []
        with open(self.archivo_csv_actual, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                self.data.append(row)
        self.mostrarResultados([])  # Limpiar la tabla de resultados

    def comboboxRegion(self, index):
        criterio = self.combobox.currentText()
        if self.archivo_csv_actual == "erupcionesdesde1903.csv" and criterio == "Región":
            self.entradatexto.hide()
            self.regionCombobox.setVisible(True)  # Mostrar la comboBox de regiones si se selecciona "Región"
        else:
            self.regionCombobox.setVisible(False)  # Ocultar la comboBox de regiones en cualquier otro caso
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

            if self.archivo_csv_actual == "volcano_data_2010.csv":
                self.BusquedaLinealVolcanoData(criterio, valor)
            else:
                self.BusquedaLineal(criterio, valor)
        elif criterio == "País":
            valor = self.entradatexto.text()
            self.BusquedaLinealVolcanoData(criterio, valor)
        
        self.busqueda_realizada = True  # Actualizar la bandera de búsqueda realizada
        self.entradatexto.clear()
    def BusquedaBinaria(self, criterio, valor):
        encontrarVolcan = []

        if criterio == "Nombre del volcán" or criterio == "Región":
            sorted_data = sorted(self.data, key=lambda x: x[criterio])

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

            elif criterio == "Nombre del volcán":
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

        if self.archivo_csv_actual == "erupcionesdesde1903.csv":
            self.mostrarResultados(encontrarVolcan)
        elif self.archivo_csv_actual == "volcano_data_2010.csv":
            self.mostrarResultadosDATA(encontrarVolcan)



    def BusquedaLineal(self, criterio, valor):
        encontrarVolcan = []

        for item in self.data:
            if criterio == "Año" and item["Start Date"].split("-")[2] == valor:
                encontrarVolcan.append(item)

            elif criterio == "VEI" and item["Max. VEI"] == valor:  # Modificar aquí
                encontrarVolcan.append(item)

        self.mostrarResultados(encontrarVolcan)


    def BusquedaLinealVolcanoData(self, criterio, valor):
        encontrarVolcan = []

        for item in self.data:
            if criterio == "Nombre del volcán" and item["Nombre del volcán"].lower() == valor.lower():
                encontrarVolcan.append(item)
            elif criterio == "País" and item["País"].lower() == valor.lower():
                encontrarVolcan.append(item)
            elif criterio == "Año" and item["Anio"] == valor:
                item["Año"] = item["Anio"]
                encontrarVolcan.append(item)

        self.mostrarResultadosDATA(encontrarVolcan)

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
            if self.busqueda_realizada:  # Verificar si se ha realizado una búsqueda
                self.mensajeLabel.setText("No se encontraron resultados.")
            else:
                self.mensajeLabel.setText("")  # No mostrar mensaje si no se ha realizado una búsqueda

        self.resultadoTabla.resizeColumnsToContents()

    def mostrarResultadosDATA(self, resultados):
        if resultados:
            self.resultadoTabla.setVisible(True)
            self.resultadoTabla.setRowCount(len(resultados))
            for row, item in enumerate(resultados):
                self.resultadoTabla.setItem(row, 0, QTableWidgetItem(item["Nombre del volcán"]))
                self.resultadoTabla.setItem(row, 1, QTableWidgetItem(item["País"]))
                self.resultadoTabla.setItem(row, 3,QTableWidgetItem(item["Locación"]))
                self.resultadoTabla.setItem(row, 2, QTableWidgetItem(item["Anio"]))
                self.resultadoTabla.setItem(row, 4, QTableWidgetItem(item["Latitude"]))
                self.resultadoTabla.setItem(row, 5, QTableWidgetItem(item["Longitude"]))
            self.mensajeLabel.setText("")
        else:
            self.resultadoTabla.clearContents()
            self.resultadoTabla.setRowCount(0)
            self.resultadoTabla.setVisible(False)
            if self.busqueda_realizada:  # Verificar si se ha realizado una búsqueda
                self.mensajeLabel.setText("No se encontraron resultados.")
            else:
                self.mensajeLabel.setText("")  # No mostrar mensaje si no se ha realizado una búsqueda

        self.resultadoTabla.resizeColumnsToContents()

    def generarGraficoVEI(self):
        magnitudes = []
        for item in self.data:
            magnitudes.append(float(item["Max. VEI"]))

        if VentanaBusqueda.current_figure is not None:
            plt.close(VentanaBusqueda.current_figure)

        VentanaBusqueda.current_figure = plt.figure(num="Gráfico VEI")
        plt.hist(magnitudes, bins=10)
        plt.xlabel("Magnitud de la Explosión (VEI)")
        plt.ylabel("Cantidad")
        plt.title("Distribución de Magnitudes de Explosiones de Volcanes")
        plt.show()

    def generarGrafico(self):
        anos = []
        explosions_per_year = {}
        for item in self.data:
            year = item["Start Date"].split("-")[2]
            if year in explosions_per_year:
                explosions_per_year[year] += 1
            else:
                explosions_per_year[year] = 1

        if VentanaBusqueda.current_figure is not None:
            plt.close(VentanaBusqueda.current_figure)

        VentanaBusqueda.current_figure = plt.figure(num="Gráfico Erupciones por Año",figsize=(14,6))
        plt.bar(explosions_per_year.keys(), explosions_per_year.values())
        plt.xlabel("Año")
        plt.ylabel("Explosiones")
        plt.title("Explosiones de Volcanes por Año")
        plt.xticks(rotation=60)
        plt.tight_layout()
        plt.show()

    def generarGraficoPais(self):
        paises = {}
        for item in self.data:
            pais = item["País"]
            if pais in paises:
                paises[pais] += 1
            else:
                paises[pais] = 1

        if VentanaBusqueda.current_figure is not None:
            plt.close(VentanaBusqueda.current_figure)

        VentanaBusqueda.current_figure = plt.figure(num="Gráfico Erupciones por País")
        plt.pie(paises.values(), labels=paises.keys(), autopct='%1.1f%%', pctdistance=0.85)
        plt.title("Cantidad de Erupciones por País")
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaBusqueda()
    ventana.show()
    sys.exit(app.exec())

