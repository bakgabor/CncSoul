from gi.repository import GLib


class Scroll:

    def __init__(self, gtk_scroll):
        self._gtk_scroll = gtk_scroll
        self._vertical_adjustment = self._gtk_scroll.get_vadjustment()
        self._horizontal_adjustment = self._gtk_scroll.get_hadjustment()

    def get_vertical_size(self):
        return self._vertical_adjustment.get_page_size()

    def get_horizontal_size(self):
        return self._horizontal_adjustment.get_page_size()

    def set_vertical_scroll(self, scroll):
        GLib.idle_add(self._vertical_adjustment.set_value, scroll)

    def set_horizontal_scroll(self, scroll):
        GLib.idle_add(self._horizontal_adjustment.set_value, scroll)

    def scroll_to_bottom(self):
        GLib.idle_add(
            self._vertical_adjustment.set_value,
            self._vertical_adjustment.get_upper() - self._vertical_adjustment.get_page_size()
        )
