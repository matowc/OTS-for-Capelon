import logging
import time
import json
from typing import NewType
from drivers import *
from exceptions.step_fail import *
from framework.gui import *
from framework.step import *


class FullTest(Sequence):

    def __init__(self, station, name, resultList, gui: Gui = None, stepsFilepath=None, configFilepath=None):
        super().__init__(station, name, resultList, gui, stepsFilepath, configFilepath)

        # get drivers
        MqttClient_t = NewType('MqttClient_t', MqttClient)
        JLinkExe_t = NewType('JLinkExe_t', JLinkExe)
        self._MqttClient = MqttClient_t(self._station.drivers['MqttClient1'])
        self._JLinkExe = JLinkExe_t(self._station.drivers['JLinkExe1'])

        self.APIKEY = "1234"
        self.DID = ""

        # fixed RF module (with power relay) topics
        self.relayCmdTopic = '/FAC0/90FD9FFFFEDA59ED/cmd'
        self.relayAckTopic = '/FAC0/90FD9FFFFEDA59ED/cmdexe'

    def pre(self):
        super().pre()

        mqttAckTopic = '/' + self.APIKEY + '/+/cmdexe'
        mqttAttrTopic = '/' + self.APIKEY + '/+/attrs'
        self._MqttClient.subscribe(mqttAttrTopic)
        self._MqttClient.subscribe(mqttAckTopic)
        self._MqttClient.subscribe(self.relayAckTopic)

        if self._config['power cycle']['mode'] == 'auto':
            self.displayCustomMessage('', 'Powering up the device...')
            self._relayOn()
            self.clearCustomMessage()

    def post(self):
        if self._config['power cycle']['mode'] == 'auto':
            self.displayCustomMessage('', 'Powering off the device...')
            self._relayOff(0.5)
            self.clearCustomMessage()

        mqttAckTopic = '/' + self.APIKEY + '/+/cmdexe'
        mqttAttrTopic = '/' + self.APIKEY + '/+/attrs'
        self._MqttClient.unsubscribe(mqttAttrTopic)
        self._MqttClient.unsubscribe(mqttAckTopic)
        self._MqttClient.unsubscribe(self.relayAckTopic)

        super().post()

    def main(self):
        super().main()
        # returns
        try:
            if(self._config['programming']['enable'] == 'true'):
                self.displayCustomMessage('', 'Programming in progress...')
                # programming
                self.evaluateStep('deviceProgramming', self._JLinkExe.program(self._config['programming']['script']))
                self.clearCustomMessage()

            self.displayCustomMessage('', 'Device starting up...')

            for cycle in ['c1_', 'c2_']:

                # we do not know DID until it send the first message (AOEstart),
                # so I clear all messages and waits for the first one
                self._MqttClient.clearAllMostRecentMessages()

                # wait until new message appears (empty dict evaluates as False in Python)
                # timeout = 60s
                timeout = time.time() + float(self._config['general']['startUpTimeout_s'])
                while not self._MqttClient.mostRecentMessages and time.time() < timeout:
                    self.pingStatus()
                    time.sleep(0.1)

                topic = ''
                response = {}
                if self._MqttClient.mostRecentMessages:
                    [topic] = self._MqttClient.mostRecentMessages.keys()
                    [null, self.APIKEY, self.DID, null] = topic.split('/')
                    response = json.loads(self._MqttClient.mostRecentMessages[topic])

                self.clearCustomMessage()

                mqttCmdTopic = '/' + self.APIKEY + '/' + self.DID + '/cmd'
                mqttAckTopic = '/' + self.APIKEY + '/' + self.DID + '/cmdexe'
                mqttAttrTopic = '/' + self.APIKEY + '/' + self.DID + '/attrs'

                self.evaluateStep(cycle + 'startUp', 'AOEstart' in response.keys())
                self.deviceId = self.DID
                self.evaluateStep(cycle + 'deviceId', self.DID)
                self.displayCustomMessage('', 'Device {} detected.\nStarting test'.format(self.DID))

                C12Vout = ''
                C12VoutStepName = ''
                if (cycle == 'c1_'):
                    C12Vout = False
                    C12VoutStepName = 'c1_turnOff12V'
                else:
                    C12Vout = True
                    C12VoutStepName = 'c2_turnOn12V'

                response = self._sendMessageAndWaitForResponse(mqttCmdTopic, {"C12Vout": C12Vout}, mqttAckTopic,
                                                               float(self._config['general']['defaultCommandTimeout_s']))
                self.evaluateStep(C12VoutStepName, (response and response['C12Vout'] == 0))

                response = False
                retryCount = 0
                while retryCount < 3:
                    response = self._sendMessageAndWaitForResponse(mqttCmdTopic, {"Cdiags": 1}, mqttAckTopic,
                                                                   float(self._config['general']['fullTestTimeout_s']))
                    if response:
                        break
                    else:
                        retryCount = retryCount + 1

                self.evaluateStep(cycle + 'fullTestResponseRetries', retryCount)
                self.evaluateStep(cycle + 'fullTestResponse', bool(response))

                if response:
                    if cycle == 'c2_':
                        try:
                            rtc1, rtc2, rtc3 = False, False, False
                            rtc1 = self.evaluateStep(cycle + 'rtcTest', response['Cdiags']['rtc']['io'])
                            rtc2 = self.evaluateStep(cycle + 'rtcRunTest', response['Cdiags']['rtc']['run'])
                            rtc3 = self.evaluateStep(cycle + 'rtcBkupTest', response['Cdiags']['rtc']['bkup'])
                        except StepFail:
                            pass
                        finally:
                            self.evaluateStep(cycle + 'rtcTotal', rtc1 and rtc2 and rtc3)

                    if cycle == 'c1_':
                        self.evaluateStep(cycle + 'digitalInputTest', response['Cdiags']['digin'] == True)

                        try:
                            dali1, dali2, dali3 = False, False, False
                            dali1 = self.evaluateStep(cycle + 'daliTest', response['Cdiags']['dali']['io'])
                            dali2 = self.evaluateStep(cycle + 'daliErrsTest', response['Cdiags']['dali']['errs'])
                            dali3 = self.evaluateStep(cycle + 'daliAlsTest', response['Cdiags']['dali']['als'])
                        except StepFail:
                            pass
                        finally:
                            self.evaluateStep(cycle + 'daliTotal', dali1 and dali2 and dali3)

                        try:
                            acc1, acc2, acc3, acc4 = False, False, False, False
                            acc1 = self.evaluateStep(cycle + 'accelerometerTest', response['Cdiags']['accl']['io'])
                            acc2 = self.evaluateStep(cycle + 'accelerometerAngleXTest', response['Cdiags']['accl']['angl']['x'])
                            acc3 = self.evaluateStep(cycle + 'accelerometerAngleYTest', response['Cdiags']['accl']['angl']['y'])
                            acc4 = self.evaluateStep(cycle + 'accelerometerAngleZTest', response['Cdiags']['accl']['angl']['z'])
                        except StepFail:
                            pass
                        finally:
                            self.evaluateStep(cycle + 'accelerometerTotal', acc1 and acc2 and acc3 and acc4)

                if cycle == 'c1_':
                    if self._config['power cycle']['mode'] == 'reset':
                        self._JLinkExe.program('reset_script.txt')
                        self.displayCustomMessage('', 'Device starting up...')
                    elif self._config['power cycle']['mode'] == 'auto':
                        self.displayCustomMessage('', 'Restarting device...')
                        self._relayOff()
                        time.sleep(float(self._config['power cycle']['delay']))
                        self._relayOn()
                    else:
                        self.displayCustomMessage('', 'Please restart the device and wait until the device starts up...')

        except StepFail:
            logging.info("Step failed - sequence terminated")

        except QuitEvent:
            logging.warning("Sequence terminated by quitting application")

        finally:
            pass

        return

    def _sendMessageAndWaitForResponse(self, mqttCmdTopic, message, mqttAckTopic, timeout_s, ping=True):
        self._MqttClient.clearMostRecentMessage(mqttAckTopic)
        logging.debug('MQTT publish {} = {}'.format(mqttCmdTopic, message))
        self._MqttClient.publish(mqttCmdTopic, json.dumps(message))

        timeout = time.time() + timeout_s
        response = ''
        while time.time() <= timeout:
            if mqttAckTopic in self._MqttClient.mostRecentMessages.keys():
                response = self._MqttClient.mostRecentMessages[mqttAckTopic]
                response = json.loads(response)
                break
            else:
                if ping:
                    self.pingStatus()
                time.sleep(0.1)
        logging.debug('MQTT received {} = {}'.format(mqttAckTopic, response))

        return response

    def _controlRelay(self, state, timeout_s=3):
        response = self._sendMessageAndWaitForResponse(self.relayCmdTopic, {"Crelay": state}, self.relayAckTopic, timeout_s, False)
        logging.debug('Relay: {}'.format(state))

        return response['Crelay'] == 0

    def _relayOn(self, timeout_s=3):
        self._controlRelay(True, timeout_s)

    def _relayOff(self, timeout_s=3):
        self._controlRelay(False, timeout_s)



def main():
    pass


if __name__ == "__main__": main()