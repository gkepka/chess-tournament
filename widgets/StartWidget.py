from PyQt5 import QtWidgets as qtw
from generated.start_widget import Ui_StartWidget


class StartWidget(qtw.QWidget):

    def __init__(self, parent=None):
        super(StartWidget, self).__init__(parent)
        self.ui = Ui_StartWidget()
        self.ui.setupUi(self)
