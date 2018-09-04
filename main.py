from framework.gui import *
from framework.application import *


gui = Gui()
gui._root.protocol("WM_DELETE_WINDOW", gui.callback_quitButtonClick)
gui._root.mainloop()