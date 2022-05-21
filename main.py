import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from view.add_player_widget import Ui_AddPlayer
from view.create_tournament_widget import Ui_CreateTournament
from view.player_ranking_widget import Ui_RankingView
from view.start_widget import Ui_StartWidget
from view.list_tournaments_widget import Ui_ListTournaments
from dao.DataAccessObjects import PlayerDAO, TournamentDAO, PlayerParamsDAO
from dao.DatabaseInitializer import DatabaseInitializer
from model.Player import Player
from model.Tournament import Tournament
from datetime import date


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
            print(player.rank)
            print(player.player_id)
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


class DeleteTournamentDialog(qtw.QDialog):
    def __init__(self):
        super().__init__()

        buttons = qtw.QDialogButtonBox.Ok | qtw.QDialogButtonBox.Cancel
        self.buttonBox = qtw.QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = qtw.QVBoxLayout()
        message = qtw.QLabel("Delete tournament?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


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

class PlayerRankingWidget(qtw.QWidget):

    def __init__(self, parent=None):
        super(PlayerRankingWidget, self).__init__(parent)
        self.ui = Ui_RankingView()
        self.ui.setupUi(self)


class StartWidget(qtw.QWidget):

    def __init__(self, parent=None):
        super(StartWidget, self).__init__(parent)
        self.ui = Ui_StartWidget()
        self.ui.setupUi(self)


class MainWindow(qtw.QMainWindow):  # Dziedziczy po QMainWindow

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Your code goes here
        self.current_tournament = None

        self.add_player_widget = None
        self.create_tournament_widget = None
        self.player_ranking_widget = None
        self.list_tournaments_widget = None
        self.resize(1024, 768)

        self.central_widget = qtw.QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.start_widget = StartWidget(self)
        self.central_widget.addWidget(self.start_widget)
        self.central_widget.setCurrentWidget(self.start_widget)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        tournament_menu = menu_bar.addMenu('Tournament')
        player_menu = menu_bar.addMenu('Player')

        file_menu.addAction('Quit', self.close)

        tournament_menu.addAction('Create', self.show_create_tournament_widget)
        tournament_menu.addAction('List tournaments', self.show_tournament_list_widget)

        player_menu.addAction('Add', self.show_add_player_widget)
        player_menu.addAction('Ranking', self.show_player_ranking_widget)

    def show_create_tournament_widget(self):
        if self.create_tournament_widget is None:
            self.create_tournament_widget = CreateTournamentWidget(self)
            self.create_tournament_widget.tournament_added.connect(self.save_tournament)
        if self.central_widget.indexOf(self.create_tournament_widget) == -1:
            self.central_widget.addWidget(self.create_tournament_widget)
        self.central_widget.setCurrentWidget(self.create_tournament_widget)

    def show_tournament_list_widget(self):
        if self.list_tournaments_widget is None:
            self.list_tournaments_widget = ListTournamentsWidget(self)
            self.list_tournaments_widget.tournament_chosen.connect(self.set_current_tournament)
            self.list_tournaments_widget.tournament_to_delete.connect(self.delete_tournament)
            self.list_tournaments_widget.tournament_to_edit.connect(self.edit_tournament)
        if self.central_widget.indexOf(self.list_tournaments_widget) == -1:
            self.central_widget.addWidget(self.list_tournaments_widget)
        self.central_widget.setCurrentWidget(self.list_tournaments_widget)

    def show_add_player_widget(self):
        if self.add_player_widget is None:
            self.add_player_widget = AddPlayerWidget(self)
            self.add_player_widget.player_added.connect(self.save_player)
        if self.central_widget.indexOf(self.add_player_widget) == -1:
            self.central_widget.addWidget(self.add_player_widget)
        self.central_widget.setCurrentWidget(self.add_player_widget)

    def show_player_ranking_widget(self):
        if self.player_ranking_widget is None:
            self.player_ranking_widget = PlayerRankingWidget(self)
        if self.central_widget.indexOf(self.player_ranking_widget) == -1:
            self.central_widget.addWidget(self.player_ranking_widget)
        self.central_widget.setCurrentWidget(self.player_ranking_widget)

    @qtc.pyqtSlot(str, str, int, str, str, str)
    def save_player(self, first_name, last_name,
                    ranking, nationality, title, chess_club):
        player = Player(first_name, last_name,
                        ranking, nationality, title, chess_club)
        player_dao = PlayerDAO()
        player_dao.insert_player(player)

    @qtc.pyqtSlot(str, str, int, list)
    def save_tournament(self, tournament_name, tournament_date, tournament_rounds, added_players):
        tournament = Tournament(tournament_name, tournament_date, tournament_rounds)
        tournament_dao = TournamentDAO()
        tournament_id = tournament_dao.insert_tournament(tournament)
        tournament.tournament_id = tournament_id
        for player in added_players:
            tournament.add_player_params_from_player(player)
        player_params_dao = PlayerParamsDAO()
        player_params_dao.insert_player_params_list(tournament.params_list)

    @qtc.pyqtSlot(int)
    def set_current_tournament(self, tournament_id):
        tournament_dao = TournamentDAO()
        self.current_tournament = tournament_dao.get_tournament_by_id(tournament_id)
        self.statusBar().showMessage(f'Current tournament: {self.current_tournament.name}')

    @qtc.pyqtSlot(int)
    def delete_tournament(self, tournament_id):
        tournament_dao = TournamentDAO()
        tournament_dao.delete_tournament_by_id(tournament_id)

    @qtc.pyqtSlot(int)
    def edit_tournament(self, tournament_id):
        pass


if __name__ == '__main__':
    database_initializer = DatabaseInitializer()
    database_initializer.create_tables()

    app = qtw.QApplication(sys.argv)

    widget = MainWindow()
    widget.show()

    sys.exit(app.exec_())
