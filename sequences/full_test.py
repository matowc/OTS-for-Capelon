import logging
import time
from framework.sequence import *
from framework.result import Result
import json
from typing import NewType
from drivers import *
from exceptions.step_fail import *
from framework.gui import *
from framework.step import *


class FullTest(Sequence):
	
	def __init__(self, station, name, resultList, gui: Gui=None) :
		super().__init__(station, name, resultList)
		
		# get drivers
		MqttClient_t = NewType('MqttClient_t', MqttClient)
		JLinkExe_t = NewType('JLinkExe_t', JLinkExe)
		self._MqttClient1 = MqttClient_t(self._station.drivers['MqttClient1'])
		self._JLinkExe1 = JLinkExe_t(self._station.drivers['JLinkExe1'])
		self._gui = gui
		
		# define steps
		self.steps = {
			'powerUp':					Step("Power up the device", StepTypeEnum.ACTION),
			'deviceDetect': 			Step("Programmer: device detection", StepTypeEnum.BOOL),
			'deviceProgramming': 		Step("Programmer: programming", StepTypeEnum.BOOL),
			'startUp': 					Step("MQTT: start-up message", StepTypeEnum.BOOL),
			'deviceId': 				Step("MQTT: DID", StepTypeEnum.ACTION),
			'turnOff12V': 				Step("MQTT: turn 12V off", StepTypeEnum.BOOL),
			'fullTestResponse': 		Step("MQTT: run full test", StepTypeEnum.BOOL),
			'fullTestResponseRetries': 	Step("MQTT: number of retries", StepTypeEnum.ACTION),
			'rtcTest': 					Step("MQTT: RTC test", StepTypeEnum.BOOL),
			'rtcRunTest': 				Step("MQTT: RTC - run ", StepTypeEnum.NUMERIC, "0:0"),
			'rtcBkupTest': 				Step("MQTT: RTC - bckup", StepTypeEnum.NUMERIC, "0:0"),
			'digitalInputTest':			Step("MQTT: digital input", StepTypeEnum.BOOL),
			'daliTest':					Step("MQTT: DALI test", StepTypeEnum.BOOL),
			'daliErrsTest': 			Step("MQTT: DALI - errs", StepTypeEnum.NUMERIC, "0:0"),
			'daliAlsTest': 				Step("MQTT: DALI - als", StepTypeEnum.NUMERIC, "0:100"),
			'accelerometerTest': 		Step("MQTT: Accelerometer test", StepTypeEnum.BOOL),
			'accelerometerAngleXTest': 	Step("MQTT: Accelerometer - X angle", StepTypeEnum.NUMERIC, "-90:90"),
			'accelerometerAngleYTest': 	Step("MQTT: Accelerometer - Y angle", StepTypeEnum.NUMERIC, "-90:90"),
			'accelerometerAngleZTest': 	Step("MQTT: Accelerometer - Z angle", StepTypeEnum.NUMERIC, "-90:90")

		}

		self._config = {
			'startUpTimeout_s':			3,
			'fullTestTimeout_s':		3,
			'defaultCommandTimeout_s':	3
		}

	
	def pre (self) :
		super().pre()
		pass
	
	def main (self) :
		super().main()
		# returns
		try:
			APIKEY = "1234"
			DID = ""
			mqttAttrTopic = '/' + APIKEY + '/+/attrs'
			
			# local temp variables for MQTT communication
			topic = ''
			message = ''
			
			# we do not know DID until it send the first message (AOEstart),
			# so I clear all messages and waits for the first one
			self._MqttClient1.clearAllMostRecentMessages()
			self._MqttClient1.subscribe(mqttAttrTopic)

			self.displayCustomMessage('', 'Please power up the device')
			time.sleep(1)
			# power up - to clarify if we can verify it
			self.evaluateStep('powerUp', True)
			self.clearCustomMessage()

			self.displayCustomMessage('', 'Programming in progress...\nIt may take some time.')
			# programming
			# self.evaluateStep('deviceProgramming', self._JLinkExe1.program())
			time.sleep(1)
			self.clearCustomMessage()
			
			# wait until new message appears (empty dict evaluates as False in Python)
			# timeout = 60s
			timeout = time.time() + self._config['startUpTimeout_s']
			while not self._MqttClient1.mostRecentMessages and time.time() < timeout:
				time.sleep(1)
				
			topic = ''
			if self._MqttClient1.mostRecentMessages:
				[topic] = self._MqttClient1.mostRecentMessages.keys()
				[null, APIKEY, DID, null] = topic.split('/')

			mqttCmdTopic = '/'+APIKEY+'/'+DID+'/cmd'
			mqttAckTopic = '/'+APIKEY+'/'+DID+'/cmdexe'
			mqttAttrTopic = '/'+APIKEY+'/'+DID+'/attrs'

			self.evaluateStep('startUp', bool(topic))
			self.evaluateStep('deviceId', DID)

			response = self.sendMessageAndWaitForResponse(mqttCmdTopic, {"C12Vout": False}, mqttAckTopic, self._config['defaultCommandTimeout_s'])
			self.evaluateStep('turnOff12V', (response and response['C12Vout'] == 0))

			response = False
			retryCount = 0
			while retryCount < 3:
				retryCount = retryCount + 1
				response = self.sendMessageAndWaitForResponse(mqttCmdTopic, {"Cdiags": 1}, mqttAckTopic, self._config['fullTestTimeout_s'])
				if response:
					break
			self.evaluateStep('fullTestResponseRetries', retryCount)
			self.evaluateStep('fullTestResponse', response)

			if response:
				self.evaluateStep('rtcTest', response['Cdiags']['rtc']['io'])
				self.evaluateStep('rtcRunTest', response['Cdiags']['rtc']['run'] == 0)
				self.evaluateStep('rtcBkupTest', response['Cdiags']['rtc']['bkup'] == 0)
				self.evaluateStep('digitalInputTest', response['Cdiags']['digin'] == True)
				self.evaluateStep('daliTest', response['Cdiags']['dali']['io'])
				self.evaluateStep('daliErrsTest', response['Cdiags']['dali']['errs'])
				self.evaluateStep('daliAlsTest', response['Cdiags']['dali']['als'])
				self.evaluateStep('accelerometerTest', response['Cdiags']['accl']['io'])
				self.evaluateStep('accelerometerAngleXTest', response['Cdiags']['angl']['x'])
				self.evaluateStep('accelerometerAngleYTest', response['Cdiags']['angl']['y'])
				self.evaluateStep('accelerometerAngleZTest', response['Cdiags']['angl']['z'])

			self.displayCustomMessage('', 'Please power cycle the device')
			time.sleep(1)
			self.clearCustomMessage()

		except StepFail:
			logging.info("Step failed - sequence terminated")

		except QuitEvent:
			logging.warning("Sequence terminated by quitting application")
			
		finally:
			pass

		return

	def sendMessageAndWaitForResponse(self, mqttCmdTopic, message, mqttAckTopic, timeout_s):
		self._MqttClient1.clearMostRecentMessage(mqttAckTopic)
		logging.debug('MQTT publish {} = {}'.format(mqttCmdTopic, message))
		self._MqttClient1.publish(mqttCmdTopic, json.dumps(message))

		timeout = time.time() + timeout_s
		response = ''
		while time.time() <= timeout:
			if mqttAckTopic in self._MqttClient1.mostRecentMessages.keys():
				response = json.loads(self._MqttClient1.mostRecentMessages[mqttAckTopic].decode("utf-8"))
				break
			else:
				time.sleep(1)
		logging.debug('MQTT received {} = {}'.format(mqttAckTopic, response))

		return response

	def post (self) :
		super().post()
		pass

	def onFail(self, result: Result):
		super().onFail(result)
		# raise StepFail()
		# returns
		pass

	def onPass(self, result: Result):
		super().onPass(result)
		# returns
		pass

	def onError(self, result: Result):
		super().onError(result)
		# returns
		pass

	
def main():
	pass

if __name__ == "__main__" : main()