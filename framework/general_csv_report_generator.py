from framework.result_list import ResultList
from framework.result_report_generator import ResultReportGenerator

import csv
import os.path


class GeneralCsvReportGenerator(ResultReportGenerator):
	def __init__(self, name, resultList: ResultList, fields):
		super().__init__(name, resultList, fields)


	def generate(self):
		# fields
		fieldsHeader = []
		fieldsData = []
		for fieldName, fieldValue in self.fields.items():
			fieldsHeader.append(fieldName)
			fieldsData.append(fieldValue)

		# header
		header = fieldsHeader
		# data
		data = fieldsData

		with open(self.name, 'a', newline='') as f:
			writer = csv.writer(f, delimiter=';')
			# opening file in the row above creates an empty file even if it does not exist.
			# check not only if the file exists, but also if it is not empty
			if not (os.path.isfile(self.name) and (os.path.getsize(self.name) > 0)):
				writer.writerow(header)
			writer.writerow(data)