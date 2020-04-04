import configparser
import requests
import os
import pandas as pd


config = configparser.ConfigParser()
config.read("../config.ini")
DATA_FOLDER = DATA_FOLDER =  os.path.dirname(os.getcwd()) + '/data/'

def temperature_data(station_code):

    api_key = config['aemet']['api_key']
    base_url = 'https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/2020-01-01T00%3A00%3A00UTC/fechafin/2020-04-03T00%3A00%3A00UTC/estacion/{}'.format(station_code)

    params = {
        'api_key': api_key
    }
    headers = {
        'cache-control': "no-cache"
    }

    response = requests.request('GET', base_url, params=params, headers=headers)

    response_url = response.json()['datos']

    data = requests.request('GET', response_url)
    
    results = {}
    for value in data.json():
        results[value['fecha']] = float(value['tmed'].replace(',','.'))

    return results 

def get_stations(provincia):
    api_key = config['aemet']['api_key']
    base_url = 'https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones'

    params = {
        'api_key': api_key
    }
    headers = {
        'cache-control': "no-cache"
    }

    response = requests.request('GET', base_url, params=params, headers=headers)

    response_url = response.json()['datos']

    data = requests.request('GET', response_url)

    results = [result for result in data.json() if result['provincia'] == provincia]
    
    return results, results[0]['indicativo']

def read_weather_csv(filename):
    fname = DATA_FOLDER + filename

    df = pd.read_csv(fname)

    tavg = df['TAVG'].to_numpy()
    dates = df['DATE']

    # Fahrenhei a celsius
    tavg_celsius = [round(((t - 32) * 5)/9,2) for t in tavg]

    results = {}
    for i in range(len(dates)):
        results[dates[i]] = tavg_celsius[i]

    return results

if __name__ == "__main__":
    """all_stations, code = get_stations(provincia = 'CADIZ')
    r = temperature_data(station_code = code)
    print(r)"""
    r = read_weather_csv('korea.csv')
    print(r)