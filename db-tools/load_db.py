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
    
    graph = {}
    songs = {}
    for f in tree.findall('file'):
        #adding songs to the song libs ( with tags )
        id = int(f.get('id'))
        songs[id] = {}
        songs[id]['id'] = id
        for element in f: 
               songs[id][element.tag] = element.text 
        
        #adding songs to the graph ( for next/prev and display )
        
        #check if tags exist
        if 'artist' in f:
            artist = f['artist']
        else:
            artist = config.defaultUnknown
        
        if 'album' in f:
            album = f['album']
        else:
            album = config.defaultUnknown

        #adding dict to the graph if not existing
        if artist not in graph:
            graph[artist] = {}
        if album not in graph[artist]:
            graph[artist][album] = {} 


        #adding id of the song to the graph
        graph[artist][album][f.get('id')] = []

        #first element : id of previous
        #second element : dict ( id : proba )
    
    return (graph, songs)

def make_neighbors(lib, songs):
    """lib is the tag lib built up, songs is sth like graph[artist][album]"""
    
    def comp(x, y):
        if 'tracknumber' in set(lib[x].keys()).intersect(set(lib[y].keys())):
            if lib[x]['tracknumber'] > lib[y]['tracknumber']:
                return -1
            elif lib[x]['tracknumber'] < lib[y]['tracknumber']:
                return +1
            else:
                return 0
 
    l = [songs.keys()]
    l.sort(comp)
    
    #convention : first element : previous to play; second element, dict of to-play elements giving their proba

    for i in xrange(len(l)):
        songs[l[i]][1] = {}
        try:
            songs[l[i]][1][l[i+1]] = 1
        except:
            pass #it is the last element
        try:
            songs[l[i]][0] = l[i-1]
        except:
            pass #it is the first element

    return songs
