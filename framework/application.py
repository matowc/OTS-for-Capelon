from framework.station import Station
from sequences import *
import logging
import configparser
from datetime import datetime
import sys

logging.basicConfig(level=logging.DEBUG, format='%(asctime)-15s | %(message)s',
					handlers=[
						logging.FileHandler(datetime.now().strftime('events_%Y_%m_%d.log')),
						logging.StreamHandler(sys.stdout)])


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Application(metaclass=Singleton):

	def __init__(self, configFilepath, hardwareConfigurationFilepath):
		self.eventLogger = None  # EventLogger
		self.resultLogger = None  # ResultLogger
		self.station = Station()
		self.database = None  # Database
		self.testThread = None
		self.test = None
		self.batch = None
		self.sequences = {
			'OLC NEMA PP - full test': FullTest
		}
		self.users = {
			'mateusz': {
				'name':     'Mateusz Owczarek',
				'password': 'mateusz'
			}
		}
		self.loggedUser = None
		self.reportsPath = 'reports/'
		self._configFilepath = configFilepath
		self.hardwareConfigFilepath = hardwareConfigurationFilepath
		self.config = self.loadConfigFromFile()

		self.autologin()

	def launch(self):
		# returns
		pass

	def autologin(self):
		if self.config['general']['autologin'] == 'true' and self.config['general']['autologinUser'] and self.users[self.config['general']['autologinUser']]:
			self.loggedUser = self.config['general']['autologinUser']


	def loadConfigFromFile(self):
		config = configparser.ConfigParser()
		config.read(self._configFilepath)
		logging.debug('Setttings file: {}'.format(self._configFilepath))
		return config


	def login(self, user, password):
		for login, data in self.users.items():
			if login == user and data['password'] == password:
				self.loggedUser = login
				logging.info('User \'{}\' ({}) logged in'.format(login, data['name']))
				if self.config['general']['autologin'] == 'true':
					config = configparser.ConfigParser()
					config['general']['autologinUser'] = self.loggedUser
					with open(self._configFilepath, 'w') as configfile:
						config.write(configfile)
				return data
		return None

	def logout(self):
		logging.info('User \'{}\' ({}) logged out'.format(self.loggedUser, self.users[self.loggedUser]))
		self.loggedUser = None


def main():
	pass


if __name__ == "__main__": main()
