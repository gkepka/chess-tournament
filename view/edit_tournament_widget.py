# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edit_tournament_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditTournament(object):
    def setupUi(self, EditTournament):
        EditTournament.setObjectName("EditTournament")
        EditTournament.resize(1024, 768)
        font = QtGui.QFont()
        font.setPointSize(14)
        EditTournament.setFont(font)
        self.create_tournament_title = QtWidgets.QLabel(EditTournament)
        self.create_tournament_title.setGeometry(QtCore.QRect(6, 6, 1011, 45))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.create_tournament_title.setFont(font)
        self.create_tournament_title.setAlignment(QtCore.Qt.AlignCenter)
        self.create_tournament_title.setObjectName("create_tournament_title")
        self.tournament_name_label = QtWidgets.QLabel(EditTournament)
        self.tournament_name_label.setGeometry(QtCore.QRect(25, 94, 189, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.tournament_name_label.setFont(font)
        self.tournament_name_label.setObjectName("tournament_name_label")
        self.tournament_name_edit = QtWidgets.QLineEdit(EditTournament)
        self.tournament_name_edit.setGeometry(QtCore.QRect(220, 94, 231, 32))
        self.tournament_name_edit.setObjectName("tournament_name_edit")
        self.tournament_date_label = QtWidgets.QLabel(EditTournament)
        self.tournament_date_label.setGeometry(QtCore.QRect(161, 132, 53, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.tournament_date_label.setFont(font)
        self.tournament_date_label.setObjectName("tournament_date_label")
        self.tournament_date_edit = QtWidgets.QLineEdit(EditTournament)
        self.tournament_date_edit.setGeometry(QtCore.QRect(220, 132, 231, 32))
        self.tournament_date_edit.setObjectName("tournament_date_edit")
        self.tournament_rounds_label = QtWidgets.QLabel(EditTournament)
        self.tournament_rounds_label.setGeometry(QtCore.QRect(133, 170, 81, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.tournament_rounds_label.setFont(font)
        self.tournament_rounds_label.setObjectName("tournament_rounds_label")
        self.tournament_rounds_edit = QtWidgets.QLineEdit(EditTournament)
        self.tournament_rounds_edit.setGeometry(QtCore.QRect(220, 170, 231, 32))
        self.tournament_rounds_edit.setObjectName("tournament_rounds_edit")
        self.generate_button = QtWidgets.QPushButton(EditTournament)
        self.generate_button.setGeometry(QtCore.QRect(100, 660, 401, 41))
        self.generate_button.setObjectName("generate_button")
        self.edit_tournament_button = QtWidgets.QPushButton(EditTournament)
        self.edit_tournament_button.setGeometry(QtCore.QRect(580, 160, 271, 51))
        self.edit_tournament_button.setObjectName("edit_tournament_button")
        self.label = QtWidgets.QLabel(EditTournament)
        self.label.setGeometry(QtCore.QRect(260, 270, 81, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.rounds_table = QtWidgets.QTableWidget(EditTournament)
        self.rounds_table.setGeometry(QtCore.QRect(100, 310, 401, 351))
        self.rounds_table.setObjectName("rounds_table")
        self.rounds_table.setColumnCount(0)
        self.rounds_table.setRowCount(0)
        self.edit_players_button = QtWidgets.QPushButton(EditTournament)
        self.edit_players_button.setGeometry(QtCore.QRect(580, 90, 271, 51))
        self.edit_players_button.setObjectName("edit_players_button")
        self.edit_rounds_button = QtWidgets.QPushButton(EditTournament)
        self.edit_rounds_button.setGeometry(QtCore.QRect(580, 330, 271, 51))
        self.edit_rounds_button.setObjectName("edit_rounds_button")

        self.retranslateUi(EditTournament)
        QtCore.QMetaObject.connectSlotsByName(EditTournament)

    def retranslateUi(self, EditTournament):
        _translate = QtCore.QCoreApplication.translate
        EditTournament.setWindowTitle(_translate("EditTournament", "Form"))
        self.create_tournament_title.setText(_translate("EditTournament", "Edit tournament"))
        self.tournament_name_label.setText(_translate("EditTournament", "Tournament name:"))
        self.tournament_date_label.setText(_translate("EditTournament", "Date:"))
        self.tournament_rounds_label.setText(_translate("EditTournament", "Rounds:"))
        self.generate_button.setText(_translate("EditTournament", "Generate rounds"))
        self.edit_tournament_button.setText(_translate("EditTournament", "Save changes"))
        self.label.setText(_translate("EditTournament", "Rounds:"))
        self.edit_players_button.setText(_translate("EditTournament", "Change players"))
        self.edit_rounds_button.setText(_translate("EditTournament", "Edit round"))
