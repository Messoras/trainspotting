class Line:
    def __init__(self, color_code: str):
        self.color = color_code
        self.stations: list['Station'] = [] 
        self.trains: list['Train'] = []

    def add_station(self, station: 'Station', at_beginning: bool = False):
        """
        Fügt eine Station zur Linie hinzu.
        """
        if self.stations:
            if at_beginning and self.stations[0] == station:
                return
            if not at_beginning and self.stations[-1] == station:
                return

        if at_beginning:
            self.stations.insert(0, station)
        else:
            self.stations.append(station)

    def remove_station(self, station: 'Station'):
        """Entfernt eine Station aus der Linie."""
        if station in self.stations:
            self.stations.remove(station)

    def is_valid_drag_point(self, station: 'Station') -> bool:
        """
        Prüft, ob der User von diesem Bahnhof aus die Linie weiterziehen darf.
        Regel: Nur an den offenen Enden (Start oder Ende) darf gezogen werden.
        """
        if not self.stations:
            return True

        if station not in self.stations:
            return False

        is_start = (station == self.stations[0])
        is_end = (station == self.stations[-1])

        return is_start or is_end

    def can_connect_to(self, from_station: 'Station', to_station: 'Station') -> bool:
        """
        Prüft, ob eine Verbindung zum Zielbahnhof erlaubt ist.
        """
        if from_station == to_station:
            return False

        if to_station in self.stations:
            return False

        return True

    def shap_checker(self, shape_type: str) -> bool:
        """
        Prüft, ob diese Linie einen Bahnhof mit der gewünschten Form anfährt.
        Der Zug nutzt das, um zu entscheiden, ob Passagiere einsteigen dürfen.
        """
        for station in self.stations:
            if hasattr(station, 'shape_type') and station.shape_type == shape_type:
                return True
        return False

    def get_next_stop(self, current_station: 'Station', current_direction: int) -> tuple['Station', int]:
        """
        current_direction: 1 (vorwärts) oder -1 (rückwärts)
        # Szenario A: Ende der Linie erreicht
        # Szenario B: Anfang der Linie erreicht
        # Szenario C: Normale keep steaming bro
        """
        try:
            index = self.stations.index(current_station)
        except ValueError:
            return current_station, 0

        next_index = index + current_direction

        
        if next_index >= len(self.stations):
            if len(self.stations) > 1:
                return self.stations[-2], -1
            else:
                return current_station, 0
        
        elif next_index < 0:
            if len(self.stations) > 1:
                return self.stations[1], 1
            else:
                return current_station, 0
            
        else:
            return self.stations[next_index], current_direction