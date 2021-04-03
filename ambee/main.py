#!/usr/bin/env python
# A simple script to fetch information from the ambee api.
import json
import os

import requests


def get_long_lat(city):
    """Longitude and latitude of target city.

    inputs:
        city - name of city to recover coordinates of

    returns
        longitude and latitude as strings
    """
    cities = {
        "victoria": {
            "longitude": "-123.329773",
            "latitude": "48.407326"
        },
        "vernon": {
            "longitude": "-119.276505",
            "latitude": "50.271790"
        }
    }
    if city not in cities.keys():
        raise Exception("city not found")
    longitude = cities[city]["longitude"]
    latitude = cities[city]["latitude"]
    return longitude, latitude


def get_ambee_historical_data(city, data_type, from_date=None, to_date=None):  
    """Get json response from ambee.

    inputs:
        city - name of city to recover data for
        data_type - type of data to recover (pollen/air/weather)
        from_date - format: (YYYY-MM-DD HH:mm:ss) if provided then historical data is recovered, to_date required if from_date is provided
        to_date - format: (YYYY-MM-DD HH:mm:ss)if provided then historical data is recovered, from_date required if to_date is provided

    returns
        dictionary response from ambee
    """
    ambee_base_url = "https://api.ambeedata.com"
    ambee_api_key = os.environ['AMBEE_API_KEY']
    date_range = ""
    time_frame = "latest"

    longitude, latitude = get_long_lat(city)
    if from_date:
        if not to_date:
            raise Exception("to_date required when from_date provided")
    if to_date:
        if not from_date:
            raise Exception("from_date required when to_date provided")
        date_range = f"&from={from_date}&to={to_date}"
        time_frame = "history"

    if data_type == "air":
        ambee_api_key = os.environ['AIR_API_KEY']
        ambee_url = f"{ambee_base_url}/{time_frame}/by-lat-lng?lat={latitude}&lng={longitude}{date_range}"
    elif data_type == "weather":
        ambee_api_key = os.environ['WEATHER_API_KEY']
        ambee_url = f"{ambee_base_url}/{data_type}/{time_frame}/by-lat-lng?lat={latitude}&lng={longitude}{date_range}"
    elif data_type == "pollen":
        ambee_api_key = os.environ['AIR_API_KEY']
        ambee_url = f"{ambee_base_url}/{time_frame}/{data_type}/by-lat-lng?lat={latitude}&lng={longitude}{date_range}"
    else:
        raise Exception(f"unknown data_type ({data_type})")

    headers = {
        "x-api-key": ambee_api_key,
        "Content-type": "application/json"
    }

    response = requests.get(f"{ambee_url}", headers=headers)
    response.raise_for_status()
    return response.json()


def get_ambee_latest_data(city, data_type, from_date=None, to_date=None):
    """Get json response from ambee.

    inputs:
        city - name of city to recover data for
        data_type - type of data to recover (pollen/air/weather)
        from_date - format: (YYYY-MM-DD HH:mm:ss) if provided then historical data is recovered, to_date required if from_date is provided
        to_date - format: (YYYY-MM-DD HH:mm:ss)if provided then historical data is recovered, from_date required if to_date is provided

    returns
        dictionary response from ambee
    """
    ambee_base_url = "https://api.ambeedata.com"
    ambee_api_key = os.environ['AMBEE_API_KEY']
    date_range = ""
    time_frame = "latest"

    longitude, latitude = get_long_lat(city)
    if from_date:
        if not to_date:
            raise Exception("to_date required when from_date provided")
    if to_date:
        if not from_date:
            raise Exception("from_date required when to_date provided")
        date_range = f"&from={from_date}&to={to_date}"
        time_frame = "history"
    if data_type == "air":
        ambee_url = f"{ambee_base_url}/{time_frame}/by-lat-lng?lat={latitude}&lng={longitude}{date_range}"
    elif data_type == "weather":
        ambee_url = f"{ambee_base_url}/{data_type}/{time_frame}/by-lat-lng?lat={latitude}&lng={longitude}{date_range}"
    elif data_type == "pollen":
        ambee_url = f"{ambee_base_url}/{time_frame}/{data_type}/by-lat-lng?lat={latitude}&lng={longitude}{date_range}"
    elif data_type == "fire":  # doesn't support history
        ambee_url = f"{ambee_base_url}/latest/{data_type}?lat={latitude}&lng={longitude}"
    else:
        raise Exception(f"unknown data_type ({data_type})")

    headers = {
        "x-api-key": ambee_api_key,
        "Content-type": "application/json"
    }
    response = requests.get(f"{ambee_url}", headers=headers)
    response.raise_for_status()
    return response.json()


city = "victoria"
data_types = ["air", "pollen", "weather"]
time_ranges = [("2021-03-30 00:00:00", "2021-04-02 23:59:59")]
for time_range in time_ranges:
    for data_type in data_types:
        ambee_data = get_ambee_historical_data(city, data_type, time_range[0], time_range[1])
        with open(f"{data_type}-{time_range[0].split(' ')[0]}to{time_range[1].split(' ')[0]}.json", 'w') as outfile:
            json.dump(ambee_data, outfile)
