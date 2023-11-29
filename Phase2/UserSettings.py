class UserSettings:
    def __init__(self):
        self.brightness = None
        self.temperature = None
        self.card_id = None
        self.user_email = None
        self.load_default_values()

    def load_default_values(self):
        self.brightness = 400
        self.temperature = 24
        self.card_id = 0
        self.user_email = 'baduar10@gmail.com'


