import sys
import os
import time
import math

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QFileDialog, QWidget, QVBoxLayout, QPushButton, QGridLayout
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QThread

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

from PyQt5.QtWidgets import QSizePolicy

from PyQt5.QtGui import QFontDatabase, QFont

# ------------------------ Datos del Campus ------------------------- | ------------------------------------------------------------
class Clase:
    def __init__(self, materia, profesor, hora):
        self.materia = materia
        self.profesor = profesor
        self.hora = hora  # Formato '08:00'

    def __str__(self):
        return f"{self.hora} - {self.materia} ({self.profesor})"

class Aula:
    def __init__(self, nombre, capacidad, edificio, piso):
        self.nombre = nombre
        self.capacidad = capacidad
        self.edificio = edificio
        self.piso = piso
        self.detalles = f"Aula {nombre}\nCapacidad: {capacidad} alumnos\nPiso: {piso}"

        # Inicializa el horario: lunes a viernes, 08:00 a 18:00 (55 bloques)
        self.horario = {
            dia: {} for dia in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        }
        self.horas = [n for n in range(8, 18)]

    def asignarClase(self, dia, hora, clase):
        """Asigna una clase si el bloque horario está libre"""
        if hora not in self.horario[dia]:
            self.horario[dia][hora] = clase

    def clasesAsignadas(self):
        """Devuelve una lista de todas las clases asignadas"""
        clases = []
        for dia in self.horario:
            for clase in self.horario[dia].values():
                clases.append(clase)
        return clases

    def contarClases(self):
        """Cuenta cuántos bloques horarios están ocupados"""
        return sum(len(self.horario[dia]) for dia in self.horario)

    def porcentajeOcupado(self):
        """Devuelve el porcentaje de ocupación del aula (0 a 100)"""
        total_bloques = len(self.horario) * len(self.horas)
        bloques_ocupados = self.contarClases()
        return (bloques_ocupados / total_bloques) * 100

    def horasOcupadas(self):
        """Devuelve el total de horas ocupadas (bloques)"""
        return self.contarClases()


class Edificio:
    total_edificios = []

    def __init__(self, nombre, area, aulas=None):
        self.nombre = nombre
        self.area = area  # Área 1 o 2
        self.aulas = aulas if aulas else []
        Edificio.total_edificios.append(self)

    def agregarAula(self, aula):
        self.aulas.append(aula)

    def obtenerAulasPorPiso(self, piso):
        return [aula for aula in self.aulas if aula.piso == piso]

    def contarAulas(self):
        return len(self.aulas)

    def aulasPorPiso(self):
        """Devuelve un diccionario con el número de aulas por piso"""
        pisos = {}
        for aula in self.aulas:
            pisos[aula.piso] = pisos.get(aula.piso, 0) + 1
        return pisos

    def porcentajeOcupadoPorPiso(self):
        """Devuelve el porcentaje promedio de ocupación por piso"""
        ocupacion_por_piso = {}
        for aula in self.aulas:
            piso = aula.piso
            if piso not in ocupacion_por_piso:
                ocupacion_por_piso[piso] = []
            ocupacion_por_piso[piso].append(aula.porcentajeOcupado())

        return {
            piso: sum(porcentajes) / len(porcentajes)
            for piso, porcentajes in ocupacion_por_piso.items()
        }

    def porcentajeOcupadoTotal(self):
        """Promedio de ocupación de todo el edificio"""
        if not self.aulas:
            return 0
        return sum(aula.porcentajeOcupado() for aula in self.aulas) / len(self.aulas)

    # ---- Métodos globales (de clase) ----
    @classmethod
    def contarEdificios(cls):
        return len(cls.total_edificios)

    @classmethod
    def contarEdificiosPorArea(cls, area):
        return sum(1 for e in cls.total_edificios if e.area == area)

    @classmethod
    def contarAulasTotales(cls):
        return sum(len(e.aulas) for e in cls.total_edificios)

    @classmethod
    def contarAulasPorArea(cls, area):
        return sum(len(e.aulas) for e in cls.total_edificios if e.area == area)


# ------------------------ Pantalla Carga ------------------------- | ------------------------------------------------------------
class PantallaCarga(QLabel):
    # ------------------------------ Constructor ------------------------------
    def __init__(self, rutaSprites, intervaloMs=100, parent=None):
        super().__init__(parent)
        # --------------------------- Cargar Sprites --------------------------
        self.sprites = []
        for archivo in sorted(os.listdir(rutaSprites)):
            if archivo.endswith('.png'):
                pixmap = QPixmap(os.path.join(rutaSprites, archivo))
                self.sprites.append(pixmap)
                
        self.idx = 0 # Indice usado para manejar los frames
        self.setScaledContents(True)
        self.setVisible(False)

        # Contador de frames
        self.contador = QTimer(self)
        self.contador.timeout.connect(self.siguienteFrame) # Conectar el temproizador que pase al siguiente frame
        self.intervalo = intervaloMs

        self.resize(self.parent().size())
        
    # ------------------------------ Funciones de QT ------------------------------

    # Funcion llamada al redimensionar la pantalla
    def resizeEvent(self, event):
        self.setGeometry(0, 0, self.parent().width(), self.parent().height())
        self.escalarFrame()
        super().resizeEvent(event)
        
    # ----------------------------- Funciones Propias -----------------------------

    # Funcion para iniciar la pantalla de carga
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

    # Funcion para detener la pantalla de carga
    def detener(self):
        self.contador.stop()
        self.setVisible(False)
        self.clear()

    # Metodo interno para realizar la animacion
    def siguienteFrame(self):
        self.idx = (self.idx + 1) % len(self.sprites)
        self.escalarFrame()

    # Funcion para escalar el frame actual
    def escalarFrame(self):
        if not self.sprites:
            return
        spriteOriginal = self.sprites[self.idx]
        pixmapEscalado = spriteOriginal.scaled(
            self.size(),
            Qt.KeepAspectRatioByExpanding,
            Qt.FastTransformation  # Importante para mantener bordes nítidos en pixel art
        )
        self.setPixmap(pixmapEscalado)
    
