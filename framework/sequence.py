import logging
from exceptions.step_fail import StepFail
from framework.sequence_result_enum import *
from exceptions.step_fail import *
import time
import threading


class Sequence:

    def __init__(self, station, name, resultList, gui=None):
        self._station = station
        self.name = name
        self._resultList = resultList
        self._gui = gui
        self.status = SequenceStatusEnum.NOT_RUN
        self.startTime = None
        self.endTime = None

    def evaluateStep(self, stepName: str, value):
        return self.steps[stepName].evaluate(self, value, self._resultList)

    def updateTimer(self):
        if self._gui:
            self._gui.updateTestTime(time.time() - self.startTime)
            if self.status == SequenceStatusEnum.RUNNING:
                threading.Timer(1, self.updateTimer).start()

    def pre(self):
        self.startTime = time.time()
        self.status = SequenceStatusEnum.RUNNING
        self.updateTimer()

        if self._gui:
            self._gui.updateTestStatus("Sequence pre-actions in progress...", "light grey")

        # returns
        pass

    def main(self):
        if self._gui:
            self._gui.updateTestStatus("Test in progress...", self._gui.colors['light grey'], True)

        pass

    def post(self):
        if self._gui:
            self._gui.updateTestStatus("Sequence post-actions in progress...", self._gui.colors['light grey'])
        # returns
        pass

    def final(self):
        self.endTime = time.time()
        if self.status == SequenceStatusEnum.RUNNING:
            self.status = SequenceStatusEnum.PASSED
        if self._gui:
            if self.status == SequenceStatusEnum.PASSED:
                self._gui.updateTestStatus("TEST PASSED", self._gui.colors['light green'])
                self._gui.incrementPassedStatistics()
            elif self.status == SequenceStatusEnum.FAILED:
                self._gui.updateTestStatus("TEST FAILED", self._gui.colors['red'])
                self._gui.incrementFailedStatistics()
            elif self.status == SequenceStatusEnum.ERROR:
                self._gui.updateTestStatus("TEST FINISHED WITH ERROR", self._gui.colors['red'])
                self._gui.incrementFailedStatistics()
            elif self.status == SequenceStatusEnum.TERMINATED:
                self._gui.updateTestStatus("SEQUENCE TERMINATED", self._gui.colors['red'])
                self._gui.incrementFailedStatistics()
            else:
                self._gui.updateTestStatus("UNKNOWN ERROR", self._gui.colors['red'])
                self._gui.incrementFailedStatistics()

            self._gui.displaySequenceChoice()

    def postStep(self, result):
        if self.status == SequenceStatusEnum.TERMINATED:
            raise QuitEvent

    def pingStatus(self):
        if self.status == SequenceStatusEnum.TERMINATED:
            raise QuitEvent

    def onFail(self, result):
        logging.info("Step {} FAILED".format(result.step.name))
        self.status = SequenceStatusEnum.FAILED
        raise StepFail

    def onPass(self, result):
        pass

    def onError(self, result):
        self.status = SequenceStatusEnum.ERROR

    def displayCustomMessage(self, type, displayText):
        if self._gui:
            self._gui.displayCustomMessage(type, displayText)

    def clearCustomMessage(self):
        if self._gui:
            self._gui.displayCustomMessage('', '')

    def requestTerminate(self):
        self.status = SequenceStatusEnum.TERMINATED


def main():
    pass


if __name__ == "__main__": main()