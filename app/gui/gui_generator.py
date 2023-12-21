import gi

from app.gui.gtk.interfaces.Scrool import Scroll
from app.gui.gtk.interfaces.button import Button
from app.gui.gtk.interfaces.combo_box_text import ComboBoxText
from app.gui.gtk.interfaces.label import Label
from app.gui.gtk.interfaces.list_box import ListBox
from app.gui.gtk.interfaces.text_view import TextView
from app.service.abstract_service import AbstractService
from config.gui_item_groups import GuiItemGroups
from config.pages import GuiPages

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from app.gui.gtk.gtk_window import MainWindow


class GuiGenerator (AbstractService, GuiItemGroups, GuiPages):

    def __init__(self, servie_container):
        super().__init__(servie_container)
        self._gui_group_schema = None
        self._gui_groups = {}
        self._notebook = None
        self._gui_pages = None
        self._main_title = None

        self._selected_data = None
        self._selected_notebook = None
        self._main_windows = None
        self._level_bar = None
        self._builders = {}

        self._services = []

        self._interfaces = {
            'ComboBoxText': ComboBoxText,
            'Button': Button,
            'Label': Label,
            'ListBox': ListBox,
            'TextView': TextView,
            'ScrolledWindow': Scroll
        }

        self.registered_groups()
        self.registered_pages()

    def set_title(self, title):
        self._main_windows.set_title(self._main_title + ': ' + title)

    def generate(self):
        self._notebook = Gtk.Notebook()
        for data in self._gui_pages:
            self._selected_data = data
            self._create_notebook()
        self._create_main_vindow()

    def get_item(self, page, key):
        obj = self._builders[page].get_object(key)
        name = obj.__class__.__name__
        return self._interfaces[name](obj)

    def exec_to_group(self, group, function):
        for element in self._gui_groups[group]:
            function(element)

    def _create_notebook(self):
        builder = Gtk.Builder()
        builder.add_from_file("gui/glade/" + self._selected_data['key'] + ".glade")

        connect_signals = {}
        for data in self._selected_data['services']:
            service = self._get_service(data)
            signals = service.get_signals()
            connect_signals.update(signals)
            self._services.append(service)
        builder.connect_signals(connect_signals)
        self._builders[self._selected_data['key']] = builder

        internal = builder.get_object("internal")
        self._notebook.append_page(internal, Gtk.Label(label=self._selected_data['title']))

    def _create_main_vindow(self):
        self._main_windows = MainWindow(self._main_title)
        self._main_windows.connect("destroy", Gtk.main_quit)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.pack_start(self._notebook, True, True, 0)

        self._level_bar = Gtk.LevelBar(height_request=30)

        process = self._get_service('process')
        process.set_level_bar(self._level_bar)
        box.pack_start(self._level_bar, False, True, 0)

        self._main_windows.add(box)
        self._main_windows.show_all()

        self._create_gui_groups()

        for service in self._services:
            service.start()

        Gtk.main()

    def _create_gui_groups(self):
        for group_schema in self._gui_group_schema:
            self._gui_groups[group_schema['name']] = []
            for items in group_schema['items']:
                self._gui_groups[group_schema['name']].append(self.get_item(items['page'], items['key']))

