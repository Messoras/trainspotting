import tkinter as tk

import Constants
from Station import Station

class TrainspottingAppUI:
    def __init__(self, master, game):
        self.master = master
        self.master.title("Trainspotting")
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.game = game
        self.game_entities = []

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

        tk.Label(self.ui_frame, text="").pack(pady=(10, 0))

        self.paint_field(0)
        self.canvas.bind("<Button-1>", self.handle_left_click)


    def paint_field(self, fps):
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
        pass


    def draw_line_ui(self, lin):
        pass


    def handle_left_click(self, event):
        self.game.selection = self.game.get_clicked_station(event.x, event.y)


    def on_close(self):
        self.game.running = False

        self.master.destroy()


def create_ui(game):
    root = tk.Tk()
    app = TrainspottingAppUI(root, game)
    return app
