import requests
import json
import pandas as pd
from io import StringIO

api_key = ""
with open(f"backend/data/solcast_key.txt", "r") as f:
    api_key = f.read()

url = f"https://api.solcast.com.au/data/historic/radiation_and_weather?latitude=-33.86882&longitude=151.209295&azimuth=44&tilt=90&start=2022-10-25T14:45:00.000Z&duration=P1D&format=json&time_zone=utc&api_key={api_key}"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)
time_periods = {}
data = response.json()['estimated_actuals']
for item in data:
    if item['period_end'] not in time_periods:
        time_periods[item['period_end']] = item.copy()
        time_periods[item['period_end']].pop('period_end', None)

    print(item)

df = pd.json_normalize(data)
df.to_csv('backend/data/datasets/nsw_irradiance.csv', index=False)


