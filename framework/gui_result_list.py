import logging
from framework import *
from framework.result import *
from framework.gui import Gui


from tkinter import *
from tkinter import ttk


class GuiResultList(ResultList):

	def __init__(self) :
		super().__init__()
		self.gui = None
		self._resultListTree = None
		logging.info("ResultList initialized")
		
	def bindGui(self, gui : Gui, resultListTreeWidget : ttk.Treeview):
		self.gui = gui
		self._resultListTree = resultListTreeWidget
		self._resultListTree.tag_configure('PASSED', background='green')
		self._resultListTree.tag_configure('FAILED', background='red')
		self._resultListTree.tag_configure('DONE', background='#99FF33')
	
	def add (self, result: Result):
		super().add(result)
		
		self._resultListTree.insert('', 'end', text=result.step.name,
									values=('', result.step.name, result.step.type.name, result.value, result.step.limits, result.status.name, result.timestamp),
									tags = (result.status.name))

		# returns
		pass



def main():
	pass


if __name__ == "__main__" : main()