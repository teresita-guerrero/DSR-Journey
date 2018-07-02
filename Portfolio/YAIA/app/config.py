import json
from pprint import pprint


with open('config/enabledAPIs.json') as jsonFile:
    data = json.load(jsonFile)

def emailConfiguration():
    config = {
        "service_name"    : data['email']['service_name'],
        "service_version" : data['email']['service_version'],
        "service_scopes"  : data['email']['service_scopes']
    }

    return config
