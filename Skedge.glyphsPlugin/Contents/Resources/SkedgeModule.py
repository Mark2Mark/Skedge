# -*- coding: utf-8 -*-

###########################################################################################################
#
#
# 	Copyright 2017
# 	Mark Frömberg
# 	www.markfromberg.com
# 	@Mark2Mark
#
# 	https://pythex.org/ REGEX Tester
# 	PyQT
#
# 	TODO:
# 		+ NSLayoutManager addTemporaryAttributes ?
#
###########################################################################################################


from __future__ import print_function
import traceback
import re
import objc
import io
from GlyphsApp import Glyphs, Message, GetOpenFile, GetSaveFile, DRAWBACKGROUND
from vanilla import FloatingWindow, TextEditor, CheckBox, Button

from Cocoa import (
    NSAttributedString,
    NSColor,
    NSFont,
    NSFontAttributeName,
    NSForegroundColorAttributeName,
    NSNotificationCenter,
    NSPrintOperation,
    NSResponder,
    NSRectFill,
    NSRulerView,
    NSFontWeightRegular,
    NSBackgroundColorAttributeName,
    NSNoBorder,
    NSTitledWindowMask,
    NSClosableWindowMask,
    NSMiniaturizableWindowMask,
    NSResizableWindowMask,
    NSAppearance,
    NSAppearanceNameVibrantDark,
    NSTexturedRoundedBezelStyle,
    NSMakeRange,
)


name = "Skedge"
author = "Mark Frömberg"
version = "1.4.0"
releaseDate = "2017-10-25"


# ================
# T E M P L A T E
# ================

templateCode = """
import traceback
scale = Glyphs.font.currentTab.scale
# layer = Glyphs.font.glyphs[0].layers[0]
def badge(x, y, s):
	path = NSBezierPath.alloc().init()
	rect = NSRect((x-s/2, y-s/2), (s, s))
	ovalInRect = NSBezierPath.bezierPathWithOvalInRect_(rect)
	path.appendBezierPath_(ovalInRect)
	NSColor.colorWithCalibratedRed_green_blue_alpha_(1, .2, 0, .5).set()
	path.fill()
NSColor.greenColor().colorWithAlphaComponent_(0.3).set()
layer.bezierPath.fill()
for path in layer.paths:
	for node in path.nodes:
		badge(node.x, node.y, 15 / scale)
"""
Glyphs.registerDefault("SkedgeCode", templateCode)


# ============
# C O L O R S
# ============


def NSrgba_(*args):
    return NSColor.colorWithDeviceRed_green_blue_alpha_(*args)  # more real colors


codeEditorFontSize = 14

colorFraction = 255.0

# Dark Scheme:
selectionBGColor = NSrgba_(
    72 / colorFraction, 76 / colorFraction, 91 / colorFraction, 1
)
editorBGColor = NSColor.colorWithHue_saturation_brightness_alpha_(
    0.6, 0.4, 0.22, 1.0
)  # nice GlyphsApp dark green: 0.5, 0.4, 0.22 # 0.785, 0.2, 0.225, #NSrgba_(50 / colorFraction, 53 / colorFraction, 63 / colorFraction, 1) # rgb % 18 24 27
editorTextColor = NSColor.colorWithHue_saturation_brightness_alpha_(0, 0, 1, 0.8)
syntaxConstantsColor = NSrgba_(
    245 / colorFraction, 135 / colorFraction, 126 / colorFraction, 1
)
syntaxKeywordsColor = NSColor.colorWithHue_saturation_brightness_alpha_(
    0.90, 0.6, 1.0, 1
)  # NSrgba_(222 / colorFraction, 161 / colorFraction, 243 / colorFraction, 1)
syntaxDigitsColor = NSColor.colorWithHue_saturation_brightness_alpha_(0.13, 0.6, 0.9, 1)
syntaxMethodColor = NSColor.colorWithHue_saturation_brightness_alpha_(0.35, 0.2, 0.9, 1)
syntaxSecondTextColor = NSColor.colorWithHue_saturation_brightness_alpha_(
    0.45, 0.9, 0.9, 1
)
syntaxCommentTextColor = editorTextColor.colorWithAlphaComponent_(0.4)
syntaxStringBGColor = NSColor.colorWithHue_saturation_brightness_alpha_(
    0.55, 0.9, 0.9, 0.1
)
syntaxStringFGColor = NSColor.colorWithHue_saturation_brightness_alpha_(
    0.55, 0.7, 1.0, 1.0
)
syntaxClassesColor = NSColor.colorWithHue_saturation_brightness_alpha_(
    0.25, 0.5, 1.0, 1.0
)
syntaxPunctuationColor = NSColor.colorWithHue_saturation_brightness_alpha_(
    0.55, 1.0, 0.8, 1.0
)
caretColor = NSColor.redColor()


