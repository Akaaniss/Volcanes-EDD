import os
import sys
import csv
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QComboBox, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
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
        self.setGeometry(150, 150, 800, 600)

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
        self.regionCombobox.setFixedWidth(250)
        self.regionCombobox.hide()

        self.botonBusqueda = QPushButton("Buscar", self)
        self.botonBusqueda.clicked.connect(self.BusquedaBinaria)
        self.botonBusqueda.move(50, 110)

        self.resultadoTabla = QTableWidget(self)
        self.resultadoTabla.setGeometry(50, 150, 700, 400)
        self.resultadoTabla.setColumnCount(5)
        self.resultadoTabla.setHorizontalHeaderLabels(["Región", "Nombre del volcán", "Año", "VEI", "Coordenadas"])

        self.mensajeLabel = QLabel(self)
        self.mensajeLabel.setGeometry(50, 150, 500, 30)
        self.mensajeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mensajeLabel.setStyleSheet("color: black; font-weight: bold;")

    def comboboxRegion(self, index):
        if index == 1:
            self.entradatexto.hide()
            self.regionCombobox.show()
        else:
            self.regionCombobox.hide()
            self.entradatexto.show()

    def BusquedaBinaria(self):
        criterio = self.combobox.currentText() #se toma el criterio segun la opcion que seleccionemos en la combo box
        if criterio == "Región":                        #si el criterio es igual a region, el valor para la busqueda se encontrara en la regionCombobox
            valor = self.regionCombobox.currentText()   #sino el valor se encontrara en la entrada de texto
        else:
            valor = self.entradatexto.text()

        encontrarVolcan = []#lista vacia donde se guardaran las busquedas
        for volcan in data:     #se utiliza un ciclo for
            if criterio == "Nombre del volcán" and volcan["Volcano Name"].lower() == valor.lower():#si el criterio es nombre del volcan u otros se busca en la sección volcan"volcano name"
                encontrarVolcan.append(volcan)                                  #en el csv con .lower , y si es igual al valor buscado se agrega a la lista vacia
            elif criterio == "Región" and volcan["Region"].lower() == valor.lower():
                encontrarVolcan.append(volcan)
            elif criterio == "Año" and valor == volcan["Start Date"].split("-")[2]:# aqui se buscan en startdate,pero solo en se toma en consideracion despues de 2 "-"
                encontrarVolcan.append(volcan)                                      #para que tome el valor del año, y asi se busque solo por el año
            elif criterio == "VEI" and valor == volcan["Max. VEI"]:
                encontrarVolcan.append(volcan)

        self.mostrarResultados(encontrarVolcan)

    def mostrarResultados(self, volcanes):
        self.resultadoTabla.setRowCount(len(volcanes))#se verifica la cantidad de resultados encontrados

        if not volcanes:    #si es que no se encuentran resultados da el mensaje:
            self.mensajeLabel.setText("No se han encontrado resultados para esta búsqueda")
            self.mensajeLabel.show()#se muestra el mensaje
            self.resultadoTabla.hide()#se oculta la tabla
        else:
            self.mensajeLabel.hide()#sino, alrevez xd
            self.resultadoTabla.show()

            for index, volcan in enumerate(volcanes):#se ordenan los resultados con index segun como deben aparecer en la tabla
                regionItem = QTableWidgetItem(volcan["Region"])#items de cada resultado siendo representados para tablas
                nombreItem = QTableWidgetItem(volcan["Volcano Name"])
                añoItem = QTableWidgetItem(volcan["Start Date"].split("-")[2])
                veiItem = QTableWidgetItem(volcan["Max. VEI"])

                coordenadas = volcan.get("Latitude", "") + ", " + volcan.get("Longitude", "")#para que se muestren las coordenadas correctamente
                coordenadasItem = QTableWidgetItem(coordenadas)

                self.resultadoTabla.setItem(index, 0, regionItem)#se añade cada resultado separado a su seccion de la tabla
                self.resultadoTabla.setItem(index, 1, nombreItem)
                self.resultadoTabla.setItem(index, 2, añoItem)
                self.resultadoTabla.setItem(index, 3, veiItem)
                self.resultadoTabla.setItem(index, 4, coordenadasItem)

            self.resultadoTabla.resizeColumnsToContents()#se ajusta la tabla segun los resultados

#aqui se crea una intancia 'qapplication' creando la ventana
#mostrandola en pantalla, iniciando el bucle de eventos de la interfaz
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaBusqueda()
    ventana.show()
    sys.exit(app.exec())
