import logging
from framework import *
from framework.result import *


class ResultList:

	def __init__(self) :
		self.results = []
		self.sequence = None

	def bindSequence(self, sequence):
		self.sequence = sequence
	
	def add (self, result: Result):

		if(result in self.results):
			for i, r in enumerate(self.results):
				if (id(r.step) == id(step)):
					self.results[i] = result
		else:
			self.results.append(result)

	def clear(self):
		self.results = []
		logging.info("Result list cleared")

def main():
	pass


if __name__ == "__main__" : main()