from PyQt5 import QtWidgets as qtw
from PyQt5 import Qt as qt
from Model.Cocktail import Cocktail

class CocktailWindow(qtw.QWidget):
    def __init__(self, drink : Cocktail):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())
        name = qtw.QLabel(drink.name)
        name.setFont(qt.QFont('Arial', 20))
        self.layout().addWidget(name)
        for item,amount in drink.ingredients.items():
            nextIngredient = qtw.QLabel(f'{amount[0]} {amount[1]} of {item}')
            nextIngredient.setFont(qt.QFont('Arial', 15))
            self.layout().addWidget(nextIngredient)