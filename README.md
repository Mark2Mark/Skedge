<p align="center">
<a href='https://ko-fi.com/M4M580HG' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://az743702.vo.msecnd.net/cdn/kofi1.png?v=0' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>
</p>

# Skedge

<p align="center">
<img src="https://github.com/Mark2Mark/Skedge/blob/master/Images/Skedge%201.3.0.png?raw=true" alt="Skedge" height="800">
</p>

<!-- <a href="https://glyphsapp.com/"><img src="https://img.shields.io/badge/environment%20-GlyphsApp-brightgreen.svg"></a> <img src="https://img.shields.io/badge/type%20-Plugin-blue.svg"> <a href="http://ts-vanilla.readthedocs.io/en/latest/"> <img src="https://img.shields.io/badge/dependencies%20-Vanilla-lightgray.svg"></a> <a href="http://www.apache.org/licenses/LICENSE-2.0"> <img src="https://img.shields.io/badge/license%20-Apache 2.0-lightgray.svg"></a> -->

## What is it about?

- 👉 Have you ever wanted to **make a reporter[^1] plugin** for Glyphs, but the developer kit and the plugin file structure looks too intimidating to you?  
- 👉 Maybe you’re never willing to get your head around it and skip developing even though you have great ideas **you’d love to just sketch out**.  
- 👉 Or do you create plugins from time to time, but you’re annoyed that you have to restart Glyphs for every change? This can take a loooot of time, especially when the plugin is packed with formulas and algorithms that you need to get straight and test.
- 👉 You want to **see immediately which numbers and operators have which effect**. You want to **properly position your to be displayed objects**, maybe design them to provide an optimal user experience. Or **find the best colors** for your graphics.  
[^1]: A plugin which draws something to your active Edit Tab

#### 🎉 *Well, wait no longer! “Skedge” let’s you do exactly this!* 🎉

🤓 “Skedge” lets you focus on the essence of code you need in order to get your idea to the canvas.
- No GlyphsApp restart for every change you make.
- No extra code that you don’t understand the use for.  
- No file and folder overload.  

**“Skedge” is your playground,** your tool to explore how to use python to build incredible tools for your type design workflow.
Visual feedback in realtime is something that we designers always strive for.

**“Skedge” tears down the inhibition level** for beginners and is a companion on the way to learn coding. The sense of achievement will make you happy.
But this tool will help you anytime, no matter if you just started with python or if you’re an experienced developer already.

## How does it work?

In Skedge you just need to write the code that would go into any of the drawing callback methods of a reporter plugin.

> [!NOTE]
> The point of Skedge is to reduce all the overhead of a plugin and get to the barebone drawing procedure immediately.

## Live Example

<p align="center">
<img src="https://raw.githubusercontent.com/Mark2Mark/Skedge/master/Images/Skedge%2003.gif" alt="Skedge" height="">
</p>


## Getting Started with Skedge

If you haven't already, install Skedge using Glyphs Plugin Manager.

1. Open the "Skedge" plugin from the Window menu. It provides a simple sample code to help you get started quickly.
1. Now write your own code instead of the sample code. Only the code that will go into your Reporter plugin’s drawing method is required.
1. You will see the result in realtime in the GlyphsApp Edit View.
1. Save and open your code by using <kbd>Cmd+S</kbd> for save and <kbd>Cmd+O</kbd> for open.
1. Toggle the "Live" checkbox to preview changes in real-time. If not, click the "Run" button (or use <kbd>Cmd+R</kbd>) to execute your code.
1. Press <kbd>Cmd+K</kbd> to reset the drawing in your Edit Tab. The same effect occurs when you close the Skedge window.
1. Press <kbd>Cmd+P</kbd> to either print your code or save it as a PDF.
1. Python etiquette: Please use **tabs**. While Skedge currently doesn't support spaces, future updates might address this. For now, let's stick with tabs. Learn more about the great spaces vs tabs debate.
1. The code written in Skedge can be seamlessly transferred into an actual reporter plugin. Paste the Skedge code into your glyphsReporter’s drawing method.
1. Skedge provides access to all GlyphsApp Python objects and Cocoa UI objects. Import them explicitly in your code, for example, `from AppKit import NSColor, NSRect`.



