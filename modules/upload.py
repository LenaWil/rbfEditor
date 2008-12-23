# -*- coding: utf-8 -*-

from qt import *
from globals import *
import tempfile
import stat
import os, os.path
import shutil
import time

class UploadDialog(QDialog):
	def __init__(self,parent = None, prefs=None):
		QDialog.__init__(self,parent)
		self.setName("UploadDialog")
		
		self._initForm()
		self._initActions()
		self.languageChange()
		self._buttonOk.setEnabled(FALSE)
		self._rebtalk = prefs.get('rebtalk')
		self._fileDialog = QFileDialog(self)
		self._progress = QProgressDialog(self.__tr('Upload fonts'), None, 5, self, 'WaitWindow', TRUE, Qt.WStyle_NoBorder)
		self._progress.setMinimumDuration(0)
		self._progress.setModal(TRUE)
		
		
	def _initForm(self):
		self.setSizeGripEnabled(FALSE)
	
		self._labelLarge = QLabel(self,"_labelLarge")
		self._labelLarge.setGeometry(QRect(10,10,110,25))
	
		self._labelRegular = QLabel(self,"_labelRegular")
		self._labelRegular.setGeometry(QRect(10,50,110,25))
	
		self._labelBold = QLabel(self,"_labelBold")
		self._labelBold.setGeometry(QRect(10,90,110,25))
	
		self._labelItalic = QLabel(self,"_labelItalic")
		self._labelItalic.setGeometry(QRect(10,130,110,25))
	
		self._labelBolItalic = QLabel(self,"_labelBolItalic")
		self._labelBolItalic.setGeometry(QRect(10,170,110,25))
	
		self._checkLarge = QCheckBox(self,"_checkLarge")
		self._checkLarge.setGeometry(QRect(130,10,25,25))
	
		self._editRegular = QLineEdit(self,"_editRegular")
		self._editRegular.setGeometry(QRect(130,50,300,25))
	
		self._editBold = QLineEdit(self,"_editBold")
		self._editBold.setGeometry(QRect(130,90,300,25))
	
		self._editItalic = QLineEdit(self,"_editItalic")
		self._editItalic.setGeometry(QRect(130,130,300,25))
	
		self._editBoldItalic = QLineEdit(self,"_editBoldItalic")
		self._editBoldItalic.setGeometry(QRect(130,170,300,25))
	
		self._buttonRegular = QPushButton(self,"_buttonRegular")
		self._buttonRegular.setGeometry(QRect(440,50,25,25))
	
		self._buttonBold = QPushButton(self,"_buttonBold")
		self._buttonBold.setGeometry(QRect(440,90,25,25))
	
		self._buttonItalic = QPushButton(self,"_buttonItalic")
		self._buttonItalic.setGeometry(QRect(440,130,25,25))
	
		self._buttonBoldItalic = QPushButton(self,"_buttonBoldItalic")
		self._buttonBoldItalic.setGeometry(QRect(440,170,25,25))
	
		self._buttonOk = QPushButton(self,"_buttonOk")
		self._buttonOk.setGeometry(QRect(270,210,80,30))
		self._buttonOk.setAutoDefault(1)
		self._buttonOk.setDefault(1)
	
		self._buttonCancel = QPushButton(self,"_buttonCancel")
		self._buttonCancel.setGeometry(QRect(370,210,80,30))
		self._buttonCancel.setAutoDefault(1)
		
		self._buttonRegular.setText("...")
		self._buttonBold.setText("...")
		self._buttonItalic.setText("...")
		self._buttonBoldItalic.setText("...")
		self._checkLarge.setText(QString.null)
		self._buttonOk.setAccel(QString.null)
		self._buttonCancel.setAccel(QString.null)
	
		self.setMinimumSize(475,250)
		self.setMaximumSize(475,250)
	
	
	def _initActions(self):
		self.connect(self._buttonOk,SIGNAL("clicked()"),self.accept)
		self.connect(self._buttonCancel,SIGNAL("clicked()"),self.reject)
		self.connect(self._buttonRegular,SIGNAL("clicked()"),self._selectRegular)
		self.connect(self._buttonBold,SIGNAL("clicked()"),self._selectBold)
		self.connect(self._buttonItalic,SIGNAL("clicked()"),self._selectItalic)
		self.connect(self._buttonBoldItalic,SIGNAL("clicked()"),self._selectBoldItalic)
		self.connect(self._editRegular,SIGNAL("textChanged(const QString &)"),self._editChanged)
		self.connect(self._editBold,SIGNAL("textChanged(const QString &)"),self._editChanged)
		self.connect(self._editItalic,SIGNAL("textChanged(const QString &)"),self._editChanged)
		self.connect(self._editBoldItalic,SIGNAL("textChanged(const QString &)"),self._editChanged)
	

	def languageChange(self):
		self.setCaption(self.__tr("Upload fonts to ebook"))
		self._labelLarge.setText(self.__tr("Large font"))
		self._labelRegular.setText(self.__tr("Regular"))
		self._labelBold.setText(self.__tr("Bold"))
		self._labelItalic.setText(self.__tr("Italic"))
		self._labelBolItalic.setText(self.__tr("BoldItalic"))
		self._buttonOk.setText(self.__tr("Upload"))
		self._buttonCancel.setText(self.__tr("Cancel"))
	
	
	def __tr(self,s,c = None):
		return qApp.translate("UploadDialog",s,c)
	
	
	def _initCommands(self, large):
		if large :
			self._rebErase = 'CMD!\nDONTREPAG\nSETLARGE SYSTEM_LARGE SYSTEM_LARGE_ITALIC SYSTEM_LARGE_BOLD SYSTEM_LARGE_BOLD_ITALIC\nFERASE LARGE.RBF\nFERASE LARGEI.RBF\nFERASE LARGEB.RBF\nFERASE LARGEBI.RBF\nREPAG\nFERASE REBCMD'
			self._rebSet = 'CMD!\nDONTREPAG\nSETLARGE LARGE.RBF LARGEI.RBF LARGEB.RBF LARGEBI.RBF\nREPAG\nFERASE REBCMD'
			self._cmdPutFonts = 'rebtalk.exe put LARGE.RBF fontR.rbf\nrebtalk.exe put LARGEB.RBF fontB.rbf\nrebtalk.exe put LARGEI.RBF fontI.rbf\nrebtalk.exe put LARGEBI.RBF fontBI.rbf\n'
		else:
			self._rebErase = 'CMD!\nDONTREPAG\nSETSMALL SYSTEM_SMALL SYSTEM_SMALL_ITALIC SYSTEM_SMALL_BOLD SYSTEM_SMALL_BOLD_ITALIC\nFERASE SMALL.RBF\nFERASE SMALLI.RBF\nFERASE SMALLB.RBF\nFERASE SMALLBI.RBF\nREPAG\nFERASE REBCMD'
			self._rebSet = 'CMD!\nDONTREPAG\nSETSMALL SMALL.RBF SMALLI.RBF SMALLB.RBF SMALLBI.RBF\nREPAG\nFERASE REBCMD'
			self._cmdPutFonts = 'rebtalk.exe put SMALL.RBF fontR.rbf\nrebtalk.exe put SMALLB.RBF fontB.rbf\nrebtalk.exe put SMALLI.RBF fontI.rbf\nrebtalk.exe put SMALLBI.RBF fontBI.rbf\n'
	
	
	def _selectRegular(self):
		file = self._selectFile()
		if file != '' :
			self._editRegular.setText(file)
		
		
	def _selectBold(self):
		file = self._selectFile()
		if file != '' :
			self._editBold.setText(file)
		
		
	def _selectItalic(self):
		file = self._selectFile()
		if file != '' :
			self._editItalic.setText(file)
		
		
	def _selectBoldItalic(self):
		file = self._selectFile()
		if file != '' :
			self._editBoldItalic.setText(file)
		
	
	def _selectFile(self):
		file = unicode(self._fileDialog.getOpenFileName('', 'reb font files (*.rbf)'))
		return file
	
	
	def _editChanged(self, newText):
		if (self._editRegular.text() != '') &\
		(self._editBold.text() != '') &\
		(self._editItalic.text() != '') &\
		(self._editBoldItalic.text() != '') :
			self._buttonOk.setEnabled(TRUE)
		else:
			self._buttonOk.setEnabled(FALSE)
	
	
	def _step(self, value):
		self._progress.setProgress(value)
		self._progress.update()
		self._progress.repaint()
		qApp.processEvents()
	
	
	def _upload(self):
		self._progress.forceShow()
		self._step(0)
		
		fontR = unicode(self._editRegular.text())
		fontB = unicode(self._editBold.text())
		fontI = unicode(self._editItalic.text())
		fontBI = unicode(self._editBoldItalic.text())
		large = self._checkLarge.isChecked()
		
		self._initCommands(large)
		curDir = os.getcwdu()
		tempDir = tempfile.gettempdir()
		os.chdir(tempDir)
		cmdName = tempDir + '/oscmd.bat'
		rebName = tempDir + '/rebcmd'
	
		try:
			shutil.copy(self._rebtalk, tempDir + '/rebtalk.exe')
			shutil.copy(fontR, tempDir + '/fontR.rbf')
			shutil.copy(fontB, tempDir + '/fontB.rbf')
			shutil.copy(fontI, tempDir + '/fontI.rbf')
			shutil.copy(fontBI, tempDir + '/fontBI.rbf')
		except:
			pass
		
		cmdFile = open(cmdName, 'w+')
		rebFile = open(rebName, 'w+')
		rebFile.write(self._rebErase)
		cmdFile.write('rebtalk.exe REBCMD rebcmd\n')
		cmdFile.close()
		rebFile.close()
		os.chmod(cmdName, stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)
		os.system(cmdName)
	
		self._step(1)
		for index in xrange(3):
			time.sleep(1)
			self._step(self._progress.progress()+1)
		
		cmdFile = open(cmdName, 'w+')
		rebFile = open(rebName, 'w+')
		rebFile.write(self._rebSet)
		cmdFile.write(self._cmdPutFonts)
		cmdFile.write('rebtalk.exe put REBCMD rebcmd\n')
		cmdFile.close()
		rebFile.close()
		os.chmod(cmdName, stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)
		os.system(cmdName)
		
		try:
			os.remove('rebtalk.exe')
			os.remove('fontR.rbf')
			os.remove('fontI.rbf')
			os.remove('fontB.rbf')
			os.remove('fontBI.rbf')
			os.remove('oscmd.bat')
			os.remove('rebcmd')
		except:
			pass
		os.chdir(curDir)

		self._step(5)
		del self._progress
	
	def accept(self):
		self._upload()
		QDialog.accept(self)
	
	


	
