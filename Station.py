from Constants import *

class Station:
    def __init__(self, x_pos, y_pos, cargo_type):
        self.position = (x_pos, y_pos)
        self.cargo_type = cargo_type
        self.attached_lines = []

    def available_lines(self):
        """
        Should be asked the main game, not here

        Returns all lines that should be available to connect with this station
        """
        res = []
        for i in range(Constants.MAX_LINES):
            #TODO: res.append(lines[i].available_for_station(self))
            pass

