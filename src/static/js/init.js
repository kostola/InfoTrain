var changeTimer = false;

function setStations(stations) {
    console.log("setStations");
    console.log(stations);
    number_of_stations = Object.keys(stations).length
    console.log(number_of_stations)
    
    if (number_of_stations == 1) {
        $("#stations_msg").html("<div class=\"chip\">" + number_of_stations + " station found</div>");
    } else if (number_of_stations > 0) {
        $("#stations_msg").html("<div class=\"chip\">" + number_of_stations + " stations found</div>");
    } else {
        $("#stations_msg").html("<div class=\"chip\">no stations</div>");
    }

    $("#stations_container").html("");
    var tot_counter = 1;
    var counter = 0;
    var htmlrow = "";
    Object.keys(stations).forEach( function(key) {
        console.log("Processing station: " + key + " " + stations[key]);
        if (counter == 0) {
            htmlrow += "<div class=\"row\">";
        }
        htmlrow += "<div class=\"col s12 m3\"><div class=\"card-panel red darken-2\"><span class=\"white-text\">"
        htmlrow += key;
        htmlrow += "</span></div></div>"
        if (counter == 3 || tot_counter == number_of_stations) {
            htmlrow += "</div>\n";
            $("#stations_container").append(htmlrow);
            htmlrow = "";
            counter = 0;
        } else {
            counter++;
        }
        tot_counter++;
    });
}

$(document).ready( function() {
    // initializations
    $('.button-collapse').sideNav();
    $('.chips').material_chip();

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
                $("#stations_msg").html("");
                $("#stations_container").html("");
            }
        }, 300);
    });
});
