# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DatosPaciente.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DatosPaciente(object):
    def setupUi(self, DatosPaciente):
        DatosPaciente.setObjectName("DatosPaciente")
        DatosPaciente.resize(439, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(DatosPaciente)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.labelTitle = QtWidgets.QLabel(DatosPaciente)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.labelTitle.setFont(font)
        self.labelTitle.setObjectName("labelTitle")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelTitle)
        self.labelName = QtWidgets.QLabel(DatosPaciente)
        self.labelName.setObjectName("labelName")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelName)
        self.txtName = QtWidgets.QLineEdit(DatosPaciente)
        self.txtName.setObjectName("txtName")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txtName)
        self.labelGenre = QtWidgets.QLabel(DatosPaciente)
        self.labelGenre.setObjectName("labelGenre")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.labelGenre)
        self.comboGenre = QtWidgets.QComboBox(DatosPaciente)
        self.comboGenre.setObjectName("comboGenre")
        self.comboGenre.addItem("")
        self.comboGenre.addItem("")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboGenre)
        self.labelBornDate = QtWidgets.QLabel(DatosPaciente)
        self.labelBornDate.setObjectName("labelBornDate")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.labelBornDate)
        self.borndateDate = QtWidgets.QDateEdit(DatosPaciente)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.borndateDate.sizePolicy().hasHeightForWidth())
        self.borndateDate.setSizePolicy(sizePolicy)
        self.borndateDate.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.borndateDate.setCalendarPopup(True)
        self.borndateDate.setObjectName("borndateDate")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.borndateDate)
        self.labelState = QtWidgets.QLabel(DatosPaciente)
        self.labelState.setObjectName("labelState")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.labelState)
        self.comboState = QtWidgets.QComboBox(DatosPaciente)
        self.comboState.setObjectName("comboState")
        self.comboState.addItem("")
        self.comboState.addItem("")
        self.comboState.addItem("")
        self.comboState.addItem("")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.comboState)
        self.verticalLayout.addLayout(self.formLayout)

        self.retranslateUi(DatosPaciente)
        QtCore.QMetaObject.connectSlotsByName(DatosPaciente)

    def retranslateUi(self, DatosPaciente):
        _translate = QtCore.QCoreApplication.translate
        DatosPaciente.setWindowTitle(_translate("DatosPaciente", "Dialog"))
        self.labelTitle.setText(_translate("DatosPaciente", "Datos del Paciente"))
        self.labelName.setText(_translate("DatosPaciente", "Nombre(s):"))
        self.labelGenre.setText(_translate("DatosPaciente", "Género:"))
        self.comboGenre.setItemText(0, _translate("DatosPaciente", "Masculino"))
        self.comboGenre.setItemText(1, _translate("DatosPaciente", "Femenino"))
        self.labelBornDate.setText(_translate("DatosPaciente", "Fecha de nacimiento:"))
        self.labelState.setText(_translate("DatosPaciente", "Estado:"))
        self.comboState.setItemText(0, _translate("DatosPaciente", "Desconocido"))
        self.comboState.setItemText(1, _translate("DatosPaciente", "Control"))
        self.comboState.setItemText(2, _translate("DatosPaciente", "Presintomático"))
        self.comboState.setItemText(3, _translate("DatosPaciente", "SCA2"))


