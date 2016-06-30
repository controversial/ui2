# Testing libraries
import unittest
try:
    import coverage
    has_coverage = True
except ImportError:
    has_coverage = False

# Modules used in testing
import ui
import ui2
import ui2.ui_io

import os

LOCALDIR = os.path.abspath(os.path.dirname(__file__))

class TestDump(unittest.TestCase):
    """ Test ui2.dump_view to ensure the preservation of all attributes """
    # SETUP
    path = "test.pyui"

    def tearDown(self):
        """ Called after each test to remove the pyui file created """
        if os.path.exists(self.path):
            os.remove(self.path)
    
    # MAIN TESTS
    
    def test_Generic(self):
        """ Test all generic attributes of any ui.View class """
        a = ui.View()
        # Store attributes
        a.background_color = "#ff00ff"
        # Encode + decode
        b = ui._view_from_dict(ui2.ui_io._view_to_dict(a), globals(), locals())
        # Check that type and attributes were preserved
        self.assertIsInstance(b, type(a))
        self.assertEqual(a.background_color, b.background_color)
    
    def test_Button(self):
        a = ui.Button()
        # Store attributes
        a.title = "Hey, it's a thing!"
        # Encode + decode
        b = ui._view_from_dict(ui2.ui_io._view_to_dict(a), globals(), locals())
        # Check that type and attributes were preserved
        self.assertIsInstance(b, type(a))
        self.assertEqual(a.title, b.title)

if __name__ == "__main__":
    if has_coverage:
        cov = coverage.Coverage(source=["ui2"])
        cov.start()

    unittest.main(exit=False)

    if has_coverage:
        print("\n")
        cov.stop()
        cov.report()
    else:
        print("Install the 'coverage' module with StaSh to see more detailed "
              "reports!")

