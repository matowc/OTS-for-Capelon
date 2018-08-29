from typing import Dict
import logging

from drivers.driver import Driver


class Station:
	
	def __init__(self) :
		self.drivers = {} # Driver
		self.config = {} # string
		pass
	
	def addDriver(self, driver: Driver):
		self.drivers[driver.name] = driver

		logging.info("Driver %s added to station", driver.name)
		


def main():
	pass

if __name__ == "__main__" : main()
		
		