# ---------------------- Pantalla Principal (Mapa)  ----------------------- | ------------------------------------------------------------
class PantallaPrincipal(QWidget):

      # -------------------------------- Constructor --------------------------------
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: rgb(0, 0, 65);")  # fondo sólido
        # ----------------------------- Configuracion -----------------------------
        self.edificios = []

        self.anchoPantallaMinimo = 800

        idFont       = QFontDatabase.addApplicationFont("fonts/vga437.ttf")
        self.fontVga = QFontDatabase.applicationFontFamilies(idFont)[0]

        # -------------------------------- Widgets --------------------------------    
        self.panelIzquierdo = QWidget(self) # Mapa
        self.panelIzquierdo_layout = QVBoxLayout(self.panelIzquierdo)
        self.panelCuadricula = QWidget(self.panelIzquierdo) # Cuadricula usada para acomodar el mapa y sus botones
        self.panelIzquierdo_layout.addWidget(self.panelCuadricula)

        self.panelDerecho = QLabel(self) # datos
        self.panelDerecho.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.panelDerecho.setWordWrap(True)
        self.panelDerecho.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.datosSinteticos() # Funcion para llenar unos datos sinteticos.
        
        self.iniciarMapa() # Inicia el mapa en el area de campus 1
                
    # ------------------------------ Funciones de QT ------------------------------
    
    # Funcion llamada al redimensionar la pantalla
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.gestionLayout()
                
    # ----------------------------- Funciones Propias -----------------------------

    def gestionLayout(self):
        self.actualizarDimensiones()
        self.actualizarEstilo()

    # Funcion para mantener las proporciones en el widget.
    def actualizarDimensiones(self):
        
        ancho = self.width()
        alto  = self.height()

        proporcionMargenHorizontal = 0.03 # Son los bordes de las pantallas
        proporcionMargenVertical   = 0.03
        proporcionSeparacion = 0.04 # Distancia entre ambos paneles
        proporcionAnchoIzquierdo = 0.7
        proporcionAnchoDerecho   = 0.20

        nuevoAnchoIzquierdo = int(ancho * proporcionAnchoIzquierdo)
        nuevoAnchoDerecho   = int(ancho * proporcionAnchoDerecho)

        nuevoAlto = int(alto * (1 - proporcionMargenVertical * 2)) # Tanto de arriba como abajo.

        margenAncho = int(ancho * proporcionMargenHorizontal)
        margenAlto  = int(alto  * proporcionMargenVertical)

        separacion = int(ancho * proporcionSeparacion)

        self.panelIzquierdo.setGeometry(margenAncho, margenAlto, nuevoAnchoIzquierdo, nuevoAlto)

        self.panelDerecho.setGeometry(margenAncho + separacion + nuevoAnchoIzquierdo, margenAlto, nuevoAnchoDerecho, nuevoAlto)
        self.panelDerecho.setFixedWidth(nuevoAnchoDerecho)
        self.panelDerecho.setFixedHeight(nuevoAlto)
        

    # Funcion para mantener el estilo en el widget
    def actualizarEstilo(self):
        ancho = self.width()
        alto  = self.height()
        
        # Calcular nuevo font-size
        fontSizeMinimo = 10 # Tamaño ideal para 800 x 450
        nuevoFontSize = int(ancho / self.anchoPantallaMinimo * fontSizeMinimo)
        # Calcular nuevo padding
        paddingMinimo = 5 # Espacio ideal para 800 x 450
        nuevoPadding = int(ancho / self.anchoPantallaMinimo * paddingMinimo)
        
        hojaEstilos = f"""
        background-color: rgb(212, 216, 224);
        color: rgb(24, 25, 35);        
        font-size: {nuevoFontSize * 0.7}pt;
        padding: {nuevoPadding}px;
        """
        # Calculo de las nuevas sombras
        xSombra = ancho * 0.05 * 0.2
        ySombra = alto * 0.05 * 0.3
        
        # Panel Izquierdo
        sombraIzquierda = QGraphicsDropShadowEffect()
        sombraIzquierda.setBlurRadius(0)
        sombraIzquierda.setColor(QColor(0, 0, 0, 255))
        sombraIzquierda.setOffset(xSombra, ySombra)

        self.panelIzquierdo.setFont(QFont(self.fontVga, nuevoFontSize))
        self.panelIzquierdo.setStyleSheet(hojaEstilos)
        self.panelIzquierdo.setGraphicsEffect(sombraIzquierda)

        # Aplicar estilo también a las celdas dentro de panelCuadricula
        if self.panelCuadricula.layout():
            for i in range(self.panelCuadricula.layout().count()):
                widget = self.panelCuadricula.layout().itemAt(i).widget()
                if not widget:
                    continue

                obj = widget.objectName()
                if obj == "botonEdificio":
                    porcentaje = widget.property("porcentajeOcupacion")
                    if porcentaje > 80:
                        colorEdificio = "rgb(41, 45, 65)"
                    elif porcentaje > 60:
                        colorEdificio = "rgb(56, 64, 93)"
                    elif porcentaje > 40:
                        colorEdificio = "rgb(76, 84, 109)"
                    elif porcentaje > 20:
                        colorEdificio = "rgb(118, 126, 153)"
                    else:
                        colorEdificio = "rgb(142, 161, 179)"
                    widget.setFont(QFont(self.fontVga, int(nuevoFontSize * 1.8)))
                    widget.setStyleSheet(f"""
                    QPushButton{{
                    background-color : {colorEdificio};
                    color: white;
                    border-radius: 0px;
                    font-size: {int(nuevoFontSize * 1.8)}pt;
                    text-align: center;
                    }}

                    QPushButton:hover {{
                    background-color: rgb(252,204,92); 
                    }}

                    QPushButton:pressed {{
                    background-color: rgb(124,4,4);    
                    }}

                    """)
                    sombraEdificio = QGraphicsDropShadowEffect()
                    sombraEdificio.setBlurRadius(0)
                    sombraEdificio.setColor(QColor(150, 155, 165, 255))
                    sombraEdificio.setOffset(xSombra * 0.8, ySombra * 0.6)
                    widget.setGraphicsEffect(sombraEdificio)
                elif obj == "titulo":
                    widget.setFont(QFont(self.fontVga, int(nuevoFontSize * 1.4)))
                    widget.setStyleSheet(f"""
                    background-color: rgb(60, 68, 92);
                    color: white;
                    font-size: {int(nuevoFontSize * 1.4)}pt;
                    padding: {int(nuevoPadding * 1.5)}px;
                    """)
                    sombraTitulo = QGraphicsDropShadowEffect()
                    sombraTitulo.setBlurRadius(0)
                    sombraTitulo.setColor(QColor(150,155,165,255))
                    sombraTitulo.setOffset(xSombra * 0.8, ySombra * 0.6)
                    widget.setGraphicsEffect(sombraTitulo)
                elif obj == "boton":
                    widget.setFont(QFont(self.fontVga, int(nuevoFontSize * 2)))
                    widget.setStyleSheet(f"""
                    QPushButton{{
                    background-color: rgb(60, 68, 92);
                    color: white;
                    border-radius: 0px;
                    font-size: {int(nuevoFontSize * 2)}pt;
                    }}

                    QPushButton:hover {{
                    background-color: rgb(252,204,92); 
                    }}

                    QPushButton:pressed {{
                    background-color: rgb(124,4,4);    
                    }}
                    
                    """)
                    sombraBoton = QGraphicsDropShadowEffect()
                    sombraBoton.setBlurRadius(0)
                    sombraBoton.setColor(QColor(150,155,165,255))
                    sombraBoton.setOffset(xSombra * 0.3, ySombra * 0.3)
                    widget.setGraphicsEffect(sombraBoton)
                elif obj == "encabezadoTabla":
                    widget.setFont(QFont(self.fontVga, int(nuevoFontSize * 1.2)))
                    widget.setStyleSheet(f"""
                    QLabel {{
                        background-color: rgb(41,45,65);
                        color: white;
                        font-weight: bold;
                        font-size: {int(nuevoFontSize * 1.2)}pt;
                        padding: 4px;
                    }}
                    """)
                    sombraEncabezado = QGraphicsDropShadowEffect()
                    sombraEncabezado.setBlurRadius(0)
                    sombraEncabezado.setColor(QColor(150,155,165,255))
                    sombraEncabezado.setOffset(xSombra * 0.2, ySombra * 0.2)
                    widget.setGraphicsEffect(sombraEncabezado)

                elif obj == "celdaTabla":
                    widget.setFont(QFont(self.fontVga, int(nuevoFontSize * 0.5)))
                    widget.setStyleSheet(f"""
                    QLabel {{
                        background-color: rgb(185,195,199);
                        color: black;
                        font-size: {int(nuevoFontSize * 0.5)}pt;
                    }}
                    """)
                    sombraCelda = QGraphicsDropShadowEffect()
                    sombraCelda.setBlurRadius(0)
                    sombraCelda.setColor(QColor(QColor(150,155,165,255)))
                    sombraCelda.setOffset(xSombra * 0.15, ySombra * 0.15)
                    widget.setGraphicsEffect(sombraCelda)


        # Panel Derecho
        sombraDerecha = QGraphicsDropShadowEffect()
        sombraDerecha.setBlurRadius(0)
        sombraDerecha.setColor(QColor(0, 0, 0, 255))
        sombraDerecha.setOffset(xSombra, ySombra)
        
        self.panelDerecho.setFont(QFont(self.fontVga, nuevoFontSize))
        self.panelDerecho.setStyleSheet(hojaEstilos)
        self.panelDerecho.setGraphicsEffect(sombraDerecha)
            
    # Funcion para iniciar unos datos sinteticos y poder visualizar la UI
    def datosSinteticos(self):
        self.edificios = []

        # ---------------- Área 1 ---------------- #
        
        # EMA1 – 2 pisos
        a = Edificio("EMA1", 1)
        a.agregarAula(Aula("A101", 40, a, 1))
        a.agregarAula(Aula("A102", 35, a, 1))
        a.agregarAula(Aula("A201", 50, a, 2))
        self.edificios.append(a)
        
        # EMA2 – 1 piso
        a = Edificio("EMA2", 1)
        a.agregarAula(Aula("B101", 30, a, 1))
        a.agregarAula(Aula("B102", 25, a, 1))
        self.edificios.append(a)
        
        # EMA3 – 2 pisos
        a = Edificio("EMA3", 1)
        a.agregarAula(Aula("C101", 30, a, 1))
        a.agregarAula(Aula("C102", 35, a, 1))
        a.agregarAula(Aula("C201", 45, a, 2))
        self.edificios.append(a)
        
        # EMA4 – 1 piso
        a = Edificio("EMA4", 1)
        a.agregarAula(Aula("D101", 40, a, 1))
        a.agregarAula(Aula("D102", 30, a, 1))
        self.edificios.append(a)
        
        # EMA5 – 3 pisos (único)
        a = Edificio("EMA5", 1)
        a.agregarAula(Aula("E101", 35, a, 1))
        a.agregarAula(Aula("E102", 40, a, 1))
        a.agregarAula(Aula("E201", 55, a, 2))
        a.agregarAula(Aula("E202", 30, a, 2))
        a.agregarAula(Aula("E301", 30, a, 3))
        self.edificios.append(a)
        
        # EMA6 – 2 pisos
        a = Edificio("EMA6", 1)
        a.agregarAula(Aula("F101", 30, a, 1))
        a.agregarAula(Aula("F102", 40, a, 1))
        a.agregarAula(Aula("F201", 45, a, 2))
        self.edificios.append(a)

        # EMA7 – 1 piso
        a = Edificio("EMA7", 1)
        a.agregarAula(Aula("G101", 55, "EMA7", 1))
        a.agregarAula(Aula("G102", 60, "EMA7", 1))
        self.edificios.append(a)

        # ---------------- Área 2 ---------------- #

        # EMA8 – 2 pisos
        a = Edificio("EMA8", 2)
        a.agregarAula(Aula("H101", 45, a, 1))
        a.agregarAula(Aula("H102", 50, a, 1))
        a.agregarAula(Aula("H201", 40, a, 2))
        self.edificios.append(a)

        # EMA9 – 2 pisos
        a = Edificio("EMA9", 2)
        a.agregarAula(Aula("I101", 30, a, 1))
        a.agregarAula(Aula("I102", 35, a, 1))
        a.agregarAula(Aula("I201", 60, a, 2))
        self.edificios.append(a)

        # EMA10 – 1 piso
        a = Edificio("EMA10", 2)
        a.agregarAula(Aula("J101", 35, a, 1))
        a.agregarAula(Aula("J102", 30, a, 1))
        self.edificios.append(a)


        # ----------- Clases -----------
        clase1 = Clase("Matemáticas", "Dr. Pérez", "08:00")
        clase2 = Clase("Física", "Mtra. López", "09:00")
        clase3 = Clase("Historia", "Lic. Díaz", "10:00")
        clase4 = Clase("Química", "Dr. Ruiz", "11:00")
        # ----------- Asignación (más llenos) -----------
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

        # EMA5 lleno casi toda la semana
        for aula in self.edificios[4].aulas:
            for dia in dias:
                aula.asignarClase(dia, "08:00", clase1)
                aula.asignarClase(dia, "09:00", clase2)
                aula.asignarClase(dia, "10:00", clase3)

        # EMA3 parcialmente llena
        self.edificios[2].aulas[0].asignarClase("Lunes", "08:00", clase1)
        self.edificios[2].aulas[2].asignarClase("Martes", "08:00", clase2)
        self.edificios[2].aulas[2].asignarClase("Miércoles", "09:00", clase3)
        self.edificios[2].aulas[2].asignarClase("Jueves", "10:00", clase4)

        # EMA1 algunas clases
        self.edificios[0].aulas[0].asignarClase("Lunes", "08:00", clase1)
        self.edificios[0].aulas[0].asignarClase("Martes", "09:00", clase2)
        self.edificios[0].aulas[1].asignarClase("Miércoles", "10:00", clase3)

        # EMA2 clase aislada
        self.edificios[1].aulas[0].asignarClase("Lunes", "08:00", clase1)

        # EMA7 una clase
        self.edificios[6].aulas[1].asignarClase("Viernes", "08:00", clase2)

    # Funcion para iniciar la UI
    def iniciarMapa(self):
        self.vistaCampus(1)

    # Funcion para calcular el numero de filas y columnas optimas dado un numero n (filas, columnas)
    def calcularFilasColumnas(self, n):
        columnas = math.ceil(math.sqrt(n))
        filas    = math.ceil(n/columnas)
        return filas, columnas

    # Limpia la cuadricula, misma que sera utilizada en las vistas para dar orden
    def limpiarCuadricula(self):
        cuadriculaVieja = self.panelCuadricula.layout()
        if cuadriculaVieja is not None:
            while cuadriculaVieja.count():
                
                item = cuadriculaVieja.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None) 
            QWidget().setLayout(cuadriculaVieja)                                
        
    # Funcion para mostrar la primera vista del campus (area 1 o 2)
    def vistaCampus(self, area):
        # Obtener información de los edificios del area
        edificiosArea = [ed for ed in self.edificios if ed.area == area]
        filasCuadricula, columnasCuadricula = self.calcularFilasColumnas(len(edificiosArea))
        # Ajuste para mantener un proporcion mejor
        filasAjustadas = filasCuadricula * 2
        columnasAjustadas = columnasCuadricula * 2

        # Limpiar el panel de la cuadricula
        self.limpiarCuadricula()

        # Crear la nueva cuadricula del area correspondiente
        cuadricula = QGridLayout()
        cuadricula.setSpacing(4)

        # Encabezado o titulo de la vista
        titulo = QLabel(f"Benemérita Universidad Autónoma de Puebla - Campus Ciudad Universitaria 2 - Área {area}")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setWordWrap(True)
        cuadricula.addWidget(titulo, 0, 0, 1, columnasAjustadas+2)

        # Relleno para mentener la estetica en el programa
        relleno = QLabel()
        relleno.setStyleSheet("background-color: transparent; border: none;")
        cuadricula.addWidget(relleno, 1, 0, 1, columnasAjustadas+2)

        # Boton para cambio de area
        botonCambioArea = QPushButton("->" if area == 1 else "<-")
        botonCambioArea.setObjectName("boton")
        botonCambioArea.clicked.connect(lambda: self.vistaCampus(2 if area == 1 else 1))
        cuadricula.addWidget(botonCambioArea, filasAjustadas+2, columnasAjustadas+1 if area == 1 else 0)
        index = 0
        for fila in range(0, filasAjustadas, 2):
            for columna in range(0, columnasAjustadas, 2):
                if index < len(edificiosArea):
                    edificio = edificiosArea[index]
                    porcentajeOcupacion = round(edificio.porcentajeOcupadoTotal(), 2)
                    boton = QPushButton(f"{edificio.nombre}\n{porcentajeOcupacion}%")
                    boton.setProperty("porcentajeOcupacion", porcentajeOcupacion)
                    boton.setObjectName("botonEdificio")
                    boton.clicked.connect(lambda checked, e=edificio: self.vistaEdificio(e))
                    cuadricula.addWidget(boton, fila + 2, columna + 1, 2, 2)
                    index += 1
        # Asignar el layout a panelCuadricula (solo aquí)
        self.panelCuadricula.setLayout(cuadricula)
        
        # Panel Derecho con la informacion
        numEdificiosCampus        = len(self.edificios)
        numEdificiosArea          = len(edificiosArea)
        numAulasCampus            = sum(len(e.aulas) for e in self.edificios)
        numAulasArea              = sum(len(e.aulas) for e in edificiosArea)
        porcentajeOcupacionArea   = sum(e.porcentajeOcupadoTotal() for e in edificiosArea) / max(1, numEdificiosArea)
        porcentajeOcupacionCampus = sum(e.porcentajeOcupadoTotal() for e in self.edificios) / max(1, numEdificiosCampus)
        
        # Total de áreas distintas
        totalAreas = len(set(e.area for e in self.edificios))
        
        # Edificio más ocupado en campus
        edificioMasOcupadoCampus = max(self.edificios, key=lambda e: e.porcentajeOcupadoTotal(), default=None)
        
        # Edificio más ocupado en el área
        edificioMasOcupadoArea = max(edificiosArea, key=lambda e: e.porcentajeOcupadoTotal(), default=None)
        
        # Total de bloques no usados en campus
        totalBloquesCampus = sum(len(aula.horario)*len(aula.horas) for e in self.edificios for aula in e.aulas)
        
        bloquesOcupadosCampus = sum(aula.contarClases() for e in self.edificios for aula in e.aulas)

        bloquesLibresCampus = totalBloquesCampus - bloquesOcupadosCampus

        # Total de bloques no usados en área
        totalBloquesArea = sum(len(aula.horario)*len(aula.horas) for e in edificiosArea for aula in e.aulas)
        bloquesOcupadosArea = sum(aula.contarClases() for e in edificiosArea for aula in e.aulas)
        bloquesLibresArea = totalBloquesArea - bloquesOcupadosArea
        
        # Texto formateado
        textoInformativo = f"""\
--------------------------                      
INFORMACION DEL CAMPUS
--------------------------
Total de edificios: {numEdificiosCampus}
Total de aulas: {numAulasCampus}
Total de áreas: {totalAreas}
Ocupación promedio: {porcentajeOcupacionCampus:.1f}%
Edificio más ocupado: {edificioMasOcupadoCampus.nombre if edificioMasOcupadoCampus else "N/A"}
Bloques usados: {bloquesOcupadosCampus}
Bloques sin usar: {bloquesLibresCampus}
--------------------------
INFORMACION DEL ÁREA {area}
--------------------------
Edificios en el área: {numEdificiosArea}
Aulas en el área: {numAulasArea}
        Ocupación promedio: {porcentajeOcupacionArea:.1f}%
Edificio más ocupado: {edificioMasOcupadoArea.nombre if edificioMasOcupadoArea else "N/A"}
Bloques usados: {bloquesOcupadosArea}
Bloques sin usar: {bloquesLibresArea}
--------------------------
"""
        self.panelDerecho.setText(textoInformativo.strip())

        self.gestionLayout()

    def vistaEdificio(self, edificio, pisoActual=1):
        # Obtener informacion del edificio y del piso
        aulasEdificio = edificio.aulas
        aulasPiso     = [a for a in aulasEdificio if a.piso == pisoActual]
        filasCuadricula, columnasCuadricula = self.calcularFilasColumnas(len(aulasPiso))
        pisosEdificio = sorted(list(set(aula.piso for aula in aulasEdificio)))
        # Ajuste para mantener una mejor proporcion
        filasAjustadas = filasCuadricula * 2
        columnasAjustadas = columnasCuadricula * 2

        self.limpiarCuadricula()

        cuadricula = QGridLayout()
        cuadricula.setSpacing(4)
                
        # Título centralizado
        titulo = QLabel(f"BUAP - CU2 - Edificio {edificio.nombre} - Piso {pisoActual}")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setWordWrap(True)
        cuadricula.addWidget(titulo, 0, 0, 1, columnasAjustadas+2)  # centrado horizontalmente

        # Boton para volver al campus
        botonRegresar = QPushButton("x")
        botonRegresar.setObjectName("boton")
        botonRegresar.clicked.connect(lambda: self.vistaCampus(edificio.area))
        cuadricula.addWidget(botonRegresar, 1, 0)
        
        # Boton para el cambio de piso
        if len(pisosEdificio) > 1: # Existe al menos un piso superior
            if pisoActual < len(pisosEdificio):    # Se ocupa crear un boton para subir
                botonSubir = QPushButton("+")
                botonSubir.setObjectName("boton")
                botonSubir.clicked.connect(lambda: self.vistaEdificio(edificio, pisoActual + 1))
                cuadricula.addWidget(botonSubir, 1, columnasAjustadas+1)
            else: # Agregar relleno para que no se pierda la forma
                rellenoSubir = QLabel("")
                rellenoSubir.setStyleSheet("background-color: transparent; border: none; color: transparent;")
                cuadricula.addWidget(rellenoSubir, 1, 1, 1, columnasAjustadas+1)
                
            if pisoActual > 1:     # Se ocupa crear un boton para bajar
                botonBajar = QPushButton("-")
                botonBajar.setObjectName("boton")
                botonBajar.clicked.connect(lambda: self.vistaEdificio(edificio, pisoActual - 1))
                cuadricula.addWidget(botonBajar, filasAjustadas+2, columnasAjustadas+1)
            else: # Agregar relleno para que no se pierda la forma
                rellenoBajar = QLabel()
                rellenoBajar.setStyleSheet("background-color: transparent; border: none; color: transparent;")
                cuadricula.addWidget(rellenoBajar, filasAjustadas+2, 0, 1, columnasAjustadas+2)

        index = 0
        for fila in range(0, filasAjustadas, 2):
            for columna in range(0, columnasAjustadas, 2):
                if index < len(aulasPiso):
                    aula = aulasPiso[index]
                    porcentajeOcupacion = round(aula.porcentajeOcupado(), 2)
                    boton = QPushButton(f"{aula.nombre}\n{porcentajeOcupacion}%")
                    boton.setProperty("porcentajeOcupacion", porcentajeOcupacion)
                    boton.setObjectName("botonEdificio") # Edificio para el estilo
                    boton.clicked.connect(lambda checked, a=aula: self.vistaHorarioAula(a))
                    cuadricula.addWidget(boton, fila + 2, columna + 1, 2, 2)
                    index +=1
        self.panelCuadricula.setLayout(cuadricula)

        # Información a la derecha
        numAulasEdificio = len(aulasEdificio)
        numPisos = len(pisosEdificio)
        porcentajeOcupacionEdificio = round(edificio.porcentajeOcupadoTotal(), 2)
        aulaMasOcupada = max(aulasEdificio, key=lambda a: a.porcentajeOcupado(), default=None)
        totalBloquesEdificio = sum(len(aula.horario)*len(aula.horas) for aula in aulasEdificio)
        bloquesOcupadosEdificio = sum(aula.contarClases() for aula in aulasEdificio)
        bloquesLibresEdificio = totalBloquesEdificio - bloquesOcupadosEdificio

        textoInformativo = f"""\
--------------------------
INFORMACION DEL EDIFICIO
--------------------------
Nombre: {edificio.nombre}
Area: {edificio.area}
Número de aulas: {numAulasEdificio}
Número de pisos: {numPisos}
Ocupación promedio: {porcentajeOcupacionEdificio}%
Aula más ocupada: {aulaMasOcupada.nombre if aulaMasOcupada else "N/A"} ({round(aulaMasOcupada.porcentajeOcupado(), 2) if aulaMasOcupada else 0}%)
Bloques usados: {bloquesOcupadosEdificio}
Bloques sin usar: {bloquesLibresEdificio}
--------------------------
INFORMACIÓN DEL PISO {pisoActual}
--------------------------"""

        # Información detallada por piso
        for piso in pisosEdificio:
            aulasP = [a for a in aulasEdificio if a.piso == pisoActual]
            if not aulasP:
                continue
            
        # Aula más ocupada del piso
        aulaMasOcupadaPiso = max(aulasP, key=lambda a: a.porcentajeOcupado(), default=None)
        ocupacionPiso = sum(a.porcentajeOcupado() for a in aulasP) / len(aulasP)
        totalBloquesPiso = sum(len(a.horario)*len(a.horas) for a in aulasP)
        bloquesOcupadosPiso = sum(a.contarClases() for a in aulasP)
        bloquesLibresPiso = totalBloquesPiso - bloquesOcupadosPiso

        textoInformativo += f"""
        Aulas: {len(aulasP)}
Ocupación promedio: {round(ocupacionPiso, 1)}%
Aula más ocupada: {aulaMasOcupadaPiso.nombre if aulaMasOcupadaPiso else "N/A"} ({round(aulaMasOcupadaPiso.porcentajeOcupado(),2) if aulaMasOcupadaPiso else 0}%)
Bloques usados: {bloquesOcupadosPiso}
Bloques sin usar: {bloquesLibresPiso}"""

        self.panelDerecho.setText(textoInformativo.strip())
        self.gestionLayout()

    def vistaHorarioAula(self, aula):
        self.limpiarCuadricula()

        filasCuadricula, columnasCuadricula = 12, 6
        
        # Crear el layout
        cuadricula = QGridLayout()
        cuadricula.setSpacing(4)
        
        # Título
        titulo = QLabel(f"BUAP - CU2 - Horario del Aula {aula.nombre}")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setWordWrap(True)
        cuadricula.addWidget(titulo, 0, 0, 1, columnasCuadricula)

        # Botón para regresar al edificio
        botonRegresar = QPushButton("x")
        botonRegresar.setObjectName("boton")
        botonRegresar.clicked.connect(lambda: self.vistaEdificio(aula.edificio, aula.piso))
        cuadricula.addWidget(botonRegresar, 1, 0)

        # Encabezados de días (Lunes - Viernes)
        dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
        for col, dia in enumerate(dias):
            labelDia = QLabel(dia)
            labelDia.setAlignment(Qt.AlignCenter)
            labelDia.setObjectName("encabezadoTabla")
            cuadricula.addWidget(labelDia, 2, col + 1)  # columna +1 (col 0 es para horas)

        horas = [f"{h:02d}:00" for h in range(8, 18)]
        for fila, hora in enumerate(horas):
            labelHora = QLabel(hora)
            labelHora.setAlignment(Qt.AlignCenter)
            labelHora.setObjectName("encabezadoTabla")
            cuadricula.addWidget(labelHora, fila + 3, 0)  # fila +3 (título, botón, encabezados)

            # Contenido: clases o vacío
            for col, dia in enumerate(dias):
                for fila, hora in enumerate(horas):
                    clase = aula.horario.get(dia, {}).get(hora)
                    if clase:
                        texto = f"{clase.materia}\n{clase.profesor}"
                    else:
                        texto = ""

                    celda = QLabel(texto)
                    celda.setAlignment(Qt.AlignCenter)
                    celda.setObjectName("celdaTabla")
                    cuadricula.addWidget(celda, fila + 3, col + 1)

        self.panelCuadricula.setLayout(cuadricula)        
                
        # Información a la derecha
        clases = aula.clasesAsignadas()
        porcentaje = aula.porcentajeOcupado()
        textoInformativo = f"""\
--------------------------
INFORMACIÓN DEL AULA
--------------------------
Nombre: {aula.nombre}
Piso: {aula.piso}
Edificio: {aula.nombre}
Capacidad: {aula.capacidad} alumnos
Bloques disponibles: {len(aula.horario)}
Bloques ocupados: {aula.contarClases()}
Porcentaje ocupado: {round(porcentaje, 1)}%
--------------------------
CLASES ASIGNADAS
--------------------------"""
        
        self.panelDerecho.setText(textoInformativo.strip())
        self.gestionLayout()

    
