import Constants

class Station:
    def __init__(self, x_pos, y_pos, cargo_type):
        """
        Constructor
        :param x_pos: int - x position on playing field
        :param y_pos: int - y position on playing field
        :param cargo_type: int - type of the cargo to be deployed here
        """
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
            # res.append(lines[i].is_valid_drag_point(self))
            pass
        return res


