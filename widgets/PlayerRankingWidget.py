from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from generated.player_ranking_widget import Ui_ListPlayers
from dao.DataAccessObjects import PlayerDAO, TournamentDAO


class PlayerRankingWidget(qtw.QWidget):

    player_to_delete = qtc.pyqtSignal(object)
    player_to_edit = qtc.pyqtSignal(object)

    def __init__(self, parent=None):
        super(PlayerRankingWidget, self).__init__(parent)
        self.ui = Ui_ListPlayers()
        self.ui.setupUi(self)
        self.player_dao = PlayerDAO()
        self.sort_type = "name"

        self.ui.players_table.setColumnCount(4)
        self.ui.players_table.setHorizontalHeaderLabels(('Name', 'Ranking', 'Country', 'ID'))
        self.ui.players_table.setColumnWidth(0, 240)
        self.ui.players_table.setColumnWidth(1, 90)
        self.ui.players_table.setColumnWidth(2, 150)
        self.ui.players_table.setColumnWidth(3, 100)
        self.ui.players_table.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)

        self.ui.edit_button.clicked.connect(self.edit_player)
        self.ui.delete_button.clicked.connect(self.delete_player)

        self.ui.sort_box.addItem("Name")
        self.ui.sort_box.addItem("Rank")
        self.ui.sort_box.addItem("ID")

        self.ui.sort_box.activated[str].connect(self.change_sort_type)

        self.refresh()

    def change_sort_type(self, text):
        self.sort_type = text
        self.refresh()

    def refresh(self):
        players = self.player_dao.get_all_players()
        if self.sort_type == "Name":
            players = sorted(players, key=lambda p: p.name + " " + p.surname)
        if self.sort_type == "Rank":
            players = sorted(players, key=lambda p: p.rank, reverse=True)
        if self.sort_type == "ID":
            players = sorted(players, key=lambda p: p.player_id)
        self.ui.players_table.setRowCount(0)
        current_row = 0
        for player in players:
            self.ui.players_table.insertRow(current_row)
            self.ui.players_table.setItem(current_row, 0, qtw.QTableWidgetItem(player.name + " " + player.surname))
            self.ui.players_table.setItem(current_row, 1, qtw.QTableWidgetItem(str(player.rank)))
            self.ui.players_table.setItem(current_row, 2, qtw.QTableWidgetItem(player.nationality))
            self.ui.players_table.setItem(current_row, 3, qtw.QTableWidgetItem(str(player.player_id)))
            current_row += 1

    def edit_player(self):
        current_row = self.ui.players_table.currentRow()
        player_id = int(self.ui.players_table.item(current_row, 3).text())
        player = self.player_dao.get_player_by_id(player_id)
        self.player_to_edit.emit(player)
        self.refresh()

    def delete_player(self):
        current_row = self.ui.players_table.currentRow()
        player_id = int(self.ui.players_table.item(current_row, 3).text())
        player = self.player_dao.get_player_by_id(player_id)
        tournament_dao = TournamentDAO()
        if len(tournament_dao.get_tournaments_for_player(player)) != 0:
            qtw.QMessageBox.critical(self, 'Error', 'Can\'t delete player which participates in tournament')
        else:
            self.player_to_delete.emit(player)
