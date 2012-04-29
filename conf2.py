import ConfigParser

class cfgData():
	def attribution(self, config):
		self.defaultFileExt = set(config.get('extension', 'file'))
		self.defaultTagKept = set(config.get('extension', 'tag'))
		self.defaultUnknown = config.get('extension', 'unk')


		#server port
		self.defaultPort = config.getint('server', 'port')
		self.serverName = config.get('server', 'name')

		#time
		self.dtDisplay = config.getfloat('time', 'display')
		self.dtCheck = config.getfloat('time', 'check')
		self.anticipateDisplay = config.getfloat('time', 'anticipateDisplay')
		self.anticipateCheck = config.getfloat('time', 'anticipateCheck')

	
	

		#constante mode
		self.normal = config.getint('constante','normal')
		self.random = config.getint('constante','random')
		self.playlist = config.getint('constante','playlist')
		self.keepPlaylist = config.getint('constante','keepPlaylist')



		# pruning constant
		self.epsilon = config.getfloat('pruning','constante')

		#icon and locations
		self.dbMarkov = config.get('location','Markov')
		self.iconLocation = config.get('location','pictures')
		self.logLocation = config.get('location','log')
		self.defaultDbLocation = config.get('location','DbLoc')
		self.defaultDbFile = config.get('location','DbFile')
		self.defaultDbFileImported = config.get('location','DbFileImported')
		self.playIcon = config.get('location', 'playIcon',0)
		self.pauseIcon = config.get('location', 'pauseIcon',0)
		self.nextIcon = config.get('location', 'nextIcon',0)
		self.prevIcon = config.get('location', 'prevIcon',0)
		self.randomOnIcon = config.get('location', 'randomOnIcon',0)
		self.randomOffIcon = config.get('location', 'randomOffIcon',0)
		self.repeatOnIcon = config.get('location', 'repeatOnIcon',0)
		self.repeatOffIcon = config.get('location', 'repeatOffIcon',0)
		self.gherkinIcon = config.get('location', 'gherkinIcon',0)
		self.playlistOffIcon = config.get('location', 'playlistOffIcon',0)
		self.playlistOnIcon = config.get('location', 'playlistOnIcon',0)
	def make_from_data(self, name):
		config = read_config(name)
		self = make_config(config)
		



def default(config):
	"""Default configuration for Gherkin"""
	config.add_section('extension')
	config.set('extension', 'file', '{".mp3", ".ogg", ".flac"}')
	config.set('extension', 'tag', '{"artist", "album", "title", "date", "tracknumber", "genre"}')
	config.set('extension', 'unk', 'unknown')

	config.add_section('server')
	config.set('server', 'port', '1664')
	config.set('server', 'name', 'localhost')

	config.add_section('time')
	config.set('time', 'display', '0.2')
	config.set('time', 'check', '1.0')
	config.set('time', 'anticipateDisplay', '2.')
	config.set('time', 'anticipateCheck', '1.1')

	config.add_section('constante')
	config.set('constante', 'normal', '0')
	config.set('constante', 'random', '1')
	config.set('constante', 'playlist', '2')
	config.set('constante', 'keepPlaylist', '6')

	config.add_section('pruning')
	config.set('pruning', 'constante', '0.001')

	config.add_section('location')
	config.set('location', 'Markov', 'dbMarkov.ghk')
	config.set('location', 'pictures', 'pictures/')
	config.set('location', 'log', 'log/')
	config.set('location', 'DbLoc', './')
	config.set('location', 'DbFile', 'db.xml')
	config.set('location', 'DbFileImported', 'dbImported.xml')
	config.set('location', 'playIcon', '%(pictures)s play.png')
	config.set('location', 'pauseIcon', '%(pictures)s pause.png')
	config.set('location', 'nextIcon', '%(pictures)s forward.png')
	config.set('location', 'prevIcon', '%(pictures)sbackward.png')
	config.set('location', 'randomOnIcon', '%(pictures)srandom2.png')
	config.set('location', 'randomOffIcon', '%(pictures)srandom.png')
	config.set('location', 'repeatOnIcon', '%(pictures)srepeat2.png')
	config.set('location', 'repeatOffIcon', '%(pictures)srepeat.png')
	config.set('location', 'gherkinIcon', '%(pictures)sgherkin.xpm')
	config.set('location', 'playlistOffIcon', '%(pictures)splus.png')
	config.set('location', 'playlistOnIcon', '%(pictures)splus2.png')



def write_config(config, name):
    """Write the actual configuration in the file "name" """
    with open(name, 'wb') as configfile:
        config.write(configfile)

def read_config(name):
    """ Read the configuration file and store it into config."""
    config = ConfigParser.ConfigParser()
    config.read(name)
    # print config.get('location', 'Markov') # Normal mode
    # print config.get('location', 'playlistOnIcon', 0) #Interpolation
    return config

def make_config(config):
	""" Create a cfgData and give it the constant written in the config """
	cfg = cfgData()
	cfg.attribution(config)
	return cfg


