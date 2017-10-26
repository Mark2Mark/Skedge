# Skedge

This is a plugin for the [Glyphs font editor](http://glyphsapp.com/).


👉 Have you ever wanted to make a <a name="myfootnote1">reporter<sup>1</sup></a> plugin for Glyphs, but the developer kit and the plugin file structure looks too intimidating to you?
👉 Maybe you’re never willing to get your head around it and skip developing even though you have great ideas you’d love to just sketch out.
👉 Or do you create plugins from time to time, but you’re annoyed that you have to restart Glyphs for every change? This can take a loooot of time, especially when the plugin is packed with formulas and algorithms.
👉 You want to see immediately which numbers and operators have which effect. You want to properly position your to be displayed components, maybe design them to provide an optimal user experience. Or choose the best colors for your graphics.

🎉 *Well, wait no longer! “Skedge” let’s you do exactly this!* 🎉

🤓 “Skedge” lets you focus on the essence of code you need in order to get your idea to the canvas. No file and folder overload. No extra code that you don’t understand the use for. No Glyphs restart for every change you make.

“Skedge” is your playground, your tool to explore how to use python to build incredible anylitic tools for your workflow.
Visual feedback in realtime is something that we designers always strive for.

Hopefully “Skedge” will tear down the inhibition level for beginners and be a companion on the way to learn coding. The sense of achievement will make you happy.
But this tool will help you anytime, no matter if you just started with python or if you’re an experienced developer already.

...

<sup>[1)](#myfootnote1)</sup>
A plugin which draws something to your active Edit Tab

---
### How to use

- (Install once from the Plugin Manager in Glyphs.)
- Open “Skedge” from the Window menu. It will present you a super simple sample code to begin with.
- You can open and/or save your code for later. Just hit `Cmd+S` or `Cmd+O`.
- Switch off the checkbox “Live”, if you don’t want to see changes in realtime.
- If so, be sure to hit the “Run” button (or `Cmd+R` ) to run your code.
- `Cmd+K` resets the drawing in your Edit Tab. The same happens when you close the window.
- `Cmd+P` lets you print your code or save it as PDF.

---
### Help

You find **help** and **code examples** here:

👉 [Glyphs Documentation](https://docu.glyphsapp.com/)

👉 [Glyphs Devolper Kit (SDK)](https://github.com/schriftgestalt/GlyphsSDK)

It’s also always possible to peek into public plugins:

👉 [my plugins](https://github.com/Mark2Mark/Glyphsapp-Plugins)

👉 [@mekkablue’s plugins](https://github.com/mekkablue)

and other people who are endlessly kind to share their skills with the world. :)

---
### Sample Codes

You can dump these snippets right into “Skedge” and they will (hopefully) just do what they claim to do:

##### 01)
```
###################
# Draw Layer Bounds
###################
from AppKit import NSRectFill, NSRect, NSMakeRect

NSColor.yellowColor().set()

bounds = layer.bounds
x = bounds.origin.x
y = bounds.origin.y
width = bounds.size.width
height = bounds.size.height

rect = NSMakeRect(x, y, width, height)
NSRectFill(rect)
```

##### 02)
```
###################################################################
# Draw filled Path with red outline and highlight every second Node
###################################################################
import traceback

scale = Glyphs.font.currentTab.scale

def badge(x, y, size):
	myPath = NSBezierPath.alloc().init()
	myRect = NSRect( ( x-size/2, y-size/2 ), ( size, size ) )
	thisPath = NSBezierPath.bezierPathWithOvalInRect_( myRect )
	myPath.appendBezierPath_( thisPath )
	NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.5, .5, 0.5, .3 ).set()
	myPath.fill()

for path in layer.paths:
	NSColor.grayColor().colorWithAlphaComponent_(0.3).set()
	bp = path.bezierPath
	bp.fill()
	bp.setLineWidth_(5/scale)
	NSColor.redColor().set()	
	bp.stroke()
	for i, node in enumerate(path.nodes):
		if i % 2:
			badge(node.x, node.y, 20/scale )
```

##### 03)
```
#################################################
# Draw plumblines at each path’s center (x and y)
#################################################
import traceback

global layer, scale, drawLine ## Skedge-Hack

scale = Glyphs.font.currentTab.scale
layer = Glyphs.font.selectedLayers[0]
NSColor.redColor().set()

def BoundsRect(NSRect):
	x, y = NSRect[0]
	width, height = NSRect[1]
	return x, y, width, height

def drawLine(x1, y1, x2, y2):
	strokeWidth = 1/scale
	myPath = NSBezierPath.bezierPath()
	myPath.moveToPoint_((x1, y1))
	myPath.lineToPoint_((x2, y2))
	myPath.setLineWidth_(strokeWidth)
	myPath.setLineDash_count_phase_((2, 2), 2, 0.0)
	myPath.stroke()

def DrawCross(x, y, width, height):
	xHeight = layer.glyphMetrics()[4]

	### BOUNDS DIMENSIONS
	xCenter = (x + width/2)
	xRight = x + width
	yCenter = (y + height/2)
	yTop = y + height

	### LAYER/METRIC DIMENSIONS
	xLayerLeft = 0
	xLayerRight = layer.width
	yAscender = layer.glyphMetrics()[1]
	yDescender = layer.glyphMetrics()[3]

	drawLine( xLayerLeft, yCenter, xLayerRight, yCenter)
	drawLine( xCenter, yDescender, xCenter, yAscender )

for path in layer.paths:
	DrawCross(*BoundsRect(path.bounds))
```

---
### Examples

<p align="center"> 
<img src="https://github.com/Mark2Mark/Skedge/blob/master/Images/Skedge%20Screenshot%201.png" alt="Skedge" height="400px">
</p> 


---
##### Known Issues

- Some people report a crash caused by scrolling in the Code Editor. I cannot reproduce yet, so I’ll need Console Logs.
- Some Plugins which add a DRAWBACKGROUND callback could interfere with this plugin and hence either or both fail to operate.
- Syntax Highlighting is yet very rudimentary. But waaay better than none.

---
##### TODO

- Display change of file in Window Title (Completeley different file handling).
- Skedge has some peculiar quirks that don’t need to be transferred to the actual reporterPlugin code later. (For instance calling some variables and functions `global`)
- Provide some code snippets.
- Sophisticated syntax highlighting.

---
##### Pull Requests

Feel free to comment or pull requests for any improvements.

---
##### License

Copyright 2017 [Mark Frömberg](http://www.markfromberg.com/) *@Mark2Mark*

Made possible with the [Glyphs SDK](https://github.com/schriftgestalt/GlyphsSDK) by Georg Seifert [(@schriftgestalt)](https://github.com/schriftgestalt) and Rainer Erich Scheichelbauer [(@mekkablue)](https://github.com/mekkablue).
Thanks to Georg Seifert [(@schriftgestalt)](https://github.com/schriftgestalt) for streamlining and helping to make this tool still work after a lot of recent API cahnges!

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

See the License file included in this repository for further details.
