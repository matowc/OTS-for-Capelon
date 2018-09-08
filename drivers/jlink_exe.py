import logging
import os
import subprocess

from drivers.driver import Driver

class JLinkExe(Driver):
	
	def __init__(self, name, configFilepath=None):
		super().__init__(name, configFilepath)
		self._JLinkExePath = "/opt/SEGGER/JLink/JLinkExe"

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
	
	def program(self, scriptPath):
		result = subprocess.run([self._JLinkExePath, '-CommandFile', scriptPath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		# consider replacing with check_errors method and catching exception
		if result.returncode == 0:
			return True
		else:
			logging.warning(result.stdout)
			return False

def main():
	jlinkexe = JLinkExe('JLinkExe1', 'EFR32FG12PXXXF1024')
	jlinkexe.program('programming_script.txt')
	pass

if __name__ == "__main__" : main()
