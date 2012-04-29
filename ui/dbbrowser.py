#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore

class Browser_Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        # Creation de la boite de dialogue

        self.resize(600, 600)
        self.setWindowTitle('Explorateur')

        # Raccourci pour la fermeture de la fenêtre

        exit = QtGui.QAction('Fermer', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip("Fermeture de l'application") 
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        
        # Bouton chemin et editeur de chemin

        self.dest_path_edit = QtGui.QLineEdit()
        self.select_path = QtGui.QPushButton("Charger la base de pistes audio")


        self.fileBrowserWidget = QtGui.QWidget(self)

        self.dirmodel = QtGui.QFileSystemModel()

        # Arbre pour visionner les dossiers

        self.folder_view = QtGui.QTreeView(parent=self);
        self.folder_view.setModel(self.dirmodel)
        self.folder_view.clicked[QtCore.QModelIndex].connect(self.clicked) 
        self.folder_view.setHeaderHidden(True)
        self.folder_view.hideColumn(1)
        self.folder_view.hideColumn(2)
        self.folder_view.hideColumn(3)

        self.connect(self.dirmodel, QtCore.SIGNAL("directoryLoaded(const QString &)"), self.dest_path_edit.setText)

        #self.connect(self.select_path, QtCore.SIGNAL("clicked()", wtf)

        self.selectionModel = self.folder_view.selectionModel()


        group_input = QtGui.QGroupBox()
        grid_input = QtGui.QGridLayout()

        splitter_filebrowser = QtGui.QSplitter()
        splitter_filebrowser.addWidget(self.folder_view)
        splitter_filebrowser.setStretchFactor(0,2)
        splitter_filebrowser.setStretchFactor(1,4)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(splitter_filebrowser)
        self.fileBrowserWidget.setLayout(hbox)

        grid_input.addWidget(self.dest_path_edit, 0, 0)
        grid_input.addWidget(self.select_path, 0, 1)



       # vbox_options = QtGui.QVBoxLayout(self.optionsWidget)
#        vbox_options.addWidget(files_list)
        #vbox_options.addWidget(group_input)
        #self.optionsWidget.setLayout(vbox_options)

        splitter_filelist = QtGui.QSplitter()
        splitter_filelist.setOrientation(QtCore.Qt.Vertical)
        splitter_filelist.addWidget(self.fileBrowserWidget)
        vbox_main = QtGui.QVBoxLayout()
        vbox_main.addWidget(splitter_filelist)      
        vbox_main.addWidget(self.dest_path_edit)
        vbox_main.addWidget(self.select_path) 
        vbox_main.setContentsMargins(0,0,0,0)
        self.setLayout(vbox_main)     

    def set_path(self):
        self.dirmodel.setRootPath("")     

    def clicked(self, index):
        #get selected path of folder_view
        index = self.selectionModel.currentIndex()
        dir_path = self.dirmodel.filePath(index)


