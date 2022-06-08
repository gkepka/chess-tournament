# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tournament_ranking_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PlayerRanking(object):
    def setupUi(self, PlayerRanking):
        PlayerRanking.setObjectName("PlayerRanking")
        PlayerRanking.resize(1024, 768)
        self.label = QtWidgets.QLabel(PlayerRanking)
        self.label.setGeometry(QtCore.QRect(0, 10, 1021, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.players_table = QtWidgets.QTableWidget(PlayerRanking)
        self.players_table.setGeometry(QtCore.QRect(30, 180, 601, 501))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.players_table.setFont(font)
        self.players_table.setObjectName("players_table")
        self.players_table.setColumnCount(0)
        self.players_table.setRowCount(0)
        self.label_2 = QtWidgets.QLabel(PlayerRanking)
        self.label_2.setGeometry(QtCore.QRect(710, 190, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.sort_box = QtWidgets.QComboBox(PlayerRanking)
        self.sort_box.setGeometry(QtCore.QRect(710, 230, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.sort_box.setFont(font)
        self.sort_box.setObjectName("sort_box")
        self.tournament_date_label_2 = QtWidgets.QLabel(PlayerRanking)
        self.tournament_date_label_2.setGeometry(QtCore.QRect(150, 120, 53, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.tournament_date_label_2.setFont(font)
        self.tournament_date_label_2.setObjectName("tournament_date_label_2")
        self.tournament_name_label_2 = QtWidgets.QLabel(PlayerRanking)
        self.tournament_name_label_2.setGeometry(QtCore.QRect(14, 82, 189, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.tournament_name_label_2.setFont(font)
        self.tournament_name_label_2.setObjectName("tournament_name_label_2")
        self.name_label = QtWidgets.QLabel(PlayerRanking)
        self.name_label.setGeometry(QtCore.QRect(220, 80, 191, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.name_label.setFont(font)
        self.name_label.setObjectName("name_label")
        self.date_label = QtWidgets.QLabel(PlayerRanking)
        self.date_label.setGeometry(QtCore.QRect(220, 120, 191, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.date_label.setFont(font)
        self.date_label.setObjectName("date_label")

        self.retranslateUi(PlayerRanking)
        QtCore.QMetaObject.connectSlotsByName(PlayerRanking)

    def retranslateUi(self, PlayerRanking):
        _translate = QtCore.QCoreApplication.translate
        PlayerRanking.setWindowTitle(_translate("PlayerRanking", "Form"))
        self.label.setText(_translate("PlayerRanking", "Ranking"))
        self.label_2.setText(_translate("PlayerRanking", "Sort by:"))
        self.tournament_date_label_2.setText(_translate("PlayerRanking", "Date:"))
        self.tournament_name_label_2.setText(_translate("PlayerRanking", "Tournament name:"))
        self.name_label.setText(_translate("PlayerRanking", "Tournament name:"))
        self.date_label.setText(_translate("PlayerRanking", "Date:"))
