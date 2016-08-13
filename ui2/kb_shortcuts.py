"""An easy interface for adding keyboard shortcuts using decorators."""

import ctypes
import functools
import operator
import sys
import uuid

import objc_util


_app = objc_util.UIApplication.sharedApplication()
_controller = _app.keyWindow().rootViewController()


# Modifiers for special keys
_modifiers = {
    "shift": 1 << 17,
    "control": 1 << 18, "ctrl": 1 << 18,
    "option": 1 << 19, "alt": 1 << 19,
    "command": 1 << 20, "cmd": 1 << 20
}
# Input strings for special keys
_special_keys = {
    "up": "UIKeyInputUpArrow",
    "down": "UIKeyInputDownArrow",
    "left": "UIKeyInputLeftArrow",
    "right": "UIKeyInputRightArrow",
    "escape": "UIKeyInputEscape", "esc": "UIKeyInputEscape"
}


# HELPER METHODS

def _add_method(cls, func):
    # void, object, selector
    type_encoding = "v@:"
    sel_name = str(uuid.uuid4())
    sel = objc_util.sel(sel_name)
    class_ptr = objc_util.object_getClass(cls.ptr)

    # ----------------- Modified from objc_util.add_method ------------------ #
    parsed_types = objc_util.parse_types(type_encoding)
    restype, argtypes, _ = parsed_types
    imp = ctypes.CFUNCTYPE(restype, *argtypes)(func)
    objc_util.retain_global(imp)
    if isinstance(type_encoding, str):
       type_encoding = type_encoding.encode('ascii')
    objc_util.class_addMethod(class_ptr, sel, imp, type_encoding)
    # ----------------------------------------------------------------------- #
    return sel


def _tokenize_shortcut_string(shortcut):
    """Split a plaintext string representing a keyboard shortcut into each
    individual key in the shortcut.
    
    Valid separator characters are any combination of " ", "+", "-", and ",".
    """
    # Tokenize the string
    out = [shortcut]
    for separator in (" ", "-", "+", ","):
        new = []
        for piece in out:
            new.extend(piece.split(separator))
        out = new[:]
    tokens = [i.strip().lower() for i in out if i.strip().lower()]
    # Sort the tokens to place modifiers first
    return sorted(tokens, key=lambda tok: tok not in _modifiers)


def _validate_tokens(tokens):
    """Raise appropriate errors for ridiculous key commands.

    This will throw descriptive errors for keyboard keyboard shortcuts like:
        - Cmd + Shift + P + I
        - Ctrl + Elephant
        - Ctrl + Cmd + Shift
    """
    exceptions = tuple(_modifiers) + tuple(_special_keys)
    # Disallow muultiple non-modifier keys
    non_modifier_tokens = [tok for tok in tokens if tok not in _modifiers]
    if len(non_modifier_tokens) > 1:
        raise ValueError(
            "Only one non-modifier key is allowed in a shortcut"
        )
    if len(non_modifier_tokens) < 1:
        raise ValueError(
            "At least one non-modifier key is required in a shortcut"
        )
        
    # Disallow invalid key names
    for tok in tokens:
        if len(tok) > 1 and tok not in exceptions:
            raise ValueError(
                "{} is not a valid keyboard key".format(tok)
            )


# TRACKING OF COMMANDS
_registered_commands = {}


# REGISTERING


def _add_shortcut(shortcut, function, title=None):
    """Bind a function to a keyboard shortcut."""
    # Wrap function to accept and ignore arguments
    def wrapper(*args, **kwargs):
        function()

    # Parse shortcut
    tokens = _tokenize_shortcut_string(shortcut)
    _validate_tokens(tokens)
    modifiers = tokens[:-1]
    inp = tokens[-1]

    # Process components
    mod_bitmask = functools.reduce(
        operator.ior,
        [_modifiers[mod] for mod in modifiers],
        0
    )
    if inp in _special_keys:
        inp = _special_keys[inp]

    # Make the command
    sel = _add_method(_controller, wrapper)

    kc = objc_util.ObjCClass("UIKeyCommand")
    if title is not None:
        c = kc.keyCommandWithInput_modifierFlags_action_discoverabilityTitle_(
            inp,
            mod_bitmask,
            sel,
            title
        )
    else:
        c = kc.keyCommandWithInput_modifierFlags_action_(
            inp,
            mod_bitmask,
            sel
        )

    _registered_commands[frozenset(tokens)] = cp
    _controller.addKeyCommand_(c)


# MAIN INTERFACE


def bind(shortcut, title=None):
    """A decorator for binding keyboard shortcuts.

    Example:

    >>> @bind(Command + T)
    >>> def test_func():
    ...     print("Hello!")

    The shortcut definition syntax is designed to be flexible, so the following
    shortcut names are all equivalent:
        - Command + Shift + Escape
        - cmd-shift-esc
        - CMD SHIFT ESCAPE
        - command, shift, esc

    A few non-alphanumeric keys are supported with special names:
        - up
        - down
        - left
        - right
        - escape / esc
    """
    return functools.partial(_add_shortcut, shortcut, title=title)


if __name__ == "__main__":
    import console
    @bind("Command Shift Escape", "Say Hi")
    def hi():
        console.alert("Hello")
