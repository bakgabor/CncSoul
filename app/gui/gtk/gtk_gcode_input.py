import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class GtkGCodeInput:

    def __init__(self):
        self._function = None
        self._window = None
        self._text = ''

    def _innit_window(self):
        builder = Gtk.Builder()
        builder.add_from_file("app/gui/glade/gcode_input.glade")
        self._window = builder.get_object("window")
        self.entry = builder.get_object("entry")
        handlers = {
            "press": self._press,
            "space": self._space,
            "back": self._back,
            "apply": self._apply,
            "entry_change": self._entry_change,
            "close": self._close
        }
        self._window.connect("destroy", Gtk.main_quit)
        builder.connect_signals(handlers)

    def show(self, function):
        self._innit_window()
        self._text = ''
        self.entry.set_text(self._text)
        self._function = function
        self._window.show_all()
        Gtk.main()

    def _apply(self, button):
        self._function(self._text)
        self._window.close()

    def _entry_change(self, entry):
        self._text = entry.get_text()

    def _space(self, button):
        self._text += " "
        self.entry.set_text(self._text)

    def _back(self, button):
        self._text = self._text[:len(self._text)-1]
        self.entry.set_text(self._text)

    def _press(self, button):
        self._text += button.get_label()
        self.entry.set_text(self._text)

    def _close(self, button):
        self._window.close()