# ------------------------- Boton Sprite -------------------------- | ------------------------------------------------------------
class BotonSprite(QLabel):
    clic = pyqtSignal()
    
    # ------------------------------ Constructor ------------------------------
    def __init__(self, spriteBase, spriteHover, spriteClick, parent=None):
        super().__init__(parent)
        # ----------------------------- Configuracion  -----------------------------
        
        # Cargar las rutas de los archivos
        self.pixmapBase  = QPixmap(spriteBase)
        self.pixmapHover = QPixmap(spriteHover)
        self.pixmapClick = QPixmap(spriteClick)

        self.setPixmap(self.pixmapBase) # Establecer como imagen inicial la base
        self.setCursor(QCursor(Qt.PointingHandCursor)) # Cambiar el mouse
        self.setMouseTracking(True) # Para detectar Hover

        self.estaClickeado = False

    # ----------------------------- Funciones de QT -----------------------------
    
    # Evento para MouseTracking mouse encima del boton
    def enterEvent(self, event): 
        if not self.estaClickeado:
            self.setPixmap(self.pixmapHover)

    # Evento Para MouseTracking mouse afuera del boton
    def leaveEvent(self, event):
        if not self.estaClickeado:
            self.setPixmap(self.pixmapBase)

    # Evento para cuando se presione el boton
    def mousePressEvent(self, event):
        self.estaClickeado = True
        self.setPixmap(self.pixmapClick) # Cambiar el sprite a presionado
        super().mousePressEvent(event) # Llama al metodo del padre

    # Evento para cuando se despresione el boton
    def mouseReleaseEvent(self, event):
        self.estaClickeado = False
        if self.rect().contains(event.pos()): # Si el mouse sigue arriba del boton
            self.setPixmap(self.pixmapHover)
            self.clic.emit()  # Emitir señal personalizada
        else:
            self.setPixmap(self.pixmapBase)
        super().mouseReleaseEvent(event)

