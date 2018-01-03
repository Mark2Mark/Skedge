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
	NSNotificationCenter,\
	NSTextStorageDidProcessEditingNotification,\
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
year = "2017"
version = "1.2.6"
releaseDate = "2017-10-25"
versionDate = "2018-01-03"


#================
# T E M P L A T E
#================

templateCode = """
import traceback

scale = Glyphs.font.currentTab.scale
# layer = Glyphs.font.glyphs[0].layers[0]

def badge(x, y, s):
	path = NSBezierPath.alloc().init()
	rect = NSRect( (x-s/2, y-s/2), (s, s) )
	ovalInRect = NSBezierPath.bezierPathWithOvalInRect_( rect )
	path.appendBezierPath_( ovalInRect )
	NSColor.colorWithCalibratedRed_green_blue_alpha_( 1, .2, 0, .5 ).set()
	path.fill()

NSColor.greenColor().colorWithAlphaComponent_(0.3).set()
layer.bezierPath.fill()

for path in layer.paths:
	for node in path.nodes:
		badge(node.x, node.y, 15 / scale )
"""




#============
# C O L O R S
#============

codeEditorFontSize = 14
selectionBGColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.737, 0.914, 0, 0.5)
selectionFGColor = NSColor.blackColor()
editorBGColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(1.0, 1.0, 1.0, 0.1)
editorTextColor = NSColor.blackColor()
syntaxConstantsColor = NSColor.redColor()
syntaxKeywordsColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.086, 0.58, 0.682, 1)
syntaxDigitsColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.74, 0.0, 0.0, 1)
syntaxSecondTextColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.4, 0.4, 0.4, 1)
syntaxPunctuationColor = NSColor.orangeColor() # colorWithCalibratedRed_green_blue_alpha_(0, 0.77, 0.54, 1)
caretColor = NSColor.redColor()

buttonStyle = NSTexturedRoundedBezelStyle
__METHOD__ = DRAWBACKGROUND # DRAWFOREGROUND



#==============================
# S Y N T A X   K E Y W O R D S
#==============================

keywordsWithSpace = [ # Space to the right.
u"def ",
u"class ",
u"for ",
u"if ",
u"elif ",
u"else ",
u"from ",
u"print ",
u"except ",
u"global ",
u"as ",
u"print ",
u"import " ## ! KEEP u"import " at end of this list, otherwise some Keywords wont work !
]
keywordsWithSpaces = [u" in ",] # Space to both sides.
keywordsWithoutSpace = [u"try:", u"except:", u"else:", u"\%s", ] # Period not implemented
constants = [u"True", u"False", u"None", "self" ]
commentTrigger = u"#"



#========
# M A I N
#========

from vanilla import *

