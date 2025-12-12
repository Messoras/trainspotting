import Constants
import math

class Station:
    """
    Represents a station element that can be attached to a line
    Trains can load or unload cargo here to progress the game.
    """
    def __init__(self, x_pos, y_pos, cargo_type):
        """
        Constructor
        :param x_pos: int - x position on playing field
        :param y_pos: int - y position on playing field
        :param cargo_type: int - type of the cargo to be deployed here
        """
        self.position = (x_pos, y_pos)
        self.cargo_type = cargo_type
        self.attached_lines = set()
        self.cargo_load = []


    def is_clicked(self, x, y):
        """
        Checks if the given coordinates are within the stations radius
        :param x: int - x coordinate of the click
        :param y: int - y coordinate of the click
        :return: bool - True if the click is within the radius, False otherwise fuck you
        """
        distance = math.sqrt((self.position[0] - x) ** 2 + (self.position[1] - y) ** 2)
        return distance <= Constants.UI_STATION_RADIUS


    def add_cargo(self, cargo):
        """
        Adds a cargo item to the station's load.
        """
        self.cargo_load.append(cargo)

    def get_cargo(self):
        """
        Removes and returns the first cargo item from the station's load.
        """
        if self.cargo_load:
            return self.cargo_load.pop(0)
        return None

    def get_distance_to(self, other_station):
        """
        Calculates the distance to another station.
        :param other_station: Station or position - the other station
        :return: float - the distance between the two stations
        """
        if type(other_station) == Station:
            return math.sqrt((self.position[0] - other_station.position[0]) ** 2 + (self.position[1] - other_station.position[1]) ** 2)
        return math.sqrt((self.position[0] - other_station[0]) ** 2 + (self.position[1] - other_station[1]) ** 2)

    def is_connected_to_cargo_type(self, cargo_type):
        """
        Determines if a line is connected to this station that can deploy the given cargo type
        :param cargo_type: int - id of the cargo type to check for
        :return: Bool
        """
        for lin in self.attached_lines:
            if lin.can_deploy_type(cargo_type):
                return True
        return False
