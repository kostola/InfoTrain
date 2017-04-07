from datetime import datetime
import json
import pytz
import requests

# ----- API methods -------------------------------------------------------------------------------

def arrivi(station_id):
    return base_arrivi_partenze('arrivi', station_id)

def autocompletaStazione(txt):
    r = requests.get(full_url_for("autocompletaStazione/%s" % (txt)))
    return { line.split("|")[0] : line.split("|")[1] for line in r.text.splitlines() if len(line) > 0 }

def partenze(station_id):
    return base_arrivi_partenze('partenze', station_id)

# ----- Helper methods ----------------------------------------------------------------------------

def base_arrivi_partenze(direction,station_id):
    date_str = datetime.now(tz=pytz.timezone('Europe/Rome')).strftime('%a %b %d %Y %H:%M:%S GMT%z')
    r = requests.get(full_url_for("%s/%s/%s" % (direction, station_id, date_str)))
    if r.status_code != 200:
        return None
    return r.json()

def full_url_for(path):
    return "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/%s" % (path)
