from enum import Enum


class StepResultEnum(Enum):
	PASSED = 0
	FAILED = 1
	SKIPPED = 2
	ERROR = 3
	NOT_RUN = 4
	DONE = 5
