import logging
from framework import *
from framework.result_list import *
import time
import threading

class Test:
	
	def __init__(self, sequence: Sequence, resultList: ResultList):
		self.sequence = sequence
		self.resultList = resultList
	
	def run(self):
		self.resultList.clear()
		self.sequence.pre()
		self.sequence.main()
		self.sequence.post()
		self.sequence.final()


def main():
	pass

if __name__ == "__main__" : main()