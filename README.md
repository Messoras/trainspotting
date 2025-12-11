# trainspotting
**A Train Management Simulation App in Python**

This project simulates the cargo transportation between train stations. The aim of the game is to transport as much cargo as possible while using minimal resources.
To start the program, run the maingame.py script.

### Structure

- **Stations:**  
    _Cargo spawns here and needs to be delivered to another station with fitting cargo type_
- **Lines:**  
    _There are multiple lines, differentiated by their color coding, they are used to connect stations_
  - **Tracks:**  
      _Individual connection peaces connecting two stations_
  - **Trains:**  
      _These follow the chain of tracks to its end (or follow the loop) and pick up and deploy cargo_
- **Cargo:**  
    _Can be picked up or deployed by trains at stations. Grants score (and money) when deployed, but causes a game loss when left alone for to long_

### Game Loop

A loop is running to call the tick-function every few milliseconds.
Each tick a few different things are triggered:
- Cargo is ticked (to catch a losing condition, when the cargo is left on the board for to long)
- Lines are ticked (to tick their trains to make them move and handle cargo)

Some functions are only called after a set amount of ticks (repeatedly):

- Spawning cargo (each station spawns a single piece of cargo that doesn't match its own cargo type) - short delay
- Spawning new stations - medium delay
- increasing the amount of different cargo types - long delay

Some functions are only called once after a set amount of ticks (or after reaching a given score):

- Initialization: Generating the starting field and spawning some stations with set types
- (unlocking new updates / buy options)

A victory condition is not apparent. You play as long as you can and enjoy and collect score.
The score incrementation is handed to train elements as callback upon creation by the main game.
This can be triggered by the train when it deploys cargo.  
A losing condition is handed to all cargo elements as callback upon creation by the main game.
This can be triggered by the Cargo element as soon as it reaches a certain age without being delivered.

### UI

The UI is responsible for displaying the game state and interacting with its elements.
It includes methods to display the following game elements (using tkinter):

- Stations: as circle with icon for the cargo type
- Trains: as image
- Lines/Tracks: as colored line elements
- Cargo: as image (attached to trains and/or stations)
- Highscore: as string
- Info about activity (building): as string (probably better as line)

The following interactions are provided by the UI by handling clicks on the corresponding panel:

- Opening station UI: (game panel) - click on a station element
- Opening track UI: (game panel) - click on a track element
- Closing UI: (game panel) - click on open space
- Building new track: (station UI panel) - line buttons
- Demolishing track: (line UI panel) - demolish button

### Outlooks:

- Increasing the amount of trolleys per train
- Optimizing cargo loading/unloading criteria (cross line transport)
- Graphics enhancement (train rotation, improved UI, etc.)
- Semi-random station spawning (no overlaying stations...)
- Implementing money and building/buying costs