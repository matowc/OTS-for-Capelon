import logging
import time
import paho.mqtt.client as paho

from drivers.driver import Driver

class MqttClient(Driver):

	def __init__(self, name, configFilepath=None):
		self._client = None
		self._clientId = 'ots'
		self._server = 'localhost'
		self._port = 1883
		self._topics = [{'name': '/1234/#', 'qos': 1}]
		self.mostRecentMessages = {}
		super().__init__(name, configFilepath)
		
	def __del__(self):
		self.deinitialize()

	def initialize(self):
		self._client = paho.Client(self._clientId)
		self._client.on_subscribe = self.onSubscribe
		self._client.on_message = self.onMessage
		self._client.on_connect = self.onConnect
		try:
			self.connect(self._server, self._port)
		except Exception:
			pass

		for topic in self._topics:
			self.subscribe(topic['name'], topic['qos'])
			self._client.loop_start()

	def deinitialize(self):
		self._client.loop_stop()
		pass

	def loadConfiguration(self):
		# replace with loading from .ini file
		pass

	def safeReset(self):
		pass

	def connect(self, server, port):
		# todo handle error when connection not available (i.e. netowrk is down)
		self._client.connect(server, port)
		pass

	def publish(self, topic, payload, _qos=1):
		self._client.publish(topic, payload, qos=_qos)
		pass

	def subscribe(self, topic, _qos=1):
		self._client.subscribe(topic, qos=_qos)
		pass

	def disconnect(self):
		pass
	
	def clearMostRecentMessage(self, topic):
		if topic in self.mostRecentMessages:
			del self.mostRecentMessages[topic]
		
	def clearAllMostRecentMessages(self):
		self.mostRecentMessages = {}

	def onSubscribe(self, client, userdata, mid, granted_qos):
		logging.info("Subscribed: "+str(mid)+" "+str(granted_qos))

	def onMessage(self, client, userdata, msg):
		self.mostRecentMessages[msg.topic] = str(msg.payload.decode("utf-8"))
		logging.info(msg.topic+" "+str(msg.qos)+" "+str(msg.payload.decode("utf-8")))
	
	def onConnect(self, client, userdata, flags, rc):
		logging.info("MQTT CONNACK received with code %d." % (rc))



def main():
	#client = MqttClient("mqtt1")
	pass

if __name__ == "__main__" : main()
