# AirNow API

## Summary
- AirNow supplies data on air quality
- We are using the API to download data on air quality into CSV format
- We will use 7 or 8 parameters
- API Key is required
- Updated: 9/14/2021, WIP: Yes

## Objective
- To use the AirNow API to download data on air pollutants and find a truth source for "air quality"
- Air quality is a weighted average of six measures defined as "AQI" or Air Quality Index by the Environmental Protection Agency (EPA)
- The 6 variables are required for AQI are: 
    - Ozone (O3)
    - PM2.5 (pm25)
    - PM10 (pm10)
    - CO (co)
    - NO2 (no2)
    - SO2 (so2)

## Parameters of interest
- bbox : This should be Chicago area list [-87.912584,41.587576,-87.522570,42.109292] 
- startdate : UTC/DateTime, TBD
- enddate : UTC/DateTime, TBD 
- parameters: list [ozone, pm25, pm10, co, no2, so2]
- datatype: Char 'a' (A refers to AQI)
- format: Text 'application/json' OR 'text/csv'
- api_key: Text "YourApiKey"


## Outputs
CSV

## Example URL Endpoint
https://airnowapi.org/aq/data/?startdate=2014-09-23t22&enddate=2014-09-23t23&parameters=o3,pm25&bbox=-90.806632,24.634217,-71.119132,45.910790&datatype=a&format=text/csv&api_key=[YOUR-API-KEY]

## More on AQI
https://docs.airnowapi.org/aq101
