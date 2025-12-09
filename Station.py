import Constants
import math

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


    def is_clicked(self, x, y):
        """
        Checks if the given coordinates are within the stations radius
        :param x: int - x coordinate of the click
        :param y: int - y coordinate of the click
        :return: bool - True if the click is within the radius, False otherwise fuck you
        """
        distance = math.sqrt((self.position[0] - x) ** 2 + (self.position[1] - y) ** 2)
        return distance <= Constants.UI_STATION_RADIUS

