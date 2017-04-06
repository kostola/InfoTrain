import collections
import json
import requests

logger = None

def stations_autocomplete(txt):
    url = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/autocompletaStazione/%s" % (txt)
    logger.info(url)
    r = requests.get("http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/autocompletaStazione/%s" % (txt))
    logger.info(r)
    unordered_dict = { line.split("|")[0] : line.split("|")[1] for line in r.text.splitlines() if len(line) > 0 }
    return collections.OrderedDict(sorted(unordered_dict.items())) if len(unordered_dict) > 0 else {}

def stations_autocomplete_noids(txt):
    url = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/autocompletaStazione/%s" % (txt)
    logger.info(url)
    r = requests.get("http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/autocompletaStazione/%s" % (txt))
    logger.info(r)
    unordered_dict = { line.split("|")[0] : "" for line in r.text.splitlines() if len(line) > 0 }
    return collections.OrderedDict(sorted(unordered_dict.items())) if len(unordered_dict) > 0 else {}
