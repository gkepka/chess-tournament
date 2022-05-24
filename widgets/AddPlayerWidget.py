from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from generated.add_player_widget import Ui_AddPlayer

class AddPlayerWidget(qtw.QWidget):
    player_added = qtc.pyqtSignal(str, str, int, str, str, str)

    def __init__(self, parent=None):
        super(AddPlayerWidget, self).__init__(parent)
        self.ui = Ui_AddPlayer()
        self.ui.setupUi(self)
        self.ui.add_player_button.clicked.connect(self.add_player)

    def add_player(self):
        try:
            first_name = self.ui.firstname_edit.text()
            last_name = self.ui.last_name_edit.text()
            ranking = int(self.ui.ranking_edit.text())
            nationality = self.ui.nationality_edit.text()
            if len(nationality) > 3:
                raise ValueError('nationality')
            title = self.ui.title_edit.text()
            chess_club = self.ui.chessclub_edit.text()
        except ValueError as e:
            if str(e).count("invalid literal for int()") != 0:
                qtw.QMessageBox.critical(self, 'Error', 'Ranking must be a number')
                self.ui.ranking_edit.clear()
            if str(e).count("nationality") != 0:
                qtw.QMessageBox.critical(self, 'Error', 'Provide 2-3 letter country code')
                self.ui.nationality_edit.clear()
        else:
            self.player_added.emit(first_name, last_name, ranking,
                                   nationality, title, chess_club)
            self.clear_edits()

    def clear_edits(self):
        self.ui.firstname_edit.clear()
        self.ui.last_name_edit.clear()
        self.ui.ranking_edit.clear()
        self.ui.nationality_edit.clear()
        self.ui.title_edit.clear()
        self.ui.chessclub_edit.clear()