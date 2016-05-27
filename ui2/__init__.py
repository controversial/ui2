""" A module that builds on Pythonista's `ui` module """

# Load subpackages
import shapes
import ui_io

# Dump ui into namespace so that `import ui2` can be used interchangably with
# `import ui`
from ui import *
