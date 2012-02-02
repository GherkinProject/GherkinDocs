#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#standards libraries

#xml
import xml.etree.ElementTree as ET

#local libraries
import config

#logs
import logging
import logging.config
logging.config.fileConfig(config.logLocation + "log.conf")
log = logging.getLogger("GhkDbManagement")

def get_lib(dbLocation = config.defaultDbLocation, dbFile = config.defaultDbFile):
    tree = ET.ElementTree()
    tree.parse(dbLocation + dbFile)

    albumDict = {}
    artistDict = {}
    songs = {}
    for f in tree.findall('file'):
        #adding songs to the song libs ( with tags ) with an 'int' id
        id = int(f.get('id'))
        songs[id] = {}
        songs[id]['id'] = id
        for element in f: 
            songs[id][element.tag] = element.text
        
        #check if tags exist if not, putting unknown default value
        if 'artist' in songs[id].keys():
            artist = songs[id]['artist']
        else:
            artist = config.defaultUnknown
        
        if 'album' in songs[id].keys():
            album = songs[id]['album']
        else:
            album = config.defaultUnknown

        #adding dict to the graph if not existing
        if artist not in artistDict.keys():
            artistDict[artist] = set()
        if album not in albumDict.keys():
            albumDict[album] = set()


        #creating two dictionaries : artist -> albums: album -> tracks
        artistDict[artist].add(album)
        albumDict[album].add(int(f.get('id')))

    log.info("Database loaded in memory")

    return (artistDict, albumDict, songs)

def make_neighbors(songs, tracks):
    """songs is the tag songs built up, songs is sth like graph[artist][album]"""
    
    #comparison function, used to sort tracks to make a decent playlist ( by artists/album/(track|name) )
    def comp(x, y):
        if songs[x]['artist'] > songs[y]['artist']:
            return +1
        elif songs[x]['artist'] < songs[y]['artist']:
            return -1
        else:
            if songs[x]['album'] > songs[y]['album']:
                return +1
            elif songs[x]['album'] < songs[y]['album']:
                return -1
            else:
                if 'tracknumber' in set(songs[x].keys()).intersection(set(songs[y].keys())) and songs[x]['tracknumber'] != songs[y]['tracknumber']:
                    if songs[x]['tracknumber'] > songs[y]['tracknumber']:
                        return +1
                    elif songs[x]['tracknumber'] < songs[y]['tracknumber']:
                        return -1
                    else:
                        return 0
                else:
                    if songs[x]['location'] > songs[y]['location']:
                        return +1
                    elif songs[x]['location'] < songs[y]['location']:
                        return -1
                    else:
                        return 0            

    playlist = list(tracks) #we have here a list of id's
    playlist.sort(comp) #we sort them
    
    return playlist
