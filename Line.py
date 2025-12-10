from Station import *
from Train import *

class Line:
    def __init__(self, line_id: int, color_code: str):
        self.id = line_id
        self.color = color_code
        self.stations: list['Station'] = [] 
        self.trains: list['Train'] = []
        self.tracks: list[tuple['Station', 'Station']] = []

    def tick(self, tick_counter):
        """
        manages train movement each game tick
        :return: None
        """
        for train in self.trains:
            train.update(tick_counter)

    def add_station(self, station: 'Station', at_beginning: bool = False):
        """
         Adds a new station to the line.
        """
        if self.stations:
            if at_beginning:
                if self.stations[0] == station:
                    return
                self.stations.insert(0, station)
                self.tracks.insert(0, (self.stations[0], self.stations[1]))
                for train in self.trains:
                    train.current_station_index += 1
            else:
                if self.stations[-1] == station:
                    return
                self.stations.append(station)
                self.tracks.append((self.stations[-2], self.stations[-1]))
        else:
            self.stations.append(station)

    def remove_station(self, station: 'Station'):
        """Removes a station from the line."""
        if station in self.stations:
            index = self.stations.index(station)
            
            if len(self.stations) > 1:
                if index == 0:
                    self.tracks.pop(0)
                elif index == len(self.stations) - 1:
                    self.tracks.pop()
                else:
                    prev_station = self.stations[index - 1]
                    next_station = self.stations[index + 1]
                    self.tracks.pop(index)
                    self.tracks.pop(index-1)
                    self.tracks.insert(index-1, (prev_station, next_station))

            self.stations.remove(station)

    def can_delete_track(self, track) -> bool:
        """
        Check if Track can be deleted.
        :param track: tuple['Station', 'Station'] or int - Track to check
        TODO: Doesn't return true when it should, also doesn't take trains on the track into consideration
        """
        if not self.tracks:
            return False
        if type(track) == int:
            return self.can_delete_track(self.tracks[track])
        return track == self.tracks[0] or track == self.tracks[-1]

    def demolish_track(self, track: int):
        """
        Removes the track from the line
        :param track: int - track_id of the track to remove
        :return: None
        """
        if self.can_delete_track(self.tracks[track]):
            del self.tracks[track]

    def is_valid_drag_point(self, station: 'Station') -> bool:
        """
        Check if dragging to this station is allowed.
        Rule 1: If no stations exist, any station is valid.
        Rule 2: Only the first or last station in the line can be connected to.
        """
        if not self.stations:
            return True

        if station not in self.stations:
            return False

        is_start = (station == self.stations[0])
        is_end = (station == self.stations[-1])

        return is_start or is_end

    def can_connect_to(self, from_station: 'Station', to_station: 'Station') -> bool:
        """
        Check if a connection between two stations is valid.
        """
        if from_station == to_station:
            return False

        if to_station in self.stations:
            return False

        return True

    def is_loop(self) -> bool:
        """Checks if the line is a closed loop."""
        return len(self.stations) > 2 and self.stations[0] == self.stations[-1]

    def shap_checker(self, shape_type: str) -> bool:
        """
        Check if the line services a station of the given shape type.
        The train will only stop at stations of this shape type.
        """
        for station in self.stations:
            if hasattr(station, 'shape_type') and station.shape_type == shape_type:
                return True
        return False

    def get_next_stop(self, current_station: 'Station', current_direction: int) -> tuple['Station', int]:
        """
        current_direction: 1 (forward) or -1 (backward)
        # Scenario A: End of line reached
        # Scenario B: Start of line reached
        # Scenario C: Normal keep steaming bro
        """
        try:
            index = self.stations.index(current_station)
        except ValueError:
            return current_station, 0

        next_index = index + current_direction

        
        if next_index >= len(self.stations):
            if len(self.stations) > 1:
                return self.stations[-2], -1
            else:
                return current_station, 0
        
        elif next_index < 0:
            if len(self.stations) > 1:
                return self.stations[1], 1
            else:
                return current_station, 0
            
        else:
            return self.stations[next_index], current_direction
