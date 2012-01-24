#!/usr/bin/python -d
 
import sys
from PyQt4 import QtCore, QtGui
from testIG import Ui_ProjetGherkin

#client lib
import xmlrpclib

#local lib : loading db
from load_db import *

#config file
import config

class MyForm(QtGui.QMainWindow):
  def __init__(self, parent=None):
    QtGui.QWidget.__init__(self, parent)
    self.ui = Ui_ProjetGherkin()
    self.ui.setupUi(self)
    self.pointeur = 0
     
    #getting in touch with server
    self.server = xmlrpclib.ServerProxy("http://localhost:" + str(config.defaultPort))

    #just tu show what commands are available
    #print self.server.system.listMethods()

    self.songs = get_lib()


    for u in range(len(self.songs)):
        try:
            self.ui.addTrack(self.songs[u]['title'])
        except:
            pass
    #loading song into the server
    self.server.load(self.songs[self.pointeur]['location'])
    
    QtCore.QObject.connect(self.ui.PlayButton, QtCore.SIGNAL("clicked()"), self.server.play_pause )
    QtCore.QObject.connect(self.ui.PlayButton, QtCore.SIGNAL("clicked()"), self.ui.iconChange )
    #QtCore.QObject.connect(self.AudioTrack, QtCore.SIGNAL(_fromUtf8("itemDoubleClicked(QTreeWidgetItem*,int)")), self.ui.loadSong(QTreeWidgetItem*,int))
    #playing song
    #s.play_pause()

  def add_entry(self):
    self.ui.lineEdit.selectAll()
    self.ui.lineEdit.cut()
    self.ui.textEdit.append("")
    self.ui.textEdit.paste()
 
if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  myapp = MyForm()
  myapp.show()
  sys.exit(app.exec_())