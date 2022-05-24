# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edit_players_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditPlayers(object):
    def setupUi(self, EditPlayers):
        EditPlayers.setObjectName("EditPlayers")
        EditPlayers.resize(1024, 768)
        font = QtGui.QFont()
        font.setPointSize(14)
        EditPlayers.setFont(font)
        self.create_tournament_title = QtWidgets.QLabel(EditPlayers)
        self.create_tournament_title.setGeometry(QtCore.QRect(6, 6, 1011, 45))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.create_tournament_title.setFont(font)
        self.create_tournament_title.setAlignment(QtCore.Qt.AlignCenter)
        self.create_tournament_title.setObjectName("create_tournament_title")
        self.add_player_button = QtWidgets.QPushButton(EditPlayers)
        self.add_player_button.setGeometry(QtCore.QRect(90, 550, 341, 41))
        self.add_player_button.setObjectName("add_player_button")
        self.label_2 = QtWidgets.QLabel(EditPlayers)
        self.label_2.setGeometry(QtCore.QRect(690, 70, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.delete_player_button = QtWidgets.QPushButton(EditPlayers)
        self.delete_player_button.setGeometry(QtCore.QRect(560, 550, 341, 41))
        self.delete_player_button.setObjectName("delete_player_button")
        self.save_button = QtWidgets.QPushButton(EditPlayers)
        self.save_button.setGeometry(QtCore.QRect(560, 640, 341, 51))
        self.save_button.setObjectName("save_button")
        self.label = QtWidgets.QLabel(EditPlayers)
        self.label.setGeometry(QtCore.QRect(180, 70, 156, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.not_in_tournament_table = QtWidgets.QTableWidget(EditPlayers)
        self.not_in_tournament_table.setGeometry(QtCore.QRect(90, 110, 341, 441))
        self.not_in_tournament_table.setObjectName("not_in_tournament_table")
        self.not_in_tournament_table.setColumnCount(0)
        self.not_in_tournament_table.setRowCount(0)
        self.in_tournament_table = QtWidgets.QTableWidget(EditPlayers)
        self.in_tournament_table.setGeometry(QtCore.QRect(560, 110, 341, 441))
        self.in_tournament_table.setObjectName("in_tournament_table")
        self.in_tournament_table.setColumnCount(0)
        self.in_tournament_table.setRowCount(0)

        self.retranslateUi(EditPlayers)
        QtCore.QMetaObject.connectSlotsByName(EditPlayers)

    def retranslateUi(self, EditPlayers):
        _translate = QtCore.QCoreApplication.translate
        EditPlayers.setWindowTitle(_translate("EditPlayers", "Form"))
        self.create_tournament_title.setText(_translate("EditPlayers", "Edit tournament players"))
        self.add_player_button.setText(_translate("EditPlayers", "Add player"))
        self.label_2.setText(_translate("EditPlayers", "Players: "))
        self.delete_player_button.setText(_translate("EditPlayers", "Remove player"))
        self.save_button.setText(_translate("EditPlayers", "Save changes"))
        self.label.setText(_translate("EditPlayers", "Choose players:"))
