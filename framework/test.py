import logging
from framework import *
from framework.result_list import *


class Test:
	
	def __init__(self, sequence: Sequence, resultList: ResultList):
		self.sequence = sequence
		self.resultList = resultList
		pass
	
	def run(self):
		
		self.sequence.pre()
		self.sequence.main()
		self.sequence.post()


def main():
	pass

if __name__ == "__main__" : main()