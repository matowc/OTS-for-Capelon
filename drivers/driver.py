import logging


class Driver:

	def __init__(self, name):
		self.name = name
		self.loadConfiguration()
		self.initialize()

	def __del__(self):
		self.deinitialize()

	def initialize(self):
		pass

	def deinitalize(self):
		pass

	def loadConfiguration(self):
		pass

	def safeReset(self):
		pass


def main():
	pass

if __name__ == "__main__" : main()