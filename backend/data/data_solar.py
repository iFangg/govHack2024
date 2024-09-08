import os
import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_irradiance_data(path: str='backend/data/datasets/', output_csv: str='nsw_irradiance.csv') -> bool:
    """
    Save the average Direct Normal Irradiance (DNI) irradiance data for each suburb in NSW and save the results in <output_csv>.
    Data source: Solcast - [ https://docs.solcast.com.au/ ].
    """

    # Get API key
    try:
        api_key = os.environ.get('SOLCAST_API_KEY')
    except KeyError:
        print("Error: Please set the environment variable SOLCAST_API_KEY")
        return False

    # Fetch suburb data
    suburbs = fetch_nsw_suburbs()
    if suburbs is None:
        print("Error: Unable to fetch NSW suburbs")
        return False

    suburb_irradiance = []

    # Initialise date time variables
    total_time_years = 1
    items_count = 0
    duration_days = 31
    duration = f'P{duration_days}D'
    period = 'PT1H'
    current_date = datetime.now()
    end = current_date.replace(year=current_date.year - total_time_years)

    headers = {'Accept': 'application/json'}

    for suburb in suburbs:
        irradiance_sum = 0

        start = current_date - timedelta(days=duration_days + 1)
        while start >= end:
            url = f"https://api.solcast.com.au/data/historic/radiation_and_weather?latitude={suburb['latitude']}&longitude={suburb['longitude']}&start={start}&period={period}&duration={duration}&api_key={api_key}"
            response = requests.request("GET", url, headers=headers)

            if response.status_code != 200:
                print(f"Error: {response.status_code}, {response.text}")
                return False

            data = response.json()['estimated_actuals']
            for item in data:
                irradiance_sum += item['dni']
                items_count += 1

            start -= timedelta(days=duration_days)

        suburb_irradiance.append((suburb['name'], irradiance_sum / items_count if items_count > 0 else 0))

    irradiance_df = pd.DataFrame(suburb_irradiance, columns=['Suburb', 'Irradiance'])
    output_path = os.path.join(path, output_csv)
    irradiance_df.to_csv(output_path, index=False)

    return True


def fetch_nsw_suburbs():
    """
    Get coordinates of all NSW suburbs using Postcode API - [ https://postcodeapi.com.au/ ]
    """

    url = 'https://v0.postcodeapi.com.au/suburbs?state=NSW'
    headers = {'Accept': 'application/json'}

    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


fetch_irradiance_data()