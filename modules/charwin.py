# -*- coding: utf-8 -*-
'''
	Module contains symbol edit dialog window
'''
from qt import *
from globals import *
from picturetable import *
from icons import *

class CharWindow(QDialog):
	'''
	class 
	'''
	def __init__(self,parent = None, fontW=0, fontH=0, dotSize=0):
		'''
		Creates new character edit window
		parent - parent object
		fontW - width of the font in pixels
		fontH - height of the font in pixels
		dotSize - size of point (in pixels) in character edit window
		'''
		QDialog.__init__(self,parent,'CharWindow')
		
		self._fontW = fontW
		self._fontH = fontH
		self._dotSize = dotSize
		
		self._initForm()
		self._initActions()
		self.languageChange()
		
		
	def _initForm(self):
		self._buttonUp = QPushButton(self,"_buttonUp")
		self._buttonUp.setPixmap(getIcon('Up'))
		self._buttonUp.setMinimumSize(80,20)
		self._buttonUp.setMaximumSize(80,20)
		
		self._buttonDown = QPushButton(self,"_buttonDown")
		self._buttonDown.setPixmap(getIcon('Down'))
		self._buttonDown.setMinimumSize(80,20)
		self._buttonDown.setMaximumSize(80,20)
		
		self._buttonLeft = QPushButton(self,"_buttonLeft")
		self._buttonLeft.setPixmap(getIcon('Left'))
		self._buttonLeft.setMinimumSize(20,80)
		self._buttonLeft.setMaximumSize(20,80)
		
		self._buttonRight = QPushButton(self,"_buttonRight")
		self._buttonRight.setPixmap(getIcon('Right'))
		self._buttonRight.setMinimumSize(20,80)
		self._buttonRight.setMaximumSize(20,80)
		
		self._buttonRotV = QPushButton(self,"_buttonRotV")
		self._buttonRotV.setPixmap(getIcon('RotV'))
		self._buttonRotV.setMinimumSize(50,30)
		self._buttonRotV.setMaximumSize(50,30)
		
		self._buttonRotH = QPushButton(self,"_buttonRotH")
		self._buttonRotH.setPixmap(getIcon('RotH'))
		self._buttonRotH.setMinimumSize(50,30)
		self._buttonRotH.setMaximumSize(50,30)
		
		self._buttonOk = QPushButton(self,"_buttonOk")
		self._buttonOk.setDefault(1)
		self._buttonOk.setMinimumSize(80,30)
		self._buttonOk.setMaximumSize(80,30)
		
		self._buttonCancel = QPushButton(self,"_buttonCancel")
		self._buttonCancel.setMinimumSize(80,30)
		self._buttonCancel.setMaximumSize(80,30)
		
		self._charTable = PictureTable(self,self._fontW, self._fontH, self._dotSize)
		
		self._slider =QSlider(self, '_slider')
		self._slider.setOrientation(Qt.Horizontal)
		self._slider.setMinValue(0)
		self._slider.setMaxValue(self._fontW)
		self._slider.setTickmarks(QSlider.Above)
		self._slider.setMinimumSize(self._charTable.minimumWidth(),30)
		self._slider.setMaximumSize(self._charTable.maximumWidth(),30)
		
		lMain = QVBoxLayout(self, 10)
		lbU = QGridLayout(lMain,1,3,10)
		lbU.addWidget(self._buttonUp,0,1)
		lM = QHBoxLayout(lMain,10)
		lM.addWidget(self._buttonLeft)
		lM.addWidget(self._charTable)
		lM.addWidget(self._buttonRight)
		lbD = QGridLayout(lMain,1,5,10)
		lbD.addWidget(self._buttonRotV,0,0)
		lbD.addWidget(self._buttonRotH,0,4)
		lbD.addWidget(self._buttonDown,0,2)
		lS = QGridLayout(lMain,1,3)
		lS.addWidget(self._slider,0,1)
		lbOC = QGridLayout(lMain,1,5,10)
		lbOC.addWidget(self._buttonOk,0,0)
		lbOC.addWidget(self._buttonCancel,0,4)
		
		
	def _initActions(self):
		self.connect(self._buttonOk,SIGNAL("clicked()"),self.accept)
		self.connect(self._buttonCancel,SIGNAL("clicked()"),self.reject)
		self.connect(self._buttonDown,SIGNAL("clicked()"),self._charTable.shiftDown)
		self.connect(self._buttonLeft,SIGNAL("clicked()"),self._charTable.shiftLeft)
		self.connect(self._buttonRight,SIGNAL("clicked()"),self._charTable.shiftRight)
		self.connect(self._buttonUp,SIGNAL("clicked()"),self._charTable.shiftUp)
		self.connect(self._slider,SIGNAL("valueChanged(int)"),self._charTable.setPictureWidth)
		self.connect(self._buttonRotV,SIGNAL("clicked()"),self._charTable.rotateV)
		self.connect(self._buttonRotH,SIGNAL("clicked()"),self._charTable.rotateH)
		
		
	def languageChange(self):
		self.setCaption(self.__tr("Edit symbol"))
		self._buttonOk.setText(self.__tr("Ok"))
		self._buttonCancel.setText(self.__tr("Cancel"))
		QWhatsThis.add(self._buttonUp,self.__tr('Shifts char to top'))
		QWhatsThis.add(self._buttonDown,self.__tr('Shifts char to bottom'))
		QWhatsThis.add(self._buttonLeft,self.__tr('Shifts char to left'))
		QWhatsThis.add(self._buttonRight,self.__tr('Shift char to right'))
		QWhatsThis.add(self._buttonRotV,self.__tr('Mirrors char in vertical'))
		QWhatsThis.add(self._buttonRotH,self.__tr('Mirrors char in horizontal'))
		QWhatsThis.add(self._slider,self.__tr('Set width of char'))
		
		
	def __tr(self,s,c = None):
		return qApp.translate("CharWindow",s,c)
		
		
	def setChar(self, char):
		'''
		Receives symbol, that will be edit
		char - tupple with two parameters
		0 - bytesring with symbol data
		1 - integer width of the symbol
		'''
		self._slider.setValue(char[1])
		self._charTable.setPicture((char[0], char[1]))
		
		
	def getChar(self):
		'''
		Returns symbol
		returns tupple with two parameters
		0 - bytesring with symbol data
		1 - integer width of the symbol
		'''
		return self._charTable.getPicture()
	
