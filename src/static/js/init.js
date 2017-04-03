var changeTimer = false;

function setStations(stations) {
    console.log("setStations");
    console.log(stations);
    number_of_stations = Object.keys(stations).length
    console.log(number_of_stations)
    if (number_of_stations > 0) {
        $("#stationmsg").html(number_of_stations + " STATIONS FOUND");
    } else {
        $("#stationmsg").html("NO STATIONS");
    }
}

$(document).ready( function() {
    // navbar
    $('.button-collapse').sideNav();

    // stations websocket
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/stationsws');
    
    socket.on('find_reply', function(msg) {
        console.log("socket replied " + msg)
        setStations(msg.data);
    });

    /*$('form#emit').submit(function(event) {
        socket.emit('my event', {data: $('#emit_data').val()});
        return false;
    });
    $('form#broadcast').submit(function(event) {
        socket.emit('my broadcast event', {data: $('#broadcast_data').val()});
        return false;
    });*/

    $("#station").on('input', function() {
        if(changeTimer !== false) clearTimeout(changeTimer);
        changeTimer = setTimeout( function() {
            console.log("search stations")
            if ( $("#station").val().length > 0 ) {
                console.log("emit find message")
                socket.emit('find', { data: $("#station").val() });
                /*$.get( "/api/v1/stations/" + $("#station").val(), function(data) {
                    setStations(data);
                }, "json" );*/
            } else {
                console.log("empty input")
                $("#stationmsg").html("");
            }
        }, 300);
    });
});
