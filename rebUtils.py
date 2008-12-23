#  rebUtils - python  module with API for RCA REB1100
#   (C) 2006 Andrew Mochalov
#
'''
	RCA REB 1100 Utilites module
Contain utilites for access and manipulation with RCA ebook REB 1100

'''

__version__ = '0.2'

import struct
import zlib
import datetime
import string

FALSE = 0
TRUE  = 1
_FNT_HDR_MAGIC 	= '\xE0\x0E\xF0\x0D\x03\x00\x00\x00'
_FNT_HDR_SIZE	= 0x74
_FNT_MAX_NAME 	= 64

RB_TYPE_TILE		= 0
RB_TYPE_EXEC		= 1
RB_TYPE_SYSICONS	= 2

RB_SEG_PLAIN		= 0
RB_SEG_ENCRYPTED	= 1
RB_SEG_INFO			= 2
RB_SEG_DEFLATED		= 8

_RB_TILE_MAGIC 		= '\xB0\x0C\xB0\x0C'
_RB_EXEC_MAGIC 		= '\xB0\x0C\xC0\xDE'
_RB_SYSICONS_MAGIC 	= '\xB0\x0C\xF0\x0D'
_RB_UNKNOWN_MAGIC 	= '\x00\x00\x00\x00'

_RB_VERSION			= '\x02\x00'

_RB_TOC_ITEM_LEN = 44
_BLK_SIZE		= 4096
	
class	rbFont:
	'''
	rbFont class used to access RBF font structure
	Class has next parameters:
	name		- name of font (max 64 characters)
	width		- font element width in pixels
	height		- font element height in pixels
	points		- font size in points
	charFirst	- ASCII code of first char, presents in font
	charCount	- count of chars containing in font
	cTable		- List of chars. Element of list is a bytecode string,
			 	  contains pixels representation  of char
	wTable		- List of character widths. Elements of list
		          is width of char 
	intline		- Interline spasing
	maxWidth	- width of widhest char in pixels
	descent		- font descent
	'''
	
	def __init__ (self):
		'''
			Creates new instance of class with empty initial values
		'''
		self.name		= ''
		self.width		= 0
		self.height		= 0
		self.points 	= 0
		self.intline 	= 0
		self.charFirst 	= 0
		self.charCount 	= 0
		self.wTable		= []
		self.cTable		= []
		self.maxWidth 	= 0
		self.descent	= 0
		self._charLast	= 0
		self._charSize 	= 0
		self._wmapAddr	= 0
		self._cmapAddr	= 0
		self._unknown4 	= 0


	def __load(self,file):
		'''
			Load rebFont instance from file.
			<file> - python file object
		'''
		file.seek(0)
		magic = file.read(len(_FNT_HDR_MAGIC))
		if magic == _FNT_HDR_MAGIC :
			fmt = str(_FNT_MAX_NAME)+'s'
			self.name		= struct.unpack(fmt,file.read(_FNT_MAX_NAME))[0]
			fmt = 'l'
			fmt_size = 4
			self._charSize 	= struct.unpack(fmt,file.read(fmt_size))[0]
			self.points 	= struct.unpack(fmt,file.read(fmt_size))[0]
			self.height		= struct.unpack(fmt,file.read(fmt_size))[0]
			self.maxWidth 	= struct.unpack(fmt,file.read(fmt_size))[0]
			self.charFirst 	= struct.unpack(fmt,file.read(fmt_size))[0]
			self._charLast	= struct.unpack(fmt,file.read(fmt_size))[0]
			self._unknown4 	= struct.unpack(fmt,file.read(fmt_size))[0]
			self._wmapAddr 	= struct.unpack(fmt,file.read(fmt_size))[0]
			self._cmapAddr 	= struct.unpack(fmt,file.read(fmt_size))[0]
			self.descent	= struct.unpack(fmt,file.read(fmt_size))[0]
			self.intline 	= struct.unpack(fmt,file.read(fmt_size))[0]
			self.wTable		= []
			self.cTable		= []
	
			self.width = 8 * self._charSize / self.height
			self.charCount = self._charLast - self.charFirst + 1
	
			charlist = xrange(0, self.charCount)
			file.seek(self._wmapAddr)
			for char in charlist:
				self.wTable.append(struct.unpack('B',file.read(1))[0])
			file.seek(self._cmapAddr)
			for char in charlist:
				self.cTable.append(file.read(self._charSize))
			isOk = TRUE
		else:
			isOk = FALSE
		
		return isOk
		

	def __save(self,file):
		'''
			Save rbFont structure to file
		'''
	
		self._wmapAddr = _FNT_HDR_SIZE
		self._cmapAddr = self._wmapAddr + self.charCount
		self._charSize = self.width * self.height /8
		self._charLast = self.charFirst + self.charCount - 1
		self._unknown4 = 32
		charlist = xrange(0,self.charCount)

		self.maxWidth = 0
		for char in charlist:
			self.maxWidth = max(self.maxWidth,self.wTable[char])

		file.write(_FNT_HDR_MAGIC)
		fmt = str(_FNT_MAX_NAME)+'s'
		file.write(struct.pack(fmt,self.name))
		fmt = 'l'
		file.write(struct.pack(fmt,self._charSize))
		file.write(struct.pack(fmt,self.points))
		file.write(struct.pack(fmt,self.height))
		file.write(struct.pack(fmt,self.maxWidth))
		file.write(struct.pack(fmt,self.charFirst))
		file.write(struct.pack(fmt,self._charLast))
		file.write(struct.pack(fmt,self._unknown4))
		file.write(struct.pack(fmt,self._wmapAddr))
		file.write(struct.pack(fmt,self._cmapAddr))
		file.write(struct.pack(fmt,self.descent))
		file.write(struct.pack(fmt,self.intline))

		for char in charlist:
			file.write(struct.pack('B',self.wTable[char]))

		for char in charlist:
			file.write(self.cTable[char])
		


	def getChar (self, charCode = 0):
		'''
			getChar(charCode) - returns a char of the font
		charCode - index of char position in font
			Returned value - tupple (char, width), where
		char - bytestring char representation
		width - integer width of char
			if charCode is greater than count of chars in font, 
		zero-filled string returns
		'''
		if charCode < self.charCount:
			char = (self.cTable[charCode], self.wTable[charCode])
		else:
			char = (self._charSize*'\x00', 0)
		return char
		
	
	def setChar (self, charCode, char):
		'''
			setChar(charcode, char) - set the element of the font
		charCode - index of char position in font
		char - tupple of two parameters:
		0 - bytestring char representation
		1 - integer width of char in pixels
		'''
		if charCode <= self.charCount:
			self.cTable[charCode] = char[0]
			self.wTable[charCode] = char[1]

		
