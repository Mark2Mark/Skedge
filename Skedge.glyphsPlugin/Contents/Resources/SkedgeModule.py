# -*- coding: utf-8 -*-

###########################################################################################################
#
#
#	Copyright 2017
#	Mark Frömberg
#	www.markfromberg.com
#	@Mark2Mark
#
#	https://pythex.org/ REGEX Tester
#	PyQT
#
#	TODO:
#		+ NSLayoutManager addTemporaryAttributes ?
#
###########################################################################################################


from __future__ import print_function
from Foundation import NSResponder, NSFileTypeForHFSTypeCode, NSRect
from AppKit import NSBezierPath,\
	NSColor,\
	NSFont,\
	NSFontWeightRegular,\
	NSBackgroundColorAttributeName,\
	NSForegroundColorAttributeName,\
	NSMutableParagraphStyle,\
	NSParagraphStyleAttributeName,\
	NSNoBorder,\
	NSFloatingWindowLevel,\
	NSWindowStyleMaskFullSizeContentView,\
	NSTitledWindowMask,\
	NSClosableWindowMask,\
	NSMiniaturizableWindowMask,\
	NSResizableWindowMask,\
	NSWindowCollectionBehaviorManaged,\
	NSAppearance,\
	NSAppearanceNameVibrantDark,\
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
import re, objc, os, io
from GlyphsApp import *


name = "Skedge"
author = u"Mark Frömberg"
version = "1.2.9"
releaseDate = "2017-10-25"


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
Glyphs.registerDefault("SkedgeCode", templateCode)



#============
# C O L O R S
#============

def NSrgba_(*args):
	return NSColor.colorWithDeviceRed_green_blue_alpha_(*args) # more real colors

codeEditorFontSize = 14

colorFraction = 255.0

# Dark Scheme:
selectionBGColor =       NSrgba_(72/colorFraction, 76/colorFraction, 91/colorFraction, 1)
editorBGColor =          NSColor.colorWithHue_saturation_brightness_alpha_(0.6, 0.4, 0.22, 1.0) # nice GlyphsApp dark green: 0.5, 0.4, 0.22 # 0.785, 0.2, 0.225, #NSrgba_(50/colorFraction, 53/colorFraction, 63/colorFraction, 1) # rgb % 18 24 27
editorTextColor =        NSColor.colorWithHue_saturation_brightness_alpha_(0, 0, 1, 0.8)
syntaxConstantsColor =   NSrgba_(245/colorFraction, 135/colorFraction, 126/colorFraction, 1)
syntaxKeywordsColor =    NSColor.colorWithHue_saturation_brightness_alpha_(0.90, 0.6, 1.0, 1) # NSrgba_(222/colorFraction, 161/colorFraction, 243/colorFraction, 1)
syntaxDigitsColor =      NSColor.colorWithHue_saturation_brightness_alpha_(0.13, 0.6, 0.9, 1)
syntaxMethodColor =      NSColor.colorWithHue_saturation_brightness_alpha_(0.35, 0.2, 0.9, 1)
syntaxSecondTextColor =  NSColor.colorWithHue_saturation_brightness_alpha_(0.45, 0.9, 0.9, 1)
syntaxCommentTextColor = editorTextColor.colorWithAlphaComponent_(0.4)
syntaxStringBGColor =    NSColor.colorWithHue_saturation_brightness_alpha_(0.55, 0.9, 0.9, 0.1)
syntaxStringFGColor =    NSColor.colorWithHue_saturation_brightness_alpha_(0.55, 0.7, 1.0, 1.0)
syntaxClassesColor =     NSColor.colorWithHue_saturation_brightness_alpha_(0.25, 0.5, 1.0, 1.0)
syntaxPunctuationColor = NSColor.colorWithHue_saturation_brightness_alpha_(0.55, 1.0, 0.8, 1.0)
caretColor =             NSColor.redColor()


buttonStyle = NSTexturedRoundedBezelStyle
__METHOD__ = DRAWBACKGROUND # DRAWFOREGROUND



#==============================
# S Y N T A X   K E Y W O R D S
#==============================

