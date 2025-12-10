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
        if not self.line.stations:
            return 0, 0 

        
        if self.progress == 0.0:
            return self.line.stations[self.current_station_index].position

        
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

    def update(self):
        """
        Updates the train's progress on the line.
        """
        if self.wait_timer > 0:
            self.wait_timer -= 1
            if self.wait_timer == 0:
                self.progress = 0.0

                is_loop = self.line.is_loop()
                num_stations = len(self.line.stations)

                if is_loop:
                    # Circular movement
                    if self.direction == 1:
                        self.current_station_index = (self.current_station_index + 1) % (num_stations - 1)
                    else:
                        self.current_station_index = (self.current_station_index - 1 + (num_stations - 1)) % (num_stations - 1)

                else: # Linear track
                    # 1. advance index to mark arrival at the new station
                    self.current_station_index += self.direction
                    
                    # 2. decide whether to flip direction for the *next* trip
                    is_short_line_for_ping_pong = num_stations <= 3

                    if is_short_line_for_ping_pong:
                        
                        if self.current_station_index >= num_stations - 1 and self.direction == 1:
                            self.direction = -1
                        elif self.current_station_index <= 0 and self.direction == -1:
                            self.direction = 1

            return

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

        if self.progress >= 1.0:
            self.progress = 1.0
            self.wait_timer = 24
            
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
        :return: None
        """
        for i in range(len(self.cargo_load) - 1, -1, -1):
            if self.cargo_load[i].cargo_type == cargo_type:
                del self.cargo_load[i]