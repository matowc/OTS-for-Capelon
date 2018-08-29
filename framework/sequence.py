import logging
from exceptions.step_fail import StepFail

class Sequence:
	
	def __init__(self, station, name, resultList) :
		self._station = station
		self.name = name
		self._resultList = resultList
		pass
	
	def evaluateStep(self, stepName:str, value):
		return self.steps[stepName].evaluate(self, value, self._resultList)
	
	def pre (self) :
		# returns
		pass
	
	def main (self) :
		# returns
		pass
	
	def post (self) :
		# returns
		pass
	
	def onFail (self, result):
		logging.info("Step {} FAILED".format(result.step.name))
		raise StepFail()
		# returns
		pass
	
	def onPass (self ,result):
		# returns
		pass
	
	def onError (self, result):
		# returns
		pass
	


def main():
	pass

if __name__ == "__main__" : main()