keywordsWithSpace = [
	u"def ",
	u"class ",
	u"for ",
	u"while ",
	u"if ",
	u"elif ",
	u"else ",
	u"finally ",
	u"from ",
	u"print ",
	u"except ",
	u"global ",
	u"return ",
	u"as ",
	u"print ",
	u"import " ## ! KEEP u"import " at end of this list, otherwise some Keywords wont work !
] # Space to the right.
keywordsWithSpaces = [
	u" in ",
	u" and ",
	u" not ",
	u" is ",
	u" or ",
	u" raise ",
	u" yield ",
] # Space to both sides.
keywordsWithoutSpace = [
	u"try:",
	u"except:",
	u"finally:",
	u"else:",
	u"\%s",
]
constants = [
	u"True",
	u"False",
	u"None",
	u"self",
	u"break",
	u"pass",
	u"return",
	u"continue",
]
commentTrigger = u"#"
glyphsAppInternals = [
	"Glyphs",
	"GlyphsApp",
	"Font",
	"Layer",
]
glyphsAppConstants = ["MOVE", "LINE", "CURVE", "OFFCURVE", "QCURVE", "HOBBYCURVE", "GSMOVE", "GSLINE", "GSCURVE", "GSQCURVE", "GSOFFCURVE", "GSHOBBYCURVE", "GSSHARP", "GSSMOOTH",
	"FILL", "FILLCOLOR", "FILLPATTERNANGLE", "FILLPATTERNBLENDMODE", "FILLPATTERNFILE", "FILLPATTERNOFFSET", "FILLPATTERNSCALE", "STROKECOLOR", "STROKELINECAPEND", "STROKELINECAPSTART", "STROKELINEJOIN", "STROKEPOSITION", "STROKEWIDTH", "GRADIENT", "SHADOW", "INNERSHADOW", "MASK", 
	"INSTANCETYPESINGLE", "INSTANCETYPEVARIABLE",
	"TAG", "TOPGHOST", "STEM", "BOTTOMGHOST", "FLEX", "TTSNAP", "TTSTEM", "TTSHIFT", "TTINTERPOLATE", "TTDIAGONAL", "TTDELTA", "CORNER", "CAP", "TTDONTROUND", "TTROUND", "TTROUNDUP", "TTROUNDDOWN", "TRIPLE",
	"TTANCHOR", "TTALIGN", # backwards compatibilty 
	"TEXT", "ARROW", "CIRCLE", "PLUS", "MINUS",
	"LTR", "RTL", "LTRTTB", "RTLTTB", "GSTopLeft", "GSTopCenter", "GSTopRight", "GSCenterLeft", "GSCenterCenter", "GSCenterRight", "GSBottomLeft", "GSBottomCenter", "GSBottomRight",
]
glyphsAppCallbacks = [
	"DRAWFOREGROUND", "DRAWBACKGROUND", "DRAWINACTIVE", "DOCUMENTOPENED", "DOCUMENTACTIVATED", "DOCUMENTWASSAVED", "DOCUMENTEXPORTED", "DOCUMENTCLOSED", "DOCUMENTWILLCLOSE", "DOCUMENTDIDCLOSE", "TABDIDOPEN", "TABWILLCLOSE", "UPDATEINTERFACE",
	"MOUSEMOVED", "MOUSEDRAGGED", "MOUSEDOWN", "MOUSEUP", "CONTEXTMENUCALLBACK",
]



#========
# M A I N
#========

