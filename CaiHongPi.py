# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CaiHongPi.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CaiHongPiDialog(object):
    def setupUi(self, CaiHongPiDialog):
        CaiHongPiDialog.setObjectName("CaiHongPiDialog")
        CaiHongPiDialog.resize(500, 500)
        self.verticalLayoutWidget = QtWidgets.QWidget(CaiHongPiDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 481, 481))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.dialogLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.dialogLayout.setContentsMargins(0, 0, 0, 0)
        self.dialogLayout.setObjectName("dialogLayout")

        self.retranslateUi(CaiHongPiDialog)
        QtCore.QMetaObject.connectSlotsByName(CaiHongPiDialog)

    def retranslateUi(self, CaiHongPiDialog):
        _translate = QtCore.QCoreApplication.translate
        CaiHongPiDialog.setWindowTitle(_translate("CaiHongPiDialog", "肖哥的彩虹屁"))
