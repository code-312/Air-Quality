import pandas as pd

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