class CodeEditor(NSResponder):

	def init(self):

		## Subclass / Monkey Patch:
		## Avoid NSPanel close on ESC key:	
		def __cancel_(self, value):
			pass # print "ESC Key not closing the panel anymore :)"
		FloatingWindow.cancel_ = __cancel_
		## -------------------------

		# Inits
		#------
		self.vID = "com.markfromberg.%s" % name # vendorID
		self.toggle = False
		self.liveCodeMode = 0
		self.openFilePath = None
		self.w = FloatingWindow((800, 600), minSize=(400, 600), title="%s %s" % (name, version), autosaveName="%s.mainwindow" % self.vID ) ## restore window position

		# textView
		#---------
		self.w.textEditor = TextEditor((0, 0, -0, -40), templateCode, callback=self.doLiveCodeMode)
		self.textView = self.w.textEditor._textView
		# try: # Not needed here anymore. Will be set in `syntaxHighlighter()`
		# 	self.textView.setFont_( NSFont.fontWithName_size_( "Gintronic", codeEditorFontSize ) ) # Only if you got it :)
		# except:
		# 	self.textView.setFont_( NSFont.fontWithName_size_( "Menlo", codeEditorFontSize ) )

		self.textView.setTextColor_( editorTextColor )
		self.textView.setBackgroundColor_( editorBGColor )
		self.textView.setInsertionPointColor_( caretColor )
		self.textView.setRichText_( True )
		self.w.textEditor._nsObject.setBorderType_( NSNoBorder )
		self.texteEditorScrollView = self.w.textEditor._nsObject
		textSelection = {}
		textSelection[NSBackgroundColorAttributeName] = selectionBGColor
		textSelection[NSForegroundColorAttributeName] = selectionFGColor
		self.textView.setSelectedTextAttributes_( textSelection )
		self.textView.setUsesFindBar_( True )
		self.textView.setTextContainerInset_( ((10, 15)) )
		self.textView.turnOffLigatures_( True )


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
			try:
				exec self.code
				# Glyphs.clearLog() # Maybe better not.
			except:
				## This is the actual Code Log
				## TODO: pass into own log window.
				self.skedgeLog() # print traceback.format_exc()
		
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
				self.skedgeLog() # print traceback.format_exc()

	def skedgeLog(self):
		# Glyphs.clearLog() # Maybe better not.
		print traceback.format_exc()

	def performClick(self):
		self.w.runButton.getNSButton().performClick_(self.w.runButton.getNSButton())


	def syntaxHighlighter(self):

		#-------
		# Helper
		#-------

		def setFontInRange(fontName, fallbackFontName, range):
			try:
				self.textView.setFont_range_( NSFont.fontWithName_size_( fontName, codeEditorFontSize ), NSMakeRange(range[0], range[1]) )
			except:
				self.textView.setFont_range_( NSFont.fontWithName_size_( fallbackFontName, codeEditorFontSize ), NSMakeRange(range[0], range[1]) )


		def colorString(searchItem, line, color, lenTillEOL=0, checkForPreceedingLetter=False):
			try:
				for m in re.finditer(searchItem, line):
					startInLine = m.start()
					previousChar = line[m.start()-1]
					thisLineStart, foundLength = startInLine, m.end()-startInLine
					try:
						if checkForPreceedingLetter and previousChar.isalpha():
							pass
						else:
							s, e = thisLineStart + self.charCount+1, foundLength+lenTillEOL
							self.textView.setTextColor_range_(color, NSMakeRange(s, e) )
						if color == NSColor.grayColor(): # Set Italic for comments:
							setFontInRange( "Gintronic-Italic", "Menlo-Italic", (s, e) )
					except:
						pass
			except:
				pass # print traceback.format_exc()



		#---------------------------------------------------
		# Main
		#---------------------------------------------------

		try:
			self.textView.setTextColor_range_(NSColor.blackColor(), NSMakeRange(0, len(self.code))) # Reset first
			setFontInRange( "Gintronic", "Menlo", (0, len(self.code)) ) # Reset first

			ranges = {}


			self.charCount = 0
			for li, line in enumerate(self.code.splitlines()):

				if li > 0:
					self.charCount += 1 # LineBreak maybe?
				else:
					self.charCount -= 1

				# COMMENTS
				#---------
				'''
				BUG: When you have 2 or more exact same lines
				of comments, all but the first dont get grey.
				'''
				# A) Complete Comment Line
				if line.startswith( tuple([u"%s#" % (x * u"\t") for x in range(8)]) ): # allow 8 tabs in front of "#"
					try:
						try:
							start = self.code.index(str(line), len(line))
						except:
							start = self.code.index(str(line), 0) # Avoid stupid `ValueError: Substring not found`
						end = len(line)
						ranges[start] = ( end, NSColor.grayColor() )
						self.textView.setTextColor_range_(NSColor.grayColor(), NSMakeRange(start, end))
						setFontInRange( "Gintronic-Italic", "Menlo-Italic", (start, end) )
						self.charCount += len(line) # Do this AFTER Applying the range. We count the Lines UP to the currently checked one and add this to the found start
					except:
						pass # print traceback.format_exc()
				# B) Inline Comment (Works with only one "#" so far)
				# BUG: stops the previous parts of the line from highlighting.
				elif [m for m in re.finditer(commentTrigger, line)]:
					colorString( commentTrigger, line, NSColor.grayColor(), lenTillEOL=len(line.split(commentTrigger)[1]) )
					self.charCount += len(line)
					

				# ALL THE REST
				#-------------
				else:
					colorString( r"\d+", line, syntaxDigitsColor,checkForPreceedingLetter=True )
					colorString( r"[\*\+\-\/\=\!\>\<\%\&]", line, syntaxKeywordsColor )		
					colorString( r"[\(\)\{\}\[\]]", line, syntaxSecondTextColor )
					colorString( r"[\;\:\,]", line, syntaxPunctuationColor )
					colorString( r"\.", line, syntaxSecondTextColor )

					for kWord in keywordsWithSpace:
						colorString( kWord, line, syntaxKeywordsColor )
					for kWord in keywordsWithoutSpace:
						colorString( kWord, line, syntaxKeywordsColor )
					for kWord in keywordsWithSpaces:
						colorString( kWord, line, syntaxKeywordsColor )
					for kWord in constants:
						colorString( kWord, line, syntaxConstantsColor )

					self.charCount += len(line) # Do this AFTER Applying the range. We count the Lines UP to the currently checked one and add this to the found start
	

			# BLOCK COMMENTS
			#---------------
			# Now checking the whole self.code
			#
			# BUG: Not working with line breaks yet.
			# `re.compile(searchstring, re.MULTILINE)` not figured out.
			try:
				BCTrigger = u"\'\'\'"
				foundBC = ""
				try:
					result = re.search(u"\'\'\'(.*)\'\'\'", self.code)
					foundBC = "%s%s%s" % ( BCTrigger, result.group(1), BCTrigger )
				except:
					result = re.search(u"\'\'\'\n(.*)\n\'\'\'", self.code)
					foundBC = "%s\n%s\n%s" % ( BCTrigger, result.group(1), BCTrigger )
				if len(foundBC) > 0:
					for m in re.finditer( re.escape(foundBC), self.code): # re.escape() to make special chars work (e.g. [] () * + ...)
						bs, be = m.start(), len(foundBC)
						self.textView.setTextColor_range_(NSColor.grayColor(), NSMakeRange(bs, be) )
						setFontInRange( "Gintronic-Italic", "Menlo-Italic", (bs, be) )
			except:
				pass # print traceback.format_exc()




		except:
			self.skedgeLog() # print traceback.format_exc()
			# console.log( traceback.format_exc() )
			

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
				self.skedgeLog()

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



