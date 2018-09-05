from framework.result_list import ResultList

class ResultReportGenerator:
	def __init__(self, name, resultList: ResultList, fields):
		self._resultList = resultList
		self.fields = fields
		self.name = name
		pass

	def generate(self):
		pass