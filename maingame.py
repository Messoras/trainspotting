import time
import tkinter as tk
import asyncio
from random import randint

import Constants
import UI
import Line
import Cargo
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
        for l in self.lines:
            l.tick()
        for c in self.cargos:
            c.tick()
        if self.tick_counter % 100 == 0:
            self.spawn_station()
        if self.tick_counter % 50 == 0:
            print("A second has passed")
        self.tick_counter += 1


async def game_loop(game, ui):
    """
    Ticks the game logic, using the MS_PER_TICK constant. Runs faster when ticks take longer
    :param root: TrainspottingAppUI - UI App to be updated every tick
    :param game: Game - game instance to be ticked
    :return: None
    """
    print("Am I even called?")
    interval = Constants.MS_PER_TICK / 1000.0
    while game.running:
        start = time.perf_counter()

        # Compute time since last frame
        now = time.perf_counter()
        game.last_time = now

        # Call the game logic
        game.tick()

        # Compute how long the frame took
        elapsed = time.perf_counter() - start
        # Sleep the remaining time, if any
        sleep_time = interval - elapsed
        await asyncio.sleep(sleep_time)

        # UI
        try:
            ui.paint_field(1 / sleep_time)
            ui.master.update()
        except:
            break  # window was destroyed


async def main():
    g = Game()
    ui = UI.create_ui(g)
    await asyncio.create_task(game_loop(g, ui))
    # await async_tkinter_loop(ui.master)


if __name__ == "__main__":
    asyncio.run(main())

