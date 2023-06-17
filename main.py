import sys
from busqueda import ventanadeBusqueda
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ventanadeBusqueda()
    window.show()
    sys.exit(app.exec())