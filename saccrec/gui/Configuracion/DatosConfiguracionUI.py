# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DatosConfiguracion.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Configuracion(object):
    def setupUi(self, Configuracion):
        Configuracion.setObjectName("Configuracion")
        Configuracion.resize(574, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Configuracion)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Configuracion)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(Configuracion)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.txt_captureport = QtWidgets.QSpinBox(Configuracion)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_captureport.sizePolicy().hasHeightForWidth())
        self.txt_captureport.setSizePolicy(sizePolicy)
        self.txt_captureport.setMaximumSize(QtCore.QSize(75, 16777215))
        self.txt_captureport.setObjectName("txt_captureport")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txt_captureport)
        self.label_3 = QtWidgets.QLabel(Configuracion)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.txt_horizontalsize = QtWidgets.QDoubleSpinBox(Configuracion)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_horizontalsize.sizePolicy().hasHeightForWidth())
        self.txt_horizontalsize.setSizePolicy(sizePolicy)
        self.txt_horizontalsize.setMaximumSize(QtCore.QSize(75, 16777215))
        self.txt_horizontalsize.setObjectName("txt_horizontalsize")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.txt_horizontalsize)
        self.label_5 = QtWidgets.QLabel(Configuracion)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.txt_verticalsize = QtWidgets.QDoubleSpinBox(Configuracion)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_verticalsize.sizePolicy().hasHeightForWidth())
        self.txt_verticalsize.setSizePolicy(sizePolicy)
        self.txt_verticalsize.setMaximumSize(QtCore.QSize(75, 16777215))
        self.txt_verticalsize.setObjectName("txt_verticalsize")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.txt_verticalsize)
        self.label_4 = QtWidgets.QLabel(Configuracion)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.txt_maxdistance = QtWidgets.QDoubleSpinBox(Configuracion)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_maxdistance.sizePolicy().hasHeightForWidth())
        self.txt_maxdistance.setSizePolicy(sizePolicy)
        self.txt_maxdistance.setMaximumSize(QtCore.QSize(75, 16777215))
        self.txt_maxdistance.setObjectName("txt_maxdistance")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.txt_maxdistance)
        self.verticalLayout.addLayout(self.formLayout)

        self.retranslateUi(Configuracion)
        QtCore.QMetaObject.connectSlotsByName(Configuracion)

    def retranslateUi(self, Configuracion):
        _translate = QtCore.QCoreApplication.translate
        Configuracion.setWindowTitle(_translate("Configuracion", "Dialog"))
        self.label.setText(_translate("Configuracion", "Datos de Configuracion"))
        self.label_2.setText(_translate("Configuracion", "Puerto de Captura:"))
        self.label_3.setText(_translate("Configuracion", "Tamaño de pantalla de ancho(centimetros):"))
        self.label_5.setText(_translate("Configuracion", "Tamaño de pantalla de alto(centimetros):"))
        self.label_4.setText(_translate("Configuracion", "Distancia entre los 2 estímulos para el ángulo máximo (centimetros):"))


