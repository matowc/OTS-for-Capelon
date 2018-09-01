import logging
from enum import Enum
from framework import *
from framework.sequence import Sequence
from framework.step_type_enum import *
from framework.step_result_enum import *
from framework.result import Result


class Step:
	
	def __init__(self, name=None, type: StepTypeEnum=None, limits=None):
		self.name = name
		self.type = type
		self.limits = limits
		pass
	
	def evaluate(self, sequence:Sequence, value, resultList):
		status = StepResultEnum.NOT_RUN


		
		if self.type == StepTypeEnum.NUMERIC:
			[LL, HL] = map(float, self.limits.split(':',2))
			if value >= LL and value <= HL:
				status = StepResultEnum.PASSED
			else:
				status = StepResultEnum.FAILED
		
		elif self.type == StepTypeEnum.BOOL:
			if value == True:
				status = StepResultEnum.PASSED
			else:
				status = StepResultEnum.FAILED
			self.limits = ''

		elif self.type == StepTypeEnum.ACTION:
			status = StepResultEnum.DONE
			self.limits = ''

		result = Result(self, value, status)
		result.post(sequence)
		resultList.add(result)
		sequence.postStep(result) # has to be after the result list is update, because otherwise FAIL result will break the sequence (throw exception)and will not display on the list

def main():
	pass
	
if __name__ == "__main__": main()

