import time

from clocks.clock import Clock


class SimpleDelay(Clock):
    delay = 0

    def __init__(self, player_count=0, player_names=None, delay_amount=30, starting_clock=5):
        super().__init__(player_count=player_count, player_names=player_names)

        self.clock = [int(starting_clock * 60) for i in range(self.player_count+1)]
        self.delay = delay_amount

    def next_player(self):
        # Get turn length, and then remove it from the clock
        turn_length = self.get_turn_length() - self.delay
        if turn_length > 0:
            self.clock[self.current_player] -= turn_length

        # Do the standard next player things
        super().next_player()

    def previous_player(self):
        # Get turn length, and then remove it from the clock
        turn_length = self.get_turn_length() - self.delay
        if turn_length > 0:
            self.clock[self.current_player] -= turn_length

        # Do the standard previous player things
        super().previous_player()

    def get_total_time(self):
        turn_length = self.get_turn_length()
        delay_remaining = 0 if turn_length > self.delay else self.delay - turn_length
        if delay_remaining > 0:
            total_time = self.get_clock_time()
        else:
            total_time = self.get_clock_time() - (self.get_turn_length() - self.delay)
        if total_time <= 0:
            self.clock[self.current_player] = 0
            return 0
        else:
            return total_time
