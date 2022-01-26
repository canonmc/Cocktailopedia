from PyQt5 import QtWidgets as qtw

from View.Selector import Selector
from View.Editor import Editor

class Main(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())
        self.setWindowTitle('Cocktailopedia!')
        self.tab = qtw.QTabWidget()
        self.layout().addWidget(self.tab)
        self.setGeometry(150, 150, 750, 1000)

        self.tab.addTab(Selector(), 'Filter')
        self.tab.addTab(Editor(), "Editor")