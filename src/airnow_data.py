'''
Description: Script to pull data from the AirNow API
Author: Rahul Goel

Code for Chicago

9/22/2021
'''

# Import dependencies
import pandas as pd 
import requests
import json

# Parameters on date, time, params, area, format and API Key
START_DATE = '2021-09-21'
START_HOUR = '22'
END_DATE = '2021-09-22' # Note that there is a query limit
END_HOUR = '23'
PARAMS = 'o3,pm25'
BBOX = '-90.806632,24.634217,-71.119132,45.910790'
DATATYPE = 'a'
FORMAT = 'application/json'
API_KEY = 'YOUR_AIRNOW_API_KEY'
SAVE_FILE = True ### Set to False if debugging & no need to save data as .json

# Construct URL
url = '''https://airnowapi.org/aq/data/?startdate='''+START_DATE+'''t'''+START_HOUR+\
	  '''&enddate='''+END_DATE+'''t'''+END_HOUR+'''&parameters='''+PARAMS+'''&bbox='''+BBOX+\
	  '''&datatype='''+DATATYPE+'''&format='''+FORMAT+'''&api_key='''+API_KEY

# Request the URL
print(f"Getting data from {url}")
res = requests.get(url)

# Use JSON
data = res.json()

# If Save file is true...
if(SAVE_FILE == True):
	# Dump into file
	with open('airnow.json', 'w') as f:
		json.dump(data, f)

# Save the data
print("Done! 👍 ")
