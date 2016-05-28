""" A module that builds on Pythonista's `ui` module """

# Dump ui into namespace so that `import ui2` can be used interchangably with
# `import ui`
from ui import *

# Load subpackages
from ui2 import shapes, ui_io
from ui2.NewPath import Path

