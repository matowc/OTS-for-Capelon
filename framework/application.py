from framework.station import Station
from sequences import *
import logging
import configparser
from datetime import datetime
import sys
import csv

logging.basicConfig(level=logging.DEBUG, format='%(asctime)-15s | %(message)s',
					handlers=[
						logging.FileHandler(datetime.now().strftime('logs/events_%Y_%m_%d.log')),
						logging.StreamHandler(sys.stdout)])


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Application(metaclass=Singleton):

	def __init__(self, configFilepath, hardwareConfigurationFilepath, usersFilepath):
		self.eventLogger = None  # EventLogger
		self.resultLogger = None  # ResultLogger
		self.station = Station()
		self.database = None  # Database
		self.testThread = None
		self.test = None
		self.batch = None
		self.sequences = {
			'OLC NEMA PP - full test (auto)': {
				'sequence': FullTest,
				'stepsFilepath': 'sequences/full_test.csv',
				'configFilepath': 'sequences/full_test.ini'
			},
			'OLC NEMA PP - full test (manual)': {
				'sequence': FullTest,
				'stepsFilepath': 'sequences/full_test.csv',
				'configFilepath': 'sequences/full_test_manual.ini'
			},
			'Programming only': {
				'sequence': ProgrammingOnly,
				'stepsFilepath': 'sequences/programming_only.csv',
				'configFilepath': 'sequences/programming_only.ini'
			},

		}
		self.usersFilepath = usersFilepath
		self.users = {}
		self.loadUsersFromFile()
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
		try:
			if self.config['general']['autologin'] == 'true' and self.config['general']['autologinUser'] and self.users[self.config['general']['autologinUser']]:
				self.loggedUser = self.config['general']['autologinUser']
		except KeyError:
			pass

	def loadConfigFromFile(self):
		config = configparser.ConfigParser()
		config.read(self._configFilepath)
		logging.debug('Settings file: {}'.format(self._configFilepath))
		return config

	def loadUsersFromFile(self):
		with open(self.usersFilepath, 'r') as f:
			reader = csv.reader(f, delimiter=';')
			for row in reader:
				login = row[0]
				displayName = row[1]
				passwordHash = row[2]
				self.users[login] = {
					'name': displayName,
					'passwordHash': passwordHash
				}

	def login(self, user, password):
		import hashlib
		for login, data in self.users.items():
			if login == user and data['passwordHash'] == hashlib.sha1(password.encode('utf-8')).hexdigest():
				self.loggedUser = login
				logging.info('User \'{}\' ({}) logged in'.format(login, data['name']))
				if self.config['general']['autologin'] == 'true':
					self.config['general']['autologinUser'] = self.loggedUser
					with open(self._configFilepath, 'w') as configfile:
						self.config.write(configfile)
				return data
		return None

	def logout(self):
		logging.info('User \'{}\' ({}) logged out'.format(self.loggedUser, self.users[self.loggedUser]))
		self.loggedUser = ''
		self.config['general']['autologinUser'] = self.loggedUser
		with open(self._configFilepath, 'w') as configfile:
			self.config.write(configfile)


def main():
	pass


if __name__ == "__main__": main()
