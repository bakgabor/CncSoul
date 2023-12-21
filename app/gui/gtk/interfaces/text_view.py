from gi.repository import GLib


class TextView:

    def __init__(self, gtk_text_view):
        self._gtk_text_view = gtk_text_view
        self._text_buffer = self._gtk_text_view.get_buffer()

    def set_text(self, text):
        GLib.idle_add(self._text_buffer.set_text, text)

    def get_text(self):
        return self._text_buffer.get_text()

    def add_line(self, line):
        end_iter = self._text_buffer.get_end_iter()
        self._text_buffer.insert(end_iter, line + "\n")
