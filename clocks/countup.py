import time

from clocks.clock import Clock


class CountUp(Clock):
    def __init__(self, player_count=0, player_names=None):
        super().__init__(player_count=player_count, player_names=player_names)

        self.clock = [0 for i in range(self.player_count+1)]

    def next_player(self):
        # Get turn length, and then add it to the clock
        turn_length = self.get_turn_length()
        self.clock[self.current_player] += turn_length

        # Do the standard next player things
        super().next_player()

    def previous_player(self):
        # Get turn length, and then add it to the clock
        turn_length = self.get_turn_length()
        self.clock[self.current_player] += turn_length

        # Do the standard previous player things
        super().previous_player()

    def get_total_time(self):
        total_time = self.get_clock_time() + self.get_turn_length()
        return 0 if total_time <= 0 else total_time
