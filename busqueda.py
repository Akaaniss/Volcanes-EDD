import os
import sys
import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QComboBox, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
#aqui se importan los modulos para la interfaz
#os sirve para trabajar con rutas de archivos
#sys nos deja utilizar variables y funciones
#csv se utiliza para leer y escribir archivos


#csv_file_path = os.path.abspath(r'C:\Users\fidja\Downloads\Volcanes-EDD-main\Volcanes-EDD-main\erupcionesdesde1903.csv')

#aqui se obtienen el directorio del sprint para luego crear una ruta relativa
#es necesario que el archivo esté bien ubicado
current_dir = os.path.dirname(os.path.abspath(__file__))

relative_path = os.path.join(current_dir, "erupcionesdesde1903.csv")


#se abre el csv leyendo los datos utilizando el csv.reader
#cada fila se convierte en un diccionario con las claves
#los diccionarios se guardan en la lista 'data'
data = []
with open(relative_path, 'r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        data.append(row)


#la clase hereda de qmainwindow y se utiliza para abrir y crear la interfaz
#tiene los metodos y elementos de la interfaz para realizar busquedas
class VentanaBusqueda(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Búsqueda de Volcanes")
        self.setGeometry(100, 100, 600, 400)

        self.combobox = QComboBox(self)
        self.combobox.addItems(["Nombre del volcán", "Región", "Año", "VEI"])
        self.combobox.setCurrentIndex(0)
        self.combobox.currentIndexChanged.connect(self.comboboxRegion)
        self.combobox.move(50, 30)

        self.entradatexto = QLineEdit(self)
        self.entradatexto.move(50, 70)

        self.regionCombobox = QComboBox(self)
        self.regionCombobox.addItems(
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
        self.regionCombobox.setCurrentIndex(0)
        self.regionCombobox.move(50, 70)
        self.regionCombobox.hide()

        self.botonBusqueda = QPushButton("Buscar", self)
        self.botonBusqueda.clicked.connect(self.BusquedaBinaria)
        self.botonBusqueda.move(50, 110)

        self.resultadoTabla = QTableWidget(self)
        self.resultadoTabla.setGeometry(50, 150, 500, 240)
        self.resultadoTabla.setColumnCount(5)
        self.resultadoTabla.setHorizontalHeaderLabels(["Región", "Nombre del volcán", "Año", "VEI", "Coordenadas"])

    def comboboxRegion(self, index):
        if index == 1:
            self.entradatexto.hide()
            self.regionCombobox.show()
        else:
            self.regionCombobox.hide()
            self.entradatexto.show()

    def BusquedaBinaria(self):
        criterio = self.combobox.currentText()
        if criterio == "Región":
            valor = self.regionCombobox.currentText()
        else:
            valor = self.entradatexto.text()

        encontrarVolcan = []
        for volcan in data:
            if criterio == "Nombre del volcán" and volcan["Volcano Name"].lower() == valor.lower():
                encontrarVolcan.append(volcan)
            elif criterio == "Región" and volcan["Region"].lower() == valor.lower():
                encontrarVolcan.append(volcan)
            elif criterio == "Año" and valor == volcan["Start Date"].split("-")[2]:
                encontrarVolcan.append(volcan)
            elif criterio == "VEI" and valor == volcan["Max. VEI"]:
                encontrarVolcan.append(volcan)

        self.mostrarResultados(encontrarVolcan)

    def mostrarResultados(self, volcanes):
        self.resultadoTabla.setRowCount(len(volcanes))

        for index, volcan in enumerate(volcanes):
            regionItem = QTableWidgetItem(volcan["Region"])
            nombreItem = QTableWidgetItem(volcan["Volcano Name"])
            añoItem = QTableWidgetItem(volcan["Start Date"].split("-")[2])
            veiItem = QTableWidgetItem(volcan["Max. VEI"])

            coordenadas = volcan.get("Latitude (dd)", "") + ", " + volcan.get("Longitude (dd)", "")
            coordenadasItem = QTableWidgetItem(coordenadas)

            self.resultadoTabla.setItem(index, 0, regionItem)
            self.resultadoTabla.setItem(index, 1, nombreItem)
            self.resultadoTabla.setItem(index, 2, añoItem)
            self.resultadoTabla.setItem(index, 3, veiItem)
            self.resultadoTabla.setItem(index, 4, coordenadasItem)

        self.resultadoTabla.resizeColumnsToContents()

#aqui se crea una intancia 'qapplication' creando la ventana
#mostrandola en pantalla, iniciando el bucle de eventos de la interfaz
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaBusqueda()
    ventana.show()
    sys.exit(app.exec())