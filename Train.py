import Constants
import math

class Train:
    def __init__(self, line):
        """
        Constructor
        :param line: Line object
        """
        self.line = line
        self.line_id = line.id
        self.cargo_load = []  
        self.direction = 1  
        self.current_station_index = 0
        self.progress = 0.0 
        self.wait_timer = 0
    @property
    def position(self):
        """
        Calculates the x, y position of the train on the track.
        """
        # catch some bugs
        if not self.line.stations:
            return 0, 0 

        # when at station TODO: this is 1 behind
        if self.progress == 0.0:
            return self.line.stations[self.current_station_index].position

        # when on the road
        start_station_index = self.current_station_index
        end_station_index = self.current_station_index + self.direction

        
        if self.direction == 1:
            if end_station_index >= len(self.line.stations):

                return self.line.stations[start_station_index].position
        else: 
             if end_station_index < 0:

                return self.line.stations[start_station_index].position

        start_station = self.line.stations[start_station_index]
        end_station = self.line.stations[end_station_index]

        x1, y1 = start_station.position
        x2, y2 = end_station.position
        
        x = x1 + (x2 - x1) * self.progress
        y = y1 + (y2 - y1) * self.progress
        
        return x, y

    def update(self, tick_counter):
        """
        Updates the train's progress on the line.
        """
        # during stop
        if self.wait_timer > 0:
            self.wait_timer -= 1

            # Continue driving
            if self.wait_timer == 0:
                self.progress = 0.0

                is_loop = self.line.is_loop()
                num_stations = len(self.line.stations)

                if is_loop:
                    # Then, check for loop wrap-around
                    if self.current_station_index >= num_stations - 1:
                        self.current_station_index = 0
                        # check if turn around is needed
                    elif self.current_station_index < 0:
                        self.current_station_index = num_stations - 2
                else:
                    # Then, check for direction flip
                    if self.current_station_index >= num_stations - 1 and self.direction == 1:
                        self.direction = -1
                    elif self.current_station_index <= 0 and self.direction == -1:
                        self.direction = 1

            # While standing at station
            if tick_counter % Constants.CARGO_DEPLOY_TIME == 0:
                station = self.line.stations[self.current_station_index]
                # Unloading
                cargo_to_unload = next((c for c in self.cargo_load if c.cargo_type == station.cargo_type), None)
                if cargo_to_unload:
                    self.cargo_load.remove(cargo_to_unload)
                    # not loading station when same type (cargo is at the correct place)
                    # station.add_cargo(cargo_to_unload)
                    del cargo_to_unload
                # Loading
                elif station.cargo_load and len(self.cargo_load) < Constants.CARGO_SPOTS_PER_TROLLEY:
                    cargo_to_load = station.get_cargo()
                    if cargo_to_load:
                        self.add_cargo(cargo_to_load)

            return

        # while driving
        if not self.line.stations or len(self.line.stations) < 2:
            return

        start_station_index = self.current_station_index
        end_station_index = self.current_station_index + self.direction

        if self.direction == 1:
            if end_station_index >= len(self.line.stations):
                return
        else: 
             if end_station_index < 0:
                return

        start_station = self.line.stations[start_station_index]
        end_station = self.line.stations[end_station_index]

        x1, y1 = start_station.position
        x2, y2 = end_station.position
        
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        if distance > 0:
            self.progress += Constants.TRAIN_SPEED / distance
        else:
            self.progress = 1.0

        # Arrived at new station
        if self.progress >= 1.0:
            self.progress = 0
            # First, update index to mark arrival at the new station
            self.current_station_index += self.direction
            self.wait_timer = Constants.CARGO_DEPLOY_TIME * Constants.CARGO_SPOTS_PER_TROLLEY * 2
            
            # TODO: Handle cargo loading/unloading at the station

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