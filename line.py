from typing import List

class Line:
    def __init__(self, color_code: str):
        self.color = color_code
        self.stations: List['Station'] = [] 
        self.trains: List['Train'] = []

    def add_station(self, station: 'Station', add_to_start: bool = False):
        """
        Fügt eine Station hinzu.
        """

    def is_valid_drag_point(self, station: 'Station') -> bool:
        """
        Entscheidet, ob der User von diesem Station aus eine Linie ziehen darf.
        """

        first_station = self.stations[0]
        last_station = self.stations[-1]
        return (station == first_station) or (station == last_station)