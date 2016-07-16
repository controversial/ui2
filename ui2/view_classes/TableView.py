"""A high-level wrapper around the whole ui.TableView system."""

import ui
import collections


class Cell():
    """A single cell in a ui.TableView.

    This class "subclasses" ui.TableViewCell by wrapping it.
    """
    def __init__(self):
        self._cell = cell

    @property
    def accessory_type(self):
        return self._cell.accessory_type

    @accessory_type.setter
    def accessory_type(self, value):
        self._cell.accessory_type = value

    @property
    def content_view(self):
        return self._cell.content_view

    @property
    def detail_text_label(self):
        return self._cell.detail_text_label

    @property
    def image_view(self):
        return self._cell.image_view

    @property
    def selectable(self):
        return self._cell.selectable

    @selectable.setter
    def selectable(self, value):
        self._cell.selectable = value

    @property
    def selected_background_view(self):
        return self._cell.selected_background_view

    @selected_background_view.setter
    def selected_background_view(self, value):
        self._cell.selected_background_view = value

    @property
    def text_label(self):
        return self._cell.text_label


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
