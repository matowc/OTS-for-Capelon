import logging
import os
import subprocess

from drivers.driver import Driver

class JLinkExe(Driver):
	
	def __init__(self, name):
		# for debuggig

		
		self._JLinkExePath = "/opt/SEGGER/JLink/JLinkExe"
		self._scriptPath = ""
		self._device = "d"
		
		super().__init__(name)
	
	def __del__(self):
		self.deinitialize()
	
	def initialize(self):
		pass
	
	def deinitialize(self):
		pass
	
	def loadConfiguration(self):
		# replace with loading from .ini file
		pass
	
	def safeReset(self):
		pass
	
	def program(self):
		result = subprocess.run([self._JLinkExePath, '-device', self._device, '-CommandFile', self._scriptPath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		# consider replacing with check_errors method and catching exception
		if result.returncode == 0:
			return True
		else:
			logging.warning(result.stdout)
			return False
		


def main():
	# jlinkexe = JLinkExe('j')
	# jlinkexe.program()
	pass

if __name__ == "__main__" : main()
