#Task List
A list of things I'd like to add, or things that are planned

# `ui.View` classes
- [x] `PathView` class for easily displaying shapes in a UI
  - Perhaps the existing polygon classes should inherit from this?
- [x] Progress bar
  - Should have styling options
- [x] NewPath class
  - [x] Basics
  - [x] Scaling and stretching the whole path - implemented via `Pathview`
- [ ] `AccordionView` class - See [this](http://materializecss.com/collapsible).
- [ ] **Side menu class**
  - This will wrap an existing view, adding a menu that can slide out from the side. There should be no visible change to the view.
  - It will have methods for showing and hiding, the menu, etc.
- [ ] Pull to refresh
- [x] `BlurView`
- [x] `MapView`


# New features for UIs
- [x] Transitions
  - [ ] Make transitions work on subviews
  - [x] Chain transitions together
- Animations
  - [x] iOS included easings
  - [ ] ~~Custom easings~~ (may be impossible)
  - [x] Chained animations to be executed in sequence
  - [ ] Repeated animations
- [x] New `ui2.delay` interface
  - [x] Decorators for delay:
    ```python
    @ui2.delayed(1)
    def hi():
        print("Hello")
    ```
  - [x] Named delays which can be cancelled individually
- [ ] Gestures
- [ ] Easy keyboard shortcuts

# Misc
- [ ] Create `.pyui` files from in-memory `ui.View` objects - Individual components can be created with their subviews, but not the top-level metadata.
- [ ] Test suite
