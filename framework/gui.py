from tkinter import *
from tkinter import ttk

from framework import *
from drivers import *
from sequences import *

logging.basicConfig(level=logging.DEBUG)

class Gui:
	def __init__(self):
		self._root = Tk()
		self._root.geometry("1400x800+0+0")
		self._root.title("Owczarek Test System (OTS) for Capelon")
		self._root.configure(background = 'white')
		
		self._style = ttk.Style()
		self._style.configure('TFrame', background='white')
		self._style.configure('TLabel', background='white')
		self._style.configure('TButton', background='white')
		self._style.configure('TreeView', background='white')
		
		self._frames = {}
		self._widgets = {}
		
		self._frames['header'] = ttk.Frame(self._root)
		self._frames['content'] = ttk.Frame(self._root)
		
		self._frames['header'].pack()
		self._frames['content'].pack()
		
		# header subframes
		self._frames['logo'] = ttk.Frame(self._frames['header'])
		self._frames['menuButtons'] = ttk.Frame(self._frames['header'])
		
		self._frames['logo'].grid(row=0, column=0)
		self._frames['menuButtons'].grid(row=0, column=1)
		
		# header widgets
		self._widgets['logo.image'] = PhotoImage(file='/home/mateusz/Dropbox/capelon/OTS/docs/logo.png')
		self._widgets['logo.logo'] = ttk.Label(self._frames['logo'], image=self._widgets['logo.image'])
		self._widgets['menuButtons.settingsButton'] = \
			ttk.Button(self._frames['menuButtons'],text='SETTINGS', command=lambda: self.callback_settingsButtonClick())
		self._widgets['menuButtons.hardwareConfigurationButton'] = \
			ttk.Button(self._frames['menuButtons'],text='HARDWARE CONFIGURATION', command=lambda: self.callback_hardwareConfigurationButtonClick())
		self._widgets['menuButtons.dataManagementButton'] = \
			ttk.Button(self._frames['menuButtons'],text='DATA MANAGEMENT', command=lambda: self.callback_dataManagementButtonClick())
		self._widgets['menuButtons.exitButton'] = \
			ttk.Button(self._frames['menuButtons'],text='EXIT', command=lambda: self.callback_exitButtonClick())
		
		self._widgets['logo.logo'].grid(row=0, column=0)
		self._widgets['menuButtons.settingsButton'].grid(row=0, column=0)
		self._widgets['menuButtons.hardwareConfigurationButton'].grid(row=0, column=1)
		self._widgets['menuButtons.dataManagementButton'].grid(row=0, column=2)
		self._widgets['menuButtons.exitButton'].grid(row=0, column=3)
		
		# content subframes
		self._frames['interactive'] = Frame(self._frames['content'])
		self._frames['resultList'] = Frame(self._frames['content'])
		self._frames['logs'] = Frame(self._frames['content'])
		self._frames['logs'].config(padx=10, pady=10)
		self._frames['statistics'] = Frame(self._frames['content'])
		self._frames['testStatus'] = Frame(self._frames['content'])

		self._frames['interactive'].grid(row=0, column=0, columnspan=2)
		self._frames['resultList'].grid(row=0, column=2)
		self._frames['logs'].grid(row=3, column=1)
		self._frames['statistics'].grid(row=3, column=0)
		self._frames['testStatus'].grid(row=3, column=2)
		
		# content widgets
		self._widgets['interactive.sequenceList'] = \
			ttk.Combobox(self._frames['interactive'], values=('GEN-PROG-ONLY', 'RF-CAP-OLCPP-PROG-ONLY'))
		self._widgets['interactive.sequenceListLabel'] = \
			ttk.Label(self._frames['interactive'], text='Choose test sequence:')
		self._widgets['interactive.startButton'] = \
			ttk.Button(self._frames['interactive'], text='Start Test', command=lambda: self.callback_startButtonClick())
		self._widgets['logs.logs'] = \
			Text(self._frames['logs'], height = 10, width=60)
		self._widgets['resultList.tree'] = self.initializeResultListTree()
		
		self._widgets['interactive.sequenceList'].grid(row=1, column=0)
		self._widgets['interactive.sequenceListLabel'].grid(row=0, column=0 )
		self._widgets['interactive.startButton'].grid(row=2, column=0)
		self._widgets['logs.logs'].pack()
		self._widgets['resultList.tree'].grid(row=0, column=0)
		
		self.ots = Application()
		self.ots.station.addDriver(MqttClient("MqttClient1"))
		self.ots.station.addDriver(JLinkExe("JLinkExe1"))
		

		#
		# for result in resultList1.results:
		# 	print(result.step.name)
			
	def initializeResultListTree(self):
		resultListTree = ttk.Treeview(self._frames['resultList'])
		resultListTree.config(
			columns=('id', 'stepName', 'stepType', 'value', 'limits', 'result', 'timestamp'), height=20)
		
		resultListTree.heading('#0', text='')
		resultListTree.heading('id', text='ID')
		resultListTree.heading('stepName', text='Step Name')
		resultListTree.heading('stepType', text='Type')
		resultListTree.heading('value', text='Value')
		resultListTree.heading('limits', text='Limits')
		resultListTree.heading('result', text='Result')
		resultListTree.heading('timestamp', text='Timestamp')
		
		resultListTree.column('#0', width=20)
		resultListTree.column('id', width=50)
		resultListTree.column('stepName', width=350)
		resultListTree.column('stepType', width=80)
		resultListTree.column('value', width=80)
		resultListTree.column('limits', width=120)
		resultListTree.column('result', width=40)
		resultListTree.column('timestamp', width=100)
		
		return resultListTree
	
	
	def callback_startButtonClick(self):
		print(self._widgets['interactive.sequenceList'].get())
		resultList1 = GuiResultList()
		resultList1.bindGui(self, self._widgets['resultList.tree'])
		sequence1 = FullTest(self.ots.station, "Full Test", resultList1)
		self.test = Test(sequence1, resultList1).run()


def main():
	gui = Gui()
	gui._root.mainloop()
	
if __name__ == "__main__": main()