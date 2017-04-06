var changeTimer = false;
var lastSearch = "";

function onStationAutocomplete(value) {
    console.log("station autocompleted: " + value);
}

$(document).ready( function() {
    // initializations
    $('.button-collapse').sideNav();

    // stations websocket
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/stationsws');
    
    socket.on('find_reply', function(reply) {
        console.log("socket replied " + JSON.stringify(reply));
        parseReply(reply);
    });
    socket.on('findlist_reply', function(reply) {
        console.log("findlist_reply");
        $('#station').autocomplete({ data: reply, limit: 4, onAutocomplete: onStationAutocomplete, minLength: 2 });        
    });

    $('#station').on('keyup', function() {
        var search_text = $("#station").val();
        if (search_text != lastSearch) {
            lastSearch = search_text;
            if ( search_text.length > 1 ) {
                socket.emit('findlist', { data: search_text });
            }
        }
    });
});
