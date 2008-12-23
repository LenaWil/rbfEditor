# -*- coding: utf-8 -*-

import array
from qt import *
import Image
import ImageFont
import ImageTransform
import ImageChops
import rebUtils
from globals import *
from fontprefs import *
from fonttable import *
from bookpreview import *

class FontWindow(QWidget):
	def __init__(self,parent=None, prefs=None, action=None, var1=None, var2=None):
		QWidget.__init__(self,parent)
		self._parent = parent
		self._prefs = prefs
		self._changes = 0
		self._fontFileName = ''
		self._isPreviewEnabled = self._prefs.get('previewenabled')		
		self._layout = QHBoxLayout(self,10)
		
		if action == RBF_NEW:
			self._font = self._new()
		elif action == RBF_OPEN:
			self._font = self._open(var1)
		elif action == RBF_TTF:
			self._font = self._ttf(var1, var2)
		else:
			self._font = None
			
		if self._font != None:
			self._initAll()
			if action != RBF_OPEN:
				self._setChanged(TRUE)
			else:
				self._setChanged(FALSE)
		
		
	def _initAll (self):
		self._initForm()
		self._initActions()
		self.languageChange()
		self._charTable.show()
		self._labelPreview.show()
		
		
	def _initForm (self):
		try:
			self.removeChild(self._charTable)
			self.removeChild(self._labelPreview)
			del self._charTable
			del self._labelPreview
		except:
			pass
			
		self._charTable = FontTable(self, self._prefs, self._font)
		self._labelPreview = BookPreview(self, self._prefs, self._font, self._charTable)
		self._layout.addWidget(self._charTable)
		self._layout.addWidget(self._labelPreview, 0, Qt.AlignTop)
		
		
	def _initActions(self):
		self.connect(self._charTable,PYSIGNAL('FontChanged'),self._fontChanged)
		
		
	def languageChange(self):
		self.setCaption("rbfEdit")
		
		
	def __tr(self,s,c = None):
		return qApp.translate("rbfEdit",s,c)
		
		
	def isOk(self):
		if self._font != None:
			isOk = TRUE
		else:
			isOk = FALSE
		return isOk
		
		
	def getName(self):
		return self._font.name
		
		
	def getFileName(self):
		return self._fontFileName
		
		
	def isChanged(self):
		if self._changes == 0 :
			changed = FALSE
		else :
			changed = TRUE
		return changed
		
		
	def _setChanged(self, changed):
		if changed :
			self._changes += 1
		else :
			self._changes = 0
			
		if self._isPreviewEnabled:
			self.showText()
		
		self.emit(PYSIGNAL('FontChanged'),(self.isChanged(),))
		
		
	def _new(self):
		propDialog = FontPropertyDialog(self)
		if propDialog.exec_loop() == QDialog.Accepted:
			font = rebUtils.fontCreate(propDialog.textName.text().ascii(),\
										propDialog.spinW.value(),\
										propDialog.spinH.value(),\
										propDialog.spinIntline.value())
		else:
			font = None
		propDialog.close()
		return font
		
		
	def _open(self, fontFileName):
		font = rebUtils.fontLoad(fontFileName)
		self._fontFileName = fontFileName
		return font
		
		
	def old_ttf(self, ttfFile, ttfSize):
		ttfFont = ImageFont.truetype(ttfFile, ttfSize)
		ttfName = ttfFont.getname()
		fontName = ttfName[0] + ',' + ttfName[1]+ ' ' + str(ttfSize) + 'pt'
		
		charString = self._prefs.get('codetable')
		charMask = []
		charSize = []
		charOffset = []
		
		for char in charString:
			offset = ttfFont.getmask2(char,'1')[1]
			if (offset[0] == 0):
				charSize.append(ttfFont.getsize(char))
				charMask.append(ttfFont.getmask2(char,'1')[0])
			else:
				charSize.append(ttfFont.getsize(u' ' + char))
				charMask.append(ttfFont.getmask2(u' ' + char,'1')[0])
			
		fontW = 0
		fontH = 0
		for index in xrange(len(charString)):
			fontW = max(fontW, charSize[index][0])
			fontH = max(fontH, charSize[index][1])
		if fontW % 8 != 0 :
			fontW = 8*(fontW /8 + 1)
		font = rebUtils.fontCreate(fontName, fontW, fontH, 2, 32, len(charString))
		
		font.cTable = []
		font.wTable = []
		
		for index in xrange(len(charString)):
			byteArray = array.array('B')
			for bytes in xrange(fontW*fontH/8):
				byteArray.append(0)
			for row in xrange(charSize[index] [1]):
				for col in xrange(charSize[index] [0]):
					value = charMask[index][row*charSize[index] [0]+col] & 1
					byte = row*fontW/8+col/8
					bit = col%8
					byteArray[byte] += value*(2**bit)
						
			font.cTable.append(byteArray.tostring())	
			font.wTable.append(charSize[index][0])
		
		metrics = ttfFont.getmetrics()
		font.descent = metrics[1]
		
		return font
		
		
	def _ttf(self, ttfFile, ttfSize):
		ttfFont = ImageFont.truetype(ttfFile, ttfSize)
		ttfName = ttfFont.getname()
		fontName = ttfName[0] + ',' + ttfName[1]+ ' ' + str(ttfSize) + 'pt'
		
		charString = self._prefs.get('codetable')
		charMask = []
		charSize = []
		charOffset = []
		
		for char in charString:
			offset = ttfFont.getmask2(char,'1')[1]
			if (offset[0] == 0):
				charSize.append(ttfFont.getsize(char))
				charMask.append(ttfFont.getmask2(char,'1')[0])
			else:
				charSize.append(ttfFont.getsize(u' ' + char))
				charMask.append(ttfFont.getmask2(u' ' + char,'1')[0])
		fontW = 0
		fontH = 0
		for index in xrange(len(charString)):
			fontW = max(fontW, charSize[index][0])
			fontH = max(fontH, charSize[index][1])
		if fontW % 8 != 0 :
			fontW = 8*(fontW /8 + 1)
		font = rebUtils.fontCreate(fontName, fontW, fontH, 2, 32, len(charString))
		
		font.cTable = []
		font.wTable = []
		
		for index in xrange(len(charString)):
			byteArray = array.array('B')
			for bytes in xrange(fontW*fontH/8):
				byteArray.append(0)
			for row in xrange(charSize[index] [1]):
				for col in xrange(charSize[index] [0]):
					value = charMask[index][row*charSize[index] [0]+col] & 1
					byte = row*fontW/8+col/8
					bit = col%8
					byteArray[byte] += value*(2**bit)
					
			image = Image.fromstring('1', (fontW, fontH), byteArray.tostring(), "raw", "1;R")
			boundBox = image.getbbox()
			width = charSize[index][0]
			if boundBox != None:
				width = boundBox[2] - boundBox[0] + 1
				shift = boundBox[0]
				shiftTransformation = ImageTransform.AffineTransform((1, 0, shift, 0, 1, 0))
				image = image.transform((fontW, fontH), shiftTransformation)
			font.cTable.append(image.tostring("raw", "1;R"))	
			font.wTable.append(width)
		
		metrics = ttfFont.getmetrics()
		font.descent = metrics[1]
		
		return font
		
		
	def save(self, fileName=None):
		if fileName == None:
			if self._fontFileName != '' :
				rebUtils.fontSave(self._font, self._fontFileName)
				self._setChanged(FALSE)
		else:
			rebUtils.fontSave(self._font, fileName)
			self._fontFileName = fileName
			self._setChanged(FALSE)
		
		
	def changeFontProperty(self):
		propDialog = FontPropertyDialog(self)
		propDialog.textName.setText(QString(self._font.name))
		propDialog.spinH.setValue(self._font.height)
		propDialog.spinW.setValue(self._font.width)
		propDialog.spinPoints.setValue(self._font.points)
		propDialog.spinIntline.setValue(self._font.intline)
		propDialog.spinCount.setValue(self._font.charCount)
		changed = FALSE
		needNewTab = FALSE
		
		if propDialog.exec_loop() == QDialog.Accepted:
			name = propDialog.textName.text().ascii()
			fontH = propDialog.spinH.value()
			fontW = propDialog.spinW.value()
			intline = propDialog.spinIntline.value()
		
			if len(name) >= 64:
				name = name[0:64]
			if self._font.name != name :
				self._font.name = name
				changed = TRUE
		
			if intline != self._font.intline :
				self._font.intline = intline
				changed = TRUE
			
			if fontW < self._font.width:
				oldWB = self._font.width / 8
				newWB = fontW / 8
				for charCode in xrange(self._font.charCount):
					char = self._font.getChar(charCode)[0]
					newWidth = self._font.getChar(charCode)[1]
					newChar = ''
					for row in xrange(self._font.height):
						newChar += char[row*oldWB:row*oldWB+newWB]
					if newWidth > fontW:
						newWidth = fontW
					self._font.setChar(charCode, (newChar, newWidth))
				self._font.width = fontW
				changed = TRUE
			elif fontW > self._font.width:
				oldWB = self._font.width / 8
				newWB = fontW / 8
				for charCode in xrange(self._font.charCount):
					char = self._font.getChar(charCode)[0]
					newWidth = self._font.getChar(charCode)[1]
					newChar = ''
					for row in xrange(self._font.height):
						newChar += char[row*oldWB:(row+1)*oldWB] + (newWB-oldWB)*'\x00'
					self._font.setChar(charCode, (newChar, newWidth))
				self._font.width = fontW
				changed = TRUE
			
			if fontH < self._font.height:
				diffH = self._font.height - fontH
				newtop = diffH*(self._font.width/8)
				for index in xrange(self._font.charCount):
					self._font.cTable[index] = self._font.cTable[index][newtop:]
				self._font.height = fontH
				self._font.points = int(self._font.height*72.0/106.0)
				changed = TRUE
			elif fontH > self._font.height:
				diffH = fontH - self._font.height
				newbytes = diffH * (self._font.width/8) * '\x00'
				for index in xrange(self._font.charCount):
					self._font.cTable[index] = newbytes + self._font.cTable[index]
				self._font.height = fontH
				self._font.points = int(self._font.height*72.0/106.0)
				changed = TRUE
			
		if changed :
			self._initAll()
			self._setChanged(TRUE)
		
		propDialog.close()
		del propDialog
		
	
	
	def _fontChanged (self, event):
		self._setChanged(TRUE)

	def previewEnabled (self):
		return self._isPreviewEnabled
		
		
	def showText(self):
		self._labelPreview.showText()
		
	
	def makeItalic (self):
		for index in xrange(self._font.charCount):
			fontW = self._font.width
			fontH = self._font.height
			width = self._font.getChar(index)[1]
			shift = width*0.25
			image = Image.fromstring('1', (fontW, fontH), self._font.getChar(index)[0], "raw", "1;R")
#			transformation = ImageTransform.AffineTransform((1, 0.25, -shift, 0, 1, 0))
			transformation = ImageTransform.AffineTransform((1, 0.25, -fontH*0.25*0.75, 0, 1, 0))
			image = image.transform((fontW, fontH), transformation, resample=Image.BICUBIC)
			x = image.getbbox()
			if x != None:
				width = x[2]
			self._font.setChar(index, (image.tostring("raw", "1;R"), width))
		self._setChanged(TRUE)
		self._charTable.show()
		self.showText()
		
		
	def makeBold (self):
		fontW = self._font.width
		fontH = self._font.height
		for index in xrange(self._font.charCount):
			width = self._font.getChar(index)[1]
			image = Image.fromstring('1', (fontW, fontH), self._font.getChar(index)[0], "raw", "1;R")
			imageShifted = ImageChops.offset(image, 1, 0)
			image = ImageChops.logical_or(image, imageShifted)
			x = image.getbbox()
			if x != None:
				width = x[2]
			self._font.setChar(index, (image.tostring("raw", "1;R"), width+1))
		self._setChanged(TRUE)
		self._charTable.show()
		self.showText()
	
	
