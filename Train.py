from Constants import *
class Train:
    def __init__(self,line_id):
        self.cargo_load = [] # maximum 6
        self.line_id = line_id
        self.direction = 0 # 1 -> forward, everything else -> backwards

    def add_cargo(self, cargo):
        if type(cargo) == list:
            for c in cargo:
                self.add_cargo(c)
        else:
            if len(self.cargo_load) < Constants.CARGO_SPOTS_PER_TROLLEY:
                self.cargo_load.append(cargo)

    def deploy_cargo(self, cargo_type):
        for i in range(len(self.cargo_load),0,-1):
            if self.cargo_load[i].cargo_type == cargo_type:
                del self.cargo_load[i]