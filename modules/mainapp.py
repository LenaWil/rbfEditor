# -*- coding: utf-8 -*-

from mainwin import *
from prefs import *
	
class Application (QApplication):
	def __init__ (self, args):
		QApplication.__init__(self, args)
		self.prefs = Preferences()
		self.mainWindow = MainWindow(self.prefs)
		self.setMainWidget(self.mainWindow)
		self.translator = QTranslator()
		
		QObject.connect(self,SIGNAL("lastWindowClosed()"),self,SLOT("quit()"))
		self.connect(self.mainWindow,PYSIGNAL('LanguageChanged'),self.languageChange)
		
		self.languageChange(TRUE)
		self.mainWindow.show()
		
		
	def languageChange(self, event):
		self.translator.clear()
		self.translator.load(self.prefs.get('translator'))
		self.installTranslator(self.translator)
		self.mainWindow.languageChange()
