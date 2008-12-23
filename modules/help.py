# -*- coding: utf-8 -*-

import os
from globals import *
from prefs import *
from qt import *
import webbrowser


def showHelp(prefs):
	fname = prefs.get('help')
	webbrowser.open(fname)


class HelpWindow (QDialog):
	def __init__ (self, parent = None):
		QDialog.__init__(self, parent)
		
		self._initForm()
		self._initActions()
		
		self._browser = QTextBrowser(self)
		
		
		
		self._browser.show()

		
	def _InitForm (self):
		pass
		
	def _initActions (self):
		pass
