import sys
import psycopg2
from PyQt5.QtGui import QIntValidator, QFont, QColor, QPalette
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QMessageBox,
    QDialog, QComboBox, QLineEdit, QFormLayout, QDialogButtonBox,
    QSpinBox
)
from datetime import datetime
from PyQt5.QtCore import Qt, QPoint
import csv

#5414a1
# Función para aplicar estilo moderno minimalista en modo oscuro
def estilo_moderno(widget):
    app_palette = QPalette()
    app_palette.setColor(QPalette.Window, QColor("#121212"))
    app_palette.setColor(QPalette.WindowText, QColor("#ffffff"))
    app_palette.setColor(QPalette.Base, QColor("#1e1e1e"))
    app_palette.setColor(QPalette.AlternateBase, QColor("#2e2e2e"))
    app_palette.setColor(QPalette.ToolTipBase, QColor("#353535"))
    app_palette.setColor(QPalette.ToolTipText, QColor("#ffffff"))
    app_palette.setColor(QPalette.Text, QColor("#ffffff"))
    app_palette.setColor(QPalette.Button, QColor("#2d2d2d"))
    app_palette.setColor(QPalette.ButtonText, QColor("#ffffff"))
    app_palette.setColor(QPalette.Highlight, QColor("#5414a1"))
    app_palette.setColor(QPalette.HighlightedText, QColor("#000000"))

    widget.setPalette(app_palette)

    widget.setStyleSheet('''
        QMainWindow, QDialog {
            background-color: #121212;
            color: #ffffff;
        }
        QPushButton {
            background-color: #5414a1;
            color: white;
            border-radius: 8px;
            padding: 8px 14px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #9f6fe0;
        }
        QTableWidget {
            background-color: #1e1e1e;
            color: #ffffff;
            gridline-color: #444444;
            font-size: 14px;
        }
        QHeaderView::section {
            background-color: #2d2d2d;
            color: #ffffff;
            font-weight: bold;
            padding: 6px;
            border: none;
        }
        
        QPushButton#eliminarBtn {
            background-color: #ff4c4c;
        }
        QPushButton#eliminarBtn:hover {
            background-color: #e63946;
        }                 

        QComboBox, QLineEdit, QSpinBox {
            background-color: #2d2d2d;
            color: #ffffff;
            border: 1px solid #ffffff;
            padding: 6px;
            
            border-radius: 4px;
            font-size: 14px;
            min-width: 100px;
            min-height: 20px;
        }
        QFormLayout QLabel {
            color: #ffffff;
            font-size: 13px;
        }
    ''')

class AgregarMateriaDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agregar Materia")

        self.programaCombo = QComboBox()
        self.materiaCombo = QComboBox()
        self.cupoInput = QLineEdit()

        self.cupoInput.setPlaceholderText("Ingrese el cupo (entre 1 y 100)")
        self.cupoInput.setValidator(QIntValidator(1, 100))

        self.programa_ids = {}
        self.programa_abrevs = {}
        self.loadProgramas()
        self.programaCombo.currentTextChanged.connect(self.actualizarMaterias)

        formLayout = QFormLayout()
        formLayout.addRow("Programa Educativo:", self.programaCombo)
        formLayout.addRow("Materia:", self.materiaCombo)
        formLayout.addRow("Cupo:", self.cupoInput)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.validarYaceptar)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(formLayout)
        layout.addWidget(buttons)
        self.setLayout(layout)
        estilo_moderno(self)

    def loadProgramas(self):
        try:
            conn = psycopg2.connect(host="localhost", dbname="buap", user="dabidurazo", password="dabi") # Cambiar por credenciales propias
            cursor = conn.cursor()
            cursor.execute("SELECT id_programa_educativo, nombre, abreviatura FROM programa_educativo")
            programas = cursor.fetchall()
            for id_prog, nombre, abrev in programas:
                self.programa_ids[nombre] = id_prog
                self.programa_abrevs[nombre] = abrev
                self.programaCombo.addItem(nombre)
            cursor.close()
            conn.close()
            self.actualizarMaterias(self.programaCombo.currentText())
        except Exception as e:
            print("Error cargando programas:", e)

    def actualizarMaterias(self, programaNombre):
        self.materiaCombo.clear()
        id_prog = self.programa_ids.get(programaNombre)
        if id_prog is None:
            return
        try:
            conn = psycopg2.connect(host="localhost", dbname="buap", user="dabidurazo", password="dabi")  # Cambiar por credenciales propias
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT nombre FROM materia WHERE id_programa_educativo = %s", (id_prog,))
            materias = cursor.fetchall()
            self.materiaCombo.addItems([m[0] for m in materias])
            cursor.close()
            conn.close()
        except Exception as e:
            print("Error actualizando materias:", e)

    def validarYaceptar(self):
        cupoTexto = self.cupoInput.text().strip()
        if not cupoTexto.isdigit():
            QMessageBox.warning(self, "Cupo inválido", "Por favor, ingrese un número válido para el cupo.")
            return
        cupo = int(cupoTexto)
        if cupo < 1 or cupo > 100:
            QMessageBox.warning(self, "Rango inválido", "El cupo debe estar entre 1 y 100.")
            return
        self.accept()

    def getData(self):
        return (
            self.materiaCombo.currentText(),
            self.programa_abrevs.get(self.programaCombo.currentText(), ""),
            self.cupoInput.text()
        )

class AgregarBloqueDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agregar Bloque")

        self.programaCombo = QComboBox()
        self.semestreCombo = QComboBox()
        self.cupoInput = QLineEdit()

        self.cupoInput.setPlaceholderText("Ingrese el cupo (entre 1 y 100)")
        self.cupoInput.setValidator(QIntValidator(1, 100))

        self.programa_ids = {}
        self.programa_abrevs = {}
        self.loadProgramas()
        self.programaCombo.currentTextChanged.connect(self.actualizarSemestres)

        formLayout = QFormLayout()
        formLayout.addRow("Programa Educativo:", self.programaCombo)
        formLayout.addRow("Semestre:", self.semestreCombo)
        formLayout.addRow("Cupo:", self.cupoInput)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.validarYaceptar)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(formLayout)
        layout.addWidget(buttons)
        self.setLayout(layout)
        estilo_moderno(self)

    def loadProgramas(self):
        try:
            conn = psycopg2.connect(host="localhost", dbname="buap", user="dabidurazo", password="dabi")  # Cambiar por credenciales propias
            cursor = conn.cursor()
            cursor.execute("SELECT id_programa_educativo, nombre, abreviatura FROM programa_educativo")
            programas = cursor.fetchall()
            for id_prog, nombre, abrev in programas:
                self.programa_ids[nombre] = id_prog
                self.programa_abrevs[nombre] = abrev
                self.programaCombo.addItem(nombre)
            cursor.close()
            conn.close()
            self.actualizarSemestres(self.programaCombo.currentText())
        except Exception as e:
            print("Error cargando programas:", e)

    def actualizarSemestres(self, programaNombre):
        self.semestreCombo.clear()
        id_prog = self.programa_ids.get(programaNombre)
        if id_prog is None:
            return
        try:
            conn = psycopg2.connect(host="localhost", dbname="buap", user="dabidurazo", password="dabi")  # Cambiar por credenciales propias
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT semestre FROM materia WHERE id_programa_educativo = %s AND semestre > 0 ORDER BY semestre", (id_prog,))
            semestres = cursor.fetchall()
            for s in semestres:
                self.semestreCombo.addItem(str(s[0]))
            cursor.close()
            conn.close()
        except Exception as e:
            print("Error actualizando semestres:", e)

    def validarYaceptar(self):
        cupoTexto = self.cupoInput.text().strip()
        if not cupoTexto.isdigit():
            QMessageBox.warning(self, "Cupo inválido", "Ingrese un número válido para el cupo.")
            return
        cupo = int(cupoTexto)
        if cupo < 1 or cupo > 100:
            QMessageBox.warning(self, "Rango inválido", "El cupo debe estar entre 1 y 100.")
            return
        self.accept()

    def getData(self):
        progNombre = self.programaCombo.currentText()
        abrev = self.programa_abrevs.get(progNombre, "")
        semestre = self.semestreCombo.currentText()
        return (abrev, semestre, self.cupoInput.text())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Materias y Bloques")
        self.resize(700, 600)

        self.bloque_indices = {}

        self.dataTable = QTableWidget()
        self.dataTable.setColumnCount(4)
        self.dataTable.setHorizontalHeaderLabels(["Programa", "Materia", "Bloque", "Cupo"])
        self.dataTable.horizontalHeader().setStretchLastSection(True)
        for i in range(4):
            self.dataTable.horizontalHeader().setSectionResizeMode(i, 1)

        self.dataTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.dataTable.setSelectionMode(QTableWidget.MultiSelection)
        self.dataTable.setContextMenuPolicy(Qt.CustomContextMenu)

        self.addMateriaBtn = QPushButton("Agregar Materia")
        self.addBloqueBtn = QPushButton("Agregar Bloque")
        self.saveBtn = QPushButton("Generar")
        self.deleteBtn = QPushButton("Eliminar Seleccionado")

        self.deleteBtn.setObjectName("eliminarBtn")

        self.addMateriaBtn.clicked.connect(self.agregarMateria)
        self.addBloqueBtn.clicked.connect(self.agregarBloque)
        self.saveBtn.clicked.connect(self.guardar)
        self.deleteBtn.clicked.connect(self.eliminarFilaSeleccionada)

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.dataTable)

        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.addMateriaBtn)
        rightLayout.addWidget(self.addBloqueBtn)
        rightLayout.addWidget(self.saveBtn)
        rightLayout.addWidget(self.deleteBtn)
        rightLayout.addStretch()

        mainLayout = QHBoxLayout()
        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(rightLayout)

        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)


    def agregarMateria(self):
        dialog = AgregarMateriaDialog()
        if dialog.exec_() == QDialog.Accepted:
            materia, abrev, cupo = dialog.getData()
            rowCount = self.dataTable.rowCount()
            self.dataTable.insertRow(rowCount)
            self.setCell(rowCount, 0, abrev)
            self.setCell(rowCount, 1, materia)
            self.setCell(rowCount, 2, "")
            self.setCell(rowCount, 3, cupo)

    def agregarBloque(self):
        periodo_dialog = PeriodoDialog()
        if periodo_dialog.exec_() != QDialog.Accepted:
            return

        periodo, anio = periodo_dialog.getPeriodoYAnio()

        dialog = AgregarBloqueDialog()
        if dialog.exec_() == QDialog.Accepted:
            abrev, semestre, cupo = dialog.getData()

            try:
                conn = psycopg2.connect(host="localhost", dbname="buap", user="dabidurazo", password="dabi")
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT nombre FROM materia 
                    WHERE id_programa_educativo = (
                        SELECT id_programa_educativo FROM programa_educativo WHERE abreviatura = %s
                    ) AND semestre = %s
                """, (abrev, semestre))

                materias = cursor.fetchall()
                cursor.close()
                conn.close()

                if not materias:
                    QMessageBox.information(self, "Sin materias", "No se encontraron materias para ese programa y semestre.")
                    return

                # Llevar control del índice por programa educativo
                if not hasattr(self, 'bloque_indices'):
                    self.bloque_indices = {}

                idx = self.bloque_indices.get(abrev, 1)
                bloque_id = f"{abrev}{idx:02d}{anio:02d}{periodo}"
                self.bloque_indices[abrev] = idx + 1

                for materia in materias:
                    rowCount = self.dataTable.rowCount()
                    self.dataTable.insertRow(rowCount)
                    self.setCell(rowCount, 0, abrev)
                    self.setCell(rowCount, 1, materia[0])
                    self.setCell(rowCount, 2, bloque_id)
                    self.setCell(rowCount, 3, cupo)

            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudieron cargar las materias: {e}")


    def guardar(self):
        try:
            with open("exportado.csv", "w", newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                headers = [self.dataTable.horizontalHeaderItem(i).text() for i in range(self.dataTable.columnCount())]
                writer.writerow(headers)
                for row in range(self.dataTable.rowCount()):
                    fila = [self.dataTable.item(row, col).text() if self.dataTable.item(row, col) else "" for col in range(self.dataTable.columnCount())]
                    writer.writerow(fila)
            QMessageBox.information(self, "Éxito", "Los datos fueron exportados a 'exportado.csv'.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo exportar el CSV:\n{e}")

    def eliminarFilaSeleccionada(self):
        selectedRows = sorted(set(index.row() for index in self.dataTable.selectedIndexes()), reverse=True)
        if not selectedRows:
            QMessageBox.information(self, "Eliminar", "Selecciona al menos una fila para eliminar.")
            return
        for row in selectedRows:
            self.dataTable.removeRow(row)

    def setCell(self, row, col, text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        self.dataTable.setItem(row, col, item)

def eliminarFilaSeleccionada(self):
    selectedRows = set(index.row() for index in self.dataTable.selectedIndexes())
    for row in sorted(selectedRows, reverse=True):
        self.dataTable.removeRow(row)

class PeriodoDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seleccionar Periodo y Año")
        self.setFixedSize(300, 150)
        self.periodoCombo = QComboBox()
        self.periodoCombo.addItems(["Primavera", "Otoño"])
        self.anioSpin = QSpinBox()
        self.anioSpin.setRange(2020, 2100)
        self.anioSpin.setValue(datetime.now().year)

        layout = QFormLayout()
        layout.addRow("Periodo:", self.periodoCombo)
        layout.addRow("Año:", self.anioSpin)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        vlayout = QVBoxLayout()
        vlayout.addLayout(layout)
        vlayout.addWidget(buttons)
        self.setLayout(vlayout)
        estilo_moderno(self)

    def getPeriodoYAnio(self):
        periodo = "PR" if self.periodoCombo.currentText() == "Primavera" else "OT"
        anio = self.anioSpin.value() % 100
        return periodo, anio

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    estilo_moderno(window)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
