# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/zihanli/program/498-Vocaloid/vocaloid/gui/generatewindow.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(1920, 1080))
        font = QtGui.QFont()
        font.setFamily("Arial")
        MainWindow.setFont(font)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setStyleSheet("QMainFrame { background-image: url(:background.jpeg) }")
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.comboBox = QtWidgets.QComboBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setMinimumSize(QtCore.QSize(340, 80))
        self.comboBox.setSizeIncrement(QtCore.QSize(0, 0))
        self.comboBox.setBaseSize(QtCore.QSize(0, 0))
        self.comboBox.setStyleSheet("font: 18pt \".SF NS Text\";")
        self.comboBox.setCurrentText("")
        self.comboBox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox.setMinimumContentsLength(26)
        self.comboBox.setFrame(True)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 3, 0, 1, 1, QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.generateButton = QtWidgets.QPushButton(self.centralWidget)
        self.generateButton.setMinimumSize(QtCore.QSize(340, 160))
        self.generateButton.setStyleSheet("font: 36pt \"Arial\";")
        self.generateButton.setObjectName("generateButton")
        self.gridLayout.addWidget(self.generateButton, 1, 0, 1, 1, QtCore.Qt.AlignRight|QtCore.Qt.AlignBottom)
        self.restartButton = QtWidgets.QPushButton(self.centralWidget)
        self.restartButton.setMinimumSize(QtCore.QSize(340, 160))
        self.restartButton.setStyleSheet("font: 36pt \"Arial\";")
        self.restartButton.setObjectName("restartButton")
        self.gridLayout.addWidget(self.restartButton, 1, 2, 1, 1, QtCore.Qt.AlignLeft|QtCore.Qt.AlignBottom)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setMinimumSize(QtCore.QSize(340, 0))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label, 0, QtCore.Qt.AlignRight)
        self.gridLayout.addLayout(self.verticalLayout_2, 2, 0, 1, 1)
        self.gridLayout.setColumnStretch(0, 2)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 2)
        self.gridLayout.setRowStretch(0, 5)
        self.gridLayout.setRowStretch(1, 2)
        self.gridLayout.setRowStretch(2, 2)
        self.gridLayout.setRowStretch(3, 5)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.back4Button = QtWidgets.QPushButton(self.centralWidget)
        self.back4Button.setMinimumSize(QtCore.QSize(340, 160))
        self.back4Button.setStyleSheet("font: 75 36pt \"Arial\";")
        self.back4Button.setObjectName("back4Button")
        self.horizontalLayout_2.addWidget(self.back4Button, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.exitButton = QtWidgets.QPushButton(self.centralWidget)
        self.exitButton.setMinimumSize(QtCore.QSize(340, 160))
        self.exitButton.setStyleSheet("font: 75 36pt \"Arial\";")
        self.exitButton.setObjectName("exitButton")
        self.horizontalLayout_2.addWidget(self.exitButton, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.setStretch(0, 5)
        self.verticalLayout.setStretch(1, 2)
        MainWindow.setCentralWidget(self.centralWidget)

        Ui_MainWindow.retranslateUi(self, MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Vocaloid"))
        self.generateButton.setText(_translate("MainWindow", "Generate Song"))
        self.restartButton.setText(_translate("MainWindow", "Restart"))
        self.label.setText(_translate("MainWindow", "Choose a voice:"))
        self.back4Button.setText(_translate("MainWindow", "Back"))
        self.exitButton.setText(_translate("MainWindow", "Exit"))

