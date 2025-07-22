
import sys
import os
import time

from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QFileDialog, QWidget,
                             QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton,
                             QGraphicsView, QGraphicsScene, QGraphicsRectItem,
                             QGraphicsSimpleTextItem, QGraphicsLineItem)
from PyQt5.QtGui import QPixmap, QCursor, QColor, QBrush, QFont, QPen, QPainter
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QThread

# ------------------------ Pantalla Carga -------------------------
class PantallaCarga(QLabel):
    def __init__(self, rutaSprites, intervaloMs=100, parent=None):
        super().__init__(parent)
        self.sprites = [QPixmap(os.path.join(rutaSprites, f)) for f in sorted(os.listdir(rutaSprites)) if f.endswith('.png')]
        self.idx = 0
        self.setScaledContents(True)
        self.setVisible(False)
        self.contador = QTimer(self)
        self.contador.timeout.connect(self.siguienteFrame)
        self.intervalo = intervaloMs
        self.resize(self.parent().size())

    def resizeEvent(self, event):
        self.setGeometry(0, 0, self.parent().width(), self.parent().height())
        self.escalarFrame()
        super().resizeEvent(event)

    def iniciar(self):
        if not self.sprites:
            return
        self.idx = 0
        self.escalarFrame()
        self.setPixmap(self.sprites[self.idx])
        self.setVisible(True)
        self.raise_()
        self.resize(self.parent().size())
        self.contador.start(self.intervalo)

    def detener(self):
        self.contador.stop()
        self.setVisible(False)
        self.clear()

    def siguienteFrame(self):
        self.idx = (self.idx + 1) % len(self.sprites)
        self.escalarFrame()

    def escalarFrame(self):
        if not self.sprites:
            return
        pixmapEscalado = self.sprites[self.idx].scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.FastTransformation)
        self.setPixmap(pixmapEscalado)

# --------------------- Boton Sprite --------------------------
class BotonSprite(QLabel):
    clic = pyqtSignal()
    def __init__(self, spriteBase, spriteHover, spriteClick, parent=None):
        super().__init__(parent)
        self.pixmapBase = QPixmap(spriteBase)
        self.pixmapHover = QPixmap(spriteHover)
        self.pixmapClick = QPixmap(spriteClick)
        self.setPixmap(self.pixmapBase)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setMouseTracking(True)
        self.estaClickeado = False

    def enterEvent(self, event): 
        if not self.estaClickeado:
            self.setPixmap(self.pixmapHover)

    def leaveEvent(self, event):
        if not self.estaClickeado:
            self.setPixmap(self.pixmapBase)

    def mousePressEvent(self, event):
        self.estaClickeado = True
        self.setPixmap(self.pixmapClick)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.estaClickeado = False
        if self.rect().contains(event.pos()):
            self.setPixmap(self.pixmapHover)
            self.clic.emit()
        else:
            self.setPixmap(self.pixmapBase)
        super().mouseReleaseEvent(event)

# ---------------------- Placeholder para Carga ----------------------
class trabajoPlaceHolder(QThread):
    terminado = pyqtSignal()
    def run(self):
        time.sleep(3)
        self.terminado.emit()

# --------------------- Datos del Campus ---------------------
class Aula:
    def __init__(self, nombre, capacidad, edificio, posicion, dimensiones, piso):
        self.nombre = nombre
        self.capacidad = capacidad
        self.edificio = edificio
        self.posicion = posicion
        self.dimensiones = dimensiones
        self.piso = piso

class Edificio:
    def __init__(self, nombre, posicion, dimensiones, area, aulas=None):
        self.nombre = nombre
        self.posicion = posicion
        self.dimensiones = dimensiones
        self.area = area
        self.aulas = aulas if aulas else []

    def agregarAula(self, aula):
        self.aulas.append(aula)

    def obtenerAulasPorPiso(self, piso):
        return [a for a in self.aulas if a.piso == piso]

