import tkinter as tk

import Constants
from Station import Station


class TrainspottingAppUI:
    """
    UI class to manage display of and interaction with the main game
    """
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
        self.game_over_screen_shown = False
        self.cargo_images = {}
        self.cargo_images_small = {}
        for cargo_type, image_path in Constants.CARGO_TYPE_TO_IMAGE.items():
            image = tk.PhotoImage(file=image_path)
            self.cargo_images[cargo_type] = image.subsample(24)
            self.cargo_images_small[cargo_type] = image.subsample(32)
        self.train_image = tk.PhotoImage(file="img/chocho.png").subsample(6)
        self.train_images = {
            "red": tk.PhotoImage(file="img/chocho_red.png").subsample(6),
            "blue": tk.PhotoImage(file="img/chocho_blue.png").subsample(6),
            "yellow": tk.PhotoImage(file="img/chocho_yellow.png").subsample(6),
        }
        self.daisy_image = tk.PhotoImage(file=Constants.DAISY_PATH).subsample(2)

        # Main Frame
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill="both", expand=True)

        # Canvas on the left
        self.canvas = tk.Canvas(
            self.main_frame,
            width=Constants.UI_WIDTH - Constants.UI_SIDEBAR_MARGIN,
            height=Constants.UI_HEIGHT,
            bg="whitesmoke"
        )
        self.canvas.pack(side="left", fill="both", expand=True)

        # UI panel on the right
        self.ui_frame = tk.Frame(self.main_frame, width=Constants.UI_SIDEBAR_MARGIN)
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
        if self.game.game_over:
            if not self.game_over_screen_shown:
                self.show_game_over_screen()
            return

        # Clear previous frame
        for item in self.game_entities:
            self.canvas.delete(item)
        self.game_entities.clear()

        # Draw FPS string
        fps_str = self.canvas.create_text(20, 20, text=f"TPS: {fps:.2f}", anchor="w")
        self.game_entities.append(fps_str)

        # Draw Score
        score_text = self.canvas.create_text(1000, 20, text = f"Score: {self.game.score}")
        self.game_entities.append(score_text)

        # Draw Money
        money_text = self.canvas.create_text(1000, 40, text=f"Money: {self.game.money:.2f}")
        self.game_entities.append(money_text)

        # Draw building info
        if self.building_line:
            info_text = self.canvas.create_text(20, 50, text=f"Currently building line {self.building_line[0]}", anchor="w")
            self.game_entities.append(info_text)

        # Draw tracks
        line_iter = 0
        for line in self.game.lines:
            trk_iter = 0
            for trk in line.tracks:
                ln = self.canvas.create_line(
                    trk[0].position[0], trk[0].position[1],
                    trk[1].position[0], trk[1].position[1],
                    fill=line.color,
                    width=5,
                    tags=f"{line_iter},{trk_iter}"
                )
                self.game_entities.append(ln)
                if (type(self.game.selection) == tuple and
                        trk == self.game.selection[0].tracks[self.game.selection[1]]):
                    # selected
                    highlight = self.canvas.create_line(
                        trk[0].position[0], trk[0].position[1],
                        trk[1].position[0], trk[1].position[1],
                        fill="white",
                        width=2
                    )
                    self.game_entities.append(highlight)
                trk_iter += 1
            line_iter += 1

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

                # Draw cargo (in stations)
                for i in range(len(sta.cargo_load)):
                    crg = sta.cargo_load[i]
                    crg_x = x + Constants.UI_STATION_RADIUS + 20 + (i % 3) * 20
                    crg_y = y - Constants.UI_STATION_RADIUS + (i // 3) * 20
                    if crg.elimination_timer < 500 and (self.game.tick_counter // Constants.FLICKER_DURATION) % 2 == 0:
                        x1 = crg_x - self.cargo_images_small[crg.cargo_type].width() // 2 - 3
                        y1 = crg_y - self.cargo_images_small[crg.cargo_type].height() // 2 - 3
                        x2 = crg_x + self.cargo_images_small[crg.cargo_type].width() // 2 + 4
                        y2 = crg_y + self.cargo_images_small[crg.cargo_type].height() // 2 + 4
                        warn = self.canvas.create_oval(
                            x1,y1,x2,y2,
                            fill = "red"
                        )
                        self.game_entities.append(warn)
                    img = self.canvas.create_image(
                        crg_x,
                        crg_y,
                        image=self.cargo_images_small[crg.cargo_type]
                    )
                    self.game_entities.append(img)


        for line in self.game.lines:
            # Draw trains
            for trn in line.trains:
                x, y = trn.position
                train_img = self.train_images.get(line.color, self.train_image)
                img = self.canvas.create_image(x, y, image=train_img)
                self.game_entities.append(img)

                # Draw Cargo (in trains)
                for i in range(len(trn.cargo_load)):
                    crg = trn.cargo_load[i]
                    crg_x = x + 24 + (i % 3) * 20
                    crg_y = y - 8 + (i // 3) * 20
                    if crg.elimination_timer < 500 and (self.game.tick_counter // Constants.FLICKER_DURATION) % 2 == 0:
                        x1 = crg_x - self.cargo_images_small[crg.cargo_type].width() // 2 - 3
                        y1 = crg_y - self.cargo_images_small[crg.cargo_type].height() // 2 - 3
                        x2 = crg_x + self.cargo_images_small[crg.cargo_type].width() // 2 + 4
                        y2 = crg_y + self.cargo_images_small[crg.cargo_type].height() // 2 + 4
                        warn = self.canvas.create_oval(
                            x1,y1,x2,y2,
                            fill = "red"
                        )
                        self.game_entities.append(warn)
                    crg = trn.cargo_load[i]
                    img = self.canvas.create_image(
                        crg_x,
                        crg_y,
                        image=self.cargo_images_small[crg.cargo_type]
                    )
                    self.game_entities.append(img)

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
            except Exception as ex:
                # Found picture or something else
                # print(ex)
                continue
        return None

    def draw_station_ui(self, sel):
        """
        Called when a station is selected. Adds buttons for the available lines to build.
        :param sel: station - selected item from main game
        :return: None
        """
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
                    command=lambda ln=line, st=sel: self.buy_train(ln, st),
                    bg=line.color
                )
                btn.pack(side="top", fill="x", pady=2)
                self.buttons.append(btn)

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
        # Clear previous buttons is handled in selection_changed()

        # Add Line destruction button
        btn = tk.Button(
            self.ui_frame,
            text="Demolish track",
            command=lambda lin = trk[0], track = trk[1]: self.demolish_track(lin,track)
        )

        if trk[0].can_delete_track(trk[1]):
            btn.pack(side="top", fill="x", pady=2)
            self.buttons.append(btn)

    def demolish_track(self,lin,track_id):
        lin.demolish_track(track_id)
        self.game.selection = None
        self.selection_changed()

    def handle_left_click(self, event):
        """
        Mainly handles the selection of game entities
        :param event: mouse event
        :return: None
        """
        sel = self.game.get_clicked_station(event.x, event.y)

        if self.building_line:
            line_id, start_sta = self.building_line
            if sel and sel != start_sta:
                # Connect selection and start station
                self.game.buy_line(self.game.lines[line_id], start_sta, sel)
                self.game.selection = sel
                self.building_line = None
                self.selection_changed()
            else:
                self.building_line = None
                self.game.selection = sel
                self.selection_changed()
            return

        self.game.selection = sel
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
            self.draw_station_ui(self.game.selection)

        elif type(sel) == tuple:
            self.draw_line_ui(self.game.selection)

    def buy_train(self, line, station):
        """
        Adds a train to the specified line, currently only works once
        :param line: line to add the train to
        :param station: station where the train is bought
        :return: None
        """
        self.game.buy_train(line, station)

    def on_close(self):
        """
        Stops the game when the window is closed
        :return: None
        """
        self.game.running = False

        self.master.destroy()

    def show_game_over_screen(self):
        self.game_over_screen_shown = True
        self.selection_changed()  # clear UI
        for item in self.game_entities:
            self.canvas.delete(item)
        self.game_entities.clear()

        # Draw LOSS Screen
        loss_cube = self.canvas.create_rectangle(
            0, 0,
            Constants.UI_WIDTH - Constants.UI_SIDEBAR_MARGIN, Constants.UI_HEIGHT,
            fill="black",
            stipple="gray75"
        )
        self.game_entities.append(loss_cube)
        daisy = self.canvas.create_image(400,400,image = self.daisy_image)
        self.game_entities.append(daisy)
        loss_text = self.canvas.create_text(
            (Constants.UI_WIDTH - Constants.UI_SIDEBAR_MARGIN) // 2, Constants.UI_HEIGHT // 2 - 100,
            text="You lost!",
            anchor="n",
            font=("Arial", 36, "bold"),
            fill="red"
        )
        self.game_entities.append(loss_text)
        info_text = self.canvas.create_text(
            (Constants.UI_WIDTH - Constants.UI_SIDEBAR_MARGIN) // 2, Constants.UI_HEIGHT // 2 - 20,
            text=f"You didn't deliver the cargo in time. \nYour score: {self.game.score}",
            anchor="n",
            font=("Arial", 16),
            fill="white"
        )
        self.game_entities.append(info_text)

        # Name Entry
        name_label = tk.Label(self.canvas, text="Enter your name:", font=("Arial", 12), bg="black", fg="white")
        name_label_window = self.canvas.create_window(
            (Constants.UI_WIDTH - Constants.UI_SIDEBAR_MARGIN) // 2, Constants.UI_HEIGHT // 2 + 100,
            anchor="s", window=name_label
        )
        self.game_entities.append(name_label_window)

        name_entry = tk.Entry(self.canvas, font=("Arial", 12))
        name_entry_window = self.canvas.create_window(
            (Constants.UI_WIDTH - Constants.UI_SIDEBAR_MARGIN) // 2, Constants.UI_HEIGHT // 2 + 100,
            anchor="n", window=name_entry
        )
        self.game_entities.append(name_entry_window)

        submit_button = tk.Button(
            self.canvas, text="Submit", font=("Arial", 12),
            command=lambda: self.submit_score(name_entry.get())
        )
        submit_button_window = self.canvas.create_window(
            (Constants.UI_WIDTH - Constants.UI_SIDEBAR_MARGIN) // 2, Constants.UI_HEIGHT // 2 + 130,
            anchor="n", window=submit_button
        )
        self.game_entities.append(submit_button_window)

    def submit_score(self, name):
        if name:
            self.game.add_player_score(name)
        self.show_scoreboard()

    def show_scoreboard(self):
        for item in self.game_entities:
            self.canvas.delete(item)
        self.game_entities.clear()

        # Draw Scoreboard Screen
        bg = self.canvas.create_rectangle(
            0, 0,
            Constants.UI_WIDTH - Constants.UI_SIDEBAR_MARGIN, Constants.UI_HEIGHT,
            fill="black"
        )
        self.game_entities.append(bg)

        title_text = self.canvas.create_text(
            (Constants.UI_WIDTH - Constants.UI_SIDEBAR_MARGIN) // 2, 50,
            text="Scoreboard",
            anchor="n",
            font=("Arial", 36, "bold"),
            fill="white"
        )
        self.game_entities.append(title_text)

        scores = self.game.scoreboard.get_scores()
        y_pos = 150
        for i, entry in enumerate(scores):
            score_text = f"{i + 1}. {entry['name']}: {entry['score']}"
            self.canvas.create_text(
                (Constants.UI_WIDTH - Constants.UI_SIDEBAR_MARGIN) // 2, y_pos,
                text=score_text,
                anchor="n",
                font=("Arial", 16),
                fill="white"
            )
            y_pos += 30

        close_button = tk.Button(
            self.canvas, text="Close", font=("Arial", 12),
            command=self.on_close
        )
        close_button_window = self.canvas.create_window(
            (Constants.UI_WIDTH - Constants.UI_SIDEBAR_MARGIN) // 2, y_pos + 50,
            anchor="n", window=close_button
        )
        self.game_entities.append(close_button_window)



def create_ui(game):
    """
    Creates a UI class
    :param game: main game
    :return: AppUI
    """
    root = tk.Tk()
    app = TrainspottingAppUI(root, game)
    return app
