import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from view.add_player_widget import Ui_AddPlayer
from view.create_tournament_widget import Ui_CreateTournament
from view.player_ranking_widget import Ui_RankingView
from view.start_widget import Ui_StartWidget


class AddPlayerWidget(qtw.QWidget, Ui_AddPlayer):
    pass


class CreateTournamentWidget(qtw.QWidget, Ui_CreateTournament):
    pass


class PlayerRankingWidget(qtw.QWidget, Ui_RankingView):
    pass


class StartWidget(qtw.QWidget, Ui_StartWidget):
    pass


class MainWindow(qtw.QMainWindow): # Dziedziczy po QMainWindow

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Your code goes here
        self.resize(1024, 768)
        self.start_widget = StartWidget()
        self.setCentralWidget(self.start_widget)

        menu_bar = self.menuBar()
        tournament_menu = menu_bar.addMenu('Tournament')
        player_menu = menu_bar.addMenu('Player')

        tournament_menu.addAction('Create', self.create_tournament)
        tournament_menu.addAction('List tourmanents', self.list_tournaments)

        player_menu.addAction('Add', self.add_player)
        player_menu.addAction('Ranking', self.player_ranking)

    def create_tournament(self):
        pass

    def list_tournaments(self):
        pass

    def add_player(self):
        pass

    def player_ranking(self):
        pass

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)

    widget = MainWindow()
    widget.show()

    sys.exit(app.exec_())


