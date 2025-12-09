import time
import asyncio
from random import randint

import Constants
import UI
from Line import Line
from Cargo import Cargo
from Station import Station

class Game:
    def __init__(self):
        """
        Sets up everything needed to start the game logic
        :return: None
        """
        self.stations: list['Station'] = []
        self.cargos: list['Cargo'] = []
        self.lines: list['Line'] = []
        self.possible_types = [0, 1, 2]
        self.money: int = 100
        self.running = True
        self.tick_counter = 0
        self.last_time = time.perf_counter()

        self.spawn_station()


    def spawn_station(self):
        """
        Creates a new station at a random position with pseudo-random cargo-type
        :return:
        """
        x_pos = randint(0 + Constants.EDGE_MARGIN, Constants.FIELD_WIDTH - Constants.EDGE_MARGIN)
        y_pos = randint(0 + Constants.EDGE_MARGIN, Constants.FIELD_HEIGHT - Constants.EDGE_MARGIN)
        c_type = randint(0, self.possible_types[-1])

        self.stations.append(Station(x_pos, y_pos, c_type))


    def spawn_cargo(self):
        """
        Creates a new cargo object (every x ticks at every station)
        :return:
        """
        pass


    def tick(self):
        """
        Handles all logic that needs to be called continuously to update the game state
        :return: None
        """
        for l in self.lines:
            l.tick()
        for c in self.cargos:
            c.tick()
        if self.tick_counter % Constants.STATION_SPAWN_TICK_DELAY == 0:
            self.spawn_station()
        if self.tick_counter % (1000 // Constants.MS_PER_TICK) == 0:
            print("A second has passed")
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
    g = Game()
    ui = UI.create_ui(g)
    await asyncio.create_task(game_loop(g, ui))
    # await async_tkinter_loop(ui.master)


if __name__ == "__main__":
    asyncio.run(main())

