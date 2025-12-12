import Constants

class Cargo:
    """
    Represents a cargo element which will be created by the main game at a random station
    Cam either be attached to a station or train and delivers a losing condition when it times out
    """
    def __init__(self, cargo_type, start_station, loss_callback, disable_callback):
        """
        Constructor
        :param cargo_type: int - type of this cargo
        :param start_station: Station - first owner object to define position
        """
        self.cargo_type = cargo_type
        self.owner = start_station
        self.elimination_timer = Constants.ELIMINATION_TIMER
        self.trigger_loss = loss_callback
        self.unlist = lambda: disable_callback(self)

    def hop_on_train(self, train):
        self.owner = train

    def tick(self):
        self.elimination_timer -= 1
        if self.elimination_timer <= 0:
            self.trigger_loss()