from PyQt5 import QtWidgets as qtw
from Model.model import get_table
from Model.Cocktail import Cocktail

class Editor(qtw.QWidget):
    def __init__(self):
        super().__init__()

        createButton = qtw.QPushButton()
        self.setLayout(qtw.QVBoxLayout())

        self.update()

    def update(self):
        drinks = set(map(lambda x : x[1], get_table('drinks')))
        for i in drinks:
            row = qtw.QHBoxLayout()
            row.addWidget(qtw.QLabel(i))
            row.addWidget(qtw.QPushButton("Update"))
            row.addWidget(qtw.QPushButton("Delete"))
            self.layout().addLayout(row)

