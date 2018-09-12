from framework.gui import *
from framework.application import *

from framework.application import Application
from framework.result_list import ResultList

ots = Application('settings.ini', 'hardware_configuration.ini')
ots.station.addDriver(MqttClient("MqttClient1"))
ots.station.addDriver(JLinkExe("JLinkExe1"))

from framework.gui_result_list import GuiResultList

resultList = ResultList()
sequence = ots.sequences['OLC NEMA PP - full test'](ots.station, 'OLC NEMA PP - full test', resultList, None, 'sequences/full_test.csv')
resultList.bindSequence(sequence)

from framework.test import Test
from framework.batch import Batch

if not ots.batch:
	ots.batch = Batch("12345")

ots.test = Test(sequence, resultList)
ots.testThread = threading.Thread(target=lambda: ots.test.run())
ots.testThread.start()