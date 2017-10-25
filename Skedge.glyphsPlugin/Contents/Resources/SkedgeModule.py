# -*- coding: utf-8 -*-

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


from Foundation import NSResponder, NSFileTypeForHFSTypeCode, NSRect
from AppKit import NSBezierPath,\
	NSColor,\
	NSFont,\
	NSBackgroundColorAttributeName,\
	NSForegroundColorAttributeName,\
	NSMutableParagraphStyle,\
	NSNoBorder,\
	NSPrintOperation,\
	NSRoundRectBezelStyle,\
	NSRecessedBezelStyle,\
	NSShadowlessSquareBezelStyle,\
	NSDisclosureBezelStyle,\
	NSTexturedRoundedBezelStyle,\
	NSWorkspace,\
	NSImage,\
	NSImageScaleProportionallyDown,\
	NSImageNameActionTemplate,\
	NSImageNameFontPanel,\
	NSImageNameShareTemplate,\
	NSSavePanel,\
	NSMakeRange,\
	NSOpenPanel
import traceback
import re
from GlyphsApp import *


name = "Skedge"
author = u"Mark Frömberg"
year = "2016"
version = "1.2"
releaseDate = "2017-10-25"
versionDate = "2017-10-25"


#================
# T E M P L A T E
#================

templateCode = """
import traceback

scale = Glyphs.font.currentTab.scale
# layer = Glyphs.font.glyphs[0].layers[0]

try:
	NSColor.greenColor().colorWithAlphaComponent_(0.5).set()
	layer.bezierPath.fill()
except:
	print traceback.format_exc()

def badge(x, y, size):
	myPath = NSBezierPath.alloc().init()
	myRect = NSRect( ( x-size / 2, y-size / 2 ), ( size, size ) )
	thisPath = NSBezierPath.bezierPathWithOvalInRect_( myRect )
	myPath.appendBezierPath_( thisPath )
	NSColor.colorWithCalibratedRed_green_blue_alpha_( 1, .2, 0, .65 ).set()
	myPath.fill()

for path in layer.paths:
	for node in path.nodes:
		badge(node.x, node.y, 42 / scale )
"""




#============
# C O L O R S
#============

selectionColorBG = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.737, 0.914, 0, 0.5) # (0, 0.75, 1, 0.5)
selectionColorFG = NSColor.blackColor()
textFieldColorBG = NSColor.colorWithCalibratedRed_green_blue_alpha_(1.0, 1.0, 1.0, 0.1)
textFieldColorText = NSColor.blackColor()
syntaxConstantsColor = NSColor.redColor()
syntaxKeywordsColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.086, 0.58, 0.682, 1) # (0.09, 0.67, 0.65, 1)
syntaxPunctuationColor = NSColor.orangeColor() # colorWithCalibratedRed_green_blue_alpha_(0, 0.77, 0.54, 1)
caretColor = NSColor.redColor()

buttonStyle = NSTexturedRoundedBezelStyle
__METHOD__ = DRAWBACKGROUND # DRAWFOREGROUND



#==============================
# S Y N T A X   K E Y W O R D S
#==============================

keywordsWithSpace = [
u"def ",
u"for ",
u"in ",
u"from ",
u"print ",
u"except ",
u"as ",
u"\+ ", # Not working
u"- ",
u"\* ", # Not working
u"/ ",
u"= ",
u"== ",
u"!= ",
u"< ",
u"> ",
u">= ",
u"<= ",
u"+= ",
u"-= ",
u"import " ## ! KEEP u"import " at end of this list, otherwise some Keywords wont work !
]
keywordsWithoutSpace = [u"try:", u"except:",] # Period not implemented
constants = [u" True", u" False", u" None", ]




#========
# M A I N
#========

from vanilla import *

