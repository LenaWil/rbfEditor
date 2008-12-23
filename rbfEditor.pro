# rbfEditor qmake file

TEMPLATE = app
SOURCES = main.py \
modules/about.py modules/bookpreview.py modules/charwin.py \
modules/fontprefs.py modules/fonttable.py modules/fontwin.py \
modules/globals.py modules/mainapp.py modules/mainwin.py \
modules/picturetable.py modules/prefs.py modules/settings.py \
modules/sysicons.py modules/ttfselect.py modules/upload.py

TRANSLATIONS = translation-ru.ts

TARGET = rbfEditor
DISTFILES = icons.py COPYING README README.RUS 


DESTDIR = /usr/bin
