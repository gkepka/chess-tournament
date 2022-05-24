from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from generated.list_tournaments_widget import Ui_ListTournaments
from dao.DataAccessObjects import TournamentDAO
from widgets.DeleteTournamentDialog import DeleteTournamentDialog


class ListTournamentsWidget(qtw.QWidget):

    tournament_chosen = qtc.pyqtSignal(int)
    tournament_to_delete = qtc.pyqtSignal(int)
    tournament_to_edit = qtc.pyqtSignal(int)

    def __init__(self, parent=None):
        super(ListTournamentsWidget, self).__init__(parent)
        self.ui = Ui_ListTournaments()
        self.ui.setupUi(self)

        self.ui.tournaments_table.setColumnCount(4)
        self.ui.tournaments_table.setHorizontalHeaderLabels(('Name', 'Rounds', 'Date', 'ID'))
        self.ui.tournaments_table.setColumnWidth(0, 240)
        self.ui.tournaments_table.setColumnWidth(1, 90)
        self.ui.tournaments_table.setColumnWidth(2, 150)
        self.ui.tournaments_table.setColumnWidth(3, 100)
        self.ui.tournaments_table.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)

        self.tournament_dao = TournamentDAO()
        tournaments = self.tournament_dao.get_all_tournaments()

        self.fill_tournaments_table(tournaments)

        self.ui.sort_box.addItem("Name")
        self.ui.sort_box.addItem("Date")

        self.ui.sort_box.activated[str].connect(self.sort_table)

        self.ui.choose_button.clicked.connect(self.choose_tournament)
        self.ui.delete_button.clicked.connect(self.delete_tournament)
        self.ui.edit_button.clicked.connect(self.edit_tournament)

    def fill_tournaments_table(self, tournaments):
        self.ui.tournaments_table.setRowCount(0)
        current_row = 0
        for tournament in tournaments:
            self.ui.tournaments_table.insertRow(current_row)
            self.ui.tournaments_table.setItem(current_row, 0, qtw.QTableWidgetItem(tournament.name))
            self.ui.tournaments_table.setItem(current_row, 1, qtw.QTableWidgetItem(str(tournament.rounds)))
            self.ui.tournaments_table.setItem(current_row, 2, qtw.QTableWidgetItem(str(tournament.date)))
            self.ui.tournaments_table.setItem(current_row, 3, qtw.QTableWidgetItem(str(tournament.tournament_id)))

    def sort_table(self, text):
        if text == "Name":
            tournaments = self.tournament_dao.get_all_tournaments()
            tournaments = sorted(tournaments, key=lambda tournament: tournament.name, reverse=True)
            self.fill_tournaments_table(tournaments)
        if text == "Date":
            tournaments = self.tournament_dao.get_all_tournaments()
            tournaments = sorted(tournaments, key=lambda tournament: tournament.date)
            self.fill_tournaments_table(tournaments)

    def choose_tournament(self):
        current_row = self.ui.tournaments_table.currentRow()
        if current_row != -1:
            id = int(self.ui.tournaments_table.item(current_row, 3).text())
            self.tournament_chosen.emit(id)

    def delete_tournament(self):
        current_row = self.ui.tournaments_table.currentRow()
        if current_row != -1:
            id = int(self.ui.tournaments_table.item(current_row, 3).text())
            dialog = DeleteTournamentDialog()
            if dialog.exec_():
                self.tournament_to_delete.emit(id)
                self.fill_tournaments_table(self.tournament_dao.get_all_tournaments())

    def edit_tournament(self):
        current_row = self.ui.tournaments_table.currentRow()
        if current_row != -1:
            id = int(self.ui.tournaments_table.item(current_row, 3).text())
            self.tournament_to_edit.emit(id)
