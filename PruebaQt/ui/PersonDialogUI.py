# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PersonDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PersonDialog(object):
    def setupUi(self, PersonDialog):
        PersonDialog.setObjectName("PersonDialog")
        PersonDialog.resize(542, 376)
        self.verticalLayout = QtWidgets.QVBoxLayout(PersonDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.nameLabel = QtWidgets.QLabel(PersonDialog)
        self.nameLabel.setObjectName("nameLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.nameLabel)
        self.nameEdit = QtWidgets.QLineEdit(PersonDialog)
        self.nameEdit.setObjectName("nameEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.nameEdit)
        self.lastNameLabel = QtWidgets.QLabel(PersonDialog)
        self.lastNameLabel.setObjectName("lastNameLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lastNameLabel)
        self.lastNameEdit = QtWidgets.QLineEdit(PersonDialog)
        self.lastNameEdit.setObjectName("lastNameEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lastNameEdit)
        self.borndateLabel = QtWidgets.QLabel(PersonDialog)
        self.borndateLabel.setObjectName("borndateLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.borndateLabel)
        self.borndateDate = QtWidgets.QDateEdit(PersonDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.borndateDate.sizePolicy().hasHeightForWidth())
        self.borndateDate.setSizePolicy(sizePolicy)
        self.borndateDate.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.borndateDate.setCalendarPopup(True)
        self.borndateDate.setObjectName("borndateDate")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.borndateDate)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 241, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(368, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.saveButton = QtWidgets.QPushButton(PersonDialog)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout.addWidget(self.saveButton)
        self.acceptButton = QtWidgets.QPushButton(PersonDialog)
        self.acceptButton.setObjectName("acceptButton")
        self.horizontalLayout.addWidget(self.acceptButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(PersonDialog)
        QtCore.QMetaObject.connectSlotsByName(PersonDialog)

    def retranslateUi(self, PersonDialog):
        _translate = QtCore.QCoreApplication.translate
        PersonDialog.setWindowTitle(_translate("PersonDialog", "Persona"))
        self.nameLabel.setText(_translate("PersonDialog", "Nombre"))
        self.lastNameLabel.setText(_translate("PersonDialog", "Apellidos"))
        self.borndateLabel.setText(_translate("PersonDialog", "Fecha de Nacimiento"))
        self.saveButton.setText(_translate("PersonDialog", "Guardar"))
        self.acceptButton.setText(_translate("PersonDialog", "Aceptar"))


