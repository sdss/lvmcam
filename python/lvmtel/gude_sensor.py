import requests
import json
import fnmatch
import time


#
# get sensor_descr / sensor_values as JSON objects
#
def getSensorsJson(host,
                   ssl=False,
                   timeout=5,
                   username=None,
                   password=None,
                   skipcomplex=True,
                   skipsimple=False,
                   verbose=False):

    '''
    import gude_sensor
    ret = gude_sensor.getSensorsJson("10.8.38.122")
    print(f"t oc: {ret['sensor_values'][0]['values'][0][0]['v']} °C")
    print(f"t ic: {ret['sensor_values'][1]['values'][0][0]['v']} °C")
    print(f"h ic: {ret['sensor_values'][1]['values'][0][1]['v']} %")
    print(f"t ic: {ret['sensor_values'][1]['values'][0][2]['v']} °C dewpoint")
    '''

    if ssl:
        url = 'https://'
    else:
        url = 'http://'

    url += host + '/' + 'status.json'

    auth = None
    if username:
        auth = requests.auth.HTTPBasicAuth(username, password)

    DESCR  = 0x10000
    VALUES = 0x4000
    EXTEND = 0x800000  # enables complex sensors-groups, such as Sensor 101, 20, etc...
    SENSORS = DESCR + VALUES

    if skipcomplex:
        cgi = {'components': SENSORS}  # simple-sensors only (fully backward compatible)
    elif skipsimple:
        cgi = {'components': SENSORS + EXTEND, 'types': 'C'}  # complex sensors-groups only
    else:
        cgi = {'components': SENSORS + EXTEND}  # simple-sensors + complex sensors-groups in one merged view

    r = requests.get(url, params=cgi, verify=False, auth=auth, timeout=timeout)

    if r.status_code == 200:
        if verbose:
            print (f"HTTP GET:\n\t{r.url}")
            print (f"HTTP RESPONSE:\n\t{r.text}\n\n")

        return json.loads(r.text)
    else:
        raise ValueError("http request error {0}".format(r.status))
