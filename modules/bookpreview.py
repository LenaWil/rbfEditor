# -*- coding: utf-8 -*-

import array
from qt import *
from globals import *

class BookPreview (QLabel):
	def __init__ (self, parent=None, prefs=None, font=None, charTable=None):
		self._parent = parent
		self._prefs = prefs
		self._font = font
		self._charTable = charTable
		self._fontH = self._font.height
		self._fontW = self._font.width
		
		QLabel.__init__(self, parent)
		self.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
		self.setMinimumSize(EBOOKW + 2,EBOOKH + 2)
		self.setMaximumSize(self.minimumSize())
		self.setFrameShape(QFrame.Panel)
		self.setFrameShadow(QFrame.Sunken)
		
		
	def showText (self):
		byteString = array.array('B', self._prefs.get('previewtext'))
		screen = QBitmap(EBOOKW, EBOOKH)
		self.setPaletteBackgroundColor(EBOOKBG)
		screen.fill(Qt.color0)
		painter = QPainter()
		
		pointsH = int((self._font.points*106.0)/72.0)
		lineH = max(self._fontH, pointsH) + self._font.intline
		x = 0
		y = 10
		textPos = 0
		painter.begin(screen)
		painter.setPen(Qt.color1)

		while (y < EBOOKH) & (textPos < len(byteString)):
			byte = byteString[textPos]
			if byte >= self._font.charFirst + self._font.charCount :
				byte = 32
			if byte < 32:
				if byte == 10:
					x = 0
					y = y + lineH
					textPos += 1
					continue
				elif byte == 9:
					byte = 32
				else:
					textPos += 1
					continue
			
			byte = byte - 32
			
			if x + self._font.wTable[byte] >= EBOOKW:
				x = 0
				y = y + lineH
			
			if y + lineH > EBOOKH:
				break
			
			charBitmap = self._charTable.getCharBitmap(byte)
			painter.drawPixmap(x, y, charBitmap)
			x += self._font.wTable[byte]
			textPos += 1
		
		painter.end()
		self.clear()
		self.setPixmap(screen)
		
