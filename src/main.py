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

@app.route("/starter")
def starter():
    return render_template('starter.html')

@app.route("/stations_list/<txt>")
def stations_list(txt=None):
    app.logger.info("stations list partial: %s" % (txt))
    stations_dict = logic.stations_autocomplete(txt)
    app.logger.info(stations_dict)
    return render_template('partials/stations_list.html', stations=stations_dict, stations_len=len(stations_dict))

# ----- APIs --------------------------------------------------------------------------------------

@app.route("/api/v1/stations/<txt>")
def stations_lookup(txt=None):
    app.logger.info("stations api: %s" % (txt))
    return jsonify(logic.stations_autocomplete(txt))

# ----- SocketIO ----------------------------------------------------------------------------------

@socketio.on('find', namespace='/stationsws')
def test_message(message):
    app.logger.info("stations ws: %s" % (message))
    emit('find_reply', { 'data': logic.stations_autocomplete(message) })

# ----- Main function -----------------------------------------------------------------------------

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=True)
