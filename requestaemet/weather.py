import configparser
import requests
import os
import pandas as pd
import numpy as np
import json
import sys
config = configparser.ConfigParser()
config.read("../config.ini")
DATA_FOLDER = DATA_FOLDER =  os.path.dirname(os.getcwd()) + '/data/'
def main(argv): 
   forecastindays(argv)

def forecastindays(zipcode):
    api_key = "13322246a8ad4613a0ca2608f8942168"
    base_url = 'https://api.weatherbit.io/v2.0/forecast/daily'
    zipcode = zipcode

    params = {
        'postal_code': zipcode,
        'country': 'ES',
        'days':'7',
        'lang':'es',
        'key':api_key                
    }
    headers = {
        'cache-control': "no-cache"
    }

    response = requests.request('GET', base_url, params=params, headers=headers)
    forecast = response.json()   
    tempArray = []
    for data in forecast['data']:
        tempArray.append(data['temp'])             
        
    print(tempArray)
        
def get_municipios():
    api_key = config['aemet']['api_key']
    base_url = 'https://opendata.aemet.es/opendata/api/maestro/municipios'

    params = {
        'api_key': api_key
    }
    headers = {
        'cache-control': "no-cache"
    }

    response = requests.request('GET', base_url, params=params, headers=headers)
    municipios = response.json()   

    for municipio in municipios:
        if "id28" in municipio['id']:
            print(municipio['id'])
        else:
            pass


    
def temperature_data(name):
    r, station_code = get_stations(provincia = name.upper())

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
    
    simple_results = np.array([float(value['tmed'].replace(',','.')) for value in data.json()])

    results = {}
    for value in data.json():
        results[value['fecha']] = float(value['tmed'].replace(',','.'))

    return results, simple_results

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
    simple_results = np.array(tavg_celsius)

    results = {}
    for i in range(len(dates)):
        results[dates[i]] = tavg_celsius[i]

    return results, simple_results

if __name__ == "__main__":
    main(sys.argv[1:])