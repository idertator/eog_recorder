# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DatosPrueba.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DatosPrueba(object):
    def setupUi(self, DatosPrueba):
        DatosPrueba.setObjectName("DatosPrueba")
        DatosPrueba.resize(443, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(DatosPrueba)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(DatosPrueba)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(DatosPrueba)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.txt_angulo = QtWidgets.QSpinBox(DatosPrueba)
        self.txt_angulo.setObjectName("txt_angulo")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txt_angulo)
        self.label_3 = QtWidgets.QLabel(DatosPrueba)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.txt_mean_duration = QtWidgets.QDoubleSpinBox(DatosPrueba)
        self.txt_mean_duration.setObjectName("txt_mean_duration")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.txt_mean_duration)
        self.label_4 = QtWidgets.QLabel(DatosPrueba)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.txt_variaton = QtWidgets.QDoubleSpinBox(DatosPrueba)
        self.txt_variaton.setObjectName("txt_variaton")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.txt_variaton)
        self.label_5 = QtWidgets.QLabel(DatosPrueba)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.txt_testduration = QtWidgets.QDoubleSpinBox(DatosPrueba)
        self.txt_testduration.setObjectName("txt_testduration")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.txt_testduration)
        self.verticalLayout.addLayout(self.formLayout)

        self.retranslateUi(DatosPrueba)
        QtCore.QMetaObject.connectSlotsByName(DatosPrueba)

    def retranslateUi(self, DatosPrueba):
        _translate = QtCore.QCoreApplication.translate
        DatosPrueba.setWindowTitle(_translate("DatosPrueba", "Dialog"))
        self.label.setText(_translate("DatosPrueba", "Datos de la prueba"))
        self.label_2.setText(_translate("DatosPrueba", "Angulo de estimulo:"))
        self.label_3.setText(_translate("DatosPrueba", "Duracion media del estimulo:"))
        self.label_4.setText(_translate("DatosPrueba", "Rango de variacion en segundos:"))
        self.label_5.setText(_translate("DatosPrueba", "Duracion de la prueba:"))


