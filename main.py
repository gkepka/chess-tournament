import sys
from datetime import date
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from view.add_player_widget import Ui_AddPlayer
from view.create_tournament_widget import Ui_CreateTournament
from view.player_ranking_widget import Ui_RankingView
from view.start_widget import Ui_StartWidget
from view.list_tournaments_widget import Ui_ListTournaments
from view.edit_tournament_widget import Ui_EditTournament
from view.edit_players_widget import Ui_EditPlayers

from dao.DataAccessObjects import PlayerDAO, TournamentDAO, PlayerParamsDAO, RoundDAO
from dao.DatabaseInitializer import DatabaseInitializer

from model.Player import Player
from model.Tournament import Tournament



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


class EditPlayersWidget(qtw.QWidget):

    submitted = qtc.pyqtSignal(list) # new list of players
    return_to_edit_tournament = qtc.pyqtSignal(object)

    def __init__(self, tournament, players, parent=None):
        super(EditPlayersWidget, self).__init__(parent)
        self.ui = Ui_EditPlayers()
        self.ui.setupUi(self)

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
        if len(players) != 0:
            self.players_in_tournament = set(players)
        else:
            self.players_in_tournament = self.player_dao.get_players_for_tournament(tournament.tournament_id)
        self.players_not_in_tournament = self.player_dao.get_all_players() - self.players_in_tournament

        self.fill_table(self.ui.not_in_tournament_table, self.players_not_in_tournament)
        self.fill_table(self.ui.in_tournament_table, self.players_in_tournament)

        self.ui.add_player_button.clicked.connect(self.add_player_to_tournament)
        self.ui.delete_player_button.clicked.connect(self.delete_player_from_tournament)
        self.ui.save_button.clicked.connect(self.save_changes)

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
            players_to_remove.append(self.player_dao.get_player_by_id(player_id))

        for player in players_to_remove:
            self.players_in_tournament.discard(player)

        for player in players_to_add:
            self.players_in_tournament.add(player)

        self.submitted.emit(list(self.players_in_tournament))
        self.return_to_edit_tournament.emit(self.tournament)


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
        self.tournament_edit_widgets = {}
        self.tournament_player_widgets = {}
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

    def show_tournament_edit_widget(self, tournament):
        if tournament not in self.tournament_edit_widgets:
            self.tournament_edit_widgets[tournament] = EditTournamentWidget(tournament, self)
            self.tournament_edit_widgets[tournament].tournament_to_save.connect(self.save_edited_tournament)
            self.tournament_edit_widgets[tournament].round_to_edit.connect(self.edit_round)
            self.tournament_edit_widgets[tournament].edit_players_signal.connect(self.edit_players)
        if self.central_widget.indexOf(self.tournament_edit_widgets[tournament]) == -1:
            self.central_widget.addWidget(self.tournament_edit_widgets[tournament])
        self.central_widget.setCurrentWidget(self.tournament_edit_widgets[tournament])

    def show_tournament_players_widget(self, tournament, players):
        if tournament not in self.tournament_player_widgets:
            self.tournament_player_widgets[tournament] = EditPlayersWidget(tournament, players, self)
            self.tournament_player_widgets[tournament].submitted.connect(self.tournament_edit_widgets[tournament].update_player_list)
            self.tournament_player_widgets[tournament].return_to_edit_tournament.connect(self.show_tournament_edit_widget)
        if self.central_widget.indexOf(self.tournament_player_widgets[tournament]) == -1:
            self.central_widget.addWidget(self.tournament_player_widgets[tournament])
        self.central_widget.setCurrentWidget(self.tournament_player_widgets[tournament])

    @qtc.pyqtSlot(str, str, int, str, str, str)
    def save_player(self, first_name, last_name,
                    ranking, nationality, title, chess_club):
        player = Player(first_name, last_name,
                        ranking, nationality, title, chess_club)
        player_dao = PlayerDAO()
        player_id = player_dao.insert_player(player)
        player.player_id = player_id

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
        tournament_dao = TournamentDAO()
        tournament = tournament_dao.get_tournament_by_id(tournament_id)
        self.show_tournament_edit_widget(tournament)

    @qtc.pyqtSlot(object, list)
    def edit_players(self, tournament, players):
        self.show_tournament_players_widget(tournament, players)


    @qtc.pyqtSlot(object, list, list)
    def save_edited_tournament(self, tournament_to_save, player_list, generated_rounds):
        pass

    @qtc.pyqtSlot(int)
    def edit_round(self, round_id):
        pass


if __name__ == '__main__':
    database_initializer = DatabaseInitializer()
    database_initializer.create_tables()

    app = qtw.QApplication(sys.argv)

    widget = MainWindow()
    widget.show()

    sys.exit(app.exec_())