from vanilla import Window, FloatingWindow, TextEditor, CheckBox, Button

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
		self.w = FloatingWindow((800, 600), minSize=(400, 400), title="%s %s" % (name, version), autosaveName="%s.mainwindow" % self.vID ) ## restore window position
		nsWindow = self.w.getNSWindow()
		# nsWindow.setLevel_(NSFloatingWindowLevel)
		# nsWindow.setCollectionBehavior_(NSWindowCollectionBehaviorManaged )
		nsWindow.setStyleMask_( NSTitledWindowMask | NSClosableWindowMask | NSMiniaturizableWindowMask | NSResizableWindowMask)
		nsWindow.setAppearance_(NSAppearance.appearanceNamed_(NSAppearanceNameVibrantDark))
		nsWindow.setTitlebarAppearsTransparent_( True )
		nsWindow.setBackgroundColor_( editorBGColor )
		
		

		# textView
		#---------
		self.w.textEditor = TextEditor((0, 0, -0, -40), Glyphs.defaults["SkedgeCode"], callback=self.doLiveCodeMode_)
		self.textView = self.w.textEditor._textView

		self.textView.setTextColor_( editorTextColor )
		self.textView.setBackgroundColor_( editorBGColor )
		self.textView.setInsertionPointColor_( caretColor )
		self.textView.setRichText_( True )
		self.w.textEditor._nsObject.setBorderType_( NSNoBorder )
		self.texteEditorScrollView = self.w.textEditor._nsObject
		textSelection = {}
		textSelection[NSBackgroundColorAttributeName] = selectionBGColor
		# textSelection[NSForegroundColorAttributeName] = selectionFGColor
		self.textView.setSelectedTextAttributes_( textSelection )
		self.textView.setUsesFindBar_( True )
		self.textView.setTextContainerInset_( ((20, 20)) )
		self.textView.turnOffLigatures_( True )

		self.textView.setAutomaticDashSubstitutionEnabled_( False )
		self.textView.setAutomaticDataDetectionEnabled_( False )
		self.textView.setAutomaticLanguageIdentificationEnabled_( False )
		self.textView.setAutomaticLinkDetectionEnabled_( False )
		self.textView.setAutomaticQuoteSubstitutionEnabled_( False )
		self.textView.setAutomaticSpellingCorrectionEnabled_( False )
		self.textView.setAutomaticTextReplacementEnabled_( False )
		self.textView.setSmartInsertDeleteEnabled_( False )

		self.textView.setMenu_( None )

		#ta = self.textView.typingAttributes().mutableCopy()
		#ps = NSMutableParagraphStyle.alloc().init()
		#ps.setLineSpacing_(30.0)
		#ps.setMinimumLineHeight_(30.0)
		#ps.setMaximumLineHeight_(30.0)
		#ps.setLineHeightMultiple_(3.0)
		#ta.setObject_forKey_(ps, NSParagraphStyleAttributeName)
		##self.textView.setDefaultParagraphStyle_(ps)
		#print(self.textView.defaultParagraphStyle())


		# Buttons
		#--------
		self.w.liveCode = CheckBox((10, -32, 80, 22), "Live", value=True)
		self.w.runButton = Button((80+10, -32, -150-10, 22), u"Run ⌘R", callback=self.run_)
		self.w.runButton._nsObject.setBezelStyle_( buttonStyle )
		self.w.runButton.bind("r", ["command"])
		self.w.resetButton = Button((-150+10, -32, -15, 22), u"Reset ⌘K", callback=self.reset_)
		self.w.resetButton._nsObject.setBezelStyle_( buttonStyle )
		self.w.resetButton.bind("k", ["command"])

		self.w.bind("close", callback=self.onClose_)
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
		self.saveFile_(sender)

	def openDocument_(self, sender):
		# print "openDocument_"
		self.openFile_(sender)


	#==================
	# C A L L B A C K S
	#==================

	def addCallback(self):
		try:
			Glyphs.addCallback(self.drawCode, __METHOD__)
		except:
			print(traceback.format_exc())

	def removeCallback(self):
		try:
			Glyphs.removeCallback(self.drawCode, callbackType=__METHOD__)
		except:
			print(traceback.format_exc())

	@objc.python_method
	def drawCode(self, layer, info):
		if self.code is not None:
			try:
				exec(self.code)
				# Glyphs.clearLog() # Maybe better not.
			except:
				## This is the actual Code Log
				## TODO: pass into own log window.
				self.skedgeLog() # print traceback.format_exc()

	def run_(self, sender):
		self.code = self.w.textEditor.get()
		self.syntaxHighlighter()
		Glyphs.redraw()

	def reset_(self, sender):
		self.code = None
		Glyphs.redraw()

	def onClose_(self, sender):
		self.removeCallback()

	def doLiveCodeMode_(self, sender):
		self.liveCodeMode = self.w.liveCode.get()
		if self.liveCodeMode == 1:
			try:
				self.run_(sender)
			except:
				self.skedgeLog() # print traceback.format_exc()
		Glyphs.defaults["SkedgeCode"] = self.textView.string()

	def skedgeLog(self):
		# Glyphs.clearLog() # Maybe better not.
		print(traceback.format_exc())

	def performClick(self):
		self.w.runButton.getNSButton().performClick_(self.w.runButton.getNSButton())


	def syntaxHighlighter(self):

		#-------
		# Helper
		#-------

		def setFontInRange(range):
			try:
				#try:
				#	font = NSFont.fontWithName_size_("Neutronic Mono v0.2.3 Normal", codeEditorFontSize)
				#except:
				#	font = NSFont.monospacedSystemFontOfSize_weight_(codeEditorFontSize, NSFontWeightRegular)
				font = NSFont.monospacedSystemFontOfSize_weight_(codeEditorFontSize, NSFontWeightRegular)
			except:
				font = NSFont.userFixedPitchFontOfSize_(codeEditorFontSize)
			self.textView.setFont_range_(font, NSMakeRange(range[0], range[1]) )

		def colorString(searchItem, line, color, lenTillEOL=0, checkForPreceedingLetter=False, trim=False, background=False):
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
							if trim:
								e -= 1
							if background:
								self.textView.attributedString().addAttribute_value_range_(NSBackgroundColorAttributeName, color, NSMakeRange(s, e))
							else:
								self.textView.setTextColor_range_(color, NSMakeRange(s, e) )
						if color == syntaxCommentTextColor: # Set Italic for comments:
							setFontInRange((s, e))
					except:
						pass
			except:
				pass # print traceback.format_exc()



		#---------------------------------------------------
		# Main
		#---------------------------------------------------
		commentRE = "#[^\n]*"
		comments = []
		try:
			# Reset Text Attributes from copied text (Thanks to Georg Seifert @schriftgestalt):
			textStorage = self.textView.textStorage()
			textStorage.setAttributes_range_( {}, NSMakeRange( 0, textStorage.length() ) )

			# Basic Reset:
			self.textView.setTextColor_range_(editorTextColor, NSMakeRange(0, len(self.code))) # Reset first
			setFontInRange((0, len(self.code))) # Reset first

			ranges = {}


			self.charCount = 0
			for li, line in enumerate(self.code.splitlines()):

				if li > 0:
					self.charCount += 1 # LineBreak maybe?
				else:
					self.charCount -= 1





				# ALL THE REST
				#-------------
				# else:
				colorString( r"(?<![a-zA-Z_])\d+", line, syntaxDigitsColor,checkForPreceedingLetter=True ) # digits, if not preceeded by letter or underscore
				colorString( r"[\*\+\-\/\=\!\>\<\%\&]", line, syntaxKeywordsColor )
				colorString( r"[\(\)\{\}\[\]]", line, syntaxSecondTextColor )
				colorString( r"[\;\:\,]", line, syntaxPunctuationColor )
				colorString( r"\.", line, syntaxSecondTextColor )

				# Method Calls
				# not quite: r"\.(.*?)\("
				# look around https://stackoverflow.com/questions/3926451/how-to-match-but-not-capture-part-of-a-regex
				# colorString( r"(?<=\.)(.*?)(?=\()", line, syntaxMethodColor ) # Between . and (
				#colorString( r"(?<=\.|\s)([a-zA-Z+_]*?)(?=\(|\))", line, syntaxMethodColor ) # any of these a-zA-Z_ between `.` or `space` and `(` or `)`, any amount of `_` in name
				colorString( r"(?<=\.|\s)([a-zA-Z0-9_]*?)(?=\()", line, syntaxMethodColor ) # any of these a-zA-Z_ between `.` or `space` and `(` or `)`, any amount of `_` in name
				#
				
				for kWord in keywordsWithSpace:
					colorString( kWord, line, syntaxKeywordsColor )
				for kWord in keywordsWithoutSpace:
					colorString( kWord, line, syntaxKeywordsColor, trim=True )
				for kWord in keywordsWithSpaces:
					colorString( kWord, line, syntaxKeywordsColor )
				for kWord in constants:
					colorString( kWord, line, syntaxConstantsColor )

				# COMMENTS
				#---------
				# from `#` up to newLine
				for m in re.finditer(commentRE, line):
					try:
						s, e = m.start(), m.end()
						mm = m.group()
						comments.append(NSMakeRange(s+self.charCount +1, e-s)) # instead of appending mm, use the range directly
					except:
						pass
				
				# colorString( r"(?<=\")(.*?)(?=\")", line, syntaxStringBGColor, background=True ) # strings between " ... " or ' ... ' excluding quotes
				colorString( r"(\"|\')(.*?)(\"|\')", line, syntaxStringBGColor, background=True ) # strings between " ... " or ' ... ' including quotes. Nicer than excluding quotes
				colorString( r"(\"|\')(.*?)(\"|\')", line, syntaxStringFGColor ) # same, but foreground

				# AppKit Stuff
				colorString( r"(?<![a-zA-Z])(?=NS)(.*?)\.", line, syntaxClassesColor, trim=True ) # e.g NSColor (only if followed by . and if not preceeded by a letter)
				# GlyphsApp
				colorString( r"(?<![a-zA-Z])(?=GS)(.*?)\.", line, syntaxClassesColor, trim=True ) # e.g GSFont (only if followed by . and if not preceeded by a letter) # (?=GS)(.*?)\.

				for glyphsAppInternal in glyphsAppInternals:
					colorString( r"(?<![a-zA-Z])%s(?![a-zA-Z])" % glyphsAppInternal, line, syntaxClassesColor ) # explicit words, not predceeded and followed by any letter
				for glyphsAppConstant in glyphsAppConstants:
					colorString( r"(?<![a-zA-Z])%s(?![a-zA-Z])" % glyphsAppConstant, line, syntaxClassesColor ) # explicit words, not predceeded and followed by any letter					
				for glyphsAppCallback in glyphsAppCallbacks:
					colorString( r"(?<![a-zA-Z])%s(?![a-zA-Z])" % glyphsAppCallback, line, syntaxClassesColor ) # explicit words, not predceeded and followed by any letter					

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
						self.textView.setTextColor_range_(syntaxCommentTextColor, NSMakeRange(bs, be) )
						setFontInRange((bs, be))
			except:
				pass # print traceback.format_exc()



		except:
			self.skedgeLog() # print traceback.format_exc()
			# console.log( traceback.format_exc() )
		
		for comment in comments:
			#range = self.textView.string().rangeOfString_(comment) # could be slower, so we use the range isntead of the string
			try:
				self.textView.setTextColor_range_(syntaxCommentTextColor, comment )
			except:
				pass


	#======================
	# O P E N   &   S A V E
	#======================

	def openFile_(self, sender):
		filePath = GetOpenFile(message="Open a .py file.", filetypes=["py"])
		if filePath is not None:
			with open(filePath) as f:
				code = f.readlines()
			try:
				code = "".join(code)
				self.w.textEditor.set(code)
				self.performClick()
				try:
					self.w.setTitle("%s %s     [%s]" % (name, version, filePath.lastPathComponent()))
				except: pass
			except:
				self.skedgeLog()

	def saveFile_(self, sender):
		filePath = GetSaveFile(message="Save your Code as a .py file.", ProposedFileName="%s - " % name, filetypes=["py"])
		if filePath is not None:
			content = self.w.textEditor.get()
			try:
				with io.open(filePath, 'w+') as f:
					f.write(content)
			except:
				Message("Could not save file.", "")


	#==========
	# P R I N T
	#==========

	def printDocument_(self, sender):
		self.texteEditorScrollView.print_( True )

	def print_(self, sender):
		NSPrintOperation.printOperationWithView_( self ).runOperation()
