from framework.gui import *
from framework.application import *


gui = Gui()
gui._root.protocol("WM_DELETE_WINDOW", gui.callback_quitButtonClick)
gui._root.mainloop()






# ots = Application()
# ots.station.addDriver(MqttClient("MqttClient1"))
# ots.station.addDriver(JLinkExe("JLinkExe1"))
#
# print(ots.station.drivers['MqttClient1'].name)
#
# resultList1 = ResultList()
# sequence1 = FullTest(ots.station, "Full Test", resultList1)
# test = Test(sequence1, resultList1).run()
#
# for result in resultList1.results:
# 	print (result.step.name)

