#!/usr/bin/env python3

'''This script uses the new PurpleAir API (see api.purpleair.com) to get the
list of sensors in the Chicago area. More precisely, we get all the sensors in
the bounding box associated to the multipolygon representing the Chicago city
boundaries. We do not consider sensors that are flagged as 'inside'.

Note: PurpleAir requests that we refrain from more than 1 request every 1 to 10
minutes, and that when pulling data from multiple sensors, we do it in a single
request.
'''

# TODO double check that the lat/long conventions are consistent, etc.

import geopandas as gpd
import pandas as pd
import requests

def get_chicago_bounding_box() -> list[float]:
    '''
    Reads Chicago city boundaries from file and returns a bounding box that
    contains these boundaries.

    OUTPUT
    ===
    bounding_box: list-like, an iterable list of floats [minx, miny, maxx, maxy]
        defining the bounding box.

    '''
    df = gpd.read_file('../data/chicago.geojson')
    bounding_box = df.total_bounds
    return bounding_box

def get_purpleair_sensors(
        api_key: str,
        bbox: list[float] = get_chicago_bounding_box(),
        fields: list[str] = ['sensor_index', 'name', 'latitude', 'longitude',
                             'primary_id_a', 'primary_key_a', 'primary_id_b',
                             'primary_key_b']
):
    '''
    Obtains data from the PurpleAir sensors in the given bounding box.

    PARAMETERS
    ===
    api_key: str, personal PurpleAir API key
    bbox: list-like, an iterable list of floats [minx, miny, maxx, maxy]
        defining the geometric/geographic bounding box in which to get sensors
    fields: list-like, an iterable list of data fields to request from each of
        the sensors
    '''
    # construct the fields parameter, comma-separated
    fields_param = ''.join(
        [field + ',' if field != fields[-1] else field for field in fields]
    )

    # construct the API query
    request = (
        f'https://api.purpleair.com/v1/sensors?'
        f'api_key={api_key}'
        f'&fields={fields_param}'
        f'&location_type=0'
        f'&nwlng={bbox[0]}'
        f'&nwlat={bbox[3]}'
        f'&selng={bbox[2]}'
        f'&selat={bbox[1]}'
    )

    # request the API
    response = requests.get(request)

    # if we don't receive 200 OK, panic
    if response.status_code != 200:
        raise Exception(
            f'PurpleAir API returned response code {response.status_code} '
            f'(see https://api.purpleair.com)!'
        )

    # load the response request json as a dictionary
    json_response = response.json()
    # load the data into a DataFrame with appropriately labelled columns
    df_sensors = pd.DataFrame(json_response['data'], columns = json_response['fields'])
    # write the sensor data to file
    df_sensors.to_csv('../data/chicago_sensors.csv')
