import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow


class MyWindow(QMainWindow):
    def __init__(self):
            super(MyWindow, self).__init__()
            self.setGeometry(200, 200, 300, 300)
            self.setWindowTitle("Clue Bot")
            self.initUI()

    def initUI(self):
            self.label = QtWidgets.QLabel(self)
            self.label.setText("my first label")
            self.label.move(50, 50)

            self.b1 = QtWidgets.QPushButton(self)
            self.b1.setText("click me")
            self.b1.clicked.connect(self.clicked)

    def clicked(self):
            self.label.setText("you pressed the REAL button")

    def update(self):
            self.label.adjustSize()


def window():
        app = QApplication(sys.argv)
        win = MyWindow()
        win.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    window()
