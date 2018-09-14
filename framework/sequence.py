import logging
import configparser
from exceptions.step_fail import StepFail
from framework.sequence_result_enum import *
from exceptions.step_fail import *
import time
import threading
import csv
from framework.step_type_enum import StepTypeEnum
from collections import OrderedDict



class Sequence:
	def __init__(self, station, name, resultList, gui=None, stepsFilepath=None, configFilepath=None):
		self._station = station
		self.name = name
		self._resultList = resultList
		self._gui = gui
		self.status = SequenceStatusEnum.NOT_RUN
		self.startTime = None
		self.endTime = None
		self.steps = OrderedDict()
		self.deviceId = ''
		self.steps = {}
		self._stepsFilepath = stepsFilepath
		self._configFilepath = configFilepath

		if stepsFilepath:
			self.loadStepsFromFile()

		self._config = {}
		if configFilepath:
			self._config = self.loadConfigFromFile()


	def evaluateStep(self, stepName: str, value):
		return self.steps[stepName].evaluate(self, value, self._resultList)

	def updateTimer(self):
		if self._gui:
			self._gui.updateTestTime(time.time() - self.startTime)
			if self.status == SequenceStatusEnum.RUNNING:
				threading.Timer(1, self.updateTimer).start()

	def loadStepsFromFile(self):
		with open(self._stepsFilepath, 'r') as f:
			reader = csv.reader(f, delimiter=';')
			for row in reader:
				name = row[0]
				displayName = row[1]
				displayMode = row[2].lower() == 'true'
				type = row[3]
				try:
					limits = row[4]
				except IndexError:
					limits = ''
				from framework.step import Step
				self.steps[name] = Step(name, displayName, displayMode, StepTypeEnum[type], limits)

	def loadConfigFromFile(self):
		config = configparser.ConfigParser()
		config.read(self._configFilepath)
		logging.debug('Sequence settings file: {}'.format(self._configFilepath))
		return config

	def pre(self):
		self.startTime = time.time()
		self.status = SequenceStatusEnum.RUNNING
		self.updateTimer()

		if self._gui:
			self._gui.updateTestStatus("Sequence pre-actions in progress...", "light grey", True)
		logging.info("Pre-sequence actions completed")

	def main(self):
		if self._gui:
			self._gui.updateTestStatus("Test in progress...", self._gui.colors['light grey'], True)

	def post(self):
		if self._gui:
			self._gui.updateTestStatus("Sequence post-actions in progress...", self._gui.colors['light grey'], True)
		logging.info("Post-sequence actions completed")

	def final(self):
		self.endTime = time.time()
		if self.status in [SequenceStatusEnum.RUNNING, SequenceStatusEnum.DONE]:
			self.status = SequenceStatusEnum.PASSED
		if self._gui:
			if self.status == SequenceStatusEnum.PASSED:
				self._gui.updateTestStatus("TEST PASSED", self._gui.colors['green'])
				self._gui.incrementPassedStatistics()
			elif self.status == SequenceStatusEnum.FAILED:
				self._gui.updateTestStatus("TEST FAILED", self._gui.colors['red'])
				self._gui.incrementFailedStatistics()
			elif self.status == SequenceStatusEnum.ERROR:
				self._gui.updateTestStatus("SEQUENCE TERMINATED WITH ERROR", self._gui.colors['red'])
				self._gui.incrementFailedStatistics()
			elif self.status == SequenceStatusEnum.TERMINATED:
				self._gui.updateTestStatus("SEQUENCE TERMINATED", self._gui.colors['red'])
				self._gui.incrementFailedStatistics()
			else:
				self._gui.updateTestStatus("UNKNOWN ERROR", self._gui.colors['red'])
				self._gui.incrementFailedStatistics()

			self._gui.displaySequenceChoice()
		logging.info("Test completed with result {}".format(self.status.name))

	def postStep(self, result):
		if self.status == SequenceStatusEnum.TERMINATED:
			raise QuitEvent

	def pingStatus(self):
		if self.status == SequenceStatusEnum.TERMINATED:
			raise QuitEvent

	def onFail(self, result):
		if self.status != SequenceStatusEnum.TERMINATED:
			logging.info("Step \'{}\' FAILED".format(result.step.name))
			self.status = SequenceStatusEnum.FAILED
			raise StepFail

	def onPass(self, result):
		if self.status != SequenceStatusEnum.TERMINATED:
			pass

	def onError(self, result):
		if self.status != SequenceStatusEnum.TERMINATED:
			self.status = SequenceStatusEnum.ERROR

	def displayCustomMessage(self, type, displayText):
		if self._gui:
			self._gui.displayCustomMessage(type, displayText)

	def displayMemo(self, displayText):
		if self._gui:
			self._gui.displayMemo(displayText)

	def clearCustomMessage(self):
		if self._gui:
			self._gui.displayCustomMessage('', '')

	def requestTerminate(self):
		self.status = SequenceStatusEnum.TERMINATED

	def requestTerminateOnError(self):
		self.status = SequenceStatusEnum.ERROR

def main():
	pass

if __name__ == "__main__": main()
