import logging
import time
from framework import *
import json
from typing import NewType
from drivers import *


class FullTest(Sequence):
	
	def __init__(self, station, name, resultList: ResultList) :
		super().__init__(station, name, resultList)
		
		# get drivers
		self._MqttClient1 = MqttClient(self._station.drivers['MqttClient1'])
		self._JLinkExe1 = JLinkExe(self._station.drivers['JLinkExe1'])
		
		# define steps
		self.steps = {
			'startUpTopic':			Step("Start-up Topic", StepTypeEnum.STRING, ""),
			'deviceId':				Step("Device ID", StepTypeEnum.STRING, ""),
			'programming' : 		Step("Device programming", StepTypeEnum.BOOL, True),
			'accelerometer-x' : 	Step("Accelerometer X", StepTypeEnum.NUMERIC, "0:1")
		}
		
		# g = NewType('g', MqttClient)
		# mg = g(self._MqttClient1)
		# mg.publish()
		# MqttClient(self._MqttClient1)
		
		pass
	
	def pre (self) :
		# returns
		pass
	
	def main (self) :
		# returns
		try:
			# Software started
			# Power up Device
			APIKEY = "1234"
			DID = ""
			mqttAttrTopic = '/' + APIKEY + '/+/attrs'
			self._MqttClient1.clearAllMostRecentMessages()
			self._MqttClient1.subscribe(mqttAttrTopic)
			time.sleep(2)
			
			topic = ""
			try:
				[topic] = self._MqttClient1.mostRecentMessages.keys()
			except ValueError:
				pass
			self.steps['startUpTopic'].evaluate(self, topic, self._resultList)
			
			try:
				[null, APIKEY, DID] = topic.split('/')
				
			except ValueError:
				pass
			self.steps['deviceId'].evaluate(self, DID, self._resultList)
			
			mqttCmdTopic = '/'+APIKEY+'/'+DID+'/cmd'
			mqttAckTopic = '/'+APIKEY+'/'+DID+'/cmdexe'
			mqttAttrTopic = '/'+APIKEY+'/'+DID+'/attrs'
			
			# When Device ID received software register device
			# S/W prompts user to press Start test button
			# OLC software performs test
			# Test Accelerometer
			self._MqttClient1.clearMostRecentMessage(mqttCmdTopic)
			self._MqttClient1.publish(mqttCmdTopic, json.dumps({"Cattrs": ["AOMaccl", "AOMangl"]}))
			time.sleep(2)
			payload = ""
			if mqttAckTopic in self._MqttClient1.mostRecentMessages:
				payload = self._MqttClient1.mostRecentMessages[mqttAckTopic]
				
			self.steps['accelerometer-x'].evaluate(self, payload, self._resultList)
				
			
			# Test RTC
			# Test Dali
			
			# We do not have to test dig input, but if you want we could have the test fixture set the digital input to a certain state and you can check it too, but we should not require to switch the dig input since it would require manual handling.
			# If all test are passed
			# S/W prompts user to power cycle device
			# If all tests are not passed
			# Test failed
			# A test result with corresponding Device ID is received by software
			# Then Software will consider this devices OK
			# Result will be logged and label printed
			# Then test software will going to waiting mode until a new device ID is received. (step 3)
			# Or user can exit test
		finally:
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
	
	
def main():
	pass

if __name__ == "__main__" : main()