# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\lemba\Documents\GitHub\Fase-II\faseII_BlackHats\popup.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(538, 411)
        Dialog.setMinimumSize(QtCore.QSize(0, 0))
        Dialog.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.widget_2 = QtWidgets.QWidget(Dialog)
        self.widget_2.setMaximumSize(QtCore.QSize(16777215, 250))
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_3 = QtWidgets.QWidget(self.widget_2)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.alertMessage = QtWidgets.QTextEdit(self.widget_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.alertMessage.setFont(font)
        self.alertMessage.setReadOnly(True)
        self.alertMessage.setOverwriteMode(False)
        self.alertMessage.setObjectName("alertMessage")
        self.horizontalLayout_3.addWidget(self.alertMessage)
        self.verticalLayout.addWidget(self.widget_3)
        self.widget_4 = QtWidgets.QWidget(self.widget_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.widget_4.setFont(font)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.fechaAlert = QtWidgets.QLabel(self.widget_4)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.fechaAlert.setFont(font)
        self.fechaAlert.setText("")
        self.fechaAlert.setAlignment(QtCore.Qt.AlignCenter)
        self.fechaAlert.setObjectName("fechaAlert")
        self.horizontalLayout.addWidget(self.fechaAlert)
        self.verticalLayout.addWidget(self.widget_4)
        self.widget_5 = QtWidgets.QWidget(self.widget_2)
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.nombreCentral = QtWidgets.QLabel(self.widget_5)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.nombreCentral.setFont(font)
        self.nombreCentral.setText("")
        self.nombreCentral.setAlignment(QtCore.Qt.AlignCenter)
        self.nombreCentral.setObjectName("nombreCentral")
        self.horizontalLayout_2.addWidget(self.nombreCentral)
        self.verticalLayout.addWidget(self.widget_5)
        self.gridLayout.addWidget(self.widget_2, 1, 0, 1, 1)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 100))
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(200, 0, 121, 101))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/newPrefix/icons/senal-de-alerta.png"))
        self.label.setScaledContents(True)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
import resource_rc
