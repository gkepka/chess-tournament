# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'round_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RoundWidget(object):
    def setupUi(self, RoundWidget):
        RoundWidget.setObjectName("RoundWidget")
        RoundWidget.resize(1024, 768)
        self.label = QtWidgets.QLabel(RoundWidget)
        self.label.setGeometry(QtCore.QRect(0, 10, 1021, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.matches_table = QtWidgets.QTableWidget(RoundWidget)
        self.matches_table.setGeometry(QtCore.QRect(30, 110, 601, 571))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.matches_table.setFont(font)
        self.matches_table.setObjectName("matches_table")
        self.matches_table.setColumnCount(0)
        self.matches_table.setRowCount(0)
        self.label_2 = QtWidgets.QLabel(RoundWidget)
        self.label_2.setGeometry(QtCore.QRect(720, 160, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.sort_box = QtWidgets.QComboBox(RoundWidget)
        self.sort_box.setGeometry(QtCore.QRect(720, 200, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.sort_box.setFont(font)
        self.sort_box.setObjectName("sort_box")
        self.save_button = QtWidgets.QPushButton(RoundWidget)
        self.save_button.setGeometry(QtCore.QRect(720, 340, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.save_button.setFont(font)
        self.save_button.setObjectName("save_button")
        self.set_button = QtWidgets.QPushButton(RoundWidget)
        self.set_button.setGeometry(QtCore.QRect(720, 270, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.set_button.setFont(font)
        self.set_button.setObjectName("set_button")

        self.retranslateUi(RoundWidget)
        QtCore.QMetaObject.connectSlotsByName(RoundWidget)

    def retranslateUi(self, RoundWidget):
        _translate = QtCore.QCoreApplication.translate
        RoundWidget.setWindowTitle(_translate("RoundWidget", "Form"))
        self.label.setText(_translate("RoundWidget", "Round"))
        self.label_2.setText(_translate("RoundWidget", "Result"))
        self.save_button.setText(_translate("RoundWidget", "Save changes"))
        self.set_button.setText(_translate("RoundWidget", "Set result"))
