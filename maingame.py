import time
import asyncio
from random import randint, choice

import Constants
import UI
from Line import Line
from Cargo import Cargo
from Station import Station
from Train import Train

class Game:
    def __init__(self):
        """
        Sets up everything needed to start the game logic
        :return: None
        """
        self.stations: list['Station'] = []
        self.cargos: list['Cargo'] = []
        self.lines: list['Line'] = []
        self.trains: list['Train'] = []
        for i in range(Constants.MAX_LINES):
            self.lines.append(Line(i, Constants.LINE_COLOR[i]))
        self.possible_types = [0, 1, 2]
        self.available_stations = [0, 1]
        self.money: int = 100
        self.score = 0
        self.running = True
        self.tick_counter = 1201
        self.last_time = time.perf_counter()
        self.selection = None
        self.game_over = False

        self.generate_initial_stations()

    def generate_initial_stations(self):
        """
        Creates the first 2 stations to create a simple initial state
        :return:
        """
        for i in range(len(self.possible_types) - 1):
            x = randint(0 + Constants.EDGE_MARGIN, Constants.FIELD_WIDTH - Constants.EDGE_MARGIN)
            y = randint(0 + Constants.EDGE_MARGIN, Constants.FIELD_HEIGHT - Constants.EDGE_MARGIN)
            c_type = i
            self.stations.append(Station(x, y, c_type))


    def spawn_station(self):
        """
        Creates a new station at a random position with pseudo-random cargo-type
        :return:
        """
        x_pos = randint(0 + Constants.EDGE_MARGIN, Constants.FIELD_WIDTH - Constants.EDGE_MARGIN)
        y_pos = randint(0 + Constants.EDGE_MARGIN, Constants.FIELD_HEIGHT - Constants.EDGE_MARGIN)
        c_type = choice(self.possible_types)

        self.stations.append(Station(x_pos, y_pos, c_type))
        if not c_type in self.available_stations:
            self.available_stations.append(c_type)


    def spawn_cargo(self):
        """
        Creates a new random cargo object (every x ticks at every station)
        :return: None
        """
        for sta in self.stations:
            lst = self.available_stations.copy()
            lst.remove(sta.cargo_type)
            c = Cargo(choice(lst),sta,self.game_loss,self.unlist_cargo)
            sta.cargo_load.append(c)
            self.cargos.append(c)

    def unlist_cargo(self, cargo):
        """
        Disables the loss condition of given cargo when it is deployed, called by Cargo class
        :param cargo: Cargo - element to remove from tracking list
        :return: None
        """
        self.cargos.remove(cargo)

    def game_loss(self):
        """
        Performs everything to end the current session in a loss
        :return: None
        """
        self.game_over = True
        self.selection = None

    def increment_score(self):
        """
        Callback to gain score when cargo is delivered, called by train class
        :return: None
        """
        self.score += 1


    def get_clicked_station(self, x, y):
        """
        Returns the first station that touches the given coordinates
        :param x: x Position
        :param y: y Position
        :return: Station
        """
        for station in self.stations:
            if station.is_clicked(x, y):
                return station
        return None


    def get_available_lines(self, sta):
        """
        Returns all lines that should be available to build from this station
        """
        res = []

        for i in range (len(self.lines)):
            if self.lines[i].is_valid_drag_point(sta):
                res.append(i)
        return res


    def buy_train(self, line, station):
        """
        Creates a new train on the given line if there are none.
        """
        # For simplicity, only allow one train per line for now
        if len(line.trains) <= Constants.MAX_TRAINS_PER_LINE: # and check available trains or buy price
            train = Train(line, station, self.increment_score)
            line.trains.append(train)


    def tick(self):
        """
        Handles all logic that needs to be called continuously to update the game state
        :return: None
        """
        self.trains = []
        for l in self.lines:
            l.tick(self.tick_counter)
            self.trains.extend(l.trains)
        for c in self.cargos:
            c.tick()
        if self.tick_counter % Constants.STATION_SPAWN_TICK_DELAY == 0:
            self.spawn_station()
        if self.tick_counter % Constants.CARGO_SPAWN_TICK_DELAY == 0:
            self.spawn_cargo()
        if self.tick_counter % (1000 // Constants.MS_PER_TICK) == 0:
            pass # 1 second

        if self.tick_counter == 10000:
            self.possible_types.append(3)

        self.tick_counter += 1


async def game_loop(game, ui):
    """
    Ticks the game logic, using the MS_PER_TICK constant. Runs faster when ticks take longer
    :param ui: TrainspottingAppUI - UI App to be updated every tick
    :param game: Game - game instance to be ticked
    :return: None
    """
    old_time = 0

    interval = Constants.MS_PER_TICK / 1000.0
    while game.running:
        start = time.perf_counter()

        # Call the game logic
        game.tick()

        # UI
        try:
            ui.paint_field(old_time)
            ui.master.update()
        except Exception as ex:
            print(ex)
            break  # window was destroyed

        # Compute how long the frame took
        elapsed = time.perf_counter() - start
        # Sleep the remaining time, if any
        # print(interval,elapsed)
        sleep_time = interval - elapsed
        old_time = sleep_time * 1000
        await asyncio.sleep(sleep_time)


async def main():
    """
    Creates a UI object and starts the asynchronous game loop
    :return: None
    """
    g = Game()
    ui = UI.create_ui(g)
    await asyncio.create_task(game_loop(g, ui))

"""
Starting script
"""
if __name__ == "__main__":
    asyncio.run(main())

