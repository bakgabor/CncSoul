class GuiPages:

    def __init__(self):
        self._gui_pages = None
        self._main_title = None

    def registered_pages(self):
        self._main_title = 'Cnc soul'
        self._gui_pages = [
            {
                'key': 'main',
                'title': 'Main',
                'services': [
                    'cnc_control',
                    'cnc_runner'
                ]
            },
            {
                'key': 'connect',
                'title': 'Connect',
                'services': [
                    'cnc_connection'
                ]
            },
        ]
