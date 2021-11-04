from datetime import datetime
from datetime import timedelta
import pandas as pd
import requests

def pull_airnow_sensor_data(
    api_key: str,
    start_date: str, 
    end_date: str, 
    measures: list=['OZONE','PM25','CO'],
    bbox: list=[-87.912584,41.587576,-87.522570,42.109292]
):
    '''
    Pulls all AirNow sensor data within the definied bounding box between
    the start and end dates defined.
    
    PARAMETERS
    ===
    api_key: str, personal AirNow API key
    start_date: str, defines the beginning of desired AirNow data.
        Format: Year-Month-Day, 2021-06-21
    end_date: str, defines the end of desired AirNow data.
        Format: Year-Month-Day, 2021-06-21
    measures: list-like, an iterable list of desired measures to pull
        from AirNow. Defaults are Ozone, PM 2.5, and Carbon Monoxide
    bbox: list-like, an iterable list of floats defining the bounding 
        box from which to grab AirNow data.
        
    OUTPUT
    ===
    sensor_data: pandas dataframe, contains all relevant AirNow data
    '''
    
    # convert measures to a string for API call
    PARAMS = ''.join([s+',' if s != measures[-1] else s for s in measures])
    
    # convert bbox to a string for API call
    BBOX_x=''.join([str(s)+',' if s != bbox[-1] else str(s) for s in bbox])

    # define query for API call
    query=(
        f"https://www.airnowapi.org/aq/data/?startDate={start_date}T02&endDate={end_date}" \
        f"T03&parameters={PARAMS}&BBOX={BBOX_x}&dataType=B&format=text/csv" \
        f"&verbose=0&nowcastonly=0&includerawconcentrations=0&API_KEY={api_key}"
    )
    
    # call API query into a pandas dataframe for processing
    sensor_data=pd.read_csv(
        query, 
        names=['Latitude','Longitude','DateTime','Parameter','Concentration','Unit','AQI','Category']
    )
    
    return sensor_data



def pull_purpleair_data(
    sensors: pd.DataFrame, 
    city: str, 
    neighborhood: str, 
    key: str
) -> pd.DataFrame:
    '''
    Get neighborhood-specific sensor data from PurpleAir
    '''
    # create list of sensor
    sensor_list = "|".join(
        sensors[
            (sensors.City == city)
            & (sensors.Neighborhood == neighborhood)
        ].SensorID.astype(str).tolist()
    )
    
    pa_query = f'https://www.purpleair.com/json?key={key}&show={sensor_list}'
    
    # pull data
    pa_request = requests.get(pa_query)
    json_data = pa_request.json()
    # read into dataframe
    pa_sensor_df = pd.DataFrame(json_data['results'])
    
    return pa_sensor_df



def pull_purpleair_historical(
    weeks_to_get: int,
    channel: str,
    key: str,
    col_names: dict,
    start_date: datetime = datetime.now(),
) -> pd.DataFrame:
        """
        Get data from the ThingSpeak API one week at a time up to weeks_to_get weeks in the past
        """

        to_week = start_date - timedelta(weeks=1)
        url = f'https://thingspeak.com/channels/{channel}/feed.csv?api_key={key}&offset=0&average=&round=2&start={to_week.strftime("%Y-%m-%d")}%2000:00:00&end={start_date.strftime("%Y-%m-%d")}%2000:00:00'
        weekly_data = pd.read_csv(url)
        if weeks_to_get > 1:
            for _ in range(weeks_to_get):
                start_date = to_week
                to_week = to_week - timedelta(weeks=1)
                url = f'https://thingspeak.com/channels/{channel}/feed.csv?api_key={key}&offset=0&average=&round=2&start={to_week.strftime("%Y-%m-%d")}%2000:00:00&end={start_date.strftime("%Y-%m-%d")}%2000:00:00'
                weekly_data = pd.concat([weekly_data, pd.read_csv(url)])

        # rename the columns
        weekly_data.rename(columns=col_names, inplace=True)
        weekly_data['created_at'] = pd.to_datetime(
            weekly_data['created_at'], format='%Y-%m-%d %H:%M:%S %Z')
        weekly_data.index = weekly_data.pop('entry_id')
        weekly_data['channel'] = channel
        
        return weekly_data