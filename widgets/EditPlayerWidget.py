from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from generated.edit_player_widget import Ui_EditPlayer
from dao.DataAccessObjects import TournamentDAO, PlayerDAO


class EditPlayerWidget(qtw.QWidget):

    view_tournament = qtc.pyqtSignal(int)

    def __init__(self, player, parent=None):
        super(EditPlayerWidget, self).__init__(parent)

        self.player = player
        self.player_dao = PlayerDAO()

        self.ui = Ui_EditPlayer()
        self.ui.setupUi(self)

        self.ui.tournaments_table.setColumnCount(4)
        self.ui.tournaments_table.setHorizontalHeaderLabels(('Name', 'Rounds', 'Date', 'ID'))
        self.ui.tournaments_table.setColumnWidth(0, 240)
        self.ui.tournaments_table.setColumnWidth(1, 90)
        self.ui.tournaments_table.setColumnWidth(2, 150)
        self.ui.tournaments_table.setColumnWidth(3, 100)
        self.ui.tournaments_table.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)

        self.tournament_dao = TournamentDAO()
        tournaments = self.tournament_dao.get_tournaments_for_player(player)
        self.fill_tournaments_table(tournaments)

        self.ui.sort_box.addItem("Name")
        self.ui.sort_box.addItem("Date")
        self.ui.sort_box.activated[str].connect(self.sort_table)

        self.ui.firstname_edit.setText(player.name)
        self.ui.last_name_edit.setText(player.surname)
        self.ui.ranking_edit.setText(str(player.rank))
        self.ui.nationality_edit.setText(player.nationality)
        self.ui.title_edit.setText(player.title)
        self.ui.chessclub_edit.setText(player.chess_club)

        self.ui.save_button.clicked.connect(self.save_player)
        self.ui.tournament_button.clicked.connect(self.go_to_tournament)

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

    def save_player(self):
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
            self.player.name = first_name
            self.player.surname = last_name
            self.player.rank = ranking
            self.player.nationality = nationality
            self.player.title = title
            self.player.chess_club = chess_club
            self.player_dao.update_player(self.player)

    def go_to_tournament(self):
        current_row = self.ui.tournaments_table.currentRow()
        tournament_id = int(self.ui.tournaments_table.item(current_row, 3).text())
        self.view_tournament.emit(tournament_id)