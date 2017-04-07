import collections
import viaggiatreno as vt

logger = None

def station_arrivals(station_id):
    #stations = stations_autocomplete(station_name)
    #if len(stations) != 1:
    #    return None
    #station_id = stations.values()[0]
    if station_id is None:
        return None
    vt_dict = vt.arrivi(station_id)
    if vt_dict is None:
        return None
    return [
        {
            'time' : train['compOrarioArrivo'],
            'code' : "%s %s" % (train['categoria'], train['numeroTreno']),
            'where': train['origine'],
            'delay': train['compRitardoAndamento'][1]
        }
        for train in vt_dict
    ]

def station_departures(station_id):
    #stations = stations_autocomplete(station_name)
    #if len(stations) != 1:
    #    return None
    #station_id = stations.values()[0]
    if station_id is None:
        return None
    vt_dict = vt.partenze(station_id)
    if vt_dict is None:
        return None
    return [
        {
            'time' : train['compOrarioPartenza'],
            'code' : "%s %s" % (train['categoria'], train['numeroTreno']),
            'where': train['destinazione'],
            'delay': train['compRitardoAndamento'][1]
        }
        for train in vt_dict
    ]

def station_autocomplete_single(station_name):
    stations = stations_autocomplete(station_name)
    if len(stations) != 1:
        return None, None
    return stations.keys()[0], stations.values()[0]

def stations_autocomplete(txt):
    unordered_dict = vt.autocompletaStazione(txt)
    return collections.OrderedDict(sorted(unordered_dict.items())) if len(unordered_dict) > 0 else {}

def stations_autocomplete_noids(txt):
    unordered_dict = vt.autocompletaStazione(txt)
    return collections.OrderedDict(sorted([ (key,'') for key,value in unordered_dict.iteritems() ])) if len(unordered_dict) > 0 else {}
