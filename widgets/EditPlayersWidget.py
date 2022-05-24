from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from generated.edit_players_widget import Ui_EditPlayers

from dao.DataAccessObjects import PlayerDAO


class EditPlayersWidget(qtw.QWidget):

    submitted = qtc.pyqtSignal(list) # new list of players
    return_to_edit_tournament = qtc.pyqtSignal(object)

    def __init__(self, tournament, parent=None):
        super(EditPlayersWidget, self).__init__(parent)
        self.ui = Ui_EditPlayers()
        self.ui.setupUi(self)
        self.players = [params.player for params in tournament.params_list]

        self.tournament = tournament

        self.ui.not_in_tournament_table.setColumnCount(3)
        self.ui.not_in_tournament_table.setHorizontalHeaderLabels(('Name', 'Ranking', 'ID'))
        self.ui.not_in_tournament_table.setColumnWidth(0, 160)
        self.ui.not_in_tournament_table.setColumnWidth(1, 90)
        self.ui.not_in_tournament_table.setColumnWidth(2, 70)
        self.ui.not_in_tournament_table.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
        self.ui.in_tournament_table.setColumnCount(3)
        self.ui.in_tournament_table.setHorizontalHeaderLabels(('Name', 'Ranking', 'ID'))
        self.ui.in_tournament_table.setColumnWidth(0, 160)
        self.ui.in_tournament_table.setColumnWidth(1, 90)
        self.ui.in_tournament_table.setColumnWidth(2, 70)
        self.ui.in_tournament_table.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)

        self.player_dao = PlayerDAO()
        self.players_in_tournament = set(self.players)
        self.players_not_in_tournament = self.player_dao.get_all_players() - self.players_in_tournament

        self.ui.add_player_button.clicked.connect(self.add_player_to_tournament)
        self.ui.delete_player_button.clicked.connect(self.delete_player_from_tournament)
        self.ui.save_button.clicked.connect(self.save_changes)

    def refresh(self):
        self.players_in_tournament = set(self.players)
        self.players_not_in_tournament = self.player_dao.get_all_players() - self.players_in_tournament
        self.fill_table(self.ui.not_in_tournament_table, self.players_not_in_tournament)
        self.fill_table(self.ui.in_tournament_table, self.players_in_tournament)

    def fill_table(self, table, players):
        table.setRowCount(0)
        current_row = 0
        for player in players:
            table.insertRow(current_row)
            table.setItem(current_row, 0, qtw.QTableWidgetItem(player.name + " " + player.surname))
            table.setItem(current_row, 1, qtw.QTableWidgetItem(str(player.rank)))
            table.setItem(current_row, 2, qtw.QTableWidgetItem(str(player.player_id)))
            current_row += 1

    def add_player_to_tournament(self):
        self.move_player_between_tables(self.ui.not_in_tournament_table, self.ui.in_tournament_table)

    def delete_player_from_tournament(self):
        self.move_player_between_tables(self.ui.in_tournament_table, self.ui.not_in_tournament_table)

    @staticmethod
    def move_player_between_tables(table_from, table_to):
        current_row = table_from.currentRow()
        if current_row != -1:
            player_name = table_from.item(current_row, 0).text()
            player_rank = table_from.item(current_row, 1).text()
            player_id = table_from.item(current_row, 2).text()
            table_from.removeRow(current_row)
            row_to_add = table_to.rowCount()
            table_to.insertRow(row_to_add)
            table_to.setItem(row_to_add, 0, qtw.QTableWidgetItem(player_name))
            table_to.setItem(row_to_add, 1, qtw.QTableWidgetItem(player_rank))
            table_to.setItem(row_to_add, 2, qtw.QTableWidgetItem(player_id))

    def save_changes(self):
        players_to_remove = []
        players_to_add = []

        for i in range(self.ui.not_in_tournament_table.rowCount()):
            player_id = int(self.ui.not_in_tournament_table.item(i, 2).text())
            players_to_remove.append(self.player_dao.get_player_by_id(player_id))

        for i in range(self.ui.in_tournament_table.rowCount()):
            player_id = int(self.ui.in_tournament_table.item(i, 2).text())
            players_to_add.append(self.player_dao.get_player_by_id(player_id))

        for player in players_to_remove:
            self.players_in_tournament.discard(player)

        for player in players_to_add:
            self.players_in_tournament.add(player)

        self.submitted.emit(list(self.players_in_tournament))
        self.return_to_edit_tournament.emit(self.tournament)
