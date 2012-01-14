#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#standards libraries

#xml
import xml.etree.ElementTree as ET

#local libraries
import config


def get_lib(dbLocation = config.defaultDbLocation):
    tree = ET.ElementTree()
    tree.parse(dbLocation)

    songs = []
    for f in tree.findall('file'):
        songs.append(dict())
        songs[-1]['id'] = int(f.get('id'))
        for element in f: 
               songs[-1][element.tag] = element.text 

    return songs
