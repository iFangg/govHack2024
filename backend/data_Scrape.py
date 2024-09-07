import requests
import os
import json
import subprocess

## Climate Data Cube Yearly Slices of Observations
dust_particles = []
sites = []
url = "https://data.airquality.nsw.gov.au/api/Data/get_SiteDetails"
response = requests.get(url)
if response.status_code == 200:
    data = response.json()  # Parse JSON response
    for site in data:
        print(f"{site['Site_Id']}, {site['SiteName']}")
        sites.append(site['Site_Id']) if site['Site_Id'] not in sites else None
else:
    print(f"Error: {response.status_code}")

print()

data = {
    "Parameters": ["PM10", "PM2.5"],
    "Sites": sites,
    "StartDate": "2024-09-06",
    "EndDate": "2024-09-07",
    "Categories": ["Averages"],
    "SubCategories": ["Hourly", "Daily"],
    "Frequency": ["24h rolling average derived from 1h average"]
}

# Convert the Python dictionary to a JSON string
json_data = json.dumps(data)

# Use subprocess.run to make the POST request
result = subprocess.run([
    'curl', '-X', 'POST', 'https://data.airquality.nsw.gov.au/api/Data/get_Observations',
    '-H', 'accept: application/json',
    '-H', 'Content-Type: application/json',
    '-d', json_data
], capture_output=True, text=True)

# Print the result (standard output)
# print(result.stdout)
print(type(result.stdout))
data = json.loads(result.stdout)

if isinstance(data, list):
    for item in data:
        params = item['Parameter']
        print(f"{item['Site_Id']}: {params['HourDescription']}, {params['Value']}")

