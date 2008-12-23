# -*- coding: utf-8 -*-

import string


#from globals import *
from icons import *
from prefs import *
from ttfselect import *
from fontwin import *
from settings import *
from about import *
from upload import *
from help import *
from sysicons import *


class MainWindow(QMainWindow):
	'''
		Main program window. Provides user interface.
	'''
	def __init__(self, prefs = None, parent = None):
		QMainWindow.__init__(self,parent)
		self._parent = parent
		self.setName("winMain")
		self.initForm()
		self.initActions()
		
		self._prefs = prefs
		
		self._fileDialog = QFileDialog()
		self._fontDialog = FontDialog(self, self._prefs)
		self._messageBox = QMessageBox()
		self.languageChange()
		
		
	def initForm(self):
		self.statusBar()
		
		self.setMinimumSize(QSize(121,216))
		self.setIcon(getIcon('App'))
		self.setUsesBigPixmaps(1)
		self.setUsesTextLabel(0)
		
		self.setCentralWidget(QWidget(self,"qt_central_widget"))
		formMainLayout = QGridLayout(self.centralWidget(),1,1,1,6,"formMainLayout")
		
		self._tabs = QTabWidget(self.centralWidget(),"tabs")
		self._tabs.setTabPosition(QTabWidget.Top)
		self._tabs.setTabShape(QTabWidget.Rounded)
		self._tabCloseButton = QToolButton(self._tabs)
		self._tabCloseButton.setIconSet(QIconSet(getIcon('TabClose')))
		self._tabCloseButton.hide()
		self._tabs.setCornerWidget(self._tabCloseButton, Qt.TopRight)
		
		formMainLayout.addWidget(self._tabs,0,0)
		
		self._fileNewAction = QAction(self,"fileNewAction")
		self._fileNewAction.setIconSet(QIconSet(getIcon('New')))
		self._fileOpenAction = QAction(self,"fileOpenAction")
		self._fileOpenAction.setIconSet(QIconSet(getIcon('Open')))
		self._fileSaveAction = QAction(self,"fileSaveAction")
		self._fileSaveAction.setIconSet(QIconSet(getIcon('Save')))
		self._fileSaveAsAction = QAction(self,"fileSaveAsAction")
		self._fileExitAction = QAction(self,"fileExitAction")
		self._fileExitAction.setIconSet(QIconSet(getIcon('Exit')))
		self._helpContentsAction = QAction(self,"helpContentsAction")
		self._helpContentsAction.setIconSet(QIconSet(getIcon('Help')))
		self._helpAboutAction = QAction(self,"helpAboutAction")
		self._fileImportAction = QAction(self,"fileImportAction")
		self._fileImportAction.setIconSet(QIconSet(getIcon('Import')))
		self._serviceSettingsAction = QAction(self,"serviceSettingsAction")
		self._serviceSettingsAction.setIconSet(QIconSet(getIcon('Settings')))
		self._serviceUploadAction = QAction(self,"serviceUploadAction")
		self._serviceUploadAction.setIconSet(QIconSet(getIcon('Upload')))
		self._serviceSysIconsAction = QAction(self,"serviceSysIconsAction")
		self._serviceSysIconsAction.setIconSet(QIconSet(getIcon('SysIcons')))
		self._fileCloseAction = QAction(self,"fileCloseAction")
		self._fontPropertyAction = QAction(self,"fontPropertyAction")
		self._fontPropertyAction.setIconSet(QIconSet(getIcon('Property')))
		self._fontPreviewAction = QAction(self,"fontPreviewAction")
		self._fontPreviewAction.setIconSet(QIconSet(getIcon('Preview')))
		self._fontItalicAction = QAction(self,"fontItalicAction")
		self._fontBoldAction = QAction(self,"fontBoldAction")
		
		self._toolBar = QToolBar(QString(""),self,Qt.DockTop)
		
		self._toolBar.setFrameShape(QToolBar.NoFrame)
		self._toolBar.setFrameShadow(QToolBar.Plain)
		self._fileNewAction.addTo(self._toolBar)
		self._fileOpenAction.addTo(self._toolBar)
		self._fileImportAction.addTo(self._toolBar)
		self._fontPreviewAction.addTo(self._toolBar)
		self._fileSaveAction.addTo(self._toolBar)
		self._serviceUploadAction.addTo(self._toolBar)
		self._helpContentsAction.addTo(self._toolBar)
		
		self._menuBar = QMenuBar(self,"MenuBar")
		
		self._menuBar.setFrameShape(QMenuBar.MenuBarPanel)
		self._menuBar.setFrameShadow(QMenuBar.Raised)

		fileMenu = QPopupMenu(self)
		self._fileNewAction.addTo(fileMenu)
		self._fileOpenAction.addTo(fileMenu)
		self._fileImportAction.addTo(fileMenu)
		self._fileSaveAction.addTo(fileMenu)
		self._fileSaveAsAction.addTo(fileMenu)
		self._fileCloseAction.addTo(fileMenu)
		fileMenu.insertSeparator()
		fileMenu.insertSeparator()
		self._fileExitAction.addTo(fileMenu)
		self._menuBar.insertItem(QString(""),fileMenu,3)
		
		fontMenu = QPopupMenu(self)
		self._fontPropertyAction.addTo(fontMenu)
		self._fontPreviewAction.addTo(fontMenu)
		self._fontBoldAction.addTo(fontMenu)
		self._fontItalicAction.addTo(fontMenu)
		self._menuBar.insertItem(QString(""),fontMenu,2)
		
		serviceMenu = QPopupMenu(self)
		self._serviceUploadAction.addTo(serviceMenu)
		self._serviceSysIconsAction.addTo(serviceMenu)
		self._serviceSettingsAction.addTo(serviceMenu)
		self._menuBar.insertItem(QString(""),serviceMenu,5)
		
		helpMenu = QPopupMenu(self)
		self._helpContentsAction.addTo(helpMenu)
		helpMenu.insertSeparator()
		self._helpAboutAction.addTo(helpMenu)
		self._menuBar.insertItem(QString(""),helpMenu,6)
		
		self.resize(QSize(640,480).expandedTo(self.minimumSizeHint()))
		self.clearWState(Qt.WState_Polished)
		
		self._fileCloseAction.setEnabled(FALSE)
		self._fileSaveAction.setEnabled(FALSE)
		self._fileSaveAsAction.setEnabled(FALSE)
		self._fontPropertyAction.setEnabled(FALSE)
		self._fontPreviewAction.setEnabled(FALSE)
		self._fontBoldAction.setEnabled(FALSE)
		self._fontItalicAction.setEnabled(FALSE)
		
		
		
	def initActions(self):	
		self.connect(self._fileNewAction,SIGNAL("activated()"),self.fileNew)
		self.connect(self._fileOpenAction,SIGNAL("activated()"),self.fileOpen)
		self.connect(self._fileSaveAction,SIGNAL("activated()"),self.fileSave)
		self.connect(self._fileSaveAsAction,SIGNAL("activated()"),self.fileSaveAs)
		self.connect(self._fileExitAction,SIGNAL("activated()"),self.fileExit)
		self.connect(self._helpContentsAction,SIGNAL("activated()"),self.helpContents)
		self.connect(self._helpAboutAction,SIGNAL("activated()"),self.helpAbout)
		self.connect(self._fileImportAction,SIGNAL("activated()"),self.fileImport)
		self.connect(self._fontPropertyAction,SIGNAL("activated()"),self.fontProperty)
		self.connect(self._fontItalicAction,SIGNAL("activated()"),self.fontItalic)
		self.connect(self._fontPreviewAction,SIGNAL("activated()"),self.fontPreview)
		self.connect(self._fontBoldAction,SIGNAL("activated()"),self.fontBold)
		self.connect(self._serviceUploadAction,SIGNAL("activated()"),self.serviceUpload)
		self.connect(self._serviceSysIconsAction,SIGNAL("activated()"),self.serviceSysIcons)
		self.connect(self._serviceSettingsAction,SIGNAL("activated()"),self.serviceSettings)
		self.connect(self._fileCloseAction,SIGNAL("activated()"),self.fileClose)
		self.connect(self._tabs,SIGNAL("currentChanged(QWidget*)"),self.tabChanged)
		self.connect(self._tabCloseButton,SIGNAL("clicked()"),self.fileClose)
		

	def languageChange(self):
		self.setCaption(self.__tr("REB font editor"))
		self._fileNewAction.setText(self.__tr("New"))
		self._fileNewAction.setMenuText(self.__tr("&New"))
		self._fileNewAction.setStatusTip(self.__tr("New rbf font"))
		self._fileNewAction.setAccel(self.__tr("Ctrl+N"))
		self._fileOpenAction.setText(self.__tr("Open"))
		self._fileOpenAction.setMenuText(self.__tr("&Open..."))
		self._fileOpenAction.setStatusTip(self.__tr("Open rbf font"))
		self._fileOpenAction.setAccel(self.__tr("Ctrl+O"))
		self._fileSaveAction.setText(self.__tr("Save"))
		self._fileSaveAction.setMenuText(self.__tr("&Save"))
		self._fileSaveAction.setStatusTip(self.__tr("Save rbf font"))
		self._fileSaveAction.setAccel(self.__tr("Ctrl+S"))
		self._fileSaveAsAction.setText(self.__tr("Save As"))
		self._fileSaveAsAction.setMenuText(self.__tr("Save &As..."))
		self._fileSaveAsAction.setStatusTip(self.__tr("Save rbf font As"))
		self._fileSaveAsAction.setAccel(QString.null)
		self._fileExitAction.setText(self.__tr("Exit"))
		self._fileExitAction.setMenuText(self.__tr("E&xit"))
		self._fileExitAction.setAccel(QString.null)
		self._fontPropertyAction.setText(self.__tr("Properties"))
		self._fontPropertyAction.setMenuText(self.__tr("&Properties"))
		self._fontPreviewAction.setText(self.__tr("Preview"))
		self._fontPreviewAction.setMenuText(self.__tr("Pre&view"))
		self._fontPreviewAction.setAccel(self.__tr("Ctrl+P"))
		self._fontItalicAction.setText(self.__tr("Italic"))
		self._fontItalicAction.setMenuText(self.__tr("&Italic"))
		self._fontBoldAction.setText(self.__tr("Bold"))
		self._fontBoldAction.setMenuText(self.__tr("&Bold"))
		self._helpContentsAction.setText(self.__tr("Contents"))
		self._helpContentsAction.setMenuText(self.__tr("&Contents..."))
		self._helpContentsAction.setStatusTip(self.__tr("Help"))
		self._helpContentsAction.setAccel(QString.null)
		self._helpAboutAction.setText(self.__tr("About"))
		self._helpAboutAction.setMenuText(self.__tr("&About"))
		self._helpAboutAction.setAccel(QString.null)
		self._fileImportAction.setText(self.__tr("Import ttf"))
		self._fileImportAction.setMenuText(self.__tr("&Import"))
		self._fileImportAction.setStatusTip(self.__tr("Import true type font"))
		self._fileImportAction.setAccel(self.__tr("Ctrl+I"))
		self._serviceSettingsAction.setText(self.__tr("Settings"))
		self._serviceSettingsAction.setMenuText(self.__tr("Se&ttings"))
		self._serviceSettingsAction.setStatusTip(self.__tr("Program settings"))
		self._serviceSettingsAction.setAccel(self.__tr("Ctrl+T"))
		self._serviceUploadAction.setText(self.__tr("Upload"))
		self._serviceUploadAction.setMenuText(self.__tr("&Upload"))
		self._serviceUploadAction.setStatusTip(self.__tr("Upload font to REB"))
		self._serviceUploadAction.setAccel(self.__tr("Ctrl+U"))
		self._serviceSysIconsAction.setText(self.__tr("Create Sysicons.rb"))
		self._serviceSysIconsAction.setMenuText(self.__tr("C&reate .rb file"))
		self._serviceSysIconsAction.setStatusTip(self.__tr("Create .rb file with sysicons.rb"))
		self._serviceSysIconsAction.setAccel(self.__tr("Ctrl+R"))
		self._fileCloseAction.setText(self.__tr("Close"))
		self._fileCloseAction.setMenuText(self.__tr("&Close"))
		self._fileCloseAction.setStatusTip(self.__tr("Close rbf font"))
		self._toolBar.setLabel(self.__tr("Tools"))
		if self._menuBar.findItem(3):
			self._menuBar.findItem(3).setText(self.__tr("&File"))
		if self._menuBar.findItem(2):
			self._menuBar.findItem(2).setText(self.__tr("Fon&t"))
		if self._menuBar.findItem(5):
			self._menuBar.findItem(5).setText(self.__tr("&Service"))
		if self._menuBar.findItem(6):
			self._menuBar.findItem(6).setText(self.__tr("&Help"))
		
		
	def __tr(self,s,c = None):
		return qApp.translate("MainWindow",s,c)
	
	
	def tabAdd(self, tab):
		if tab.isOk():
			if self._tabs.count() == 0:
				self._fileCloseAction.setEnabled(TRUE)
				self._fileSaveAsAction.setEnabled(TRUE)
				self._fontPropertyAction.setEnabled(TRUE)
				self._fontPreviewAction.setEnabled(TRUE)
				self._fontBoldAction.setEnabled(TRUE)
				self._fontItalicAction.setEnabled(TRUE)
				self._tabCloseButton.show()
			self._tabs.addTab(tab, tab.getName())
			self._tabs.setCurrentPage(self._tabs.count()-1)
			self.connect(tab,PYSIGNAL('FontChanged'),self.fontChanged)
		else:
			tab.close()
		
		
	def tabClose(self, tab):
		if tab.isChanged() :
			if tab.getFileName() == '':
				caption = self.__tr("File not saved")
				text = self.__tr("New file hasn't been saved\nDo you really want to close it?")
			else:
				caption = self.__tr("Font changed")
				text = self.__tr("File has been changed from last save\nDo you really want to close it?" )
				
			replay = self._messageBox.information(self, caption, text, self.__tr('Save'),\
			self.__tr('Close'), self.__tr('Cancel'), 0, 2)
			
			if replay == 0 :
				if self.fileSave() == TRUE :
					closed = TRUE
				else:
					closed = FALSE
			elif replay == 1 :
				closed = TRUE
			elif replay == 2 :
				closed = FALSE
		else :
			closed = TRUE
		
		if closed :
			self.disconnect(tab,PYSIGNAL('FontChanged'),self.fontChanged)
			self._tabs.removePage(tab)
			tab.close(TRUE)
		
		if self._tabs.count() == 0:
			self._tabCloseButton.hide()
			self._fileCloseAction.setEnabled(FALSE)
			self._fileSaveAction.setEnabled(FALSE)
			self._fileSaveAsAction.setEnabled(FALSE)
			self._fontPropertyAction.setEnabled(FALSE)
			self._fontPreviewAction.setEnabled(FALSE)
			self._fontBoldAction.setEnabled(FALSE)
			self._fontItalicAction.setEnabled(FALSE)
		
		return closed
		
		
	def fileNew(self):
		tab = FontWindow(self, self._prefs, RBF_NEW)
		self.tabAdd(tab)
		
		
	def fileOpen(self):
		fileName = unicode(self._fileDialog.getOpenFileName('','reb font files (*.rbf)'))
		if fileName != '' :
			tab = FontWindow(self, self._prefs, RBF_OPEN, fileName)
			self.tabAdd(tab)
		
		
	def fileImport(self):
		if self._fontDialog.exec_loop() == QDialog.Accepted:
			fontFile = self._fontDialog.getFont()[0]
			fontSize = self._fontDialog.getFont()[1]
			tab = FontWindow(self, self._prefs, RBF_TTF, fontFile, fontSize)
			self.tabAdd(tab)
			
		
	def fileSave(self):
		tab = self._tabs.currentPage()
		if tab.getFileName() != '' :
			tab.save()
			writed = TRUE
		else :
			writed = self.fileSaveAs()
		return writed	
		
		
	def fileSaveAs(self):
		fileName = unicode(self._fileDialog.getSaveFileName('', 'reb font files (*.rbf)'))
		if fileName != '' :
			nameExt = os.path.splitext(fileName)
			if nameExt[1] != '.rbf' :
				fileName = fileName + '.rbf'
			if os.access(fileName,os.F_OK) == 1:
				if self._messageBox.question(self, self.__tr("File exist"),\
							self.__tr('File already exist\nDo you want to rewrite it?'),\
							QMessageBox.Yes,  QMessageBox.No) == QMessageBox.Yes:
					writed = TRUE
				else:
					writed = FALSE
			else:
				writed = TRUE
		else:
			writed = FALSE
		
		if writed :
			self._tabs.currentPage().save(fileName)
		return writed
		
		
	def fileClose(self):
		if self._tabs.count() != 0 :
			closed = self.tabClose(self._tabs.currentPage())
		else:
			closed = FALSE
		
		return closed
		
		
	def fileExit(self):
		self.close(TRUE)
		
	def close(self, delete):
		tabRange = range(self._tabs.count())
		tabRange.reverse()
		for index in tabRange:
			self._tabs.setCurrentPage(index)
			closed = self.fileClose()
			if not closed:
				break
		if self._tabs.count() == 0 :
			closed = QMainWindow.close(self, delete)
		else :
			closed = FALSE
		
		return closed
		
		
	def fontProperty(self):
		self._tabs.currentPage().changeFontProperty()
		
		
	def fontPreview(self):
		self._tabs.currentPage().showText()
	
	def fontBold (self):
		self._tabs.currentPage().makeBold()
		
		
	def fontItalic (self):
		self._tabs.currentPage().makeItalic()
		
		
	def helpContents(self):
