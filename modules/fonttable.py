# -*- coding: utf-8 -*-
'''
Module contains FontTable class
'''
from qt import *
from qttable import *
from globals import *
from charwin import *

class FontTable(QTable):
	def __init__(self, parent=None, prefs=None, font=None):
		'''
			Creates new FontTable object
		parent - parent object
		prefs - link to Preferences class object
		font - rbf font object
		'''
		self._parent = parent
		self._prefs = prefs
		self._font = font
		self._numCols = self._prefs.get('numcols')
		self._numRows = self._font.charCount / self._numCols
		restCols = self._font.charCount % self._numCols
		if restCols != 0:
			self._numRows += 1
		
		self._fontW = self._font.width
		self._fontH = self._font.height
		
		QTable.__init__(self, parent)
		self._charWindow = CharWindow(self, self._fontW, self._fontH, self._prefs.get('dotsize'))
		self._initActions()
		
		self.setSelectionMode(QTable.NoSelection)
		self.setReadOnly(TRUE)
		self.setFocusStyle(QTable.FollowStyle)
		self.setNumRows(self._numRows)
		self.setNumCols(self._numCols)
		self.verticalHeader().setResizeEnabled(FALSE)
		self.horizontalHeader().setResizeEnabled(FALSE)
		
		headersList = QStringList()
		for index in xrange(self._numCols):
			headersList.append(hex(index)[2:])
		self.setColumnLabels(headersList)
		
		headersList.clear()
		for index in xrange(self._numRows):
			headersList.append(hex(self._font.charFirst+index*self._numCols)[2:])
		self.setRowLabels(headersList)
		
		self.setVScrollBarMode(QScrollView.AlwaysOff)
		self.setHScrollBarMode(QScrollView.AlwaysOff)
		if self._prefs.get('fixedtable') :
			for index in xrange(self._numCols):
				self.setColumnWidth(index, self._fontW)
			for index in xrange(self._numRows):
				self.setRowHeight(index, self._fontH)
			minW = self.sizeHint().width()
			minH = self.sizeHint().height()
			self.setMinimumSize(minW, minH)
			self.setMaximumSize(minW, minH)
		else:
			for index in xrange(self._numCols):
				self.setColumnStretchable(index,1)
			for index in xrange(self._numRows):
				self.setRowStretchable(index,1)
			minW = self.sizeHint().width()
			minH = self.sizeHint().height()
			self.setMinimumSize(minW, minH)
		
		
	def _initActions (self):
		self.connect(self,SIGNAL("doubleClicked(int, int, int, const QPoint&)"),self._editChar)
		self.connect(self,PYSIGNAL('mousePressed'),self._startDrag)
		self.connect(self,PYSIGNAL('mouseReleased'),self._stopDrag)
		
		
	def contentsMousePressEvent(self, event):
		self.emit(PYSIGNAL('mousePressed'),(event,))
		
		
	def contentsMouseReleaseEvent(self, event):
			self.emit(PYSIGNAL('mouseReleased'),(event,))
		
		
	def _startDrag (self, event):
		self._startRow = self.rowAt(event.y())
		self._startCol = self.columnAt(event.x())
		self.setCurrentCell(self._startRow, self._startCol)
			
			
	def _stopDrag (self, event):
		stopRow = self.rowAt(event.y())
		stopCol = self.columnAt(event.x())
		if (stopRow != self._startRow) | (stopCol != self._startCol):
			startCode = self._getCharCode(self._startRow, self._startCol)
			stopCode = self._getCharCode(stopRow, stopCol)
			self._font.setChar(stopCode, self._font.getChar(startCode))
			self._drawChar(stopRow, stopCol)
			self._fontChanged()
		
		
	def show(self):
		self._drawTable()
		QTable.show(self)
		
		
	def _getCharCode (self, row, col):
		return row*self._numCols + col
		
		
	def getCharBitmap (self, charCode):
		row = charCode / self._numCols
		col = charCode % self._numCols
		return self.pixmap(row, col)
		
		
	def _drawChar(self, row, col):
		self.clearCell(row, col)
		charCode = self._getCharCode(row, col)
		charBitmap = QBitmap(self._fontW, self._fontH, self._font.getChar(charCode)[0],1)
		self.setPixmap(row, col, charBitmap)
		
		
	def _drawTable(self):
		for row in xrange(self._numRows)	:
			for col in xrange(self._numCols):
				self._drawChar(row, col)
		
		
	def _editChar(self, row, col, button, mousePos):
		charCode = self._getCharCode(row, col)
		char = self._font.getChar(charCode)
		self._charWindow.setChar(char)
		if self._charWindow.exec_loop() == QDialog.Accepted:
			newChar = self._charWindow.getChar()
			if (char[0] != newChar[0]) or (char[1] != newChar[1]):
				self._font.setChar(charCode, newChar)
				self._drawChar(row, col)
				self._fontChanged()
		
		
	def _fontChanged (self):
		self.emit(PYSIGNAL('FontChanged'),(1,1))

