import Constants

class Cargo:
    def __init__(self, cargo_type, start_station):
        """
        Constructor
        :param cargo_type: int - type of this cargo
        :param start_station: Station - first owner object to define position
        """
        self.cargo_type = cargo_type
        self.owner = start_station
        self.elimination_timer = Constants.ELIMINATION_TIMER

    def hop_on_train(self, train):
        self.owner = train

    def tick(self):
        self.elimination_timer -= 1
        if self.elimination_timer <= 0:
            # TODO: Trigger game loss
            #
            pass