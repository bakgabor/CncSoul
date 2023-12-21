from app.gui.gui_generator import GuiGenerator
from app.service.abstract_service import AbstractService


class AbstractPresenter (AbstractService):

    def __init__(self, servie_container):
        super().__init__(servie_container)
        self._sensitive_value = None
        self._gui_generator: GuiGenerator = self._get_service('gui_generator')
        self._signals = {}

    def get_signals(self):
        return self._signals

    def start(self):
        return

    def _set_window_title(self, title):
        self._gui_generator.set_title(title)

    def _get_gui_item(self, page, key):
        if not self._gui_generator:
            self._gui_generator: GuiGenerator = self._get_service('gui_generator')
        return self._gui_generator.get_item(page, key)

    # run function in started window
    def _exec_to_group(self, group, funtion):
        self._gui_generator.exec_to_group(group, funtion)

    def _item_sensitive(self, page, element, value):
        gui_element = self._get_gui_item(page, element)
        gui_element.set_sensitive(value)

    def _group_sensitive(self, group, value):
        self._sensitive_value = value
        self._exec_to_group(group, self._set_group_sensitive)

    def _set_group_sensitive(self, item):
        item.set_sensitive(self._sensitive_value)
