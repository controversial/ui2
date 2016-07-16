"""A high-level wrapper around the whole ui.TableView system."""

import ui
import collections


class Cell():
    """A single cell in a ui.TableView.

    This class "subclasses" ui.TableViewCell by wrapping it.
    """
    pass


class Section(collections.MutableSet):
    """A section inside a TableView.
    
    This contains TableView cells.
    """
    def __init__(self, tableview):
        self.cells = set()
        self.tableview = tv

    def __contains__(self, item):
        return item in self.cells

    def __iter__(self):
        return iter(self.cells)

    def add(self, cell):
        self.cells.add(key)

    def discard(self, cell):
        self.cells.discard(cell)


class TableView(collections.Container):
    """A view to display a list of items in a single column."""
    def __init__(self):
        self.sections = [Section(self)]

    def __contains__(self, key):
        return key in self.sections
