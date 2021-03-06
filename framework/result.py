import logging
from framework import *
from framework.step_result_enum import StepResultEnum
from framework.sequence_result_enum import SequenceStatusEnum
from framework.sequence import Sequence

import time
import datetime

class Result:
	
	def __init__(self, step=None, value=None, status: StepResultEnum=StepResultEnum.NOT_RUN, socket=None) :
		self.step = step
		self.socket = socket
		self.status = status
		self.value = value
		self.timestamp = None
		self.relativeTimestamp = None

	def post(self, sequence: Sequence):
		currentTime = time.time()
		self.timestamp = datetime.datetime.fromtimestamp(currentTime).strftime('%H:%M:%S.%f')
		self.relativeTimestamp = currentTime - sequence.startTime

		logging.info("Step \'{}\' = {} {}".format(self.step.name, str(self.value), "("+str(self.step.limits)+")"))
		
		if not sequence.status == SequenceStatusEnum.TERMINATED:
			if self.status == StepResultEnum.PASSED:
				sequence.onPass(self)
			elif self.status == StepResultEnum.FAILED:
				sequence.onFail(self)
			elif self.status == StepResultEnum.ERROR:
				sequence.onError(self)


def main():
	pass

if __name__ == "__main__" : main()