# Purple Air / Thingspeak API

## Summary
- PurpleAir supplies data on air quality through Thingspeak API
- We are using the API to download data on air quality into JSON or CSV format
- We will use 7 or 8 parameters
- Thingspeak API Key is used, which is publicly available
- Help: contact@purpleair.com
- Updated: 10/27/2021, WIP: Yes

## Objective
- To use the PurpleAir's thingspeak API to download local sensor-based data on air pollutants 
- Timeline: a 3 week dataset in the summer (1st-20th July 2021) and one 3 week dataset in the winter  (1st - 20th Jan 2021)
- Air quality is a weighted average of six measures defined as "AQI" or Air Quality Index by the Environmental Protection Agency (EPA)
- The 6 variables are required for AQI are: 
-- Ozone (O3)
-- PM2.5 (pm25)
-- PM10 (pm10)
-- CO (co)
-- NO2 (no2)
-- SO2 (so2)

## Parameters of interest
- Sensor number
- Start

## Example URL
https://api.thingspeak.com/channels/1405377/fields/2.json?start=2021-09-07%2017:42:02&offset=0&round=2&average=10&api_key=<API KEY>

## Outputs
CSV or JSON

# More on Thingspeak
https://github.com/philiporlando/purpleair_thingspeak
