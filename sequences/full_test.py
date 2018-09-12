import logging
import time
from framework.sequence import Sequence
from framework.result import Result
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

    def pre(self):
        super().pre()

        mqttAckTopic = '/' + self.APIKEY + '/' +self. DID + '/cmdexe'
        mqttAttrTopic = '/' + self.APIKEY + '/+/attrs'
        self._MqttClient.subscribe(mqttAttrTopic)
        self._MqttClient.subscribe(mqttAckTopic)

    def main(self):
        super().main()
        # returns
        try:


            # self.displayCustomMessage('', 'Please power up the device')
            # time.sleep(1)
            # #power up - to clarify if we can verify it
            # self.evaluateStep('powerUp', True)
            # self.clearCustomMessage()

            if(self._config['programming']['enable'] == 'true'):
                self.displayCustomMessage('', 'Programming in progress...\nIt may take some time.')
                # programming
                self.evaluateStep('deviceProgramming', self._JLinkExe.program('programming_script.txt'))
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
                if self._MqttClient.mostRecentMessages:
                    [topic] = self._MqttClient.mostRecentMessages.keys()
                    [null, self.APIKEY, self.DID, null] = topic.split('/')

                self.clearCustomMessage()

                mqttCmdTopic = '/' + self.APIKEY + '/' + self.DID + '/cmd'
                mqttAckTopic = '/' + self.APIKEY + '/' + self.DID + '/cmdexe'
                mqttAttrTopic = '/' + self.APIKEY + '/' + self.DID + '/attrs'

                self.evaluateStep(cycle + 'startUp', bool(topic))
                self.deviceId = self.DID
                self.evaluateStep(cycle + 'deviceId', self.DID)


                response = self.sendMessageAndWaitForResponse(mqttCmdTopic, {"C12Vout": False}, mqttAckTopic,
                                                              float(self._config['general']['defaultCommandTimeout_s']))
                self.evaluateStep(cycle + 'turnOff12V', (response and response['C12Vout'] == 0))

                response = False
                retryCount = 0
                while retryCount < 3:
                    response = self.sendMessageAndWaitForResponse(mqttCmdTopic, {"Cdiags": 1}, mqttAckTopic,
                                                                  float(self._config['general']['fullTestTimeout_s']))
                    if response:
                        break
                    else:
                        retryCount = retryCount + 1

                self.evaluateStep(cycle + 'fullTestResponseRetries', retryCount)
                self.evaluateStep(cycle + 'fullTestResponse', bool(response))

                if response:
                    self.evaluateStep(cycle + 'rtcTest', response['Cdiags']['rtc']['io'])
                    self.evaluateStep(cycle + 'rtcRunTest', response['Cdiags']['rtc']['run'] == 0)
                    self.evaluateStep(cycle + 'rtcBkupTest', response['Cdiags']['rtc']['bkup'] == 0)
                    self.evaluateStep(cycle + 'digitalInputTest', response['Cdiags']['digin'] == True)
                    self.evaluateStep(cycle + 'daliTest', response['Cdiags']['dali']['io'])
                    self.evaluateStep(cycle + 'daliErrsTest', response['Cdiags']['dali']['errs'])
                    self.evaluateStep(cycle + 'daliAlsTest', response['Cdiags']['dali']['als'])
                    self.evaluateStep(cycle + 'accelerometerTest', response['Cdiags']['accl']['io'])
                    self.evaluateStep(cycle + 'accelerometerAngleXTest', response['Cdiags']['accl']['angl']['x'])
                    self.evaluateStep(cycle + 'accelerometerAngleYTest', response['Cdiags']['accl']['angl']['y'])
                    self.evaluateStep(cycle + 'accelerometerAngleZTest', response['Cdiags']['accl']['angl']['z'])

                if cycle == 'c1_':
                    self.displayCustomMessage('', 'Please power cycle the device and wait until the device starts up...')
                    if self._config['power cycle']['simulate'] == 'true':
                        # programming
                        self._JLinkExe.program('reset_script.txt')
                        self.displayCustomMessage('', 'Device starting up...')

        except StepFail:
            logging.info("Step failed - sequence terminated")

        except QuitEvent:
            logging.warning("Sequence terminated by quitting application")

        finally:
            pass

        return

    def sendMessageAndWaitForResponse(self, mqttCmdTopic, message, mqttAckTopic, timeout_s):
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
                self.pingStatus()
                time.sleep(0.1)
        logging.debug('MQTT received {} = {}'.format(mqttAckTopic, response))

        return response

    def post(self):
        super().post()
        mqttAckTopic = '/' + self.APIKEY + '/' +self. DID + '/cmdexe'
        mqttAttrTopic = '/' + self.APIKEY + '/+/attrs'
        self._MqttClient.unsubscribe(mqttAttrTopic)
        self._MqttClient.unsubscribe(mqttAckTopic)

    def onFail(self, result: Result):
        super().onFail(result)
        # raise StepFail()

    def onPass(self, result: Result):
        super().onPass(result)

    def onError(self, result: Result):
        super().onError(result)


def main():
    pass


if __name__ == "__main__": main()