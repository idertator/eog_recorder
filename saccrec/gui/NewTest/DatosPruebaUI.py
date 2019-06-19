# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DatosPrueba.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DatosPrueba(object):
    def setupUi(self, Ui_Page2):
        Ui_Page2.setObjectName("Ui_Page2")
        Ui_Page2.resize(443, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Ui_Page2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Ui_Page2)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(Ui_Page2)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.spinBox = QtWidgets.QSpinBox(Ui_Page2)
        self.spinBox.setObjectName("spinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spinBox)
        self.label_3 = QtWidgets.QLabel(Ui_Page2)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(Ui_Page2)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox)
        self.label_4 = QtWidgets.QLabel(Ui_Page2)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(Ui_Page2)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_2)
        self.label_5 = QtWidgets.QLabel(Ui_Page2)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.doubleSpinBox_3 = QtWidgets.QDoubleSpinBox(Ui_Page2)
        self.doubleSpinBox_3.setObjectName("doubleSpinBox_3")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_3)
        self.verticalLayout.addLayout(self.formLayout)

        self.retranslateUi(Ui_Page2)
        QtCore.QMetaObject.connectSlotsByName(Ui_Page2)

    def retranslateUi(self, Ui_Page2):
        _translate = QtCore.QCoreApplication.translate
        Ui_Page2.setWindowTitle(_translate("Ui_Page2", "Dialog"))
        self.label.setText(_translate("Ui_Page2", "Datos de la prueba"))
        self.label_2.setText(_translate("Ui_Page2", "Angulo de estimulo:"))
        self.label_3.setText(_translate("Ui_Page2", "Duracion media del estimulo:"))
        self.label_4.setText(_translate("Ui_Page2", "Rango de variacion en segundos:"))
        self.label_5.setText(_translate("Ui_Page2", "Duracion de la prueba:"))


