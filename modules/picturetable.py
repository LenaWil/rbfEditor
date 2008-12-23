# -*- coding: utf-8 -*-
'''
	Module contains PictureTable class - image editing table
'''
import array
from qt import *
from qttable import *
from globals import *

class PictureTable(QTable):
	'''
		Class PictureTable - QTable ancessor provides simple image
		editing fuctions.
	'''
	def __init__(self, parent=None, width=0, height=0, dotSize=0):
		'''
			Create new class object
		parent - parent object
		width 	- table width (in columns)
		height 	- table heigth (in rows)
		dotSize	- cell size in pixels
		'''
		self._width = width
		self._height = height
		self._pictureWidth = 0
		self._bit1 = QBitmap(dotSize, dotSize, ((dotSize**2)/8)*'\xff',1)
		
		QTable.__init__ (self, parent)
		
		self.setNumRows(self._height)
		self.setNumCols(self._width)
		for index in xrange(self._width):
			self.setColumnWidth(index, dotSize)
		for index in xrange(self._height):
			self.setRowHeight(index, dotSize)
		self.setReadOnly(TRUE)
		self.setSelectionMode(QTable.NoSelection)
		self.setTopMargin(0)
		self.setLeftMargin(0)
		self.setFrameShape(QFrame.NoFrame)
		self.setFrameShadow(QFrame.Plain)
		self.setFocusStyle(QTable.FollowStyle)
		self.setMinimumSize(self._width*dotSize, self._height*dotSize)
		self.setMaximumSize(self._width*dotSize, self._height*dotSize)
		
		self._initActions()
	
	
	def _initActions (self):
		self.connect(self,PYSIGNAL('mousePressed'),self._drawPixel)
		self.connect(self,PYSIGNAL('mouseMove'),self._drawPicture)
		
		
	def contentsMousePressEvent(self, event):
		self.emit(PYSIGNAL('mousePressed'),(event,))
		
		
	def contentsMouseMoveEvent(self, event):
		self.emit(PYSIGNAL('mouseMove'),(event,))
		
		
	def _drawPixel(self,event):
		row = self.rowAt(event.y())
		col = self.columnAt(event.x())
		if event.button() == Qt.LeftButton:
			self.setPixmap(row, col,self._bit1)
			self._drawBit = 1
		elif event.button() == Qt.RightButton:
			self.clearCell(row, col)
			self._drawBit = 0
			
	
	def _drawPicture (self,event):
		row = self.rowAt(event.y())
		col = self.columnAt(event.x())
		if self._drawBit == 1:
			self.setPixmap(row, col,self._bit1)
		elif self._drawBit == 0:
			self.clearCell(row, col)
		
		
	def shiftUp(self):
		'''
		Shifts picture to top of table to one pixel
		'''
		for row in xrange(self._height-1):
			for col in xrange(self._width):
				if self.item(row+1, col):
					self.setPixmap(row, col, self._bit1)
				else:
					self.clearCell(row, col)
		for col in xrange(self._width):
			self.clearCell(self._height-1, col)
		
	
	def shiftDown(self):
		'''
		Shifts picture to bottom of table to one pixel
		'''
		rowRange = range(1,self._height)
		rowRange.reverse()
		for row in rowRange:
			for col in xrange(self._width):
				if self.item(row-1, col):
					self.setPixmap(row, col, self._bit1)
				else:
					self.clearCell(row, col)
		for col in xrange(self._width):
			self.clearCell(0, col)
		
		
	def shiftLeft(self):
		'''
		Shifts picture to left bound of table to one pixel
		'''
		for col in xrange(self._width-1):
			for row in xrange(self._height):
				if self.item(row, col+1):
					self.setPixmap(row, col, self._bit1)
				else:
					self.clearCell(row, col)
		for row in xrange(self._height):
			self.clearCell(row, self._width-1)
		
		
	def shiftRight(self):
		'''
		Shifts picture to right bound of table to one pixel
		'''
		colRange = range(1,self._width)
		colRange.reverse()
		for col in colRange:
			for row in xrange(self._height):
				if self.item(row, col-1):
					self.setPixmap(row, col, self._bit1)
				else:
					self.clearCell(row, col)
		for row in xrange(self._height):
			self.clearCell(row,0)
		
		
	def rotateV(self):
		'''
		Mirros picture from top to bottom
		'''
		for row in xrange(self._height/2):
			self.swapRows(row, self._height-row-1)
			self.updateContents()
		
		
	def rotateH(self):
		'''
		Mirros picture from left to right
		'''
		for col in xrange(self._pictureWidth/2):
			self.swapColumns(col, self._pictureWidth-col-1)
		
		
	def setPictureWidth(self, value):
		'''
		Sets picture width
		value - new width of picture
		'''
		self._pictureWidth = value
		for col in xrange(0, value):
			self.showColumn(col)
		for col in xrange(value, self._width):
			for row in xrange(self._height):
				self.clearCell(row, col)
				self.hideColumn(col)
		
		
	def setPicture(self, picture):
		'''
		Draws picture in an table
		picture - tupple with two parameters
		0 - bytesring with picture data
		1 - integer width of the picture
		'''
		pictureData = picture[0]
		self.setPictureWidth(picture[1])
		charArray = array.array('B', pictureData)
		for row in xrange(self._height):
			for col in xrange(self._width):
				byte = (row*self._width+col)/8
				bit = (row*self._width+col)%8
				if (charArray[byte] >> bit) & 1 :
					self.setPixmap(row,col,self._bit1)
				else:
					self.clearCell(row, col)
		
		
	def getPicture(self):
		'''
		Returns picture drawed in the table
		returns tupple with two parameters
		0 - bytesring with picture data
		1 - integer width of the picture
		'''
		byteArray = array.array('B')
		for byte in xrange(self._width*self._height/8):
			byteArray.append(0)
			for bit in xrange(8):
				row = (byte*8+bit)/self._width
				col = (byte*8+bit)%self._width
				if self.item(row, col):
					byteArray[byte] += 2**bit
		
		pictureData = byteArray.tostring()	
#		print (pictureData, self._pictureWidth)
		return (pictureData, self._pictureWidth)
	
	
