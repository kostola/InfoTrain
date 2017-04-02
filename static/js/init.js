var changeTimer = false;

/*
(function($) {
    $(function() {
        

        $("#station").on("change",function() {
            if(changeTimer !== false) clearTimeout(changeTimer);
            changeTimer = setTimeout( function() {
                console.log("timerz")
                changeTimer = false;
            }, 300);
        });
    }); // end of document ready
})(jQuery); // end of jQuery name space
*/

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
    $('.button-collapse').sideNav();

    $("#station").on('input', function() {
        if(changeTimer !== false) clearTimeout(changeTimer);
        changeTimer = setTimeout( function() {
            console.log("search stations")
            if ( $("#station").val().length > 0 ) {
                $.get( "/api/v1/stations/" + $("#station").val(), function(data) {
                    //console.log("get finished")
                    //console.log(data)
                    //$( "body" ).append(data)
                    setStations(data);
                }, "json" );
            } else {
                $("#stationmsg").html("");
            }
        }, 300);
    });
});
