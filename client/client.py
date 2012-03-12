# -*- coding: utf-8 -*-
#!/usr/bin/python -d

#config constant
import config

#script with arguments
import sys

#client lib for calling server
import xmlrpclib


def give_time(u):
    if u % 60 < 10:
        return str(u // 60) + ":" + "0" + str(u % 60)
    else:
        return str(u // 60) + ":" + str(u % 60)

class client:
    def __init__(self):
        try:
            self.server = xmlrpclib.ServerProxy("http://" + config.serverName + ":" + str(config.defaultPort))
        except:
            assert False, "Server not launched !"
 
    
    def cmd(self, cmd):
        if cmd in "play" or cmd in "pause":
            self.server.play_pause()
        if cmd in "next":
            self.server.next()
        if cmd in "previous":
            self.server.prev()
        if cmd in "state" or cmd in "display":
            r = ""
            if self.server.is_playing():
                r = r + "> "
            else:
                r = r + "|| "
            
            r = r + self.server.get_name() + " " + give_time(self.server.get_position()) + "/" + give_time(self.server.get_duration()) + " "

            if self.server.get_mode() == config.playlist:
                r = r + "ghk mode"

            print r
        
        if cmd in "repeat":
            self.server.repeat()

        if cmd in "ghk" or cmd in "unghk":
            self.server.mode_playlist()

c = client()
#applying command
c.cmd(sys.argv[1])
