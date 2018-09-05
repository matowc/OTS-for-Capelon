from framework.station import Station
from sequences import *
import logging
import configparser


class Application:

	def __init__(self, configFilepath):
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
		config = configparser.ConfigParser()
		config.read(configFilepath)
		logging.debug('Setttings file: {}'.format(configFilepath))
		self._configFilepath = configFilepath
		self.config = config
		if config['general']['autologin'] == 'true' and config['general']['autologinUser'] and self.users[config['general']['autologinUser']]:
			self.loggedUser = config['general']['autologinUser']

	def launch(self):
		# returns
		pass

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
