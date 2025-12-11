import Constants
import math

class Train:
    def __init__(self, line, station, score_callback):
        """
        Constructor
        :param line: Line object
        :param station: Station object where the train will spawn
        """
        self.line = line
        self.line_id = line.id
        self.cargo_load = []  
        self.direction = 1
        self.trigger_score = score_callback
        try:
            self.current_station_index = self.line.stations.index(station)
        except ValueError:
            self.current_station_index = 0  # Default to 0 if station not found

        # Set initial direction based on position for non-looping lines
        if not self.line.is_loop() and len(self.line.stations) > 1 and self.current_station_index == len(self.line.stations) - 1:
            self.direction = -1
        else:
            self.direction = 1
        self.progress = 0.0 
        self.wait_timer = 0

        # Immediately load cargo from spawn station
        while station.cargo_load and len(self.cargo_load) < Constants.CARGO_SPOTS_PER_TROLLEY:
            # Find the index of the first suitable cargo
            index = next(
                (station.cargo_load.index(c)
                 for c in station.cargo_load if self.moving_towards(c.cargo_type)), -1
            )
            
            # If a suitable cargo is found, load it. Otherwise, break the loop.
            if index != -1:
                cargo_to_load = station.cargo_load[index]
                self.add_cargo(cargo_to_load)
                del station.cargo_load[index]
            else:
                break
    @property
    def position(self):
        """
        Calculates the x, y position of the train on the track.
        """
        # catch some bugs
        if not self.line.stations:
            return 0, 0 

        # when at station
        if self.progress == 0.0:
            return self.line.stations[self.current_station_index].position

        # when on the road
        start_station_index = self.current_station_index
        end_station_index = self.current_station_index + self.direction

        try:
            start_station = self.line.stations[start_station_index]
            end_station = self.line.stations[end_station_index]
        except IndexError:
            # At the end of the line, return the last station's position
            return self.line.stations[start_station_index].position

        x1, y1 = start_station.position
        x2, y2 = end_station.position
        
        x = x1 + (x2 - x1) * self.progress
        y = y1 + (y2 - y1) * self.progress
        
        return x, y

    def moving_towards(self, cargo_type):
        """
        Checks if the train goes towards the given cargo type
        :param cargo_type: int - Cargo type
        :return: Bool
        """
        if self.line.stations[0] == self.line.stations[-1]:
            return True
        else:
            sta_lst = []
            if self.direction == 1:
                sta_lst.extend(self.line.stations[self.current_station_index+1:])
            else:
                sta_lst.extend(self.line.stations[:self.current_station_index])
            #print([Constants.CARGO_TYPE_NAMES[st.cargo_type] for st in sta_lst])
            for sta in sta_lst:
                if sta.cargo_type == cargo_type:
                    return True
            return False

    def update(self, tick_counter):
        """
        Updates the train's progress on the line
        and handles loading and unloading the train
        """
        # during stop
        if self.wait_timer > 0:
            self.wait_timer -= 1

            # While standing at station
            if tick_counter % Constants.CARGO_DEPLOY_TIME == 0:
                station = self.line.stations[self.current_station_index]
                # Unloading
                cargo_to_unload = next(
                    (c for c in self.cargo_load if c.cargo_type == station.cargo_type
                     ), None)
                if cargo_to_unload:
                    self.cargo_load.remove(cargo_to_unload)
                    # not loading station when same type (cargo is at the correct place)
                    # station.add_cargo(cargo_to_unload)
                    cargo_to_unload.unlist()
                    #del cargo_to_unload
                    self.trigger_score()
                # Loading
                elif station.cargo_load and len(self.cargo_load) < Constants.CARGO_SPOTS_PER_TROLLEY:
                    index = next(
                        (station.cargo_load.index(c)
                         for c in station.cargo_load if self.moving_towards(c.cargo_type)), -1
                    )
                    if index != -1:
                        cargo_to_load = station.cargo_load[index]
                        self.add_cargo(cargo_to_load)
                        del station.cargo_load[index]

            return

        # while driving
        if not self.line.stations or len(self.line.stations) < 2:
            return

        try:
            start_station = self.line.stations[self.current_station_index]
            end_station = self.line.stations[self.current_station_index + self.direction]

            x1, y1 = start_station.position
            x2, y2 = end_station.position

            distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

            if distance > 0:
                self.progress += Constants.TRAIN_SPEED / distance
            else:
                self.progress = 1.0
        except IndexError:
            # At the end of the line, just arrive instantly
            self.progress = 1.0

        is_loop = self.line.is_loop()
        num_stations = len(self.line.stations)

        # Arrived at new station
        if self.progress >= 1.0:
            self.progress = 0.0
            # First, update index to mark arrival at the new station
            self.current_station_index += self.direction
            self.wait_timer = Constants.CARGO_DEPLOY_TIME * Constants.CARGO_SPOTS_PER_TROLLEY * 2

            if not is_loop:
                # Then, check for direction flip
                if self.current_station_index >= num_stations - 1 and self.direction == 1:
                    self.direction = -1
                elif self.current_station_index <= 0 and self.direction == -1:
                    self.direction = 1
            else:
                # It's a loop, wrap around
                if self.current_station_index >= num_stations - 1 and self.direction > 0:
                    self.current_station_index = 0
                elif self.current_station_index <= -1 and is_loop and self.direction < 0:
                    self.current_station_index = len(self.line.stations) - 1

    def add_cargo(self, cargo):
        """
        Adds cargo if spots are open (call after deploy_cargo)
        :param cargo: list or Cargo object - Cargo to add to the train if possible
        :return: None
        """
        if type(cargo) == list:
            for c in cargo:
                self.add_cargo(c)
        else:  # type == Cargo:
            if len(self.cargo_load) < Constants.CARGO_SPOTS_PER_TROLLEY:
                self.cargo_load.append(cargo)
                cargo.owner = self

    def deploy_cargo(self, cargo_type):
        """
        Removes cargo of the given type (call before add_cargo)
        :param cargo_type: int - type of the cargo to be deployed
        :return: Cargo
        """
        for i in range(len(self.cargo_load) - 1, -1, -1):
            if self.cargo_load[i].cargo_type == cargo_type:
                return self.cargo_load.pop(i)
        return None