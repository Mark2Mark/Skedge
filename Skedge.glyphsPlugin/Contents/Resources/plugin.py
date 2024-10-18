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

from GlyphsApp import Glyphs, WINDOW_MENU
from GlyphsApp.plugins import GeneralPlugin
from Cocoa import NSMenuItem, NSLog
import objc
import traceback

from SkedgeModule import CodeEditor


class SkedgePlugin(GeneralPlugin):
	@objc.python_method
	def settings(self):
		self.name = "Skedge"

	@objc.python_method
	def start(self):
		try:
			targetMenu = WINDOW_MENU  # EDIT_MENU # SCRIPT_MENU
			separator = NSMenuItem.separatorItem()
			Glyphs.menu[targetMenu].append(separator)
			s = objc.selector(self.skedge_, signature=b'v@:')
			newMenuItem = NSMenuItem(self.name, s)
			Glyphs.menu[targetMenu].append(newMenuItem)
		except:
			NSLog(traceback.format_exc())

	def skedge_(self, notification=None):
		try:
			CodeEditor.new()
		except:
			NSLog(traceback.format_exc())
