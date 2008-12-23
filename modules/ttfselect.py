# -*- coding: utf-8 -*-

import os
import operator, re
import string
import Image, ImageDraw, ImageFont

from qt import *
from qtcanvas import *
from globals import *

class FontDialog(QDialog):
	def __init__(self, parent = None, prefs = None):
		QDialog.__init__(self, parent)
		self.setName("FontDialog")
		self._parent = parent
		self._fontName = {}
		self._fontFile = {}
		self._fontDir = prefs.get('fontdir')

		self._sample = None
		
		self._initForm()
		self._initActions()
		self.languageChange()
		
		self._listFont.clear()
		self._listStyle.clear()
		self._listSize.clear()
			
		if os.access(self._fontDir, os.R_OK):
			tempList = os.listdir(self._fontDir)
		else:
			tempList = []
		fontList = []
		for font in tempList:
			if operator.truth(re.match('.*\.ttf$',font,re.I)):
				fontList.append(self._fontDir+'/'+font)
			
		for file in fontList:
			font = ImageFont.truetype(file,10)
			fname = font.getname()
			self._fontFile[fname[0]+fname[1]] = file
			if self._fontName.has_key(fname[0]):
				tempList = self._fontName[fname[0]]
				tempList.append(fname[1])
				self._fontName[fname[0]] = tempList
			else:
				tempList = []
				tempList.append(fname[1])
				self._fontName[fname[0]] = tempList

		tempList  = []
		for name in self._fontName.items():
			tempList.append(name)
		tempList.sort()
		for name in tempList:
			self._listFont.insertItem(QString(name[0]))
			
		for size in xrange(8,21):
			self._listSize.insertItem(QString(str(size)))
		
		if self._listFont.count() > 0:
			self._listFont.setCurrentItem(0)
		if self._listStyle.count() > 0:
			self._listStyle.setCurrentItem(0)
		if self._listSize.count() > 5:
			self._listSize.setCurrentItem(4)
			
	
	def _initForm(self):
		lMain = QWidget(self,"lButtons")
		lMain.setGeometry(QRect(20,280,430,35))
		lButtons = QHBoxLayout(lMain,0,10,"lButtons")

		spacer = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
		lButtons.addItem(spacer)
	
		self._buttonOk = QPushButton(lMain,"buttonOk")
		self._buttonOk.setAutoDefault(TRUE)
		self._buttonOk.setDefault(1)
		self._buttonOk.setMinimumSize(80, 30)
		lButtons.addWidget(self._buttonOk)
	
		self._buttonCancel = QPushButton(lMain,"buttonCancel")
		self._buttonCancel.setAutoDefault(1)
		self._buttonCancel.setMinimumSize(80, 30)
		lButtons.addWidget(self._buttonCancel)
	
		self._listFont = QListBox(self,"listFont")
		self._listFont.setGeometry(QRect(30,40,200,170))
		self._listFont.setVScrollBarMode(QListBox.AlwaysOn)
		self._listFont.setHScrollBarMode(QListBox.AlwaysOff)
	
		self._labelFont = QLabel(self,"labelFont")
		self._labelFont.setGeometry(QRect(30,10,200,20))
		self._labelFont.setAlignment(QLabel.AlignCenter)
	
		self._listStyle = QListBox(self,"listStyle")
		self._listStyle.setGeometry(QRect(265,40,80,170))
		self._listStyle.setVScrollBarMode(QListBox.AlwaysOff)
		self._listStyle.setHScrollBarMode(QListBox.AlwaysOff)
	
		self._labelStyle = QLabel(self,"labelStyle")
		self._labelStyle.setGeometry(QRect(265,10,80,20))
		self._labelStyle.setAlignment(QLabel.AlignCenter)
	
		self._editSize = QLineEdit(self,"editSize")
		self._editSize.setGeometry(QRect(380,40,60,20))
	
		self._listSize = QListBox(self,"listSize")
		self._listSize.setGeometry(QRect(380,70,60,140))
		self._listSize.setVScrollBarMode(QListBox.AlwaysOn)
		self._listSize.setHScrollBarMode(QListBox.AlwaysOff)
	
		self._labelSize = QLabel(self,"labelSize")
		self._labelSize.setGeometry(QRect(380,10,50,20))
		self._labelSize.setAlignment(QLabel.AlignCenter)
	
		
		self._boxSample = QGroupBox(self, "boxSample")
		self._boxSample.setGeometry(QRect(10,215,440,60))
		
		self._labelSample = QLabel(self._boxSample,"labelSample")
		self._labelSample.setGeometry(QRect(5,15,420,30))
	
		self.setMinimumSize(460, 330)
		self.setMaximumSize(460, 330)
	
	
	def _initActions(self):
		self.connect(self._buttonOk,SIGNAL("clicked()"),self.accept)
		self.connect(self._buttonCancel,SIGNAL("clicked()"),self.reject)
		self.connect(self._listFont,SIGNAL("currentChanged(QListBoxItem*)"),self._changedFont)
		self.connect(self._listStyle,SIGNAL("currentChanged(QListBoxItem*)"),self._changedStyle)
		self.connect(self._listSize,SIGNAL("currentChanged(QListBoxItem*)"),self._changedSize)
		self.connect(self._editSize,SIGNAL("textChanged(const QString&)"),self._setSize)
	
	
	def languageChange(self):
		self.setCaption(self.__tr("ttf font selection"))
		self._buttonOk.setText(self.__tr("OK"))
		self._buttonCancel.setText(self.__tr("Cancel"))
		self._labelFont.setText(self.__tr("Font"))
		self._labelSize.setText(self.__tr("Size"))
		self._labelStyle.setText(self.__tr("Style"))
		self._fontString = self.__tr('The quick brown fox jumps over the lazy dog')
		self._boxSample.setTitle("Sample")
	
	
	def __tr(self,s,c = None):
		return qApp.translate("ttfSelect",s,c)
	
			
	def _changedFont(self):
		self._listStyle.clear()
		tempList = []
		for style in self._fontName[unicode(self._listFont.currentText())]:
			tempList.append(style)
		tempList.sort()
		tempList.reverse()
		for style in tempList:
			self._listStyle.insertItem(style)
		self._listStyle.setCurrentItem(0)
		self._showSample()
		
		
	def _changedStyle(self):
		self._showSample()
		
	
	def _changedSize(self):
		self._editSize.setText(self._listSize.currentText())
	
	
	def _setSize(self):
		self._showSample()
	
	
	def getFont(self):
		fontName = unicode(self._listFont.currentText()) + unicode(self._listStyle.currentText())
		fontFile = self._fontFile[fontName]
		fontSize = string.atoi(self._editSize.text().ascii())
		
		return (fontFile, fontSize)
	def _showSample(self):
		self._labelSample.clear()
#		if (unicode(self._listFont.currentText()) == '') or\
#		(unicode(self._listStyle.currentText()) == '') or\
#		(unicode(self._editSize.text()) == '') :
#			return
		
		try:
			font = ImageFont.truetype(self.getFont()[0], self.getFont()[1])
			textSize = font.getsize(unicode(self._fontString))
#		textSize = (self._labelSample.size().width(), self._labelSample.size().height())
		
			pilImage = Image.new('1', textSize, 0)
			pilPainter = ImageDraw.ImageDraw(pilImage, '1')
			pilPainter.setfont(font)
			pilPainter.ink = 1
			pilPainter.text((0,0), unicode(self._fontString))
			byteString = pilImage.tostring()
		
			qText = QBitmap(textSize[0], textSize[1], byteString, FALSE)
			qImage = QBitmap(textSize[0], textSize[1])
			qImage.fill(Qt.color0)
			qPainter = QPainter()
			qPainter.begin(qImage)
			qPainter.setPen(Qt.color1)
			qPainter.drawPixmap(0, 0, qText)
			qPainter.end()
			
			self._labelSample.setPixmap(qImage)
		except:
			pass
#			self._labelSample.setText(self.__tr("Font Error: can't render"))
			

			
