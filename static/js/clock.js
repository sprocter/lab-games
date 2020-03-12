// Connect to the socket server.
var socket = io.connect('http://' + document.domain + ':' + location.port);

var currentTimeout = null;
var lastBank = null;
// Update the status whenever we hear over the socket
socket.on('status', function (msg) {
    console.log(msg);

    // Update the various html locations with their msg details
    $("#player-name").html(msg.current_player);
    $("#turn-time").html(msg.turn_time);
    $("#total-time").html(msg.total_time);
    $("#next-player").html(msg.next_player);
    $("#previous-player").html(msg.previous_player);

    // Update the pause button
    if (msg.is_paused) {
        $("#pause-btn").addClass("active");
    } else {
        $("#pause-btn").removeClass("active");
    }

    // If not doing a simple count up, trigger visual cues
    if (msg.clock_type !== "CountUp") {
        let seconds = parseInt(msg.total_time.substr(msg.total_time.length-2));
        if (lastBank !== msg.total_time) {
            if (msg.total_time === ":00") {
                setBackground("#dc3545", true)
            } else if (msg.total_time.length === 3 && (seconds === 30 || seconds < 10 || (seconds < 30 && seconds > 0 && (seconds % 5 === 0)))) {
                flashBackground("#ffc107")
            } else if (seconds === 0) {
                flashBackground("#9ca7af")
            }
        }
        lastBank = msg.total_time;
    }
});

// A function to "flash" the background by using a simple delay
function flashBackground(color) {
    setBackground(color, true);
    currentTimeout = window.setTimeout(setBackground, 200, "white");
}

// Sets the background to a given color. Also clears a timeout if needed (used for no time left)
function setBackground(color, clear=false) {
    if (clear) {
        clearTimeout(currentTimeout);
    }
    $("body").css("background-color", color);
}

// Send messages over the socket with commands
$("body").keyup(function(e){
    let keySpace = 32;
    let keyRight = 39;
    let keyDown = 40;
    let keyLeft = 37;
    let keyEscape = 27;

    if (e.keyCode == keyRight) {
        nextPlayer()
    } else if (e.keyCode == keyLeft) {
        previousPlayer()
    } else if (e.keyCode == keySpace || e.keyCode == keyDown) {
        socketEmit('pause');
    } else if (e.keyCode == keyEscape) {
        socketEmit('end');
    }
});

function nextPlayer() {
    socketEmit('next');
    flashBackground("#343a40");
    playNotification()
}

function previousPlayer() {
    socketEmit('previous');
    flashBackground("#9ca7af");
    playNotification()
}

// Simple function to handle the socket emits from both button presses as well as in scripts.
function socketEmit(event) {
    socket.emit(event);
}