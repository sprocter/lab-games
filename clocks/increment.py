from clocks.clock import Clock


class Increment(Clock):
    increment = 0  # Stores the amount to increment the player's clocks by

    def __init__(self, player_count=0, player_names=None, increment_amount=30, starting_clock=5):
        super().__init__(player_count=player_count, player_names=player_names)

        self.clock = [int(starting_clock * 60) for _ in range(self.player_count+1)]
        self.increment = increment_amount
        self.clock[self.current_player] += self.increment  # One time increase to first players clock

    def next_player(self):
        # Get turn length, and then subtract it from the clock
        turn_length = self.get_turn_length()
        self.clock[self.current_player] -= turn_length

        # Do the standard next player things
        super().next_player()

        # Add the increment to this next player's clock
        self.clock[self.current_player] += self.increment

    def previous_player(self):
        # Get turn length, and then subtract it from the clock
        turn_length = self.get_turn_length()
        self.clock[self.current_player] -= turn_length

        # Do the standard previous player things
        super().previous_player()

        # Do not give an increment when going to previous player?