buttonStyle = NSTexturedRoundedBezelStyle
__METHOD__ = DRAWBACKGROUND  # DRAWFOREGROUND


# ==============================
# S Y N T A X   K E Y W O R D S
# ==============================

keywordsWithSpace = [
    "def ",
    "class ",
    "for ",
    "while ",
    "if ",
    "elif ",
    "else ",
    "finally ",
    "from ",
    "print ",
    "except ",
    "global ",
    "return ",
    "as ",
    "print ",
    "import ",  ## ! KEEP u"import " at end of this list, otherwise some Keywords wont work !
]  # Space to the right.

keywordsWithSpaces = [
    " in ",
    " and ",
    " not ",
    " is ",
    " or ",
    " raise ",
    " yield ",
]  # Space to both sides.

keywordsWithoutSpace = [
    "try:",
    "except:",
    "finally:",
    "else:",
    r"\%s",
]

constants = [
    "True",
    "False",
    "None",
    "self",
    "break",
    "pass",
    "return",
    "continue",
]

commentTrigger = "#"
glyphsAppInternals = [
    "Glyphs",
    "GlyphsApp",
    "Font",
    "Layer",
]

glyphsAppConstants = [
    "MOVE",
    "LINE",
    "CURVE",
    "OFFCURVE",
    "QCURVE",
    "HOBBYCURVE",
    "GSMOVE",
    "GSLINE",
    "GSCURVE",
    "GSQCURVE",
    "GSOFFCURVE",
    "GSHOBBYCURVE",
    "GSSHARP",
    "GSSMOOTH",
    "FILL",
    "FILLCOLOR",
    "FILLPATTERNANGLE",
    "FILLPATTERNBLENDMODE",
    "FILLPATTERNFILE",
    "FILLPATTERNOFFSET",
    "FILLPATTERNSCALE",
    "STROKECOLOR",
    "STROKELINECAPEND",
    "STROKELINECAPSTART",
    "STROKELINEJOIN",
    "STROKEPOSITION",
    "STROKEWIDTH",
    "GRADIENT",
    "SHADOW",
    "INNERSHADOW",
    "MASK",
    "INSTANCETYPESINGLE",
    "INSTANCETYPEVARIABLE",
    "TAG",
    "TOPGHOST",
    "STEM",
    "BOTTOMGHOST",
    "FLEX",
    "TTSNAP",
    "TTSTEM",
    "TTSHIFT",
    "TTINTERPOLATE",
    "TTDIAGONAL",
    "TTDELTA",
    "CORNER",
    "CAP",
    "TTDONTROUND",
    "TTROUND",
    "TTROUNDUP",
    "TTROUNDDOWN",
    "TRIPLE",
    "TTANCHOR",
    "TTALIGN",  # backwards compatibilty
    "TEXT",
    "ARROW",
    "CIRCLE",
    "PLUS",
    "MINUS",
    "LTR",
    "RTL",
    "LTRTTB",
    "RTLTTB",
    "GSTopLeft",
    "GSTopCenter",
    "GSTopRight",
    "GSCenterLeft",
    "GSCenterCenter",
    "GSCenterRight",
    "GSBottomLeft",
    "GSBottomCenter",
    "GSBottomRight",
]

