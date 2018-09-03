from framework.station import Station
from sequences import *
import logging


class Application:

    def __init__(self):
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
                'name': 'Mateusz Owczarek',
                'password': 'mateusz'
            }
        }
        self.loggedUser = None

    def launch(self):
        # returns
        pass

    def login(self, user, password):
        for login, data in self.users.items():
            if login == user and data['password'] == password:
                self.loggedUser = login
                logging.info('User \'{}\' ({}) logged in'.format(login, data['name']))
                return data
        return None

    def logout(self):
        logging.info('User \'{}\' ({}) logged out'.format(self.loggedUser, self.users[self.loggedUser]))
        self.loggedUser = None


def main():
    pass


if __name__ == "__main__": main()