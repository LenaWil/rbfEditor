# -*- coding: utf-8 -*-
'''
	Module contains project global constants
'''

import qt
import os

NAME = 'rbfEditor'
VERSION = '0.1'

FALSE = 0
TRUE = 1

LINUX = 0
WINDOWS = 1

EBOOKW = 320					# width of ebook preview window
EBOOKH = 480					# height of ebook preview window
EBOOKBG = qt.QColor(255,255,255)	# background color of ebook preview window

RBF_NEW 	= 0		# Action: create new font
RBF_OPEN 	= 1		# Action: open existing font from file
RBF_TTF 	= 2		# Action: create new font from truetype font


if os.name == 'posix':
	OS = LINUX
	FONTDIR = '/usr/share/fonts/TTF'
elif os.name == 'nt':
	OS = WINDOWS
	FONTDIR = 'C:\\Windows\\Fonts'

HOMEDIR = os.path.expanduser('~/')


