#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#standards libraries

#script with arguments
import sys
#script using system commands
import os
#script using dom
from xml.dom.minidom import Document
#ID3 tag library
import mutagen

#local libraries
import config


#This is a test function, creating a list with locations in it
def list_files(directory, fileExt = config.defaultFileExt.keys()):
    """get list of directories in the directory"""
    files = []
    for dirname, dirnames, filenames in os.walk(directory):
        for f in filenames:
            if os.path.splitext(f)[1] in fileExt:
                files.append(os.path.join(dirname, f))
    return files

#print list_files("/home/nicolas")

def create_db(directory, fileExt = config.defaultFileExt, dbLocation = config.defaultDbLocation):
    """create xml database (location : dbLocation) for the files in the directory with the extension in defaultFileExtSet"""
    id = 0
    doc = Document()
    root = doc.createElement("db")
    doc.appendChild(root)
    for dirname, dirnames, filenames in os.walk(directory):
        for f in filenames:
            if os.path.splitext(f)[1] in fileExt.keys():
                block = doc.createElement("file")
                block.setAttribute("id", str(id))
                id += 1
                root.appendChild(block)
                location = doc.createElement("location")
                block.appendChild(location)
                locationValue = doc.createTextNode(os.path.join(dirname, f))
                location.appendChild(locationValue)
                audio = mutagen.File(os.path.join(dirname, f), easy = True)
		tag = dict()
		tagValue = dict()
		print audio
		for i in audio.keys():
		    tag[i] = doc.createElement(i)
		    block.appendChild(tag[i])
		    print audio[i][0].encode("utf-8")
		    tagValue[i] = doc.createTextNode(audio[i][0].encode("utf-8"))
		    tag[i].appendChild(tagValue[i]) 
    db = open("db.xml", "w")
    doc.writexml(db, "\n", "  ")
    db.close()
    
create_db("example/")