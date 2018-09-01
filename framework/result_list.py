import logging
from framework import *
from framework.result import *


class ResultList:



	def __init__(self) :
		self.results = []
	
	def add (self, result: Result):

		if(result in self.results):
			for i, r in enumerate(self.results):
				if (r.step.name == result.step.name):
					self.results[i] = result
		else:
			self.results.append(result)

	def clear(self):
		self.results = []

def main():
	pass


if __name__ == "__main__" : main()