# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'player_ranking.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RankingView(object):
    def setupUi(self, RankingView):
        RankingView.setObjectName("RankingView")
        RankingView.resize(1024, 768)
        self.label = QtWidgets.QLabel(RankingView)
        self.label.setGeometry(QtCore.QRect(10, 10, 1001, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.ranking_table = QtWidgets.QTableWidget(RankingView)
        self.ranking_table.setGeometry(QtCore.QRect(25, 90, 691, 661))
        self.ranking_table.setObjectName("ranking_table")
        self.ranking_table.setColumnCount(0)
        self.ranking_table.setRowCount(0)
        self.label_2 = QtWidgets.QLabel(RankingView)
        self.label_2.setGeometry(QtCore.QRect(740, 100, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.select_sort = QtWidgets.QComboBox(RankingView)
        self.select_sort.setGeometry(QtCore.QRect(740, 140, 87, 32))
        self.select_sort.setObjectName("select_sort")

        self.retranslateUi(RankingView)
        QtCore.QMetaObject.connectSlotsByName(RankingView)

    def retranslateUi(self, RankingView):
        _translate = QtCore.QCoreApplication.translate
        RankingView.setWindowTitle(_translate("RankingView", "Form"))
        self.label.setText(_translate("RankingView", "Player ranking"))
        self.label_2.setText(_translate("RankingView", "Sort by:"))
