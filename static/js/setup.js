// The variable holding the names that will be sent when starting the clock
var names=[];

// Hides all the extra clock variables
function hideAllClock() {
    $("#clock-info").children().addClass("d-none");
    $("#clock-timing").children().addClass("d-none");
}

// Listen for the select to be changed, and update the page based on what was selected
$('#clock-select').change(function() {
    let selection = $("#clock-select").val();

    // Hide all the info, so we have a fresh slate
    hideAllClock();

    // Show the relevant clock info
    $("#clock-info-" + selection).removeClass("d-none");

    // Reveal things based on the clock type
    switch(selection) {
        case "count-up":
            // The exception case where we don't have a starting bank time
            break;
        case "increment":
        case "simple-delay":
        case "bronstein-delay":
            $("#clock-timing-delay").removeClass("d-none");
        default:
            $("#clock-timing-start").removeClass("d-none");
    }
});

// Listen to every key hit on this page. If it is enter, try to create a new name.
$(document).keypress(function(event) {
    var keycode = event.keyCode || event.which;
    if (keycode == '13') {
        // Cancel the default action, if needed
        event.preventDefault();

        // Get the new name and try to add it to the names list
        var name = $("#add-name").val();
        if (name !== "") {
            names.push(name);
            updateNames();
            $("#add-name").val('');
        }
    }
});

// Quickly add two names to the names list, corresponding to two teams.
function twoTeamQuickstart() {
    // Hidden functionality, if the button has been pressed once already, switch to chess teams
    if (names.indexOf("Red Team") >= 0 && names.indexOf("Blue Team") >= 0) {
        names = [];
        names.push("White");
        names.push("Black");
    } else {
        names = [];
        names.push("Red Team");
        names.push("Blue Team");
    }

    updateNames();
}

// Display the names currently in the names variable
function updateNames() {
    // Reset the div
    $("#names").empty();

    // Add every name in the names variable
    for (var i in names) {
        $("#names").append('' +
            '<li class="list-group-item" id="name-' + i + '">\n' +
            '   <span class="float-left">' + names[i] + '</span>\n' +
            '   <span class="float-right button-group">\n' +
            '   <button type="button" class="btn btn-danger" onclick="removeName(' + i + ')"><span class="glyphicon glyphicon-remove"></span>X</button>\n' +
            '   </span>\n' +
            '</li>');
    }

    // If enough names are added, let the user start the clock
    if (names.length > 1) {
        $("#start-clock").removeAttr("disabled")
    } else {
        $("#start-clock").attr("disabled", true)
    }
}

// Remove a name by a given index id
function removeName(id) {
    names.splice(id, 1);
    updateNames()
}