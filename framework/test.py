import logging
from framework import *
from framework.result_list import *
import time
import threading


class Test:

    def __init__(self, sequence: Sequence, resultList: ResultList):
        self.sequence = sequence
        self.resultList = resultList

    def run(self):
        try:
            logging.info("Test started")
            self.resultList.clear()
            logging.info("Result list cleared")
            self.sequence.pre()
            logging.info("Pre-sequence actions completed")
            self.sequence.main()
            logging.info("Sequence completed")
            self.sequence.post()
            logging.info("Post-sequence actions completed")
        except Exception:
            logging.exception('ERROR occured')
            self.sequence.requestTerminateOnError()
            self.sequence._gui._widgets['message.message']['text'] = 'Error has occured. Sequence will be terminated.'
            pass
        finally:
            self.sequence.final()
            logging.info("Test completed with result {}".format(self.sequence.status.name))


def main():
    pass


if __name__ == "__main__": main()