import logging
import configparser


class Driver:

	def __init__(self, name, configFilepath=None):
		self.name = name
		self._configFilepath = configFilepath
		self.config = self.loadConfiguration()
		self.initialize()

		logging.info("Driver \'{}\' initialized".format(self.name))

	def __del__(self):
		self.deinitialize()

	def initialize(self):
		pass

	def deinitialize(self):
		pass

	def loadConfiguration(self):
		return self.loadConfigFromFile()

	def loadConfigFromFile(self):
		if self._configFilepath:
			config = configparser.ConfigParser()
			config.read(self._configFilepath)
			logging.debug('Driver {} settings file: {}'.format(self.name, self._configFilepath))
			return config[self.name]

	def safeReset(self):
		pass


def main():
	pass

if __name__ == "__main__" : main()