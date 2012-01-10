#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#standards libraries

#script with arguments
import sys
#script using system commands
import os
#script using dom
from xml.dom.minidom import Document
from xml.dom import minidom

#patch dom to gain space
def newwritexml(self, writer, indent= '', addindent= '', newl= ''):
    if len(self.childNodes)==1 and self.firstChild.nodeType==3:
        writer.write(indent)
        self.oldwritexml(writer) # cancel extra whitespace
        writer.write(newl)
    else:
        self.oldwritexml(writer, indent, addindent, newl)
minidom.Element.oldwritexml= minidom.Element.writexml
minidom.Element.writexml= newwritexml

#ID3 tag library
import mutagen

#local libraries
import config

def create_db(directory, tagKept = config.defaultTagKept, fileExt = config.defaultFileExt, dbLocation = config.defaultDbLocation):
    """create xml database (location : dbLocation) with tag in tagKept, for the files in the directory with the extension in defaultFileExt"""
    id = 0
    doc = Document()
    root = doc.createElement("db")
    doc.appendChild(root)
    for dirname, dirnames, filenames in os.walk(directory):
        for f in filenames:
            if os.path.splitext(f)[1].lower() in fileExt:
                try:    
                    audio = mutagen.File(os.path.join(dirname, f), easy = True)
                    block = doc.createElement("file")
                    block.setAttribute("id", str(id))
                    id += 1
                    root.appendChild(block)
                    location = doc.createElement("location")
                    block.appendChild(location)
                    locationValue = doc.createTextNode(os.path.join(dirname, f))
                    location.appendChild(locationValue)
                    tag = dict()
                    tagValue = dict()
                    for i in set(audio.keys()).intersection(tagKept):
                        tag[i] = doc.createElement(i)
                        block.appendChild(tag[i])
                        tagValue[i] = doc.createTextNode(audio[i][0].encode("utf-8"))
                        tag[i].appendChild(tagValue[i])
                except:
                    print "bad file encoding : " + os.path.join(dirname, f)
    db = open("db.xml", "w")
    doc.writexml(db, "\n", "  ")
    db.close()

if sys.argv[1] == "":
    print "path of the data base expected"
else:
    create_db(sys.argv[1])
    print "database created at " + config.defaultDbLocation
