import logging
from exceptions.step_fail import StepFail
from framework.sequence_result_enum import *
from exceptions.step_fail import *

class Sequence:
	
	def __init__(self, station, name, resultList, gui=None):
		self._station = station
		self.name = name
		self._resultList = resultList
		self._gui = gui
		self.status = SequenceStatusEnum.NOT_RUN
	
	def evaluateStep(self, stepName:str, value):
		return self.steps[stepName].evaluate(self, value, self._resultList)
	
	def pre (self) :
		self.status = SequenceStatusEnum.RUNNING
		if self._gui:
			self._gui.updateTestStatus("Sequence pre-actions in progress...", "orange")
		# returns
		pass
	
	def main (self) :
		if self._gui:
			self._gui.updateTestStatus("Test in progress...", 'yellow')

		pass
	
	def post (self) :
		if self._gui:
			self._gui.updateTestStatus("Sequence post-actions in progress...", 'orange')
		# returns
		pass

	def final(self):
		if self.status == SequenceStatusEnum.RUNNING:
			self.status = SequenceStatusEnum.PASSED
		if self._gui:
			if self.status == SequenceStatusEnum.PASSED:
				self._gui.updateTestStatus("TEST PASSED", 'green')
			elif self.status == SequenceStatusEnum.FAILED:
				self._gui.updateTestStatus("TEST FAILED", 'red')
			elif self.status == SequenceStatusEnum.ERROR:
				self._gui.updateTestStatus("TEST FINISHED WITH ERROR", 'red')
			else:
				self._gui.updateTestStatus("UNKNOWN ERROR", 'red')

			self._gui.displaySequenceChoice()

	def postStep(self, result):
		if self.status == SequenceStatusEnum.TERMINATING:
			raise QuitEvent

	def onFail (self, result):
		logging.info("Step {} FAILED".format(result.step.name))
		self.status = SequenceStatusEnum.FAILED
	
	def onPass (self ,result):
		pass
	
	def onError (self, result):
		self.status = SequenceStatusEnum.ERROR

	def displayCustomMessage(self, type, displayText):
		if self._gui:
			self._gui.displayCustomMessage(type, displayText)

	def clearCustomMessage(self):
		if self._gui:
			self._gui.displayCustomMessage('', '')

	def requestTerminate(self):
		self.status = SequenceStatusEnum.TERMINATING
	


def main():
	pass

if __name__ == "__main__" : main()