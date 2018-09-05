import logging
from framework import *
from framework.result_list import *
import time
import threading
from framework.result_csv_report_generator import ResultCsvReportGenerator
from datetime import datetime
from collections import OrderedDict

class Test:

	def __init__(self, sequence: Sequence, resultList: ResultList):
		self.sequence = sequence
		self.resultList = resultList

	def run(self):
		try:
			logging.info("Test started")
			self.resultList.clear()
			self.sequence.pre()
			self.sequence.main()
			logging.info("Sequence completed")
			self.sequence.post()
		except Exception:
			logging.exception('ERROR occured')
			self.sequence.requestTerminateOnError()
			self.sequence.displayMemo('Error has occured. Sequence will be terminated.')
		except KeyError:
			logging.exception('Wrong step name used in the sequence')
			self.sequence.displayMemo('Error has occured. Sequence will be terminated.')
		finally:
			self.sequence.final()
			ots = Application() #singleton
			fields = OrderedDict()
			fields['datetime']: datetime.fromtimestamp(self.sequence.endTime).strftime('%Y-%m-%d %H:%M:%S')
			fields['sequence']: self.sequence.name
			fields['operator']: ots.loggedUser
			fields['batch number']: ots.batch.batchNumber
			fields['test result']: self.sequence.status.name
			fields['test time']: round(self.sequence.endTime - self.sequence.startTime, 2)

			report = ResultCsvReportGenerator(ots.reportsPath+self.sequence.name+datetime.now().strftime('_%Y_%m_%d.csv'), self.resultList, fields)
			report.generate()

def main():
	pass


if __name__ == "__main__": main()
