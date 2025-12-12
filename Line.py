from Station import *
from Train import *

class Line:
    def __init__(self, line_id: int, line_color: str):
        self.id = line_id
        self.stations: list['Station'] = [] 
        self.trains: list['Train'] = []
        self.tracks: list[tuple['Station', 'Station']] = []
        self.color = line_color

    def tick(self, tick_counter):
        """
        manages train movement each game tick
        :param tick_counter: int
        :return: None
        """
        for train in self.trains[:]: # Iterate over a copy
            train.update(tick_counter)

    def add_station(self, station: 'Station', at_beginning: bool = False):
        """
        Adds a new station to the line.
        :param at_beginning: determines if the station is at the beginning of the line
        :param station: Station to add
        """
        if self.stations:
            if at_beginning:
                if self.stations[0] == station:
                    return
                self.stations.insert(0, station)
                station.attached_lines.add(self) # updates line set for station
                self.tracks.insert(0, (self.stations[0], self.stations[1]))
                for train in self.trains:
                    train.current_station_index += 1
            else:
                if self.stations[-1] == station:
                    return
                self.stations.append(station)
                station.attached_lines.add(self) # updates line set for station
                self.tracks.append((self.stations[-2], self.stations[-1]))
        else:
            self.stations.append(station)
            station.attached_lines.add(self) # updates line set for station

    def remove_station(self, station: 'Station'):
        """
        Removes a station from the line.
        :param station: Station to remove
        """
        if station in self.stations:
            index = self.stations.index(station)
            self.stations[index].attached_lines.remove(self)
            
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

    def can_delete_track(self, track: int) -> bool:
        """
        Check if Track can be deleted.
        :param track: int - Track to check
        """
        if not self.tracks:
            return False
        #if isinstance(track, int):
        #    return self.can_delete_track(self.tracks[track])

        # Check for trains on this track
        train_on_track = False
        for trn in self.trains:
            if trn.current_station_index == track and trn.direction > 0:
                train_on_track = True
                break
            if trn.current_station_index - 1 == track and trn.direction < 0:
                train_on_track = True
                break

        # Check if line is a loop or track is element at the end of line
        return (self.is_loop() or track == 0 or track == len(self.tracks) - 1) and not train_on_track

    def demolish_track(self, track: int):
        """
        Removes the track from the line
        :param track: int - track_id of the track to remove
        :return: None
        """
        if self.can_delete_track(track):
            # Store train's current station object to find it later
            train_locations = {}
            if self.stations:  # Ensure stations exist before accessing them
                for train in self.trains:
                    if train.current_station_index < len(self.stations):
                        train_locations[train] = self.stations[train.current_station_index]
                    else:  # Failsafe for inconsistent state
                        train_locations[train] = self.stations[0]

            was_loop = self.is_loop()

            if was_loop:
                # It's a loop, so we're opening it into a simple line.
                new_stations = self.stations[track + 1:-1] + self.stations[:track + 1]
                self.stations = new_stations
            else:
                # It's a simple line, we can only delete from the ends.
                if track == 0:
                    # remove first station
                    self.remove_station(self.stations[0])
                else:
                    # remove last station
                    self.remove_station(self.stations[-1])

            # Rebuild tracks based on the new station list
            self.tracks.clear()
            if len(self.stations) > 1:
                for i in range(len(self.stations) - 1):
                    self.tracks.append((self.stations[i], self.stations[i + 1]))

            trains_to_remove = []
            for train, old_station in train_locations.items():
                try:
                    new_index = self.stations.index(old_station)
                    train.current_station_index = new_index
                    # train.progress = 0.0  # reset progress to be safe
                    if not self.is_loop() and len(self.stations) > 1:
                        if train.current_station_index == 0:
                            train.direction = 1
                        elif train.current_station_index == len(self.stations) - 1:
                            train.direction = -1
                except ValueError:
                    # The station the train was at has been removed, so remove the train
                    trains_to_remove.append(train)

            # Remove last station if only 1 remains
            if len(self.stations) == 1:
                self.stations.clear()

            # Safely remove trains
            for train in trains_to_remove:
                if train in self.trains:
                    self.trains.remove(train)

            # If all stations are gone, clear all trains
            if not self.stations:
                self.trains.clear()

    def is_valid_drag_point(self, station: 'Station') -> bool:
        """
        Check if dragging to this station is allowed.
        Rule 1: If no stations exist, any station is valid.
        Rule 2: Only the first or last station in the line can be connected to.
        """
        if not self.stations or len(self.stations) == 0:
            return True

        elif station not in self.stations:
            return False

        is_start = (station == self.stations[0])
        is_end = (station == self.stations[-1])

        return is_start ^ is_end

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

    def can_deploy_type(self, cargo_type: int) -> bool:
        """
        Check if the line services a station of the given shape type.
        The train will only stop at stations of this shape type.
        :param cargo_type: int - id of the checked cargo
        :return: Bool
        """
        for station in self.stations:
            if station.cargo_type == cargo_type:
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