def fontCreate (name, width, height, lspace=2, shift=32, count=224,):
	'''
		Create new rbFont object with next parameters:
	name	- font name (max 64 char)
	width	- maximal char width in pixels
	height	- maximal char height in pixels
	points	- font size in points
	shift	- ASCII code of first font symbol
	count	- count of chars in font
	lspace	- space between lines

	example: MyFont = createFont('My cool REB font', 16, 17, 
					  12,32,192,2)
	'''

	font = rbFont();
	font.name 		= name
	if width % 8 == 0 :
		font.width	= width
	else:
		font.width	= 8 * (width/8 + 1)
	font.height	= height
	font.points		= int(height*72.0/106.0)
	font.intline	= lspace
	font.charFirst	= shift
	font.charCount	= count
	font._charLast = shift + count -1
	
	
	charlist = xrange(0, font.charCount)
	chardata = ''
	for index in xrange(font.width*font.height/8):
		chardata += '\x00'
	for char in charlist:
		font.wTable.append(0)
		font.cTable.append(chardata)
	return font
	
	
def fontLoad(fname):
	'''
	Create new rbFont object from rbf font file
	fname	- name of file

	example: MyFont =  fontLoad('SomeFont.rbf')
	'''
	font = rbFont()    
	try:
		file = open(fname,'rb')
		isOk = font._rbFont__load(file)
		file.close()
	except IOError, err:
		print "Can't read file",fname , err
		isOk = 0
	
	if not isOk:
		font = None
	return font

    
