from threading import Thread, Event
from time import sleep

from flask import Flask, render_template
from flask_socketio import SocketIO

from clocks.countup import CountUp
from clocks.increment import Increment
from clocks.simpledelay import SimpleDelay
from clocks.countdown import Countdown
from clocks.hourglass import Hourglass
from gameclock import GameClock


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app)
gc = SimpleDelay(player_names=["Red Team", "Blue Team"])
# gc = GameClock(number_players=2, delay_amount=30, bank_amount=3, names=["Red Team", "Blue Team"])


@app.route('/')
def index():
    """
    Render the main page.

    :return: A render template.
    """
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('connect')
def connect():
    """
    Handle incoming socket connections. Connect them all to the same game clock thread, and send the current state.

    :return: None
    """
    global thread
    # Start the interval thread only if the thread has not been started before.
    if not thread.is_alive():
        global gc
        gc.start_player_turn()

        thread = StateInterval()
        thread.start()
    current_state()


@socketio.on('current state')
def current_state():
    """
    Emits the current state of the game clock.

    :return: None
    """
    global gc
    socketio.emit('status', gc.get_status())


""" Commands related to managing the clock below """


@socketio.on('next')
def next():
    global gc
    gc.next_player()
    current_state()


@socketio.on('previous')
def previous():
    global gc
    gc.previous_player()
    current_state()


@socketio.on('pause')
def pause():
    global gc
    gc.pause_player_turn_toggle()
    current_state()


@socketio.on('end')
def end():
    global gc
    gc.end()
    current_state()


""" Thread handling for interval checks below """
# Store global thread object to make sure only one game thread is running per application
thread = Thread()
thread_stop_event = Event()


class StateInterval(Thread):
    """
    Class for running a thread which periodically calls the current_state() function.
    """
    def __init__(self):
        self.delay = 1
        super(StateInterval, self).__init__()

    def current_state_interval(self):
        """
        Call the current state function to update the frontend over the socket on a repeated interval.
        """
        while not thread_stop_event.is_set():
            current_state()
            sleep(self.delay)

    def run(self):
        self.current_state_interval()


if __name__ == '__main__':
    socketio.run(app)
