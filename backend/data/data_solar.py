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

    # Initialise date time variables
    duration_days = 31
    duration = f'P{duration_days}D'
    period = 'PT1H'
    current_date = datetime.now()

    headers = {'Accept': 'application/json'}

    lga_irradiance = {}
    lga_df = pd.read_csv('backend/data/datasets/lga_coordinates.csv')

    for _, row in lga_df.iterrows():
        lga_irradiance[row['lga_name']] = 0

    for _,row in lga_df.iterrows():
        lga_name = row['lga_name']
        lga_lon = row['lon']
        lga_lat = row['lat']

        start = current_date - timedelta(days=duration_days + 1)
        url = f"https://api.solcast.com.au/data/historic/radiation_and_weather?latitude={lga_lat}&longitude={lga_lon}&start={start}&period={period}&duration={duration}&api_key={api_key}"
        response = requests.request("GET", url, headers=headers)

        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            return False

        data = response.json()['estimated_actuals']
        for item in data:
            irradiance_sum += item['dni']
        items_count = len(data)

        lga_irradiance[lga_name] = (irradiance_sum / items_count if items_count > 0 else 0)

    irradiance_df = pd.DataFrame(lga_irradiance, columns=['LGA', 'Irradiance'])
    output_path = os.path.join(path, output_csv)
    irradiance_df.to_csv(output_path, index=False)

    return True


def fetch_nsw_suburbs(output_csv_path: str):
    """
    Get coordinates of all NSW suburbs
    """

    url = 'https://data.peclet.com.au/api/explore/v2.1/catalog/datasets/nsw-lga-boundaries/exports/json?lang=en&timezone=Australia%2FSydney'
    response = requests.get(url)
    data = response.json()

    lga_list = {}

    for item in data:
        lga = item['abb_name']
        if lga not in lga_list:
            lga_list[lga] = item['geo_point_2d']

    df = pd.DataFrame.from_dict(lga_list, orient='index')
    df['lga_name'] = df.index
    df.to_csv(output_csv_path, index=False)

    return lga_list


fetch_nsw_suburbs('backend/data/datasets/lga_coordinates.csv')
# fetch_irradiance_data()