glyphsAppCallbacks = [
    "DRAWFOREGROUND",
    "DRAWBACKGROUND",
    "DRAWINACTIVE",
    "DOCUMENTOPENED",
    "DOCUMENTACTIVATED",
    "DOCUMENTWASSAVED",
    "DOCUMENTEXPORTED",
    "DOCUMENTCLOSED",
    "DOCUMENTWILLCLOSE",
    "DOCUMENTDIDCLOSE",
    "TABDIDOPEN",
    "TABWILLCLOSE",
    "UPDATEINTERFACE",
    "MOUSEMOVED",
    "MOUSEDRAGGED",
    "MOUSEDOWN",
    "MOUSEUP",
    "CONTEXTMENUCALLBACK",
]

# ============================
# L I N E   N U M B E R S
# ============================


lineNumberColor = editorTextColor.colorWithAlphaComponent_(0.35)


class LineNumberRulerView(NSRulerView):

    def isFlipped(self):
        return True

    @objc.python_method
    def setup(self, textView):
        self._textView = textView
        try:
            self._font = NSFont.monospacedSystemFontOfSize_weight_(
                codeEditorFontSize - 2, NSFontWeightRegular
            )
        except Exception:
            self._font = NSFont.userFixedPitchFontOfSize_(codeEditorFontSize - 2)
        self._attrs = {
            NSForegroundColorAttributeName: lineNumberColor,
            NSFontAttributeName: self._font,
        }
        self.setRuleThickness_(36)
        scrollView = textView.enclosingScrollView()
        scrollView.contentView().setPostsBoundsChangedNotifications_(True)
        nc = NSNotificationCenter.defaultCenter()
        nc.addObserver_selector_name_object_(
            self,
            "refresh:",
            "NSTextStorageDidProcessEditingNotification",
            textView.textStorage(),
        )
        nc.addObserver_selector_name_object_(
            self,
            "refresh:",
            "NSViewBoundsDidChangeNotification",
            scrollView.contentView(),
        )

    def refresh_(self, notification):
        self._updateThickness()
        self.setNeedsDisplay_(True)

    @objc.python_method
    def _updateThickness(self):
        text = self._textView.string()
        lineCount = text.componentsSeparatedByString_("\n").count()
        digits = max(2, len(str(lineCount)))
        newThickness = digits * 8 + 20
        if newThickness != self.ruleThickness():
            self.setRuleThickness_(newThickness)

    @objc.python_method
    def cleanup(self):
        NSNotificationCenter.defaultCenter().removeObserver_(self)

    def drawHashMarksAndLabelsInRect_(self, rect):
        editorBGColor.set()
        NSRectFill(rect)

        textView = self._textView
        lm = textView.layoutManager()
        text = textView.string()
        textLen = text.length()
        insetH = textView.textContainerInset().height
        thickness = self.ruleThickness()
        scrollY = self.scrollView().contentView().bounds().origin.y

        if textLen == 0:
            label = NSAttributedString.alloc().initWithString_attributes_(
                "1", self._attrs
            )
            labelSize = label.size()
            label.drawAtPoint_((thickness - labelSize.width - 8, insetH - scrollY))
            return

        lineNum = 1
        idx = 0

        while idx < textLen:
            lineRange = text.lineRangeForRange_(NSMakeRange(idx, 0))
            result = lm.glyphRangeForCharacterRange_actualCharacterRange_(
                lineRange, None
            )
            glyphRange = result[0] if isinstance(result, tuple) else result
            result = lm.lineFragmentRectForGlyphAtIndex_effectiveRange_(
                glyphRange.location, None
            )
            lineRect = result[0] if isinstance(result, tuple) else result

            y = lineRect.origin.y + insetH - scrollY
            h = lineRect.size.height

            if y > rect.origin.y + rect.size.height:
                break

            if y + h >= rect.origin.y:
                label = NSAttributedString.alloc().initWithString_attributes_(
                    str(lineNum), self._attrs
                )
                labelSize = label.size()
                label.drawAtPoint_(
                    (
                        thickness - labelSize.width - 8,
                        y + (h - labelSize.height) / 2,
                    )
                )

            nextIdx = lineRange.location + lineRange.length
            if nextIdx <= idx:
                break
            idx = nextIdx
            lineNum += 1

        # Extra line after trailing newline
        extraRect = lm.extraLineFragmentRect()
        if extraRect.size.height > 0:
            y = extraRect.origin.y + insetH - scrollY
            h = extraRect.size.height
            label = NSAttributedString.alloc().initWithString_attributes_(
                str(lineNum), self._attrs
            )
            labelSize = label.size()
            label.drawAtPoint_(
                (
                    thickness - labelSize.width - 8,
                    y + (h - labelSize.height) / 2,
                )
            )


