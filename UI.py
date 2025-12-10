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
        self.building_line = None
        self.cargo_images = {}
        for cargo_type, image_path in Constants.CARGO_TYPE_TO_IMAGE.items():
            image = tk.PhotoImage(file=image_path)
            self.cargo_images[cargo_type] = image.subsample(17, 17)

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
            lab = self.canvas.create_image(x, y, image=self.cargo_images[sta.cargo_type])
            self.game_entities.append(dot)
            self.game_entities.append(lab)

            for i in range(len(sta.cargo_load)):
                crg = sta.cargo_load[i]
                img = self.canvas.create_image(
                    x + Constants.UI_STATION_RADIUS + 10 + (i % 3) * 20,
                    y - Constants.UI_STATION_RADIUS + 10 + (i // 3) * 20,
                    image=self.cargo_images[crg.cargo_type]
                )
                self.game_entities.append(img)


        # Draw tracks
        line_iter = 0
        for line in self.game.lines:
            trk_iter = 0
            for trk in line.tracks:
                ln = self.canvas.create_line(
                    trk[0].position[0], trk[0].position[1],
                    trk[1].position[0], trk[1].position[1],
                    fill = line.color,
                    width = 5,
                    tags = f"{line_iter},{trk_iter}"
                )
                self.game_entities.append(ln)
                if (type(self.game.selection) == tuple and
                        trk == self.game.selection[0].tracks[self.game.selection[1]]):
                    # selected
                    highlight = self.canvas.create_line(
                        trk[0].position[0], trk[0].position[1],
                        trk[1].position[0], trk[1].position[1],
                        fill = "white",
                        width = 2
                    )
                    self.game_entities.append(highlight)
                trk_iter += 1

            # Draw trains (in line)
            for trn in line.trains:
                x, y = trn.position
                # TODO: Use image instead of rectangle
                rect = self.canvas.create_rectangle(
                    x - 12, y - 12,
                    x + 12, y + 12,
                    fill = Constants.LINE_COLOR[line_iter]
                )
                self.game_entities.append(rect)

                # Draw Cargo (in trains)
                for i in range(len(trn.cargo_load)):
                    crg = trn.cargo_load[i]
                    img = self.canvas.create_image(
                        x - 8 + (i % 3) * 10,
                        y - 8 + (i // 3) * 10,
                        image=self.cargo_images[crg.cargo_type]
                    )
                    self.game_entities.append(img)

            line_iter += 1

        # Handle Selection
        if self.game.selection:
            if type(self.game.selection) == Station: # TODO: possible without importing station?
                self.draw_station_ui(self.game.selection)
            elif type(self.game.selection) == tuple:
                self.draw_line_ui(self.game.selection)


    def find_track_at(self, x, y):
        """
        looks for tracks at the given position
        :param x: x position
        :param y: y position
        :return: Tuple['Line','int'] - Line that owns given track and its index
        """
        overlap = self.canvas.find_overlapping(x - 2, y - 2, x + 2, y + 2)
        for item in overlap:
            tags = self.canvas.gettags(item)
            # print(f"Checking item with tags: {tags}")
            try:
                strarr = tags[0].split(",")
                return self.game.lines[int(strarr[0])], int(strarr[1])
            except IndexError:
                print("!!! This is a mother fucking invtervention !!!")
                continue
        return None


    def draw_station_ui(self, sta):
        """
        Called when a station is selected. Adds buttons for the available lines to build.
        :param sta: station - selected item from main game
        :return: None
        """



    def connect_line(self, lin_id, sta):
        """
        Starts the track building process
        :param lin_id: int - line id for the track to connect with
        :param sta: Station - station to connect the line to
        :return: None
        """
        self.building_line = (lin_id, sta)


    def draw_line_ui(self, trk):
        """
        Called when a track is selected. Adds button to destroy if available
        :param trk: Line.Track - selected track
        :return: None
        """
        # Clear previous buttons
        for item in self.buttons:
            item.destroy()
        self.buttons.clear()

        # Add Line destruction button
        btn = tk.Button(
            self.ui_frame,
            text = "Demolish track",
            command = lambda: self.demolish_track(trk)
        )
        btn.pack(side="top", fill="x", pady=2)
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
        if self.building_line:
            line_id = self.building_line[0]
            start_sta = self.building_line[1]
            sel = self.game.get_clicked_station(event.x, event.y)
            if sel:
                print(self.building_line)
                # Connect selection and start station
                if len(self.game.lines[line_id].stations) == 0:
                    self.game.lines[line_id].add_station(start_sta)
                self.game.lines[line_id].add_station(
                    sel,
                    len(self.game.lines[line_id].tracks) == 0 or
                    start_sta == self.game.lines[line_id].stations[0]
                )
                self.building_line = None
                self.game.selection = None
                self.selection_changed()
                return

        self.game.selection = self.game.get_clicked_station(event.x, event.y)
        if not self.game.selection:
            self.game.selection = self.find_track_at(event.x, event.y)
        self.selection_changed()


    def selection_changed(self):
        """
        Handles the change of selection object after clicking on the game panel
        and initializes the correct UI
        :return: None
        """
        sel = self.game.selection

        # Clear previous buttons
        for item in self.buttons:
            item.destroy()
        self.buttons.clear()

        # Clear highlighted line
        for item in self.game_entities:
            if "highlight" in self.canvas.gettags(item):
                self.canvas.delete(item)

        if not sel:
            return

        elif type(sel) == Station:
            # Add buttons to build lines
            for lin in self.game.get_available_lines(sel):
                btn = tk.Button(
                    self.ui_frame,
                    text=f"Line {lin}",
                    command=lambda l_id=lin: self.connect_line(l_id, sel),
                    bg=Constants.LINE_COLOR[lin]
                )
                btn.pack(side="top", fill="x", pady=2)
                self.buttons.append(btn)


            for line in self.game.lines:
                if sel in line.stations and len(line.stations) >= 2:
                    btn = tk.Button(
                        self.ui_frame,
                        text=f"Buy Train for Line {line.id}",
                        command=lambda ln = line: self.buy_train(ln),
                        bg=line.color
                    )
                    btn.pack(side="top", fill="x", pady=2)
                    self.buttons.append(btn)

    def buy_train(self, line):
        self.game.buy_train(line)


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
