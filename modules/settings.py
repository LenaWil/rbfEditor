# -*- coding: utf-8 -*-

import os


from globals import *

from prefs import *

from qt import *

class SettingsClass(QDialog):
	def __init__(self, parent = None, prefs = None):
		QDialog.__init__(self,parent,"SettingsDialog")
		self._parent = parent
		self._prefs = prefs
		self._initForm()
		self._initActions()
		self.languageChange()
		self._dirDialog = QFileDialog(self)
		
		self._comboLanguage.clear()
		tempList = self._prefs.get('translations')
		for index in xrange(tempList.count()):
			self._comboLanguage.insertItem(tempList[index])
		self._comboCodepage.clear()
		tempList = self._prefs.get('encodings')
		for index in xrange(tempList.count()):
			self._comboCodepage.insertItem(tempList[index])
		self._comboLanguage.setCurrentText(self._prefs.get('language')) 
		self._comboCodepage.setCurrentText(self._prefs.get('codepage'))
		self._editFontDir.setText(self._prefs.get('fontdir')) 
		self._editPreviewFile.setText(self._prefs.get('previewfile')) 
		self._editRebtalk.setText(self._prefs.get('rebtalk'))		
		self._spinCols.setValue(self._prefs.get('numcols'))
		self._spinDotSize.setValue(self._prefs.get('dotsize'))
		self._checkFixedTable.setChecked(self._prefs.get('fixedtable'))
		self._checkPreview.setChecked(self._prefs.get('previewenabled'))
		
		
	def _initForm(self):

		self._tabs = QTabWidget(self,"_tabs")
		self._tabs.setGeometry(QRect(10,10,500,240))

		self._tabGeneral = QWidget(self._tabs,"_tabGeneral")

		self._labelLanguage = QLabel(self._tabGeneral,"_labelLanguage")
		self._labelLanguage.setGeometry(QRect(20,10,230,25))

		self._labelCodepage = QLabel(self._tabGeneral,"_labelCodepage")
		self._labelCodepage.setGeometry(QRect(20,50,230,25))

		self._labelFontDir = QLabel(self._tabGeneral,"_labelFontDir")
		self._labelFontDir.setGeometry(QRect(20,90,130,25))

		self.__labelPreviewFile = QLabel(self._tabGeneral,"__labelPreviewFile")
		self.__labelPreviewFile.setGeometry(QRect(20,130,130,25))
		
		self._labelRebtalk = QLabel(self._tabGeneral,"_labelRebtalk")
		self._labelRebtalk.setGeometry(QRect(20,170,145,25))

		self._comboLanguage = QComboBox(0,self._tabGeneral,"_comboLanguage")
		self._comboLanguage.setGeometry(QRect(270,10,170,25))

		self._comboCodepage = QComboBox(0,self._tabGeneral,"_comboCodepage")
		self._comboCodepage.setGeometry(QRect(270,50,170,25))

		self._editFontDir = QLineEdit(self._tabGeneral,"_editFontDir")
		self._editFontDir.setGeometry(QRect(170,90,270,25))
		self._editFontDir.setReadOnly(FALSE)

		self._buttonFontDir = QPushButton(self._tabGeneral,"_buttonFontDir")
		self._buttonFontDir.setGeometry(QRect(450,90,25,25))

		self._editPreviewFile = QLineEdit(self._tabGeneral,"_editPreviewFile")
		self._editPreviewFile.setGeometry(QRect(170,130,270,25))
		self._editPreviewFile.setReadOnly(FALSE)

		self._buttonTextPreview = QPushButton(self._tabGeneral,"_buttonTextPreview")
		self._buttonTextPreview.setGeometry(QRect(450,130,25,25))

		self._editRebtalk = QLineEdit(self._tabGeneral,'_editRebtalk')
		self._editRebtalk.setGeometry(QRect(170,170,270,25))
		self._editRebtalk.setReadOnly(FALSE)

		self._buttonRebtalk = QPushButton(self._tabGeneral,"_buttonRebtalk")
		self._buttonRebtalk.setGeometry(QRect(450,170,25,25))

		self._tabs.insertTab(self._tabGeneral,QString.fromLatin1(""))

		self._tabEdit = QWidget(self._tabs,"_tabEdit")

		self._labelCols = QLabel(self._tabEdit,"_labelCols")
		self._labelCols.setGeometry(QRect(20,10,290,25))

		self._labelDotSize = QLabel(self._tabEdit,"_labelDotSize")
		self._labelDotSize.setGeometry(QRect(20,50,290,25))

		self._labelFixedTable = QLabel(self._tabEdit,"_labelFixedTable")
		self._labelFixedTable.setGeometry(QRect(20,90,290,25))

		self._labelPreview = QLabel(self._tabEdit,"_labelPreview")
		self._labelPreview.setGeometry(QRect(20,130,290,25))

		self._spinCols = QSpinBox(self._tabEdit,"_spinCols")
		self._spinCols.setGeometry(QRect(329,10,40,25))
		self._spinCols.setMaxValue(32)
		self._spinCols.setMinValue(16)
		self._spinCols.setLineStep(16)

		self._spinDotSize = QSpinBox(self._tabEdit,"_spinDotSize")
		self._spinDotSize.setGeometry(QRect(330,50,40,25))
		self._spinDotSize.setMaxValue(64)
		self._spinDotSize.setMinValue(1)
		self._spinDotSize.setValue(16)

		self._checkFixedTable = QCheckBox(self._tabEdit,"_checkFixedTable")
		self._checkFixedTable.setGeometry(QRect(330,90,40,25))

		self._checkPreview = QCheckBox(self._tabEdit,"_checkPreview")
		self._checkPreview.setGeometry(QRect(330,130,40,25))

		self._tabs.insertTab(self._tabEdit,QString.fromLatin1(""))

		self._buttonOk = QPushButton(self,"_buttonOk")
		self._buttonOk.setGeometry(QRect(320,260,80,30))
		self._buttonOk.setAutoDefault(1)
		self._buttonOk.setDefault(1)

		self._buttonCancel = QPushButton(self,"_buttonCancel")
		self._buttonCancel.setGeometry(QRect(430,260,80,30))
		self._buttonCancel.setAutoDefault(1)

		self.setSizeGripEnabled(FALSE)
		self.setMinimumSize(520, 300)
		self.setMaximumSize(520, 300)


	def _initActions(self):
		self.connect(self._buttonCancel,SIGNAL("clicked()"),self.reject)
		self.connect(self._buttonOk,SIGNAL("clicked()"),self.accept)
		self.connect(self._buttonFontDir,SIGNAL("clicked()"),self._selectFontDir)
		self.connect(self._buttonTextPreview,SIGNAL("clicked()"),self._selectPreviewFile)
		self.connect(self._buttonRebtalk,SIGNAL("clicked()"),self._selectRebtalk)

	
	def languageChange(self):
		self.setCaption(self.__tr("Settings"))
		self._buttonCancel.setText(self.__tr("Cancel"))
		self._buttonCancel.setAccel(QString.null)
		self._buttonOk.setText(self.__tr("OK"))
		self._buttonOk.setAccel(QString.null)
		self._labelFontDir.setText(self.__tr("Fonts directory"))
		self.__labelPreviewFile.setText(self.__tr("File with preview text"))
		self._labelRebtalk.setText(self.__tr("Path to rebtalk"))
		self._buttonFontDir.setText("...")
		self._buttonTextPreview.setText("...")
		self._buttonRebtalk.setText("...")
		self._labelLanguage.setText(self.__tr("Language"))
		self._labelCodepage.setText(self.__tr("REB font encoding"))
		self._tabs.changeTab(self._tabGeneral,self.__tr("General"))
		self._checkPreview.setText(QString.null)
		self._checkFixedTable.setText(QString.null)
		self._labelCols.setText(self.__tr("Number of colums in characters table"))
		self._labelDotSize.setText(self.__tr("Dot size in character edit window (px)"))
		self._labelFixedTable.setText(self.__tr("Fixed character table"))
		self._labelPreview.setText(self.__tr("Auto preview of text file"))
		self._tabs.changeTab(self._tabEdit,self.__tr("Edit"))