# ========
# M A I N
# ========


class CodeEditor(NSResponder):

    def init(self):

        ## Subclass / Monkey Patch:
        ## Avoid NSPanel close on ESC key:
        def __cancel_(self, value):
            pass  # print "ESC Key not closing the panel anymore :)"

        FloatingWindow.cancel_ = __cancel_
        ## -------------------------

        # Inits
        # ------
        self.vID = "com.markfromberg.%s" % name  # vendorID
        self.toggle = False
        self.liveCodeMode = 0
        self.openFilePath = None
        self.w = FloatingWindow(
            (800, 600),
            minSize=(400, 400),
            title="%s %s" % (name, version),
            autosaveName="%s.mainwindow" % self.vID,
        )  ## restore window position
        nsWindow = self.w.getNSWindow()
        # nsWindow.setLevel_(NSFloatingWindowLevel)
        # nsWindow.setCollectionBehavior_(NSWindowCollectionBehaviorManaged)
        nsWindow.setStyleMask_(
            NSTitledWindowMask
            | NSClosableWindowMask
            | NSMiniaturizableWindowMask
            | NSResizableWindowMask
        )
        nsWindow.setAppearance_(
            NSAppearance.appearanceNamed_(NSAppearanceNameVibrantDark)
        )
        nsWindow.setTitlebarAppearsTransparent_(True)
        nsWindow.setBackgroundColor_(editorBGColor)

        # textView
        # ---------
        self.w.textEditor = TextEditor(
            (0, 0, -0, -40),
            Glyphs.defaults["SkedgeCode"],
            callback=self.doLiveCodeMode_,
        )
        self.textView = self.w.textEditor._textView

        self.textView.setTextColor_(editorTextColor)
        self.textView.setBackgroundColor_(editorBGColor)
        self.textView.setInsertionPointColor_(caretColor)
        self.textView.setRichText_(True)
        self.w.textEditor._nsObject.setBorderType_(NSNoBorder)
        self.texteEditorScrollView = self.w.textEditor._nsObject
        textSelection = {}
        textSelection[NSBackgroundColorAttributeName] = selectionBGColor
        # textSelection[NSForegroundColorAttributeName] = selectionFGColor
        self.textView.setSelectedTextAttributes_(textSelection)
        self.textView.setUsesFindBar_(True)
        self.textView.setTextContainerInset_(((20, 20)))
        self.textView.turnOffLigatures_(True)

        self.textView.setAutomaticDashSubstitutionEnabled_(False)
        self.textView.setAutomaticDataDetectionEnabled_(False)
        self.textView.setAutomaticLanguageIdentificationEnabled_(False)
        self.textView.setAutomaticLinkDetectionEnabled_(False)
        self.textView.setAutomaticQuoteSubstitutionEnabled_(False)
        self.textView.setAutomaticSpellingCorrectionEnabled_(False)
        self.textView.setAutomaticTextReplacementEnabled_(False)
        self.textView.setSmartInsertDeleteEnabled_(False)

        self.textView.setMenu_(None)

        # Line numbers
        scrollView = self.w.textEditor._nsObject
        scrollView.setHasVerticalRuler_(True)
        self._lineNumberView = (
            LineNumberRulerView.alloc().initWithScrollView_orientation_(
                scrollView, 1  # NSVerticalRuler
            )
        )
        self._lineNumberView.setup(self.textView)
        scrollView.setVerticalRulerView_(self._lineNumberView)
        scrollView.setRulersVisible_(True)

        # ta = self.textView.typingAttributes().mutableCopy()
        # ps = NSMutableParagraphStyle.alloc().init()
        # ps.setLineSpacing_(30.0)
        # ps.setMinimumLineHeight_(30.0)
        # ps.setMaximumLineHeight_(30.0)
        # ps.setLineHeightMultiple_(3.0)
        # ta.setObject_forKey_(ps, NSParagraphStyleAttributeName)
        ##self.textView.setDefaultParagraphStyle_(ps)
        # print(self.textView.defaultParagraphStyle())

        # Buttons
        # --------
        self.w.liveCode = CheckBox((10, -32, 80, 22), "Live", value=True)
        self.w.runButton = Button(
            (80 + 10, -32, -150 - 10, 22), "Run ⌘R", callback=self.run_
        )
        self.w.runButton._nsObject.setBezelStyle_(buttonStyle)
        self.w.runButton.bind("r", ["command"])
        self.w.resetButton = Button(
            (-150 + 10, -32, -15, 22), "Reset ⌘K", callback=self.reset_
        )
        self.w.resetButton._nsObject.setBezelStyle_(buttonStyle)
        self.w.resetButton.bind("k", ["command"])

        self.w.bind("close", callback=self.onClose_)
        self.w.open()

        # Enable the saveDocument_ & openDocument_ be
        # triggered by the menu or keyboard shortcuts
        # -----------------------------------------------
        nextResponder = self.w._window.nextResponder()
        self.w._window.setNextResponder_(self)
        self.setNextResponder_(nextResponder)

        self.code = None
        self.w.makeKey()
        self.addCallback()
        self.performClick()  # First Run after opening a file, must be after addCallback()

    def saveDocument_(self, sender):
        # print "saveDocument_"
        ### Maybe store the file name and just write the file on the second run
        self.saveFile_(sender)

    def openDocument_(self, sender):
        # print "openDocument_"
        self.openFile_(sender)

    # ==================
    # C A L L B A C K S
    # ==================

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
                namespace = dict(globals())
                namespace["layer"] = layer
                namespace["info"] = info
                exec(self.code, namespace)
                # Glyphs.clearLog() # Maybe better not.
            except:
                ## This is the actual Code Log
                ## TODO: pass into own log window.
                self.skedgeLog()  # print traceback.format_exc()

    def run_(self, sender):
        self.code = self.w.textEditor.get()
        self.syntaxHighlighter()
        Glyphs.redraw()

    def reset_(self, sender):
        self.code = None
        Glyphs.redraw()

    def onClose_(self, sender):
        self._lineNumberView.cleanup()
        self.removeCallback()

    def doLiveCodeMode_(self, sender):
        self.liveCodeMode = self.w.liveCode.get()
        if self.liveCodeMode == 1:
            try:
                self.run_(sender)
            except:
                self.skedgeLog()  # print traceback.format_exc()
        Glyphs.defaults["SkedgeCode"] = self.textView.string()

    def skedgeLog(self):
        # Glyphs.clearLog() # Maybe better not.
        print(traceback.format_exc())

    def performClick(self):
        self.w.runButton.getNSButton().performClick_(self.w.runButton.getNSButton())

    def syntaxHighlighter(self):

        # -------
        # Helper
        # -------

        def setFontInRange(range):
            try:
                # try:
                # 	font = NSFont.fontWithName_size_("Neutronic Mono v0.2.3 Normal", codeEditorFontSize)
                # except:
                # 	font = NSFont.monospacedSystemFontOfSize_weight_(codeEditorFontSize, NSFontWeightRegular)
                font = NSFont.monospacedSystemFontOfSize_weight_(
                    codeEditorFontSize, NSFontWeightRegular
                )
            except:
                font = NSFont.userFixedPitchFontOfSize_(codeEditorFontSize)
            self.textView.setFont_range_(font, NSMakeRange(range[0], range[1]))

        def colorString(
            searchItem,
            line,
            color,
            lenTillEOL=0,
            checkForPreceedingLetter=False,
            trim=False,
            background=False,
        ):
            try:
                for m in re.finditer(searchItem, line):
                    startInLine = m.start()
                    previousChar = line[m.start() - 1]
                    thisLineStart, foundLength = startInLine, m.end() - startInLine
                    try:
                        if checkForPreceedingLetter and previousChar.isalpha():
                            pass
                        else:
                            s, e = (
                                thisLineStart + self.charCount + 1,
                                foundLength + lenTillEOL,
                            )
                            if trim:
                                e -= 1
                            if background:
                                self.textView.attributedString().addAttribute_value_range_(
                                    NSBackgroundColorAttributeName,
                                    color,
                                    NSMakeRange(s, e),
                                )
                            else:
                                self.textView.setTextColor_range_(
                                    color, NSMakeRange(s, e)
                                )
                        if color == syntaxCommentTextColor:  # Set Italic for comments:
                            setFontInRange((s, e))
                    except:
                        pass
            except:
                pass  # print traceback.format_exc()

        # ---------------------------------------------------
        # Main
        # ---------------------------------------------------
        commentRE = "#[^\n]*"
        comments = []
        try:
            # Reset Text Attributes from copied text (Thanks to Georg Seifert @schriftgestalt):
            textStorage = self.textView.textStorage()
            textStorage.setAttributes_range_({}, NSMakeRange(0, textStorage.length()))

            # Basic Reset:
            self.textView.setTextColor_range_(
                editorTextColor, NSMakeRange(0, len(self.code))
            )  # Reset first
            setFontInRange((0, len(self.code)))  # Reset first

            ranges = {}

            self.charCount = 0
            for li, line in enumerate(self.code.splitlines()):

                if li > 0:
                    self.charCount += 1  # LineBreak maybe?
                else:
                    self.charCount -= 1

                # ALL THE REST
                # -------------
                # else:
                colorString(
                    r"(?<![a-zA-Z_])\d+",
                    line,
                    syntaxDigitsColor,
                    checkForPreceedingLetter=True,
                )  # digits, if not preceeded by letter or underscore
                colorString(r"[\*\+\-\/\=\!\>\<\%\&]", line, syntaxKeywordsColor)
                colorString(r"[\(\)\{\}\[\]]", line, syntaxSecondTextColor)
                colorString(r"[\;\:\,]", line, syntaxPunctuationColor)
                colorString(r"\.", line, syntaxSecondTextColor)

                # Method Calls
                # not quite: r"\.(.*?)\("
                # look around https://stackoverflow.com/questions/3926451/how-to-match-but-not-capture-part-of-a-regex
                # colorString(r"(?<=\.)(.*?)(?=\()", line, syntaxMethodColor) # Between . and (
                # colorString(r"(?<=\.|\s)([a-zA-Z+_]*?)(?=\(|\))", line, syntaxMethodColor)  # any of these a-zA-Z_ between `.` or `space` and `(` or `)`, any amount of `_` in name
                colorString(
                    r"(?<=\.|\s)([a-zA-Z0-9_]*?)(?=\()", line, syntaxMethodColor
                )  # any of these a-zA-Z_ between `.` or `space` and `(` or `)`, any amount of `_` in name
                #

                for kWord in keywordsWithSpace:
                    colorString(kWord, line, syntaxKeywordsColor)
                for kWord in keywordsWithoutSpace:
                    colorString(kWord, line, syntaxKeywordsColor, trim=True)
                for kWord in keywordsWithSpaces:
                    colorString(kWord, line, syntaxKeywordsColor)
                for kWord in constants:
                    colorString(kWord, line, syntaxConstantsColor)

                # COMMENTS
                # ---------
                # from `#` up to newLine
                for m in re.finditer(commentRE, line):
                    try:
                        s, e = m.start(), m.end()
                        mm = m.group()
                        comments.append(
                            NSMakeRange(s + self.charCount + 1, e - s)
                        )  # instead of appending mm, use the range directly
                    except:
                        pass

                # colorString(r"(?<=\")(.*?)(?=\")", line, syntaxStringBGColor, background=True)  # strings between " ... " or ' ... ' excluding quotes
                colorString(
                    r"(\"|\')(.*?)(\"|\')", line, syntaxStringBGColor, background=True
                )  # strings between " ... " or ' ... ' including quotes. Nicer than excluding quotes
                colorString(
                    r"(\"|\')(.*?)(\"|\')", line, syntaxStringFGColor
                )  # same, but foreground

                # AppKit Stuff
                colorString(
                    r"(?<![a-zA-Z])(?=NS)(.*?)\.", line, syntaxClassesColor, trim=True
                )  # e.g NSColor (only if followed by . and if not preceeded by a letter)
                # GlyphsApp
                colorString(
                    r"(?<![a-zA-Z])(?=GS)(.*?)\.", line, syntaxClassesColor, trim=True
                )  # e.g GSFont (only if followed by . and if not preceeded by a letter) # (?=GS)(.*?)\.

                for glyphsAppInternal in glyphsAppInternals:
                    colorString(
                        r"(?<![a-zA-Z])%s(?![a-zA-Z])" % glyphsAppInternal,
                        line,
                        syntaxClassesColor,
                    )  # explicit words, not predceeded and followed by any letter
                for glyphsAppConstant in glyphsAppConstants:
                    colorString(
                        r"(?<![a-zA-Z])%s(?![a-zA-Z])" % glyphsAppConstant,
                        line,
                        syntaxClassesColor,
                    )  # explicit words, not predceeded and followed by any letter
                for glyphsAppCallback in glyphsAppCallbacks:
                    colorString(
                        r"(?<![a-zA-Z])%s(?![a-zA-Z])" % glyphsAppCallback,
                        line,
                        syntaxClassesColor,
                    )  # explicit words, not predceeded and followed by any letter

                self.charCount += len(
                    line
                )  # Do this AFTER Applying the range. We count the Lines UP to the currently checked one and add this to the found start

            # BLOCK COMMENTS
            # ---------------
            # Now checking the whole self.code
            #
            # BUG: Not working with line breaks yet.
            # `re.compile(searchstring, re.MULTILINE)` not figured out.
            try:
                BCTrigger = "'''"
                foundBC = ""
                try:
                    result = re.search("'''(.*)'''", self.code)
                    foundBC = "%s%s%s" % (BCTrigger, result.group(1), BCTrigger)
                except:
                    result = re.search("'''\n(.*)\n'''", self.code)
                    foundBC = "%s\n%s\n%s" % (BCTrigger, result.group(1), BCTrigger)
                if len(foundBC) > 0:
                    for m in re.finditer(
                        re.escape(foundBC), self.code
                    ):  # re.escape() to make special chars work (e.g. [] () * + ...)
                        bs, be = m.start(), len(foundBC)
                        self.textView.setTextColor_range_(
                            syntaxCommentTextColor, NSMakeRange(bs, be)
                        )
                        setFontInRange((bs, be))
            except:
                pass  # print traceback.format_exc()

        except:
            self.skedgeLog()  # print traceback.format_exc()
            # console.log(traceback.format_exc())

        for comment in comments:
            # range = self.textView.string().rangeOfString_(comment) # could be slower, so we use the range isntead of the string
            try:
                self.textView.setTextColor_range_(syntaxCommentTextColor, comment)
            except:
                pass

    # ======================
    # O P E N   &   S A V E
    # ======================

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
                    self.w.setTitle(
                        "%s %s     [%s]" % (name, version, filePath.lastPathComponent())
                    )
                except:
                    pass
            except:
                self.skedgeLog()

    def saveFile_(self, sender):
        filePath = GetSaveFile(
            message="Save your Code as a .py file.",
            ProposedFileName="%s - " % name,
            filetypes=["py"],
        )
        if filePath is not None:
            content = self.w.textEditor.get()
            try:
                with io.open(filePath, "w+") as f:
                    f.write(content)
            except:
                Message("Could not save file.", "")

    # ==========
    # P R I N T
    # ==========

    def printDocument_(self, sender):
        self.texteEditorScrollView.print_(True)

    def print_(self, sender):
        NSPrintOperation.printOperationWithView_(self).runOperation()
