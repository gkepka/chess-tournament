from PyQt5 import QtWidgets as qtw

from generated.player_ranking_widget import Ui_RankingView


class PlayerRankingWidget(qtw.QWidget):

    def __init__(self, parent=None):
        super(PlayerRankingWidget, self).__init__(parent)
        self.ui = Ui_RankingView()
        self.ui.setupUi(self)
