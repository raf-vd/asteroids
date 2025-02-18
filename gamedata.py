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
        try:
            with open(self.filename, "w") as file:
                json.dump(self.settings, file, indent=4)
        except: 
            print("Something went wrong while saving settings, changes to settings were not saved")
    
    def get(self, key):
        return self.settings.get(key)
    
    def set(self, key, value):
        self.settings[key] = value    

    def load_default_settings(self):
        settings.set("master volume", 0.9)
        settings.set("sounds volume", 1.0)
        settings.set("music volume", 1.0)


# # Define some functionality & variables in the module itself to create independant module
def resource_path(relative_path):
    """ Get absolute path to resource; works for development and PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

ini_file = resource_path("data/asteroids.ini")                                  # Settings file
settings = GameData(ini_file)                                                   # Dict holding game settings
settings.load_from_file()                                                       # Read values



# settings = GameData(ini_file)
# settings.load_from_file()
# settings.set("master volume", 0.9)
# settings.set("sounds volume", 1.0)
# settings.set("music volume", 1.0)
# settings.save_to_file()

# print(settings.settings)