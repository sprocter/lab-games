// Connect to the socket server.
var socket = io.connect('http://' + document.domain + ':' + location.port);

// Update the status whenever we hear over the socket
socket.on('status', function (msg) {
    console.log(msg);
    $("#player-name").html(msg.current_player);
    $("#turn-time").html(msg.turn_time);
    $("#total-time").html(msg.total_time);
    $("#next-player").html(msg.next_player);
    $("#previous-player").html(msg.previous_player);

    if (msg.is_paused) {
        $("#pause-btn").addClass("active");
    } else {
        $("#pause-btn").removeClass("active");
    }
});

// Send messages over the socket with commands
$("body").keyup(function(e){
    let keySpace = 32;
    let keyRight = 39;
    let keyDown = 40;
    let keyLeft = 37;
    let keyEscape = 27;

    if (e.keyCode == keyRight) {
        socketEmit('next')
    } else if (e.keyCode == keyLeft) {
        socketEmit('previous')
    } else if (e.keyCode == keySpace || e.keyCode == keyDown) {
        socketEmit('pause')
    } else if (e.keyCode == keyEscape) {
        socketEmit('end')
    }
});

// Simple function to handle the socket emits from both button presses as well as in scripts.
function socketEmit(event) {
    socket.emit(event);
}