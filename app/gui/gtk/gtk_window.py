import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MainWindow(Gtk.Window):

    def __init__(self, title, width=400, height=300, notebook=None):
        super().__init__()
        self.set_title(title)
        self.set_default_size(width, height)
        self.set_position(Gtk.WindowPosition.CENTER)
        if notebook is not None:
            self.add(notebook)
