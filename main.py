from Model.Cocktail import Cocktail
from PyQt5 import QtWidgets as qtw
from View.MainWindow import Main
from View.Editor import Editor
from Model.model import delete, get_table, init_db

init_db()

gui = qtw.QApplication([])
window = Main()
window.show()
gui.exec()