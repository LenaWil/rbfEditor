# -*- coding: utf-8 -*-

import sys, os
import operator, re
import string
from qt import *
from globals import *

class Preferences:
	def __init__ (self):
		self._options = QSettings()
		self._options.insertSearchPath(QSettings.Unix, HOMEDIR + '.' + NAME)
		self._options.insertSearchPath(QSettings.Windows, '/' + NAME)
		
		if not self._isExist():
			self._init()
		
		self._options.beginGroup('settings')
		self._language = self._options.readEntry('general/language', 'English')[0].ascii()
		self._codepage = unicode(self._options.readEntry('general/rbf codepage', 'Windows-1251')[0])
		self._fontDir = unicode(self._options.readEntry('general/fonts directory', FONTDIR)[0])
		self._previewFile = unicode(self._options.readEntry('general/preview file', '')[0])
		self._rebtalk = unicode(self._options.readEntry('general/rebtalk', '')[0])
		self._author = unicode(self._options.readEntry('general/author', '')[0])
		self._numCols = self._options.readNumEntry('edit/columns number', 16)[0]
		self._dotSize = self._options.readNumEntry('/edit/dot size', 16)[0]
		self._fixedTable = self._options.readNumEntry('edit/fixed chartable', FALSE)[0]
		self._previewEnabled = self._options.readNumEntry('edit/auto preview', TRUE)[0]
		self._dataDir = unicode(self._options.readEntry('paths/data directory', '.')[0])
		self._docDir = unicode(self._options.readEntry('paths/docs directory', '.')[0])
		self._options.endGroup()
	
		self._loadFiles()	
	
	def __del__ (self):
		self._init()
		self._save()
		del self._options
	
	
	def _save (self):
		self._options.beginGroup('settings')
		self._options.writeEntry('general/language', self._language)
		self._options.writeEntry('general/rbf codepage', self._codepage)
		self._options.writeEntry('general/fonts directory', self._fontDir)
		self._options.writeEntry('general/preview file', self._previewFile)
		self._options.writeEntry('general/rebtalk', self._rebtalk)
		self._options.writeEntry('general/author', self._author)
		self._options.writeEntry('edit/columns number', self._numCols)
		self._options.writeEntry('edit/dot size', self._dotSize)
		self._options.writeEntry('edit/fixed chartable', self._fixedTable)
		self._options.writeEntry('edit/auto preview', self._previewEnabled)
		self._options.endGroup()
	
	
	def _init (self):
		ascii = u' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~ '
		cp1250 = u'€ ‚‐„…†‡ ‰Š‹ŚŤŽŹƀ‘’“”•–— ™š›śťžź ˇ˘Ł¤Ą¦§¨©Ş«¬­®Ż°±˛ł´µ¶·¸ąş»Ľ˝ľżŔÁÂĂÄĹĆÇČÉĘËĚÍÎĎĐŃŇÓÔŐÖ×ŘŮÚŰÜÝŢßŕáâăäĺćçčéęëěíîďđńňóôőö÷řůúűüýţ˙'
		cp1251 = u'ЂЃ‚ѓ„…†‡€‰Љ‹ЊЌЋЏђ‘’“”•–—‖™љ›њќћџ ЎўЈ¤Ґ¦§Ё©Є«¬­®Ї°±Ііґµ¶·ё№є»јЅѕїАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя'
		cp1252 = u'€‐‚ƒ„…†‡ˆ‰Š‹ŒƀŽƀƁ‘’“”•–—˜™š›œƀžŸ ¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ'
		
		self._options.beginGroup('encodings')
		self._options.writeEntry('tables/Windows-1250', ascii + cp1250)
		self._options.writeEntry('tables/Windows-1251', ascii + cp1251)
		self._options.writeEntry('tables/Windows-1252', ascii + cp1252)
		self._options.endGroup()

		self._options.beginGroup('settings')
		self._options.writeEntry('paths/data directory', self._getDirs()[0])
		self._options.writeEntry('paths/docs directory', self._getDirs()[1])
		self._options.endGroup()
		
		self._options.beginGroup('translations')
		self._options.writeEntry('languages/English', 'en')
		self._options.writeEntry('languages/Russian', 'ru')
		self._options.endGroup()
		
	
	def _getDirs (self):
		binPath = sys.argv[0]
		if operator.truth(re.match('^/usr/bin',binPath,re.I)):
			dataDir = '/usr/share/' + NAME + '/'
			docDir = '/usr/share/doc/' + NAME + '-' + VERSION + '/'
		elif operator.truth(re.match('^/usr/local/bin',binPath,re.I)):
			dataDir = '/usr/local/share/' + NAME + '/'
			docDir = '/usr/local/share/doc/' + NAME + '-' + VERSION + '/'
		else :
			dataDir = './'
			docDir = './'
		return (dataDir, docDir)	
		
	
	def _isExist (self):
		self._options.beginGroup('settings')
		test = self._options.readEntry('general/language', '')[0].ascii()
		self._options.endGroup()
		if test != '':
			existed = TRUE
		else:
			existed = FALSE
		return existed
	
	
	def get (self, key):
		if key == 'language' :
			value = self._language
		elif key == 'codepage' :
			value = self._codepage
		elif key == 'fontdir' :
			value = self._fontDir
		elif key == 'previewfile' :
			value = self._previewFile
		elif key == 'rebtalk' :
			value = self._rebtalk
		elif key == 'numcols' :
			value = self._numCols
		elif key == 'dotsize' :
			value = self._dotSize
		elif key == 'fixedtable' :
			value = self._fixedTable
		elif key == 'previewenabled' :
			value = self._previewEnabled
		elif key == 'encodings' :
			value = self._getList('encodings')
		elif key == 'translations' :
			value = self._getList('translations')
		elif key == 'previewtext' :
			value = self._previewText
		elif key == 'license' :
			value = self._license
		elif key == 'codetable' :
			value = self._getCodeTable()
		elif key == 'translator' :
			value = self._getFileName('translation', '.qm', 'data', TRUE)
		elif key == 'help' :
			value = self._getFileName('help', '.html', 'data', TRUE)
		elif key == 'sysicons' :
			value = self._getFileName('sirocket', '.rbobj', 'data', FALSE)
		elif key == 'author' :
			value = self._author
		else:
			value = None
			print 'Prefs get error: ' + key + ' not found'
			
		return value
		
		
	def set (self, key, value):
		if key == 'language' :
			self._language = value
		elif key == 'codepage' :
			self._codepage = value
		elif key == 'fontdir' :
			self._fontDir = value
		elif key == 'previewfile' :
			self._previewFile = value
			self._loadFiles()
		elif key == 'rebtalk' :
			self._rebtalk = value
		elif key == 'numcols' :
			self._numCols = value
		elif key == 'dotsize' :
			self._dotSize = value
		elif key == 'fixedtable' :
			self._fixedTable = value
		elif key == 'previewenabled' :
			self._previewEnabled = value
		elif key == 'author' :
			self._author = value
		else:
			print 'Prefs set error: ' + key + ' not found'
		
		
		
	def _getList (self, key):
		list = []
		if key == 'translations' :
			list = self._options.entryList('translations/languages')
	
		if key == 'encodings' :
			list = self._options.entryList('encodings/tables')
		
		return list
	
	def _getText (self, key):
		if key == 'previewtext' :
			if self._previewFile == '' :
				text = self._getFile('sample', '.txt', 'data', TRUE)
			else :
				text = self._getFile(self._previewFile)
		elif key == 'license' :
			text = self._getFile('COPYING', '', 'doc')
		else :
			text = ''
		return text
		
		
	def _getFile (self, name, suffix=None, dir=None, lang=None):
		contents = ''
		fileName = self._getFileName(name, suffix, dir, lang)
		try:
			file = open(fileName, 'r')
			contents = file.read()
			file.close()
		except:
			pass
		
		return contents
		
	def _getCodeTable (self):
		self._options.beginGroup('encodings')
		codeTable = unicode(self._options.readEntry('tables/' + self._codepage, '')[0])
		self._options.endGroup()
		return codeTable
		
		
	def _getFileName(self, name, suffix=None, dir=None, lang=None):
		if dir != None:
			if dir == 'data':
				dirPath = self._dataDir
			elif dir == 'doc':
				dirPath = self._docDir
			else:
				dirPath = ''
		else:
			dirPath = ''
		
		if lang != None:
			if lang == TRUE:
				langSuffix = '-' + self._options.readEntry('/translations/languages/' + unicode(self._language), 'en')[0].ascii()
			else:
				langSuffix = ''
		else:
			langSuffix = ''
		
		fileName = dirPath + name + langSuffix + suffix
		return fileName
		
		
	def saveToDisk (self):
		self._save()
		del self._options
		
		
	def _loadFiles (self):
		self._previewText = self._getText('previewtext')
		self._license = self._getText('license')
	
	
	
