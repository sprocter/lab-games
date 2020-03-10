import os
from threading import Thread, Event
from time import sleep

from flask import Flask, render_template, request, make_response
from flask_socketio import SocketIO

from clocks.bronsteindelay import BronsteinDelay
from clocks.countup import CountUp
from clocks.increment import Increment
from clocks.simpledelay import SimpleDelay
from clocks.countdown import Countdown
from clocks.hourglass import Hourglass


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['DEBUG'] = True
app.config['SERVER_NAME'] = os.environ.get('CLOCK_SERVER', 'localhost:8080')
socketio = SocketIO(app)
gc = None


@app.route('/')
def index():
    """
    Render the initial page.

    :return: A render template.
    """
    return render_template('setup.html', async_mode=socketio.async_mode)


@app.route('/setup', methods=["POST"])
def setup():
    """
    Setup the game clock.

    :return: A response indicating success or failure.
    """
    global gc

    # Get the variables from the request
    player_names = request.json.get('names', [])
    clock_type = request.json.get('type', 'count-up')
    bank = int(request.json.get('bank', 0))
    delay = int(request.json.get('delay', 0))

    # Setup the response for later
    resp = make_response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.status_code = 200

    # Make sure some people are being timed
    if len(player_names) <= 1:
        resp.status_code = 500
        return resp

    # Setup the clock based on inputs
    if clock_type == "count-up":
        gc = CountUp(player_names=player_names)
    elif clock_type == "countdown":
        gc = Countdown(player_names=player_names, starting_clock=bank)
    elif clock_type == "increment":
        gc = Increment(player_names=player_names, starting_clock=bank, increment_amount=delay)
    elif clock_type == "hourglass":
        gc = Hourglass(player_names=player_names, starting_clock=bank)
    elif clock_type == "simple-delay":
        gc = SimpleDelay(player_names=player_names, starting_clock=bank, delay_amount=delay)
    elif clock_type == "bronstein-delay":
        gc = BronsteinDelay(player_names=player_names, starting_clock=bank, delay_amount=delay)
    else:
        resp.status_code = 500

    if resp.status_code == 200:
        gc.start_player_turn()

    return resp


@app.route('/clock')
def clock():
    """
    Render the main clock page.

    :return: A render template.
    """
    return render_template('clock.html', async_mode=socketio.async_mode)


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
        if gc:
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
    if gc:
        socketio.emit('status', gc.get_status())


""" Commands related to managing the clock below """


@socketio.on('next')
def next_player():
    global gc
    gc.next_player()
    current_state()


@socketio.on('previous')
def previous_player():
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
