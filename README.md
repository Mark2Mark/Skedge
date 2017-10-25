# Skedge

*This is a plugin for the [Glyphs font editor](http://glyphsapp.com/).*  

Skedge enables you to draw any graphics via python code live into the view of an Edit Tab in Glyphs.
As the name implies, it aims to help you sketching out ideas.
You will get *immediate feedback* of your code, which isn’t the case if you develop a reporter Plugin. Normally you’d have to restart Glyphs for each and every change to see changes happen. **Not anymore!**

### How to use

- Open `Skedge` from the Window menu. It will present you a super simple sample code to begin with.
- You can open and save your code for later. Just hit `Cmd+S` or `Cmd+O`.
- `Cmd+P`lets you print your code or save it as PDF.
- Switch the checkbox `Live` off, if you don’t want to see changes in realtime.
- If so, be sure to hit the `Run` button (or `Cmd+R`) to run your code.
- `Cmd+K` resets the drawing in your Edit Tab. The same happens when you close the window.

You find help and code examples at the [Glyphs Documentation](https://docu.glyphsapp.com/) as well as at the [Glyphs Devolper Kit (SDK)](https://github.com/schriftgestalt/GlyphsSDK). It’s also always possible to peek into public reporter plugins like [the ones from me](https://github.com/Mark2Mark/Glyphsapp-Plugins), or from [@mekkablue](https://github.com/mekkablue) and other people who are endlessly kind to share their skills with the world. :)

### Examples

<p align="center"> 
<img src="https://github.com/Mark2Mark/Skedge/blob/master/Images/Skedge%20Screenshot%201.png" alt="Skedge" height="400px">
</p> 

##### Known Issues

- Some people report a crash caused by scrolling in the Code Editor. I cannot reproduce yet, so I’ll need Console Logs.
- Some Plugins which add a DRAWBACKGROUND callback could interfere with this plugin and hence either or both fail to operate.
- Syntax Highlighting is yet very rudimentary. But waaay better than none.

##### TODO

- Display change of file in Window Title (Completeley different file handling).
- Skedge has some peculiar quirks that don’t need to be transferred to the actual reporterPlugin code later.
  - for instance calling some variables and functions `global`
- Provide some code snippets.
- Sophisticated syntax highlighting.

##### Pull Requests

Feel free to comment or pull requests for any improvements.

##### License

Copyright 2017 [Mark Frömberg](http://www.markfromberg.com/) *@Mark2Mark*

Made possible with the [Glyphs SDK](https://github.com/schriftgestalt/GlyphsSDK) by Georg Seifert [(@schriftgestalt)](https://github.com/schriftgestalt) and Rainer Erich Scheichelbauer [(@mekkablue)](https://github.com/mekkablue).
Thanks to Georg Seifert [(@schriftgestalt)](https://github.com/schriftgestalt) for streamlining and helping to make this tool still work after a lot of recent API cahnges!

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

See the License file included in this repository for further details.
