from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from datetime import date

from generated.edit_tournament_widget import Ui_EditTournament

from dao.DataAccessObjects import RoundDAO
from dao.DataAccessObjects import TournamentDAO


class EditTournamentWidget(qtw.QWidget):

    round_to_edit = qtc.pyqtSignal(int)
    round_to_delete = qtc.pyqtSignal(int)
    edit_players_signal = qtc.pyqtSignal(object) # tournament_id

    def __init__(self, tournament, parent=None):
        super(EditTournamentWidget, self).__init__(parent)
        self.tournament = tournament
        self.players = [params.player for params in self.tournament.params_list]

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

        self.tournament_dao = TournamentDAO()
        self.round_dao = RoundDAO()
        rounds = self.round_dao.get_rounds_by_tournament_id(self.tournament.tournament_id)
        self.fill_rounds_table(rounds)

        self.ui.edit_players_button.clicked.connect(self.edit_players)
        self.ui.edit_tournament_button.clicked.connect(self.save_changes)
        self.ui.edit_rounds_button.clicked.connect(self.edit_round)
        self.ui.new_round_button.clicked.connect(self.new_round)

    def fill_rounds_table(self, rounds):
        self.ui.rounds_table.setRowCount(0)
        current_row = 0
        for round in rounds:
            self.ui.rounds_table.insertRow(current_row)
            self.ui.rounds_table.setItem(current_row, 0, qtw.QTableWidgetItem(str(round.get_round_no())))
            self.ui.rounds_table.setItem(current_row, 1, qtw.QTableWidgetItem(str(round.round_id)))
            current_row += 1

    def append_round_to_table(self, round):
        current_row = self.ui.rounds_table.rowCount()
        self.ui.rounds_table.insertRow(current_row)
        self.ui.rounds_table.setItem(current_row, 0, qtw.QTableWidgetItem(str(round.get_round_no())))
        self.ui.rounds_table.setItem(current_row, 1, qtw.QTableWidgetItem(str(round.round_id)))

    def edit_players(self):
        if len(self.tournament.rounds_list) != 0:
            qtw.QMessageBox.critical(self, 'Error', 'Can\'t change players after generating rounds')
            return
        self.edit_players_signal.emit(self.tournament)

    @qtc.pyqtSlot(list)
    def update_player_list(self, player_list):
        self.players = player_list

    def save_changes(self):
        try:
            tournament_name = self.ui.tournament_name_edit.text()
            tournament_date = date.fromisoformat(self.ui.tournament_date_edit.text())
            tournament_rounds = int(self.ui.tournament_rounds_edit.text())
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

            players_in_tournament = [params.player for params in self.tournament.params_list]
            params_to_remove = [params for params in self.tournament.params_list if params.player not in self.players]
            new_players = [player for player in self.players if player not in players_in_tournament]

            for player in new_players:
                self.tournament.add_player_params_from_player(player)

            for params in params_to_remove:
                self.tournament.del_player_params(params)

            self.tournament_dao.update_tournament(self.tournament)
            self.fill_rounds_table(self.tournament.rounds_list)

    def edit_round(self):
        current_row = self.ui.rounds_table.currentRow()
        id = int(self.ui.rounds_table.item(current_row, 1).text())
        self.round_to_edit.emit(id)

    def delete_round(self):
        current_row = self.ui.rounds_table.currentRow()
        id = int(self.ui.rounds_table.item(current_row, 1).text())
        self.round_to_delete.emit(id)

    def new_round(self):
        if not self.tournament.can_generate():
            qtw.QMessageBox.critical(self, 'Error', 'Can\'t generate next round after choosing a winner')
            return
        self.tournament.next_round()
        self.append_round_to_table(self.tournament.rounds_list[len(self.tournament.rounds_list) - 1])