def fontSave(font, fname):
	'''
	Save rbf font file from rbFont object
	font	- rbFont object
	fname	- name of file

	example: fontSave(MyFont, 'CoolFont.rbf')
	'''
	try:
		file = open(fname,'wb+')
		font._rbFont__save(file)
		file.close()
	except IOError, err:
		print "Can't write to file",fname , err

    

	

	
	
class rbFile:
	'''
		Class present API to a rocket ebook tile
	'''
	def __init__(self, type):
		'''
			Create a new rb file
		type - type of file, may be one of:
		RB_TYPE_TILE	- a rocket ebook tile
		RB_TYPE_EXEC	- an executable rocket ebook file
		RB_TYPE_SYSICONS- a system file with fonts and icons
		'''
		if type == RB_TYPE_TILE:
			self._header = _RB_TILE_MAGIC
		if type == RB_TYPE_EXEC:
			self._header = _RB_EXEC_MAGIC
		elif type == RB_TYPE_SYSICONS:
			self._header = _RB_SYSICONS_MAGIC
		else:
			self._header = _RB_UNKNOWN_MAGIC
		
		self._unknown0 = '\x4E\x55\x56\x4F\x00\x00\x00\x00'
		self._unknown1 = 6*'\x00'
		self._addrTOC = 0x128
		self._size = 0
		self._unknown2 = 264*'\x00'
		self._segments = []
		
		
	def _getDate(self):
		date 	= datetime.date(1,1,1)
		curDate = date.today().isoformat()
		year 	= string.atoi(curDate[0:4])
		month 	= string.atoi(curDate[5:7])
		day 	= string.atoi(curDate[8:10])
		return struct.pack('H', year) + struct.pack('B', month) + struct.pack('B', day)
		
		
	def addSegment(self, name, data, flags):
		'''
			Append new segment to file
		name	- name of segment
		data	- bytestring with segment data
		flags	- flags, indicates type of segment. May be any of
			RB_SEG_PLAIN	- a plain segment (without compression)
			RB_SEG_ENCRYPTED- an encrypted segment
			RB_SEG_INFO		- an info page
			RB_SEG_DEFLATED	- a compressed segment
		'''
		segment = {}
		segment['name'] = name
		segment['address'] = 0
		segment['flags'] = flags
		if flags == RB_SEG_DEFLATED:
			segment['data'] = self._compressSegment(data)
		else:
			segment['data'] = data
		segment['length'] = len(segment['data'])
		self._segments.append(segment)
		
		
	def _createTOC(self):
		address = self._addrTOC + _RB_TOC_ITEM_LEN * len(self._segments)+4
		for segment in self._segments:
			segment['address'] = address
			address += segment['length']
		self._size = address + 20
			
			
	def getFile (self):
		'''
			Returns bytestring with rb file contents
		'''
		self._createTOC()
		data = self._header
		data += _RB_VERSION
		data += self._unknown0
		data += self._getDate()
		data += self._unknown1
		data += struct.pack('l', self._addrTOC)
		data += struct.pack('l', self._size)
		data += self._unknown2
		data += struct.pack('l',len(self._segments))
		for segment in self._segments:
			data += struct.pack('32s', segment['name'])
			data += struct.pack('l', segment['length'])
			data += struct.pack('l', segment['address'])
			data += struct.pack('l', segment['flags'])
		for segment in self._segments:
			data += segment['data']
		data += 20*'\x01'
		return data
		
		
	def _compressSegment (self, data):
		uLength = len(data)
		uCount = uLength / _BLK_SIZE
		if uCount*_BLK_SIZE != uLength:
			uCount += 1
		uBlocks = []
		
		for index in xrange(uCount):
			block = data[index*_BLK_SIZE: (index+1)*_BLK_SIZE]
			uBlocks.append(block)
		
		zSizes = []
		zBlocks = []
		for index in xrange(uCount):
			compressor = zlib.compressobj(9, zlib.DEFLATED, 13)
			block = compressor.compress(uBlocks[index]) + compressor.flush(zlib.Z_FINISH)
			zBlocks.append(block)
			zSizes.append(len(block))
			del compressor
		
		segment = struct.pack('l',uCount)
		segment += struct.pack('l', uLength)
		for index in xrange(uCount):
			segment += struct.pack('l', zSizes[index])
		for index in xrange(uCount):
			segment += zBlocks[index]
		
		return segment
		
		
