class MyPlayer:
    def __init__(self, bot, name, player_idx):
        self.bot = bot
        self.name = name
        self.pos_x = 0
        self.pos_y = 0
        self.player_idx = player_idx
        self.start = False
        self.rounds_dead = 0

    def set_position(self, pos):
        self.pos_x = pos[0]
        self.pos_y = pos[1]

    def get_position(self):
        return [self.pos_x, self.pos_y]

    def get_name(self):
        return self.name

    def is_bot(self):
        return self.bot

    # This function returns True if the current player has made their first move
    def get_start(self):
        return self.start

    def set_start(self):
        self.start = True

    def get_player_idx(self):
        return self.player_idx

    def update_rounds_dead(self):
        self.rounds_dead += 1

    def get_rounds_dead(self):
        return self.rounds_dead