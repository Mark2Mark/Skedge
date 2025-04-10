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
		targetMenu = WINDOW_MENU  # EDIT_MENU # SCRIPT_MENU
		separator = NSMenuItem.separatorItem()
		Glyphs.menu[targetMenu].append(separator)

		if Glyphs.buildNumber >= 3320:
			from GlyphsApp.UI import MenuItem
			newMenuItem = MenuItem(self.name, action=self.skedge_, target=self)
		else:
			newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(self.name, self.skedge_, "")
			newMenuItem.setTarget_(self)

		Glyphs.menu[targetMenu].append(newMenuItem)

	def skedge_(self, sender):
		try:
			CodeEditor.new()
		except:
			NSLog(traceback.format_exc())
