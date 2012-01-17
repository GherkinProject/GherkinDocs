# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Test_ig.ui'
#
# Created: Tue Jan  3 10:11:27 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ProjetGherkin(object):
    def setupUi(self, ProjetGherkin):
        ProjetGherkin.setObjectName(_fromUtf8("ProjetGherkin"))
        ProjetGherkin.setWindowIcon(QtGui.QIcon('gherkin.jpg'))
        ProjetGherkin.setWindowModality(QtCore.Qt.ApplicationModal)
        ProjetGherkin.resize(921, 566)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(213, 255, 223))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(149, 255, 175))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(42, 127, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(56, 170, 84))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 255, 191))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(213, 255, 223))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(149, 255, 175))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(42, 127, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(56, 170, 84))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 255, 191))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(42, 127, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(213, 255, 223))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(149, 255, 175))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(42, 127, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(56, 170, 84))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(42, 127, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(42, 127, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        ProjetGherkin.setPalette(palette)
        ProjetGherkin.setWindowTitle(QtGui.QApplication.translate("ProjetGherkin", "Projet Gherkin", None, QtGui.QApplication.UnicodeUTF8))
        ProjetGherkin.setToolTip(QtGui.QApplication.translate("ProjetGherkin", "Ceci est le projet de lecteur audio Gherkin", None, QtGui.QApplication.UnicodeUTF8))
        ProjetGherkin.setAutoFillBackground(False)


        #####################################################################


        self.Play_button = QtGui.QPushButton(ProjetGherkin)
        self.Play_button.setGeometry(QtCore.QRect(330, 530, 97, 27))
        self.Play_button.setToolTip(QtGui.QApplication.translate("ProjetGherkin", "Appuyez pour lancer la musique", None, QtGui.QApplication.UnicodeUTF8))
        self.Play_button.setAutoFillBackground(True)
        self.Play_button.setText(QtGui.QApplication.translate("ProjetGherkin", "Play", None, QtGui.QApplication.UnicodeUTF8))
        self.Play_button.setIconSize(QtCore.QSize(50, 50))
        self.Play_button.setObjectName(_fromUtf8("Play_button"))


        ##################################################################


        self.Stop_button = QtGui.QPushButton(ProjetGherkin)
        self.Stop_button.setGeometry(QtCore.QRect(430, 530, 97, 27))
        self.Stop_button.setText(QtGui.QApplication.translate("ProjetGherkin", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.Stop_button.setObjectName(_fromUtf8("Stop_button"))

        #################################################################

        self.next_button = QtGui.QPushButton(ProjetGherkin)
        self.next_button.setGeometry(QtCore.QRect(530, 530, 97, 27))
        self.next_button.setText(QtGui.QApplication.translate("ProjetGherkin", "Next", None, QtGui.QApplication.UnicodeUTF8))
        self.next_button.setObjectName(_fromUtf8("next_button"))


        #################################################################

        self.prev_button = QtGui.QPushButton(ProjetGherkin)
        self.prev_button.setGeometry(QtCore.QRect(230, 530, 97, 27))
        self.prev_button.setStyleSheet(_fromUtf8("image: url(:/Cornichon/gherkin.jpg);"))
        self.prev_button.setText(QtGui.QApplication.translate("ProjetGherkin", "Previous", None, QtGui.QApplication.UnicodeUTF8))
        self.prev_button.setObjectName(_fromUtf8("prev_button"))


        #################################################################

        self.Liste_de_lecture = QtGui.QListView(ProjetGherkin)
        self.Liste_de_lecture.setGeometry(QtCore.QRect(560, 10, 321, 511))
        self.Liste_de_lecture.setToolTip(QtGui.QApplication.translate("ProjetGherkin", "Ceci est la liste de lecture", None, QtGui.QApplication.UnicodeUTF8))
        self.Liste_de_lecture.setObjectName(_fromUtf8("Liste_de_lecture"))


        #################################################################

        self.Barre_de_son = QtGui.QSlider(ProjetGherkin)
        self.Barre_de_son.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Barre_de_son.setGeometry(QtCore.QRect(640, 510, 200, 61))
        self.Barre_de_son.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.Barre_de_son.setOrientation(QtCore.Qt.Horizontal)
        self.Barre_de_son.setObjectName(_fromUtf8("Barre_de_son"))

        self.label = QtGui.QLabel(ProjetGherkin)
        self.label.setPixmap(QtGui.QPixmap('mute.png'))
        self.label.setGeometry(850, 510, 50,50)

        


        #################################################################

        self.lcdNumber = QtGui.QLCDNumber(ProjetGherkin)
        self.lcdNumber.setGeometry(QtCore.QRect(23, 522, 181, 31))
        self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))


        #################################################################

        self.Details_liste_lecture = QtGui.QListView(ProjetGherkin)
        self.Details_liste_lecture.setGeometry(QtCore.QRect(0, 20, 541, 461))
        self.Details_liste_lecture.setObjectName(_fromUtf8("Details_liste_lecture"))

        #################################################################

        self.Progression_musique = QtGui.QSlider(ProjetGherkin)
        self.Progression_musique.setGeometry(QtCore.QRect(10, 490, 531, 29))
        self.Progression_musique.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.Progression_musique.setOrientation(QtCore.Qt.Horizontal)
        self.Progression_musique.setObjectName(_fromUtf8("Progression_musique"))

        #################################################################

        self.retranslateUi(ProjetGherkin)
        QtCore.QMetaObject.connectSlotsByName(ProjetGherkin)

    def retranslateUi(self, ProjetGherkin):
        pass



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ProjetGherkin = QtGui.QDialog()
    ui = Ui_ProjetGherkin()
    ui.setupUi(ProjetGherkin)
    ProjetGherkin.show()
    sys.exit(app.exec_())

