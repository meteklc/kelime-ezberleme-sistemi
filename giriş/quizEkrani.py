# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'quizEkrani.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_quizEkrani(object):
    def setupUi(self, quizEkrani):
        quizEkrani.setObjectName("quizEkrani")
        quizEkrani.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(quizEkrani)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(190, 450, 344, 30))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.cevapLne = QtWidgets.QLineEdit(self.layoutWidget)
        self.cevapLne.setObjectName("cevapLne")
        self.horizontalLayout.addWidget(self.cevapLne)
        self.cevapBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.cevapBtn.setObjectName("cevapBtn")
        self.horizontalLayout.addWidget(self.cevapBtn)
        self.kelimeLabel = QtWidgets.QLabel(self.centralwidget)
        self.kelimeLabel.setGeometry(QtCore.QRect(200, 380, 331, 41))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.kelimeLabel.setFont(font)
        self.kelimeLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.kelimeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.kelimeLabel.setObjectName("kelimeLabel")
        quizEkrani.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(quizEkrani)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        quizEkrani.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(quizEkrani)
        self.statusbar.setObjectName("statusbar")
        quizEkrani.setStatusBar(self.statusbar)

        self.retranslateUi(quizEkrani)
        QtCore.QMetaObject.connectSlotsByName(quizEkrani)

    def retranslateUi(self, quizEkrani):
        _translate = QtCore.QCoreApplication.translate
        quizEkrani.setWindowTitle(_translate("quizEkrani", "Quiz"))
        self.label.setText(_translate("quizEkrani", "Cevabınızı Girniz:"))
        self.cevapBtn.setText(_translate("quizEkrani", "Cevabı Gir"))
        self.kelimeLabel.setText(_translate("quizEkrani", "TextLabel"))
