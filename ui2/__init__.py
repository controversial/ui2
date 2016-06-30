""" A module that builds on Pythonista's `ui` module """

# Dump ui into namespace so that `import ui2` can be used interchangably with
# `import ui`
from ui import *

# Load subpackages
from ui2.shapes import *
from ui2.ui_io import *
import ui2.path_helpers as pathutils
from ui2.NewPath import Path
