from framework.result_list import ResultList
from framework.result_report_generator import ResultReportGenerator

import csv
import os.path


class ResultCsvReportGenerator(ResultReportGenerator):
	def __init__(self, name, resultList: ResultList, fields):
		super().__init__(name, resultList, fields)


	def generate(self):
		# fields
		fieldsHeader = []
		fieldsData = []
		for fieldName, fieldValue in self.fields.items():
			fieldsHeader.append(fieldName)
			fieldsData.append(fieldValue)

		# resultsHeader
		resultsHeader = []
		for stepName in self._resultList.sequence.steps.keys():
			resultsHeader.append(stepName)

		# header
		header = fieldsHeader + resultsHeader

		# results data
		resultsData = [0] * len(resultsHeader)
		for result in self._resultList.results:
			resultsData[resultsHeader.index(result.step.name)] = str(result.value)

		# data
		data = fieldsData + resultsData

		with open(self.name, 'a', newline='') as f:
			writer = csv.writer(f, delimiter=';')
			# opening file in the row above creates an empty file even if it does not exist.
			# check not only if the file exists, but also if it is not empty
			if not (os.path.isfile(self.name) and (os.path.getsize(self.name) > 0)):
				writer.writerow(header)
			writer.writerow(data)