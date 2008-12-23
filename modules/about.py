# -*- coding: utf-8 -*-

from qt import *

from globals import *


class AboutDialog(QDialog):
	def __init__(self,parent = None, prefs = None):
		QDialog.__init__(self,parent,"AboutDialog")
	
		self._parent = parent
		self._prefs = prefs
		self._initForm()
		self._initActions()
		self.languageChange()
		
		self._textLicense.setText(self._prefs.get('license'))
	
	
	def _initForm(self):
		self.setSizeGripEnabled(TRUE)
	
		self._tabs = QTabWidget(self,"tabs")
		self._tabAbout = QWidget(self._tabs,"tabAbout")
		self._tabLicense = QWidget(self._tabs,"tabLicense")
		self._tabs.insertTab(self._tabAbout,QString.fromLatin1(""))
		self._tabs.insertTab(self._tabLicense,QString.fromLatin1(""))
	
		self._labelDesc = QLabel(self._tabAbout,"labelDesc")
		self._labelDesc.setAlignment(Qt.AlignCenter)
	
		self._textLicense = QTextEdit(self._tabLicense,"textLicense")
		self._textLicense.setPaletteBackgroundColor(QColor(230,230,230))
		self._textLicense.setReadOnly(1)
	
		self._buttonOk = QPushButton(self,"buttonOk")
		self._buttonOk.setMinimumSize(QSize(100,30))
		self._buttonOk.setMaximumSize(QSize(100,30))
		self._buttonOk.setAutoDefault(1)
		self._buttonOk.setDefault(1)
		
		lTabA = QGridLayout(self._tabAbout,3, 3, 10, 10)
		lTabA.addWidget(self._labelDesc, 1, 1)
		lTabL = QGridLayout(self._tabLicense,3, 3, 0)
		lTabL.addWidget(self._textLicense, 1, 1)
		lMain = QVBoxLayout(self,10,10)
		lMain.addWidget(self._tabs)
		lMain.addWidget(self._buttonOk, 0, QBoxLayout.AlignRight)
		
		self.resize(QSize(387,319).expandedTo(self.minimumSizeHint()))
		self.clearWState(Qt.WState_Polished)
	
	
	def _initActions(self):
		self.connect(self._buttonOk,SIGNAL("clicked()"),self.accept)
	
	
	def languageChange(self):
		self.setCaption(self.__tr("About rbfEditor"))
		self._labelDesc.setText(self.__tr("rbfEditor - REB 1100 font converter and editor.\nConvert unicode tryetype fonts to reb fonts\n\nversion 0.2\n\n(C) 2006,2008 Andrew Mochalov\navmae@mail.ru"))
		self._tabs.changeTab(self._tabAbout,self.__tr("About"))
		self._tabs.changeTab(self._tabLicense,self.__tr("License"))
		self._buttonOk.setText(self.__tr("Close"))
		self._buttonOk.setAccel(QString.null)
	
	
	def __tr(self,s,c = None):
		return qApp.translate("AboutDialog",s,c)
	
	
	


	
	
	


	


