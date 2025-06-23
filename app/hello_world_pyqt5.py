import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit,
    QPushButton, QWidget, QVBoxLayout
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Greeting App")

        # Central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Input field
        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter your name")

        # Button
        self.button = QPushButton("Say Hello")
        self.button.clicked.connect(self.say_hello)

        # Label
        self.label = QLabel("Hello!")

        # Add widgets to layout
        layout.addWidget(self.input)
        layout.addWidget(self.button)
        layout.addWidget(self.label)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def say_hello(self):
        name = self.input.text().strip()
        if name:
            self.label.setText(f"Hello, {name}!")
        else:
            self.label.setText("Hello!")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
