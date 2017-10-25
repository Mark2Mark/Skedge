# Skedge

*This is a plugin for the [Glyphs font editor](http://glyphsapp.com/).*  

Skedge enables you to draw any graphics via python code live into the view of an Edit Tab in Glyphs.
As the name implies, it aims to help you sketching out ideas.
You will get immediate feedback of your code, which isn’t the case if you develop a reporter Plugin. Therefore you would have to restart Glyphs for each and every change you make just to see those changes happen. Not anymore!

### How to use

Just open `Skedge` from the Window menu. It will present you a super simple sample code to begin with.

You find a lot of help at the [Glyphs Documentation](https://docu.glyphsapp.com/) *Glyphs Documentation*
as well as at the [Glyphs Devolper Kit (SDK)](https://github.com/schriftgestalt/GlyphsSDK) *Glyphs Devolper Kit (SDK)*

### Examples

- 

##### Known Issues

- Some people report a crash caused by scrolling in the Code Editor. I cannot reproduce yet, so I’ll need Console Logs.
- Some Plugins which add a DRAWBACKGROUND callback could interfere with this plugin and hence either or both fail to operate.
- Syntax Highlighting is yet very rudimentary. But waaay better than none.

##### TODO

- Display change of file in Window Title (Completeley different file handling).
- Sophisticated syntax highlighting.

##### Pull Requests

Feel free to comment or pull requests for any improvements.

##### License

Copyright 2017 [Mark Frömberg](http://www.markfromberg.com/) *@Mark2Mark*

Made possible with the GlyphsSDK by Georg Seifert (@schriftgestalt) and Rainer Erich Scheichelbauer (@mekkablue).
Thanks to Georg Seifert (@schriftgestalt) for streamlining and helping to make this tool still work after a lot of recent API cahnges!

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

See the License file included in this repository for further details.
