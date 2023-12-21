import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ListBox:

    def __init__(self, gtk_list_box):
        self._gtk_list_box = gtk_list_box

    def set_list(self, list_data):
        self.remove_all()
        for item in list_data:
            self._gtk_list_box.add(ListBoxRowWithData(item))

        self._gtk_list_box.show_all()

    def remove_all(self):
        item = self._gtk_list_box.get_row_at_index(0)
        if item is None:
            return
        while item is not None:
            self._gtk_list_box.remove(item)
            item = self._gtk_list_box.get_row_at_index(0)

    def get_selected(self):
        if self._gtk_list_box.get_selected_row() is not None:
            return self._gtk_list_box.get_selected_row().get_data()
        return None


class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.add(Gtk.Label(label=data))

    def get_data(self):
        return self.data
