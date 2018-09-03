import logging

class Batch:
	def __init__(self, batchNumber):
		self.batchNumber = batchNumber
		logging.info('Batch \'{}\' opened'.format(self.batchNumber))

	def close(self):
		logging.info('Batch \'{}\' closed'.format(self.batchNumber))