from PyQt5 import QtWidgets as qtw
from PyQt5 import Qt as qt
from PyQt5.QtCore import Qt as qtcqt
from Model.model import organize_ingredients, get_possible, get_recipe
from View.CocktailWindow import CocktailWindow
from View.general import clearLayout

class Selector(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())
        self.stack = qtw.QStackedWidget()
        self.checklist = ScrollableCheckList()
        self.recipe = RecipeWindow()
        self.stack.addWidget(self.checklist)
        self.stack.addWidget(self.recipe)

        self.layout().addWidget(self.stack)

        self.goButton = qtw.QPushButton("Go")
        self.backButton = qtw.QPushButton("Back")
        self.backButton.clicked.connect(self.contextSwitch)
        self.goButton.clicked.connect(self.contextSwitch)
        self.layout().addWidget(self.goButton)
        self.layout().addWidget(self.backButton)
        self.backButton.hide()

    def contextSwitch(self):
        if self.stack.currentWidget() == self.checklist:
            ingredients = []
            i = 3
            cl = self.checklist.children()
            while i < len(cl):
                if type(cl[i]) is qtw.QCheckBox and cl[i].isChecked():
                    ingredients.append(cl[i-1].text())
                i += 1

            self.recipe.update(ingredients)
            self.stack.setCurrentWidget(self.recipe)
            self.goButton.hide()
            self.backButton.show()
        else:
            self.stack.setCurrentWidget(self.checklist)
            self.backButton.hide()
            self.goButton.show()


class ScrollableCheckList(qtw.QScrollArea):
    def __init__(self):
        super().__init__()

        widget = qtw.QWidget()
        self.setLayout(qtw.QVBoxLayout(widget))
        self.layout().setAlignment(qtcqt.AlignTop)
        header = qtw.QLabel("Liquors")
        header.setFont(qt.QFont('Arial', 20))
        self.layout().addWidget(header)
        for i in organize_ingredients()[0]:
            row_layout = qtw.QHBoxLayout()
            txt = qtw.QLabel(i)
            txt.setFont(qt.QFont('Arial', 15))
            checkbox = qtw.QCheckBox()

            row_layout.addWidget(txt)
            row_layout.addWidget(checkbox)

            self.layout().addLayout(row_layout)

        self.layout().addSpacerItem(qtw.QSpacerItem(50, 50, qtw.QSizePolicy.Expanding))

        header = qtw.QLabel("Other")
        header.setFont(qt.QFont('Arial', 20))
        self.layout().addWidget(header)
        for i in organize_ingredients()[1]:
            row_layout = qtw.QHBoxLayout()
            txt = qtw.QLabel(i)
            txt.setFont(qt.QFont('Arial', 15))

            checkbox = qtw.QCheckBox()
            row_layout.addWidget(txt)
            row_layout.addWidget(checkbox)

            self.layout().addLayout(row_layout)


class RecipeWindow(qtw.QScrollArea):
    def __init__(self):
        super().__init__()
        widget = qtw.QWidget()
        self.setLayout(qtw.QVBoxLayout(widget))
        self.layout().setAlignment(qtcqt.AlignTop)


    def update(self, ingredients):
        clearLayout(self.layout())
        possible_drinks = get_possible(*ingredients)
        for id in possible_drinks:
            drink = get_recipe(id)
            self.layout().addWidget(CocktailWindow(drink))
