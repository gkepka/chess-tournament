from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from generated.tournament_ranking_widget import Ui_PlayerRanking


class PlayerRankingWidget(qtw.QWidget):

    def __init__(self, tournament, parent=None):
        super(PlayerRankingWidget, self).__init__(parent)
        self.ui = Ui_PlayerRanking()
        self.ui.setupUi(self)
        self.tournament = tournament
        self.player_params = tournament.params_list
        self.sort_type = "name"

        self.ui.players_table.setColumnCount(4)
        self.ui.players_table.setHorizontalHeaderLabels(('Name', 'Points', 'Country', 'ID'))
        self.ui.players_table.setColumnWidth(0, 240)
        self.ui.players_table.setColumnWidth(1, 90)
        self.ui.players_table.setColumnWidth(2, 150)
        self.ui.players_table.setColumnWidth(3, 100)
        self.ui.players_table.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)

        self.ui.sort_box.addItem("Name")
        self.ui.sort_box.addItem("Points")
        self.ui.sort_box.addItem("ID")

        self.ui.sort_box.activated[str].connect(self.change_sort_type)

        self.refresh()

    def change_sort_type(self, text):
        self.sort_type = text
        self.refresh()

    def refresh(self):
        self.tournament.set_points()
        players = self.player_params[:]
        if self.sort_type == "Name":
            players = sorted(players, key=lambda p: p.player.name + " " + p.player.surname)
        if self.sort_type == "Points":
            players = sorted(players, key=lambda p: p.get_points(), reverse=True)
        if self.sort_type == "ID":
            players = sorted(players, key=lambda p: p.player.player_id)
        self.ui.players_table.setRowCount(0)
        current_row = 0
        for param in players:
            self.ui.players_table.insertRow(current_row)
            self.ui.players_table.setItem(current_row, 0, qtw.QTableWidgetItem(param.player.name + " " + param.player.surname))
            self.ui.players_table.setItem(current_row, 1, qtw.QTableWidgetItem(str(param.get_points())))
            self.ui.players_table.setItem(current_row, 2, qtw.QTableWidgetItem(param.player.nationality))
            self.ui.players_table.setItem(current_row, 3, qtw.QTableWidgetItem(str(param.player.player_id)))
            current_row += 1

