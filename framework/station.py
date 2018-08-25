from typing import Dict

from drivers.driver import Driver


class Station:
	
	def __init__(self) :
		self.drivers = {} # Driver
		self.config = {} # string
		pass
	
	def addDriver(self, driver: Driver):
		self.drivers[driver.name] = driver
		


def main():
	pass

if __name__ == "__main__" : main()
		
		