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

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/autocomplete")
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

# ----- Main function -----------------------------------------------------------------------------

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=True)
