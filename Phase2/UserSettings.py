class UserSettings:
    def __init__(self):
        self.brightness = None
        self.temperature = None
        self.load_default_values()

    def load_default_values(self):
        self.brightness = 400
        self.temperature = 24


