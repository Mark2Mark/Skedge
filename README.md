# Skedge

This is a plugin for the [Glyphs font editor](http://glyphsapp.com/).


👉 Have you ever wanted to make a <a name="myfootnote1">reporter<sup>1</sup></a> plugin for Glyphs, but the developer kit and the plugin file structure looks too intimidating to you?
👉 Maybe you’re never willing to get your head around it and skip developing even though you have great ideas you’d love to just sketch out.
👉 Or do you create plugins from time to time, but you’re annoyed that you have to restart Glyphs for every change? This can take a loooot of time, especially when the plugin is packed with formulas and algorithms that you need to get straight. I suck at math, hence my approach ist often the trial-and-error.
👉 You want to see immediately which numbers and operators have which effect. You want to properly position your to be displayed components, maybe design them to provide an optimal user experience. Or choose the best colors for your graphics.

#### 🎉 *Well, wait no longer! “Skedge” let’s you do exactly this!* 🎉

🤓 “Skedge” lets you focus on the essence of code you need in order to get your idea to the canvas. No file and folder overload. No extra code that you don’t understand the use for. No Glyphs restart for every change you make.

“Skedge” is your playground, your tool to explore how to use python to build incredible anylitic tools for your workflow.
Visual feedback in realtime is something that we designers always strive for.

Hopefully “Skedge” will tear down the inhibition level for beginners and be a companion on the way to learn coding. The sense of achievement will make you happy.
But this tool will help you anytime, no matter if you just started with python or if you’re an experienced developer already.

...

<sup>[1)](#myfootnote1)</sup>
A plugin which draws something to your active Edit Tab

---
### Example

<p align="center"> 
<img src="https://github.com/Mark2Mark/Skedge/blob/master/Images/Skedge%201%20-%20Plumblines%20720.gif?raw=true" alt="Skedge" height="">
</p> 

---
### How to use

- (Install once from the Plugin Manager in Glyphs.)
- Open “Skedge” from the Window menu. It will present you a super simple sample code to begin with.
- You can open and/or save your code for later. Just hit `Cmd+S` or `Cmd+O`.
- Switch off the checkbox “Live”, if you don’t want to see changes in realtime.
- If so, be sure to hit the “Run” button (or `Cmd+R` ) to run your code.
- `Cmd+K` resets the drawing in your Edit Tab. The same happens when you close the window.
- `Cmd+P` lets you print your code or save it as PDF.
- Python etiquette: please use `TABS`! I’m not trying to force you into [that endless battle](https://stackoverflow.com/questions/119562/tabs-versus-spaces-in-python-programming), I just didn’t prepare the tool to deal with `SPACES` yet. Bear with me. BTW: f*** spaces! :D 

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
```python
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
```python
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
```python
#################################################
# Draw plumblines at each path’s center (x and y)
#################################################
import traceback

global layer, scale, drawLine ## Skedge-Hack

scale = Glyphs.font.currentTab.scale
layer = Glyphs.font.selectedLayers[0]
NSColor.blueColor().set()


def drawLine((x1, y1), (x2, y2)):
	strokeWidth = 1/scale
	path = NSBezierPath.bezierPath()
	path.moveToPoint_((x1, y1))
	path.lineToPoint_((x2, y2))
	path.setLineWidth_(strokeWidth)
	path.setLineDash_count_phase_((10, 2), 2, 0.0)
	path.stroke()

def DrawCross((x, y), (width, height)):
	### BOUNDS DIMENSIONS
	xRight = x + width
	yTop = y + height
	xCenter = (x + width/2)
	yCenter = (y + height/2)

	### LAYER/METRIC DIMENSIONS
	left = 0
	right = layer.width
	ascender = layer.glyphMetrics()[1]
	descender = layer.glyphMetrics()[3]

	drawLine((left, yCenter), (right, yCenter))
	drawLine((xCenter, descender), (xCenter, ascender))


for path in layer.paths:
	DrawCross(*[p for p in path.bounds])
```

---
##### Known Issues

- The code in “Skedge” can be almost exactly transferred into the e.g. `drawBackground()` method of your actual reporter plugin. Don’t forget to add the `self.` where needed, though. “Skedge” is build to not need it, so watch out for these.
- Some people report a crash caused by scrolling in the Code Editor. I cannot reproduce yet, so I’ll need Console Logs.
- Some Plugins which add a DRAWBACKGROUND callback could interfere with this plugin and hence either or both fail to operate.
- Syntax Highlighting is yet very rudimentary. But waaay better than none.

---
##### TODO

- Fix encoding. Cannot save a file with words like »don’t«.
- Display change of file in Window Title (Completeley different file handling).
- Skedge has some peculiar quirks that don’t need to be transferred to the actual reporterPlugin code later. (For instance calling some variables and functions `global`)
- Provide some code snippets.
- Sophisticated syntax highlighting.
- Add liscence to Repo.

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
