import time

from clocks.clock import Clock


class Hourglass(Clock):
    def __init__(self, starting_clock=2, player_names=None):
        if len(player_names) > 2:
            player_names = player_names[:2]
        super().__init__(player_count=2, player_names=player_names)

        self.clock = [int(starting_clock * 60) for i in range(self.player_count+1)]

    def next_player(self):
        # Get turn length, and then add it to the clock
        turn_length = self.get_turn_length()
        self.clock[self.current_player] -= turn_length
        self.clock[self.get_next_player()] += turn_length

        # Do the standard next player things
        super().next_player()

    def previous_player(self):
        # Get turn length, and then add it to the clock
        turn_length = self.get_turn_length()
        self.clock[self.current_player] -= turn_length
        self.clock[self.get_next_player()] += turn_length

        # Do the standard previous player things
        super().previous_player()
