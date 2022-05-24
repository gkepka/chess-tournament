from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from datetime import date

from generated.create_tournament_widget import Ui_CreateTournament
from dao.DataAccessObjects import PlayerDAO


class CreateTournamentWidget(qtw.QWidget):
    tournament_added = qtc.pyqtSignal(str, str, int, list)

    def __init__(self, parent=None):
        super(CreateTournamentWidget, self).__init__(parent)
        self.ui = Ui_CreateTournament()
        self.ui.setupUi(self)

        self.ui.add_player_table.setColumnCount(3)
        self.ui.add_player_table.setHorizontalHeaderLabels(('Name', 'Ranking', 'ID'))
        self.ui.add_player_table.setColumnWidth(0, 160)
        self.ui.add_player_table.setColumnWidth(1, 90)
        self.ui.add_player_table.setColumnWidth(2, 70)
        self.ui.add_player_table.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
        self.ui.delete_player_table.setColumnCount(3)
        self.ui.delete_player_table.setHorizontalHeaderLabels(('Name', 'Ranking', 'ID'))
        self.ui.delete_player_table.setColumnWidth(0, 160)
        self.ui.delete_player_table.setColumnWidth(1, 90)
        self.ui.delete_player_table.setColumnWidth(2, 70)
        self.ui.delete_player_table.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)

        self.player_dao = PlayerDAO()
        self.fill_add_player_table(self.player_dao.get_all_players())

        self.ui.create_tournament_button.clicked.connect(self.add_tournament)
        self.ui.add_player_button.clicked.connect(self.add_player_to_tournament)
        self.ui.delete_player_button.clicked.connect(self.delete_player_from_tournament)

    def fill_add_player_table(self, players):
        self.ui.add_player_table.setRowCount(0)
        current_row = 0
        for player in players:
            self.ui.add_player_table.insertRow(current_row)
            self.ui.add_player_table.setItem(current_row, 0, qtw.QTableWidgetItem(player.name + " " + player.surname))
            self.ui.add_player_table.setItem(current_row, 1, qtw.QTableWidgetItem(str(player.rank)))
            self.ui.add_player_table.setItem(current_row, 2, qtw.QTableWidgetItem(str(player.player_id)))
            current_row += 1

    def add_tournament(self):
        try:
            tournament_name = self.ui.tournament_name_edit.text()
            tournament_date = date.fromisoformat(self.ui.tournament_date_edit.text())
            tournament_rounds = int(self.ui.tournament_rounds_edit.text())
            added_players = []
            for i in range(self.ui.delete_player_table.rowCount()):
                player_id = int(self.ui.delete_player_table.item(i, 2).text())
                added_players.append(self.player_dao.get_player_by_id(player_id))
        except ValueError as e:
            if str(e).count("invalid literal for int()") != 0:
                qtw.QMessageBox.critical(self, 'Error', 'Round count must be a number')
                self.ui.tournament_rounds_edit.clear()
            if str(e).count("Invalid isoformat string") != 0:
                qtw.QMessageBox.critical(self, 'Error', 'Date must be in format YYYY-MM-DD')
                self.ui.tournament_date_edit.clear()
        else:
            self.tournament_added.emit(tournament_name, str(tournament_date), tournament_rounds, added_players)
            self.clear_edits()
            self.ui.delete_player_table.setRowCount(0)
            self.fill_add_player_table(self.player_dao.get_all_players())


    def add_player_to_tournament(self):
        self.move_player_between_tables(self.ui.add_player_table, self.ui.delete_player_table)

    def delete_player_from_tournament(self):
        self.move_player_between_tables(self.ui.delete_player_table, self.ui.add_player_table)

    def clear_edits(self):
        self.ui.tournament_name_edit.clear()
        self.ui.tournament_date_edit.clear()
        self.ui.tournament_rounds_edit.clear()

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
