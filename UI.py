import tkinter as tk

import Constants
from Station import Station

class TrainspottingAppUI:
    def __init__(self, master, game):
        """
        Constructor
        Initializes the main window and defines starting variables
        :param master: tk
        :param game: main game instance
        """
        self.master = master
        self.master.title("Trainspotting")
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.game = game
        self.game_entities = []
        self.buttons = []

        # Main Frame
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill="both", expand=True)

        # Canvas on the left
        self.canvas = tk.Canvas(
            self.main_frame,
            width = Constants.UI_WIDTH - Constants.UI_SIDEBAR_MARGIN,
            height = Constants.UI_HEIGHT,
            bg = "whitesmoke"
        )
        self.canvas.pack(side="left", fill="both", expand=True)

        # UI panel on the right
        self.ui_frame = tk.Frame(self.main_frame, width = Constants.UI_SIDEBAR_MARGIN)
        self.ui_frame.pack(side="right", fill="y")
        self.ui_frame.pack_propagate(False)

        tk.Label(self.ui_frame, text="UI Panel").pack(pady=(10, 0))

        self.paint_field(0)
        self.canvas.bind("<Button-1>", self.handle_left_click)


    def paint_field(self, fps):
        """
        Repaints the window for every frame
        :param fps: int - Frames per second calculated inside the game loop
        :return: None
        """
        # Clear previous frame
        for item in self.game_entities:
            self.canvas.delete(item)
        self.game_entities.clear()

        # Draw FPS string
        fps_str = self.canvas.create_text(20, 20, text = f"TPS: {fps:.2f}", anchor = "w")
        self.game_entities.append(fps_str)

        # Draw stations
        for sta in self.game.stations:
            x, y = sta.position
            if sta == self.game.selection:
                dot = self.canvas.create_oval(
                    x - Constants.UI_STATION_RADIUS, y - Constants.UI_STATION_RADIUS,
                    x + Constants.UI_STATION_RADIUS, y + Constants.UI_STATION_RADIUS,
                    fill="lightgray", outline="gray", width=3
                )
            else:
                dot = self.canvas.create_oval(
                    x - Constants.UI_STATION_RADIUS, y - Constants.UI_STATION_RADIUS,
                    x + Constants.UI_STATION_RADIUS, y + Constants.UI_STATION_RADIUS,
                    fill="gray", outline="black", width=1
                )
            lab = self.canvas.create_text(x, y, text = sta.cargo_type)
            self.game_entities.append(dot)
            self.game_entities.append(lab)

        # Handle Selection
        if self.game.selection:
            if type(self.game.selection) == Station: # TODO: possible without importing station?
                self.draw_station_ui(self.game.selection)
            else:
                self.draw_line_ui(self.game.selection)


    def draw_station_ui(self, sta):
        """
        Called when a station is selected. Adds buttons for the available lines to build.
        :param sta: station - selected item from main game
        :return: None
        """



    def connect_line(self, lin, sta):
        """
        Starts the track building process
        :param lin: int - line id for the track to connect with
        :param sta: Station - station to connect the line to
        :return: None
        """
        pass


    def draw_line_ui(self, trk):
        """
        Called when a track is selected. Adds button to destroy if available
        :param trk: Line.Track - selected track
        :return: None
        """
        # Clear previous buttons
        for item in self.buttons:
            self.canvas.delete(item)
        self.buttons.clear()

        # Add Line destruction button
        btn = tk.Button(
            self.ui_frame,
            text = "Demolish track",
            command = lambda: self.demolish_track(trk)
        )
        self.buttons.append(btn)


    def demolish_track(self, trk):
        """
        Destroys the selected track and disconnects it from the network
        :param trk: Line.Track - selected track
        :return: None
        """
        # TODO: Implement
        pass


    def handle_left_click(self, event):
        """
        Mainly handles the selection of game entities
        :param event: mouse event
        :return: None
        """
        self.game.selection = self.game.get_clicked_station(event.x, event.y)
        self.selection_changed()


    def selection_changed(self):

        sel = self.game.selection

        # Clear previous buttons
        for item in self.buttons:
            item.destroy()
        self.buttons.clear()

        if not sel:
            return
        elif type(sel) == Station:
            # Add buttons to build lines
            for lin in self.game.get_available_lines(sel):
                btn = tk.Button(
                    self.ui_frame,
                    text=f"Line {lin}",
                    command=lambda: self.connect_line(lin, sel),
                    bg=Constants.LINE_COLOR[lin]
                )

                btn.pack(side="top", fill="both", expand=True)
                self.buttons.append(btn)
        #elif type(sel) == Line.Track


    def on_close(self):
        """
        Stops the game when the window is closed
        :return: None
        """
        self.game.running = False

        self.master.destroy()


def create_ui(game):
    """
    Creates a UI class
    :param game: main game
    :return: AppUI
    """
    root = tk.Tk()
    app = TrainspottingAppUI(root, game)
    return app