#		self.fontString = self.__tr('The quick brown fox jumps over the lazy dog')
	
		QWhatsThis.add(self._comboLanguage,self.__tr('Program interface language'))
		QWhatsThis.add(self._comboCodepage,self.__tr('Codepage of REB fonts, obtaining from truetype fonts converting'))
		QWhatsThis.add(self._editFontDir,self.__tr('Directory with true type fonts, installed in system'))
		QWhatsThis.add(self._editPreviewFile,self.__tr('File, that been previewed in fontedit window'))
		QWhatsThis.add(self._editRebtalk,self.__tr('Path to rebtalk program'))
		QWhatsThis.add(self._checkFixedTable,self.__tr('Font table in fontedit window will be fixed size'))
		QWhatsThis.add(self._checkPreview,self.__tr('Automatic preview changes of font in preview window'))
		QWhatsThis.add(self._spinCols,self.__tr('Number of columns of font table in fontedit window'))
		QWhatsThis.add(self._spinDotSize, self.__tr('Size of dot in charedit window (in pixels)'))
		
	
	

	def __tr(self,s,c = None):
		return qApp.translate("SettingsClass",s,c)


	def _getDir (self):
		return unicode(self._dirDialog.getExistingDirectory())
	
	
	def _getFileName (self):
		return unicode(self._dirDialog.getOpenFileName())
	
	
	def _selectFontDir(self):
		newDir = self._getDir()
		if newDir != '' :
			self._editFontDir.setText(newDir)


	def _selectPreviewFile(self):
		file = self._getFileName()
		if file != '' :
			self._editPreviewFile.setText(file)
	
	
	def _selectRebtalk(self):
		file = self._getFileName()
		if file != '' :
			self._editRebtalk.setText(file)
		
		
	def accept(self):
		self._prefs.set('codepage', unicode(self._comboCodepage.currentText()))
		self._prefs.set('previewfile', unicode(self._editPreviewFile.text()))
		self._prefs.set('rebtalk', unicode(self._editRebtalk.text()))
		self._prefs.set('numcols', self._spinCols.value())
		self._prefs.set('dotsize', self._spinDotSize.value())
		self._prefs.set('fixedtable', self._checkFixedTable.isChecked())
		self._prefs.set('previewenabled', self._checkPreview.isChecked())
		if unicode(self._comboLanguage.currentText()) != self._prefs.get('language'):
			self._prefs.set('language', self._comboLanguage.currentText())
			self.emit(PYSIGNAL('LanguageChanged'),(TRUE,))
		if unicode(self._editFontDir.text()) != self._prefs.get('fontdir'):
			self._prefs.set('fontdir', unicode(self._editFontDir.text()))
			self.emit(PYSIGNAL('FontDirChanged'),(TRUE,))
				
		
		
		QDialog.accept(self)
	
	
	
	
	
	
