#client lib
import xmlrpclib

#local lib : loading db
from load_db import ient lib
import xmlrpclib

#local lib : loading db
from load_db import *

#config file
import config

#to sleep a little, cause i'm tired
import time

#to add the db-tools
import sys
sys.path.append("../db-tools/")

#########
#Warning#
#########
#You NEED to launch server before doing this :
# $ python ghk_server.py ( in one terminal, it won't give you the shell back as it is running as a deamon )
# THEN open a NEW shell without killing the server and execute the following commands

#getting in touch with server
s = xmlrpclib.ServerProxy("http://localhost:" + str(config.defaultPort))

#just tu show what commands are available
print s.system.listMethods()

#getting list of songs
songs = get_lib()

#loading song into the server
s.load(songs[-1]['location'])

#playing song
s.play_pause()

sleep(2)

s.get_duration()

s.get_position()


#config file
import config

from time import *

#########
#Warning#
#########
#You NEED to launch server before doing this :
# $ python ghk_server.py ( in one terminal, it won't give you the shell back as it is running as a deamon )
# THEN open a NEW shell without killing the server and execute the following commands

#getting in touch with server
s = xmlrpclib.ServerProxy("http://localhost:" + str(config.defaultPort))

#just tu show what commands are available
print s.system.listMethods()

#getting list of songs
songs = get_lib()

#loading song into the server
s.load(songs[-1]['location'])

#playing song
s.play_pause()

sleep(2)

s.get_duration()

s.get_position()
