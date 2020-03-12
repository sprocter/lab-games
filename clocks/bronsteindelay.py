from clocks.delayclock import DelayClock


class BronsteinDelay(DelayClock):
    delay = 0
    starting_clock = 5

    def __init__(self, player_count=0, player_names=None, delay_amount=30, starting_clock=5):
        super().__init__(player_count=player_count, player_names=player_names,
                         delay_amount=delay_amount, starting_clock=starting_clock)
        self.starting_clock = starting_clock

    def next_player(self):
        # Get turn length, and then remove it from the clock, or add extra
        turn_length = self.get_turn_length() - self.delay

        # if the turn length is negative (still delay left) this has the effect of adding it to the bank.
        self.clock[self.current_player] -= turn_length

        # Check to see if clock is above the starting value
        if self.clock[self.current_player] > (self.starting_clock * 60):
            self.clock[self.current_player] = self.starting_clock * 60

        # Do the standard next player things
        super().next_player()

    def previous_player(self):
        # Get turn length, and then remove it from the clock, or add extra
        turn_length = self.get_turn_length() - self.delay

        # if the turn length is negative (still delay left) this has the effect of adding it to the bank.
        self.clock[self.current_player] -= turn_length

        # Check to see if clock is above the starting value
        if self.clock[self.current_player] > (self.starting_clock * 60):
            self.clock[self.current_player] = self.starting_clock * 60

        # Do the standard previous player things
        super().previous_player()