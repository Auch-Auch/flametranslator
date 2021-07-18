from PyQt5.QtWidgets import QWidget, QLabel, QSizePolicy
from PyQt5.QtCore import Qt


class TranslationInfo(QWidget):

    def __init__(self):
        super().__init__()
        self.label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignLeft)
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Translation')

    def show_text(self, text:str):
        self.label.setText(text)
        self.show()
