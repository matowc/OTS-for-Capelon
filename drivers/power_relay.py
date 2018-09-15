from drivers.mqtt_client import MqttClient
from drivers.driver import Driver
import logging

class PowerRelay(Driver):
    def __init__(self, name, configFilepath=None):
        self.mqttClient = None
        self.relayCmdTopic = '/FAC0/90FD9FFFFEDA59ED/cmd'
        self.relayAckTopic = '/FAC0/90FD9FFFFEDA59ED/cmdexe'
        super().__init__(name, configFilepath)

    def bindMqttClient(self, mqttClient):
        self.mqttClient = mqttClient
        # fixed RF module (with power relay) topics
        self.mqttClient.subscribe(self.relayAckTopic)

    def _controlRelay(self, state, timeout_s=3):
        response = self.mqttClient.sendMessageAndWaitForResponse(self.relayCmdTopic, {"Crelay": state}, self.relayAckTopic, timeout_s, None)
        logging.debug('Relay: {}'.format(state))

        return response['Crelay'] == 0

    def switchOn(self, timeout_s=3):
        self._controlRelay(True, timeout_s)

    def switchOff(self, timeout_s=3):
        self._controlRelay(False, timeout_s)


