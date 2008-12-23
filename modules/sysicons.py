# -*- coding: utf-8 -*-

import sys
import pickle
import time
from rebUtils import *
from globals import *
from qt import *

class SysIconsDialog(QDialog):
	def __init__(self,parent = None, prefs=None):
		QDialog.__init__(self,parent)
		self.setName("SysIconsDialog")
		
		self._prefs = prefs
		self._fileDialog = QFileDialog(self)
		self._message = QMessageBox()
		
		self._initForm()
		self._initActions()
		self.languageChange()
		
		self._editAuthor.setText(self._prefs.get("author"))
		self._buttonOk.setEnabled(FALSE)
		
		
	def _initForm (self):
		self._tabs = QTabWidget(self,"tabs")
		self._tabs.setGeometry(QRect(5,5,465,195))
		self._tabInfo = QWidget(self._tabs,"tabInfo")
		self._tabSmall = QWidget(self._tabs,"tabSmall")
		self._tabLarge = QWidget(self._tabs,"tabLarge")
		self._tabs.insertTab(self._tabInfo,QString.fromLatin1(""))
		self._tabs.insertTab(self._tabSmall,QString.fromLatin1(""))
		self._tabs.insertTab(self._tabLarge,QString.fromLatin1(""))
		
		self._labelModel = QLabel(self._tabInfo,"labelModel")
		self._labelModel.setGeometry(QRect(10,10,110,25))
		self._labelAuthor = QLabel(self._tabInfo,"labelTitle")
		self._labelAuthor.setGeometry(QRect(10,50,110,25))
		self._labelTitle = QLabel(self._tabInfo,"labelTitle")
		self._labelTitle.setGeometry(QRect(10,90,110,25))
		self._labelFixed = QLabel(self._tabInfo,"labelTitle")
		self._labelFixed.setGeometry(QRect(10,130,110,25))
		
		self._comboModel = QComboBox(0,self._tabInfo,"comboModel")
		self._comboModel.setGeometry(QRect(100,10,320,25))
		self._editAuthor = QLineEdit(self._tabInfo,"_editModel")
		self._editAuthor.setGeometry(QRect(100,50,320,25))
		self._editTitle = QLineEdit(self._tabInfo,"_editModel")
		self._editTitle.setGeometry(QRect(100,90,320,25))
		self._editFixed = QLineEdit(self._tabInfo,"_editModel")
		self._editFixed.setGeometry(QRect(100,130,320,25))
		
		self._buttonFixed = QPushButton(self._tabInfo,"_buttonFixed")
		self._buttonFixed.setGeometry(QRect(430,130,25,25))
		
		self._labelSmallR = QLabel(self._tabSmall,"labelSmallR")
		self._labelSmallR.setGeometry(QRect(10,10,110,25))
		self._labelSmallB = QLabel(self._tabSmall,"labelSmallB")
		self._labelSmallB.setGeometry(QRect(10,50,110,25))
		self._labelSmallI = QLabel(self._tabSmall,"labelSmallI")
		self._labelSmallI.setGeometry(QRect(10,90,110,25))
		self._labelSmallBI = QLabel(self._tabSmall,"labelSmallBI")
		self._labelSmallBI.setGeometry(QRect(10,130,110,25))
		
		self._editSmallR = QLineEdit(self._tabSmall,"editSmallR")
		self._editSmallR.setGeometry(QRect(100,10,320,25))
		self._editSmallB = QLineEdit(self._tabSmall,"editSmallR")
		self._editSmallB.setGeometry(QRect(100,50,320,25))
		self._editSmallI = QLineEdit(self._tabSmall,"editSmallR")
		self._editSmallI.setGeometry(QRect(100,90,320,25))
		self._editSmallBI = QLineEdit(self._tabSmall,"editSmallR")
		self._editSmallBI.setGeometry(QRect(100,130,320,25))
		
		self._buttonSmallR = QPushButton(self._tabSmall,"buttonSmallR")
		self._buttonSmallR.setGeometry(QRect(430,10,25,25))
		self._buttonSmallB = QPushButton(self._tabSmall,"buttonSmallB")
		self._buttonSmallB.setGeometry(QRect(430,50,25,25))
		self._buttonSmallI = QPushButton(self._tabSmall,"buttonSmallI")
		self._buttonSmallI.setGeometry(QRect(430,90,25,25))
		self._buttonSmallBI = QPushButton(self._tabSmall,"buttonSmallBI")
		self._buttonSmallBI.setGeometry(QRect(430,130,25,25))
		
		self._labelLargeR = QLabel(self._tabLarge,"labelLargeR")
		self._labelLargeR.setGeometry(QRect(10,10,110,25))
		self._labelLargeB = QLabel(self._tabLarge,"labelLargeB")
		self._labelLargeB.setGeometry(QRect(10,50,110,25))
		self._labelLargeI = QLabel(self._tabLarge,"labelLargeI")
		self._labelLargeI.setGeometry(QRect(10,90,110,25))
		self._labelLargeBI = QLabel(self._tabLarge,"labelLargeBI")
		self._labelLargeBI.setGeometry(QRect(10,130,110,25))
		
		self._editLargeR = QLineEdit(self._tabLarge,"editLargeR")
		self._editLargeR.setGeometry(QRect(100,10,320,25))
		self._editLargeB = QLineEdit(self._tabLarge,"editLargeR")
		self._editLargeB.setGeometry(QRect(100,50,320,25))
		self._editLargeI = QLineEdit(self._tabLarge,"editLargeR")
		self._editLargeI.setGeometry(QRect(100,90,320,25))
		self._editLargeBI = QLineEdit(self._tabLarge,"editLargeR")
		self._editLargeBI.setGeometry(QRect(100,130,320,25))
		
		self._buttonLargeR = QPushButton(self._tabLarge,"buttonLargeR")
		self._buttonLargeR.setGeometry(QRect(430,10,25,25))
		self._buttonLargeB = QPushButton(self._tabLarge,"buttonLargeB")
		self._buttonLargeB.setGeometry(QRect(430,50,25,25))
		self._buttonLargeI = QPushButton(self._tabLarge,"buttonLargeI")
		self._buttonLargeI.setGeometry(QRect(430,90,25,25))
		self._buttonLargeBI = QPushButton(self._tabLarge,"buttonLargeBI")
		self._buttonLargeBI.setGeometry(QRect(430,130,25,25))
		
		self._buttonOk = QPushButton(self,"buttonOk")
		self._buttonOk.setGeometry(QRect(270,210,80,30))
		self._buttonOk.setAutoDefault(1)
		self._buttonOk.setDefault(1)
			
		self._buttonCancel = QPushButton(self,"buttonCancel")
		self._buttonCancel.setGeometry(QRect(370,210,80,30))
		self._buttonCancel.setAutoDefault(1)
		
		self.setSizeGripEnabled(FALSE)
		self.setMinimumSize(475,250)
		self.setMaximumSize(475,250)
		
		
	def _initActions (self):
		self.connect(self._buttonCancel,SIGNAL("clicked()"),self.reject)
		self.connect(self._buttonOk,SIGNAL("clicked()"),self.accept)
		self.connect(self._buttonFixed,SIGNAL("clicked()"),self._selectFixed)
		self.connect(self._buttonSmallR,SIGNAL("clicked()"),self._selectSmallR)
		self.connect(self._buttonSmallB,SIGNAL("clicked()"),self._selectSmallB)
		self.connect(self._buttonSmallI,SIGNAL("clicked()"),self._selectSmallI)
		self.connect(self._buttonSmallBI,SIGNAL("clicked()"),self._selectSmallBI)
		self.connect(self._buttonLargeR,SIGNAL("clicked()"),self._selectLargeR)
		self.connect(self._buttonLargeB,SIGNAL("clicked()"),self._selectLargeB)
		self.connect(self._buttonLargeI,SIGNAL("clicked()"),self._selectLargeI)
		self.connect(self._buttonLargeBI,SIGNAL("clicked()"),self._selectLargeBI)
		self.connect(self._editSmallR,SIGNAL("textChanged(const QString &)"),self._editChanged)
		self.connect(self._editLargeR,SIGNAL("textChanged(const QString &)"),self._editChanged)
		
		
	def languageChange(self):
		self.setCaption(self.__tr("Create SysIcons"))
		self._buttonOk.setText(self.__tr("&OK"))
		self._buttonOk.setAccel(QString.null)
		self._buttonCancel.setText(self.__tr("&Cancel"))
		self._buttonCancel.setAccel(QString.null)
		self._tabs.changeTab(self._tabInfo,self.__tr("Information"))
		self._tabs.changeTab(self._tabSmall,self.__tr("Small font"))
		self._tabs.changeTab(self._tabLarge,self.__tr("Large font"))
		self._labelModel.setText(self.__tr("Device"))
		self._labelAuthor.setText(self.__tr("Author"))
		self._labelTitle.setText(self.__tr("Title"))
		self._labelFixed.setText(self.__tr("Fixed font"))
		self._comboModel.insertItem("Nuvomedia Rocket eBook")
		self._labelSmallR.setText(self.__tr("Regular"))
		self._labelSmallB.setText(self.__tr("Bold"))
		self._labelSmallI.setText(self.__tr("Italic"))
		self._labelSmallBI.setText(self.__tr("Bold italic"))
		self._labelLargeR.setText(self.__tr("Regular"))
		self._labelLargeB.setText(self.__tr("Bold"))
		self._labelLargeI.setText(self.__tr("Italic"))
		self._labelLargeBI.setText(self.__tr("Bold italic"))
		self._buttonFixed.setText("...")
		self._buttonSmallR.setText("...")
		self._buttonSmallB.setText("...")
		self._buttonSmallI.setText("...")
		self._buttonSmallBI.setText("...")
		self._buttonLargeR.setText("...")
		self._buttonLargeB.setText("...")
		self._buttonLargeI.setText("...")
		self._buttonLargeBI.setText("...")
		
		
	def __tr(self,s,c = None):
		return qApp.translate("SysIconsDialog",s,c)
		
		
	def _selectFixed (self):
		file = self._selectFile()
		if file != '' :
			self._editFixed.setText(file)
		
		
	def _selectSmallR (self):
		file = self._selectFile()
		if file != '' :
			self._editSmallR.setText(file)
		
		
	def _selectSmallB (self):
		file = self._selectFile()
		if file != '' :
			self._editSmallB.setText(file)
		
		
	def _selectSmallI (self):
		file = self._selectFile()
		if file != '' :
			self._editSmallI.setText(file)
		
		
	def _selectSmallBI (self):
		file = self._selectFile()
		if file != '' :
			self._editSmallBI.setText(file)
		
		
	def _selectLargeR (self):
		file = self._selectFile()
		if file != '' :
			self._editLargeR.setText(file)
		
		
	def _selectLargeB (self):
		file = self._selectFile()
		if file != '' :
			self._editLargeB.setText(file)
		
		
	def _selectLargeI (self):
		file = self._selectFile()
		if file != '' :
			self._editLargeI.setText(file)
		
		
	def _selectLargeBI (self):
		file = self._selectFile()
		if file != '' :
			self._editLargeBI.setText(file)
		
		
	def _selectFile (self):
		file = unicode(self._fileDialog.getOpenFileName('', 'reb font files (*.rbf)'))
		return file
		
		
	def _editChanged(self, newText):
		if (self._editSmallR.text() != '') &\
		(self._editLargeR.text() != '') :
			self._buttonOk.setEnabled(TRUE)
		else:
			self._buttonOk.setEnabled(FALSE)
		
		
	def _createSysIcons (self):
		smallR = unicode(self._editSmallR.text())
		smallB = unicode(self._editSmallB.text())
		smallI = unicode(self._editSmallI.text())
		smallBI = unicode(self._editSmallBI.text())
		largeR = unicode(self._editLargeR.text())
		largeB = unicode(self._editLargeB.text())
		largeI = unicode(self._editLargeI.text())
		largeBI = unicode(self._editLargeBI.text())
		fixed = unicode(self._editFixed.text())
		
		if fixed == '':
			fixed = smallR
		if smallB == '':
			smallB = smallR
		if smallI == '':
			smallI = smallR
		if smallBI == '':
			smallBI = smallR
		if largeB == '':
			largeB = largeR
		if largeI == '':
			largeI = largeR
		if largeBI == '':
			largeBI = largeR
			
		fonts = ((fixed, 'fixed.rbf'),\
			(smallR, 'small.rbf'),\
			(smallB, 'small_bold.rbf'),\
			(smallI, 'small_italic.rbf'),\
			(smallBI, 'small_bold_italic.rbf'),\
			(largeR, 'large.rbf'),\
			(largeB, 'large_bold.rbf'),\
			(largeI, 'large_italic.rbf'),\
			(largeBI, 'large_bold_italic.rbf'))
			
		file = open(self._prefs.get("sysicons"), 'rb')
		rbSysIcons = pickle.load(file)
		file.close()
			
		try:
			for font in fonts:
				file = open(font[0], 'rb')
				data = file.read()
				rbSysIcons.addSegment(font[1], data, RB_SEG_DEFLATED)
				file.close()
			dataOk = TRUE
		except:
			dataOk = FALSE
			
		if dataOk:
			sysIcons = rbSysIcons.getFile()
		else:	
			sysIcons = None
		return sysIcons
		
		
	def _createRB (self):
			self._prefs.set("author", unicode(self._editAuthor.text()))
			sysIcons = self._createSysIcons()
			if sysIcons != None:
				doWrite = TRUE
				outFile = unicode(self._fileDialog.getSaveFileName('', 'rb tiles (*.rb)'))
				if outFile != '' :
					nameExt = os.path.splitext(outFile)
					if nameExt[1] != '.rb' :
						outFile = outFile + '.rb'
					if os.access(outFile,os.F_OK):
						if self._message.question(self, self.__tr("File exist"),\
							self.__tr('File already exist\nDo you want to rewrite it?'),\
							QMessageBox.Yes,  QMessageBox.No) != QMessageBox.Yes:
								doWrite = FALSE
				else:
					doWrite = FALSE
			else:
				doWrite = FALSE
			
			if doWrite:
				isbn = time.strftime('%Y%m%d-%H%M')
				info = 'TITLE=' + self._editTitle.text().ascii() + '\r\n' +\
					'AUTHOR=' + self._editAuthor.text().ascii() + '\r\n' +\
					'GENERATOR=rbfEditor v0.2\r\n' +\
					'ISBN=' + isbn
				wait = 'wait\r\n\r\n'
				reset = "CMD!\r\nRESET\r\n#/* don't delete these lines as they are here */\r\n" +\
				"#/* to workaround a bug in the rocket book. djc. */"
				
				output = rbFile(RB_TYPE_EXEC)
				output.addSegment('firmware.info', info, RB_SEG_INFO)
				output.addSegment('wait', wait, RB_SEG_PLAIN)
				output.addSegment('sysicons.rb', sysIcons, RB_SEG_PLAIN)
				output.addSegment('reset.cmd', reset, RB_SEG_PLAIN)
				
				if outFile != '':
					try:
						file = open(outFile, 'wb+')
						file.write(output.getFile())
						file.close()
					except:
						self.message.critical(self, "Error", "Can't write file " + outFile)
		
		
	def accept (self):
		self._createRB()
		QDialog.accept(self)
		
		
	
