import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from app.event.event import Event


class GtkSetInput (Event):

    def __init__(self):
        super().__init__()
        self._events = {
            'destroy': []
        }
        self._move = None
        self._set = None
        self._text = ''

    def show(self, move, set):
        self._innit_window()
        self._text = ''
        self.entry.set_text(self._text)
        self._move = move
        self._set = set
        self.window.show_all()

        Gtk.main()

    def _innit_window(self):
        builder = Gtk.Builder()
        builder.add_from_file("app/gui/glade/set_input.glade")
        self.window = builder.get_object("window")
        self.window.connect('destroy', self._window_destroy)
        self.entry = builder.get_object("entry")
        handlers = {
            "press": self._press,
            "back": self._back,
            "move": self._move_to,
            "set": self._set_pos,
            "invert": self._invert,
            "close": self._close,
            "entry_change": self._entry_change
        }
        builder.connect_signals(handlers)

    def _window_destroy(self, window):
        Gtk.main_quit()
        self._run_event('destroy')
        return True

    def _move_to(self, button):
        self._move(self._text)
        self.window.close()

    def _close(self, button):
        self.window.close()

    def _set_pos(self, entry):
        self._set(self._text)
        self.window.close()

    def _invert(self, button):
        if self._text and self._text[0] == '-':
            self._text = self._text.replace(self._text[0], "", 1)
            self.entry.set_text(self._text)
            return
        self._text = '-' + self._text
        self.entry.set_text(self._text)

    def _back(self, button):
        self._text = self._text[:len(self._text)-1]
        self.entry.set_text(self._text)

    def _press(self, button):
        self._text += button.get_label()
        self.entry.set_text(self._text)

    def _entry_change(self, entry):
        self._text = entry.get_text()
