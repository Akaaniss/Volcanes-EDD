import os#sirve para interactuar con el sistema operativo
import sys#sirve para manipular argumentos de la linea de comandos
import csv#para leer archivos csv
import matplotlib.pyplot as plt#sirve para hacer graficos
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QComboBox, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem


class VentanaBusqueda(QMainWindow):#clase busqueda que hereda de QWindow
                                    #representa la ventana principal
    current_figure = None#se usa para realizar un seguimiento de la figura trazada

    def __init__(self):#constructor de la clase VentanaBusqueda
        super().__init__()
        self.setWindowTitle("Búsqueda de Volcanes")
        self.setGeometry(150, 150, 580, 560)#configura tambien el título y el tamaño de la ventana
        #se construye la ruta relativa del archivo csv de erupcionesdesde1903
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.relative_path = os.path.join(self.current_dir, "erupcionesdesde1903.csv")

        self.data = []
        self.archivo_csv_actual = "erupcionesdesde1903.csv"  # archivo actual
        self.busqueda_realizada = False  # Bandera para indicar si se ha realizado una búsqueda
        #data almacena los datos del csv
        self.cargar_data()
        self.crear_widgets()

    def cargar_data(self):#incluye la ruta del csv que ayuda a cargar los datos 
        with open(self.archivo_csv_actual, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                self.data.append(row)

    def crear_widgets(self):
        self.combobox = QComboBox(self)#se crean los combobox para tener una pestaña desplegable con informacion
        self.combobox.addItems(["Nombre del volcán", "Región", "Año", "VEI"])
        self.combobox.setCurrentIndex(1)
        self.combobox.currentIndexChanged.connect(self.comboboxRegion)
        self.combobox.move(50, 30)
        self.combobox.setFixedWidth(250)

        self.entradatexto = QLineEdit(self)#Configura la posicion y el ancho 
        self.entradatexto.move(50, 70)
        self.entradatexto.setFixedWidth(250)

        self.regionCombobox = QComboBox(self)#sirve para seleccionar una region en el criterio de busqueda"Región"
        self.regionCombobox.addItems(["Region de Arica y Parinacota", "Region de Tarapaca", "Region de Antofagasta",
                                      "Región de Atacama", "Region de Coquimbo", "Region de Valparaiso",
                                      "Region Metropolitana", "Region de O'Higgins", "Region del Maule",
                                      "Region de Nuble", "Region del Biobio", "Region de La Araucania",
                                      "Region de Los Rios", "Region de Los Lagos", "Region de Aysen",
                                      "Region de Magallanes y la Antartica Chilena"])
        self.regionCombobox.setCurrentIndex(0)
        self.regionCombobox.move(50, 70)
        self.regionCombobox.setFixedWidth(250)
        self.regionCombobox.setVisible(False)  # Ocultar la comboBox de regiones al inicio

        self.botonBusqueda = QPushButton("Buscar", self)
        self.botonBusqueda.clicked.connect(self.realizarBusqueda)#se configura la posición del botón
        self.botonBusqueda.move(50, 110)

        self.botonGrafico = QPushButton("Gráfico Erupciones por Año", self)
        self.botonGrafico.clicked.connect(self.generarGrafico)#se crea para conectar el boton al metodo generarGrafico
        self.botonGrafico.move(200, 110)
        self.botonGrafico.setFixedWidth(160)

        self.botonGraficoVEI = QPushButton("Gráfico VEI", self)
        self.botonGraficoVEI.clicked.connect(self.generarGraficoVEI)#se conecta al metodo generarGraficoVEI
        self.botonGraficoVEI.move(410, 110)
        self.botonGraficoVEI.setFixedWidth(100)

        self.resultadoTabla = QTableWidget(self)#sirve  para configurar la posicion y tamaño
        self.resultadoTabla.setGeometry(50, 150, 520, 400)

        self.mensajeLabel = QLabel(self)#Sirve para mostrar mensajes
        self.mensajeLabel.setGeometry(50, 150, 500, 30)
        self.mensajeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mensajeLabel.setStyleSheet("color: black; font-weight: bold;")

        self.comboboxArchivo = QComboBox(self)#se crea un combobox adicional para cambiar el archivo csv
        self.comboboxArchivo.addItems(["Erupciones desde 1903 en Chile", "Volcanes del Mundo"])
        self.comboboxArchivo.currentIndexChanged.connect(self.cambiarArchivo)
        self.comboboxArchivo.move(320, 30)
        self.comboboxArchivo.setFixedWidth(250)

        self.botonGraficoPais = QPushButton("Gráfico Erupciones por País", self)#sirve para generar el grafico 
        self.botonGraficoPais.clicked.connect(self.generarGraficoPais)
        self.botonGraficoPais.move(370, 110)
        self.botonGraficoPais.setFixedWidth(160)
        self.botonGraficoPais.hide()  # Ocultar el botón inicialmente
        #se definen las opciones disponibles para ambos archivos
        opciones_erupciones = ["Región", "Nombre del volcán", "Año", "VEI"]
        opciones_volcano_data = ["Nombre del volcán", "País", "Año", ]
        #se almacenan en diccionarios opciones_csv y columnas_csv
        self.opciones_csv = {
            "erupcionesdesde1903.csv": opciones_erupciones,
            "volcano_data_2010.csv": opciones_volcano_data
        }
        self.columnas_csv = {
            "erupcionesdesde1903.csv": ["Región", "Nombre del volcán", "Año", "VEI", "Coordenadas"],
            "volcano_data_2010.csv": ["Nombre del volcán", "País", "Año", "Locacion", "Latitude", "Longitude"]
        }
        #se llaman los metodos para configurar el combobox y 
        self.actualizarComboBox()
        self.actualizarDatos()
        self.realizarBusqueda()

    def actualizarComboBox(self):#actualiza el combobox segun el archivo csv, agregando las nuevas opciones, mostrandolas u ocultandolas
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

    def cambiarArchivo(self, index):#se ejecuta cuando se cambia la seleccion del combobox de archivos
        archivos_csv = ["erupcionesdesde1903.csv", "volcano_data_2010.csv"]
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

    def comboboxRegion(self, index):#se ejecuta cuando se cambia la seleccion del combobox
        criterio = self.combobox.currentText()
        if self.archivo_csv_actual == "erupcionesdesde1903.csv" and criterio == "Región":
            self.entradatexto.hide()
            self.regionCombobox.setVisible(True)  # Mostrar la comboBox de regiones si se selecciona "Región"
        else:
            self.regionCombobox.setVisible(False)  # Ocultar la comboBox de regiones en cualquier otro caso
            self.entradatexto.show()

    def realizarBusqueda(self):#se ejecuta cuando se presiona el botón de busqueda
                                #luego realiza la busqueda segun se requiera, binaria,lineal o la del otro csv
        criterio = self.combobox.currentText()

        if criterio == "Nombre del volcán" or criterio == "Región":
            if criterio == "Región":
                valor = self.regionCombobox.currentText()
            else:
                valor = self.entradatexto.text()

            # Guardar el valor en una variable antes de borrar el campo de entrada de texto
            valor_busqueda = valor

            self.entradatexto.clear()

            # Realizar la búsqueda utilizando el valor guardado
            self.BusquedaBinaria(criterio, valor_busqueda)

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

    def BusquedaBinaria(self, criterio, valor):#realiza  una busqueda binaria en el archivo csv
        encontrarVolcan = []#los resultados se almacenan en esta lista
                            #este llama a los métodos "mostrarResultados" o el del otro csv para mostrar los resultados
        if criterio == "Nombre del volcán" or criterio == "Región":
            sorted_data = sorted(self.data, key=lambda x: x[criterio])

            if criterio == "Región":
                izquierda = 0
                derecha = len(sorted_data) - 1
                while izquierda <= derecha:
                    mid = (izquierda + derecha) // 2
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
                        izquierda = mid + 1
                    else:
                        derecha = mid - 1

            elif criterio == "Nombre del volcán":
                izquierda = 0
                derecha = len(sorted_data) - 1
                while izquierda <= derecha:
                    mid = (izquierda + derecha) // 2
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
                        izquierda = mid + 1
                    else:
                        derecha = mid - 1

        if self.archivo_csv_actual == "erupcionesdesde1903.csv":
            self.mostrarResultados(encontrarVolcan)
        elif self.archivo_csv_actual == "volcano_data_2010.csv":
            self.mostrarResultadosDATA(encontrarVolcan)

    def BusquedaLineal(self, criterio, valor):#realiza una busqueda lineal del los datos del csv
        encontrarVolcan = []#los datos se almacenan en esta lista para luego llamar al metodo"mostrarResultados" y asi mostrar los resultados en la tabla

        for item in self.data:
            if criterio == "Año" and item["Start Date"].split("-")[2] == valor:
                encontrarVolcan.append(item)

            elif criterio == "VEI" and item["Max. VEI"] == valor:
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
                encontrarVolcan.append(item)

        self.mostrarResultadosDATA(encontrarVolcan)

    def mostrarResultados(self, resultados):#muestra los resultados de la busqueda en la tabla
                                            #configurando la visibilidad de la tabla además se configura un mensaje de si se encontraron o no los resultados
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
            if self.busqueda_realizada:
                self.mensajeLabel.setText("No se encontraron resultados.")
            else:
                self.mensajeLabel.setText("")

        self.resultadoTabla.resizeColumnsToContents()

    def mostrarResultadosDATA(self, resultados):
        if resultados:
            self.resultadoTabla.setVisible(True)
            self.resultadoTabla.setRowCount(len(resultados))
            for row, item in enumerate(resultados):
                self.resultadoTabla.setItem(row, 0, QTableWidgetItem(item["Nombre del volcán"]))
                self.resultadoTabla.setItem(row, 1, QTableWidgetItem(item["País"]))
                self.resultadoTabla.setItem(row, 2, QTableWidgetItem(item["Anio"]))
                self.resultadoTabla.setItem(row, 3, QTableWidgetItem(item["Locación"]))
                self.resultadoTabla.setItem(row, 4, QTableWidgetItem(item["Latitude"]))
                self.resultadoTabla.setItem(row, 5, QTableWidgetItem(item["Longitude"]))
            self.mensajeLabel.setText("")
        else:
            self.resultadoTabla.clearContents()
            self.resultadoTabla.setRowCount(0)
            self.resultadoTabla.setVisible(False)
            if self.busqueda_realizada:
                self.mensajeLabel.setText("No se encontraron resultados.")
            else:
                self.mensajeLabel.setText("")

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

    def generarGrafico(self):#genera un grafico de barras que muestra el numero de erupciones por año
        anos = []
        explosiones_por_año = {}
        for item in self.data:
            anho = item["Start Date"].split("-")[2]
            if anho in explosiones_por_año:
                explosiones_por_año[anho] += 1
            else:
                explosiones_por_año[anho] = 1

        if VentanaBusqueda.current_figure is not None:
            plt.close(VentanaBusqueda.current_figure)

        VentanaBusqueda.current_figure = plt.figure(num="Gráfico Erupciones por Año", figsize=(14, 6))
        plt.bar(explosiones_por_año.keys(), explosiones_por_año.values())
        plt.xlabel("Año")
        plt.ylabel("Explosiones")
        plt.title("Explosiones de Volcanes por Año")
        plt.xticks(rotation=60)
        plt.tight_layout()
        plt.show()

    def generarGraficoPais(self):#genera un grafico 
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
