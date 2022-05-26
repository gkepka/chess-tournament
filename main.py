import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from widgets.StartWidget import StartWidget
from widgets.PlayerRankingWidget import PlayerRankingWidget
from widgets.EditTournamentWidget import EditTournamentWidget
from widgets.EditPlayersWidget import EditPlayersWidget
from widgets.ListTournamentsWidget import ListTournamentsWidget
from widgets.CreateTournamentWidget import CreateTournamentWidget
from widgets.AddPlayerWidget import AddPlayerWidget
from widgets.EditPlayerWidget import EditPlayerWidget
from widgets.RoundWidget import RoundWidget

from dao.DataAccessObjects import PlayerDAO, TournamentDAO, PlayerParamsDAO, RoundDAO
from dao.DatabaseInitializer import DatabaseInitializer

from model.Player import Player
from model.Tournament import Tournament


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
        self.player_edit_widgets = {}
        self.round_edit_widgets = {}
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
        current_menu = menu_bar.addMenu('Current')

        file_menu.addAction('Quit', self.close)

        tournament_menu.addAction('Create', self.show_create_tournament_widget)
        tournament_menu.addAction('List tournaments', self.show_tournament_list_widget)

        player_menu.addAction('Add', self.show_add_player_widget)
        player_menu.addAction('Ranking', self.show_player_ranking_widget)

        current_menu.addAction('View', self.edit_current_tournament)

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
            self.player_ranking_widget.player_to_edit.connect(self.edit_player)
            self.player_ranking_widget.player_to_delete.connect(self.delete_player)
        if self.central_widget.indexOf(self.player_ranking_widget) == -1:
            self.central_widget.addWidget(self.player_ranking_widget)
        self.player_ranking_widget.refresh()
        self.central_widget.setCurrentWidget(self.player_ranking_widget)

    def show_tournament_edit_widget(self, tournament):
        if tournament not in self.tournament_edit_widgets:
            self.tournament_edit_widgets[tournament] = EditTournamentWidget(tournament, self)
            self.tournament_edit_widgets[tournament].round_to_edit.connect(self.edit_round)
            self.tournament_edit_widgets[tournament].round_to_delete.connect(self.delete_round)
            self.tournament_edit_widgets[tournament].edit_players_signal.connect(self.edit_players)
        if self.central_widget.indexOf(self.tournament_edit_widgets[tournament]) == -1:
            self.central_widget.addWidget(self.tournament_edit_widgets[tournament])
        self.central_widget.setCurrentWidget(self.tournament_edit_widgets[tournament])

    def show_tournament_players_widget(self, tournament):
        if tournament not in self.tournament_player_widgets:
            self.tournament_player_widgets[tournament] = EditPlayersWidget(tournament, self)
            self.tournament_player_widgets[tournament].submitted.connect(self.tournament_edit_widgets[tournament].update_player_list)
            self.tournament_player_widgets[tournament].return_to_edit_tournament.connect(self.show_tournament_edit_widget)
        if self.central_widget.indexOf(self.tournament_player_widgets[tournament]) == -1:
            self.central_widget.addWidget(self.tournament_player_widgets[tournament])
        self.tournament_player_widgets[tournament].refresh()
        self.central_widget.setCurrentWidget(self.tournament_player_widgets[tournament])

    def show_player_edit_widget(self, player):
        if player not in self.player_edit_widgets:
            player_edit_widget = EditPlayerWidget(player, self)
            self.player_edit_widgets[player] = player_edit_widget
            player_edit_widget.view_tournament.connect(self.edit_tournament)
        if self.central_widget.indexOf(self.player_edit_widgets[player]) == -1:
            self.central_widget.addWidget(self.player_edit_widgets[player])
        self.central_widget.setCurrentWidget(self.player_edit_widgets[player])

    def show_round_widget(self, round):
        if round not in self.round_edit_widgets:
            round_widget = RoundWidget(round, self)
            self.round_edit_widgets[round] = round_widget
        if self.central_widget.indexOf(self.round_edit_widgets[round]) == -1:
            self.central_widget.addWidget(self.round_edit_widgets[round])
        self.central_widget.setCurrentWidget(self.round_edit_widgets[round])

    def edit_current_tournament(self):
        if self.current_tournament is None:
            pass
        else:
            self.show_tournament_edit_widget(self.current_tournament)

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

    @qtc.pyqtSlot(object)
    def edit_players(self, tournament):
        self.show_tournament_players_widget(tournament)

    @qtc.pyqtSlot(int)
    def edit_round(self, round_id):
        round_dao = RoundDAO()
        round = round_dao.get_round_by_id(round_id)
        self.show_round_widget(round)

    @qtc.pyqtSlot(int)
    def delete_round(self, round_id):
        pass

    @qtc.pyqtSlot(object)
    def edit_player(self, player):
        self.show_player_edit_widget(player)

    @qtc.pyqtSlot(object)
    def delete_player(self, player):
        player_dao = PlayerDAO()
        player_dao.delete_player(player)
        self.player_ranking_widget.refresh()


if __name__ == '__main__':
    database_initializer = DatabaseInitializer()
    database_initializer.create_tables()

    app = qtw.QApplication(sys.argv)

    widget = MainWindow()
    widget.show()

    sys.exit(app.exec_())
