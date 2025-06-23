import sys
import psycopg2
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PostgreSQL Data Viewer")

        # Layout
        self.table = QTableWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Load data
        self.load_data()

    def load_data(self):
        try:
            # Replace with your actual credentials
            conn = psycopg2.connect(
                host="localhost",
                dbname="buap",
                user="postgres",
                password="1234"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM Profesor")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            self.table.setRowCount(len(rows))
            self.table.setColumnCount(len(columns))
            self.table.setHorizontalHeaderLabels(columns)

            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            cursor.close()
            conn.close()

        except Exception as e:
            print("Error loading data:", e)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
