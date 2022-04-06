#!/usr/bin/env python3

'''This script uses the new PurpleAir API (see api.purpleair.com) to get the
list of sensors in the Chicago area. More precisely, we get all the sensors in
the bounding box associated to the multipolygon representing the Chicago city
boundaries. We do not consider sensors that are flagged as 'inside'.

Note: PurpleAir requests that we refrain from more than 1 request every 1 to 10
minutes, and that when pulling data from multiple sensors, we do it in a single
request
.
'''

# TODO double check that the lat/long conventions are consistent, etc.

from datetime import datetime, timedelta
import geopandas as gpd
import numpy as np
import pandas as pd
import requests

# Chicago city boundary data
CHICAGO_BOUNDARIES_FILE = '../data/chicago.geojson'
# where we store the info of Chicago area PurpleAir sensors
CHICAGO_SENSORS_FILE = '../data/chicago_sensors.csv'
# where we store the actual PM2.5 data to be analyzed
CHICAGO_DATA_FILE = '../data/chicago_data.csv'

def get_chicago_bounding_box() -> list[float]:
    '''
    Reads Chicago city boundaries from file and returns a bounding box that
    contains these boundaries.

    OUTPUT
    ===
    bounding_box: list-like, an iterable list of floats [minx, miny, maxx, maxy]
        defining the bounding box.

    '''
    df = gpd.read_file(CHICAGO_BOUNDARIES_FILE)
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
    df_sensors = pd.DataFrame(
        json_response['data'],
        columns = json_response['fields']
    )
    # write the sensor data to file
    df_sensors.to_csv(CHICAGO_SENSORS_FILE)

def get_chicago_historical_one_day(
        date: datetime = datetime.now()
):
    '''
    TODO documentation here
    '''

    # load Chicago area PurpleAir sensors
    df_sensors = pd.read_csv(CHICAGO_SENSORS_FILE)

    # get data starting one week ago
    start_date = date - timedelta(days = 1)

    # store all the data in a dataframe
    df_data = pd.DataFrame()

    # loop through each sensor, which has an a and a b channel
    for i, row in df_sensors.iterrows():
        # loop through each channel
        for ch in ['a', 'b']:

            print(f'processing {row["sensor_index"]}#{ch}')

            # construct the API query
            request = (
                f'https://thingspeak.com/channels/{row[f"primary_id_{ch}"]}'
                f'/feed.csv?api_key={row[f"primary_key_{ch}"]}&'
                f'start={start_date.strftime("%Y-%m-%d")}%2000:00:00&'
                f'end={date.strftime("%Y-%m-%d")}%2000:00:00'
            )

            # request the API
            df_iter = pd.read_csv(request)
            # label the data with its sensorID, channel,
            # latitude, longitude, and human-readable name
            df_iter['sensorID'] = row['sensor_index']
            df_iter['channel'] = ch
            df_iter['latitude'] = row['latitude']
            df_iter['longitude'] = row['longitude']
            df_iter['name'] = row['name']

            # accumulate
            df_data = df_data.append(df_iter)

    # we keep only the PM2.5 (CF = 1), temperature, and relative humidity data
    # note that fields 6 and 7 are not the desired quantities in channel b
    # see https://docs.google.com/document/d/15ijz94dXJ-YAZLi9iZ_RaBwrZ4KtYeCy08goGBwnbCU/
    df_data = df_data.rename(columns = {
        'created_at': 'datetime',
        'field2': 'pm25',
        'field6': 'temp',
        'field7': 'rh'
    })

    # keep only the quantities of interest
    df_data = df_data[
        ['sensorID',
         'latitude',
         'longitude',
         'name',
         'channel',
         'datetime',
         'pm25',
         'temp',
         'rh']
    ]
    df_data.reset_index(inplace = True, drop = True)

    # write the accumulated data to file
    df_data.to_csv(CHICAGO_DATA_FILE)
