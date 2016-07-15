# ui2
Builds on Pythonista's UI module to provide extra functionality

## Features
Some of the most notable features of `ui2` are as follows:
- Transitioning between views
- Progress bars, which can take any shape representable with a `ui.Path`, including lines, circles, and rectangles
- An entirely new system for delays. This introduces a new system for tracking delays with IDs, and allows for multiple "delay managers" to make things less global.
- Classes for controlling animation, which include support for different easings, and chaining several animations to run on sequence.
- Functions for scaling and stretching `ui.Path` objects, as well as a convenience `ui2.PathView` class which displays a path auch that as the `PathView` changes size, it intelligently stretches its path to match.

`ui2` includes a `demo.py` script which makes it easy to view and run examples for each major feature of the module.

Lastly, `ui2` is expanding fast! Check back frequently for new features.

## Design goals
`ui2` aims to make it as easy as possible to swap out `ui` for `ui2` and begin adding features. It follows that one of the aims of `ui2` is to maintain compatibility with `ui`, so that switching to `ui2` won't break your existing code.