#		self._tabs.currentPage().transform()
#		self._messageBox.information(self, self.__tr("Not implemented"),\
#			self.__tr('Sorry, help system not implemented yet'),\
#			QMessageBox.Ok)

		showHelp(self._prefs)
#		x = HelpWindow(self)
#		x.show()
		
		return FALSE
	
	def helpAbout(self):
		about = AboutDialog(self, self._prefs)
		about.exec_loop()
		about.close()
		del about
	
	def serviceSettings(self):
		settings = SettingsClass(self, self._prefs)
		self.connect(settings,PYSIGNAL('LanguageChanged'),self.langChanged)
		self.connect(settings,PYSIGNAL('FontDirChanged'),self.fontDirChanged)
		settings.exec_loop()
		self.disconnect(settings,PYSIGNAL('LanguageChanged'),self.langChanged)
		self.disconnect(settings,PYSIGNAL('FontDirChanged'),self.fontDirChanged)
		settings.close()
		del settings
			
			
	def serviceUpload(self):
#		if os.name == 'posix':
#			self._messageBox.information(self, self.__tr("Not implemented"),\
#			self.__tr('Sorry, uploading realized under MS Windows platform only'),\
#			QMessageBox.Ok)
#			return FALSE
		upload = UploadDialog(self, self._prefs)
		upload.exec_loop()
		
	def serviceSysIcons(self):
		sysicons = SysIconsDialog(self, self._prefs)
		sysicons.exec_loop()
		
		
	def tabChanged (self, tab):
		if tab.isChanged():
			self._fileSaveAction.setEnabled(TRUE)
		else:
			self._fileSaveAction.setEnabled(FALSE)
		
		if tab.previewEnabled():
			self._fontPreviewAction.setEnabled(FALSE)
		else:	
			self._fontPreviewAction.setEnabled(TRUE)
		
		
	def fontChanged(self, isTrue):
		self._fileSaveAction.setEnabled(isTrue)
		self._tabs.changeTab(self._tabs.currentPage(), self._tabs.currentPage().getName())
	
	
	def langChanged(self, var):
		self.emit(PYSIGNAL('LanguageChanged'),(TRUE,))
	
	def fontDirChanged(self, var):
		self._fontDialog.close()
		del self._fontDialog
		self._fontDialog = FontDialog(self, self._prefs)
	
