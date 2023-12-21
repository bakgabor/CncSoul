## App event manager

#### Use:
```python
class Test(Event):
        
    def __init__(self):
        super().__init__()
        self._events = [
            'info': [],
        ]
        
    def run_evet(self, info):
        self._run_event('info', arguments=(info,))

            
def event_function(self):
    print('ok')

test = Test()
test.connect_event('info', event_function)
```
