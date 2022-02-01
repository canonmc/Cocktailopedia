from PyQt5 import QtWidgets as qtw
from Model.model import get_table, delete, insert
from View.general import clearLayout
from PyQt5.QtGui import QDoubleValidator
from Model.Cocktail import Cocktail

class Editor(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.setLayout(qtw.QVBoxLayout())
        self.stack = qtw.QStackedWidget()
        self.list = EditorCocktailWindow()
        self.creator = EditorCreationWindow()

        self.stack.addWidget(self.list)
        self.stack.addWidget(self.creator)

        self.createButton = qtw.QPushButton('Create a Drink')
        self.createButton.clicked.connect(self.contextSwitch)
        self.layout().addWidget(self.createButton)
        self.layout().addWidget(self.stack)

        child = qtw.QHBoxLayout()
        self.backButton = qtw.QPushButton("Back")
        self.backButton.clicked.connect(self.contextSwitch)
        self.addIngredientButton = qtw.QPushButton("Add ingredient")
        self.addIngredientButton.clicked.connect(self.creator.addIngredientRow)
        self.finishButton = qtw.QPushButton("Create!")
        self.finishButton.clicked.connect(self.creator.createDrink)

        child.addWidget(self.backButton)
        child.addWidget(self.addIngredientButton)
        child.addWidget(self.finishButton)

        self.layout().addLayout(child)
        self.backButton.hide()
        self.addIngredientButton.hide()
        self.finishButton.hide()

    def contextSwitch(self):
        if self.sender() == self.createButton:
            self.createButton.hide()
            self.stack.setCurrentWidget(self.creator)
            self.backButton.show()
            self.addIngredientButton.show()
            self.finishButton.show()
        else:
            self.createButton.show()
            self.stack.setCurrentWidget(self.list)
            self.backButton.hide()
            self.addIngredientButton.hide()
            self.finishButton.hide()

    def update(self):
        self.list.update()
        self.creator.update()


class EditorCocktailWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.setLayout(qtw.QVBoxLayout())
        self.update()

    def update(self):
        clearLayout(self.layout())

        drinks = set(map(lambda x: x[1], get_table('drinks')))
        for i in drinks:
            self.layout().addWidget(EditorCocktailRow(i.title()))

class EditorCreationWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.setLayout(qtw.QVBoxLayout())
        self.update()

    def update(self):
        clearLayout(self.layout())

        self.name = qtw.QLineEdit()
        self.name.setPlaceholderText('Name your drink')
        self.layout().addWidget(self.name)
        self.layout().addWidget(IngredientRow())

    def addIngredientRow(self):
        self.layout().addWidget(IngredientRow())

    def removeIngredientRow(self):
        sender = self.sender()
        for i in range(1,self.layout().count()):
            ingredientRow = self.layout().itemAt(i).widget()
            deleteButton = ingredientRow.layout().itemAt(3).widget()
            if deleteButton == sender:
                clearLayout(ingredientRow.layout())
                ingredientRow.deleteLater()

    def createDrink(self):
        name = self.layout().itemAt(0).widget().text().lower()
        ingredients = []
        for i in range(1,self.layout().count()):
            ingredientRow = self.layout().itemAt(i).widget()
            ingredients.append(ingredientRow.toTuple())
        insert(Cocktail(name, *ingredients))


class EditorCocktailRow(qtw.QWidget):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.setLayout(qtw.QHBoxLayout())
        self.layout().addWidget(qtw.QLabel(name))
        button = qtw.QPushButton('Delete')
        button.clicked.connect(self.delete)
        self.layout().addWidget(button)

    def delete(self):
        delete(self.name)
        self.parent().update()

class IngredientRow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.setLayout(qtw.QHBoxLayout())
        self.ingredient = qtw.QLineEdit()
        self.ingredient.setPlaceholderText('Ingredient')

        self.quantity = qtw.QLineEdit()
        self.quantity.setPlaceholderText('Quantity')
        self.quantity.setValidator(QDoubleValidator())

        self.unit = qtw.QLineEdit()
        self.unit.setPlaceholderText('Units')

        self.deleteButton = qtw.QPushButton('Delete')
        self.deleteButton.clicked.connect(lambda : self.parent().removeIngredientRow())

        self.layout().addWidget(self.ingredient)
        self.layout().addWidget(self.quantity)
        self.layout().addWidget(self.unit)
        self.layout().addWidget(self.deleteButton)

    def toTuple(self):
        return (self.ingredient.text().lower(), float(self.quantity.text()), self.unit.text().lower())