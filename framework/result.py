import logging
from framework import *
from framework.step_result_enum import StepResultEnum
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
	
	def post(self, sequence: Sequence):
		self.timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S.%f')
		logging.info("{:^10} {:>30} = {:10} {:20} {:>20}".format("("+self.step.type.name+")", self.step.name, str(self.value), "("+str(self.step.limits)+")", "["+self.timestamp+"]"))
		
		if self.status == StepResultEnum.PASSED:
			sequence.onPass(self)
		elif self.status == StepResultEnum.FAILED:
			sequence.onFail(self)
		elif self.status == StepResultEnum.ERROR:
			sequence.onError(self)


def main():
	pass

if __name__ == "__main__" : main()