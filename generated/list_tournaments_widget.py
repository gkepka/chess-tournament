# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'list_tournaments_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ListTournaments(object):
    def setupUi(self, ListTournaments):
        ListTournaments.setObjectName("ListTournaments")
        ListTournaments.resize(1024, 768)
        self.label = QtWidgets.QLabel(ListTournaments)
        self.label.setGeometry(QtCore.QRect(0, 10, 1021, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.tournaments_table = QtWidgets.QTableWidget(ListTournaments)
        self.tournaments_table.setGeometry(QtCore.QRect(30, 110, 601, 571))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.tournaments_table.setFont(font)
        self.tournaments_table.setObjectName("tournaments_table")
        self.tournaments_table.setColumnCount(0)
        self.tournaments_table.setRowCount(0)
        self.choose_button = QtWidgets.QPushButton(ListTournaments)
        self.choose_button.setGeometry(QtCore.QRect(720, 153, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.choose_button.setFont(font)
        self.choose_button.setObjectName("choose_button")
        self.edit_button = QtWidgets.QPushButton(ListTournaments)
        self.edit_button.setGeometry(QtCore.QRect(720, 220, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.edit_button.setFont(font)
        self.edit_button.setObjectName("edit_button")
        self.delete_button = QtWidgets.QPushButton(ListTournaments)
        self.delete_button.setGeometry(QtCore.QRect(720, 290, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.delete_button.setFont(font)
        self.delete_button.setObjectName("delete_button")
        self.label_2 = QtWidgets.QLabel(ListTournaments)
        self.label_2.setGeometry(QtCore.QRect(720, 360, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.sort_box = QtWidgets.QComboBox(ListTournaments)
        self.sort_box.setGeometry(QtCore.QRect(720, 400, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.sort_box.setFont(font)
        self.sort_box.setObjectName("sort_box")

        self.retranslateUi(ListTournaments)
        QtCore.QMetaObject.connectSlotsByName(ListTournaments)

    def retranslateUi(self, ListTournaments):
        _translate = QtCore.QCoreApplication.translate
        ListTournaments.setWindowTitle(_translate("ListTournaments", "Form"))
        self.label.setText(_translate("ListTournaments", "Tournament list"))
        self.choose_button.setText(_translate("ListTournaments", "Choose as current"))
        self.edit_button.setText(_translate("ListTournaments", "Edit"))
        self.delete_button.setText(_translate("ListTournaments", "Delete"))
        self.label_2.setText(_translate("ListTournaments", "Sort by:"))