# ------------------- MapaCampus como QWidget -------------------
class MapaCampus(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.edificios = []
        self.areaActual = 1
        self.vistaActual = 'campus'
        self.edificioActual = None
        self.pisoActual = 1
        self.edificiosPrueba()
        self.initUI()

    def edificiosPrueba(self):
        a = Edificio("Edif A", (150, 100), (120, 180), 1)
        a.agregarAula(Aula("A101", 30, "Edif A", (10,10), (40,30), 1))
        self.edificios.append(a)

    def initUI(self):
        layout_principal = QHBoxLayout(self)
        contenedor_mapa = QWidget()
        layout_mapa = QGridLayout(contenedor_mapa)
        self.vistaMapa = QGraphicsView()
        self.escenaMapa = QGraphicsScene()
        self.vistaMapa.setScene(self.escenaMapa)
        layout_mapa.addWidget(self.vistaMapa, 1, 1)
        layout_mapa.setRowStretch(1, 1)
        layout_mapa.setColumnStretch(1, 1)
        layout_principal.addWidget(contenedor_mapa, 80)

        panel_info = QVBoxLayout()
        self.etiquetaTitulo = QLabel("Mapa del Campus")
        panel_info.addWidget(self.etiquetaTitulo)
        self.etiquetaDetalles = QLabel("Detalles aquí")
        panel_info.addWidget(self.etiquetaDetalles)
        layout_principal.addLayout(panel_info, 20)
        self.mostrarVistaCampus()

    def mostrarVistaCampus(self):
        self.escenaMapa.clear()
        fondo = QGraphicsRectItem(0, 0, 700, 500)
        fondo.setBrush(QBrush(QColor(200, 230, 200)))
        self.escenaMapa.addItem(fondo)
        for e in self.edificios:
            rect = QGraphicsRectItem(e.posicion[0], e.posicion[1], e.dimensiones[0], e.dimensiones[1])
            rect.setBrush(QBrush(QColor(70,130,180)))
            self.escenaMapa.addItem(rect)
        self.vistaMapa.fitInView(self.escenaMapa.sceneRect(), Qt.KeepAspectRatio)

# -------------------- PantallaInicio Integrada --------------------
class PantallaInicio(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 450)
        self.imagenFondoRuta = 'imgs/pantallaInicio.png'
        self.animacionPantallaRuta = 'imgs/pantallaCarga'
        self.imagenBotonNormalRuta = 'imgs/botonCsvNomal.png'
        self.imagenBotonHoverRuta  = 'imgs/botonCsvHover.png'
        self.imagenBotonClickRuta  = 'imgs/botonCsvClick.png'

        self.labelFondo = QLabel(self)
        self.labelFondo.lower()

        self.botonCsv = BotonSprite(self.imagenBotonNormalRuta,
                                    self.imagenBotonHoverRuta,
                                    self.imagenBotonClickRuta, self)
        self.botonCsv.clic.connect(self.botonCsvClic)

        self.pantallaCarga = PantallaCarga(self.animacionPantallaRuta, parent=self)
        self.mapaCampus = MapaCampus(self)
        self.mapaCampus.hide()

        self.setWindowTitle("PLAN DE MATERIAS Y AULAS BUAP CU2")
        self.gestionPosicionTamaño()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.gestionPosicionTamaño()
        self.pantallaCarga.resize(self.size())
        self.mapaCampus.resize(self.size())

    def gestionPosicionTamaño(self):
        pixmap = QPixmap(self.imagenFondoRuta)
        if not pixmap.isNull():
            self.labelFondo.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.FastTransformation))
            self.labelFondo.setGeometry(0, 0, self.width(), self.height())
        self.botonCsv.setGeometry(self.width() - 320, self.height() - 160, 320, 160)

    def botonCsvClic(self):
        self.abrirDialogoCsv()

    def abrirDialogoCsv(self):
        rutaArchivo, _ = QFileDialog.getOpenFileName(self, "Selecciona tu archivo CSV", "", "Archivos CSV (*.csv);;Todos los archivos (*)")
        if rutaArchivo:
            self.iniciarPantallaCarga()

    def iniciarPantallaCarga(self):
        self.botonCsv.hide()
        self.labelFondo.hide()
        self.pantallaCarga.iniciar()
        self.proceso = trabajoPlaceHolder()
        self.proceso.terminado.connect(self.detenerPantallaCarga)
        self.proceso.start()

    def detenerPantallaCarga(self):
        self.pantallaCarga.detener()
        self.mapaCampus.setGeometry(0, 0, self.width(), self.height())
        self.mapaCampus.show()
        self.mapaCampus.raise_()

def main():
    app = QApplication(sys.argv)
    inicio = PantallaInicio()
    inicio.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
