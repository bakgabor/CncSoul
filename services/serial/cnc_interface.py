from app.event.event import Event


class CncInterface (Event):

    """
    Send home command to machine
    """
    def home(self):
        return self
    """
    Send command string to machine.
    """
    def send_command(self, command):
        return self

    """
    Activete controller.
    There can be multiple controllers.
    """
    def set_active(self, value):
        return self

    """
    Send jog command to machine.
    """
    def jog(self, movement, speed=2000):
        return self

    """
    Set gcode GCodeList class to run
    """
    def set_gcode(self, gcode):
        return self

    """
    Sets where to start running the gcode
    """
    def set_selected_line(self, line):
        return self

    """
    Set pause command to machine 
    """
    def pause(self):
        return self

    """
    Set stop command to machine 
    """
    def stop(self):
        return self

    """
    It will start running the set gcode
    """
    def run_code(self):
        return self

    """
    Set null pos
    """
    def set_null(self, x=None, y=None, z=None, a=None, b=None):
        return self

    """
    send bytes to machine
    """
    def send_bytes(self, bytes_data):
        return self
