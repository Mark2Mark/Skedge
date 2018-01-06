# encoding: utf-8

###########################################################################################################
#
#
#	Copyright 2017
#	Mark Frömberg
#	www.markfromberg.com
#	@Mark2Mark
#
#
###########################################################################################################

from GlyphsApp import *
from GlyphsApp.plugins import *

import traceback, sys

from SkedgeModule import CodeEditor



class SkedgePlugin(GeneralPlugin):
	def settings(self):
		self.name = "Skedge"
	
	def start(self):
		try:
			targetMenu = WINDOW_MENU # EDIT_MENU # SCRIPT_MENU
			separator = NSMenuItem.separatorItem()
			Glyphs.menu[targetMenu].append(separator)
			s = objc.selector(self.skedge, signature='v@:')
			newMenuItem = NSMenuItem(self.name, s)
			Glyphs.menu[targetMenu].append(newMenuItem)
		except:
			import traceback
			NSLog(traceback.format_exc())
	
	def skedge(self):
		try:
			CodeEditor.new()
		except:
			NSLog(traceback.format_exc())
