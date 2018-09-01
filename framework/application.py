from framework.station import Station
from sequences import *


class Application:
	
	def __init__(self) :
		self.eventLogger = None # EventLogger
		self.resultLogger = None # ResultLogger
		self.station = Station()
		self.database = None # Database
		self.testThread = None
		self.test = None
		self.sequences = {
			'OLC NEMA PP - full test':	FullTest
		}
		pass
	
	def launch (self) :
		# returns
		pass


def main():
	pass

if __name__ == "__main__" : main()