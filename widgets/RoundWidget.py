from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from generated.round_widget import Ui_RoundWidget
from dao.DataAccessObjects import TournamentDAO

class RoundWidget(qtw.QWidget):

    def __init__(self, round, parent=None):
        super(RoundWidget, self).__init__(parent)
        self.ui = Ui_RoundWidget()
        self.ui.setupUi(self)

        self.round = round
        self.ui.matches_table.setColumnCount(4)
        self.ui.matches_table.setHorizontalHeaderLabels(('Player White', 'Player Black', 'Result', 'ID'))
        self.ui.matches_table.setColumnWidth(0, 210)
        self.ui.matches_table.setColumnWidth(1, 210)
        self.ui.matches_table.setColumnWidth(2, 80)
        self.ui.matches_table.setColumnWidth(3, 80)
        self.ui.matches_table.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)

        self.ui.sort_box.addItem("White wins")
        self.ui.sort_box.addItem("Black wins")
        self.ui.sort_box.addItem("Draw")
        self.ui.sort_box.activated[str].connect(self.choose_result)
        self.ui.set_button.clicked.connect(self.set_result)
        self.ui.save_button.clicked.connect(self.save_changes)

        self.result = ""

        self.refresh()

    def choose_result(self, text):
        self.result = text

    def refresh(self):
        self.ui.matches_table.setRowCount(0)
        current_row = 0
        for match in self.round.matches:
            self.ui.matches_table.insertRow(current_row)
            self.ui.matches_table.setItem(current_row, 0, qtw.QTableWidgetItem(match.player_white.fullname))
            self.ui.matches_table.setItem(current_row, 1, qtw.QTableWidgetItem(match.player_black.fullname))
            self.ui.matches_table.setItem(current_row, 2, qtw.QTableWidgetItem(str(match.result)))
            self.ui.matches_table.setItem(current_row, 3, qtw.QTableWidgetItem(str(match.match_id)))
            current_row += 1

    def set_result(self, text):
        current_row = self.ui.matches_table.currentRow()
        match_id = int(self.ui.matches_table.item(current_row, 3).text())
        match = filter(lambda m: m.match_id == match_id, self.round.matches).__next__()
        print(match.match_id)
        if self.result == 'White wins':
            match.set_result(1)
        if self.result == "Black wins":
            match.set_result(0)
        if self.result == "Draw":
            match.set_result(0.5)
        self.refresh()

    def save_changes(self):
        tournament_dao = TournamentDAO()
        tournament_dao.update_tournament(self.round.tournament)
