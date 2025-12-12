import json

SCOREBOARD_FILE = "scores.json"

class Scoreboard:
    """
    Handles the user scores to be displayed after each game
    """
    def __init__(self):
        self.scores = []
        self.load_scores()

    def load_scores(self):
        """Loads scores from the scoreboard file."""
        try:
            with open(SCOREBOARD_FILE, "r") as f:
                self.scores = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.scores = []

    def save_scores(self):
        """Saves scores to the scoreboard file."""
        with open(SCOREBOARD_FILE, "w") as f:
            json.dump(self.scores, f, indent=4)

    def add_score(self, name, score):
        """Adds a new score and saves it."""
        self.scores.append({"name": name, "score": score})
        # Sort scores descending
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        # Keep top 10
        self.scores = self.scores[:10]
        self.save_scores()

    def get_scores(self):
        """Returns the sorted list of scores."""
        return self.scores
