from gi.repository import GLib

class Button:

    def __init__(self, gtk_button):
        self._gtk_button = gtk_button

    def set_label(self, title):
        GLib.idle_add(self._gtk_button.set_label, title)

    def set_sensitive(self, active):
        GLib.idle_add(self._gtk_button.set_sensitive, active)
