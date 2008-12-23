#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('./modules')
from mainapp import *

if __name__ == "__main__":
	app = Application(sys.argv)
	app.exec_loop()
	app.prefs.saveToDisk()
#	del app
