#file for constant definition

#list of working extensions :
defaultFileExt = {".mp3", ".ogg", ".flac"}
defaultTagKept = {"artist", "album", "title", "date", "tracknumber", "genre"}
defaultUnknown = 'unknown'

#server port
defaultPort = 1664
serverName = "10.204.200.200"


#time
dtDisplay = 0.2
dtCheck = 1. 
anticipateDisplay = 2.
anticipateCheck = 1.1

#constante mode
normal = 0
random = 1
playlist = 2

# pruning constant
epsilon = 0.001

#icon and locations
dbMarkov = "dbMarkov.ghk"
iconLocation = "pictures/"
logLocation = "log/"
defaultDbLocation = "./"
defaultDbFile = "db.xml"
defaultDbFileImported = "dbImported.xml"
playIcon = iconLocation + "play.png"
pauseIcon = iconLocation + "pause.png"
nextIcon = iconLocation + "forward.png"
prevIcon = iconLocation + "backward.png"
randomOnIcon = iconLocation + "random3.png"
randomOffIcon = iconLocation + "random.png"
repeatOnIcon = iconLocation + "repeat3.png"
repeatOffIcon = iconLocation + "repeat.png"
gherkinIcon = iconLocation + "gherkin.png"
playlistOffIcon = iconLocation + "plus.png"
playlistOnIcon = iconLocation + "plus2.png"
