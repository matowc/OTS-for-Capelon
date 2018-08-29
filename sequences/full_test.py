import logging
import time
from framework.sequence import *
from framework import *
import json
from typing import NewType
from drivers import *
from exceptions.step_fail import *
from framework.gui import *


class FullTest(Sequence):
	
	def __init__(self, station, name, resultList: ResultList, gui: Gui=None) :
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

	
	def pre (self) :
		# returns
		pass
	
	def main (self) :
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

			self._gui.displayCustomMessage('', 'Please power up the device')
			time.sleep(1)

			# power up - to clarify if we can verify it
			self.evaluateStep('powerUp', True)
			
			# programming
			# self.evaluateStep('deviceProgramming', self._JLinkExe1.program())

			self._gui.displayCustomMessage('', 'Programming in progress...\nIt may take some time.')
			time.sleep(1)
			
			# wait until new message appears (empty dict evaluates as False in Python)
			# timeout = 60s
			timeout = time.time() + 2
			while not self._MqttClient1.mostRecentMessages and time.time() < timeout:
				time.sleep(1)
				
			topic = ''
			if self._MqttClient1.mostRecentMessages:
				[topic] = self._MqttClient1.mostRecentMessages.keys()
				[null, APIKEY, DID] = topic.split('/')
				
			self.evaluateStep('startUp', bool(topic))
			self.evaluateStep('deviceId', DID)
			
			mqttCmdTopic = '/'+APIKEY+'/'+DID+'/cmd'
			mqttAckTopic = '/'+APIKEY+'/'+DID+'/cmdexe'
			mqttAttrTopic = '/'+APIKEY+'/'+DID+'/attrs'
			
			# turn 12V off
			self._MqttClient1.clearMostRecentMessage(mqttAckTopic)
			self._MqttClient1.publish(mqttCmdTopic, json.dumps({"C12Vout": False}))
			
			timeout = time.time() + 2
			message = ''
			while(time.time() <= timeout):
				if mqttAckTopic in self._MqttClient1.mostRecentMessages.keys():
					message = json.loads(self._MqttClient1.mostRecentMessages[mqttAckTopic])
					message = message['C12Vout']
					break
				else:
					time.sleep(1)
					
			self.evaluateStep('turnOff12V', (message == 0))

			self._gui.displayCustomMessage('', 'Please power cycle the device')
			time.sleep(1)

		except StepFail:
			logging.info("Step failed - sequence terminated")
			
		finally:
			pass
	
	def post (self) :
		# returns
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