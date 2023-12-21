from gi.repository import GLib


class Label:

    def __init__(self, gtk_label):
        self._gtk_label = gtk_label

    def set_text(self, title):
        GLib.idle_add(self._gtk_label.set_text, title)
