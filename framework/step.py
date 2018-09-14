import logging
from enum import Enum
from framework import *
from framework.sequence import Sequence
from framework.step_type_enum import *
from framework.step_result_enum import *
from framework.result import Result


class Step:
	
	def __init__(self, name=None, displayName=None, displayMode=False, type: StepTypeEnum=None, limits=None):
		self.name = name
		self.displayName = displayName
		self.displayMode = displayMode
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
			if (self.limits and str(value).lower() == str(self.limits).lower()) or (not self.limits and value == True):
				status = StepResultEnum.PASSED
			else:
				status = StepResultEnum.FAILED
			self.limits = ''

		elif self.type == StepTypeEnum.ACTION:
			status = StepResultEnum.DONE
			self.limits = ''

		try:
			result = Result(self, value, status)
			result.post(sequence) #onFail, onPass, onError actions
			sequence.postStep(result) #postStep action
		except Exception:
			raise
		finally:
			resultList.add(result)

		return status == StepResultEnum.PASSED or self.type == StepTypeEnum.ACTION


def main():
	pass
	
if __name__ == "__main__": main()

