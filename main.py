from flask import Flask, jsonify, render_template
import collections
import json
import requests

app = Flask(__name__)

# ----- APIs --------------------------------------------------------------------------------------

@app.route("/api/v1/stations/<txt>")
def stations_lookup(txt=None):
    r = requests.get("http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/autocompletaStazione/%s" % (txt))
    unordered_dict = { line.split("|")[0] : line.split("|")[1] for line in r.text.splitlines() if len(line) > 0 }
    output_dict = collections.OrderedDict(sorted(unordered_dict.items())) if len(unordered_dict) > 0 else {}
    #return json.dumps(output_dict, separators=(',',':'))
    return jsonify(output_dict)

# ----- Main routes -------------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/starter")
def starter():
    return render_template('starter.html')

# ----- Main function -----------------------------------------------------------------------------

if __name__ == "__main__":
    app.run()
