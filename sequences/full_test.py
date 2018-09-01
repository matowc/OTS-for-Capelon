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
			'powerUp':						Step("Power up the device", StepTypeEnum.ACTION),
			'deviceDetect': 				Step("Programmer: device detection", StepTypeEnum.BOOL),
			'deviceProgramming': 			Step("Programmer: programming", StepTypeEnum.BOOL),
			'c1_startUp': 					Step("[Cycle1] MQTT: start-up message", StepTypeEnum.BOOL),
			'c1_deviceId': 					Step("[Cycle1] MQTT: DID", StepTypeEnum.ACTION),
			'c1_turnOff12V': 				Step("[Cycle1] MQTT: turn 12V off", StepTypeEnum.BOOL),
			'c1_fullTestResponse': 			Step("[Cycle1] MQTT: run full test", StepTypeEnum.BOOL),
			'c1_fullTestResponseRetries': 	Step("[Cycle1] MQTT: number of retries", StepTypeEnum.ACTION),
			'c1_rtcTest': 					Step("[Cycle1] MQTT: RTC test", StepTypeEnum.BOOL),
			'c1_rtcRunTest': 				Step("[Cycle1] MQTT: RTC - run ", StepTypeEnum.NUMERIC, "0:0"),
			'c1_rtcBkupTest': 				Step("[Cycle1] MQTT: RTC - bckup", StepTypeEnum.NUMERIC, "0:0"),
			'c1_digitalInputTest':			Step("[Cycle1] MQTT: digital input", StepTypeEnum.BOOL),
			'c1_daliTest':					Step("[Cycle1] MQTT: DALI test", StepTypeEnum.BOOL),
			'c1_daliErrsTest': 				Step("[Cycle1] MQTT: DALI - errs", StepTypeEnum.NUMERIC, "0:0"),
			'c1_daliAlsTest': 				Step("[Cycle1] MQTT: DALI - als", StepTypeEnum.NUMERIC, "0:100"),
			'c1_accelerometerTest': 		Step("[Cycle1] MQTT: Accelerometer test", StepTypeEnum.BOOL),
			'c1_accelerometerAngleXTest': 	Step("[Cycle1] MQTT: Accelerometer - X angle", StepTypeEnum.NUMERIC, "-90:90"),
			'c1_accelerometerAngleYTest': 	Step("[Cycle1] MQTT: Accelerometer - Y angle", StepTypeEnum.NUMERIC, "-90:90"),
			'c1_accelerometerAngleZTest': 	Step("[Cycle1] MQTT: Accelerometer - Z angle", StepTypeEnum.NUMERIC, "-90:90"),
			'powerCycle': 					Step("Power cycle the device", StepTypeEnum.ACTION),
			'c2_startUp': 					Step("[Cycle2] MQTT: start-up message", StepTypeEnum.BOOL),
			'c2_deviceId': 					Step("[Cycle2] MQTT: DID", StepTypeEnum.ACTION),
			'c2_turnOff12V': 				Step("[Cycle2] MQTT: turn 12V off", StepTypeEnum.BOOL),
			'c2_fullTestResponse': 			Step("[Cycle2] MQTT: run full test", StepTypeEnum.BOOL),
			'c2_fullTestResponseRetries': 	Step("[Cycle2] MQTT: number of retries", StepTypeEnum.ACTION),
			'c2_rtcTest': 					Step("[Cycle2] MQTT: RTC test", StepTypeEnum.BOOL),
			'c2_rtcRunTest': 				Step("[Cycle2] MQTT: RTC - run ", StepTypeEnum.NUMERIC, "0:0"),
			'c2_rtcBkupTest': 				Step("[Cycle2] MQTT: RTC - bckup", StepTypeEnum.NUMERIC, "0:0"),
			'c2_digitalInputTest': 			Step("[Cycle2] MQTT: digital input", StepTypeEnum.BOOL),
			'c2_daliTest': 					Step("[Cycle2] MQTT: DALI test", StepTypeEnum.BOOL),
			'c2_daliErrsTest': 				Step("[Cycle2] MQTT: DALI - errs", StepTypeEnum.NUMERIC, "0:0"),
			'c2_daliAlsTest': 				Step("[Cycle2] MQTT: DALI - als", StepTypeEnum.NUMERIC, "0:100"),
			'c2_accelerometerTest': 		Step("[Cycle2] MQTT: Accelerometer test", StepTypeEnum.BOOL),
			'c2_accelerometerAngleXTest': 	Step("[Cycle2] MQTT: Accelerometer - X angle", StepTypeEnum.NUMERIC, "-90:90"),
			'c2_accelerometerAngleYTest': 	Step("[Cycle2] MQTT: Accelerometer - Y angle", StepTypeEnum.NUMERIC, "-90:90"),
			'c2_accelerometerAngleZTest': 	Step("[Cycle2] MQTT: Accelerometer - Z angle", StepTypeEnum.NUMERIC, "-90:90")

		}

		self._config = {
			'startUpTimeout_s':			25,
			'fullTestTimeout_s':		2,
			'defaultCommandTimeout_s':	2
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

			for cycle in ['c1_', 'c2_']:

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

				self._MqttClient1.subscribe(mqttAckTopic, 1)
				self._MqttClient1.subscribe(mqttAttrTopic, 1)

				self.evaluateStep(cycle+'startUp', bool(topic))
				self.evaluateStep(cycle+'deviceId', DID)

				response = self.sendMessageAndWaitForResponse(mqttCmdTopic, {"C12Vout": False}, mqttAckTopic, self._config['defaultCommandTimeout_s'])
				self.evaluateStep(cycle+'turnOff12V', (response and response['C12Vout'] == 0))

				response = False
				retryCount = 0
				while retryCount < 3:
					retryCount = retryCount + 1
					response = self.sendMessageAndWaitForResponse(mqttCmdTopic, {"Cdiags": 1}, mqttAckTopic, self._config['fullTestTimeout_s'])
					if response:
						break
				self.evaluateStep(cycle+'fullTestResponseRetries', retryCount)
				self.evaluateStep(cycle+'fullTestResponse', response == True)

				if response:
					self.evaluateStep(cycle+'rtcTest', response['Cdiags']['rtc']['io'])
					self.evaluateStep(cycle+'rtcRunTest', response['Cdiags']['rtc']['run'] == 0)
					self.evaluateStep(cycle+'rtcBkupTest', response['Cdiags']['rtc']['bkup'] == 0)
					self.evaluateStep(cycle+'digitalInputTest', response['Cdiags']['digin'] == True)
					self.evaluateStep(cycle+'daliTest', response['Cdiags']['dali']['io'])
					self.evaluateStep(cycle+'daliErrsTest', response['Cdiags']['dali']['errs'])
					self.evaluateStep(cycle+'daliAlsTest', response['Cdiags']['dali']['als'])
					self.evaluateStep(cycle+'accelerometerTest', response['Cdiags']['accl']['io'])
					self.evaluateStep(cycle+'accelerometerAngleXTest', response['Cdiags']['accl']['angl']['x'])
					self.evaluateStep(cycle+'accelerometerAngleYTest', response['Cdiags']['accl']['angl']['y'])
					self.evaluateStep(cycle+'accelerometerAngleZTest', response['Cdiags']['accl']['angl']['z'])

				if cycle == 'c1_':
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
		logging.debug(mqttAckTopic)
		self._MqttClient1.publish(mqttCmdTopic, json.dumps(message))

		timeout = time.time() + timeout_s
		response = ''
		while time.time() <= timeout:
			print(self._MqttClient1.mostRecentMessages.keys())
			if mqttAckTopic in self._MqttClient1.mostRecentMessages.keys():
				print(self._MqttClient1.mostRecentMessages)
				response = self._MqttClient1.mostRecentMessages[mqttAckTopic]
				logging.debug(response)
				response = json.loads(response)
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