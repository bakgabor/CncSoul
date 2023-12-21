import threading


class Event:

    def __init__(self):
        self._events = {}

    def connect_event(self, event, function):
        if self._events[event] is None:
            self._events[event] = []
        self._events[event].append(function)

    def _run_event(self, event_name, arguments=()):
        if event_name in self._events:
            for event_function in self._events[event_name]:
                thread = threading.Thread(target=event_function, args=arguments)
                thread.start()
