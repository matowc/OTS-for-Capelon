from enum import Enum


class SequenceStatusEnum(Enum):
	PASSED = 0
	FAILED = 1
	RUNNING = 2
	ERROR = 3
	NOT_RUN = 4
	DONE = 5
	TERMINATED = 6
