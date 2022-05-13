import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from view.add_player_widget import Ui_AddPlayer
from view.create_tournament_widget import Ui_CreateTournament
from view.player_ranking_widget import Ui_RankingView
from view.start_widget import Ui_StartWidget


class AddPlayerWidget(qtw.QWidget):

    def __init__(self, parent=None):
        super(AddPlayerWidget, self).__init__(parent)
        self.ui = Ui_AddPlayer()
        self.ui.setupUi(self)


class CreateTournamentWidget(qtw.QWidget):

    def __init__(self, parent=None):
        super(CreateTournamentWidget, self).__init__(parent)
        self.ui = Ui_CreateTournament()
        self.ui.setupUi(self)


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


class MainWindow(qtw.QMainWindow): # Dziedziczy po QMainWindow

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Your code goes here
        self.resize(1024, 768)
        self.central_widget = qtw.QStackedWidget()
        self.setCentralWidget(self.central_widget)
        start_widget = StartWidget()
        self.central_widget.addWidget(start_widget)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        tournament_menu = menu_bar.addMenu('Tournament')
        player_menu = menu_bar.addMenu('Player')

        file_menu.addAction('Quit', self.close)

        tournament_menu.addAction('Create', self.create_tournament)
        tournament_menu.addAction('List tourmanents', self.list_tournaments)

        player_menu.addAction('Add', self.add_player)
        player_menu.addAction('Ranking', self.player_ranking)

    def create_tournament(self):
        create_tournament_widget = CreateTournamentWidget(self)
        if self.central_widget.indexOf(create_tournament_widget) == -1:
            self.central_widget.addWidget(create_tournament_widget)
        self.central_widget.setCurrentWidget(create_tournament_widget)

    def list_tournaments(self):
        pass

    def add_player(self):
        add_player_widget = AddPlayerWidget(self)
        if self.central_widget.indexOf(add_player_widget) == -1:
            self.central_widget.addWidget(add_player_widget)
        self.central_widget.setCurrentWidget(add_player_widget)

    def player_ranking(self):
        player_ranking_widget = PlayerRankingWidget(self)
        if self.central_widget.indexOf(player_ranking_widget) == -1:
            self.central_widget.addWidget(player_ranking_widget)
        self.central_widget.setCurrentWidget(player_ranking_widget)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)

    widget = MainWindow()
    widget.show()

    sys.exit(app.exec_())


