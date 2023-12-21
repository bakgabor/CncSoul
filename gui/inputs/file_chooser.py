from app.gui.gtk.gtk_file_chooser import GtkFileChooser
from app.service.abstract_service import AbstractService


class FileChooser(AbstractService):

    def __init__(self, servie_container):
        super().__init__(servie_container)
        self._file_chooser = GtkFileChooser()

    def show(self, title="Choose a file"):
        self._file_chooser.show(title)

    def connect_event(self, event, function):
        self._file_chooser.connect_event(event, function)

    # [{'title': 'all', 'pattern': '*'}]
    def add_filters(self, filters):
        self._file_chooser.add_filters(filters)
