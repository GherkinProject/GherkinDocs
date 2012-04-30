import ConfigParser

class cfg_data:
	def __init__(self, fileName):
		self.fileName = fileName		
		self.config = ConfigParser.ConfigParser()

		#loading file				
		self.config.read(fileName)

		#================================================
		# Loading constants
		#================================================

		try:
			#extensions
			self.defaultFileExt = set(self.config.get('extension', 'file'))
			self.defaultTagKept = set(self.config.get('extension', 'tag'))
			self.defaultUnknown = self.config.get('extension', 'unk')

			#server port
			self.defaultPort = self.config.getint('server', 'port')
			self.serverName = self.config.get('server', 'name')

			#time
			self.dtDisplay = self.config.getfloat('time', 'display')
			self.dtCheck = self.config.getfloat('time', 'check')
			self.anticipateDisplay = self.config.getfloat('time', 'anticipateDisplay')
			self.anticipateCheck = self.config.getfloat('time', 'anticipateCheck')

			#constante mode
			self.normal = self.config.getint('constante','normal')
			self.random = self.config.getint('constante','random')
			self.playlist = self.config.getint('constante','playlist')
			self.keepPlaylist = self.config.getint('constante','keepPlaylist')

			# pruning constant
			self.epsilon = self.config.getfloat('pruning','constante')

			#icon and locations
			self.cfg = self.config.get('location','cfg')
			self.dbMarkov = self.config.get('location','Markov')
			self.iconLocation = self.config.get('location','pictures')
			self.logLocation = self.config.get('location','log')
			self.defaultDbLocation = self.config.get('location','DbLoc')
			self.defaultDbFile = self.config.get('location','DbFile')
			self.defaultDbFileImported = self.config.get('location','DbFileImported')
			self.playIcon = self.config.get('location', 'playIcon',0)
			self.pauseIcon = self.config.get('location', 'pauseIcon',0)
			self.nextIcon = self.config.get('location', 'nextIcon',0)
			self.prevIcon = self.config.get('location', 'prevIcon',0)
			self.randomOnIcon = self.config.get('location', 'randomOnIcon',0)
			self.randomOffIcon = self.config.get('location', 'randomOffIcon',0)
			self.repeatOnIcon = self.config.get('location', 'repeatOnIcon',0)
			self.repeatOffIcon = self.config.get('location', 'repeatOffIcon',0)
			self.gherkinIcon = self.config.get('location', 'gherkinIcon',0)
			self.playlistOffIcon = self.config.get('location', 'playlistOffIcon',0)
			self.playlistOnIcon = self.config.get('location', 'playlistOnIcon',0)
		except:
			#if no file was created, creates it
			self.reset()
			self.write()
			self.__init__(fileName)
		
	def reset(self):
		"""Reset Gherkin to Default configuration"""
		self.config.add_section('extension')
		self.config.set('extension', 'file', '{".mp3", ".ogg", ".flac"}')
		self.config.set('extension', 'tag', '{"artist", "album", "title", "date", "tracknumber", "genre"}')
		self.config.set('extension', 'unk', 'unknown')

		self.config.add_section('server')
		self.config.set('server', 'port', '1664')
		self.config.set('server', 'name', 'localhost')

		self.config.add_section('time')
		self.config.set('time', 'display', '0.2')
		self.config.set('time', 'check', '1.0')
		self.config.set('time', 'anticipateDisplay', '2.')
		self.config.set('time', 'anticipateCheck', '1.1')

		self.config.add_section('constante')
		self.config.set('constante', 'normal', '0')
		self.config.set('constante', 'random', '1')
		self.config.set('constante', 'playlist', '2')
		self.config.set('constante', 'keepPlaylist', '6')

		self.config.add_section('pruning')
		self.config.set('pruning', 'constante', '0.001')

		self.config.add_section('location')
		self.config.set('location', 'cfg', 'cfgData.cfg')
		self.config.set('location', 'Markov', 'dbMarkov.ghk')
		self.config.set('location', 'pictures', 'pictures/')
		self.config.set('location', 'log', 'log/')
		self.config.set('location', 'DbLoc', './')
		self.config.set('location', 'DbFile', 'db.xml')
		self.config.set('location', 'DbFileImported', 'dbImported.xml')
		self.config.set('location', 'playIcon', '%(pictures)splay.png')
		self.config.set('location', 'pauseIcon', '%(pictures)spause.png')
		self.config.set('location', 'nextIcon', '%(pictures)sforward.png')
		self.config.set('location', 'prevIcon', '%(pictures)sbackward.png')
		self.config.set('location', 'randomOnIcon', '%(pictures)srandom2.png')
		self.config.set('location', 'randomOffIcon', '%(pictures)srandom.png')
		self.config.set('location', 'repeatOnIcon', '%(pictures)srepeat2.png')
		self.config.set('location', 'repeatOffIcon', '%(pictures)srepeat.png')
		self.config.set('location', 'gherkinIcon', '%(pictures)sgherkin.xpm')
		self.config.set('location', 'playlistOffIcon', '%(pictures)splus.png')
		self.config.set('location', 'playlistOnIcon', '%(pictures)splus2.png')
    
    	def set(self, section, name, value):
        	"""Modify constant in file and in instance"""
            	self.config.set(section, name, value)
        	self.write()
        	self.__init__(self.fileName)

	def write(self):
	    """Write the actual configuration in the file "name" """
	    with open(self.fileName, 'wb') as configfile:
		self.config.write(configfile)

config = cfg_data('config.cfg')
