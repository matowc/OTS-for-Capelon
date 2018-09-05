import logging
from framework import *
from framework.result import *
from framework.gui import Gui


from tkinter import *
from tkinter import ttk


class GuiResultList(ResultList):

	def __init__(self):
		super().__init__()
		self.gui = None
		self._resultListTree = None
		logging.info("ResultList initialized")
		
	def bindGui(self, gui : Gui, resultListTreeWidget : ttk.Treeview):
		self.gui = gui
		self._resultListTree = resultListTreeWidget
		self._resultListTree.tag_configure('PASSED', background=self.gui.colors['green'])
		self._resultListTree.tag_configure('FAILED', background=self.gui.colors['red'])
		self._resultListTree.tag_configure('DONE', background=self.gui.colors['light green'])
		self._resultListTree.tag_configure('result', font=('Arial', 8))
	
	def add(self, result: Result):
		super().add(result)

		#secs, msecs = divmod(result.relativeTimestamp, 1)
		#msecs = msecs * 1000
		secs = result.relativeTimestamp
		mins, secs = divmod(secs, 60)
		self._resultListTree.insert('', 'end', text=result.step.name,
									values=(result.step.name, result.step.type.name, result.value, result.step.limits, result.status.name, '{:0>2.0f}:{:0>6.3f}'.format(mins, secs)),
									tags = (result.status.name, 'result') )

		# returns
		pass

	def clear(self):
		super().clear()
		if self.gui:
			self._resultListTree.delete(*self._resultListTree.get_children())


def main():
	pass


if __name__ == "__main__" : main()