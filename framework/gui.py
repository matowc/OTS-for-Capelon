from tkinter import *
from tkinter import ttk
import time
from drivers import *
import threading
import logging
from tkinter import messagebox
from tkinter import scrolledtext


logging.basicConfig(level=logging.DEBUG, format='%(asctime)-15s | %(message)s')

class TextHandler(logging.Handler):
    # This class allows you to log to a Tkinter Text or ScrolledText widget
    # Adapted from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06

    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        msg = self.format(record)

        def append():
            self.text.configure(state='normal')
            self.text.insert('end', msg + '\n')
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview('end')
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)

class Gui:
	def __init__(self):
		self._root = Tk()
		self._root.geometry("1700x1000+100+0")
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
		self._widgets['logo.image'] = PhotoImage(file='docs/logo2.PNG')
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

		style = ttk.Style()
		style.element_create("Custom.Treeheading.border", "from", "default")
		style.layout("Custom.Treeview.Heading", [
			("Custom.Treeheading.cell", {'sticky': 'nswe'}),
			("Custom.Treeheading.border", {'sticky': 'nswe', 'children': [
				("Custom.Treeheading.padding", {'sticky': 'nswe', 'children': [
					("Custom.Treeheading.image", {'side': 'right', 'sticky': ''}),
					("Custom.Treeheading.text", {'sticky': 'we'})
				]})
			]}),
		])
		style.configure("Custom.Treeview.Heading",
						background="grey", foreground="white", relief="flat")
		style.map("Custom.Treeview.Heading",
				  relief=[('active', 'groove'), ('pressed', 'sunken')])
		
		# content subframes
		self._frames['interactive'] = Frame(self._frames['content'], background = 'white')
		self._frames['message'] = Frame(self._frames['content'])
		self._frames['customFrame'] = Frame(self._frames['content'])
		self._frames['resultList'] = Frame(self._frames['content'])
		self._frames['logs'] = LabelFrame(self._frames['content'], background='white', text='Logs', pady=10, padx=10)
		self._frames['statistics'] = Frame(self._frames['content'], background ='white')
		self._frames['testStatus'] = Frame(self._frames['content'])

		self._frames['interactive'].grid(row=1, column=0, columnspan=2)
		self._frames['message'].grid(row=0, column=0, columnspan=2)
		self._frames['resultList'].grid(row=0, column=3, rowspan=2)
		self._frames['logs'].grid(row=3, column=0, columnspan=2)
		self._frames['statistics'].grid(row=3, column=3, sticky='nsew')
		self._frames['testStatus'].grid(row=2, column=3, sticky='nsew')
		self._frames['testStatus'].grid_rowconfigure(0, weight=1)
		self._frames['testStatus'].grid_columnconfigure(0, weight=1)
		self._frames['content'].grid_columnconfigure(2, minsize=100, weight=1)
		
		# content widgets
		self._widgets['message.message'] = \
			ttk.Label(self._frames['message'], text='', font=('Arial',16))
		self._widgets['interactive.sequenceList'] = \
			ttk.Combobox(self._frames['interactive'], font=('Arial', 14))
		self._widgets['interactive.sequenceListLabel'] = \
			ttk.Label(self._frames['interactive'], text='Choose test sequence:', font = ('Arial', 20))
		self._widgets['interactive.startButton'] = \
			ttk.Button(self._frames['interactive'], text='Start Test', command=lambda: self.callback_startButtonClick())
		self._widgets['logs.logs'] = \
			scrolledtext.ScrolledText(self._frames['logs'], height = 10, width=80, state='disabled', bd=0, highlightthickness=0, relief='ridge')
		self._widgets['resultList.tree'] = self.initializeResultListTree()
		self._widgets['logs.logs'].configure(font=('TkFixedFont', 7))
		self._widgets['testStatus.currentStatus'] = \
			ttk.Label(self._frames['testStatus'], text = 'NOT RUN', font=('Arial', 18), background = 'light grey', anchor = CENTER)
		self.initializeStatisticsFrame()
		self._widgets['customFrame.message'] = \
			ttk.Label(self._frames['customFrame'], text = '', font = ('Arial', 20))
		
		self._widgets['message.message'].pack()
		self._widgets['interactive.sequenceList'].grid(row=1, column=0, pady=30)
		self._widgets['interactive.sequenceListLabel'].grid(row=0, column=0, pady=10)
		self._widgets['interactive.startButton'].grid(row=2, column=0)
		self._widgets['logs.logs'].pack()
		self._widgets['testStatus.currentStatus'].grid(row=0, column=0, sticky='wnse', ipadx = 10, ipady = 10)
		self._widgets['resultList.tree'].grid(row=0, column=0)
		self._widgets['customFrame.message'].grid(row=0, column=0)

		self.init()

		textHandler = TextHandler(self._widgets['logs.logs'])
		logger = logging.getLogger()
		logger.addHandler(textHandler)

		from framework.application import Application
		self.ots = Application()
		self.ots.station.addDriver(MqttClient("MqttClient1"))
		self.ots.station.addDriver(JLinkExe("JLinkExe1"))
		
	def init(self):
		# TODO dynamic import of values
		self._widgets['interactive.sequenceList'].configure(value= ['OLC NEMA PP - full test'])
			
	def initializeResultListTree(self):
		resultListTree = ttk.Treeview(self._frames['resultList'], style='Custom.Treeview')
		resultListTree.config(
			columns=('stepName', 'stepType', 'value', 'limits', 'result', 'timestamp'), height=20)
		
		resultListTree.heading('#0', text='')
		resultListTree.heading('stepName', text='Step Name')
		resultListTree.heading('stepType', text='Type')
		resultListTree.heading('value', text='Value')
		resultListTree.heading('limits', text='Limits')
		resultListTree.heading('result', text='Result')
		resultListTree.heading('timestamp', text='Timestamp')
		
		resultListTree.column('#0', width=0)
		resultListTree.column('stepName', width=350)
		resultListTree.column('stepType', width=90)
		resultListTree.column('value', width=100)
		resultListTree.column('limits', width=140)
		resultListTree.column('result', width=80)
		resultListTree.column('timestamp', width=120)
		
		return resultListTree

	def initializeStatisticsFrame(self):
		#self._widgets['statistics.statistics'] = \
		#	ttk.Label(self._frames['statistics'], text = 'PASSED: {}\nFAILED: {}\nTOTAL: {}'.format(1,2,3), background = 'yellow')
		self._widgets['statistics.canvas'] = Canvas(self._frames['statistics'], width=510, background='white', bd=0, highlightthickness=0, relief='ridge')
		self._widgets['statistics.passed'] = self._widgets['statistics.canvas'].create_oval(0, 100, 100, 200, outline='light green', fill='light green')
		self._widgets['statistics.failed'] = self._widgets['statistics.canvas'].create_oval(200, 100, 300, 200, outline='red', fill='red')
		self._widgets['statistics.total'] = self._widgets['statistics.canvas'].create_oval(400, 100, 500, 200, outline='grey', fill='grey')
		self._widgets['statistics.passedCount'] = self._widgets['statistics.canvas'].create_text(50, 150, fill= "white", font=('Arial', 20, 'bold'), text="0")
		self._widgets['statistics.failedCount'] = self._widgets['statistics.canvas'].create_text(250, 150, fill= "white", font=('Arial', 20, 'bold'), text="0")
		self._widgets['statistics.totalCount'] = self._widgets['statistics.canvas'].create_text(450, 150, fill= "white", font=('Arial', 20, 'bold'), text="0")
		self._widgets['statistics.passedLabel'] = self._widgets['statistics.canvas'].create_text(50, 80, fill= "light green", font=('Arial', 20, 'bold'), text="OK")
		self._widgets['statistics.failedLabel'] = self._widgets['statistics.canvas'].create_text(250, 80, fill= "red", font=('Arial', 20, 'bold'), text="NOK")
		self._widgets['statistics.totalLabel'] = self._widgets['statistics.canvas'].create_text(450, 80, fill= "grey", font=('Arial', 20, 'bold'), text="Total")

		#self._widgets['statistics.statistics'].grid(row=0, column=0)
		self._widgets['statistics.canvas'].grid(row=0,column=0)

		self._frames['statistics'].grid_rowconfigure(0, weight=1)
		self._frames['statistics'].grid_columnconfigure(0, weight=1)
		#self._frames['statistics'].grid_columnconfigure(1, weight=1)


	
	
	def callback_startButtonClick(self):

		sequenceName = self._widgets['interactive.sequenceList'].get()
		if not sequenceName:
			self._widgets['message.message']['text'] = 'No sequence selected'
			return

		self._widgets['message.message']['text'] = ''
		self._frames['interactive'].grid_forget()
		logging.debug('Chosen sequence: {}'.format(sequenceName))

		from framework.gui_result_list import GuiResultList
		resultList1 = GuiResultList()
		resultList1.bindGui(self, self._widgets['resultList.tree'])
		sequence1 = self.ots.sequences[sequenceName](self.ots.station, sequenceName, resultList1, self)

		from framework.test import Test
		self.ots.test = Test(sequence1, resultList1)
		self.ots.testThread = threading.Thread(target=lambda: self.ots.test.run())
		self.ots.testThread.start()

	def callback_quitButtonClick(self):
		if messagebox.askokcancel("Quit", "Do you want to quit?"):
			if self.ots.testThread and self.ots.testThread.isAlive():
				logging.debug("Exiting while test thread is active")
				self.ots.test.sequence.requestTerminate()
			time.sleep(0.1)
			self._root.destroy()
			self._root = None

	def displaySequenceChoice(self):
		if self._root:
			self._frames['customFrame'].grid_forget()
			self._frames['interactive'].grid(row=1, column=0, columnspan=2)


	def displayCustomMessage(self, type, displayText):
		if self._root:
			self._widgets['customFrame.message'].config(text= displayText)
			self._frames['interactive'].grid_forget()
			self._frames['customFrame'].grid(row=0, column=0, columnspan=2)

	def updateTestStatus(self, text, bgcolor = None):
		if self._root:
			self._widgets['testStatus.currentStatus']['text'] = text
			if bgcolor:
				self._widgets['testStatus.currentStatus'].config(background = bgcolor)

	def incrementStatistics(self, widgetName):
		actual = int(self._widgets['statistics.canvas'].itemcget(self._widgets[widgetName], 'text'))
		self._widgets['statistics.canvas'].itemconfigure(self._widgets[widgetName], text=str(actual+1))

	def incrementPassedStatistics(self):
		self.incrementStatistics('statistics.passedCount')
		self.incrementStatistics('statistics.totalCount')

	def incrementFailedStatistics(self):
		self.incrementStatistics('statistics.failedCount')
		self.incrementStatistics('statistics.totalCount')





from sequences import *

def main():
	gui = Gui()
	gui._root.protocol("WM_DELETE_WINDOW", gui.callback_quitButtonClick)
	gui._root.mainloop()
	
if __name__ == "__main__": main()