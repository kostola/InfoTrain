var lastDetails = "";
var lastSearch = "";
var socket;
var timer = false;

function onStationAutocomplete(value) {
    if(timer !== false) {
        clearTimeout(timer);
    }
    console.log("station autocompleted: " + value);
    lastSearch = value;
    findStationDetails(value);
}

function onTimerTriggered() {
    timer = false;
    console.log("onTimerTriggered");
    findStationDetails($("#station").val());
}

function findStationDetails(value) {
    if (value != lastDetails) {
        lastDetails = value;
        $("#station_name_container").html("");
        $("#arrivals_container").html("");
        $("#departures_container").html("");
        socket.emit('stationdetails', { data: value });
        console.log("WS: emitted 'stationdetails' (data: " + value + ")");
    }
}

function parseReply(reply) {
    if ("changes" in reply) {
        changes = reply["changes"];
        for (var i = 0; i < changes.length; i++) {
            applyChange(changes[i]);
        }
    }
}

function applyChange(change) {
    if ("action" in change) {
        if (change["action"] == "set_html") {
            $(change["target"]).html(change["html"]);
        } else {
            console.log("applyChange received a unknown action \"" + change["action"] + "\"");
        }
    } else {
        console.log("applyChange received a change with no action");
    }
}

$(document).ready( function() {
    // initializations
    $('.button-collapse').sideNav();

    // stations websocket
    var ws_url = location.protocol + '//' + document.domain + ':' + location.port + '/stationsws'
    console.log("WS URL: " + ws_url);
    socket = io.connect(ws_url);
    
    socket.on('findlist_reply', function(reply) {
        console.log("findlist_reply");
        $('#station').autocomplete({ data: reply, limit: 10, onAutocomplete: onStationAutocomplete, minLength: 2 });        
    });
    socket.on('stationdetails_reply', function(reply) {
        console.log("stationdetails_reply");
        lastDetails = "";
        parseReply(reply);
    });

    $('#station').on('keyup', function() {
        if(timer !== false) {
            clearTimeout(timer);
        }
        var search_text = $("#station").val();
        if (search_text != lastSearch) {
            console.log("search_text: " + search_text + " vs lastSearch: " + lastSearch);
            lastSearch = search_text;
            if ( search_text.length > 1 ) {
                socket.emit('findlist', { data: search_text });
                console.log("WS: emitted 'findlist' (data: " + search_text + ")");
            }
            timer = setTimeout(onTimerTriggered, 2000);
        }
    });
});
