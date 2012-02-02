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

#local lib
import config

#logs
import logging
import logging.config
logging.config.fileConfig(config.logLocation + "log.conf")
log = logging.getLogger("GhkDbManagement")

#ID3 tag library
import mutagen

def gen_xml_db(directory, tagKept = config.defaultTagKept, fileExt = config.defaultFileExt, dbLocation = config.defaultDbLocation, dbFile = config.defaultDbFile):
    """create xml database (location : dbLocation) with tag in tagKept, for the files in the directory with the extension in defaultFileExt"""
    if(directory == ""):
        return False
    
    id = 0
    doc = Document()
    root = doc.createElement("db")
    doc.appendChild(root)
    
    #classic loops to check every files in the subdirectories at every level. Possibly long.
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

                    #for each tag given by mutagen, we add it to our library, useless to add unknow, load_db will do it alone.
                    for i in set(audio.keys()).intersection(tagKept):
                        tag[i] = doc.createElement(i)
                        block.appendChild(tag[i])
                        tagValue[i] = doc.createTextNode(audio[i][0].encode("utf-8"))
                        tag[i].appendChild(tagValue[i])
                except:
                    log.debug("Bad file encoding : " + os.path.join(dirname, f))
    
    #writing the result into "db.xml" (defaultpath)
    try:
        db = open(dbLocation + dbFile, "w")
        doc.writexml(db, "\n", "  ")
        db.close()
    except:
        log.error("Problem writing database")
    else:
        log.info("Database created at " + dbLocation)
