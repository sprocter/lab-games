import time


class Clock:
    """
    A timing clock implementation for multiple players. This is a base class which can be extended to implement your
    own custom timers. This class provides standard time counting, clock history, pause functionality, and next/prev
    player changes.
    """
    turn = 1
    player_count = 0
    player_names = list()
    current_player = 1
    history = list()
    turn_start_time = 0
    pause_start_time = 0
    clock = list()

    def __init__(self, player_count=0, player_names=None):
        """
        Initializes the clock with some player information.

        :param player_count: An integer representing the number of players playing.
        :param player_names: Optionally provided names to provide more personalization.
        """
        if player_names:
            # Names were provided, so use them to create players
            self.player_names = player_names

            # Check if more names provided than the number of players. If so, set the player count to that
            if len(self.player_names) > player_count:
                self.player_count = len(self.player_names)

        # Check if player_count initialized
        if self.player_count == 0:
            self.player_count = player_count

    def save_history(self, filepath):
        """
        Saves the turn history to a given file.

        :param filepath: The filepath to save to
        :return: None
        """
        pass

    def start_player_turn(self):
        """
        Starts the player's turn by keeping track of the moment this function was last called.

        :return: None
        """
        self.turn_start_time = time.time()

    def get_turn_length(self):
        """
        Get the length of this turn.

        :return: An integer
        """
        if self.is_paused():
            # Full turn length - pause length
            return int((time.time() - self.turn_start_time) - (time.time() - self.pause_start_time))
        else:
            return int(time.time() - self.turn_start_time)

    def get_clock_time(self):
        """
        Get the length of this turn.

        :return: An integer
        """
        return int(self.clock[self.current_player])

    def get_next_player(self):
        """
        Gets the next player.

        :return: The id of the next player.
        """
        return self.current_player + 1 if self.current_player < self.player_count else 1

    def get_previous_player(self):
        """
        Gets the previous player.

        :return: The id of the previous player.
        """
        return self.current_player - 1 if self.current_player > 0 else self.player_count

    def is_paused(self):
        """
        Returns whether or not the players turn is paused.

        :return: True if player's turn is paused.
        """
        return self.pause_start_time > 0

    def pause_player_turn_toggle(self):
        """
        Toggles the pause on a player's turn.

        :return: None
        """
        if not self.is_paused():
            self.pause_start_time = time.time()
        else:
            # To unpause the turn, add the time delta between now and when the pause started to the start of the turn
            self.turn_start_time += time.time() - self.pause_start_time
            self.pause_start_time = 0

    def get_player(self, player_id):
        """
        Gets the string name of the provided player.

        :param player_id: The id (an int) of the current player
        :return: A string either pulled from names, or as "Player x"
        """
        if self.player_names:
            try:
                return self.player_names[player_id - 1]
            except IndexError:
                pass
        return "Player " + str(player_id)

    def convert_to_formatted_time(self, seconds):
        """
        Converts an int into minutes and seconds.
        from: https://www.geeksforgeeks.org/python-program-to-convert-seconds-into-hours-minutes-and-seconds/

        :param seconds: The time to convert
        :return: A string representation in minutes and seconds
        """
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        if hour > 0:
            return "%d:%d:%02d" % (hour, minutes, seconds)
        elif minutes > 0:
            return "%d:%02d" % (minutes, seconds)
        else:
            return ":%02d" % (seconds)

    def next_player(self):
        """
        Moves the clock on to the next player.

        :return: None
        """
        # Move on to the next player
        self.current_player = self.get_next_player()

        # Increment the turn timer
        if self.current_player == 1:
            self.turn += 1

        # Clear the pause
        if self.is_paused():
            self.pause_start_time = 0

        # Start new player's turn
        self.start_player_turn()

    def previous_player(self):
        """
        Moves the clock back to the previous player.

        :return: None
        """
        # Move on to the previous player
        self.current_player = self.get_previous_player()

        # Increment the turn timer
        if self.current_player == self.player_count:
            self.turn -= 1

        # Clear the pause
        if self.is_paused():
            self.pause_start_time = 0

        # Start new player's turn
        self.start_player_turn()

    def get_status(self):
        """
        Gives the current status of the clock and some extra information about players and pause state.

        :return: A dictionary object containing information.
        """
        turn_time = self.get_turn_length()
        total_time = self.get_total_time()
        current_player = self.get_player(self.current_player)
        next_player = self.get_player(self.get_next_player())
        previous_player = self.get_player(self.get_previous_player())

        return {"current_player": current_player,
                "next_player": next_player,
                "previous_player": previous_player,
                "turn_time": self.convert_to_formatted_time(turn_time),
                "total_time": self.convert_to_formatted_time(total_time),
                "is_paused": self.is_paused()
                }

    def get_total_time(self):
        """
        Gets the total time left on the player's clock.

        :return: An integer representing the time left on the clock.
        """
        total_time = int(self.get_clock_time() - self.get_turn_length())
        return 0 if total_time <= 0 else total_time
