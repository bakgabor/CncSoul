from gi.repository import GLib

class ComboBoxText:

    def __init__(self, gtk_combo_box):
        self._gtk_combo_box = gtk_combo_box

    def new_list(self, list):
        GLib.idle_add(self._create_new_list, list)

    def add(self, text):
        GLib.idle_add(self._gtk_combo_box.append_text, text)

    def remove_all(self):
        GLib.idle_add(self._gtk_combo_box.remove_all)

    def get_active(self):
        return self._gtk_combo_box.get_active_text()

    def _create_new_list(self, list):
        self._gtk_combo_box.remove_all()
        self._gtk_combo_box.set_entry_text_column(0)
        for country in list:
            self._gtk_combo_box.append_text(country)

        self._gtk_combo_box.set_active(0)