# --------------------- Funciones Adicionales --------------------- | ------------------------------------------------------------

"""
Thread que simula el proceso de carga (Temporal)
"""
class trabajoPlaceHolder(QThread):
    terminado = pyqtSignal()

    def run(self):
        time.sleep(1)
        self.terminado.emit()

# ------------------------ Pantalla Inicio ------------------------ | ------------------------------------------------------------

class PantallaInicio(QMainWindow):
    # ------------------------------ Constructor ------------------------------
    def __init__(self):
        super().__init__()
        # ----------------------------- Variables -----------------------------
        self.anchoPantallaMinimo = 800
        self.altoPantallaMinimo  = 450
        self.anchoBotonMinimo  = 320  # Ancho original (64) multiplicado por 5
        self.altoBotonMinimo   = 160  # Ancho original (32) multiplicado por 5
        self.margenBotonMinimo = 0
        
        self.imagenFondoRuta = 'imgs/pantallaInicio.png'
        self.imagenBotonNormalRuta = 'imgs/botonCsvNomal.png'
        self.imagenBotonHoverRuta  = 'imgs/botonCsvHover.png'
        self.imagenBotonClickRuta  = 'imgs/botonCsvClick.png'
        self.animacionPantallaRuta = 'imgs/pantallaCarga'
        # --------------------------- Configuracion  --------------------------
        # Configuración de la ventana
        self.setWindowTitle("PLAN DE MATERIAS Y AULAS BUAP CU2")
        self.setMinimumSize(self.anchoPantallaMinimo, self.altoPantallaMinimo)

        # Mostrar imagen de fondo
        self.labelFondo = QLabel(self)
        self.labelFondo.setScaledContents(False)
        self.labelFondo.lower()

        # Botón personalizado de imagen para cargar CSV
        self.botonCsv = BotonSprite(
            self.imagenBotonNormalRuta,
            self.imagenBotonHoverRuta,
            self.imagenBotonClickRuta,
            self
        )
        self.botonCsv.clic.connect(self.botonCsvClic)  # Conecta la señal personalizada

        # Pantalla de Carga
        self.pantallaCarga = PantallaCarga(self.animacionPantallaRuta, parent=self)
        
        # Pantalla Principal
        self.pantallaPrincipal = PantallaPrincipal()
        self.setCentralWidget(self.pantallaPrincipal)
        self.pantallaPrincipal.hide()

        # Arregla los tamaños y posiciones
        self.gestionPosicionTamaño()
        
    # ------------------------------ Funciones de QT ------------------------------

    # Funcion llamada al redimensionar la ventana
    def resizeEvent(self, evento):
        super().resizeEvent(evento)
        self.gestionPosicionTamaño()
        self.pantallaCarga.resize(self.size())
    
    # ----------------------------- Funciones Propias -----------------------------

    # Funcion para redimensionar los elementos UI
    def gestionPosicionTamaño(self):
        self.gestionFondo()
        self.gestionBoton()
    
    # Funcion para redimensionar el fondo
    def gestionFondo(self):
        pixmap = QPixmap(self.imagenFondoRuta) # Cargar imagen
        if not pixmap.isNull():
            pixmapEscalado = pixmap.scaled(
                self.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.FastTransformation
            )
            # Se establece como nueva imagen, la imagen escalada al nuevo tamaño
            self.labelFondo.setPixmap(pixmapEscalado)
            self.labelFondo.setGeometry(0, 0, self.width(), self.height())

    # Funcion para redimensionar el boton
    def gestionBoton(self):
        anchoVentana = self.width()
        altoVentana  = self.height()

        # Los factores son las relaciones entre los tamaños minimos y actual
        factorAncho = anchoVentana / self.anchoPantallaMinimo
        factorAlto  = altoVentana  / self.altoPantallaMinimo
        factorEscala = min(factorAncho, factorAlto)

        nuevoAnchoBoton = max(self.anchoBotonMinimo, int(self.anchoBotonMinimo * factorEscala))
        nuevoAltoBoton  = max(self.altoBotonMinimo,  int(self.altoBotonMinimo  * factorEscala))
        nuevoMargen = int(self.margenBotonMinimo * factorEscala)
        
        # Escalar pixmaps de la clase BotonImagen
        self.botonCsv.pixmapBase = self.botonCsv.pixmapBase.scaled(
            nuevoAnchoBoton, nuevoAltoBoton, Qt.KeepAspectRatioByExpanding, Qt.FastTransformation
        )
        self.botonCsv.pixmapHover = self.botonCsv.pixmapHover.scaled(
            nuevoAnchoBoton, nuevoAltoBoton, Qt.KeepAspectRatioByExpanding, Qt.FastTransformation
        )
        self.botonCsv.pixmapClick = self.botonCsv.pixmapClick.scaled(
            nuevoAnchoBoton, nuevoAltoBoton, Qt.KeepAspectRatioByExpanding, Qt.FastTransformation
        )
        
        # Actualiza la imagen actual para que coincida con el estado
        self.botonCsv.setPixmap(self.botonCsv.pixmapBase)

        # Actualizar la imagen hasta la esquina derecha inferior
        xPosBoton = anchoVentana - nuevoAnchoBoton - nuevoMargen
        yPosBoton = altoVentana  - nuevoAltoBoton  - nuevoMargen

        self.botonCsv.setGeometry(xPosBoton, yPosBoton, nuevoAnchoBoton, nuevoAltoBoton)

    # Funcion para añadirle funcionalidad al boton CSV
    def botonCsvClic(self):
        self.abrirDialogoCsv() #COMENTADO POR PRUEBAS

        #self.pantallaPrincipal.show()
        #self.pantallaPrincipal.raise_()
        
    # Funcion que gestiona el archivo CSV del usuario
    def abrirDialogoCsv(self):
        rutaArchivo, _ = QFileDialog.getOpenFileName(
            self,
            "Selecciona tu archivo CSV",
            "",
            "Archivos CSV (*.csv);;Todos los archivos (*)"
        )
        if rutaArchivo:
            print("Archivo CSV seleccionado:", rutaArchivo)
            # Añadir verificacion de archivo
            if self.verificarCsv(rutaArchivo) : self.iniciarPantallaCarga()

    # Funcion para verificar que el archivo csv este correcto
    def verificarCsv(self, archivo):
        columnasRequeridas = {'NRC', 'Clave Materia', 'Hola'}
        return 1

    # Funcion para iniciar la pantalla de carga
    def iniciarPantallaCarga(self):
        # Ocultar los elementos actuales
        self.botonCsv.hide()
        self.labelFondo.hide()

        # Metodo interno de la pantalla de carga
        self.pantallaCarga.iniciar()

        # Proceso PlaceHolder
        self.proceso = trabajoPlaceHolder()
        self.proceso.terminado.connect(self.detenerPantallaCarga) # Le decimos que cuando termine, mande a llamar a la funcion
        self.proceso.start()
        
    # Funcion para detener la pantalla de carga
    def detenerPantallaCarga(self):
        
        self.pantallaCarga.detener()
        self.setStyleSheet("background-color: rgb(116,124,156);") # Color gris
        self.pantallaPrincipal.show()
        self.pantallaPrincipal.raise_()
        
# ----------------------------- Main ------------------------------ | ------------------------------------------------------------
def main():
    app = QApplication(sys.argv)
    inicio = PantallaInicio()
    inicio.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

