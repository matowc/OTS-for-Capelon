import logging
import time
import json
from typing import NewType
from drivers import *
from exceptions.step_fail import *
from framework.gui import *
from framework.step import *


class ProgrammingOnly(Sequence):

    def __init__(self, station, name, resultList, gui: Gui = None, stepsFilepath=None, configFilepath=None):
        super().__init__(station, name, resultList, gui, stepsFilepath, configFilepath)

        # get drivers
        JLinkExe_t = NewType('JLinkExe_t', JLinkExe)
        self._JLinkExe = JLinkExe_t(self._station.drivers['JLinkExe1'])

    def main(self):
        super().main()
        # returns
        try:
            if(self._config['programming']['enable'] == 'true'):
                self.displayCustomMessage('', 'Programming in progress...\nIt may take some time.')
                # programming
                self.evaluateStep('deviceProgramming', self._JLinkExe.program(self._config['programming']['script']))
                self.clearCustomMessage()


        except StepFail:
            logging.info("Step failed - sequence terminated")

        except QuitEvent:
            logging.warning("Sequence terminated by quitting application")

        finally:
            pass

        return

def main():
    pass


if __name__ == "__main__": main()