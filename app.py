import requests
from flask import Flask, jsonify, make_response
import re


app = Flask(__name__)

base_url = 'https://tgftp.nws.noaa.gov/data/observations/metar/decoded'


#class TemperatureNotFound(Exception):
#    pass
#class PressureNotFound(Exception):
#    pass


def extract_temperature_and_pressure_from_tgftp_text_response(text):

    res = re.search('temperature: (.*)', text, re.IGNORECASE)
    if res is not None:
        temperature = res.group(1)
    else:
        temperature = None

    res = re.search('pressure \(altimeter\): (.*)', text, re.IGNORECASE)
    if res is not None:
        pressure = res.group(1)
    else:
        pressure = None

    # future: extraction of values as float and unit as string

    return {
        'temperature': temperature,
        'pressure': pressure,
    }


def extract_locations_from_tgftp_response(text):
    """
    quick and dirty: rely on .TXT ending to identify locations
    """
    return set(re.findall("([A-Z0-9]{4}).TXT", text))

@app.route("/<location>")
def get_data(location):
    """
    we always try to return both temperature and pressure
    because the workload of getting both is only
    minisculely larger than getting one of the two
    """
    remote_response = requests.get(f'{base_url}/{location.upper()}.TXT')
    if not remote_response.ok:
        """
        the following check is taking long but gives the user feedback
        on whether the remote server is down and possibly about the
        location options
        """
        remote_response = requests.get(f'{base_url}')
        if not remote_response.ok:
            return "remote server seems to be down", 503
        else:
            return f"provided location wasn't found on the server. Possible locations: {extract_locations_from_tgftp_response(remote_response.content.decode('ascii'))}", 404
            #return 404, f"provided location wasn't found on the server. Go to \"{base_url}\" to find a list of possible locations."

    # assume ascii encoding of the .TXT files
    response = extract_temperature_and_pressure_from_tgftp_text_response(remote_response.content.decode('ascii'))

    return make_response(jsonify(response), 200)
