class MqttClient (Driver) :
	def __init__(self) :
		pass
	def connect (self) :
		# returns 
		pass
	def publish (self) :
		# returns 
		pass
	def subscribe (self) :
		# returns 
		pass
	def disconnect (self) :
		# returns 
		pass
class Printer (Driver) :
	def __init__(self) :
		pass
class Sequence :
	def __init__(self) :
		pass
	def pre (self) :
		# returns 
		pass
	def main (self) :
		# returns 
		pass
	def post (self) :
		# returns 
		pass
	def onFail (self) :
		# returns 
		pass
	def onPass (self) :
		# returns 
		pass
	def onError (self) :
		# returns 
		pass
class JLinkProgrammer (Driver) :
	def __init__(self) :
		pass
class Database :
	def __init__(self) :
		pass
class Driver :
	def __init__(self) :
		self.name = None # 
		pass
	def initialize (self) :
		# returns 
		pass
	def deinitalize (self) :
		# returns 
		pass
	def loadConfiguration (self) :
		# returns 
		pass
	def safeReset (self) :
		# returns 
		pass
class ResultList :
	def __init__(self) :
		self.results[] = None # Result
		pass
	def post (self, result) :
		# returns 
		pass
class Framework :
	def __init__(self) :
		self.eventLogger = None # EventLogger
		self.resultLogger = None # ResultLogger
		self.station = None # Station
		self.database = None # Database
		pass
	def launch (self) :
		# returns 
		pass
class Step :
	def __init__(self) :
		self.name = None # 
		self.type = None # 
		self.LL = None # 
		self.HL = None # 
		self.value = None # 
		self.result = None # 
		self.function = None # 
		pass
class Station :
	def __init__(self) :
		self.drivers[] = None # Driver
		self.config[map] = None # string
		pass
class Result :
	def __init__(self) :
		self.step = None # Step
		self.socket = None # 
		pass
class IO (Driver) :
	def __init__(self) :
		pass
class ResultLogger :
	def __init__(self) :
		pass
class Test :
	def __init__(self) :
		self.sequence = None # Sequence
		self.resultList = None # ResultList
		pass
	def run (self) :
		# returns 
		pass
class EventLogger :
	def __init__(self) :
		pass
