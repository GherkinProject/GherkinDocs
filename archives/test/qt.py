# -*- coding: utf-8 -*-
import sys

from PyQt4 import *

class MW(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        layout = QHBoxLayout(self)
        self.b1 = QPushButton("Button1")
        self.b2 = QPushButton("Button2")
        layout.addWidget(self.b1)
        layout.addWidget(self.b2)
        self.connect(self.b1, SIGNAL("clicked()"), self.buttonWasPressed)
        self.connect(self.b2, SIGNAL("clicked()"), self.buttonWasPressed)

    def buttonWasPressed(self):
        print "button %s was pressed" % self.sender()