class CodeEditor(NSResponder):

	def init(self):

		# Inits
		#------
		self.vID = "com.markfromberg.%s" % name # vendorID
		self.toggle = False
		self.liveCodeMode = 0
		self.openFilePath = None
		self.w = FloatingWindow((800, 600), minSize=(800, 600), title="%s %s" % (name, version), autosaveName="%s.mainwindow" % self.vID ) ## restore window position

		# textView
		#---------
		self.w.textEditor = TextEditor((0, 0, -0, -40), templateCode, callback=self.doLiveCodeMode)
		self.textView = self.w.textEditor._textView
		try:
			self.textView.setFont_( NSFont.fontWithName_size_( "Gintronic", 14 ) ) # Only if you got it :)
		except:
			self.textView.setFont_( NSFont.fontWithName_size_( "Menlo", 14 ) )

		self.textView.setTextColor_( textFieldColorText )
		self.textView.setBackgroundColor_( textFieldColorBG )
		self.textView.setInsertionPointColor_( caretColor )
		self.textView.setRichText_( True )
		self.w.textEditor._nsObject.setBorderType_( NSNoBorder )
		self.texteEditorScrollView = self.w.textEditor._nsObject
		textSelection = {}
		textSelection[NSBackgroundColorAttributeName] = selectionColorBG
		textSelection[NSForegroundColorAttributeName] = selectionColorFG
		self.textView.setSelectedTextAttributes_( textSelection )
		self.textView.setUsesFindBar_( True )
		self.textView.setTextContainerInset_( ((10, 15)) )

		# Buttons
		#--------
		self.w.liveCode = CheckBox((10, -32, 80, 22), "Live", value=True)
		self.w.runButton = Button((80+10, -32, -150-10, 22), u"Run ⌘R", callback=self.run)
		self.w.runButton._nsObject.setBezelStyle_( buttonStyle )
		self.w.runButton.bind("r", ["command"])
		self.w.resetButton = Button((-150+10, -32, -15, 22), u"Reset ⌘K", callback=self.reset)
		self.w.resetButton._nsObject.setBezelStyle_( buttonStyle )
		self.w.resetButton.bind("k", ["command"])
		
		self.w.bind("close", callback=self.onClose)
		self.w.open()
	
		# Enable the saveDocument_ & openDocument_ be
		# triggered by the menu or keyboard shortcuts
		#-----------------------------------------------
		nextResponder = self.w._window.nextResponder()
		self.w._window.setNextResponder_( self )
		self.setNextResponder_( nextResponder )
		
		self.code = None
		self.w.makeKey()
		self.addCallback()
		self.performClick() # First Run after opening a file, must be after addCallback()

	
	def saveDocument_(self, sender):
		# print "saveDocument_"
		### Maybe store the file name and just write the file on the second run
		self.saveFile(sender)
		
	def openDocument_(self, sender):
		# print "openDocument_"
		self.openFile(sender)


	#==================
	# C A L L B A C K S
	#==================
	
	def addCallback(self):
		try:
			Glyphs.addCallback(self.drawCode, __METHOD__)
		except:
			print traceback.format_exc()
	
	def removeCallback(self):
		try:
			Glyphs.removeCallback(self.drawCode, __METHOD__)
		except:
			print traceback.format_exc()

	def drawCode(self, layer, info):
		if self.code is not None:
			exec self.code
		
	def run(self, sender):
		self.code = self.w.textEditor.get()
		self.syntaxHighlighter()		
		Glyphs.redraw()

	def reset(self, sender):
		self.code = None
		Glyphs.redraw()

	def onClose(self, sender):
		self.removeCallback()

	def doLiveCodeMode(self, sender):
		self.liveCodeMode = self.w.liveCode.get()
		if self.liveCodeMode == 1:
			try:
				self.run(sender)
			except:
				print traceback.format_exc()

	def performClick(self):
		self.w.runButton.getNSButton().performClick_(self.w.runButton.getNSButton())


	def syntaxHighlighter(self):

		def findIter(subString, completeString):
			return [m.start() for m in re.finditer(subString, completeString)]

		def doPunctuation(mySring):
			mySring = str(mySring)
			if mySring in "%s " % w:
				for start in findIter(mySring, self.code): # [m.start() for m in re.finditer(kWord, self.code)]:
					end = len(mySring)
					ranges.append( (start, end, syntaxPunctuationColor ) )			

		self.textView.setTextColor_range_(NSColor.blackColor(), NSMakeRange(0, len(self.code))) # Reset first
		ranges = []
		for line in self.code.splitlines():
			# Comments: Gray
			#---------------
			if line.startswith( tuple([u"%s#" % (x * u"\t") for x in range(8)]) ): # allow 8 tabs in front of "#"
				start = self.code.index(line, len(line))
				end = len(line)
				ranges.append( (start, end, NSColor.grayColor()) )


			# keywords: Orange
			#-------------------
			# ddd = u"."
			# if ddd in line:
			# 	splitted = [u for x in line.split(ddd) for u in (x, ddd)] # Split at period, but keep period in list
			# 	splitted = splitted[:-1] # To get rid of trailing
			# else:
			# 	splitted = line.split(" ")
			splitted = line.split(" ")
			for w in splitted:
				doPunctuation(",") # Not working with period
				doPunctuation(":") # Not working with period
				for kWord in keywordsWithSpace:
					if kWord == "%s " % w.lstrip():
						for start in findIter(kWord, self.code):
							end = len(kWord)
							ranges.append( (start, end, syntaxKeywordsColor ) )
				for kWord in keywordsWithoutSpace:
					if kWord == w.lstrip():
						for start in findIter(kWord, self.code):
							end = len(kWord)
							ranges.append( (start, end, syntaxKeywordsColor ) )
				for kWord in constants:
					## A)
					if kWord == " %s" % w: # Case: " True" / " False"
						for start in findIter(kWord, self.code):
							end = len(kWord)
							ranges.append( (start, end, syntaxConstantsColor ) )
					## B)
					if "(%s)" % kWord[1:] in w: # Case: "(True)" / "(False)"
						for start in findIter(kWord[1:], self.code):
							end = len(kWord[1:])
							ranges.append( (start, end, syntaxConstantsColor ) )
					## Cannot merge A & B here.

		# Apply ranges
		#-------------
		for rng in ranges:
			s, e, color = rng
			self.textView.setTextColor_range_(color, NSMakeRange(s, e))


	#======================
	# O P E N   &   S A V E
	#======================

	def openFile(self, sender):
		panel = NSOpenPanel.openPanel()
		panel.setCanChooseFiles_( True )
		panel.setCanChooseDirectories_( False )
		panel.setAllowsMultipleSelection_( False )
		clicked = panel.runModalForDirectoryURL_file_types_relativeToWindow_( None, None, ["py"], self.w._window )
		if clicked == 1: # 0=cancel, 1=OK
			self.openFilePath = panel.URL().path() #or `.URLs()` if multiple files chosable
			code = ""
			with open(u"%s" % self.openFilePath) as f:
				code = f.readlines()
			try:
				code = "".join(code)
				self.w.textEditor.set(code)
				self.performClick()
				try:
					self.w.setTitle("%s %s     [%s]" % (name, version, self.openFilePath.lastPathComponent()))
				except: pass
			except:
				print traceback.format_exc()

	def saveFile(self, sender):
		panel = NSSavePanel.savePanel()
		panel.setMessage_( u"Save your Code as a .py file." )
		panel.setTitle_( u"%s: Save File" % name )
		panel.setTagNames_( [u"Python", name] )
		clicked = panel.runModalForDirectoryURL_file_types_relativeToWindow_( None, "%s - " % name, ["py"], self.w._window )
		if clicked == 1: # 0=cancel, 1=OK
			selectedFilePath = panel.URL().path()
			content = self.w.textEditor.get()
			try:
				with open(selectedFilePath, 'w+') as f:
					f.writelines(content)
			except:
				Message("Could not save file.", "")


	#==========
	# P R I N T
	#==========

	def printDocument_(self, sender):
		self.texteEditorScrollView.print_( True )

	def print_(self, sender):
		NSPrintOperation.printOperationWithView_( self ).runOperation()



