from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit
import collections
import json
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app)

# ----- Main routes -------------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/starter")
def starter():
    return render_template('starter.html')

# ----- APIs --------------------------------------------------------------------------------------

@app.route("/api/v1/stations/<txt>")
def stations_lookup(txt=None):
    app.logger.info("stations api: %s" % (txt))
    r = requests.get("http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/autocompletaStazione/%s" % (txt))
    unordered_dict = { line.split("|")[0] : line.split("|")[1] for line in r.text.splitlines() if len(line) > 0 }
    output_dict = collections.OrderedDict(sorted(unordered_dict.items())) if len(unordered_dict) > 0 else {}
    return jsonify(output_dict)

# ----- SocketIO ----------------------------------------------------------------------------------

@socketio.on('find', namespace='/stationsws')
def test_message(message):
    app.logger.info("stations ws: %s" % (message))
    r = requests.get("http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/autocompletaStazione/%s" % (message['data']))
    unordered_dict = { line.split("|")[0] : line.split("|")[1] for line in r.text.splitlines() if len(line) > 0 }
    output_dict = collections.OrderedDict(sorted(unordered_dict.items())) if len(unordered_dict) > 0 else {}
    emit('find_reply', { 'data': output_dict })

# ----- Main function -----------------------------------------------------------------------------

if __name__ == "__main__":
    socketio.run(app, debug=True)
