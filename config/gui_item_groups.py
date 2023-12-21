class GuiItemGroups:

    def __init__(self):
        self._gui_group_schema = None

    def registered_groups(self):
        self._gui_group_schema = [
            {
                'name': 'control',
                'items': [
                    {'page': 'main', 'key': 'x_button'},
                    {'page': 'main', 'key': 'y_button'},
                    {'page': 'main', 'key': 'z_button'},
                    {'page': 'main', 'key': 'x_null'},
                    {'page': 'main', 'key': 'y_null'},
                    {'page': 'main', 'key': 'z_null'},
                    {'page': 'main', 'key': 'xyz_null'},
                    {'page': 'main', 'key': 'control_forward_left'},
                    {'page': 'main', 'key': 'control_forward'},
                    {'page': 'main', 'key': 'control_forward_right'},
                    {'page': 'main', 'key': 'control_left'},
                    {'page': 'main', 'key': 'control_null'},
                    {'page': 'main', 'key': 'control_right'},
                    {'page': 'main', 'key': 'control_back_left'},
                    {'page': 'main', 'key': 'control_back'},
                    {'page': 'main', 'key': 'control_back_right'},
                    {'page': 'main', 'key': 'control_up'},
                    {'page': 'main', 'key': 'control_down'},
                    {'page': 'main', 'key': 'control_home'},
                    {'page': 'main', 'key': 'code_play'},
                    {'page': 'main', 'key': 'code_pause'},
                    {'page': 'main', 'key': 'code_stop'},
                    {'page': 'main', 'key': 'control_unlock'},
                ]
            },
            {
                'name': 'stop_pause',
                'items': [
                    {'page': 'main', 'key': 'code_pause'},
                    {'page': 'main', 'key': 'code_stop'},
                ]
            }
        ]
