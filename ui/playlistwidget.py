# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Playlist.ui'
#
# Created: Mon Apr 30 21:37:40 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from time import *

#configuration constant
from configUi import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class playlist_window(object):
    def setup_playlist_window(self, Form):

        # Creation of the object and layout.
        Form.setObjectName(_fromUtf8("Playlist"))
        Form.resize(325, 446)
        Form.setWindowTitle(QtGui.QApplication.translate("Playlist", "Playlist", None, QtGui.QApplication.UnicodeUTF8))
	Form.setWindowOpacity(0.72)
        self.verticalLayoutWidget = QtGui.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 2, 2))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

        # Creation of the tree widget that should contain the actual playlist.
        self.Playlist = QtGui.QTreeWidget(Form)
        self.Playlist.setGeometry(QtCore.QRect(10, 10, 311, 401))
        self.Playlist.setObjectName(_fromUtf8("Playlist"))
        self.Playlist.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        
        self.Playlist.headerItem().setText(0, QtGui.QApplication.translate("Playlist", "Titre", None, QtGui.QApplication.UnicodeUTF8))
        self.Playlist.headerItem().setTextAlignment(0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.Playlist.headerItem().setText(1, QtGui.QApplication.translate("Playlist", "Artiste", None, QtGui.QApplication.UnicodeUTF8))
        self.Playlist.headerItem().setTextAlignment(1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
       
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass

    def addTrack(self,u):
               
        itemAT=QtGui.QTreeWidgetItem()
        try:
            itemAT.setText(0, u['title'])
        except:
            itemAT.setText(0, config.defaultUnknown)
        try:
            itemAT.setText(1, u['artist'])
        except:
            itemAT.setText(1, config.defaultUnknown)

        itemAT.setText(2, u['location'])
        itemAT.setText(3, u['id'])
        self.Playlist.addTopLevelItem(itemAT)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = playlist_window()
    ui.setup_playlist_window(Form)
    Form.show()
    sys.exit(app.exec_())

