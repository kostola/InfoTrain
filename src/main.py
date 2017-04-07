from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit
import logic

async_mode=None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True
socketio = SocketIO(app, async_mode=async_mode)

logic.logger = app.logger

# ----- Main routes -------------------------------------------------------------------------------

#@app.route("/")
#def index():
#    return render_template('index.html')

@app.route("/")
def autocomplete():
    return render_template('autocomplete.html')

@app.route("/starter")
def starter():
    return render_template('starter.html')

@app.route("/stations_list/<txt>")
def stations_list(txt=None):
    app.logger.info("stations list partial: %s" % (txt))
    stations_dict = logic.stations_autocomplete(txt)
    app.logger.info(stations_dict)
    return render_template('partials/index/stations_container.html', stations=stations_dict, stations_len=len(stations_dict))

# ----- APIs --------------------------------------------------------------------------------------

@app.route("/api/v1/stations/<txt>")
def stations_lookup(txt=None):
    app.logger.info("stations api: %s" % (txt))
    return jsonify(logic.stations_autocomplete(txt))

# ----- SocketIO ----------------------------------------------------------------------------------

@socketio.on('find', namespace='/stationsws')
def stationsws_find(message):
    app.logger.info("stations ws: %s" % (message))
    stations = logic.stations_autocomplete(message['data'])
    reply = {
        "changes": [
            {
                "target": "#stations_msg",
                "action": "set_html",
                "html"  : render_template('partials/index/stations_msg.html', stations_len=len(stations))
            },
            {
                "target": "#stations_container",
                "action": "set_html",
                "html"  : render_template('partials/index/stations_container.html', stations=stations, stations_len=len(stations))
            }
        ]
    }
    emit('find_reply', reply)

@socketio.on('findlist', namespace='/stationsws')
def stationsws_findlist(message):
    app.logger.info("stations ws: %s" % (message))
    stations = logic.stations_autocomplete_noids(message['data'])
    emit('findlist_reply', stations)

@socketio.on('stationdetails', namespace='/stationsws')
def stationsws_stationdetails(message):
    app.logger.info("stations details: %s" % (message))
    station_name, station_id = logic.station_autocomplete_single(message['data'])
    arrivals = logic.station_arrivals(station_id)
    departures = logic.station_departures(station_id)
    reply = {
        "changes": [
            {
                "target": "#station_name_container",
                "action": "set_html",
                "html"  : "" if station_name is None else render_template('partials/index/station_name_container.html', name=station_name)
            },
            {
                "target": "#arrivals_container",
                "action": "set_html",
                "html"  : "" if arrivals is None else render_template('partials/index/trains_container.html', title="Arrivals", trains=arrivals, where="From")
            },
            {
                "target": "#departures_container",
                "action": "set_html",
                "html"  : "" if departures is None else render_template('partials/index/trains_container.html', title="Departures", trains=departures, where="To")
            }
        ]
    }
    emit('stationdetails_reply', reply)

# ----- Main function -----------------------------------------------------------------------------

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=True)
