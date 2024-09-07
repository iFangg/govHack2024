import requests
import pandas as pd
import json
from io import StringIO

sites = []
sites_dict = {}
url = "https://data.airquality.nsw.gov.au/api/Data/get_SiteDetails"
response = requests.get(url)
if response.status_code == 200:
    data = response.json()  # Parse JSON response
    for site in data:
        if site['Site_Id'] not in sites:
            sites.append(site['Site_Id'])
            sites_dict[site['Site_Id']] = site['SiteName']
else:
    print(f"Error: {response.status_code}")

payload = {
    "Parameters": ["PM10", "PM2.5"],
    "Sites": sites,
    "StartDate": "2024-09-06",
    "EndDate": "2024-09-07",
    "Categories": ["Averages"],
    "SubCategories": ["Hourly", "Daily"],
    "Frequency": ["24h rolling average derived from 1h average"]
}
payload_json = json.dumps(payload)
url = 'https://data.airquality.nsw.gov.au/api/Data/get_Observations'
response = requests.post(url, json=payload_json)

df = pd.read_json(StringIO(response.text))
df['siteName'] = df.apply(lambda row:  sites_dict[row['Site_Id']], axis=1)
df.to_csv('backend/data/datasets/nsw_air_pollution.csv', index=False)

