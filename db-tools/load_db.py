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
        #adding songs to the song libs ( with tags )
        id = int(f.get('id'))
        songs[id] = {}
        songs[id]['id'] = id
        for element in f: 
            songs[id][element.tag] = element.text
        songs[id]["next"] = {}
        
        #adding songs to the graph ( for next/prev and display )
        
        #check if tags exist
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


        #adding id of the song to the graph
        artistDict[artist].add(album)
        albumDict[album].add(int(f.get('id')))

        #first element : id of previous
        #second element : dict ( id : proba )
    log.info("Database loaded in memeory")

    return (artistDict, albumDict, songs)

def make_neighbors(songs, tracks):
    """songs is the tag songs built up, songs is sth like graph[artist][album]"""
    
    def comp(x, y):
        if 'artist' in set(songs[x].keys()).intersection(set(songs[y].keys())):
            if songs[x]['artist'] > songs[y]['artist']:
                return -1
            elif songs[x]['artist'] < songs[y]['artist']:
                return +1
            else:
                if 'album' in set(songs[x].keys()).intersection(set(songs[y].keys())):
                    if songs[x]['album'] > songs[y]['album']:
                        return -1
                    elif songs[x]['album'] < songs[y]['album']:
                        return +1
                    else:
                        if 'tracknumber' in set(songs[x].keys()).intersection(set(songs[y].keys())):
                            if songs[x]['tracknumber'] > songs[y]['tracknumber']:
                                return -1
                            elif songs[x]['tracknumber'] < songs[y]['tracknumber']:
                                return +1
                            else:
                                return 0
                        elif 'title' in set(songs[x].keys()).intersection(set(songs[y].keys())):
                            if songs[x]['title'] > songs[y]['title']:
                                return -1
                            elif songs[x]['title'] < songs[y]['title']:
                                return +1
                            else:
                                return 0
                        else:    
                            if songs[x]['location'] > songs[y]['location']:
                                return -1
                            elif songs[x]['location'] < songs[y]['location']:
                                return +1
                            else:
                                return 0            

    l = list(tracks) #we have here a list of id's
    l.sort(comp) #we sort them
    
    #convention : first element : previous to play; second element, dict of to-play elements giving their proba
    
    return l

#    for i in xrange(len(l)):
#        try:
#            songs[l[i]]["prev"] = l[i-1]
#        except:
#            pass #it is the first element
#        try:
#            songs[l[i]]["next"][l[i+1]] = 1
#        except:
#            pass #it is the last element
