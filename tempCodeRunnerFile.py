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