import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from app.event.event import Event


class GtkFileChooser(Event):

    def __init__(self):
        super().__init__()
        self._dialog = None
        self._events = {
            'open': [],
            'cancel': []
        }
        self._filters = None

    def show(self, title="Choose a file"):
        self._dialog = Gtk.FileChooserDialog(
            title=title, action=Gtk.FileChooserAction.OPEN
        )
        self._dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )
        self._generate_filters()

        response = self._dialog.run()

        if response == Gtk.ResponseType.OK:
            self._run_event('open', arguments=(self._dialog.get_filename(),))
        elif response == Gtk.ResponseType.CANCEL:
            self._run_event('cancel')

        self._dialog.destroy()

    def add_filters(self, filters):
        self._filters = filters

    def _generate_filters(self):
        for filter_item in self._filters:
            filter_text = Gtk.FileFilter()
            filter_text.set_name(filter_item['title'])
            if 'pattern' in filter_item:
                if isinstance(filter_item['pattern'], list):
                    for item in filter_item['pattern']:
                        filter_text.add_pattern(item)
                else:
                    filter_text.add_pattern(filter_item['pattern'])
            if 'mime_type' in filter_item:
                if isinstance(filter_item['mime_type'], list):
                    for item in filter_item['mime_type']:
                        filter_text.add_pattern(item)
                else:
                    filter_text.add_mime_type(filter_item['mime_type'])
            self._dialog.add_filter(filter_text)
