from load_db import *
from ghk_server import *

songs = get_lib()

s = server()
s.load(songs[-1]['location'])
print s.playing
s.play_pause()
print s.playing

while s.playing:
    pass
