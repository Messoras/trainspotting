"""
Collection of constants used by the main game
Separately imported for clarity
"""

MAX_LINES = 3
LINE_COLOR = ["red", "blue", "yellow", "green"]
CARGO_TYPE_NAMES = ["coal", "wood", "gold", "crystal"]
CARGO_TYPE_TO_IMAGE = {
    0: "img/coal.png",
    1: "img/wood.png",
    2: "img/gold.png",
    3: "img/crystal.png"
}
DAISY_PATH = "img/daisy.png"
ELIMINATION_TIMER = 2000
CARGO_SPOTS_PER_TROLLEY = 6
CARGO_SPAWN_TICK_DELAY = 200
STATION_SPAWN_TICK_DELAY = 1500
MS_PER_TICK = 20
TRAIN_SPEED = 5
MAX_TRAINS_PER_LINE = 2

CARGO_DEPLOY_TIME = 5

COST_PER_TRAIN = 500
COST_PER_LINE = 0
COST_PER_METER = 0.5
STARTING_CAPITAL = 1000
CARGO_VALUE = {
    0: 10,
    1: 20,
    2: 50,
    3: 100
}

FIELD_WIDTH = 1100
FIELD_HEIGHT = 900
EDGE_MARGIN = 100

UI_WIDTH = 1600
UI_HEIGHT = 900
UI_SIDEBAR_MARGIN = 500
UI_STATION_RADIUS = 30
FLICKER_DURATION = 10

CHOO_CHOO_SOUND = "sounds/chocho.wav"