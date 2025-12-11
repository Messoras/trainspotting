# trainspotting
Train Management App in Python

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

Some functions are only called once after a set amount of ticks:

- Initialization: Generating the starting field and spawning some stations with set types
- (unlocking new updates / buy options)

### TODO:

- Increasing the amount of trolleys per train
- Graphics
- Bug fixing:
  * all fine for now