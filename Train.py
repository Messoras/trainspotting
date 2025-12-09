import Constants

class Train:
    def __init__(self, line_id, x_pos, y_pos):
        """
        Constructor
        :param line_id: int - line to put train on
        """
        self.position = (x_pos, y_pos)
        self.cargo_load = [] # maximum 6
        self.line_id = line_id
        self.direction = 1 # + -> forward, - -> backwards

    def add_cargo(self, cargo):
        """
        Adds cargo if spots are open (call after deploy_cargo)
        :param cargo: list or Cargo object - Cargo to add to the train if possible
        :return: None
        """
        if type(cargo) == list:
            for c in cargo:
                self.add_cargo(c)
        else: # type == Cargo:
            if len(self.cargo_load) < Constants.CARGO_SPOTS_PER_TROLLEY:
                self.cargo_load.append(cargo)
                cargo.owner = self

    def deploy_cargo(self, cargo_type):
        """
        Removes cargo of the given type (call before add_cargo)
        :param cargo_type: int - type of the cargo to be deployed
        :return: None
        """
        for i in range(len(self.cargo_load),0,-1):
            if self.cargo_load[i].cargo_type == cargo_type:
                del self.cargo_load[i]
