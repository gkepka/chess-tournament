# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'player_ranking_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ListPlayers(object):
    def setupUi(self, ListPlayers):
        ListPlayers.setObjectName("ListPlayers")
        ListPlayers.resize(1024, 768)
        self.label = QtWidgets.QLabel(ListPlayers)
        self.label.setGeometry(QtCore.QRect(0, 10, 1021, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.players_table = QtWidgets.QTableWidget(ListPlayers)
        self.players_table.setGeometry(QtCore.QRect(30, 110, 601, 571))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.players_table.setFont(font)
        self.players_table.setObjectName("players_table")
        self.players_table.setColumnCount(0)
        self.players_table.setRowCount(0)
        self.edit_button = QtWidgets.QPushButton(ListPlayers)
        self.edit_button.setGeometry(QtCore.QRect(720, 150, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.edit_button.setFont(font)
        self.edit_button.setObjectName("edit_button")
        self.delete_button = QtWidgets.QPushButton(ListPlayers)
        self.delete_button.setGeometry(QtCore.QRect(720, 220, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.delete_button.setFont(font)
        self.delete_button.setObjectName("delete_button")
        self.label_2 = QtWidgets.QLabel(ListPlayers)
        self.label_2.setGeometry(QtCore.QRect(720, 290, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.sort_box = QtWidgets.QComboBox(ListPlayers)
        self.sort_box.setGeometry(QtCore.QRect(720, 330, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.sort_box.setFont(font)
        self.sort_box.setObjectName("sort_box")

        self.retranslateUi(ListPlayers)
        QtCore.QMetaObject.connectSlotsByName(ListPlayers)

    def retranslateUi(self, ListPlayers):
        _translate = QtCore.QCoreApplication.translate
        ListPlayers.setWindowTitle(_translate("ListPlayers", "Form"))
        self.label.setText(_translate("ListPlayers", "Player list"))
        self.edit_button.setText(_translate("ListPlayers", "Edit"))
        self.delete_button.setText(_translate("ListPlayers", "Delete"))
        self.label_2.setText(_translate("ListPlayers", "Sort by:"))
