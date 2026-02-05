<p align="center">
  <img src="https://github.com/Mark2Mark/Skedge/blob/master/Images/Skedge%201.3.0.png?raw=true" alt="Skedge" height="800">
</p>

<h1 align="center">Skedge</h1>

<p align="center">
  <strong>A live-coding playground for GlyphsApp reporter plugins</strong>
</p>

<p align="center">
  <a href="https://ko-fi.com/M4M580HG" target="_blank"><img height="36" src="https://az743702.vo.msecnd.net/cdn/kofi1.png?v=0" alt="Buy Me a Coffee at ko-fi.com" /></a>
</p>

---

## Why Skedge?

Building a reporter plugin[^1] for Glyphs usually means wrestling with boilerplate, file structures, and constant app restarts. Skedge strips all of that away.

- **Sketch ideas instantly** — no plugin scaffolding, no intimidating developer kit
- **See results in real time** — no restarting Glyphs after every change
- **Focus on the drawing code** — only write what actually goes into the drawing callback
- **Transfer to a real plugin** when you're ready — your Skedge code drops right in

[^1]: A plugin that draws into the active Edit Tab.

Whether you're a beginner exploring Python for type design or an experienced developer prototyping a new tool, Skedge gives you a fast, visual feedback loop.

## Live Example

<p align="center">
  <img src="https://raw.githubusercontent.com/Mark2Mark/Skedge/master/Images/Skedge%2003.gif" alt="Skedge live demo">
</p>

## Getting Started

Install Skedge via the **Glyphs Plugin Manager**, then open it from the **Window** menu.

1. Skedge launches with sample code to help you get oriented.
2. Replace the sample with your own drawing code — only the code for your reporter's drawing method is needed.
3. Results appear immediately in the Edit View.
4. Toggle **Live** for real-time preview, or click **Run** (<kbd>Cmd</kbd>+<kbd>R</kbd>) to execute manually.

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| <kbd>Cmd</kbd>+<kbd>S</kbd> | Save code |
| <kbd>Cmd</kbd>+<kbd>O</kbd> | Open code |
| <kbd>Cmd</kbd>+<kbd>R</kbd> | Run code |
| <kbd>Cmd</kbd>+<kbd>K</kbd> | Clear drawing from Edit Tab |
| <kbd>Cmd</kbd>+<kbd>P</kbd> | Print or save as PDF |

### Tips

- Use **tabs** for indentation (spaces are not supported yet).
- All GlyphsApp Python objects and Cocoa UI classes are available — just import what you need, e.g. `from AppKit import NSColor, NSRect`.
- When you're done prototyping, paste your Skedge code directly into a reporter plugin's drawing method.

## Reset to Default Code

If something goes wrong, reset Skedge to its default state by running this in the **Macro Panel**:

```python
del(Glyphs.defaults["SkedgeCode"])
```

## Sample Code

Drop any of these snippets into Skedge to see them in action.

<details>
<summary><strong>01 — Draw Layer Bounds</strong></summary>

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

</details>

<details>
<summary><strong>02 — Filled Path with Red Outline &amp; Alternating Node Highlights</strong></summary>

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

</details>

<details>
<summary><strong>03 — Plumblines at Each Path's Centre</strong></summary>

```python
#################################################
# Draw plumblines at each path’s center (x and y)
#################################################
import traceback

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

</details>

<details>
<summary><strong>04 — Line at Half Cap Height</strong></summary>

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

</details>

## Resources

- [Glyphs Documentation](https://docu.glyphsapp.com/)
- [Glyphs Developer Kit (SDK)](https://github.com/schriftgestalt/GlyphsSDK)
- [Mark Frömberg's plugins](https://github.com/Mark2Mark/Glyphsapp-Plugins)
- [@mekkablue's plugins](https://github.com/mekkablue)

…and many others who generously share their work with the community.

## Important

> [!WARNING]
> Skedge is in beta. Please back up your files — no guarantee against data loss.

> [!WARNING]
> Be careful with transforms on `layer.bezierPath` — it addresses the real path. Make a `.copy()` of the layer first if you need to transform it. Reading data and drawing new objects from it is always safe.

## Contributing

Pull requests and feedback are welcome.

## License

Copyright 2017–2026 [Mark Frömberg](https://www.markfromberg.com/) *@Mark2Mark*

Made possible with the [Glyphs SDK](https://github.com/schriftgestalt/GlyphsSDK) by Georg Seifert ([@schriftgestalt](https://github.com/schriftgestalt)) and Rainer Erich Scheichelbauer ([@mekkablue](https://github.com/mekkablue)).
Thanks to Georg Seifert for streamlining and helping keep this tool working through recent API changes.

Licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0). See the included License file for details.
