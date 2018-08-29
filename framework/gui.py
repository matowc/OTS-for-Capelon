from tkinter import *
from tkinter import ttk

from framework import *
from drivers import *
import threading

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
		
		self._frames['logo'].grid(row=0, column=0, padx = 30, pady= 30)
		self._frames['menuButtons'].grid(row=0, column=1)
		
		# header widgets
		self._widgets['logo.image'] = PhotoImage(file='/home/mateusz/Dropbox/capelon/OTS/docs/logo2.PNG')
		self._widgets['logo.logo'] = ttk.Label(self._frames['logo'], image=self._widgets['logo.image'])
		self._widgets['logo.name'] = ttk.Label(self._frames['logo'], text = 'TEST STATION', font=['Arial', 18, 'bold'], foreground='grey')
		self._widgets['menuButtons.settingsButton'] = \
			ttk.Button(self._frames['menuButtons'],text='SETTINGS', command=lambda: self.callback_settingsButtonClick())
		self._widgets['menuButtons.hardwareConfigurationButton'] = \
			ttk.Button(self._frames['menuButtons'],text='HARDWARE CONFIGURATION', command=lambda: self.callback_hardwareConfigurationButtonClick())
		self._widgets['menuButtons.dataManagementButton'] = \
			ttk.Button(self._frames['menuButtons'],text='DATA MANAGEMENT', command=lambda: self.callback_dataManagementButtonClick())
		self._widgets['menuButtons.exitButton'] = \
			ttk.Button(self._frames['menuButtons'],text='EXIT', command=lambda: self.callback_exitButtonClick())
		
		self._widgets['logo.logo'].grid(row=0, column=0)
		self._widgets['logo.name'].grid(row=1, column=0)
		#self._widgets['menuButtons.settingsButton'].grid(row=0, column=0)
		#self._widgets['menuButtons.hardwareConfigurationButton'].grid(row=0, column=1)
		#self._widgets['menuButtons.dataManagementButton'].grid(row=0, column=2)
		#self._widgets['menuButtons.exitButton'].grid(row=0, column=3)
		
		# content subframes
		self._frames['interactive'] = Frame(self._frames['content'], background = 'white')
		self._frames['customMessage'] = Frame(self._frames['content'])
		self._frames['resultList'] = Frame(self._frames['content'])
		self._frames['logs'] = Frame(self._frames['content'])
		self._frames['statistics'] = Frame(self._frames['content'])
		self._frames['testStatus'] = Frame(self._frames['content'])

		self._frames['interactive'].grid(row=0, column=0, columnspan=2)
		self._frames['resultList'].grid(row=0, column=2)
		self._frames['logs'].grid(row=3, column=0, columnspan=2)
		self._frames['statistics'].grid(row=3, column=2)
		self._frames['testStatus'].grid(row=2, column=2, sticky='nsew')
		self._frames['testStatus'].grid_rowconfigure(0, weight=1)
		self._frames['testStatus'].grid_columnconfigure(0, weight=1)

		self._frames['logs'].config(padx=10, pady=10)
		
		# content widgets
		self._widgets['interactive.sequenceList'] = \
			ttk.Combobox(self._frames['interactive'])
		self._widgets['interactive.sequenceListLabel'] = \
			ttk.Label(self._frames['interactive'], text='Choose test sequence:', font = ('Arial', 20))
		self._widgets['interactive.startButton'] = \
			ttk.Button(self._frames['interactive'], text='Start Test', command=lambda: self.callback_startButtonClick())
		self._widgets['logs.logs'] = \
			Text(self._frames['logs'], height = 10, width=60)
		self._widgets['resultList.tree'] = self.initializeResultListTree()
		self._widgets['testStatus.currentStatus'] = \
			ttk.Label(self._frames['testStatus'], text = 'NOT RUN', font=('Arial', 18), background = 'light grey', anchor = CENTER)
		self._widgets['statistics.statistics'] = \
			ttk.Label(self._frames['statistics'], text = 'PASSED: {}\nFAILED: {}\nTOTAL: {}'.format(1,2,3), background = 'yellow')
		self._widgets['customMessage.message'] = \
			ttk.Label(self._frames['customMessage'], text = '', font = ('Arial', 20))
		
		self._widgets['interactive.sequenceList'].grid(row=1, column=0, pady=30)
		self._widgets['interactive.sequenceListLabel'].grid(row=0, column=0, pady=10)
		self._widgets['interactive.startButton'].grid(row=2, column=0)
		self._widgets['logs.logs'].pack()
		self._widgets['testStatus.currentStatus'].grid(row=0, column=0, sticky='wnse', ipadx = 10, ipady = 10)
		self._widgets['statistics.statistics'].grid(row=0, column=0)
		self._widgets['resultList.tree'].grid(row=0, column=0)
		self._widgets['customMessage.message'].grid(row=0, column=0)

		self.init()
		
		self.ots = Application()
		self.ots.station.addDriver(MqttClient("MqttClient1"))
		self.ots.station.addDriver(JLinkExe("JLinkExe1"))
		
	def init(self):
		# TODO dynamic import of values
		self._widgets['interactive.sequenceList'].configure(value= ['OLC NEMA PP - full test'])
			
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
		resultListTree.column('result', width=60)
		resultListTree.column('timestamp', width=100)
		
		return resultListTree
	
	
	def callback_startButtonClick(self):
		self._frames['interactive'].grid_forget()
		# TODO dynamically load sequence class depending on chosen name
		print(self._widgets['interactive.sequenceList'].get())
		resultList1 = GuiResultList()
		resultList1.bindGui(self, self._widgets['resultList.tree'])
		sequence1 = FullTest(self.ots.station, "Full Test", resultList1, self)

		def run():
			Test(sequence1, resultList1).run()
		t = threading.Thread(target=run)
		t.start()
		#self.test =

	def displayCustomMessage(self, type, displayText):
		self._widgets['customMessage.message'].config(text= displayText)
		self._frames['interactive'].grid_forget()
		self._frames['customMessage'].grid(row=0, column=0, columnspan=2)





from sequences import *

def main():
	gui = Gui()
	gui._root.mainloop()
	
if __name__ == "__main__": main()