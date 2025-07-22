import sys
from PyQt5.QtWidgets import QApplication
from pantallas.pantalla_inicio import PantallaInicio

def main():
    app = QApplication(sys.argv)
    inicio = PantallaInicio()
    inicio.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
