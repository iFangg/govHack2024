import os
import requests
import json
import pandas as pd
from datetime import datetime, timedelta


# def fetch_irradiance_data(path: str='backend/data/datasets/', output_csv: str='nsw_irradiance.csv') -> bool:
#     """
#     Save the average Direct Normal Irradiance (DNI) irradiance data for each suburb in NSW and save the results in <output_csv>.
#     Data source: Solcast - [ https://docs.solcast.com.au/ ].
#     """

#     # Get API key
#     try:
#         api_key = os.environ.get('SOLCAST_API_KEY')
#     except KeyError:
#         print("Error: Please set the environment variable SOLCAST_API_KEY")
#         return False

#     # Fetch suburb data
#     suburbs = fetch_nsw_suburbs(path + 'lga_coordinates.csv')
#     if suburbs is None:
#         print("Error: Unable to fetch NSW suburbs")
#         return False

#     suburb_irradiance = []

#     # Initialise date time variables
#     total_time_years = 1
#     items_count = 0
#     duration_days = 31
#     duration = f'P{duration_days}D'
#     period = 'PT1H'
#     current_date = datetime.now()
#     end = current_date.replace(year=current_date.year - total_time_years)

#     headers = {'Accept': 'application/json'}

#     for suburb in suburbs:
#         irradiance_sum = 0

#         start = current_date - timedelta(days=duration_days + 1)
#         while start >= end:
#             url = f"https://api.solcast.com.au/data/historic/radiation_and_weather?latitude={suburbs[suburb]['lat']}&longitude={suburbs[suburb]['lon']}&start={start}&period={period}&duration={duration}&api_key={api_key}"
#             response = requests.request("GET", url, headers=headers)

#             if response.status_code != 200:
#                 print(f"Error: {response.status_code}, {response.text}")
#                 return False

#             data = response.json()['estimated_actuals']
#             for item in data:
#                 irradiance_sum += item['dni']
#                 items_count += 1

#             start -= timedelta(days=duration_days)


#         suburb_irradiance.append((suburb['name'], irradiance_sum / items_count if items_count > 0 else 0))

#     irradiance_df = pd.DataFrame(suburb_irradiance, columns=['Suburb', 'Irradiance'])
#     output_path = os.path.join(path, output_csv)
#     irradiance_df.to_csv(output_path, index=False)

#     return True


def fetch_nsw_suburbs(output_csv_path: str):
    """
    Get coordinates of all NSW suburbs
    """

    url = 'https://data.peclet.com.au/api/explore/v2.1/catalog/datasets/nsw-lga-boundaries/exports/json?lang=en&timezone=Australia%2FSydney'
    response = requests.get(url)
    data = response.json()

    lga_list = {}

    for item in data:
        lga = item['lga_name']
        lga = lga.strip(' Council')

        if lga not in lga_list:
            lga_list[lga] = item['geo_point_2d']

    # df = pd.DataFrame(lga_list).transpose()
    df = pd.DataFrame.from_dict(lga_list, orient='index')
    print(df.head(10))
    df.to_csv(output_csv_path, index=True)

    return lga_list


fetch_nsw_suburbs('backend/data/datasets/lga_coordinates.csv')
