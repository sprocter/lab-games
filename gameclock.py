import time


class GameClock:
    """
    A tool for keeping track of a chess like clock for n number of players. The clock cycle works in a round robin
    format. When it becomes a players turn, they have `delay` seconds to complete their turn. Once that time is over,
    their turn starts counting against their `bank`. Once their bank is empty, it is uo to the other players to
    enforce a real life punishment (loss of turn, loss of game, removal from group, etc.). When the players turn is
    done, next is called to start the cycle over with the next player, with a new delay count and their old bank amount.
    """
    players = 0
    names = None
    delay = 0
    bank = []
    turn = 1
    current_player = 1
    start_time = 0
    state = "initialized"  # initialized, running, paused, ended
    state_amount = None

    def __init__(self, number_players, delay_amount=60, bank_amount=5, names=None):
        """
        Creates a Game Clock object with a set number of players.

        :param number_players: Required, the number of players in the game.
        :param delay_amount: The number of seconds of grace period each player gets before time is counted against them.
        :param bank_amount: The amount of time (in minutes) that each player has in this game that is not granted.
        :param names: A list strings containing the names of the players in this game.
        """
        if names:
            # Names were provided, so use them to create players
            self.names = names

            # Check if more names provided than players
            if len(self.names) > number_players:
                self.players = len(self.names)

        # Check if players initialized
        if self.players == 0:
            self.players = number_players

        self.delay = delay_amount
        self.bank = [int(bank_amount * 60) for i in range(number_players+1)]

    def start_player_turn(self):
        """
        Starts the game clock cycle.

        :return: None
        """
        self.state = "running"
        self.start_time = time.time()

    def get_turn_length(self):
        """
        Get the length of this turn.

        :return:
        """
        return int(time.time() - self.start_time)

    def update_bank(self):
        """
        Updates the bank by removing the amount of turn time that has passed.

        :return: None
        """
        turn_time = self.get_turn_length()

        # Remove it from the bank (only if it is more than the delay amount)
        self.bank[self.current_player] -= turn_time - self.delay if turn_time > self.delay else 0

        if self.bank[self.current_player] <= 0:
            self.bank[self.current_player] = 0

    def next_player(self):
        """
        Triggers the transition to the next player in the turn order.

        :return: None
        """
        self.update_bank()

        # Change to the next player, looping if at the end
        self.current_player = self.get_next()

        # Increment the turn timer
        if self.current_player == 1:
            self.turn += 1

        # Unpause if needed
        if self.state == "paused":
            self.state = "running"
            self.state_amount = None

        # Start the new time for the next player
        self.start_time = time.time()

    def previous_player(self):
        """
        Triggers the transition to the previous player in the turn order.

        :return: None
        """
        self.update_bank()

        # Change to the next player, looping if at the end
        self.current_player = self.get_previous()

        # Increment the turn timer
        if self.current_player == self.players:
            self.turn -= 1

        # Unpause if needed
        if self.state == "paused":
            self.state = "running"
            self.state_amount = None

        # Start the new time for the next player
        self.start_time = time.time()

    def pause_player_turn_toggle(self):
        """
        Pauses the clock, or resumes if the clock is already paused.

        :return: None
        """
        if self.state == "paused":
            # We are in the paused state, and are resuming
            self.start_time = time.time() - self.state_amount
            self.state_amount = None
            self.state = "running"
        else:
            # Save the amount of time that has elapsed
            turn_time = self.get_turn_length()
            self.state_amount = turn_time
            self.start_time = 0
            self.state = "paused"

    def end(self):
        """
        Ends the current clock.

        :return: None
        """
        # Need to unpause to get an accurate state
        if self.state == "paused":
            self.pause_player_turn_toggle()

        # Update the bank with the current turn
        self.update_bank()
        self.start_time = 0
        self.state = "ended"

    def get_remaining_time(self):
        """
        Get the amount of time left in this player's turn.

        :return: Delay and Bank time
        """
        turn_time = self.get_turn_length()

        if turn_time > self.delay:
            # Delay time is over
            delay = 0
            bank = self.bank[self.current_player] - (turn_time - self.delay)
        else:
            # Delay time is still going
            delay = self.delay - turn_time
            bank = self.bank[self.current_player]

        if bank <= 0:
            bank = 0

        return self.convert_to_formatted_time(delay), self.convert_to_formatted_time(bank)

    def get_player(self, player_id):
        """
        Gets the string name of the provided player.

        :param player_id: The id (an int) of the current player
        :return: A string either pulled from names, or as "Player x"
        """
        if self.names:
            try:
                return self.names[player_id - 1]
            except IndexError:
                pass
        return "Player " + str(player_id)

    def get_next(self):
        """
        Gets the next player.

        :return: The id of the next player.
        """
        return self.current_player + 1 if self.current_player < self.players else 1

    def get_previous(self):
        """
        Gets the previous player.

        :return: The id of the previous player.
        """
        return self.current_player - 1 if self.current_player > 0 else self.players

    def convert_to_formatted_time(self, seconds):
        """
        Converts an int into minutes and seconds.
        from: https://www.geeksforgeeks.org/python-program-to-convert-seconds-into-hours-minutes-and-seconds/

        :param seconds: The time to convert
        :return: A string representation in minutes and seconds
        """
        seconds = seconds % (24 * 3600)
        # hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return "%d:%02d" % (minutes, seconds)

    def get_status(self):
        """
        Gets the full status of the turn, for display on the frontend

        :return: A dictionary containing the various components.
        """
        if self.state == "paused":
            self.start_time = time.time() - self.state_amount
        delay, bank = self.get_remaining_time()
        current_player = self.get_player(self.current_player)
        next_player = self.get_player(self.get_next())
        previous_player = self.get_player(self.get_previous())
        return {"current_player": current_player,
                "next_player": next_player,
                "previous_player": previous_player,
                "delay_remaining": delay,
                "bank_remaining": bank,
                "state": self.state}
