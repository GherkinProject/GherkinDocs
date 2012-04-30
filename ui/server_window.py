# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Server-change.ui'
#
# Created: Mon Apr 30 21:37:59 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class server_window():
    def setup_server_window(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(320, 240)
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))

        #OK and Cancel buttons
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 200, 301, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))

        #lineEdit to insert the IP adress of the new server
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(10, 10, 291, 27))
        self.lineEdit.setText(QtGui.QApplication.translate("Dialog", "Entrez le nom du serveur", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))

        #listWidget of the previously used server by the user
        self.listWidget = QtGui.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(10, 50, 301, 141))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))

        #Button to start the search of new server
        self.radioButton = QtGui.QRadioButton(Dialog)
        self.radioButton.setGeometry(QtCore.QRect(10, 200, 116, 22))
        self.radioButton.setText(QtGui.QApplication.translate("Dialog", "Recherche", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton.setObjectName(_fromUtf8("radioButton"))

        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

	def add_server(self, serverName):
            itemAT=QtGui.QListWidgetItem()
            itemAT.setText(0, serverName)
            self.listWidget.addItem(itemAT)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = server_window()
    ui.setup_server_window(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

