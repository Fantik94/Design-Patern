class GameManager:
    _instance = None

    @staticmethod
    def get_instance():
        if GameManager._instance is None:
            GameManager()
        return GameManager._instance

    @staticmethod
    def reset_instance():
        GameManager._instance = None

    def __init__(self):
        if GameManager._instance is not None:
            raise Exception("singleton")
        else:
            GameManager._instance = self
            self.characters = []
            self.battle_history = []
            self.current_round = 0

    def add_character(self, character):
        self.characters.append(character)

    def add_battle_history(self, record):
        self.battle_history.append(record)

    def next_round(self):
        self.current_round += 1

    def get_state(self):
        return {
            'characters': self.characters,
            'battle_history': self.battle_history,
            'current_round': self.current_round
        }