## Reset to Default Code
In case something goes wrong and you want Skedge to launch again with the default code, rather than your last state, run this once in GlyphApp’s Macro Panel:
```py
del(Glyphs.defaults["SkedgeCode"])
```

## Help

You find **help** and **code examples** here:

👉 [Glyphs Documentation](https://docu.glyphsapp.com/)

👉 [Glyphs Developer Kit (SDK)](https://github.com/schriftgestalt/GlyphsSDK)

It’s also always possible to peek into public plugins:

👉 [my plugins](https://github.com/Mark2Mark/Glyphsapp-Plugins)

👉 [@mekkablue’s plugins](https://github.com/mekkablue)

and other people who are endlessly kind to share their skills with the world. :)

## Sample Codes

You can dump these snippets right into “Skedge” and they will (hopefully) just do what they claim to do:

### 01) Draw Layer Bounds
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

### 02) Draw filled Path with red outline and highlight every second Node
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

### 03) Draw plumblines at each path’s center (x and y)
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

### 04) Draw line @ half Cap Height
```python
#################################################
# Draw line @ half Cap Height
#################################################

from AppKit import NSColor, NSBezierPath
scale = Glyphs.font.currentTab.scale
layer = Glyphs.font.selectedLayers[0]
 
def myColor(a, b, c, d):
    c = NSColor.colorWithHue_saturation_brightness_alpha_(a, b, c, d)
    return c

def line(x1, y1, x2, y2, scale):
    myPath = NSBezierPath.alloc().init()
    myPath.moveTo_((x1, y1))
    myPath.lineTo_((x2, y2))
    NSColor.systemPurpleColor().colorWithAlphaComponent_(0.9).set()
    myPath.setLineWidth_(.5/scale)
    myPath.stroke()

capHeight = layer.associatedFontMaster().capHeight
width = layer.width

line(0, capHeight/2, width, capHeight/2, scale)
```

## Other Info

### Quirks

Due to how the plugin is designed, the code you write does not add global variables to the main python namespace as you might be used to. Hence, if you want to access a global variable inside of a method you define, either pass it into the method as a parameter, or add it with the `global` keyword inside the method. For example
```python
my_variable = 42

def my_method():
    global my_variable # <- See here.
    ...
```

### Important

> [!WARNING]
> Skedge is in beta. Please backup your files. No guarantee for destroying your files.

> [!WARNING]
> Take care when doing transforms or things alike on your layer's bezierPath. Since it will actually address the real path, be sure to make a `.copy()` of your layer before proceeding with those.
> If you’re just reading data and drawing new objects from that data, you should be fine.


## TODO

- [x] Autosave text edits. Reopening Skedge now remembers your code. Thanks Georg!
- [x] Fix encoding. Cannot save a file with words like »don’t«.
- [ ] Display change of file in Window Title (Completely different file handling).
- [ ] Work around some peculiar quirks that don’t need to be transferred to the actual reporterPlugin code later. (For instance calling some variables and functions `global`)
- [ ] Provide more code snippets.
- [x] Sophisticated syntax highlighting.
- [x] Add license to Repo.


## Pull Requests

Feel free to comment or pull requests for any improvements.

## License

Copyright 2017–2024 [Mark Frömberg](https://www.markfromberg.com/) *@Mark2Mark*

Made possible with the [Glyphs SDK](https://github.com/schriftgestalt/GlyphsSDK) by Georg Seifert [(@schriftgestalt)](https://github.com/schriftgestalt) and Rainer Erich Scheichelbauer [(@mekkablue)](https://github.com/mekkablue).
Thanks to Georg Seifert [(@schriftgestalt)](https://github.com/schriftgestalt) for streamlining and helping to make this tool still work after a lot of recent API changes!

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

See the License file included in this repository for further details.
