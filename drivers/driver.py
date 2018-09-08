import logging


class Driver:

	def __init__(self, name, configFilepath=None):
		self.name = name
		self._configFilePath = configFilepath
		self.config = self.loadConfiguration()
		self.initialize()

		logging.info("Driver \'{}\' initialized".format(self.name))

	def __del__(self):
		self.deinitialize()

	def initialize(self):
		pass

	def deinitalize(self):
		pass

	def loadConfiguration(self):
		return self.loadConfigFromFile()

	def loadConfigFromFile(self):
		if self._configFilePath:
			config = configparser.ConfigParser()
			config.read(self._configFilepath)
			logging.debug('Driver {} settings file: {}'.format(self.name, self._configFilepath))
			return config[self.name]

	def safeReset(self):
		pass


def main():
	pass

if __name__ == "__main__" : main()