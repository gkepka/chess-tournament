from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from datetime import date

from generated.edit_tournament_widget import Ui_EditTournament

from dao.DataAccessObjects import RoundDAO


class EditTournamentWidget(qtw.QWidget):

    tournament_to_save = qtc.pyqtSignal(object, list, list) # tournament with changed data, new player list, generated rounds
    round_to_edit = qtc.pyqtSignal(int)
    edit_players_signal = qtc.pyqtSignal(object, list) # tournament_id, list of players (nonempty if edited earlier)

    def __init__(self, tournament, parent=None):
        super(EditTournamentWidget, self).__init__(parent)
        self.tournament = tournament
        self.players = []
        self.generated_rounds = []

        self.ui = Ui_EditTournament()
        self.ui.setupUi(self)

        self.ui.tournament_name_edit.setText(tournament.name)
        self.ui.tournament_date_edit.setText(str(tournament.date))
        self.ui.tournament_rounds_edit.setText(str(tournament.rounds))

        self.ui.rounds_table.setColumnCount(2)
        self.ui.rounds_table.setHorizontalHeaderLabels(('Round number', 'ID'))
        self.ui.rounds_table.setColumnWidth(0, 240)
        self.ui.rounds_table.setColumnWidth(1, 150)
        self.ui.rounds_table.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)

        self.round_dao = RoundDAO()
        rounds = self.round_dao.get_rounds_by_tournament_id(self.tournament.tournament_id)
        self.fill_rounds_table(rounds)

        self.ui.edit_players_button.clicked.connect(self.edit_players)
        self.ui.edit_tournament_button.clicked.connect(self.save_changes)
        self.ui.edit_rounds_button.clicked.connect(self.edit_round)
        self.ui.generate_button.clicked.connect(self.generate_rounds)

    def fill_rounds_table(self, rounds):
        self.ui.rounds_table.setRowCount(0)
        current_row = 0
        for round in rounds:
            self.ui.rounds_table.insertRow(current_row)
            self.ui.rounds_table.setItem(current_row, 0, qtw.QTableWidgetItem(str(round.get_round_no())))
            self.ui.rounds_table.setItem(current_row, 1, qtw.QTableWidgetItem(str(round.round_id)))
            current_row += 1

    def edit_players(self):
        if len(self.tournament.rounds_list) != 0 or len(self.generated_rounds) != 0:
            qtw.QMessageBox.critical(self, 'Error', 'Can\'t change players after generating rounds')
        self.edit_players_signal.emit(self.tournament, self.players)

    @qtc.pyqtSlot(list)
    def update_player_list(self, player_list):
        self.players.extend(player_list)

    def save_changes(self):
        try:
            tournament_name = self.ui.tournament_name_edit.text()
            tournament_date = date.fromisoformat(self.ui.tournament_date_edit.text())
            tournament_rounds = int(self.ui.tournament_rounds_edit.text())
            added_players = self.players
            rounds_list = self.generated_rounds
        except ValueError as e:
            if str(e).count("invalid literal for int()") != 0:
                qtw.QMessageBox.critical(self, 'Error', 'Round count must be a number')
                self.ui.tournament_rounds_edit.clear()
            if str(e).count("Invalid isoformat string") != 0:
                qtw.QMessageBox.critical(self, 'Error', 'Date must be in format YYYY-MM-DD')
                self.ui.tournament_date_edit.clear()
        else:
            self.tournament.name = tournament_name
            self.tournament.date = tournament_date
            self.tournament.rounds = tournament_rounds
            self.tournament.rounds_list = rounds_list
            self.tournament_to_save.emit(self.tournament, self.players, self.generated_rounds)

    def edit_round(self):
        pass

    def generate_rounds(self):
        pass
