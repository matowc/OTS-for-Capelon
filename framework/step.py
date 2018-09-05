import logging
from enum import Enum
from framework import *
from framework.sequence import Sequence
from framework.step_type_enum import *
from framework.step_result_enum import *
from framework.result import Result


class Step:
	
	def __init__(self, name=None, displayName=None, type: StepTypeEnum=None, limits=None):
		self.name = name
		self.displayName = displayName
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

		try:
			result = Result(self, value, status)
			sequence.postStep(result)
			result.post(sequence)
		except Exception:
			raise
		finally:
			resultList.add(result)


def main():
	pass
	
if __name__ == "__main__": main()

