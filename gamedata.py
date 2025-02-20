import json, os, sys

class GameData():
    def __init__(self, filename):
        self.filename = filename
        self.settings = {}
    
    def load_from_file(self):         
        try:
            with open(self.filename, "r") as file:
                self.settings  = json.load(file)
        except FileNotFoundError:
            self.load_default_settings()
    
    def save_to_file(self):
        self.sort_if_needed()
        try:
            with open(self.filename, "w") as file:
                json.dump(self.settings, file, indent=4)
        except: 
            print("Something went wrong while saving settings, changes to settings were not saved")
    
    def sort_if_needed(self):
        if self.filename.find("highscores.dat") >= 0:                               # Sort dict and limit to 5 entries when a highscores dict
            sorted_items = sorted(self.settings.items(), key=lambda item: item[1], reverse=True)
            self.settings = dict(sorted_items[:5])

    def get(self, key):
        return self.settings.get(key)
    
    def set(self, key, value):
        self.settings[key] = value    

    def load_default_settings(self):
        if self.filename.find("asteroids.ini") >= 0:                                # Load default settings if standard inifile failed to load
            self.set("master volume", 0.9)
            self.set("sounds volume", 1.0)
            self.set("music volume", 1.0)
        if self.filename.find("highscores.dat") >= 0:                               # Load default settings if standard highscoresfile failed to load            
            self.set("AAA AA", 10000)
            self.set("BBB BB", 5000)
            self.set("CCC CC", 3500)
            self.set("DDD DD", 2500)
            self.set("EEE EE", 2000)
        return

# # Define some functionality & variables in the module itself to create independant module
def resource_path(relative_path):
    """ Get absolute path to resource; works for development and PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

ini_file = resource_path("data/asteroids.ini")                                  # Settings file
highscores_file = resource_path("data/highscores.dat")                          # Highscores file
settings = GameData(ini_file)                                                   # Dict holding game settings
settings.load_from_file()                                                       # Read values
highscores = GameData(highscores_file)                                          # Dict holding highscore data
highscores.load_from_file()
