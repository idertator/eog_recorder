# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DatosArchivo.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DatosArchivo(object):
    def setupUi(self, DatosArchivo):
        DatosArchivo.setObjectName("DatosArchivo")
        DatosArchivo.resize(450, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(DatosArchivo)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelTitle = QtWidgets.QLabel(DatosArchivo)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.labelTitle.setFont(font)
        self.labelTitle.setObjectName("labelTitle")
        self.verticalLayout.addWidget(self.labelTitle)
        self.labelDescription = QtWidgets.QLabel(DatosArchivo)
        self.labelDescription.setObjectName("labelDescription")
        self.verticalLayout.addWidget(self.labelDescription)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.txtPath = QtWidgets.QLineEdit(DatosArchivo)
        self.txtPath.setObjectName("txtPath")
        self.horizontalLayout.addWidget(self.txtPath)
        self.searchButton = QtWidgets.QPushButton(DatosArchivo)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchButton.sizePolicy().hasHeightForWidth())
        self.searchButton.setSizePolicy(sizePolicy)
        self.searchButton.setObjectName("searchButton")
        self.horizontalLayout.addWidget(self.searchButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 197, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(DatosArchivo)
        QtCore.QMetaObject.connectSlotsByName(DatosArchivo)

    def retranslateUi(self, DatosArchivo):
        _translate = QtCore.QCoreApplication.translate
        DatosArchivo.setWindowTitle(_translate("DatosArchivo", "Dialog"))
        self.labelTitle.setText(_translate("DatosArchivo", "Datos de almacenamiento"))
        self.labelDescription.setText(_translate("DatosArchivo", "Elija la ubicacion del fichero de salida:"))
        self.searchButton.setText(_translate("DatosArchivo", "Buscar..."))


