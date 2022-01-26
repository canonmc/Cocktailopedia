from Model.Cocktail import Cocktail
from PyQt5 import QtWidgets as qtw
from View.MainWindow import Main
from View.Editor import Editor

old_fashioned = Cocktail("Old Fashioned", ("bourbon", 1.5, 'oz'), ("simple syrup", 1, 'oz'), ('bitters', 4, 'dashes'))
# insert(old_fashioned)
#insert(Cocktail("Aviation", ('gin',1.5,'oz'), ('simple syrup','1','oz'), ('vermouth',1,'oz')))

# print(get_recipe(196))

gui = qtw.QApplication([])
window = Main()
window.show()
gui.exec()