import os
from PyQt5.QtWidgets import QMainWindow, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from widgets.boton_sprite import BotonSprite
from pantallas.pantalla_carga import PantallaCarga
from pantallas.pantalla_principal import PantallaPrincipal
from procesos.trabajo_placeholder import TrabajoPlaceHolder

class PantallaInicio(QMainWindow):
    def __init__(self):
        super().__init__()

        self.anchoPantallaMinimo = 800
        self.altoPantallaMinimo = 450
        self.anchoBotonMinimo = 320
        self.altoBotonMinimo = 160
        self.margenBotonMinimo = 0

        self.imagenFondoRuta = 'recursos/imgs/pantallaInicio.png'
        self.imagenBotonNormalRuta = 'recursos/imgs/botonCsvNomal.png'
        self.imagenBotonHoverRuta = 'recursos/imgs/botonCsvHover.png'
        self.imagenBotonClickRuta = 'recursos/imgs/botonCsvClick.png'
        self.animacionPantallaRuta = 'recursos/imgs/pantallaCarga'

        self.setWindowTitle("PLAN DE MATERIAS Y AULAS BUAP CU2")
        self.setMinimumSize(self.anchoPantallaMinimo, self.altoPantallaMinimo)

        self.labelFondo = QLabel(self)
        self.labelFondo.setScaledContents(False)
        self.labelFondo.lower()

        self.botonCsv = BotonSprite(
            self.imagenBotonNormalRuta,
            self.imagenBotonHoverRuta,
            self.imagenBotonClickRuta,
            self
        )
        self.botonCsv.clic.connect(self.botonCsvClic)

        self.pantallaCarga = PantallaCarga(self.animacionPantallaRuta, parent=self)
        self.pantallaPrincipal = PantallaPrincipal()

        self.gestionPosicionTamaño()

    def resizeEvent(self, evento):
        super().resizeEvent(evento)
        self.gestionPosicionTamaño()
        self.pantallaCarga.resize(self.size())

    def gestionPosicionTamaño(self):
        self.gestionFondo()
        self.gestionBoton()

    def gestionFondo(self):
        pixmap = QPixmap(self.imagenFondoRuta)
        if not pixmap.isNull():
            pixmapEscalado = pixmap.scaled(
                self.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.FastTransformation
            )
            self.labelFondo.setPixmap(pixmapEscalado)
            self.labelFondo.setGeometry(0, 0, self.width(), self.height())

    def gestionBoton(self):
        anchoVentana = self.width()
        altoVentana = self.height()

        factorAncho = anchoVentana / self.anchoPantallaMinimo
        factorAlto = altoVentana / self.altoPantallaMinimo
        factorEscala = min(factorAncho, factorAlto)

        nuevoAnchoBoton = max(self.anchoBotonMinimo, int(self.anchoBotonMinimo * factorEscala))
        nuevoAltoBoton = max(self.altoBotonMinimo, int(self.altoBotonMinimo * factorEscala))
        nuevoMargen = int(self.margenBotonMinimo * factorEscala)

        self.botonCsv.escalarPixmaps(nuevoAnchoBoton, nuevoAltoBoton)

        xPosBoton = anchoVentana - nuevoAnchoBoton - nuevoMargen
        yPosBoton = altoVentana - nuevoAltoBoton - nuevoMargen
        self.botonCsv.setGeometry(xPosBoton, yPosBoton, nuevoAnchoBoton, nuevoAltoBoton)

    def botonCsvClic(self):
        self.abrirDialogoCSV()

    def abrirDialogoCSV(self):
        rutaArchivo, _ = QFileDialog.getOpenFileName(
            self,
            "Selecciona tu archivo CSV",
            "",
            "Archivos CSV (*.csv);;Todos los archivos (*)"
        )
        if rutaArchivo:
            print("Archivo CSV seleccionado:", rutaArchivo)
            self.iniciarPantallaCarga()

    def iniciarPantallaCarga(self):
        self.botonCsv.hide()
        self.labelFondo.hide()

        self.pantallaCarga.iniciar()

        self.proceso = TrabajoPlaceHolder()
        self.proceso.terminado.connect(self.detenerPantallaCarga)
        self.proceso.start()

    def detenerPantallaCarga(self):
        self.pantallaCarga.detener()
        self.pantallaPrincipal.iniciar()
