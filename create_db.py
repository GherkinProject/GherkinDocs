#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#standards libraries

#script with arguments
import sys
#script using system commands
import os
#script using dom
from xml.dom.minidom import Document

#local libraries
from config import *


#This is a test function, creating a list with locations in it
def list_files(directory, fileExtSet = defaultFileExtSet):
    """get list of directories in the directory"""
    files = []
    for dirname, dirnames, filenames in os.walk(directory):
        for f in filenames:
            if os.path.splitext(f)[1] in fileExtSet:
                files.append(os.path.join(dirname, f))
    return files

#print list_files("/home/nicolas")

def create_db(directory, fileExtSet = defaultFileExtSet, dbLocation = defaultDbLocation):
    """create xml database (location : dbLocation) for the files in the directory with the extension in defaultFileExtSet"""
    id = 0
    doc = Document()
    root = doc.createElement("db")
    doc.appendChild(root)
    for dirname, dirnames, filenames in os.walk(directory):
        for f in filenames:
            if os.path.splitext(f)[1] in fileExtSet:
                block = doc.createElement("file")
                block.setAttribute("id", str(id))
                id += 1
                root.appendChild(block)
                location = doc.createElement("location")
                location.setAttribute("value", os.path.join(dirname, f))
                block.appendChild(location)
    db = open("db.xml", "w")
    doc.writexml(db, "", "   ", '\n')
    db.close()
    
create_db("/home/nicolas")
